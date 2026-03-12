import flask
import flask_socketio
import shutil
import psutil
import math
import os

import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import cryowizardlib.CSLogin as CSLogin
import cryowizardlib.JobAPIs as JobAPIs
import cryowizardlib.Toolbox as toolbox



app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'some_kind_of_secret_key'
socketio = flask_socketio.SocketIO(app, cors_allowed_origins='*')
filedir = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))  # folder path to .../CryoWizard/CryoWizard

cryowizard_settings = toolbox.readyaml(os.path.join(filedir, 'cryowizard_settings.yml'))
multithread = toolbox.MultiThreadingRun(threadpoolmaxsize=cryowizard_settings['CryoWizard_settings']['GUI']['max_thread_num'], try_mode=True)



########################################################### ext part ###########################################################


@socketio.on('check_cryowizard_user_login_action')
def check_cryowizard_user_login_action(cryosparc_username, cryosparc_password):
    try:
        cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(email=cryosparc_username, password=cryosparc_password)
        flask_socketio.emit('js_check_cryowizard_user_login_action', {'result': True})
    except:
        flask_socketio.emit('js_check_cryowizard_user_login_action', {'result': False})


@socketio.on('create_cryowizard_external_job_action')
def create_cryowizard_external_job_action(cryosparc_username, cryosparc_password, project, workspace):
    # create new cryowizard job and base parameters
    import initialize
    new_cryowizard_job_uid = initialize.create_cryowizard_job(cryosparc_username, cryosparc_password, project, workspace, 'test')
    new_cryowizard_data_dir = initialize.get_cryowizard_job_data_path(cryosparc_username, cryosparc_password, project, new_cryowizard_job_uid)
    base_parameters_folder_path = initialize.create_parameters(new_cryowizard_data_dir, {'type': 'base_parameters'})
    # flask_socketio.emit('js_create_cryowizard_external_job_action', {'project': project, 'workspace': workspace, 'new_cryowizard_jobid': new_cryowizard_job_uid})


# no need to be on socketio
# @socketio.on('modify_cryowizard_external_job_action')
def modify_cryowizard_external_job_action(cryosparc_username, cryosparc_password, project, jobid, parameters):
    # create base parameters (if do not exist) and create new cryowizard_preset_pipeline_info.json by gui input parameters
    # caution: type of each parameter in parameters is str, do not convert in advance
    import initialize
    cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(email=cryosparc_username, password=cryosparc_password)
    cryowizard_job = cshandle.find_external_job(project, jobid)
    cryowizard_data_dir = initialize.get_cryowizard_job_data_path(cryosparc_username, cryosparc_password, project, jobid)
    job_inputs_info = JobAPIs.get_job_connected_inputs(cryowizard_job)

    new_preprocess_movie_source_job_uids = None
    new_preprocess_micrograph_source_job_uids = None
    new_preprocess_particle_source_job_uids = None
    new_preprocess_cryoranker_source_job_uids = None
    if (len(job_inputs_info['input_movies']) > 0):
        new_preprocess_movie_source_job_uids = [(job_inputs_info['input_movies'][i]['job_uid'] + '_' + job_inputs_info['input_movies'][i]['job_output_name']) for i in range(len(job_inputs_info['input_movies']))]
    if (len(job_inputs_info['input_micrographs']) > 0):
        new_preprocess_micrograph_source_job_uids = [(job_inputs_info['input_micrographs'][i]['job_uid'] + '_' + job_inputs_info['input_micrographs'][i]['job_output_name']) for i in range(len(job_inputs_info['input_micrographs']))]
    if (len(job_inputs_info['input_particles']) > 0):
        new_preprocess_particle_source_job_uids = [(job_inputs_info['input_particles'][i]['job_uid'] + '_' + job_inputs_info['input_particles'][i]['job_output_name']) for i in range(len(job_inputs_info['input_particles']))]
    if (len(job_inputs_info['input_cryorankers']) > 0):
        new_preprocess_cryoranker_source_job_uids = [(job_inputs_info['input_cryorankers'][i]['job_uid'] + '_' + job_inputs_info['input_cryorankers'][i]['job_output_name']) for i in range(len(job_inputs_info['input_cryorankers']))]
    if (len(job_inputs_info['input_templates']) > 0):
        pass
    if (len(job_inputs_info['input_volumes']) > 0):
        pass
    if (len(job_inputs_info['input_masks']) > 0):
        pass

    if not os.path.exists(os.path.join(cryowizard_data_dir, 'parameters', 'base_parameters', 'cryowizard_preset_pipeline_info.json')):
        base_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'base_parameters'})
    else:
        base_parameters_folder_path = os.path.join(cryowizard_data_dir, 'parameters', 'base_parameters')
    if parameters is not None:
        preset_pipeline_info_cmd = ('python ' + os.path.join(os.path.dirname(filedir), 'CryoWizard.py') +
                                    ' --MakePresetPipelineInfo' +
                                    ' --cryosparc_username \'' + cryosparc_username + '\'' +
                                    ' --cryosparc_password \'' + cryosparc_password + '\'' +
                                    ' --cryosparc_project ' + project +
                                    ' --cryowizard_job_uid ' + jobid +
                                    ' --preset_pipeline_type ' + (parameters['pipeline_type'] if len(parameters['pipeline_type']) > 0 else 'default'))
        if new_preprocess_movie_source_job_uids is not None:
            preset_pipeline_info_cmd += (' --source_movie_job_uid ' + ' '.join(new_preprocess_movie_source_job_uids))
        if new_preprocess_micrograph_source_job_uids is not None:
            preset_pipeline_info_cmd += (' --source_micrograph_job_uid ' + ' '.join(new_preprocess_micrograph_source_job_uids))
        if new_preprocess_particle_source_job_uids is not None:
            preset_pipeline_info_cmd += (' --source_particle_job_uid ' + ' '.join(new_preprocess_particle_source_job_uids))
        if new_preprocess_cryoranker_source_job_uids is not None:
            preset_pipeline_info_cmd += (' --source_cryoranker_job_uid ' + ' '.join(new_preprocess_cryoranker_source_job_uids))
        if (len(parameters['pixelsize']) > 0):
            preset_pipeline_info_cmd += (' --raw_pixel_size ' + '\'' + parameters['pixelsize'] + '\'')
        if (len(parameters['diameter']) > 0):
            preset_pipeline_info_cmd += (' --particle_diameter ' + '\'' + parameters['diameter'] + '\'')
        if (len(parameters['ctf_resolution']) > 0):
            preset_pipeline_info_cmd += (' --ctf_fit_resolution ' + '\'' + parameters['ctf_resolution'] + '\'')
        if (len(parameters['symmetry']) > 0):
            preset_pipeline_info_cmd += (' --symmetry ' + '\'' + parameters['symmetry'] + '\'')
        if (len(parameters['gpu_num']) > 0):
            preset_pipeline_info_cmd += (' --gpu_num ' + '\'' + parameters['gpu_num'] + '\'')
        if (len(parameters['inference_gpu_ids']) > 0):
            preset_pipeline_info_cmd += (' --inference_gpu_ids ' + '\'' + parameters['inference_gpu_ids'] + '\'')
        if ((len(parameters['get_type']) > 0) and (len(parameters['cutoff_condition']) > 0)):
            if (parameters['get_type'] == 'num'):
                preset_pipeline_info_cmd += (' --get_top_particles_num ' + '\'' + parameters['cutoff_condition'] + '\'')
            elif (parameters['get_type'] == 'score'):
                preset_pipeline_info_cmd += (' --get_top_particles_score ' + '\'' + parameters['cutoff_condition'] + '\'')
        os.system(preset_pipeline_info_cmd)
    else:
        preset_pipeline_info_cmd = ('python ' + os.path.join(os.path.dirname(filedir), 'CryoWizard.py') +
                                    ' --MakePresetPipelineInfo' +
                                    ' --cryosparc_username \'' + cryosparc_username + '\'' +
                                    ' --cryosparc_password \'' + cryosparc_password + '\'' +
                                    ' --cryosparc_project ' + project +
                                    ' --cryowizard_job_uid ' + jobid +
                                    ' --preset_pipeline_type default')
        if new_preprocess_movie_source_job_uids is not None:
            preset_pipeline_info_cmd += (' --source_movie_job_uid ' + ' '.join(new_preprocess_movie_source_job_uids))
        if new_preprocess_micrograph_source_job_uids is not None:
            preset_pipeline_info_cmd += (' --source_micrograph_job_uid ' + ' '.join(new_preprocess_micrograph_source_job_uids))
        if new_preprocess_particle_source_job_uids is not None:
            preset_pipeline_info_cmd += (' --source_particle_job_uid ' + ' '.join(new_preprocess_particle_source_job_uids))
        if new_preprocess_cryoranker_source_job_uids is not None:
            preset_pipeline_info_cmd += (' --source_cryoranker_job_uid ' + ' '.join(new_preprocess_cryoranker_source_job_uids))
        os.system(preset_pipeline_info_cmd)

    # flask_socketio.emit('js_modify_cryowizard_external_job_action', {'project': project, 'workspace': workspace, 'new_external_jobid': new_cryowizard_job_uid})


