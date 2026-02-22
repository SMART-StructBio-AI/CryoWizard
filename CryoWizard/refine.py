#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import scipy
import os

import sys
sys.path.append(os.path.dirname(__file__))

import cryowizardlib.CSLogin as CSLogin
import cryowizardlib.JobAPIs as JobAPIs
import cryowizardlib.Toolbox as toolbox



def plot_final_refine_curve(cryowizard_job, plot_info_list, sorted_combined_scores_list, parameters_folder_name):
    sorted_plot_info_list = sorted(plot_info_list, key=lambda x: x['particle_num'], reverse=False)
    sorted_particle_num_list = []
    sorted_min_score_list = []
    sorted_resolution_list = []
    for plot_info_list_ptr in range(len(sorted_plot_info_list)):
        if sorted_plot_info_list[plot_info_list_ptr]['particle_num'] in sorted_particle_num_list:
            continue
        sorted_particle_num_list.append(sorted_plot_info_list[plot_info_list_ptr]['particle_num'])
        sorted_min_score_list.append(sorted_plot_info_list[plot_info_list_ptr]['min_score'])
        sorted_resolution_list.append(sorted_plot_info_list[plot_info_list_ptr]['resolution'])
    try:
        interpolate_function = scipy.interpolate.interp1d(sorted_particle_num_list, sorted_resolution_list, kind='quadratic', bounds_error=False)
        interpolated_sorted_particle_num_list = np.arange(sorted_particle_num_list[0], sorted_particle_num_list[-1], (sorted_particle_num_list[-1] - sorted_particle_num_list[0]) / 100.0)
        interpolated_sorted_resolution_list = interpolate_function(interpolated_sorted_particle_num_list)
    except:
        interpolated_sorted_particle_num_list = sorted_particle_num_list
        interpolated_sorted_resolution_list = sorted_resolution_list
    plt.clf()
    plt.ioff()
    plt.plot(interpolated_sorted_particle_num_list, interpolated_sorted_resolution_list)
    plt.xlabel('Particle number')
    plt.ylabel('Resolution (A)')
    plt.title('ParticleNumber-Resolution curve (' + parameters_folder_name + ')')
    cryowizard_job.log_plot(plt, 'Plot ParticleNumber-Resolution curve (' + parameters_folder_name + ')')

    sorted_plot_info_list = sorted(plot_info_list, key=lambda x: x['particle_num'], reverse=True)
    sorted_particle_num_list = []
    sorted_min_score_list = []
    sorted_resolution_list = []
    for plot_info_list_ptr in range(len(sorted_plot_info_list)):
        if sorted_plot_info_list[plot_info_list_ptr]['particle_num'] in sorted_particle_num_list:
            continue
        sorted_particle_num_list.append(sorted_plot_info_list[plot_info_list_ptr]['particle_num'])
        sorted_min_score_list.append(sorted_plot_info_list[plot_info_list_ptr]['min_score'])
        sorted_resolution_list.append(sorted_plot_info_list[plot_info_list_ptr]['resolution'])
    try:
        interpolate_function = scipy.interpolate.interp1d(sorted_min_score_list, sorted_resolution_list, kind='quadratic', bounds_error=False)
        interpolated_sorted_min_score_list = np.arange(sorted_min_score_list[0], sorted_min_score_list[-1], (sorted_min_score_list[-1] - sorted_min_score_list[0]) / 100.0)
        interpolated_sorted_resolution_list = interpolate_function(interpolated_sorted_min_score_list)
    except:
        interpolated_sorted_min_score_list = sorted_min_score_list
        interpolated_sorted_resolution_list = sorted_resolution_list
    plt.clf()
    plt.ioff()
    plt.plot(interpolated_sorted_min_score_list, interpolated_sorted_resolution_list)
    plt.gca().invert_xaxis()
    plt.xlabel('Score')
    plt.ylabel('Resolution (A)')
    plt.title('Score-Resolution curve (' + parameters_folder_name + ')')
    cryowizard_job.log_plot(plt, 'Plot Score-Resolution curve (' + parameters_folder_name + ')')

    scores_list = []
    for particle_uid_score in sorted_combined_scores_list:
        scores_list.append(particle_uid_score['score'])
    sorted_scores_list = sorted(scores_list, reverse=True)
    particle_num_list = [(int)(particle_num_ptr + 1) for particle_num_ptr in range(len(sorted_scores_list))]
    plt.clf()
    plt.ioff()
    plt.plot(particle_num_list, scores_list)
    plt.xlabel('Particle number')
    plt.ylabel('Score')
    plt.title('ParticleNumber-Score curve (' + parameters_folder_name + ')')
    cryowizard_job.log_plot(plt, 'Plot ParticleNumber-Score curve (' + parameters_folder_name + ')')


