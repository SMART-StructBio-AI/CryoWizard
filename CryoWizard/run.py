#!/usr/bin/env python

import numpy as np
import datetime
import time
import os

import sys
sys.path.append(os.path.dirname(__file__))

import initialize
import importfiles
import preprocess
import cryoranker
import refine
import postprocess
import cryowizardlib.CSLogin as CSLogin
import cryowizardlib.JobAPIs as JobAPIs
import cryowizardlib.Toolbox as toolbox



def cryowizard_run_update_best_volume(dealjobs_instance, cryowizard_data_dir, output_groups):
    if output_groups['volume'] is not None:
        for single_output_volume_job_uid in output_groups['volume']:
            single_output_volume_job_uid = JobAPIs.extract_source_job_ids(single_output_volume_job_uid)
            if os.path.exists(os.path.join(cryowizard_data_dir, 'metadata', 'best_volume.json')):
                best_volume = toolbox.readjson(os.path.join(cryowizard_data_dir, 'metadata', 'best_volume.json'))
                if (dealjobs_instance.GetNURefineFinalResolution(single_output_volume_job_uid) < best_volume['resolution']):
                    toolbox.savetojson({'jobuid': single_output_volume_job_uid, 'resolution': (float)(dealjobs_instance.GetNURefineFinalResolution(single_output_volume_job_uid))}, os.path.join(cryowizard_data_dir, 'metadata', 'best_volume.json'), False)
            else:
                toolbox.savetojson({'jobuid': single_output_volume_job_uid, 'resolution': (float)(dealjobs_instance.GetNURefineFinalResolution(single_output_volume_job_uid))}, os.path.join(cryowizard_data_dir, 'metadata', 'best_volume.json'), False)
        best_volume = toolbox.readjson(os.path.join(cryowizard_data_dir, 'metadata', 'best_volume.json'))
        return best_volume
    else:
        return None