@socketio.on('check_cryowizard_external_job_parameters_action')
def check_cryowizard_external_job_parameters_action(cryosparc_username, cryosparc_password, project, jobid):
    import initialize
    cryowizard_data_dir = initialize.get_cryowizard_job_data_path(cryosparc_username, cryosparc_password, project, jobid)
    if not os.path.exists(os.path.join(cryowizard_data_dir, 'parameters', 'base_parameters', 'cryowizard_preset_pipeline_info.json')):
        modify_cryowizard_external_job_action(cryosparc_username, cryosparc_password, project, jobid, None)
    parameters = toolbox.readjson(os.path.join(cryowizard_data_dir, 'parameters', 'base_parameters', 'cryowizard_preset_pipeline_info.json'))
    flask_socketio.emit('js_check_cryowizard_external_job_parameters_action', {'project': project, 'jobid': jobid, 'parameters': parameters})


@socketio.on('queue_cryowizard_external_job_action')
def queue_cryowizard_external_job_action(cryosparc_username, cryosparc_password, project, jobid, gui_parameters):
    import initialize
    cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(email=cryosparc_username, password=cryosparc_password)
    cryowizard_job = cshandle.find_external_job(project, jobid)
    workspace = cryowizard_job.doc['workspace_uids'][0]
    dealjobs = JobAPIs.DealJobs(cshandle, project, workspace, None)

    os.system('python ' + os.path.join(os.path.dirname(filedir), 'CryoWizard.py') +
              ' --KillPipeline' +
              ' --cryosparc_username \'' + cryosparc_username + '\'' +
              ' --cryosparc_password \'' + cryosparc_password + '\'' +
              ' --cryosparc_project ' + project +
              ' --cryowizard_job_uid ' + jobid)
    modify_cryowizard_external_job_action(cryosparc_username, cryosparc_password, project, jobid, gui_parameters)

    cryowizard_data_dir = initialize.get_cryowizard_job_data_path(cryosparc_username, cryosparc_password, project, jobid)
    parameters = toolbox.readjson(os.path.join(cryowizard_data_dir, 'parameters', 'base_parameters', 'cryowizard_preset_pipeline_info.json'))

    # create preset pipeline
    if (parameters['preset_pipeline_type'] == 'default'):
        create_preset_pipeline_cmd = ('python ' + os.path.join(os.path.dirname(filedir), 'CryoWizard.py') +
                                      ' --CreatePresetPipeline' +
                                      ' --preset_pipeline_type default' +
                                      ' --cryosparc_username \'' + cryosparc_username + '\'' +
                                      ' --cryosparc_password \'' + cryosparc_password + '\'' +
                                      ' --cryosparc_project ' + project +
                                      ' --cryosparc_workspace ' + workspace +
                                      ' --cryowizard_job_uid ' + jobid)
        if parameters['preset_pipeline_args']['source_movie_job_uid'] is not None:
            create_preset_pipeline_cmd += (' --source_movie_job_uid ' + ' '.join(parameters['preset_pipeline_args']['source_movie_job_uid']))
        if parameters['preset_pipeline_args']['source_micrograph_job_uid'] is not None:
            create_preset_pipeline_cmd += (' --source_micrograph_job_uid ' + ' '.join(parameters['preset_pipeline_args']['source_micrograph_job_uid']))
        if parameters['preset_pipeline_args']['source_particle_job_uid'] is not None:
            create_preset_pipeline_cmd += (' --source_particle_job_uid ' + ' '.join(parameters['preset_pipeline_args']['source_particle_job_uid']))
        if parameters['preset_pipeline_args']['inference_gpu_ids'] is not None:
            create_preset_pipeline_cmd += (' --inference_gpu_ids \'' + (str)(parameters['preset_pipeline_args']['inference_gpu_ids']) + '\'')
        if parameters['preset_pipeline_args']['raw_pixel_size'] is not None:
            create_preset_pipeline_cmd += (' --raw_pixel_size ' + '\'' + (str)(parameters['preset_pipeline_args']['raw_pixel_size']) + '\'')
        if parameters['preset_pipeline_args']['particle_diameter'] is not None:
            create_preset_pipeline_cmd += (' --particle_diameter ' + '\'' + (str)(parameters['preset_pipeline_args']['particle_diameter']) + '\'')
        if parameters['preset_pipeline_args']['ctf_fit_resolution'] is not None:
            create_preset_pipeline_cmd += (' --ctf_fit_resolution ' + '\'' + (str)(parameters['preset_pipeline_args']['ctf_fit_resolution']) + '\'')
        if parameters['preset_pipeline_args']['symmetry'] is not None:
            create_preset_pipeline_cmd += (' --symmetry ' + '\'' + (str)(parameters['preset_pipeline_args']['symmetry']) + '\'')
        if parameters['preset_pipeline_args']['gpu_num'] is not None:
            create_preset_pipeline_cmd += (' --gpu_num ' + '\'' + (str)(parameters['preset_pipeline_args']['gpu_num']) + '\'')
        os.system(create_preset_pipeline_cmd)

    elif (parameters['preset_pipeline_type'] == 'simpler'):
        create_preset_pipeline_cmd = ('python ' + os.path.join(os.path.dirname(filedir), 'CryoWizard.py') +
                                      ' --CreatePresetPipeline' +
                                      ' --preset_pipeline_type simpler' +
                                      ' --cryosparc_username \'' + cryosparc_username + '\'' +
                                      ' --cryosparc_password \'' + cryosparc_password + '\'' +
                                      ' --cryosparc_project ' + project +
                                      ' --cryosparc_workspace ' + workspace +
                                      ' --cryowizard_job_uid ' + jobid)
        if parameters['preset_pipeline_args']['source_movie_job_uid'] is not None:
            create_preset_pipeline_cmd += (' --source_movie_job_uid ' + ' '.join(parameters['preset_pipeline_args']['source_movie_job_uid']))
        if parameters['preset_pipeline_args']['source_micrograph_job_uid'] is not None:
            create_preset_pipeline_cmd += (' --source_micrograph_job_uid ' + ' '.join(parameters['preset_pipeline_args']['source_micrograph_job_uid']))
        if parameters['preset_pipeline_args']['source_particle_job_uid'] is not None:
            create_preset_pipeline_cmd += (' --source_particle_job_uid ' + ' '.join(parameters['preset_pipeline_args']['source_particle_job_uid']))
        if parameters['preset_pipeline_args']['inference_gpu_ids'] is not None:
            create_preset_pipeline_cmd += (' --inference_gpu_ids \'' + (str)(parameters['preset_pipeline_args']['inference_gpu_ids']) + '\'')
        if parameters['preset_pipeline_args']['raw_pixel_size'] is not None:
            create_preset_pipeline_cmd += (' --raw_pixel_size ' + '\'' + (str)(parameters['preset_pipeline_args']['raw_pixel_size']) + '\'')
        if parameters['preset_pipeline_args']['particle_diameter'] is not None:
            create_preset_pipeline_cmd += (' --particle_diameter ' + '\'' + (str)(parameters['preset_pipeline_args']['particle_diameter']) + '\'')
        if parameters['preset_pipeline_args']['ctf_fit_resolution'] is not None:
            create_preset_pipeline_cmd += (' --ctf_fit_resolution ' + '\'' + (str)(parameters['preset_pipeline_args']['ctf_fit_resolution']) + '\'')
        if parameters['preset_pipeline_args']['symmetry'] is not None:
            create_preset_pipeline_cmd += (' --symmetry ' + '\'' + (str)(parameters['preset_pipeline_args']['symmetry']) + '\'')
        if parameters['preset_pipeline_args']['gpu_num'] is not None:
            create_preset_pipeline_cmd += (' --gpu_num ' + '\'' + (str)(parameters['preset_pipeline_args']['gpu_num']) + '\'')
        os.system(create_preset_pipeline_cmd)

    elif (parameters['preset_pipeline_type'] == 'cryoranker_only'):
        create_preset_pipeline_cmd = ('python ' + os.path.join(os.path.dirname(filedir), 'CryoWizard.py') +
                                      ' --CreatePresetPipeline' +
                                      ' --preset_pipeline_type cryoranker_only' +
                                      ' --cryosparc_username \'' + cryosparc_username + '\'' +
                                      ' --cryosparc_password \'' + cryosparc_password + '\'' +
                                      ' --cryosparc_project ' + project +
                                      ' --cryosparc_workspace ' + workspace +
                                      ' --cryowizard_job_uid ' + jobid)
        if parameters['preset_pipeline_args']['source_movie_job_uid'] is not None:
            create_preset_pipeline_cmd += (' --source_movie_job_uid ' + ' '.join(parameters['preset_pipeline_args']['source_movie_job_uid']))
        if parameters['preset_pipeline_args']['source_micrograph_job_uid'] is not None:
            create_preset_pipeline_cmd += (' --source_micrograph_job_uid ' + ' '.join(parameters['preset_pipeline_args']['source_micrograph_job_uid']))
        if parameters['preset_pipeline_args']['source_particle_job_uid'] is not None:
            create_preset_pipeline_cmd += (' --source_particle_job_uid ' + ' '.join(parameters['preset_pipeline_args']['source_particle_job_uid']))
        if parameters['preset_pipeline_args']['inference_gpu_ids'] is not None:
            create_preset_pipeline_cmd += (' --inference_gpu_ids \'' + (str)(parameters['preset_pipeline_args']['inference_gpu_ids']) + '\'')
        if parameters['preset_pipeline_args']['raw_pixel_size'] is not None:
            create_preset_pipeline_cmd += (' --raw_pixel_size ' + '\'' + (str)(parameters['preset_pipeline_args']['raw_pixel_size']) + '\'')
        if parameters['preset_pipeline_args']['particle_diameter'] is not None:
            create_preset_pipeline_cmd += (' --particle_diameter ' + '\'' + (str)(parameters['preset_pipeline_args']['particle_diameter']) + '\'')
        if parameters['preset_pipeline_args']['ctf_fit_resolution'] is not None:
            create_preset_pipeline_cmd += (' --ctf_fit_resolution ' + '\'' + (str)(parameters['preset_pipeline_args']['ctf_fit_resolution']) + '\'')
        if parameters['preset_pipeline_args']['gpu_num'] is not None:
            create_preset_pipeline_cmd += (' --gpu_num ' + '\'' + (str)(parameters['preset_pipeline_args']['gpu_num']) + '\'')
        os.system(create_preset_pipeline_cmd)

    elif (parameters['preset_pipeline_type'] == 'cryoranker_get_top_particles'):
        create_preset_pipeline_cmd = ('python ' + os.path.join(os.path.dirname(filedir), 'CryoWizard.py') +
                                      ' --CreatePresetPipeline' +
                                      ' --preset_pipeline_type cryoranker_get_top_particles' +
                                      ' --cryosparc_username \'' + cryosparc_username + '\'' +
                                      ' --cryosparc_password \'' + cryosparc_password + '\'' +
                                      ' --cryosparc_project ' + project +
                                      ' --cryosparc_workspace ' + workspace +
                                      ' --cryowizard_job_uid ' + jobid)
        if parameters['preset_pipeline_args']['source_cryoranker_job_uid'] is not None:
            create_preset_pipeline_cmd += (' --source_cryoranker_job_uid ' + ' '.join(parameters['preset_pipeline_args']['source_cryoranker_job_uid']))
        if parameters['preset_pipeline_args']['get_top_particles_num'] is not None:
            create_preset_pipeline_cmd += (' --get_top_particles_num ' + '\'' + (str)(parameters['preset_pipeline_args']['get_top_particles_num']) + '\'')
        if parameters['preset_pipeline_args']['get_top_particles_score'] is not None:
            create_preset_pipeline_cmd += (' --get_top_particles_score ' + '\'' + (str)(parameters['preset_pipeline_args']['get_top_particles_score']) + '\'')
        os.system(create_preset_pipeline_cmd)

    elif (parameters['preset_pipeline_type'] == 'custom'):
        # create pipeline / modify parameters by user in web / cmd, do nothing here
        pass

    # run pipeline
    def run_cryowizard_pipeline(cryosparc_username, cryosparc_password, project, cryowizard_job_uid):
        os.system('python ' + os.path.join(os.path.dirname(filedir), 'CryoWizard.py') +
                  ' --RunPipeline' +
                  ' --cryosparc_username \'' + cryosparc_username + '\'' +
                  ' --cryosparc_password \'' + cryosparc_password + '\'' +
                  ' --cryosparc_project ' + project +
                  ' --cryowizard_job_uid ' + cryowizard_job_uid)
    def check_and_kill_cryowizard_pipeline(cryosparc_username, cryosparc_password, project, cryowizard_job_uid):
        cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(email=cryosparc_username, password=cryosparc_password)
        target_cryowizard_job = cshandle.find_external_job(project, cryowizard_job_uid)
        target_cryowizard_job.wait_for_status({'launched', 'started', 'running'})
        target_cryowizard_job.wait_for_done()
        os.system('python ' + os.path.join(os.path.dirname(filedir), 'CryoWizard.py') +
                  ' --KillPipeline' +
                  ' --cryosparc_username \'' + cryosparc_username + '\'' +
                  ' --cryosparc_password \'' + cryosparc_password + '\'' +
                  ' --cryosparc_project ' + project +
                  ' --cryowizard_job_uid ' + cryowizard_job_uid)

    initialize.make_pipeline(cryowizard_data_dir)
    initialize.make_cryowizard_connections(cryosparc_username, cryosparc_password, project, jobid)
    multithread.setthread(run_cryowizard_pipeline, cryosparc_username=cryosparc_username, cryosparc_password=cryosparc_password, project=project, cryowizard_job_uid=jobid)
    multithread.setthread(check_and_kill_cryowizard_pipeline, cryosparc_username=cryosparc_username, cryosparc_password=cryosparc_password, project=project, cryowizard_job_uid=jobid)

    # flask_socketio.emit('js_queue_cryowizard_external_job_action', {'project': project, 'workspace': workspace, 'new_external_jobid': new_external_job.uid})