def refine_initial(cryowizardjob, cryowizardlog, project_dir, parameters_folder_name, dealjobs_instance, parameters, source_job_id, sorted_combined_scores_list):
    globaldir = os.path.normpath(project_dir)
    parametersdir = os.path.join(globaldir, 'parameters', 'refine', parameters_folder_name)
    metadatadir = os.path.join(globaldir, 'metadata', 'refine', parameters_folder_name)

    # build jobs
    if (len(sorted_combined_scores_list) <= (parameters['base_abinit_particle_num'] * parameters['abinit_num'])):
        base_abinit_particle_num = (int)(np.floor((float)(len(sorted_combined_scores_list)) / (float)(parameters['abinit_num'])))
        abinit_num = parameters['abinit_num']
    else:
        base_abinit_particle_num = parameters['base_abinit_particle_num']
        abinit_num = parameters['abinit_num']
    restack_particles_class = JobAPIs.CreateRestackParticles(dealjobs_instance)
    restack_particles_parameters = toolbox.readjson(os.path.join(parametersdir, 'restack_particles_parameters.json'))
    abinit_class = JobAPIs.CreateHomoAbinit(dealjobs_instance)
    abinit_parameters = toolbox.readjson(os.path.join(parametersdir, 'abinit_parameters.json'))
    nurefine_initial_class = JobAPIs.CreateNonuniformRefine(dealjobs_instance)
    nurefine_initial_parameters = toolbox.readjson(os.path.join(parametersdir, 'nurefine_parameters_initial.json'))
    orientation_diagnostics_initial_class = JobAPIs.CreateOrientationDiagnostics(dealjobs_instance)
    orientation_diagnostics_initial_parameters = toolbox.readjson(os.path.join(parametersdir, 'orientation_diagnostics_parameters_initial.json'))
    created_jobs_info = []
    jobs_for_search_best_one = []
    for abinit_count in range(abinit_num):
        particle_num = (int)((abinit_count + 1) * base_abinit_particle_num)
        get_particle_job = JobAPIs.create_get_particles_by_score_job(dealjobs_instance, JobAPIs.extract_source_job_ids(source_job_id), dealjobs_instance.GetCryoSPARCJobListOutputNames(source_job_id, 'particle'), sorted_combined_scores_list, target_particle_num=particle_num)
        JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Get Particles job created: ' + get_particle_job.uid + ', particle number: ' + (str)(particle_num))
        current_particles_job_uid = get_particle_job.uid
        current_particles_job_name = 'particles_selected'
        if parameters['low_cache_mode']:
            restack_particles_job = restack_particles_class.QueueRestackJob(restack_particles_parameters, [current_particles_job_uid], [current_particles_job_name])
            created_jobs_info.append(JobAPIs.create_created_jobs_info_item(restack_particles_job.uid, parents=[current_particles_job_uid]))
            JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Restack Particles job created: ' + restack_particles_job.uid)
            current_particles_job_uid = restack_particles_job.uid
            current_particles_job_name = 'particles'
        abinit_job = abinit_class.QueueHomoAbinitJob(abinit_parameters, [current_particles_job_uid], [current_particles_job_name])
        created_jobs_info.append(JobAPIs.create_created_jobs_info_item(abinit_job.uid, parents=[current_particles_job_uid], gpu_need=1))
        JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Ab-Initio Reconstruction job created: ' + abinit_job.uid + ', particle number: ' + (str)(particle_num))
        nurefine_initial_job = nurefine_initial_class.QueueNonuniformRefineJob(nurefine_initial_parameters, [current_particles_job_uid], [current_particles_job_name], abinit_job.uid, 'volume_class_0')
        created_jobs_info.append(JobAPIs.create_created_jobs_info_item(nurefine_initial_job.uid, parents=[current_particles_job_uid, abinit_job.uid], gpu_need=1))
        JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Initial Non-uniform Refinement job created: ' + nurefine_initial_job.uid + ', particle number: ' + (str)(particle_num))
        if parameters['orientation_balance']:
            orientation_diagnostics_initial_job = orientation_diagnostics_initial_class.QueueOrientationDiagnosticsJob(orientation_diagnostics_initial_parameters, nurefine_initial_job.uid, 'volume')
            created_jobs_info.append(JobAPIs.create_created_jobs_info_item(orientation_diagnostics_initial_job.uid, parents=[nurefine_initial_job.uid]))
            JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Orientation Diagnostics job created: ' + orientation_diagnostics_initial_job.uid + ', particle number: ' + (str)(particle_num))
            jobs_for_search_best_one.append({'particle_num': particle_num, 'nurefine': nurefine_initial_job.uid, 'orientation_diagnostics': orientation_diagnostics_initial_job.uid})
        else:
            jobs_for_search_best_one.append({'particle_num': particle_num, 'nurefine': nurefine_initial_job.uid, 'orientation_diagnostics': None})
    toolbox.savetojson(created_jobs_info, os.path.join(metadatadir, 'abinitial_created_jobs_info.json'), False)
    toolbox.savetojson(jobs_for_search_best_one, os.path.join(metadatadir, 'abinitial_jobs_for_search_best_one.json'), False)


