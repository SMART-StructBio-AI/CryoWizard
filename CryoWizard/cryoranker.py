#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import subprocess
import shutil
import datetime
import time
import os

import sys
sys.path.append(os.path.dirname(__file__))

import cryowizardlib.CSLogin as CSLogin
import cryowizardlib.JobAPIs as JobAPIs
import cryowizardlib.Toolbox as toolbox



def plot_particle_num_score_curve(cryoranker_job, scores, parameters_folder_name):
    scores_list = []
    for particle_uid, score in scores.items():
        scores_list.append(score)
    sorted_scores_list = sorted(scores_list, reverse=True)
    particle_num_list = [(int)(particle_num_ptr + 1) for particle_num_ptr in range(len(sorted_scores_list))]
    plt.clf()
    plt.ioff()
    plt.plot(particle_num_list, sorted_scores_list)
    plt.xlabel('Particle number')
    plt.ylabel('Score')
    plt.title('ParticleNumber-Score curve (' + parameters_folder_name + ')')
    cryoranker_job.log_plot(plt, 'Plot ParticleNumber-Score curve (' + parameters_folder_name + ')')


def combine_particles_to_single_restack_particles_job(cryowizardjob, cryowizardlog, project_dir, parameters_folder_name):
    filedir = os.path.normpath(os.path.dirname(__file__))
    globaldir = os.path.normpath(project_dir)
    parametersdir = os.path.join(globaldir, 'parameters', 'cryoranker', parameters_folder_name)
    metadatadir = os.path.join(globaldir, 'metadata', 'cryoranker', parameters_folder_name)

    # initialize
    if not os.path.exists(metadatadir):
        os.makedirs(metadatadir)
    parameters = toolbox.readjson(os.path.join(globaldir, 'parameters', 'base_parameters', 'parameters.json'))
    cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(email=parameters['cryosparc_username'], password=parameters['cryosparc_password'])
    dealjobs = JobAPIs.DealJobs(cshandle, parameters['project'], parameters['workspace'], parameters['lane'])

    source_job_id_name_list = toolbox.readjson(os.path.join(parametersdir, 'source_particle_job_uid.json'))['source_job_uid']
    source_job_id = JobAPIs.resolve_source_job_uids(globaldir, source_job_id_name_list, 'particle')

    # build jobs
    restack_particles_class = JobAPIs.CreateRestackParticles(dealjobs)
    restack_particles_parameters = toolbox.readjson(os.path.join(parametersdir, 'restack_particles_parameters.json'))

    created_jobs_info = []
    restack_particles_job = restack_particles_class.QueueRestackJob(restack_particles_parameters, JobAPIs.extract_source_job_ids(source_job_id), dealjobs.GetCryoSPARCJobListOutputNames(source_job_id, 'particle'))
    created_jobs_info.append(JobAPIs.create_created_jobs_info_item(restack_particles_job.uid, parents=source_job_id))
    JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Restack Particles job created: ' + restack_particles_job.uid)
    toolbox.savetojson(created_jobs_info, os.path.join(metadatadir, 'created_jobs_info.json'), False)