@socketio.on('continue_cryowizard_external_job_action')
def continue_cryowizard_external_job_action(cryosparc_username, cryosparc_password, project, jobid):
    # run pipeline
    def run_cryowizard_pipeline(cryosparc_username, cryosparc_password, project, cryowizard_job_uid):
        os.system('python ' + os.path.join(os.path.dirname(filedir), 'CryoWizard.py') +
                  ' --RunPipeline' +
                  ' --cryosparc_username \'' + cryosparc_username + '\'' +
                  ' --cryosparc_password \'' + cryosparc_password + '\'' +
                  ' --cryosparc_project ' + project +
                  ' --cryowizard_job_uid ' + cryowizard_job_uid)
    def check_and_kill_cryowizard_pipeline(cryosparc_username, cryosparc_password, project, cryowizard_job_uid):
        cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(email=cryosparc_username, password=cryosparc_password)
        target_cryowizard_job = cshandle.find_external_job(project, cryowizard_job_uid)
        target_cryowizard_job.wait_for_status({'launched', 'started', 'running'})
        target_cryowizard_job.wait_for_done()
        os.system('python ' + os.path.join(os.path.dirname(filedir), 'CryoWizard.py') +
                  ' --KillPipeline' +
                  ' --cryosparc_username \'' + cryosparc_username + '\'' +
                  ' --cryosparc_password \'' + cryosparc_password + '\'' +
                  ' --cryosparc_project ' + project +
                  ' --cryowizard_job_uid ' + cryowizard_job_uid)

    os.system('python ' + os.path.join(os.path.dirname(filedir), 'CryoWizard.py') +
              ' --KillPipeline' +
              ' --cryosparc_username \'' + cryosparc_username + '\'' +
              ' --cryosparc_password \'' + cryosparc_password + '\'' +
              ' --cryosparc_project ' + project +
              ' --cryowizard_job_uid ' + jobid)

    multithread.setthread(run_cryowizard_pipeline, cryosparc_username=cryosparc_username, cryosparc_password=cryosparc_password, project=project, cryowizard_job_uid=jobid)
    multithread.setthread(check_and_kill_cryowizard_pipeline, cryosparc_username=cryosparc_username, cryosparc_password=cryosparc_password, project=project, cryowizard_job_uid=jobid)

    # flask_socketio.emit('js_continue_cryowizard_external_job_action', {'project': project, 'workspace': workspace, 'new_external_jobid': new_external_job.uid})