def refine_search_single_turn(cryowizardjob, cryowizardlog, project_dir, parameters_folder_name, dealjobs_instance, parameters, source_job_id, sorted_combined_scores_list, best_nurefine_uid, start_particle_num, end_particle_num, turn_count, best_refine_jobs_info_item):
    globaldir = os.path.normpath(project_dir)
    parametersdir = os.path.join(globaldir, 'parameters', 'refine', parameters_folder_name)
    metadatadir = os.path.join(globaldir, 'metadata', 'refine', parameters_folder_name)

    # build jobs
    single_turn_grid_num = parameters['refine_grid_num_in_each_turn'][turn_count]
    if best_refine_jobs_info_item is None:
        half_single_turn_particle_num_step = (int)(np.floor((float)(end_particle_num - start_particle_num) / (float)(single_turn_grid_num * 2)))
        single_turn_particle_num_grid = [(int)(half_single_turn_particle_num_step + start_particle_num + 2 * grid_ptr * half_single_turn_particle_num_step) for grid_ptr in range(single_turn_grid_num)]
    else:
        half_single_turn_particle_num_step = (int)(np.floor((float)(end_particle_num - start_particle_num) / (float)((single_turn_grid_num + 1) * 2)))
        single_turn_particle_num_grid = [(int)(half_single_turn_particle_num_step + start_particle_num + 2 * grid_ptr * half_single_turn_particle_num_step) for grid_ptr in range((int)(single_turn_grid_num / 2))]
        single_turn_particle_num_grid += [(int)(half_single_turn_particle_num_step + start_particle_num + 2 * grid_ptr * half_single_turn_particle_num_step) for grid_ptr in range((int)(single_turn_grid_num / 2 + 1), (int)(single_turn_grid_num + 1))]
    restack_particles_class = JobAPIs.CreateRestackParticles(dealjobs_instance)
    restack_particles_parameters = toolbox.readjson(os.path.join(parametersdir, 'restack_particles_parameters.json'))
    nurefine_final_class = JobAPIs.CreateNonuniformRefine(dealjobs_instance)
    nurefine_final_parameters = toolbox.readjson(os.path.join(parametersdir, 'nurefine_parameters_final.json'))
    orientation_diagnostics_final_class = JobAPIs.CreateOrientationDiagnostics(dealjobs_instance)
    orientation_diagnostics_final_parameters = toolbox.readjson(os.path.join(parametersdir, 'orientation_diagnostics_parameters_final.json'))
    created_jobs_info = []
    jobs_for_search_best_one = []
    if best_refine_jobs_info_item is not None:
        jobs_for_search_best_one.append({'particle_num': best_refine_jobs_info_item['particle_num'], 'nurefine': best_refine_jobs_info_item['nurefine'], 'orientation_diagnostics': best_refine_jobs_info_item['orientation_diagnostics'], 'particle_start': (int)(start_particle_num + 2 * (single_turn_grid_num / 2) * half_single_turn_particle_num_step), 'particle_end': (int)(start_particle_num + 2 * (single_turn_grid_num / 2 + 1) * half_single_turn_particle_num_step)})
    for gird_ptr in range(single_turn_grid_num):
        particle_num = single_turn_particle_num_grid[gird_ptr]
        get_particle_job = JobAPIs.create_get_particles_by_score_job(dealjobs_instance, JobAPIs.extract_source_job_ids(source_job_id), dealjobs_instance.GetCryoSPARCJobListOutputNames(source_job_id, 'particle'), sorted_combined_scores_list, target_particle_num=particle_num)
        JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Get Particles job created: ' + get_particle_job.uid + ', particle number: ' + (str)(particle_num))
        current_particles_job_uid = get_particle_job.uid
        current_particles_job_name = 'particles_selected'
        if parameters['low_cache_mode']:
            restack_particles_job = restack_particles_class.QueueRestackJob(restack_particles_parameters, [current_particles_job_uid], [current_particles_job_name])
            created_jobs_info.append(JobAPIs.create_created_jobs_info_item(restack_particles_job.uid, parents=[current_particles_job_uid]))
            JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Restack Particles job created: ' + restack_particles_job.uid)
            current_particles_job_uid = restack_particles_job.uid
            current_particles_job_name = 'particles'
        nurefine_final_job = nurefine_final_class.QueueNonuniformRefineJob(nurefine_final_parameters, [current_particles_job_uid], [current_particles_job_name], best_nurefine_uid, 'volume')
        created_jobs_info.append(JobAPIs.create_created_jobs_info_item(nurefine_final_job.uid, parents=[current_particles_job_uid, best_nurefine_uid], gpu_need=1))
        JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Final Non-uniform Refinement job created: ' + nurefine_final_job.uid + ', particle number: ' + (str)(particle_num))
        if parameters['orientation_balance']:
            orientation_diagnostics_final_job = orientation_diagnostics_final_class.QueueOrientationDiagnosticsJob(orientation_diagnostics_final_parameters, nurefine_final_job.uid, 'volume')
            created_jobs_info.append(JobAPIs.create_created_jobs_info_item(orientation_diagnostics_final_job.uid, parents=[nurefine_final_job.uid]))
            JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Orientation Diagnostics job created: ' + orientation_diagnostics_final_job.uid + ', particle number: ' + (str)(particle_num))
            jobs_for_search_best_one.append({'particle_num': particle_num, 'nurefine': nurefine_final_job.uid, 'orientation_diagnostics': orientation_diagnostics_final_job.uid, 'particle_start': (int)(particle_num - half_single_turn_particle_num_step), 'particle_end': (int)(particle_num + half_single_turn_particle_num_step)})
        else:
            jobs_for_search_best_one.append({'particle_num': particle_num, 'nurefine': nurefine_final_job.uid, 'orientation_diagnostics': None, 'particle_start': (int)(particle_num - half_single_turn_particle_num_step), 'particle_end': (int)(particle_num + half_single_turn_particle_num_step)})
    toolbox.savetojson(created_jobs_info, os.path.join(metadatadir, 'refine_turn_' + (str)(turn_count) + '_created_jobs_info.json'), False)
    toolbox.savetojson(jobs_for_search_best_one, os.path.join(metadatadir, 'refine_turn_' + (str)(turn_count) + '_jobs_for_search_best_one.json'), False)