def cryoranker_get_score(cryowizardjob, cryowizardlog, project_dir, parameters_folder_name):
    filedir = os.path.normpath(os.path.dirname(__file__))
    globaldir = os.path.normpath(project_dir)
    metadatadir = os.path.join(globaldir, 'metadata', 'cryoranker', parameters_folder_name)

    # initialize
    if not os.path.exists(metadatadir):
        os.makedirs(metadatadir)
    parameters = toolbox.readjson(os.path.join(globaldir, 'parameters', 'base_parameters', 'parameters.json'))
    cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(email=parameters['cryosparc_username'], password=parameters['cryosparc_password'])
    dealjobs = JobAPIs.DealJobs(cshandle, parameters['project'], parameters['workspace'], parameters['lane'])

    if not os.path.exists(os.path.join(metadatadir, 'created_jobs_info.json')):
        combine_particles_to_single_restack_particles_job(cryowizardjob, cryowizardlog, project_dir, parameters_folder_name)
    created_jobs_info = toolbox.readjson(os.path.join(metadatadir, 'created_jobs_info.json'))
    JobAPIs.run_all_created_jobs(dealjobs, parameters, created_jobs_info)
    restack_particles_jobuid = created_jobs_info[0]['jobuid']

    project = dealjobs.cshandle.find_project(dealjobs.project)
    if os.path.exists(os.path.join(metadatadir, 'created_cryoranker_jobs_info.json')):
        created_cryoranker_jobs_info = toolbox.readjson(os.path.join(metadatadir, 'created_cryoranker_jobs_info.json'))
        cryoranker_job = project.find_external_job(created_cryoranker_jobs_info[0]['jobuid'])
        if not (cryoranker_job.status in ['building']):
            if cryoranker_job.status in ['launched', 'started', 'running', 'waiting']:
                cryoranker_job.kill()
            try:
                cryoranker_job.clear()
                cryoranker_job.wait_for_status('building', 5)
            except:
                pass
    else:
        cryoranker_job = project.create_external_job(dealjobs.workspace, title='CryoRanker')
        created_cryoranker_jobs_info = [JobAPIs.create_created_cryoranker_jobs_info_item(cryoranker_job.uid, parents=[restack_particles_jobuid + '_particles'])]
        toolbox.savetojson(created_cryoranker_jobs_info, os.path.join(metadatadir, 'created_cryoranker_jobs_info.json'), False)

    add_input_name = 'input_particles'
    cryoranker_job.add_input(type='particle', name=add_input_name, min=1, slots=['blob', 'ctf'], title='Input Particle')
    cryoranker_job.connect(target_input=add_input_name, source_job_uid=restack_particles_jobuid, source_output='particles')

    # run
    JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Start to run cryoranker: ' + cryoranker_job.uid)
    cryorankertimebegin = datetime.datetime.now()
    with cryoranker_job.run():
        input_particles_dataset = cryoranker_job.load_input(name=add_input_name)
        if os.path.exists(os.path.join(metadatadir, 'GetScore.sh')):
            os.remove(os.path.join(metadatadir, 'GetScore.sh'))
        if os.path.exists(os.path.join(metadatadir, 'GetScore.out')):
            os.remove(os.path.join(metadatadir, 'GetScore.out'))
        usable_port = toolbox.scanusableport([_ for _ in range(parameters['accelerate_port_start'], parameters['accelerate_port_end'])])
        with open(os.path.join(metadatadir, 'GetScore.sh'), 'a') as f:
            f.write('#!/bin/bash\n')
            if parameters['inference_gpu_ids'] is not None:
                f.write('export CUDA_VISIBLE_DEVICES=\'' + parameters['inference_gpu_ids'] + '\'\n')
            f.write('cd ' + metadatadir + '\n')
            f.write('accelerate launch  --mixed_precision=bf16 --main_process_port=' + (str)(usable_port) + ' ' + os.path.join(filedir, 'cryoranker_getscores.py') + '\n')
        cryoranker_job.subprocess(('bash ' + os.path.join(metadatadir, 'GetScore.sh')).split(' '), mute=True)

        if os.path.exists(os.path.join(metadatadir, 'scores.json')):
            output_groups = JobAPIs.create_output_groups(particle=[cryoranker_job.uid + '_particles'], ranker=[cryoranker_job.uid + '_particles'])
            toolbox.savetojson(output_groups, os.path.join(metadatadir, 'output_groups.json'), False)

            scores = toolbox.readjson(os.path.join(metadatadir, 'scores.json'))
            plot_particle_num_score_curve(cryoranker_job, scores, parameters_folder_name)

            output_particles_dataset = input_particles_dataset
            add_output_name = 'particles'
            cryoranker_job.add_output(type='particle', name=add_output_name, slots=['blob'], passthrough=add_input_name)
            cryoranker_job.save_output(add_output_name, output_particles_dataset)

    if not os.path.exists(os.path.join(metadatadir, 'scores.json')):
        cryoranker_job.stop(error=True)
    else:
        shutil.copy(os.path.join(metadatadir, 'scores.json'), os.path.join(dealjobs.GetProjectPath(), cryoranker_job.uid, 'scores.json'))

    cryorankertimeend = datetime.datetime.now()
    JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'CryoRanker finished! Time spent: ' + (str)(cryorankertimeend - cryorankertimebegin))