################################################################################################################################



########################################################### web part ###########################################################


@app.route('/')
def index():
    response = flask.make_response(flask.render_template('index.html'))
    return response


@socketio.on('web_create_cryowizard_external_job_action')
def web_create_cryowizard_external_job_action(target_workflow_name, cryosparc_username, cryosparc_password, project, workspace):
    import initialize
    new_cryowizard_job_uid = initialize.create_cryowizard_job(cryosparc_username, cryosparc_password, project, workspace, 'test')
    flask_socketio.emit('js_web_create_cryowizard_external_job_action_' + target_workflow_name, {'new_cryowizard_jobid': new_cryowizard_job_uid})


@socketio.on('web_check_cryowizard_external_job_existence_action')
def web_check_cryowizard_external_job_existence_action(target_workflow_name, cryosparc_username, cryosparc_password, project, jobid):
    try:
        cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(email=cryosparc_username, password=cryosparc_password)
        cryowizard_job = cshandle.find_external_job(project, jobid)
        cryowizard_existence = True
    except:
        cryowizard_existence = False
    flask_socketio.emit('js_web_check_cryowizard_external_job_existence_action_' + target_workflow_name, {'cryowizard_existence': cryowizard_existence})


@socketio.on('web_check_preset_pipeline_info_action')
def web_check_preset_pipeline_info_action(target_workflow_name, cryosparc_username, cryosparc_password, project, workspace, jobid, preset_pipeline_type):
    import initialize
    os.system('python ' + os.path.join(os.path.dirname(filedir), 'CryoWizard.py') +
              ' --KillPipeline' +
              ' --cryosparc_username \'' + cryosparc_username + '\'' +
              ' --cryosparc_password \'' + cryosparc_password + '\'' +
              ' --cryosparc_project ' + project +
              ' --cryowizard_job_uid ' + jobid)

    cryowizard_data_dir = initialize.get_cryowizard_job_data_path(cryosparc_username, cryosparc_password, project, jobid)
    if not os.path.exists(os.path.join(cryowizard_data_dir, 'parameters', 'base_parameters', 'cryowizard_preset_pipeline_info.json')):
        initialize.modify_used_preset_pipeline_info(cryowizard_data_dir, preset_pipeline_type, None)
    cryowizard_preset_pipeline_info = toolbox.readjson(os.path.join(cryowizard_data_dir, 'parameters', 'base_parameters', 'cryowizard_preset_pipeline_info.json'))
    flask_socketio.emit('js_web_check_preset_pipeline_info_action_' + target_workflow_name, {'preset_pipeline_info': cryowizard_preset_pipeline_info})