def refine(cryowizardjob, cryowizardlog, project_dir, parameters_folder_name):
    globaldir = os.path.normpath(project_dir)
    parametersdir = os.path.join(globaldir, 'parameters', 'refine', parameters_folder_name)
    metadatadir = os.path.join(globaldir, 'metadata', 'refine', parameters_folder_name)

    # initialize
    if not os.path.exists(metadatadir):
        os.makedirs(metadatadir)
    parameters = toolbox.readjson(os.path.join(globaldir, 'parameters', 'base_parameters', 'parameters.json'))
    cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(email=parameters['cryosparc_username'], password=parameters['cryosparc_password'])
    dealjobs = JobAPIs.DealJobs(cshandle, parameters['project'], parameters['workspace'], parameters['lane'])

    source_job_id_name_list = toolbox.readjson(os.path.join(parametersdir, 'source_cryoranker_job_uid.json'))['source_job_uid']
    source_job_id = JobAPIs.resolve_source_job_uids(globaldir, source_job_id_name_list, 'ranker')

    # combine ranker scores
    sorted_combined_scores_list = JobAPIs.combine_cryoranker_scores(dealjobs, JobAPIs.extract_source_job_ids(source_job_id))

    # build jobs
    created_jobs_info = []
    ## initial
    JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Getting initial volume...')
    if not os.path.exists(os.path.join(metadatadir, 'abinitial_created_jobs_info.json')):
        refine_initial(cryowizardjob, cryowizardlog, project_dir, parameters_folder_name, dealjobs, parameters, source_job_id, sorted_combined_scores_list)
    abinitial_created_jobs_info = toolbox.readjson(os.path.join(metadatadir, 'abinitial_created_jobs_info.json'))
    JobAPIs.run_all_created_jobs(dealjobs, parameters, abinitial_created_jobs_info)
    created_jobs_info += abinitial_created_jobs_info
    JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Getting initial volume done')
    ## final refine
    JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Getting final volume...')
    ### prepare first iteration parameters
    abinitial_jobs_for_search_best_one = toolbox.readjson(os.path.join(metadatadir, 'abinitial_jobs_for_search_best_one.json'))
    best_nurefine_job_uid = None
    best_nurefine_job_resolution = np.inf
    if parameters['orientation_balance']:
        pass
    else:
        for abinitial_jobs_info in abinitial_jobs_for_search_best_one:
            nurefine_job_uid = abinitial_jobs_info['nurefine']
            nurefine_job_resolution = dealjobs.GetNURefineFinalResolution(nurefine_job_uid)
            if (nurefine_job_resolution < best_nurefine_job_resolution):
                best_nurefine_job_uid = nurefine_job_uid
                best_nurefine_job_resolution = nurefine_job_resolution
    best_initial_nurefine_job_uid = best_nurefine_job_uid
    turn_num = len(parameters['refine_grid_num_in_each_turn'])
    if (len(sorted_combined_scores_list) <= parameters['min_refine_particle_num']):
        start_particle_num = 0
        end_particle_num = len(sorted_combined_scores_list)
    else:
        min_refine_score_particle_num = 0
        max_refine_score_particle_num = 0
        for sorted_combined_scores_ptr in range(len(sorted_combined_scores_list)):
            if (sorted_combined_scores_list[sorted_combined_scores_ptr]['score'] >= parameters['min_refine_score']):
                min_refine_score_particle_num += 1
            if (sorted_combined_scores_list[sorted_combined_scores_ptr]['score'] >= parameters['max_refine_score']):
                max_refine_score_particle_num += 1
        start_particle_num = min_refine_score_particle_num if (min_refine_score_particle_num > parameters['min_refine_particle_num']) else parameters['min_refine_particle_num']
        end_particle_num = max_refine_score_particle_num if (max_refine_score_particle_num < parameters['max_refine_particle_num']) else parameters['max_refine_particle_num']
        if (start_particle_num > end_particle_num):
            start_particle_num = min_refine_score_particle_num
            end_particle_num = max_refine_score_particle_num
    ### run
    best_refine_jobs_info_item = None
    for turn_count in range(turn_num):
        if not os.path.exists(os.path.join(metadatadir, 'refine_turn_' + (str)(turn_count) + '_created_jobs_info.json')):
            refine_search_single_turn(cryowizardjob, cryowizardlog, project_dir, parameters_folder_name, dealjobs, parameters, source_job_id, sorted_combined_scores_list, best_initial_nurefine_job_uid, start_particle_num, end_particle_num, turn_count, best_refine_jobs_info_item)
        refine_created_jobs_info = toolbox.readjson(os.path.join(metadatadir, 'refine_turn_' + (str)(turn_count) + '_created_jobs_info.json'))
        JobAPIs.run_all_created_jobs(dealjobs, parameters, refine_created_jobs_info)
        created_jobs_info += refine_created_jobs_info
        refine_jobs_for_search_best_one = toolbox.readjson(os.path.join(metadatadir, 'refine_turn_' + (str)(turn_count) + '_jobs_for_search_best_one.json'))
        best_nurefine_job_uid = None
        best_nurefine_job_resolution = np.inf
        if parameters['orientation_balance']:
            pass
        else:
            for refine_jobs_info in refine_jobs_for_search_best_one:
                nurefine_job_uid = refine_jobs_info['nurefine']
                nurefine_job_resolution = dealjobs.GetNURefineFinalResolution(nurefine_job_uid)
                if (nurefine_job_resolution < best_nurefine_job_resolution):
                    best_nurefine_job_uid = nurefine_job_uid
                    best_nurefine_job_resolution = nurefine_job_resolution
                    best_refine_jobs_info_item = refine_jobs_info
                    start_particle_num = refine_jobs_info['particle_start']
                    end_particle_num = refine_jobs_info['particle_end']
    ## plot curves in cryowizard job
    if parameters['orientation_balance']:
        pass
    else:
        plot_info_list = []
        abinitial_jobs_for_search_best_one = toolbox.readjson(os.path.join(metadatadir, 'abinitial_jobs_for_search_best_one.json'))
        for abinitial_jobs_info in abinitial_jobs_for_search_best_one:
            nurefine_job_uid = abinitial_jobs_info['nurefine']
            nurefine_job_resolution = dealjobs.GetNURefineFinalResolution(nurefine_job_uid)
            particle_num = abinitial_jobs_info['particle_num']
            min_score = sorted_combined_scores_list[particle_num - 1]['score']
            plot_info_list.append({'particle_num': particle_num, 'min_score': min_score, 'resolution': nurefine_job_resolution})
        for turn_count in range(turn_num):
            refine_jobs_for_search_best_one = toolbox.readjson(os.path.join(metadatadir, 'refine_turn_' + (str)(turn_count) + '_jobs_for_search_best_one.json'))
            for refine_jobs_info in refine_jobs_for_search_best_one:
                nurefine_job_uid = refine_jobs_info['nurefine']
                nurefine_job_resolution = dealjobs.GetNURefineFinalResolution(nurefine_job_uid)
                particle_num = refine_jobs_info['particle_num']
                min_score = sorted_combined_scores_list[particle_num - 1]['score']
                plot_info_list.append({'particle_num': particle_num, 'min_score': min_score, 'resolution': nurefine_job_resolution})
        plot_final_refine_curve(cryowizardjob, plot_info_list, sorted_combined_scores_list, parameters_folder_name)

    toolbox.savetojson(created_jobs_info, os.path.join(metadatadir, 'created_jobs_info.json'), False)
    output_groups = JobAPIs.create_output_groups(particle=[best_nurefine_job_uid + '_particles'], volume=[best_nurefine_job_uid + '_volume'], mask=[best_nurefine_job_uid + '_mask'])
    toolbox.savetojson(output_groups, os.path.join(metadatadir, 'output_groups.json'), False)