def cryoranker_get_score_slurm(cryowizardjob, cryowizardlog, project_dir, parameters_folder_name):
    def get_slurm_output(cryoranker_job, output_file_path, slurm_job_uid, temp_file_save_dir):
        def read_and_log(file_path, job):
            command_process = subprocess.Popen('tail -f ' + file_path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            while True:
                line = ''
                single_character = command_process.stdout.read(1)
                while not ((single_character == '\r') or (single_character == '\n')):
                    line += single_character
                    single_character = command_process.stdout.read(1)
                line = line.rstrip()
                if (line == '[getscore_slurm_script_done]'):
                    break
                if (len(line) > 0):
                    job.log(line)
        while True:
            if os.path.exists(output_file_path):
                break
            else:
                time.sleep(5)
        multithreadpool = toolbox.MultiThreadingRun(1)
        multithreadpool.setthread(read_and_log, file_path=output_file_path, job=cryoranker_job)
        while True:
            if not toolbox.checkifslurmjobinqueue(slurm_job_uid, temp_file_save_dir):
                with open(output_file_path, 'a') as f:
                    f.write('\n[getscore_slurm_script_done]\n')
                break
            else:
                time.sleep(5)

    filedir = os.path.normpath(os.path.dirname(__file__))
    globaldir = os.path.normpath(project_dir)
    metadatadir = os.path.join(globaldir, 'metadata', 'cryoranker', parameters_folder_name)

    # initialize
    if not os.path.exists(metadatadir):
        os.makedirs(metadatadir)
    parameters = toolbox.readjson(os.path.join(globaldir, 'parameters', 'base_parameters', 'parameters.json'))
    cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(email=parameters['cryosparc_username'], password=parameters['cryosparc_password'])
    dealjobs = JobAPIs.DealJobs(cshandle, parameters['project'], parameters['workspace'], parameters['lane'])

    if not os.path.exists(os.path.join(metadatadir, 'created_jobs_info.json')):
        combine_particles_to_single_restack_particles_job(cryowizardjob, cryowizardlog, project_dir, parameters_folder_name)
    created_jobs_info = toolbox.readjson(os.path.join(metadatadir, 'created_jobs_info.json'))
    JobAPIs.run_all_created_jobs(dealjobs, parameters, created_jobs_info)
    restack_particles_jobuid = created_jobs_info[0]['jobuid']

    project = dealjobs.cshandle.find_project(dealjobs.project)
    if os.path.exists(os.path.join(metadatadir, 'created_cryoranker_jobs_info.json')):
        created_cryoranker_jobs_info = toolbox.readjson(os.path.join(metadatadir, 'created_cryoranker_jobs_info.json'))
        cryoranker_job = project.find_external_job(created_cryoranker_jobs_info[0]['jobuid'])
        if not (cryoranker_job.status in ['building']):
            if cryoranker_job.status in ['launched', 'started', 'running', 'waiting']:
                cryoranker_job.kill()
            try:
                cryoranker_job.clear()
                cryoranker_job.wait_for_status('building', 5)
            except:
                pass
    else:
        cryoranker_job = project.create_external_job(dealjobs.workspace, title='CryoRanker')
        created_cryoranker_jobs_info = [JobAPIs.create_created_cryoranker_jobs_info_item(cryoranker_job.uid, parents=[restack_particles_jobuid + '_particles'])]
        toolbox.savetojson(created_cryoranker_jobs_info, os.path.join(metadatadir, 'created_cryoranker_jobs_info.json'), False)

    add_input_name = 'input_particles'
    cryoranker_job.add_input(type='particle', name=add_input_name, min=1, slots=['blob', 'ctf'], title='Input Particle')
    cryoranker_job.connect(target_input=add_input_name, source_job_uid=restack_particles_jobuid, source_output='particles')

    # run
    JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Start to run cryoranker: ' + cryoranker_job.uid)
    cryorankertimebegin = datetime.datetime.now()
    with cryoranker_job.run():
        input_particles_dataset = cryoranker_job.load_input(name=add_input_name)
        if os.path.exists(os.path.join(metadatadir, 'GetScore.sh')):
            os.remove(os.path.join(metadatadir, 'GetScore.sh'))
        if os.path.exists(os.path.join(metadatadir, 'GetScore.out')):
            os.remove(os.path.join(metadatadir, 'GetScore.out'))
        with open(os.path.join(globaldir, 'parameters', 'base_parameters', 'SlurmHeader.sh'), 'r') as source_f:
            source_f_data = source_f.readlines()
            with open(os.path.join(metadatadir, 'GetScore.sh'), 'a') as f:
                for source_single_line in source_f_data:
                    f.write(source_single_line.strip() + '\n')
                f.write('#SBATCH -o GetScore.out\n')
                f.write('#SBATCH -e GetScore.out\n')
                if parameters['inference_gpu_ids'] is not None:
                    f.write('export CUDA_VISIBLE_DEVICES=\'' + parameters['inference_gpu_ids'] + '\'\n')
                f.write('cd ' + metadatadir + '\n')
                f.write('srun accelerate launch  --mixed_precision=bf16 ' + os.path.join(filedir, 'cryoranker_getscores.py') + '\n')
        os.system('cd ' + metadatadir + '&&sbatch GetScore.sh > ' + os.path.join(metadatadir, 'slurm_uid'))
        while True:
            if os.path.exists(os.path.join(metadatadir, 'slurm_uid')):
                with open(os.path.join(metadatadir, 'slurm_uid'), 'r') as f:
                    slurm_uid = f.readline().split()[-1]
                break
            else:
                time.sleep(1)
        get_slurm_output(cryoranker_job, os.path.join(metadatadir, 'GetScore.out'), slurm_uid, metadatadir)

        if os.path.exists(os.path.join(metadatadir, 'scores.json')):
            output_groups = JobAPIs.create_output_groups(particle=[cryoranker_job.uid + '_particles'], ranker=[cryoranker_job.uid + '_particles'])
            toolbox.savetojson(output_groups, os.path.join(metadatadir, 'output_groups.json'), False)

            scores = toolbox.readjson(os.path.join(metadatadir, 'scores.json'))
            plot_particle_num_score_curve(cryoranker_job, scores, parameters_folder_name)

            output_particles_dataset = input_particles_dataset
            add_output_name = 'particles'
            cryoranker_job.add_output(type='particle', name=add_output_name, slots=['blob'], passthrough=add_input_name)
            cryoranker_job.save_output(add_output_name, output_particles_dataset)

    if not os.path.exists(os.path.join(metadatadir, 'scores.json')):
        cryoranker_job.stop(error=True)
    else:
        shutil.copy(os.path.join(metadatadir, 'scores.json'), os.path.join(dealjobs.GetProjectPath(), cryoranker_job.uid, 'scores.json'))

    cryorankertimeend = datetime.datetime.now()
    JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'CryoRanker finished! Time spent: ' + (str)(cryorankertimeend - cryorankertimebegin))