@socketio.on('web_add_preset_pipeline_action')
def web_add_preset_pipeline_action(target_workflow_name, cryosparc_username, cryosparc_password, project, workspace, jobid, preset_pipeline_type, preset_pipeline_parameters):
    import initialize
    os.system('python ' + os.path.join(os.path.dirname(filedir), 'CryoWizard.py') +
              ' --KillPipeline' +
              ' --cryosparc_username \'' + cryosparc_username + '\'' +
              ' --cryosparc_password \'' + cryosparc_password + '\'' +
              ' --cryosparc_project ' + project +
              ' --cryowizard_job_uid ' + jobid)
    os.system('python ' + os.path.join(os.path.dirname(filedir), 'CryoWizard.py') +
              ' --ClearAll' +
              ' --cryosparc_username \'' + cryosparc_username + '\'' +
              ' --cryosparc_password \'' + cryosparc_password + '\'' +
              ' --cryosparc_project ' + project +
              ' --cryowizard_job_uid ' + jobid)

    if preset_pipeline_type in ['custom']:
        os.system('python ' + os.path.join(os.path.dirname(filedir), 'CryoWizard.py') +
                  ' --CreateParameterFiles' +
                  ' --parameter_type base_parameters' +
                  ' --cryosparc_username \'' + cryosparc_username + '\'' +
                  ' --cryosparc_password \'' + cryosparc_password + '\'' +
                  ' --cryosparc_project ' + project +
                  ' --cryowizard_job_uid ' + jobid)
        modify_base_parameters_cmd = ('python ' + os.path.join(os.path.dirname(filedir), 'CryoWizard.py') +
                                      ' --ModifyParameterFiles' +
                                      ' --parameter_folder_name base_parameters' +
                                      ' --cryosparc_username \'' + cryosparc_username + '\'' +
                                      ' --cryosparc_password \'' + cryosparc_password + '\'' +
                                      ' --cryosparc_project ' + project +
                                      ' --cryosparc_workspace ' + workspace +
                                      ' --cryowizard_job_uid ' + jobid)
        for key, value in preset_pipeline_parameters.items():
            if value is not None:
                modify_base_parameters_cmd += (' --' + key + ' \'' + value + '\'')
        os.system(modify_base_parameters_cmd)
        print('web modify base parameters cmd:', modify_base_parameters_cmd, flush=True)
    else:
        create_preset_pipeline_cmd = ('python ' + os.path.join(os.path.dirname(filedir), 'CryoWizard.py') +
                                      ' --CreatePresetPipeline' +
                                      ' --preset_pipeline_type ' + preset_pipeline_type +
                                      ' --cryosparc_username \'' + cryosparc_username + '\'' +
                                      ' --cryosparc_password \'' + cryosparc_password + '\'' +
                                      ' --cryosparc_project ' + project +
                                      ' --cryosparc_workspace ' + workspace +
                                      ' --cryowizard_job_uid ' + jobid)
        for key, value in preset_pipeline_parameters.items():
            if value is not None:
                create_preset_pipeline_cmd += (' --' + key + ' \'' + value + '\'')
        os.system(create_preset_pipeline_cmd)
        print('web create pipeline cmd:', create_preset_pipeline_cmd, flush=True)

    flask_socketio.emit('js_web_add_preset_pipeline_action_' + target_workflow_name, {})