def cryowizard_run(cryosparc_username, cryosparc_password, project, cryowizard_job_uid):
    cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(email=cryosparc_username, password=cryosparc_password)
    project_handle = cshandle.find_project(project)
    cryowizard_job = project_handle.find_external_job(cryowizard_job_uid)
    cryowizard_data_dir = os.path.normpath(initialize.get_cryowizard_job_data_path(cryosparc_username, cryosparc_password, project, cryowizard_job_uid))
    toolbox.savetojson(os.getpid(), os.path.join(cryowizard_data_dir, 'cryowizard_run_pid.json'), False)
    if not os.path.exists(os.path.join(cryowizard_data_dir, 'metadata')):
        os.makedirs(os.path.join(cryowizard_data_dir, 'metadata'))

    # if not (cryowizard_job.status in ['building']):
    #     if cryowizard_job.status in ['launched', 'started', 'running', 'waiting']:
    #         cryowizard_job.kill()
    #     try:
    #         cryowizard_job.clear()
    #         cryowizard_job.wait_for_status('building', 5)
    #     except:
    #         pass

    with cryowizard_job.run():
        # with open(os.path.join(cryowizard_data_dir, 'metadata', 'cryowizard.log'), 'a') as cryowizard_log_file:
        #     pass
        # if os.path.exists(os.path.join(cryowizard_data_dir, 'metadata', 'cryowizard.log')):
        if True:
            cryowizard_log_file = os.path.join(cryowizard_data_dir, 'metadata', 'cryowizard.log')
            JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, 'Start to run CryoWizard')
            wholetimebegin = datetime.datetime.now()

            # initialize
            parameters = toolbox.readjson(os.path.join(cryowizard_data_dir, 'parameters', 'base_parameters', 'parameters.json'))
            cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(email=parameters['cryosparc_username'], password=parameters['cryosparc_password'])
            dealjobs = JobAPIs.DealJobs(cshandle, parameters['project'], parameters['workspace'], parameters['lane'])

            # running pipeline
            pipeline = toolbox.readjson(os.path.join(cryowizard_data_dir, 'parameters', 'base_parameters', 'pipeline.json'))
            step_sorted_pipeline = sorted(pipeline, key=lambda x: x['step'], reverse=False)
            for step_ptr in range(len(step_sorted_pipeline)):
                pipeline_step = step_sorted_pipeline[step_ptr]['step']
                pipeline_nodes = step_sorted_pipeline[step_ptr]['nodes']
                JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, '****************** Pipeline step ' + (str)(pipeline_step) + ' start ******************')
                singlesteptimebegin = datetime.datetime.now()
                # build jobs
                for single_pipeline_node in pipeline_nodes:
                    JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, '--- Pipeline step ' + (str)(pipeline_step) + ' node ' + single_pipeline_node + ' start building ---')
                    single_pipeline_node_head = single_pipeline_node.split('_')[0]
                    if (single_pipeline_node_head == 'import'):
                        parametersdir = os.path.join(cryowizard_data_dir, 'parameters', 'import', single_pipeline_node)
                        metadatadir = os.path.join(cryowizard_data_dir, 'metadata', 'import', single_pipeline_node)
                        parameters_type = toolbox.readjson(os.path.join(parametersdir, 'type.json'))['parameters_type']
                        if parameters_type in ['import_movie_file_parameters']:
                            if os.path.exists(os.path.join(metadatadir, 'created_jobs_info.json')):
                                JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, '--- Pipeline step ' + (str)(pipeline_step) + ' node ' + single_pipeline_node + ' building done ---')
                                continue
                            importfiles.import_movie(cryowizard_job, cryowizard_log_file, cryowizard_data_dir, single_pipeline_node)
                        elif parameters_type in ['import_micrograph_file_parameters']:
                            if os.path.exists(os.path.join(metadatadir, 'created_jobs_info.json')):
                                JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, '--- Pipeline step ' + (str)(pipeline_step) + ' node ' + single_pipeline_node + ' building done ---')
                                continue
                            importfiles.import_micrograph(cryowizard_job, cryowizard_log_file, cryowizard_data_dir, single_pipeline_node)
                        elif parameters_type in ['import_particle_file_parameters']:
                            if os.path.exists(os.path.join(metadatadir, 'created_jobs_info.json')):
                                JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, '--- Pipeline step ' + (str)(pipeline_step) + ' node ' + single_pipeline_node + ' building done ---')
                                continue
                            importfiles.import_particle(cryowizard_job, cryowizard_log_file, cryowizard_data_dir, single_pipeline_node)
                        elif parameters_type in ['import_volume_file_parameters']:
                            if os.path.exists(os.path.join(metadatadir, 'created_jobs_info.json')):
                                JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, '--- Pipeline step ' + (str)(pipeline_step) + ' node ' + single_pipeline_node + ' building done ---')
                                continue
                            importfiles.import_volume(cryowizard_job, cryowizard_log_file, cryowizard_data_dir, single_pipeline_node)

                        # other elif

                        else:
                            JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, parametersdir + ' parameters_type wrong')
                        JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, '--- Pipeline step ' + (str)(pipeline_step) + ' node ' + single_pipeline_node + ' building done ---')
                    elif (single_pipeline_node_head == 'preprocess'):
                        parametersdir = os.path.join(cryowizard_data_dir, 'parameters', 'preprocess', single_pipeline_node)
                        metadatadir = os.path.join(cryowizard_data_dir, 'metadata', 'preprocess', single_pipeline_node)
                        parameters_type = toolbox.readjson(os.path.join(parametersdir, 'type.json'))['parameters_type']
                        if parameters_type in ['preprocess_movie_with_blob_pick_parameters']:
                            if os.path.exists(os.path.join(metadatadir, 'created_jobs_info.json')):
                                JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, '--- Pipeline step ' + (str)(pipeline_step) + ' node ' + single_pipeline_node + ' building done ---')
                                continue
                            preprocess.movie_to_particle_with_blob_pick(cryowizard_job, cryowizard_log_file, cryowizard_data_dir, single_pipeline_node)
                        elif parameters_type in ['preprocess_movie_with_template_pick_parameters']:
                            if os.path.exists(os.path.join(metadatadir, 'created_jobs_info.json')):
                                JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, '--- Pipeline step ' + (str)(pipeline_step) + ' node ' + single_pipeline_node + ' building done ---')
                                continue
                            preprocess.movie_to_particle_with_template_pick(cryowizard_job, cryowizard_log_file, cryowizard_data_dir, single_pipeline_node)
                        elif parameters_type in ['preprocess_micrograph_with_blob_pick_parameters']:
                            if os.path.exists(os.path.join(metadatadir, 'created_jobs_info.json')):
                                JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, '--- Pipeline step ' + (str)(pipeline_step) + ' node ' + single_pipeline_node + ' building done ---')
                                continue
                            preprocess.micrograph_to_particle_with_blob_pick(cryowizard_job, cryowizard_log_file, cryowizard_data_dir, single_pipeline_node)
                        elif parameters_type in ['preprocess_micrograph_with_template_pick_parameters']:
                            if os.path.exists(os.path.join(metadatadir, 'created_jobs_info.json')):
                                JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, '--- Pipeline step ' + (str)(pipeline_step) + ' node ' + single_pipeline_node + ' building done ---')
                                continue
                            preprocess.micrograph_to_particle_with_template_pick(cryowizard_job, cryowizard_log_file, cryowizard_data_dir, single_pipeline_node)
                        elif parameters_type in ['preprocess_particle_parameters']:
                            if os.path.exists(os.path.join(metadatadir, 'created_jobs_info.json')):
                                JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, '--- Pipeline step ' + (str)(pipeline_step) + ' node ' + single_pipeline_node + ' building done ---')
                                continue
                            preprocess.import_particles(cryowizard_job, cryowizard_log_file, cryowizard_data_dir, single_pipeline_node)
                        elif parameters_type in ['create_templates_parameters']:
                            if os.path.exists(os.path.join(metadatadir, 'created_jobs_info.json')):
                                JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, '--- Pipeline step ' + (str)(pipeline_step) + ' node ' + single_pipeline_node + ' building done ---')
                                continue
                            preprocess.create_templates(cryowizard_job, cryowizard_log_file, cryowizard_data_dir, single_pipeline_node)
                        elif parameters_type in ['reference_based_auto_select_2d']:
                            if os.path.exists(os.path.join(metadatadir, 'created_jobs_info.json')):
                                JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, '--- Pipeline step ' + (str)(pipeline_step) + ' node ' + single_pipeline_node + ' building done ---')
                                continue
                            preprocess.reference_based_auto_select_2D(cryowizard_job, cryowizard_log_file, cryowizard_data_dir, single_pipeline_node)
                        elif parameters_type in ['junk_detector']:
                            if os.path.exists(os.path.join(metadatadir, 'created_jobs_info.json')):
                                JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, '--- Pipeline step ' + (str)(pipeline_step) + ' node ' + single_pipeline_node + ' building done ---')
                                continue
                            preprocess.micrograph_junk_detector(cryowizard_job, cryowizard_log_file, cryowizard_data_dir, single_pipeline_node)

                        # other elif

                        else:
                            JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, parametersdir + ' parameters_type wrong')
                        JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, '--- Pipeline step ' + (str)(pipeline_step) + ' node ' + single_pipeline_node + ' building done ---')
                    elif (single_pipeline_node_head == 'cryoranker'):
                        parametersdir = os.path.join(cryowizard_data_dir, 'parameters', 'cryoranker', single_pipeline_node)
                        metadatadir = os.path.join(cryowizard_data_dir, 'metadata', 'cryoranker', single_pipeline_node)
                        parameters_type = toolbox.readjson(os.path.join(parametersdir, 'type.json'))['parameters_type']
                        if (parameters_type == 'cryoranker_parameters'):
                            JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, '--- Pipeline step ' + (str)(pipeline_step) + ' node ' + single_pipeline_node + ' building done ---')
                            continue
                        if (parameters_type == 'get_top_particles'):
                            JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, '--- Pipeline step ' + (str)(pipeline_step) + ' node ' + single_pipeline_node + ' building done ---')
                            continue

                        # other elif

                        else:
                            JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, parametersdir + ' parameters_type wrong')
                        JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, '--- Pipeline step ' + (str)(pipeline_step) + ' node ' + single_pipeline_node + ' building done ---')
                    elif (single_pipeline_node_head == 'refine'):
                        parametersdir = os.path.join(cryowizard_data_dir, 'parameters', 'refine', single_pipeline_node)
                        metadatadir = os.path.join(cryowizard_data_dir, 'metadata', 'refine', single_pipeline_node)
                        parameters_type = toolbox.readjson(os.path.join(parametersdir, 'type.json'))['parameters_type']
                        if (parameters_type == 'refine_parameters'):
                            JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, '--- Pipeline step ' + (str)(pipeline_step) + ' node ' + single_pipeline_node + ' building done ---')
                            continue

                        # other elif

                        else:
                            JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, parametersdir + ' parameters_type wrong')
                        JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, '--- Pipeline step ' + (str)(pipeline_step) + ' node ' + single_pipeline_node + ' building done ---')
                    elif (single_pipeline_node_head == 'postprocess'):
                        parametersdir = os.path.join(cryowizard_data_dir, 'parameters', 'postprocess', single_pipeline_node)
                        metadatadir = os.path.join(cryowizard_data_dir, 'metadata', 'postprocess', single_pipeline_node)
                        parameters_type = toolbox.readjson(os.path.join(parametersdir, 'type.json'))['parameters_type']
                        if (parameters_type == 'motion_and_ctf_refine_parameters'):
                            if os.path.exists(os.path.join(metadatadir, 'created_jobs_info.json')):
                                JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, '--- Pipeline step ' + (str)(pipeline_step) + ' node ' + single_pipeline_node + ' building done ---')
                                continue
                            postprocess.motion_and_ctf_refine(cryowizard_job, cryowizard_log_file, cryowizard_data_dir, single_pipeline_node)

                        # other elif

                        else:
                            JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, parametersdir + ' parameters_type wrong')
                        JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, '--- Pipeline step ' + (str)(pipeline_step) + ' node ' + single_pipeline_node + ' building done ---')

                    # other elif

                    else:
                        JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, 'parameters_folder_name wrong')
                        return
                # run jobs
                JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, '--- Running pipeline step ' + (str)(pipeline_step) + ' ---')
                for single_pipeline_node in pipeline_nodes:
                    single_pipeline_node_head = single_pipeline_node.split('_')[0]
                    if (single_pipeline_node_head == 'import'):
                        parametersdir = os.path.join(cryowizard_data_dir, 'parameters', 'import', single_pipeline_node)
                        metadatadir = os.path.join(cryowizard_data_dir, 'metadata', 'import', single_pipeline_node)
                        parameters_type = toolbox.readjson(os.path.join(parametersdir, 'type.json'))['parameters_type']
                        if parameters_type in ['import_movie_file_parameters', 'import_micrograph_file_parameters', 'import_particle_file_parameters', 'import_volume_file_parameters']:
                            created_jobs_info = toolbox.readjson(os.path.join(metadatadir, 'created_jobs_info.json'))
                            JobAPIs.run_all_created_jobs(dealjobs, parameters, created_jobs_info)
                    elif (single_pipeline_node_head == 'preprocess'):
                        parametersdir = os.path.join(cryowizard_data_dir, 'parameters', 'preprocess', single_pipeline_node)
                        metadatadir = os.path.join(cryowizard_data_dir, 'metadata', 'preprocess', single_pipeline_node)
                        parameters_type = toolbox.readjson(os.path.join(parametersdir, 'type.json'))['parameters_type']
                        if parameters_type in ['preprocess_movie_with_blob_pick_parameters', 'preprocess_movie_with_template_pick_parameters', 'preprocess_micrograph_with_blob_pick_parameters', 'preprocess_micrograph_with_template_pick_parameters', 'preprocess_particle_parameters', 'create_templates_parameters', 'reference_based_auto_select_2d', 'junk_detector']:
                            created_jobs_info = toolbox.readjson(os.path.join(metadatadir, 'created_jobs_info.json'))
                            JobAPIs.run_all_created_jobs(dealjobs, parameters, created_jobs_info)
                    elif (single_pipeline_node_head == 'cryoranker'):
                        # ranker runs directly here regardless of safe_mode, don't add ranker jobs to all_created_jobs_info_list
                        parametersdir = os.path.join(cryowizard_data_dir, 'parameters', 'cryoranker', single_pipeline_node)
                        metadatadir = os.path.join(cryowizard_data_dir, 'metadata', 'cryoranker', single_pipeline_node)
                        parameters_type = toolbox.readjson(os.path.join(parametersdir, 'type.json'))['parameters_type']
                        if (parameters_type == 'cryoranker_parameters'):
                            if not os.path.exists(os.path.join(metadatadir, 'scores.json')):
                                if parameters['if_slurm']:
                                    cryoranker.cryoranker_get_score_slurm(cryowizard_job, cryowizard_log_file, cryowizard_data_dir, single_pipeline_node)
                                else:
                                    cryoranker.cryoranker_get_score(cryowizard_job, cryowizard_log_file, cryowizard_data_dir, single_pipeline_node)
                        if (parameters_type == 'get_top_particles'):
                            if not os.path.exists(os.path.join(metadatadir, 'output_groups.json')):
                                cryoranker.get_top_particles(cryowizard_job, cryowizard_log_file, cryowizard_data_dir, single_pipeline_node)
                    elif (single_pipeline_node_head == 'refine'):
                        parametersdir = os.path.join(cryowizard_data_dir, 'parameters', 'refine', single_pipeline_node)
                        metadatadir = os.path.join(cryowizard_data_dir, 'metadata', 'refine', single_pipeline_node)
                        parameters_type = toolbox.readjson(os.path.join(parametersdir, 'type.json'))['parameters_type']
                        if (parameters_type == 'refine_parameters'):
                            refine.refine(cryowizard_job, cryowizard_log_file, cryowizard_data_dir, single_pipeline_node)
                            output_groups = toolbox.readjson(os.path.join(metadatadir, 'output_groups.json'))
                            best_volume = cryowizard_run_update_best_volume(dealjobs, cryowizard_data_dir, output_groups)
                            JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, 'Getting final volume done, current best volume job uid: ' + best_volume['jobuid'] + ', best resolution: ' + (str)(round(best_volume['resolution'], 2)))
                    elif (single_pipeline_node_head == 'postprocess'):
                        parametersdir = os.path.join(cryowizard_data_dir, 'parameters', 'postprocess', single_pipeline_node)
                        metadatadir = os.path.join(cryowizard_data_dir, 'metadata', 'postprocess', single_pipeline_node)
                        parameters_type = toolbox.readjson(os.path.join(parametersdir, 'type.json'))['parameters_type']
                        if (parameters_type == 'motion_and_ctf_refine_parameters'):
                            created_jobs_info = toolbox.readjson(os.path.join(metadatadir, 'created_jobs_info.json'))
                            JobAPIs.run_all_created_jobs(dealjobs, parameters, created_jobs_info)
                            output_groups = toolbox.readjson(os.path.join(metadatadir, 'output_groups.json'))
                            best_volume = cryowizard_run_update_best_volume(dealjobs, cryowizard_data_dir, output_groups)
                            JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, 'Getting final volume done, current best volume job uid: ' + best_volume['jobuid'] + ', best resolution: ' + (str)(round(best_volume['resolution'], 2)))


                    # other elif

                    else:
                        JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, 'parameters_folder_name wrong')
                        return
                # check if all finished
                JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, '--- Running pipeline step ' + (str)(pipeline_step) + ' done ---')
                singlesteptimeend = datetime.datetime.now()
                JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, '****************** Pipeline step ' + (str)(pipeline_step) + ' done, Time spent: ' + (str)(singlesteptimeend - singlesteptimebegin) + ' ******************')

            # add cryowizard output groups
            if os.path.exists(os.path.join(cryowizard_data_dir, 'metadata', 'best_volume.json')):
                best_volume_info = toolbox.readjson(os.path.join(cryowizard_data_dir, 'metadata', 'best_volume.json'))
                best_final_nurefine_job_uid = best_volume_info['jobuid']
                best_final_nurefine_job = dealjobs.cshandle.find_job(dealjobs.project, best_final_nurefine_job_uid)
                best_final_nurefine_job_volume_dataset = best_final_nurefine_job.load_output('volume')
                add_output_volume_name = 'best_volume'
                try:
                    cryowizard_job.save_output(add_output_volume_name, best_final_nurefine_job_volume_dataset)
                except:
                    cryowizard_job.add_output(type='volume', name=add_output_volume_name, slots=['map', 'map_sharp'])
                    cryowizard_job.save_output(add_output_volume_name, best_final_nurefine_job_volume_dataset)
                JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, 'Final best volume job uid: ' + best_volume_info['jobuid'] + ', best resolution: ' + (str)(round(best_volume_info['resolution'], 2)))

            wholetimeend = datetime.datetime.now()
            JobAPIs.cryowizard_log(cryowizard_job, cryowizard_log_file, 'CryoWizard finished! Time spent: ' + (str)(wholetimeend - wholetimebegin))