def get_top_particles(cryowizardjob, cryowizardlog, project_dir, parameters_folder_name):
    globaldir = os.path.normpath(project_dir)
    parametersdir = os.path.join(globaldir, 'parameters', 'cryoranker', parameters_folder_name)
    metadatadir = os.path.join(globaldir, 'metadata', 'cryoranker', parameters_folder_name)

    # initialize
    if not os.path.exists(metadatadir):
        os.makedirs(metadatadir)
    parameters = toolbox.readjson(os.path.join(globaldir, 'parameters', 'base_parameters', 'parameters.json'))
    cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(email=parameters['cryosparc_username'], password=parameters['cryosparc_password'])
    dealjobs = JobAPIs.DealJobs(cshandle, parameters['project'], parameters['workspace'], parameters['lane'])

    get_top_particles_parameters = toolbox.readjson(os.path.join(parametersdir, 'get_top_particles_parameters.json'))
    source_job_id_name_list = toolbox.readjson(os.path.join(parametersdir, 'source_cryoranker_job_uid.json'))['source_job_uid']
    source_job_id = JobAPIs.resolve_source_job_uids(globaldir, source_job_id_name_list, 'ranker')

    # combine ranker scores
    sorted_combined_scores_list = JobAPIs.combine_cryoranker_scores(dealjobs, JobAPIs.extract_source_job_ids(source_job_id))

    if (get_top_particles_parameters['get_type'] == 'num'):
        get_particle_job = JobAPIs.create_get_particles_by_score_job(dealjobs, JobAPIs.extract_source_job_ids(source_job_id), dealjobs.GetCryoSPARCJobListOutputNames(source_job_id, 'particle'), sorted_combined_scores_list, target_particle_num=get_top_particles_parameters['cut_off_point'])
        JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Get Particles job created: ' + get_particle_job.uid + ', type: ' + get_top_particles_parameters['get_type'] + ', cut-off point: ' + (str)(get_top_particles_parameters['cut_off_point']))
        output_groups = JobAPIs.create_output_groups(particle=[get_particle_job.uid + '_particles_selected'], ranker=source_job_id)
        toolbox.savetojson(output_groups, os.path.join(metadatadir, 'output_groups.json'), False)
    elif (get_top_particles_parameters['get_type'] == 'score'):
        get_particle_job = JobAPIs.create_get_particles_by_score_job(dealjobs, JobAPIs.extract_source_job_ids(source_job_id), dealjobs.GetCryoSPARCJobListOutputNames(source_job_id, 'particle'), sorted_combined_scores_list, target_score=get_top_particles_parameters['cut_off_point'])
        JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Get Particles job created: ' + get_particle_job.uid + ', type: ' + get_top_particles_parameters['get_type'] + ', cut-off point: ' + (str)(get_top_particles_parameters['cut_off_point']))
        output_groups = JobAPIs.create_output_groups(particle=[get_particle_job.uid + '_particles_selected'], ranker=source_job_id)
        toolbox.savetojson(output_groups, os.path.join(metadatadir, 'output_groups.json'), False)
    else:
        JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Get Particles type wrong')