@socketio.on('web_add_single_pipeline_node_action')
def web_add_single_pipeline_node_action(target_workflow_name, cryosparc_username, cryosparc_password, project, jobid, pipeline_node_type):
    import initialize
    os.system('python ' + os.path.join(os.path.dirname(filedir), 'CryoWizard.py') +
              ' --KillPipeline' +
              ' --cryosparc_username \'' + cryosparc_username + '\'' +
              ' --cryosparc_password \'' + cryosparc_password + '\'' +
              ' --cryosparc_project ' + project +
              ' --cryowizard_job_uid ' + jobid)

    cryowizard_data_dir = initialize.get_cryowizard_job_data_path(cryosparc_username, cryosparc_password, project, jobid)
    new_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': pipeline_node_type})

    flask_socketio.emit('js_web_add_single_pipeline_node_action_' + target_workflow_name, {})


@socketio.on('web_delete_single_pipeline_node_action')
def web_delete_single_pipeline_node_action(target_workflow_name, cryosparc_username, cryosparc_password, project, jobid, pipeline_node_name):
    import initialize
    os.system('python ' + os.path.join(os.path.dirname(filedir), 'CryoWizard.py') +
              ' --KillPipeline' +
              ' --cryosparc_username \'' + cryosparc_username + '\'' +
              ' --cryosparc_password \'' + cryosparc_password + '\'' +
              ' --cryosparc_project ' + project +
              ' --cryowizard_job_uid ' + jobid)
    os.system('python ' + os.path.join(os.path.dirname(filedir), 'CryoWizard.py') +
              ' --ClearAll' +
              ' --cryosparc_username \'' + cryosparc_username + '\'' +
              ' --cryosparc_password \'' + cryosparc_password + '\'' +
              ' --cryosparc_project ' + project +
              ' --cryowizard_job_uid ' + jobid +
              ' --target_data_name ' + pipeline_node_name)

    flask_socketio.emit('js_web_delete_single_pipeline_node_action_' + target_workflow_name, {})


@socketio.on('web_pipeline_node_save_parameters_action')
def web_pipeline_node_save_parameters_action(target_workflow_name, cryosparc_username, cryosparc_password, project, jobid, pipeline_node_name, pipeline_node_parameters):
    import initialize
    create_preset_pipeline_cmd = ('python ' + os.path.join(os.path.dirname(filedir), 'CryoWizard.py') +
                                  ' --ModifyParameterFiles' +
                                  ' --parameter_folder_name ' + pipeline_node_name +
                                  ' --cryosparc_username \'' + cryosparc_username + '\'' +
                                  ' --cryosparc_password \'' + cryosparc_password + '\'' +
                                  ' --cryosparc_project ' + project +
                                  ' --cryowizard_job_uid ' + jobid)
    for key, value in pipeline_node_parameters.items():
        if value is not None:
            create_preset_pipeline_cmd += (' --' + key + ' \'' + value + '\'')
    os.system(create_preset_pipeline_cmd)

    flask_socketio.emit('js_web_pipeline_node_save_parameters_action_' + target_workflow_name, {})