def cryowizard_kill(cryosparc_username, cryosparc_password, project, cryowizard_job_uid):
    cryowizard_data_dir = os.path.normpath(initialize.get_cryowizard_job_data_path(cryosparc_username, cryosparc_password, project, cryowizard_job_uid))
    if os.path.exists(os.path.join(cryowizard_data_dir, 'cryowizard_run_pid.json')):
        cryowizard_run_pid = toolbox.readjson(os.path.join(cryowizard_data_dir, 'cryowizard_run_pid.json'))
        try:
            toolbox.killprocesswithpid(cryowizard_run_pid)
        except:
            pass

    parameters = toolbox.readjson(os.path.join(cryowizard_data_dir, 'parameters', 'base_parameters', 'parameters.json'))
    cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(email=parameters['cryosparc_username'], password=parameters['cryosparc_password'])
    dealjobs = JobAPIs.DealJobs(cshandle, parameters['project'], parameters['workspace'], parameters['lane'])

    if os.path.exists(os.path.join(cryowizard_data_dir, 'metadata', 'import')):
        metadata_folder_items = os.listdir(os.path.join(cryowizard_data_dir, 'metadata', 'import'))
        for single_data_folder_name in metadata_folder_items:
            single_data_folder_name_head = single_data_folder_name.split('_')[0]
            if (single_data_folder_name_head == 'import'):
                parametersdir = os.path.join(cryowizard_data_dir, 'parameters', 'import', single_data_folder_name)
                metadatadir = os.path.join(cryowizard_data_dir, 'metadata', 'import', single_data_folder_name)
                parameters_type = toolbox.readjson(os.path.join(parametersdir, 'type.json'))['parameters_type']
                if parameters_type in ['import_movie_file_parameters', 'import_micrograph_file_parameters', 'import_particle_file_parameters', 'import_volume_file_parameters']:
                    if os.path.exists(os.path.join(metadatadir, 'created_jobs_info.json')):
                        created_jobs_info = toolbox.readjson(os.path.join(metadatadir, 'created_jobs_info.json'))
                        JobAPIs.kill_all_created_jobs(dealjobs, created_jobs_info)

    if os.path.exists(os.path.join(cryowizard_data_dir, 'metadata', 'preprocess')):
        metadata_folder_items = os.listdir(os.path.join(cryowizard_data_dir, 'metadata', 'preprocess'))
        for single_data_folder_name in metadata_folder_items:
            single_data_folder_name_head = single_data_folder_name.split('_')[0]
            if (single_data_folder_name_head == 'preprocess'):
                parametersdir = os.path.join(cryowizard_data_dir, 'parameters', 'preprocess', single_data_folder_name)
                metadatadir = os.path.join(cryowizard_data_dir, 'metadata', 'preprocess', single_data_folder_name)
                parameters_type = toolbox.readjson(os.path.join(parametersdir, 'type.json'))['parameters_type']
                if parameters_type in ['preprocess_movie_with_blob_pick_parameters', 'preprocess_movie_with_template_pick_parameters', 'preprocess_micrograph_with_blob_pick_parameters', 'preprocess_micrograph_with_template_pick_parameters', 'preprocess_particle_parameters', 'create_templates_parameters', 'reference_based_auto_select_2d', 'junk_detector']:
                    if os.path.exists(os.path.join(metadatadir, 'created_jobs_info.json')):
                        created_jobs_info = toolbox.readjson(os.path.join(metadatadir, 'created_jobs_info.json'))
                        JobAPIs.kill_all_created_jobs(dealjobs, created_jobs_info)

    if os.path.exists(os.path.join(cryowizard_data_dir, 'metadata', 'cryoranker')):
        metadata_folder_items = os.listdir(os.path.join(cryowizard_data_dir, 'metadata', 'cryoranker'))
        for single_data_folder_name in metadata_folder_items:
            single_data_folder_name_head = single_data_folder_name.split('_')[0]
            if (single_data_folder_name_head == 'cryoranker'):
                parametersdir = os.path.join(cryowizard_data_dir, 'parameters', 'cryoranker', single_data_folder_name)
                metadatadir = os.path.join(cryowizard_data_dir, 'metadata', 'cryoranker', single_data_folder_name)
                parameters_type = toolbox.readjson(os.path.join(parametersdir, 'type.json'))['parameters_type']
                if (parameters_type == 'cryoranker_parameters'):
                    if os.path.exists(os.path.join(metadatadir, 'created_jobs_info.json')):
                        created_jobs_info = toolbox.readjson(os.path.join(metadatadir, 'created_jobs_info.json'))
                        JobAPIs.kill_all_created_jobs(dealjobs, created_jobs_info)
                    if os.path.exists(os.path.join(metadatadir, 'created_cryoranker_jobs_info.json')):
                        created_cryoranker_jobs_info = toolbox.readjson(os.path.join(metadatadir, 'created_cryoranker_jobs_info.json'))
                        JobAPIs.kill_all_created_jobs(dealjobs, created_cryoranker_jobs_info)
                    if os.path.exists(os.path.join(metadatadir, 'slurm_uid')):
                        with open(os.path.join(metadatadir, 'slurm_uid'), 'r') as f:
                            slurm_uid = f.readline().split()[-1]
                        if toolbox.checkifslurmjobinqueue(slurm_uid, metadatadir):
                            try:
                                os.system('scancel ' + (str)(slurm_uid))
                            except:
                                pass
                elif (parameters_type == 'get_top_particles'):
                    pass

    if os.path.exists(os.path.join(cryowizard_data_dir, 'metadata', 'refine')):
        metadata_folder_items = os.listdir(os.path.join(cryowizard_data_dir, 'metadata', 'refine'))
        for single_data_folder_name in metadata_folder_items:
            single_data_folder_name_head = single_data_folder_name.split('_')[0]
            if (single_data_folder_name_head == 'refine'):
                parametersdir = os.path.join(cryowizard_data_dir, 'parameters', 'refine', single_data_folder_name)
                metadatadir = os.path.join(cryowizard_data_dir, 'metadata', 'refine', single_data_folder_name)
                parameters_type = toolbox.readjson(os.path.join(parametersdir, 'type.json'))['parameters_type']
                if (parameters_type == 'refine_parameters'):
                    if os.path.exists(os.path.join(metadatadir, 'abinitial_created_jobs_info.json')):
                        abinitial_created_jobs_info = toolbox.readjson(os.path.join(metadatadir, 'abinitial_created_jobs_info.json'))
                        JobAPIs.kill_all_created_jobs(dealjobs, abinitial_created_jobs_info)
                    for turn_count in range(len(parameters['refine_grid_num_in_each_turn'])):
                        if os.path.exists(os.path.join(metadatadir, 'refine_turn_' + (str)(turn_count) + '_created_jobs_info.json')):
                            refine_created_jobs_info = toolbox.readjson(os.path.join(metadatadir, 'refine_turn_' + (str)(turn_count) + '_created_jobs_info.json'))
                            JobAPIs.kill_all_created_jobs(dealjobs, refine_created_jobs_info)

    if os.path.exists(os.path.join(cryowizard_data_dir, 'metadata', 'postprocess')):
        metadata_folder_items = os.listdir(os.path.join(cryowizard_data_dir, 'metadata', 'postprocess'))
        for single_data_folder_name in metadata_folder_items:
            single_data_folder_name_head = single_data_folder_name.split('_')[0]
            if (single_data_folder_name_head == 'postprocess'):
                parametersdir = os.path.join(cryowizard_data_dir, 'parameters', 'postprocess', single_data_folder_name)
                metadatadir = os.path.join(cryowizard_data_dir, 'metadata', 'postprocess', single_data_folder_name)
                parameters_type = toolbox.readjson(os.path.join(parametersdir, 'type.json'))['parameters_type']
                if (parameters_type == 'motion_and_ctf_refine_parameters'):
                    created_jobs_info = toolbox.readjson(os.path.join(metadatadir, 'created_jobs_info.json'))
                    JobAPIs.kill_all_created_jobs(dealjobs, created_jobs_info)

    dealjobs.KillJobSafely([cryowizard_job_uid])