@socketio.on('web_check_pipeline_nodes_action')
def web_check_pipeline_nodes_action(target_workflow_name, cryosparc_username, cryosparc_password, project, workspace, jobid):
    import initialize
    cryowizard_data_dir = initialize.get_cryowizard_job_data_path(cryosparc_username, cryosparc_password, project, jobid)
    if not os.path.exists(os.path.join(cryowizard_data_dir, 'parameters', 'base_parameters', 'cryowizard_preset_pipeline_info.json')):
        base_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'base_parameters'})
    else:
        base_parameters_folder_path = os.path.join(cryowizard_data_dir, 'parameters', 'base_parameters')
    os.system('python ' + os.path.join(os.path.dirname(filedir), 'CryoWizard.py') +
              ' --ModifyParameterFiles' +
              ' --parameter_folder_name base_parameters' +
              ' --cryosparc_username \'' + cryosparc_username + '\'' +
              ' --cryosparc_password \'' + cryosparc_password + '\'' +
              ' --cryosparc_project ' + project +
              ' --cryosparc_workspace ' + workspace +
              ' --cryowizard_job_uid ' + jobid)
    all_parameters_folder_info, used_single_parameters_folder_name_list, pipeline = initialize.make_pipeline(cryowizard_data_dir)

    all_single_parameters_folder_name_list = []
    all_single_parameters_folder_type_info = {}
    for single_parameters_folder_info_ptr in range(len(all_parameters_folder_info)):
        single_parameters_folder_name = all_parameters_folder_info[single_parameters_folder_info_ptr]['single_parameters_folder_name']
        single_parameters_folder_type = all_parameters_folder_info[single_parameters_folder_info_ptr]['single_parameters_folder_type']
        # single_parameters_folder_request_jobs = all_parameters_folder_info[single_parameters_folder_info_ptr]['single_parameters_folder_request_jobs']
        # single_parameters_folder_if_need_job_inputs = all_parameters_folder_info[single_parameters_folder_info_ptr]['single_parameters_folder_if_need_job_inputs']
        all_single_parameters_folder_name_list.append(single_parameters_folder_name)
        all_single_parameters_folder_type_info[single_parameters_folder_name] = single_parameters_folder_type
    unused_single_parameters_folder_name_list = toolbox.list_difference(all_single_parameters_folder_name_list, used_single_parameters_folder_name_list)

    if not os.path.exists(os.path.join(cryowizard_data_dir, 'parameters', 'base_parameters', 'cryowizard_preset_pipeline_info.json')):
        initialize.modify_used_preset_pipeline_info(cryowizard_data_dir, 'custom')
    cryowizard_preset_pipeline_info = toolbox.readjson(os.path.join(cryowizard_data_dir, 'parameters', 'base_parameters', 'cryowizard_preset_pipeline_info.json'))

    source_inputs_info = {}
    if os.path.exists(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', 'base_parameters', 'cmd_input_parameter_info_dict.json')):
        source_inputs_info['base_parameters'] = toolbox.readjson(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', 'base_parameters', 'cmd_input_parameter_info_dict.json'))
    all_parameter_type_folder = os.listdir(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters'))
    for single_parameter_type_folder in all_parameter_type_folder:
        if single_parameter_type_folder in ['import', 'preprocess', 'cryoranker', 'refine', 'postprocess']:
            single_parameter_type_folder_files_list = os.listdir(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', single_parameter_type_folder))
            for single_parameters_folder in single_parameter_type_folder_files_list:
                single_parameters_folder_head = single_parameters_folder.split('_')[0]
                if (single_parameters_folder_head == single_parameter_type_folder):
                    if os.path.exists(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', single_parameter_type_folder, single_parameters_folder, 'cmd_input_parameter_info_dict.json')):
                        source_inputs_info[single_parameters_folder] = toolbox.readjson(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', single_parameter_type_folder, single_parameters_folder, 'cmd_input_parameter_info_dict.json'))

    flask_socketio.emit('js_web_check_pipeline_nodes_action_' + target_workflow_name, {
        'pipeline': pipeline,
        'preset_pipeline_info': cryowizard_preset_pipeline_info,
        'all_single_parameters_folder_type_info': all_single_parameters_folder_type_info,
        'used_single_parameters_folder_name_list': used_single_parameters_folder_name_list,
        'unused_single_parameters_folder_name_list': unused_single_parameters_folder_name_list,
        'source_inputs_info': source_inputs_info
    })


@socketio.on('web_run_cryowizard_external_job_action')
def web_run_cryowizard_external_job_action(target_workflow_name, cryosparc_username, cryosparc_password, project, jobid):
    import initialize
    # run pipeline
    def run_cryowizard_pipeline(cryosparc_username, cryosparc_password, project, cryowizard_job_uid):
        os.system('python ' + os.path.join(os.path.dirname(filedir), 'CryoWizard.py') +
                  ' --RunPipeline' +
                  ' --cryosparc_username \'' + cryosparc_username + '\'' +
                  ' --cryosparc_password \'' + cryosparc_password + '\'' +
                  ' --cryosparc_project ' + project +
                  ' --cryowizard_job_uid ' + cryowizard_job_uid)
    def check_and_kill_cryowizard_pipeline(cryosparc_username, cryosparc_password, project, cryowizard_job_uid):
        cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(email=cryosparc_username, password=cryosparc_password)
        target_cryowizard_job = cshandle.find_external_job(project, cryowizard_job_uid)
        target_cryowizard_job.wait_for_status({'launched', 'started', 'running'})
        target_cryowizard_job.wait_for_done()
        os.system('python ' + os.path.join(os.path.dirname(filedir), 'CryoWizard.py') +
                  ' --KillPipeline' +
                  ' --cryosparc_username \'' + cryosparc_username + '\'' +
                  ' --cryosparc_password \'' + cryosparc_password + '\'' +
                  ' --cryosparc_project ' + project +
                  ' --cryowizard_job_uid ' + cryowizard_job_uid)

    os.system('python ' + os.path.join(os.path.dirname(filedir), 'CryoWizard.py') +
              ' --KillPipeline' +
              ' --cryosparc_username \'' + cryosparc_username + '\'' +
              ' --cryosparc_password \'' + cryosparc_password + '\'' +
              ' --cryosparc_project ' + project +
              ' --cryowizard_job_uid ' + jobid)
    os.system('python ' + os.path.join(os.path.dirname(filedir), 'CryoWizard.py') +
              ' --ClearMetadata' +
              ' --cryosparc_username \'' + cryosparc_username + '\'' +
              ' --cryosparc_password \'' + cryosparc_password + '\'' +
              ' --cryosparc_project ' + project +
              ' --cryowizard_job_uid ' + jobid)

    cryowizard_data_dir = initialize.get_cryowizard_job_data_path(cryosparc_username, cryosparc_password, project, jobid)
    initialize.make_pipeline(cryowizard_data_dir)
    initialize.make_cryowizard_connections(cryosparc_username, cryosparc_password, project, jobid)
    multithread.setthread(run_cryowizard_pipeline, cryosparc_username=cryosparc_username, cryosparc_password=cryosparc_password, project=project, cryowizard_job_uid=jobid)
    multithread.setthread(check_and_kill_cryowizard_pipeline, cryosparc_username=cryosparc_username, cryosparc_password=cryosparc_password, project=project, cryowizard_job_uid=jobid)

    # flask_socketio.emit('js_web_run_cryowizard_external_job_action_' + target_workflow_name, {})


@socketio.on('web_continue_cryowizard_external_job_action')
def web_continue_cryowizard_external_job_action(target_workflow_name, cryosparc_username, cryosparc_password, project, jobid):
    import initialize
    # run pipeline
    def run_cryowizard_pipeline(cryosparc_username, cryosparc_password, project, cryowizard_job_uid):
        os.system('python ' + os.path.join(os.path.dirname(filedir), 'CryoWizard.py') +
                  ' --RunPipeline' +
                  ' --cryosparc_username \'' + cryosparc_username + '\'' +
                  ' --cryosparc_password \'' + cryosparc_password + '\'' +
                  ' --cryosparc_project ' + project +
                  ' --cryowizard_job_uid ' + cryowizard_job_uid)
    def check_and_kill_cryowizard_pipeline(cryosparc_username, cryosparc_password, project, cryowizard_job_uid):
        cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(email=cryosparc_username, password=cryosparc_password)
        target_cryowizard_job = cshandle.find_external_job(project, cryowizard_job_uid)
        target_cryowizard_job.wait_for_status({'launched', 'started', 'running'})
        target_cryowizard_job.wait_for_done()
        os.system('python ' + os.path.join(os.path.dirname(filedir), 'CryoWizard.py') +
                  ' --KillPipeline' +
                  ' --cryosparc_username \'' + cryosparc_username + '\'' +
                  ' --cryosparc_password \'' + cryosparc_password + '\'' +
                  ' --cryosparc_project ' + project +
                  ' --cryowizard_job_uid ' + cryowizard_job_uid)

    os.system('python ' + os.path.join(os.path.dirname(filedir), 'CryoWizard.py') +
              ' --KillPipeline' +
              ' --cryosparc_username \'' + cryosparc_username + '\'' +
              ' --cryosparc_password \'' + cryosparc_password + '\'' +
              ' --cryosparc_project ' + project +
              ' --cryowizard_job_uid ' + jobid)

    multithread.setthread(run_cryowizard_pipeline, cryosparc_username=cryosparc_username, cryosparc_password=cryosparc_password, project=project, cryowizard_job_uid=jobid)
    multithread.setthread(check_and_kill_cryowizard_pipeline, cryosparc_username=cryosparc_username, cryosparc_password=cryosparc_password, project=project, cryowizard_job_uid=jobid)

    # flask_socketio.emit('js_web_continue_cryowizard_external_job_action_' + target_workflow_name, {})


@socketio.on('web_kill_cryowizard_external_job_action')
def web_kill_cryowizard_external_job_action(target_workflow_name, cryosparc_username, cryosparc_password, project, jobid):
    os.system('python ' + os.path.join(os.path.dirname(filedir), 'CryoWizard.py') +
              ' --KillPipeline' +
              ' --cryosparc_username \'' + cryosparc_username + '\'' +
              ' --cryosparc_password \'' + cryosparc_password + '\'' +
              ' --cryosparc_project ' + project +
              ' --cryowizard_job_uid ' + jobid)
    # flask_socketio.emit('js_web_kill_cryowizard_external_job_action_' + target_workflow_name, {})


@socketio.on('web_clear_cryowizard_external_job_metadata_action')
def web_clear_cryowizard_external_job_metadata_action(target_workflow_name, cryosparc_username, cryosparc_password, project, jobid):
    os.system('python ' + os.path.join(os.path.dirname(filedir), 'CryoWizard.py') +
              ' --KillPipeline' +
              ' --cryosparc_username \'' + cryosparc_username + '\'' +
              ' --cryosparc_password \'' + cryosparc_password + '\'' +
              ' --cryosparc_project ' + project +
              ' --cryowizard_job_uid ' + jobid)
    os.system('python ' + os.path.join(os.path.dirname(filedir), 'CryoWizard.py') +
              ' --ClearMetadata' +
              ' --cryosparc_username \'' + cryosparc_username + '\'' +
              ' --cryosparc_password \'' + cryosparc_password + '\'' +
              ' --cryosparc_project ' + project +
              ' --cryowizard_job_uid ' + jobid)
    # flask_socketio.emit('js_web_clear_cryowizard_external_job_metadata_action_' + target_workflow_name, {})


@socketio.on('web_show_cryowizard_external_job_results_action')
def web_show_cryowizard_external_job_results_action(target_workflow_name, cryosparc_username, cryosparc_password, project, jobid):
    import initialize
    cryowizard_data_dir = initialize.get_cryowizard_job_data_path(cryosparc_username, cryosparc_password, project, jobid)
    response_data = []
    if os.path.exists(os.path.join(cryowizard_data_dir, 'metadata', 'cryowizard.log')):
        with open(os.path.join(cryowizard_data_dir, 'metadata', 'cryowizard.log'), 'r') as f:
            response_data = f.readlines()
    flask_socketio.emit('js_web_show_cryowizard_external_job_results_action_' + target_workflow_name, {'response': response_data})


@app.route('/DownloadMap', methods=['GET'])
def DownloadMap():
    import initialize
    cryosparc_username = flask.request.args.get('username')
    cryosparc_password = flask.request.args.get('password')
    project = flask.request.args.get('project')
    jobid = flask.request.args.get('jobuid')

    cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(email=cryosparc_username, password=cryosparc_password)
    cryowizard_job = cshandle.find_external_job(project, jobid)
    workspace = cryowizard_job.doc['workspace_uids'][0]
    dealjobs = JobAPIs.DealJobs(cshandle, project, workspace, None)

    cryowizard_data_dir = initialize.get_cryowizard_job_data_path(cryosparc_username, cryosparc_password, project, jobid)
    if os.path.exists(os.path.join(cryowizard_data_dir, 'metadata', 'best_volume.json')):
        try:
            best_volume_info = toolbox.readjson(os.path.join(cryowizard_data_dir, 'metadata', 'best_volume.json'))
            best_final_nurefine_job_uid = best_volume_info['jobuid']
            best_final_nurefine_job = dealjobs.cshandle.find_job(dealjobs.project, best_final_nurefine_job_uid)
            best_final_nurefine_job_volume_dataset = best_final_nurefine_job.load_output('volume')
            # print(best_final_nurefine_job_volume_dataset, flush=True)
            return flask.send_file(os.path.join(dealjobs.GetProjectPath(), best_final_nurefine_job_volume_dataset[0]['map_sharp/path']), as_attachment=True)
        except:
            return '<div>Map download failed...</div><script type="text/javascript">setTimeout(function(){window.close();}, 5000);</script>'
    else:
        return '<div>Job did not finish yet, please wait...</div><script type="text/javascript">setTimeout(function(){window.close();}, 5000);</script>'








################################################################################################################################



def startup_gui(gui_port):
    cryowizard_settings = toolbox.readyaml(os.path.join(filedir, 'cryowizard_settings.yml'))
    if gui_port is None:
        final_gui_port = cryowizard_settings['CryoWizard_settings']['GUI']['gui_port']
    else:
        final_gui_port = gui_port
    print('Web service start, press Ctrl+C to quit if you want to stop this web service. (GUI port: ' + (str)(final_gui_port) + ')', flush=True)
    print('For the user tutorial and full documentation of CryoWizard, please refer to: https://github.com/SMART-StructBio-AI/CryoWizard', flush=True)
    socketio.run(app, host='0.0.0.0', port=final_gui_port)