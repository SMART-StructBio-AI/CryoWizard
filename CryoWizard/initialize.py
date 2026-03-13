#!/usr/bin/env python

import numpy as np
import math
import shutil
import copy
import os

import sys
sys.path.append(os.path.dirname(__file__))

import cryowizardlib.JobAPIs as JobAPIs
import cryowizardlib.Toolbox as toolbox



def install(user_email, user_password, license, hostname, port, cryoranker_model_weight_path, other_args):

    def get_job_parameters(cshandle, job_name_list, job_parameters_map_save_path, job_name_save_path, ignore_param_list=['random_seed']):
        # get all_job_parameters
        specs = cshandle.get_job_specs()
        all_job_parameters = {}
        for i in range(len(specs)):
            for j in range(len(specs[i]['contains'])):
                job_name = specs[i]['contains'][j]['name']
                job_parameters = {}
                for param in specs[i]['contains'][j]['params_base']:
                    job_parameters[param] = {'title': specs[i]['contains'][j]['params_base'][param]['title'], 'default_value': specs[i]['contains'][j]['params_base'][param]['value']}
                all_job_parameters[job_name] = job_parameters
        # get target job parameters
        for job_name_ptr in range(len(job_name_list)):
            job_name = job_name_list[job_name_ptr]
            if job_name in all_job_parameters:
                job_parameters = {}
                job_parameters_map = {}
                selected_job_name = job_name
                for param in all_job_parameters[job_name]:
                    if param in ignore_param_list:
                        continue
                    job_parameters[all_job_parameters[job_name][param]['title']] = all_job_parameters[job_name][param]['default_value']
                    job_parameters_map[all_job_parameters[job_name][param]['title']] = param
                toolbox.savetojson(job_parameters_map, job_parameters_map_save_path)
                toolbox.savetojson(selected_job_name, job_name_save_path)
                return job_parameters
        return None

    filedir = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
    if not JobAPIs.check_cryosparc_tools_version('4.5'):
        print('CryoSPARC/cryosparc-tools version could not be lower than 4.5, installation fail', flush=True)
        return

    # create license file
    toolbox.savetojson({'license': (str)(license), 'host': (str)(hostname), 'port': (int)(port)}, os.path.join(filedir, 'CryoWizard', 'parameters', 'cs_login_info.json'))

    # save model weight info
    ## cryoranker
    if os.path.exists(os.path.join(os.path.normpath(cryoranker_model_weight_path), 'cryo_ranker_v1.5_vit_b_model.safetensors')):
        cryoranker_inference_settings = toolbox.readyaml(os.path.join(filedir, 'CryoRanker', 'CryoRanker', 'cryoranker_inference_settings.yml'))
        cryoranker_inference_settings['path_model_proj'] = os.path.normpath(cryoranker_model_weight_path)
        toolbox.savetoyaml(cryoranker_inference_settings, os.path.join(filedir, 'CryoRanker', 'CryoRanker', 'cryoranker_inference_settings.yml'))
    else:
        print('cryo_ranker_v1.5_vit_b_model.safetensors do not exist in ' + cryoranker_model_weight_path + ', installation fail', flush=True)
        return
    ## other models in the future...

    # create cryowizard cache path
    if os.path.exists(os.path.join(filedir, 'CryoWizard', 'cryowizardcache')):
        shutil.rmtree(os.path.join(filedir, 'CryoWizard', 'cryowizardcache'))
    os.makedirs(os.path.join(filedir, 'CryoWizard', 'cryowizardcache'))

    # pack extension.zip
    if os.path.exists(os.path.join(filedir, 'extension.zip')):
        os.remove(os.path.join(filedir, 'extension.zip'))
    toolbox.packtozip(os.path.join(filedir, 'CryoWizard', 'cryowizardgui', 'extension'), False, True)
    shutil.move(os.path.join(filedir, 'CryoWizard', 'cryowizardgui', 'extension.zip'), os.path.join(filedir, 'extension.zip'))

    # create cryosparc job parameters
    import cryowizardlib.CSLogin as CSLogin
    cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(email=user_email, password=user_password)
    cryowizard_settings = toolbox.readyaml(os.path.join(filedir, 'CryoWizard', 'cryowizard_settings.yml'))
    if other_args.cryosparc_lane is not None:
        cryowizard_settings['CryoWizard_settings']['BaseParameters']['lane'] = other_args.cryosparc_lane
    if other_args.slurm is not None:
        if other_args.slurm in ['true', 'True', 'yes', 'Yes', 'y', 'Y']:
            cryowizard_settings['CryoWizard_settings']['BaseParameters']['if_slurm'] = True
        elif other_args.slurm in ['false', 'False', 'no', 'No', 'n', 'N']:
            cryowizard_settings['CryoWizard_settings']['BaseParameters']['if_slurm'] = False
    cryowizard_settings['CryoSPARC_job_settings'] = {}

    import_movies_job_name_list = ['import_movies']
    import_micrographs_job_name_list = ['import_micrographs']
    import_particle_stack_job_name_list = ['import_particles']
    import_volume_job_name_list = ['import_volumes']
    patch_motion_correction_job_name_list = ['patch_motion_correction_multi']
    patch_ctf_estimation_job_name_list = ['patch_ctf_estimation_multi']
    blob_picker_job_name_list = ['blob_picker_gpu']
    template_picker_job_name_list = ['template_picker_gpu']
    create_templates_job_name_list = ['create_templates']
    extract_from_micrographs_job_name_list = ['extract_micrographs_multi']
    classification_2d_job_name_list = ['class_2D_new']
    reference_select_2d_job_name_list = ['reference_select_2D']
    junk_detector_job_name_list = ['junk_detector_v1']
    abinit_job_name_list = ['homo_abinit']
    nurefine_job_name_list = ['nonuniform_refine_new', 'nonuniform_refine']
    reference_motion_correction_job_name_list = ['reference_motion_correction']
    ctf_refine_global_job_name_list = ['ctf_refine_global']
    ctf_refine_local_job_name_list = ['ctf_refine_local']
    restack_particles_job_name_list = ['restack_particles']
    particle_set_tools_job_name_list = ['particle_sets']
    curate_exposures_job_name_list = ['curate_exposures_v2']
    orientation_diagnostics_job_name_list = ['orientation_diagnostics']

    cryowizard_settings['CryoSPARC_job_settings']['ImportMovies'] = get_job_parameters(cshandle, import_movies_job_name_list, os.path.join(filedir, 'CryoWizard', 'parameters', 'import_movies_parameters_map.json'), os.path.join(filedir, 'CryoWizard', 'parameters', 'import_movies_job_name.json'))
    cryowizard_settings['CryoSPARC_job_settings']['ImportMicrographs'] = get_job_parameters(cshandle, import_micrographs_job_name_list, os.path.join(filedir, 'CryoWizard', 'parameters', 'import_micrographs_parameters_map.json'), os.path.join(filedir, 'CryoWizard', 'parameters', 'import_micrographs_job_name.json'))
    cryowizard_settings['CryoSPARC_job_settings']['ImportParticleStack'] = get_job_parameters(cshandle, import_particle_stack_job_name_list, os.path.join(filedir, 'CryoWizard', 'parameters', 'import_particle_stack_parameters_map.json'), os.path.join(filedir, 'CryoWizard', 'parameters', 'import_particle_stack_job_name.json'))
    cryowizard_settings['CryoSPARC_job_settings']['ImportVolume'] = get_job_parameters(cshandle, import_volume_job_name_list, os.path.join(filedir, 'CryoWizard', 'parameters', 'import_volume_parameters_map.json'), os.path.join(filedir, 'CryoWizard', 'parameters', 'import_volume_job_name.json'))
    cryowizard_settings['CryoSPARC_job_settings']['PatchMotionCorrection'] = get_job_parameters(cshandle, patch_motion_correction_job_name_list, os.path.join(filedir, 'CryoWizard', 'parameters', 'patch_motion_correction_parameters_map.json'), os.path.join(filedir, 'CryoWizard', 'parameters', 'patch_motion_correction_job_name.json'))
    cryowizard_settings['CryoSPARC_job_settings']['PatchCTFEstimation'] = get_job_parameters(cshandle, patch_ctf_estimation_job_name_list, os.path.join(filedir, 'CryoWizard', 'parameters', 'patch_ctf_estimation_parameters_map.json'), os.path.join(filedir, 'CryoWizard', 'parameters', 'patch_ctf_estimation_job_name.json'))
    cryowizard_settings['CryoSPARC_job_settings']['BlobPicker'] = get_job_parameters(cshandle, blob_picker_job_name_list, os.path.join(filedir, 'CryoWizard', 'parameters', 'blob_picker_parameters_map.json'), os.path.join(filedir, 'CryoWizard', 'parameters', 'blob_picker_job_name.json'))
    cryowizard_settings['CryoSPARC_job_settings']['TemplatePicker'] = get_job_parameters(cshandle, template_picker_job_name_list, os.path.join(filedir, 'CryoWizard', 'parameters', 'template_picker_parameters_map.json'), os.path.join(filedir, 'CryoWizard', 'parameters', 'template_picker_job_name.json'))
    cryowizard_settings['CryoSPARC_job_settings']['CreateTemplates'] = get_job_parameters(cshandle, create_templates_job_name_list, os.path.join(filedir, 'CryoWizard', 'parameters', 'create_templates_parameters_map.json'), os.path.join(filedir, 'CryoWizard', 'parameters', 'create_templates_job_name.json'))
    cryowizard_settings['CryoSPARC_job_settings']['ExtractFromMicrographs'] = get_job_parameters(cshandle, extract_from_micrographs_job_name_list, os.path.join(filedir, 'CryoWizard', 'parameters', 'extract_micrographs_parameters_map.json'), os.path.join(filedir, 'CryoWizard', 'parameters', 'extract_micrographs_job_name.json'))
    cryowizard_settings['CryoSPARC_job_settings']['AbInitialReconstruction'] = get_job_parameters(cshandle, abinit_job_name_list, os.path.join(filedir, 'CryoWizard', 'parameters', 'abinit_parameters_map.json'), os.path.join(filedir, 'CryoWizard', 'parameters', 'abinit_job_name.json'))
    cryowizard_settings['CryoSPARC_job_settings']['NonUniformRefinement_initial'] = get_job_parameters(cshandle, nurefine_job_name_list, os.path.join(filedir, 'CryoWizard', 'parameters', 'nurefine_parameters_map.json'), os.path.join(filedir, 'CryoWizard', 'parameters', 'nurefine_job_name.json'))
    cryowizard_settings['CryoSPARC_job_settings']['NonUniformRefinement_final'] = copy.deepcopy(cryowizard_settings['CryoSPARC_job_settings']['NonUniformRefinement_initial'])
    cryowizard_settings['CryoSPARC_job_settings']['RestackParticles'] = get_job_parameters(cshandle, restack_particles_job_name_list, os.path.join(filedir, 'CryoWizard', 'parameters', 'restack_particles_parameters_map.json'), os.path.join(filedir, 'CryoWizard', 'parameters', 'restack_particles_job_name.json'))
    cryowizard_settings['CryoSPARC_job_settings']['ReferenceMotionCorrection'] = get_job_parameters(cshandle, reference_motion_correction_job_name_list, os.path.join(filedir, 'CryoWizard', 'parameters', 'reference_motion_correction_parameters_map.json'), os.path.join(filedir, 'CryoWizard', 'parameters', 'reference_motion_correction_job_name.json'))
    cryowizard_settings['CryoSPARC_job_settings']['CTFRefineGlobal'] = get_job_parameters(cshandle, ctf_refine_global_job_name_list, os.path.join(filedir, 'CryoWizard', 'parameters', 'ctf_refine_global_parameters_map.json'), os.path.join(filedir, 'CryoWizard', 'parameters', 'ctf_refine_global_job_name.json'))
    cryowizard_settings['CryoSPARC_job_settings']['CTFRefineLocal'] = get_job_parameters(cshandle, ctf_refine_local_job_name_list, os.path.join(filedir, 'CryoWizard', 'parameters', 'ctf_refine_local_parameters_map.json'), os.path.join(filedir, 'CryoWizard', 'parameters', 'ctf_refine_local_job_name.json'))
    cryowizard_settings['CryoSPARC_job_settings']['ParticleSetsTool'] = get_job_parameters(cshandle, particle_set_tools_job_name_list, os.path.join(filedir, 'CryoWizard', 'parameters', 'particle_set_tools_parameters_map.json'), os.path.join(filedir, 'CryoWizard', 'parameters', 'particle_set_tools_job_name.json'))
    cryowizard_settings['CryoSPARC_job_settings']['CurateExposures'] = get_job_parameters(cshandle, curate_exposures_job_name_list, os.path.join(filedir, 'CryoWizard', 'parameters', 'curate_exposures_parameters_map.json'), os.path.join(filedir, 'CryoWizard', 'parameters', 'curate_exposures_job_name.json'))
    cryowizard_settings['CryoSPARC_job_settings']['OrientationDiagnostics_initial'] = get_job_parameters(cshandle, orientation_diagnostics_job_name_list, os.path.join(filedir, 'CryoWizard', 'parameters', 'orientation_diagnostics_parameters_map.json'), os.path.join(filedir, 'CryoWizard', 'parameters', 'orientation_diagnostics_job_name.json'))
    cryowizard_settings['CryoSPARC_job_settings']['OrientationDiagnostics_final'] = copy.deepcopy(cryowizard_settings['CryoSPARC_job_settings']['OrientationDiagnostics_initial'])

    # modify some default parameters
    cryowizard_settings['CryoSPARC_job_settings']['RestackParticles']['Particle batch size'] = 1000
    cryowizard_settings['CryoSPARC_job_settings']['NonUniformRefinement_initial']['Number of extra final passes'] = 3
    cryowizard_settings['CryoSPARC_job_settings']['NonUniformRefinement_initial']['Initial lowpass resolution (A)'] = 15
    cryowizard_settings['CryoSPARC_job_settings']['NonUniformRefinement_final']['Number of extra final passes'] = 3
    cryowizard_settings['CryoSPARC_job_settings']['NonUniformRefinement_final']['Initial lowpass resolution (A)'] = 15
    cryowizard_settings['CryoSPARC_job_settings']['CurateExposures']['CTF fit resolution (Å)'] = '0,8'

    if JobAPIs.check_cryosparc_tools_version('4.7'):
        cryowizard_settings['CryoSPARC_job_settings']['2DClassification'] = get_job_parameters(cshandle, classification_2d_job_name_list, os.path.join(filedir, 'CryoWizard', 'parameters', '2d_classification_parameters_map.json'), os.path.join(filedir, 'CryoWizard', 'parameters', '2d_classification_job_name.json'))
        cryowizard_settings['CryoSPARC_job_settings']['ReferenceBasedAutoSelect2D'] = get_job_parameters(cshandle, reference_select_2d_job_name_list, os.path.join(filedir, 'CryoWizard', 'parameters', 'reference_select_2d_parameters_map.json'), os.path.join(filedir, 'CryoWizard', 'parameters', 'reference_select_2d_job_name.json'))
        cryowizard_settings['CryoSPARC_job_settings']['JunkDetector'] = get_job_parameters(cshandle, junk_detector_job_name_list, os.path.join(filedir, 'CryoWizard', 'parameters', 'junk_detector_parameters_map.json'), os.path.join(filedir, 'CryoWizard', 'parameters', 'junk_detector_job_name.json'))
        # modify some default parameters
        cryowizard_settings['CryoSPARC_job_settings']['2DClassification']['Number of final full iterations'] = 3
        cryowizard_settings['CryoSPARC_job_settings']['2DClassification']['Number of online-EM iterations'] = 40
        cryowizard_settings['CryoSPARC_job_settings']['2DClassification']['Batchsize per class'] = 400
        cryowizard_settings['CryoSPARC_job_settings']['2DClassification']['Remove duplicate particles'] = False
        cryowizard_settings['CryoSPARC_job_settings']['ReferenceBasedAutoSelect2D']['Exclude classes worse than resolution (A)'] = 30
        cryowizard_settings['CryoSPARC_job_settings']['ReferenceBasedAutoSelect2D']['Maximum Sobel score'] = 3.0
        cryowizard_settings['CryoSPARC_job_settings']['ReferenceBasedAutoSelect2D']['Minimum Correlation score'] = 0.5
    else:
        print('Warning: CryoSPARC/cryosparc-tools version is lower than 4.7, junk_detector and reference_based_auto_select_2d function would be not available (CryoWizard core features and preset pipelines would not be affected)', flush=True)

    toolbox.savetoyaml(cryowizard_settings, os.path.join(filedir, 'CryoWizard', 'cryowizard_settings.yml'))


def create_cryowizard_job(cryosparc_username, cryosparc_password, project, workspace, lane, title='CryoWizard'):

    import cryowizardlib.CSLogin as CSLogin

    cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(email=cryosparc_username, password=cryosparc_password)
    dealjobs = JobAPIs.DealJobs(cshandle, project, workspace, lane)

    project_handle = dealjobs.cshandle.find_project(dealjobs.project)
    new_cryowizard_job = project_handle.create_external_job(dealjobs.workspace, title=title)

    add_input_movie_name = 'input_movies'
    add_input_micrograph_name = 'input_micrographs'
    add_input_particle_name = 'input_particles'
    add_input_ranker_name = 'input_cryorankers'
    add_input_template_name = 'input_templates'
    add_input_volume_name = 'input_volumes'
    add_input_mask_name = 'input_masks'
    new_cryowizard_job.add_input(type='exposure', name=add_input_movie_name, min=0, title='Input Movie')
    new_cryowizard_job.add_input(type='exposure', name=add_input_micrograph_name, min=0, title='Input Micrograph')
    new_cryowizard_job.add_input(type='particle', name=add_input_particle_name, min=0, title='Input Particle')
    new_cryowizard_job.add_input(type='particle', name=add_input_ranker_name, min=0, title='Input CryoRanker')
    new_cryowizard_job.add_input(type='template', name=add_input_template_name, min=0, title='Input Template')
    new_cryowizard_job.add_input(type='volume', name=add_input_volume_name, min=0, title='Input Volume')
    new_cryowizard_job.add_input(type='mask', name=add_input_mask_name, min=0, title='Input Mask')

    if not os.path.exists(os.path.join(dealjobs.GetProjectPath(), new_cryowizard_job.uid, 'cryowizard')):
        os.makedirs(os.path.join(dealjobs.GetProjectPath(), new_cryowizard_job.uid, 'cryowizard'))

    return new_cryowizard_job.uid


def get_cryowizard_job_data_path(cryosparc_username, cryosparc_password, project, cryowizard_job_uid):
    # path to .../Jxxx/cryowizard
    import cryowizardlib.CSLogin as CSLogin
    cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(email=cryosparc_username, password=cryosparc_password)
    return os.path.join(os.path.normpath((str)(cshandle.find_project(project).dir())), cryowizard_job_uid, 'cryowizard')


def modify_used_preset_pipeline_info(cryowizard_data_dir, preset_pipeline_type, args=None):
    source_python_file_path = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
    cryowizard_settings = toolbox.readyaml(os.path.join(source_python_file_path, 'CryoWizard', 'cryowizard_settings.yml'))
    cryowizard_preset_pipeline_info = {
        'preset_pipeline_type': preset_pipeline_type,
        'preset_pipeline_args': {
            'cryosparc_lane': cryowizard_settings['CryoWizard_settings']['BaseParameters']['lane'],
            'slurm': cryowizard_settings['CryoWizard_settings']['BaseParameters']['if_slurm'],
            'inference_gpu_ids': cryowizard_settings['CryoWizard_settings']['BaseParameters']['inference_gpu_ids'],
            'source_movie_job_uid': None,
            'source_micrograph_job_uid': None,
            'source_particle_job_uid': None,
            'source_cryoranker_job_uid': None,
            'movies_data_path': None,
            'gain_reference_path': None,
            'micrographs_data_path': None,
            'particles_data_path': None,
            'particles_meta_path': None,
            'accelerating_voltage': None,
            'spherical_aberration': None,
            'total_exposure_dose': None,
            'raw_pixel_size': 1.0,
            'particle_diameter': 100,
            'ctf_fit_resolution': '0,6',
            'symmetry': 'C1',
            'gpu_num': 1,
            'get_top_particles_num': None,
            'get_top_particles_score': None,
        }
    }
    if args is not None:
        if args.cryosparc_lane is not None:
            cryowizard_preset_pipeline_info['preset_pipeline_args']['cryosparc_lane'] = args.cryosparc_lane
        if args.slurm is not None:
            if args.slurm in ['true', 'True', 'yes', 'Yes', 'y', 'Y']:
                cryowizard_preset_pipeline_info['preset_pipeline_args']['slurm'] = True
            elif args.slurm in ['false', 'False', 'no', 'No', 'n', 'N']:
                cryowizard_preset_pipeline_info['preset_pipeline_args']['slurm'] = False
        if args.inference_gpu_ids is not None:
            cryowizard_preset_pipeline_info['preset_pipeline_args']['inference_gpu_ids'] = args.inference_gpu_ids
        if args.source_movie_job_uid is not None:
            cryowizard_preset_pipeline_info['preset_pipeline_args']['source_movie_job_uid'] = args.source_movie_job_uid
        if args.source_micrograph_job_uid is not None:
            cryowizard_preset_pipeline_info['preset_pipeline_args']['source_micrograph_job_uid'] = args.source_micrograph_job_uid
        if args.source_particle_job_uid is not None:
            cryowizard_preset_pipeline_info['preset_pipeline_args']['source_particle_job_uid'] = args.source_particle_job_uid
        if args.source_cryoranker_job_uid is not None:
            cryowizard_preset_pipeline_info['preset_pipeline_args']['source_cryoranker_job_uid'] = args.source_cryoranker_job_uid
        if args.movies_data_path is not None:
            cryowizard_preset_pipeline_info['preset_pipeline_args']['movies_data_path'] = args.movies_data_path
        if args.gain_reference_path is not None:
            cryowizard_preset_pipeline_info['preset_pipeline_args']['gain_reference_path'] = args.gain_reference_path
        if args.micrographs_data_path is not None:
            cryowizard_preset_pipeline_info['preset_pipeline_args']['micrographs_data_path'] = args.micrographs_data_path
        if args.particles_data_path is not None:
            cryowizard_preset_pipeline_info['preset_pipeline_args']['particles_data_path'] = args.particles_data_path
        if args.particles_meta_path is not None:
            cryowizard_preset_pipeline_info['preset_pipeline_args']['particles_meta_path'] = args.particles_meta_path
        if args.accelerating_voltage is not None:
            cryowizard_preset_pipeline_info['preset_pipeline_args']['accelerating_voltage'] = args.accelerating_voltage
        if args.spherical_aberration is not None:
            cryowizard_preset_pipeline_info['preset_pipeline_args']['spherical_aberration'] = args.spherical_aberration
        if args.total_exposure_dose is not None:
            cryowizard_preset_pipeline_info['preset_pipeline_args']['total_exposure_dose'] = args.total_exposure_dose
        if args.raw_pixel_size is not None:
            cryowizard_preset_pipeline_info['preset_pipeline_args']['raw_pixel_size'] = args.raw_pixel_size
        if args.particle_diameter is not None:
            cryowizard_preset_pipeline_info['preset_pipeline_args']['particle_diameter'] = args.particle_diameter
        if args.ctf_fit_resolution is not None:
            cryowizard_preset_pipeline_info['preset_pipeline_args']['ctf_fit_resolution'] = args.ctf_fit_resolution
        if args.symmetry is not None:
            cryowizard_preset_pipeline_info['preset_pipeline_args']['symmetry'] = args.symmetry
        if args.gpu_num is not None:
            cryowizard_preset_pipeline_info['preset_pipeline_args']['gpu_num'] = args.gpu_num
        if args.get_top_particles_num is not None:
            cryowizard_preset_pipeline_info['preset_pipeline_args']['get_top_particles_num'] = args.get_top_particles_num
        if args.get_top_particles_score is not None:
            cryowizard_preset_pipeline_info['preset_pipeline_args']['get_top_particles_score'] = args.get_top_particles_score

    toolbox.savetojson(cryowizard_preset_pipeline_info, os.path.join(cryowizard_data_dir, 'parameters', 'base_parameters', 'cryowizard_preset_pipeline_info.json'), False)


def create_parameters(cryowizard_data_dir, parameter_info):
    # parameter_info type list:
    #     {'type': 'base_parameters'}
    #     {'type': 'import_movie_file_parameters'}
    #     {'type': 'import_micrograph_file_parameters'}
    #     {'type': 'import_particle_file_parameters'}
    #     {'type': 'import_volume_file_parameters'}
    #     {'type': 'preprocess_movie_with_blob_pick_parameters'}
    #     {'type': 'preprocess_movie_with_template_pick_parameters'}
    #     {'type': 'preprocess_micrograph_with_blob_pick_parameters'}
    #     {'type': 'preprocess_micrograph_with_template_pick_parameters'}
    #     {'type': 'preprocess_particle_parameters'}
    #     {'type': 'create_templates_parameters'}
    #     {'type': 'reference_based_auto_select_2d'}
    #     {'type': 'junk_detector'}
    #     {'type': 'cryoranker_parameters'}
    #     {'type': 'get_top_particles'}
    #     {'type': 'refine_parameters'}
    #     {'type': 'motion_and_ctf_refine_parameters'}

    # input types: empty, movie, micrograph, particle
    # output types: particle

    globaldir = os.path.normpath(cryowizard_data_dir)
    source_python_file_path = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
    if (parameter_info['type'] == 'base_parameters'):
        new_parameters_folder_path = os.path.join(globaldir, 'parameters', 'base_parameters')
        if not os.path.exists(new_parameters_folder_path):
            os.makedirs(new_parameters_folder_path)
        cmd_input_parameter_info_dict = {
            "cryosparc_lane": {'current_value': None},
            "slurm": {'current_value': None},
            "inference_gpu_ids": {'current_value': None},
        }
        cryowizard_settings = toolbox.readyaml(os.path.join(source_python_file_path, 'CryoWizard', 'cryowizard_settings.yml'))
        toolbox.savetojson(cryowizard_settings['CryoWizard_settings']['BaseParameters'], os.path.join(new_parameters_folder_path, 'parameters.json'))
        toolbox.savetojson(cmd_input_parameter_info_dict, os.path.join(new_parameters_folder_path, 'cmd_input_parameter_info_dict.json'))
        shutil.copy(os.path.join(source_python_file_path, 'CryoWizard', 'parameters', 'SlurmHeader.sh'), os.path.join(new_parameters_folder_path, 'SlurmHeader.sh'))
        modify_used_preset_pipeline_info(cryowizard_data_dir, 'custom', None)
        return new_parameters_folder_path
    elif (parameter_info['type'] == 'import_movie_file_parameters'):
        if not os.path.exists(os.path.join(globaldir, 'parameters', 'import')):
            os.makedirs(os.path.join(globaldir, 'parameters', 'import'))
        if not os.path.exists(os.path.join(globaldir, 'parameters', 'import', 'folder_id_count.json')):
            toolbox.savetojson(0, os.path.join(globaldir, 'parameters', 'import', 'folder_id_count.json'))
        folder_id_count = toolbox.readjson(os.path.join(globaldir, 'parameters', 'import', 'folder_id_count.json'))
        new_parameters_folder_path = os.path.join(globaldir, 'parameters', 'import', 'import_' + (str)(folder_id_count))
        if not os.path.exists(new_parameters_folder_path):
            os.makedirs(new_parameters_folder_path)
        cryowizard_settings = toolbox.readyaml(os.path.join(source_python_file_path, 'CryoWizard', 'cryowizard_settings.yml'))
        for item in [
            {'parameter_name': 'ImportMovies', 'file_name': 'import_movies_parameters.json'}
        ]:
            toolbox.savetojson(cryowizard_settings['CryoSPARC_job_settings'][item['parameter_name']], os.path.join(new_parameters_folder_path, item['file_name']))
        type_info = {
            'parameters_type': parameter_info['type'],
            'input_type': ['file']
        }
        cmd_input_parameter_info_dict = {
            'movies_data_path': {'current_value': None},
            'gain_reference_path': {'current_value': None},
            'accelerating_voltage': {'current_value': None},
            'spherical_aberration': {'current_value': None},
            'total_exposure_dose': {'current_value': None},
            'raw_pixel_size': {'current_value': None},
        }
        toolbox.savetojson(type_info, os.path.join(new_parameters_folder_path, 'type.json'))
        toolbox.savetojson(cmd_input_parameter_info_dict, os.path.join(new_parameters_folder_path, 'cmd_input_parameter_info_dict.json'))
        toolbox.savetojson((int)(folder_id_count + 1), os.path.join(globaldir, 'parameters', 'import', 'folder_id_count.json'))
        return new_parameters_folder_path
    elif (parameter_info['type'] == 'import_micrograph_file_parameters'):
        if not os.path.exists(os.path.join(globaldir, 'parameters', 'import')):
            os.makedirs(os.path.join(globaldir, 'parameters', 'import'))
        if not os.path.exists(os.path.join(globaldir, 'parameters', 'import', 'folder_id_count.json')):
            toolbox.savetojson(0, os.path.join(globaldir, 'parameters', 'import', 'folder_id_count.json'))
        folder_id_count = toolbox.readjson(os.path.join(globaldir, 'parameters', 'import', 'folder_id_count.json'))
        new_parameters_folder_path = os.path.join(globaldir, 'parameters', 'import', 'import_' + (str)(folder_id_count))
        if not os.path.exists(new_parameters_folder_path):
            os.makedirs(new_parameters_folder_path)
        cryowizard_settings = toolbox.readyaml(os.path.join(source_python_file_path, 'CryoWizard', 'cryowizard_settings.yml'))
        for item in [
            {'parameter_name': 'ImportMicrographs', 'file_name': 'import_micrographs_parameters.json'}
        ]:
            toolbox.savetojson(cryowizard_settings['CryoSPARC_job_settings'][item['parameter_name']], os.path.join(new_parameters_folder_path, item['file_name']))
        type_info = {
            'parameters_type': parameter_info['type'],
            'input_type': ['file']
        }
        cmd_input_parameter_info_dict = {
            'micrographs_data_path': {'current_value': None},
            'accelerating_voltage': {'current_value': None},
            'spherical_aberration': {'current_value': None},
            'total_exposure_dose': {'current_value': None},
            'raw_pixel_size': {'current_value': None},
        }
        toolbox.savetojson(type_info, os.path.join(new_parameters_folder_path, 'type.json'))
        toolbox.savetojson(cmd_input_parameter_info_dict, os.path.join(new_parameters_folder_path, 'cmd_input_parameter_info_dict.json'))
        toolbox.savetojson((int)(folder_id_count + 1), os.path.join(globaldir, 'parameters', 'import', 'folder_id_count.json'))
        return new_parameters_folder_path
    elif (parameter_info['type'] == 'import_particle_file_parameters'):
        if not os.path.exists(os.path.join(globaldir, 'parameters', 'import')):
            os.makedirs(os.path.join(globaldir, 'parameters', 'import'))
        if not os.path.exists(os.path.join(globaldir, 'parameters', 'import', 'folder_id_count.json')):
            toolbox.savetojson(0, os.path.join(globaldir, 'parameters', 'import', 'folder_id_count.json'))
        folder_id_count = toolbox.readjson(os.path.join(globaldir, 'parameters', 'import', 'folder_id_count.json'))
        new_parameters_folder_path = os.path.join(globaldir, 'parameters', 'import', 'import_' + (str)(folder_id_count))
        if not os.path.exists(new_parameters_folder_path):
            os.makedirs(new_parameters_folder_path)
        cryowizard_settings = toolbox.readyaml(os.path.join(source_python_file_path, 'CryoWizard', 'cryowizard_settings.yml'))
        for item in [
            {'parameter_name': 'ImportParticleStack', 'file_name': 'import_particle_stack_parameters.json'}
        ]:
            toolbox.savetojson(cryowizard_settings['CryoSPARC_job_settings'][item['parameter_name']], os.path.join(new_parameters_folder_path, item['file_name']))
        type_info = {
            'parameters_type': parameter_info['type'],
            'input_type': ['file']
        }
        cmd_input_parameter_info_dict = {
            'particles_data_path': {'current_value': None},
            'particles_meta_path': {'current_value': None},
        }
        toolbox.savetojson(type_info, os.path.join(new_parameters_folder_path, 'type.json'))
        toolbox.savetojson(cmd_input_parameter_info_dict, os.path.join(new_parameters_folder_path, 'cmd_input_parameter_info_dict.json'))
        toolbox.savetojson((int)(folder_id_count + 1), os.path.join(globaldir, 'parameters', 'import', 'folder_id_count.json'))
        return new_parameters_folder_path
    elif (parameter_info['type'] == 'import_volume_file_parameters'):
        if not os.path.exists(os.path.join(globaldir, 'parameters', 'import')):
            os.makedirs(os.path.join(globaldir, 'parameters', 'import'))
        if not os.path.exists(os.path.join(globaldir, 'parameters', 'import', 'folder_id_count.json')):
            toolbox.savetojson(0, os.path.join(globaldir, 'parameters', 'import', 'folder_id_count.json'))
        folder_id_count = toolbox.readjson(os.path.join(globaldir, 'parameters', 'import', 'folder_id_count.json'))
        new_parameters_folder_path = os.path.join(globaldir, 'parameters', 'import', 'import_' + (str)(folder_id_count))
        if not os.path.exists(new_parameters_folder_path):
            os.makedirs(new_parameters_folder_path)
        cryowizard_settings = toolbox.readyaml(os.path.join(source_python_file_path, 'CryoWizard', 'cryowizard_settings.yml'))
        for item in [
            {'parameter_name': 'ImportVolume', 'file_name': 'import_volume_parameters.json'}
        ]:
            toolbox.savetojson(cryowizard_settings['CryoSPARC_job_settings'][item['parameter_name']], os.path.join(new_parameters_folder_path, item['file_name']))
        type_info = {
            'parameters_type': parameter_info['type'],
            'input_type': ['file']
        }
        cmd_input_parameter_info_dict = {
            'volume_data_path': {'current_value': None},
            'volume_emdb_id': {'current_value': None},
            'volume_import_type': {'current_value': None},
            'volume_pixelsize': {'current_value': None},
        }
        toolbox.savetojson(type_info, os.path.join(new_parameters_folder_path, 'type.json'))
        toolbox.savetojson(cmd_input_parameter_info_dict, os.path.join(new_parameters_folder_path, 'cmd_input_parameter_info_dict.json'))
        toolbox.savetojson((int)(folder_id_count + 1), os.path.join(globaldir, 'parameters', 'import', 'folder_id_count.json'))
        return new_parameters_folder_path
    elif (parameter_info['type'] == 'preprocess_movie_with_blob_pick_parameters'):
        if not os.path.exists(os.path.join(globaldir, 'parameters', 'preprocess')):
            os.makedirs(os.path.join(globaldir, 'parameters', 'preprocess'))
        if not os.path.exists(os.path.join(globaldir, 'parameters', 'preprocess', 'folder_id_count.json')):
            toolbox.savetojson(0, os.path.join(globaldir, 'parameters', 'preprocess', 'folder_id_count.json'))
        folder_id_count = toolbox.readjson(os.path.join(globaldir, 'parameters', 'preprocess', 'folder_id_count.json'))
        new_parameters_folder_path = os.path.join(globaldir, 'parameters', 'preprocess', 'preprocess_' + (str)(folder_id_count))
        if not os.path.exists(new_parameters_folder_path):
            os.makedirs(new_parameters_folder_path)
        cryowizard_settings = toolbox.readyaml(os.path.join(source_python_file_path, 'CryoWizard', 'cryowizard_settings.yml'))
        for item in [
            {'parameter_name': 'PatchMotionCorrection', 'file_name': 'patch_motion_correction_parameters.json'},
            {'parameter_name': 'PatchCTFEstimation', 'file_name': 'patch_ctf_estimation_parameters.json'},
            {'parameter_name': 'CurateExposures', 'file_name': 'curate_exposures_parameters.json'},
            {'parameter_name': 'BlobPicker', 'file_name': 'blob_picker_parameters.json'},
            {'parameter_name': 'ExtractFromMicrographs', 'file_name': 'extract_micrographs_parameters.json'}
        ]:
            toolbox.savetojson(cryowizard_settings['CryoSPARC_job_settings'][item['parameter_name']], os.path.join(new_parameters_folder_path, item['file_name']))
        type_info = {
            'parameters_type': parameter_info['type'],
            'input_type': ['movie']
        }
        cmd_input_parameter_info_dict = {
            'source_movie_job_uid': {'current_value': None},
            'raw_pixel_size': {'current_value': None},
            'particle_diameter': {'current_value': None},
            'ctf_fit_resolution': {'current_value': None},
            'gpu_num': {'current_value': None},
        }
        toolbox.savetojson(type_info, os.path.join(new_parameters_folder_path, 'type.json'))
        toolbox.savetojson({'source_job_uid': []}, os.path.join(new_parameters_folder_path, 'source_movie_job_uid.json'))
        toolbox.savetojson(cmd_input_parameter_info_dict, os.path.join(new_parameters_folder_path, 'cmd_input_parameter_info_dict.json'))
        toolbox.savetojson((int)(folder_id_count + 1), os.path.join(globaldir, 'parameters', 'preprocess', 'folder_id_count.json'))
        return new_parameters_folder_path
    elif (parameter_info['type'] == 'preprocess_movie_with_template_pick_parameters'):
        if not os.path.exists(os.path.join(globaldir, 'parameters', 'preprocess')):
            os.makedirs(os.path.join(globaldir, 'parameters', 'preprocess'))
        if not os.path.exists(os.path.join(globaldir, 'parameters', 'preprocess', 'folder_id_count.json')):
            toolbox.savetojson(0, os.path.join(globaldir, 'parameters', 'preprocess', 'folder_id_count.json'))
        folder_id_count = toolbox.readjson(os.path.join(globaldir, 'parameters', 'preprocess', 'folder_id_count.json'))
        new_parameters_folder_path = os.path.join(globaldir, 'parameters', 'preprocess', 'preprocess_' + (str)(folder_id_count))
        if not os.path.exists(new_parameters_folder_path):
            os.makedirs(new_parameters_folder_path)
        cryowizard_settings = toolbox.readyaml(os.path.join(source_python_file_path, 'CryoWizard', 'cryowizard_settings.yml'))
        for item in [
            {'parameter_name': 'PatchMotionCorrection', 'file_name': 'patch_motion_correction_parameters.json'},
            {'parameter_name': 'PatchCTFEstimation', 'file_name': 'patch_ctf_estimation_parameters.json'},
            {'parameter_name': 'CurateExposures', 'file_name': 'curate_exposures_parameters.json'},
            {'parameter_name': 'TemplatePicker', 'file_name': 'template_picker_parameters.json'},
            {'parameter_name': 'ExtractFromMicrographs', 'file_name': 'extract_micrographs_parameters.json'}
        ]:
            toolbox.savetojson(cryowizard_settings['CryoSPARC_job_settings'][item['parameter_name']], os.path.join(new_parameters_folder_path, item['file_name']))
        type_info = {
            'parameters_type': parameter_info['type'],
            'input_type': ['movie', 'template']
        }
        cmd_input_parameter_info_dict = {
            'source_movie_job_uid': {'current_value': None},
            'source_template_job_uid': {'current_value': None},
            'raw_pixel_size': {'current_value': None},
            'particle_diameter': {'current_value': None},
            'ctf_fit_resolution': {'current_value': None},
            'gpu_num': {'current_value': None},
        }
        toolbox.savetojson(type_info, os.path.join(new_parameters_folder_path, 'type.json'))
        toolbox.savetojson({'source_job_uid': []}, os.path.join(new_parameters_folder_path, 'source_movie_job_uid.json'))
        toolbox.savetojson({'source_job_uid': []}, os.path.join(new_parameters_folder_path, 'source_template_job_uid.json'))
        toolbox.savetojson(cmd_input_parameter_info_dict, os.path.join(new_parameters_folder_path, 'cmd_input_parameter_info_dict.json'))
        toolbox.savetojson((int)(folder_id_count + 1), os.path.join(globaldir, 'parameters', 'preprocess', 'folder_id_count.json'))
        return new_parameters_folder_path
    elif (parameter_info['type'] == 'preprocess_micrograph_with_blob_pick_parameters'):
        if not os.path.exists(os.path.join(globaldir, 'parameters', 'preprocess')):
            os.makedirs(os.path.join(globaldir, 'parameters', 'preprocess'))
        if not os.path.exists(os.path.join(globaldir, 'parameters', 'preprocess', 'folder_id_count.json')):
            toolbox.savetojson(0, os.path.join(globaldir, 'parameters', 'preprocess', 'folder_id_count.json'))
        folder_id_count = toolbox.readjson(os.path.join(globaldir, 'parameters', 'preprocess', 'folder_id_count.json'))
        new_parameters_folder_path = os.path.join(globaldir, 'parameters', 'preprocess', 'preprocess_' + (str)(folder_id_count))
        if not os.path.exists(new_parameters_folder_path):
            os.makedirs(new_parameters_folder_path)
        cryowizard_settings = toolbox.readyaml(os.path.join(source_python_file_path, 'CryoWizard', 'cryowizard_settings.yml'))
        for item in [
            {'parameter_name': 'PatchCTFEstimation', 'file_name': 'patch_ctf_estimation_parameters.json'},
            {'parameter_name': 'CurateExposures', 'file_name': 'curate_exposures_parameters.json'},
            {'parameter_name': 'BlobPicker', 'file_name': 'blob_picker_parameters.json'},
            {'parameter_name': 'ExtractFromMicrographs', 'file_name': 'extract_micrographs_parameters.json'}
        ]:
            toolbox.savetojson(cryowizard_settings['CryoSPARC_job_settings'][item['parameter_name']], os.path.join(new_parameters_folder_path, item['file_name']))
        type_info = {
            'parameters_type': parameter_info['type'],
            'input_type': ['micrograph']
        }
        cmd_input_parameter_info_dict = {
            'source_micrograph_job_uid': {'current_value': None},
            'raw_pixel_size': {'current_value': None},
            'particle_diameter': {'current_value': None},
            'ctf_fit_resolution': {'current_value': None},
            'gpu_num': {'current_value': None},
        }
        toolbox.savetojson(type_info, os.path.join(new_parameters_folder_path, 'type.json'))
        toolbox.savetojson({'source_job_uid': []}, os.path.join(new_parameters_folder_path, 'source_micrograph_job_uid.json'))
        toolbox.savetojson(cmd_input_parameter_info_dict, os.path.join(new_parameters_folder_path, 'cmd_input_parameter_info_dict.json'))
        toolbox.savetojson((int)(folder_id_count + 1), os.path.join(globaldir, 'parameters', 'preprocess', 'folder_id_count.json'))
        return new_parameters_folder_path
    elif (parameter_info['type'] == 'preprocess_micrograph_with_template_pick_parameters'):
        if not os.path.exists(os.path.join(globaldir, 'parameters', 'preprocess')):
            os.makedirs(os.path.join(globaldir, 'parameters', 'preprocess'))
        if not os.path.exists(os.path.join(globaldir, 'parameters', 'preprocess', 'folder_id_count.json')):
            toolbox.savetojson(0, os.path.join(globaldir, 'parameters', 'preprocess', 'folder_id_count.json'))
        folder_id_count = toolbox.readjson(os.path.join(globaldir, 'parameters', 'preprocess', 'folder_id_count.json'))
        new_parameters_folder_path = os.path.join(globaldir, 'parameters', 'preprocess', 'preprocess_' + (str)(folder_id_count))
        if not os.path.exists(new_parameters_folder_path):
            os.makedirs(new_parameters_folder_path)
        cryowizard_settings = toolbox.readyaml(os.path.join(source_python_file_path, 'CryoWizard', 'cryowizard_settings.yml'))
        for item in [
            {'parameter_name': 'PatchCTFEstimation', 'file_name': 'patch_ctf_estimation_parameters.json'},
            {'parameter_name': 'CurateExposures', 'file_name': 'curate_exposures_parameters.json'},
            {'parameter_name': 'TemplatePicker', 'file_name': 'template_picker_parameters.json'},
            {'parameter_name': 'ExtractFromMicrographs', 'file_name': 'extract_micrographs_parameters.json'}
        ]:
            toolbox.savetojson(cryowizard_settings['CryoSPARC_job_settings'][item['parameter_name']], os.path.join(new_parameters_folder_path, item['file_name']))
        type_info = {
            'parameters_type': parameter_info['type'],
            'input_type': ['micrograph', 'template']
        }
        cmd_input_parameter_info_dict = {
            'source_micrograph_job_uid': {'current_value': None},
            'source_template_job_uid': {'current_value': None},
            'raw_pixel_size': {'current_value': None},
            'particle_diameter': {'current_value': None},
            'ctf_fit_resolution': {'current_value': None},
            'gpu_num': {'current_value': None},
        }
        toolbox.savetojson(type_info, os.path.join(new_parameters_folder_path, 'type.json'))
        toolbox.savetojson({'source_job_uid': []}, os.path.join(new_parameters_folder_path, 'source_micrograph_job_uid.json'))
        toolbox.savetojson({'source_job_uid': []}, os.path.join(new_parameters_folder_path, 'source_template_job_uid.json'))
        toolbox.savetojson(cmd_input_parameter_info_dict, os.path.join(new_parameters_folder_path, 'cmd_input_parameter_info_dict.json'))
        toolbox.savetojson((int)(folder_id_count + 1), os.path.join(globaldir, 'parameters', 'preprocess', 'folder_id_count.json'))
        return new_parameters_folder_path
    elif (parameter_info['type'] == 'preprocess_particle_parameters'):
        if not os.path.exists(os.path.join(globaldir, 'parameters', 'preprocess')):
            os.makedirs(os.path.join(globaldir, 'parameters', 'preprocess'))
        if not os.path.exists(os.path.join(globaldir, 'parameters', 'preprocess', 'folder_id_count.json')):
            toolbox.savetojson(0, os.path.join(globaldir, 'parameters', 'preprocess', 'folder_id_count.json'))
        folder_id_count = toolbox.readjson(os.path.join(globaldir, 'parameters', 'preprocess', 'folder_id_count.json'))
        new_parameters_folder_path = os.path.join(globaldir, 'parameters', 'preprocess', 'preprocess_' + (str)(folder_id_count))
        if not os.path.exists(new_parameters_folder_path):
            os.makedirs(new_parameters_folder_path)
        type_info = {
            'parameters_type': parameter_info['type'],
            'input_type': ['particle']
        }
        cmd_input_parameter_info_dict = {
            'source_particle_job_uid': {'current_value': None},
        }
        toolbox.savetojson(type_info, os.path.join(new_parameters_folder_path, 'type.json'))
        toolbox.savetojson({'source_job_uid': []}, os.path.join(new_parameters_folder_path, 'source_particle_job_uid.json'))
        toolbox.savetojson(cmd_input_parameter_info_dict, os.path.join(new_parameters_folder_path, 'cmd_input_parameter_info_dict.json'))
        toolbox.savetojson((int)(folder_id_count + 1), os.path.join(globaldir, 'parameters', 'preprocess', 'folder_id_count.json'))
        return new_parameters_folder_path
    elif (parameter_info['type'] == 'create_templates_parameters'):
        if not os.path.exists(os.path.join(globaldir, 'parameters', 'preprocess')):
            os.makedirs(os.path.join(globaldir, 'parameters', 'preprocess'))
        if not os.path.exists(os.path.join(globaldir, 'parameters', 'preprocess', 'folder_id_count.json')):
            toolbox.savetojson(0, os.path.join(globaldir, 'parameters', 'preprocess', 'folder_id_count.json'))
        folder_id_count = toolbox.readjson(os.path.join(globaldir, 'parameters', 'preprocess', 'folder_id_count.json'))
        new_parameters_folder_path = os.path.join(globaldir, 'parameters', 'preprocess', 'preprocess_' + (str)(folder_id_count))
        if not os.path.exists(new_parameters_folder_path):
            os.makedirs(new_parameters_folder_path)
        cryowizard_settings = toolbox.readyaml(os.path.join(source_python_file_path, 'CryoWizard', 'cryowizard_settings.yml'))
        for item in [
            {'parameter_name': 'CreateTemplates', 'file_name': 'create_templates_parameters.json'},
        ]:
            toolbox.savetojson(cryowizard_settings['CryoSPARC_job_settings'][item['parameter_name']], os.path.join(new_parameters_folder_path, item['file_name']))
        type_info = {
            'parameters_type': parameter_info['type'],
            'input_type': ['volume']
        }
        cmd_input_parameter_info_dict = {
            'source_volume_job_uid': {'current_value': None},
        }
        toolbox.savetojson(type_info, os.path.join(new_parameters_folder_path, 'type.json'))
        toolbox.savetojson({'source_job_uid': []}, os.path.join(new_parameters_folder_path, 'source_volume_job_uid.json'))
        toolbox.savetojson(cmd_input_parameter_info_dict, os.path.join(new_parameters_folder_path, 'cmd_input_parameter_info_dict.json'))
        toolbox.savetojson((int)(folder_id_count + 1), os.path.join(globaldir, 'parameters', 'preprocess', 'folder_id_count.json'))
        return new_parameters_folder_path
    elif (parameter_info['type'] == 'reference_based_auto_select_2d'):
        if not os.path.exists(os.path.join(globaldir, 'parameters', 'preprocess')):
            os.makedirs(os.path.join(globaldir, 'parameters', 'preprocess'))
        if not os.path.exists(os.path.join(globaldir, 'parameters', 'preprocess', 'folder_id_count.json')):
            toolbox.savetojson(0, os.path.join(globaldir, 'parameters', 'preprocess', 'folder_id_count.json'))
        folder_id_count = toolbox.readjson(os.path.join(globaldir, 'parameters', 'preprocess', 'folder_id_count.json'))
        new_parameters_folder_path = os.path.join(globaldir, 'parameters', 'preprocess', 'preprocess_' + (str)(folder_id_count))
        if not os.path.exists(new_parameters_folder_path):
            os.makedirs(new_parameters_folder_path)
        cryowizard_settings = toolbox.readyaml(os.path.join(source_python_file_path, 'CryoWizard', 'cryowizard_settings.yml'))
        for item in [
            {'parameter_name': 'RestackParticles', 'file_name': 'restack_particles_parameters.json'},
            {'parameter_name': '2DClassification', 'file_name': '2d_classification_parameters.json'},
            {'parameter_name': 'ReferenceBasedAutoSelect2D', 'file_name': 'reference_select_2d_parameters.json'}
        ]:
            toolbox.savetojson(cryowizard_settings['CryoSPARC_job_settings'][item['parameter_name']], os.path.join(new_parameters_folder_path, item['file_name']))
        type_info = {
            'parameters_type': parameter_info['type'],
            'input_type': ['particle']
        }
        cmd_input_parameter_info_dict = {
            'source_particle_job_uid': {'current_value': None},
            'source_volume_job_uid': {'current_value': None},
            'gpu_num': {'current_value': None},
        }
        toolbox.savetojson(type_info, os.path.join(new_parameters_folder_path, 'type.json'))
        toolbox.savetojson({'source_job_uid': []}, os.path.join(new_parameters_folder_path, 'source_particle_job_uid.json'))
        toolbox.savetojson({'source_job_uid': []}, os.path.join(new_parameters_folder_path, 'source_volume_job_uid.json'))
        toolbox.savetojson(cmd_input_parameter_info_dict, os.path.join(new_parameters_folder_path, 'cmd_input_parameter_info_dict.json'))
        toolbox.savetojson((int)(folder_id_count + 1), os.path.join(globaldir, 'parameters', 'preprocess', 'folder_id_count.json'))
        return new_parameters_folder_path
    elif (parameter_info['type'] == 'junk_detector'):
        if not os.path.exists(os.path.join(globaldir, 'parameters', 'preprocess')):
            os.makedirs(os.path.join(globaldir, 'parameters', 'preprocess'))
        if not os.path.exists(os.path.join(globaldir, 'parameters', 'preprocess', 'folder_id_count.json')):
            toolbox.savetojson(0, os.path.join(globaldir, 'parameters', 'preprocess', 'folder_id_count.json'))
        folder_id_count = toolbox.readjson(os.path.join(globaldir, 'parameters', 'preprocess', 'folder_id_count.json'))
        new_parameters_folder_path = os.path.join(globaldir, 'parameters', 'preprocess', 'preprocess_' + (str)(folder_id_count))
        if not os.path.exists(new_parameters_folder_path):
            os.makedirs(new_parameters_folder_path)
        cryowizard_settings = toolbox.readyaml(os.path.join(source_python_file_path, 'CryoWizard', 'cryowizard_settings.yml'))
        for item in [
            {'parameter_name': 'JunkDetector', 'file_name': 'junk_detector_parameters.json'}
        ]:
            toolbox.savetojson(cryowizard_settings['CryoSPARC_job_settings'][item['parameter_name']], os.path.join(new_parameters_folder_path, item['file_name']))
        type_info = {
            'parameters_type': parameter_info['type'],
            'input_type': ['particle']
        }
        cmd_input_parameter_info_dict = {
            'source_particle_job_uid': {'current_value': None},
        }
        toolbox.savetojson(type_info, os.path.join(new_parameters_folder_path, 'type.json'))
        toolbox.savetojson({'source_job_uid': []}, os.path.join(new_parameters_folder_path, 'source_particle_job_uid.json'))
        toolbox.savetojson(cmd_input_parameter_info_dict, os.path.join(new_parameters_folder_path, 'cmd_input_parameter_info_dict.json'))
        toolbox.savetojson((int)(folder_id_count + 1), os.path.join(globaldir, 'parameters', 'preprocess', 'folder_id_count.json'))
        return new_parameters_folder_path
    elif (parameter_info['type'] == 'cryoranker_parameters'):
        if not os.path.exists(os.path.join(globaldir, 'parameters', 'cryoranker')):
            os.makedirs(os.path.join(globaldir, 'parameters', 'cryoranker'))
        if not os.path.exists(os.path.join(globaldir, 'parameters', 'cryoranker', 'folder_id_count.json')):
            toolbox.savetojson(0, os.path.join(globaldir, 'parameters', 'cryoranker', 'folder_id_count.json'))
        folder_id_count = toolbox.readjson(os.path.join(globaldir, 'parameters', 'cryoranker', 'folder_id_count.json'))
        new_parameters_folder_path = os.path.join(globaldir, 'parameters', 'cryoranker', 'cryoranker_' + (str)(folder_id_count))
        if not os.path.exists(new_parameters_folder_path):
            os.makedirs(new_parameters_folder_path)
        cryowizard_settings = toolbox.readyaml(os.path.join(source_python_file_path, 'CryoWizard', 'cryowizard_settings.yml'))
        for item in [
            {'parameter_name': 'RestackParticles', 'file_name': 'restack_particles_parameters.json'}
        ]:
            toolbox.savetojson(cryowizard_settings['CryoSPARC_job_settings'][item['parameter_name']], os.path.join(new_parameters_folder_path, item['file_name']))
        type_info = {
            'parameters_type': parameter_info['type'],
            'input_type': ['particle']
        }
        cmd_input_parameter_info_dict = {
            'source_particle_job_uid': {'current_value': None},
        }
        toolbox.savetojson(type_info, os.path.join(new_parameters_folder_path, 'type.json'))
        toolbox.savetojson({'source_job_uid': []}, os.path.join(new_parameters_folder_path, 'source_particle_job_uid.json'))
        toolbox.savetojson(cmd_input_parameter_info_dict, os.path.join(new_parameters_folder_path, 'cmd_input_parameter_info_dict.json'))
        toolbox.savetojson((int)(folder_id_count + 1), os.path.join(globaldir, 'parameters', 'cryoranker', 'folder_id_count.json'))
        return new_parameters_folder_path
    elif (parameter_info['type'] == 'get_top_particles'):
        if not os.path.exists(os.path.join(globaldir, 'parameters', 'cryoranker')):
            os.makedirs(os.path.join(globaldir, 'parameters', 'cryoranker'))
        if not os.path.exists(os.path.join(globaldir, 'parameters', 'cryoranker', 'folder_id_count.json')):
            toolbox.savetojson(0, os.path.join(globaldir, 'parameters', 'cryoranker', 'folder_id_count.json'))
        folder_id_count = toolbox.readjson(os.path.join(globaldir, 'parameters', 'cryoranker', 'folder_id_count.json'))
        new_parameters_folder_path = os.path.join(globaldir, 'parameters', 'cryoranker', 'cryoranker_' + (str)(folder_id_count))
        if not os.path.exists(new_parameters_folder_path):
            os.makedirs(new_parameters_folder_path)
        type_info = {
            'parameters_type': parameter_info['type'],
            'input_type': ['cryoranker']
        }
        cmd_input_parameter_info_dict = {
            'source_cryoranker_job_uid': {'current_value': None},
            'get_top_particles_num': {'current_value': None},
            'get_top_particles_score': {'current_value': None},
        }
        toolbox.savetojson(type_info, os.path.join(new_parameters_folder_path, 'type.json'))
        toolbox.savetojson({'get_type': 'score', 'cut_off_point': 0.6}, os.path.join(new_parameters_folder_path, 'get_top_particles_parameters.json'))
        toolbox.savetojson({'source_job_uid': []}, os.path.join(new_parameters_folder_path, 'source_cryoranker_job_uid.json'))
        toolbox.savetojson(cmd_input_parameter_info_dict, os.path.join(new_parameters_folder_path, 'cmd_input_parameter_info_dict.json'))
        toolbox.savetojson((int)(folder_id_count + 1), os.path.join(globaldir, 'parameters', 'cryoranker', 'folder_id_count.json'))
        return new_parameters_folder_path
    elif (parameter_info['type'] == 'refine_parameters'):
        if not os.path.exists(os.path.join(globaldir, 'parameters', 'refine')):
            os.makedirs(os.path.join(globaldir, 'parameters', 'refine'))
        if not os.path.exists(os.path.join(globaldir, 'parameters', 'refine', 'folder_id_count.json')):
            toolbox.savetojson(0, os.path.join(globaldir, 'parameters', 'refine', 'folder_id_count.json'))
        folder_id_count = toolbox.readjson(os.path.join(globaldir, 'parameters', 'refine', 'folder_id_count.json'))
        new_parameters_folder_path = os.path.join(globaldir, 'parameters', 'refine', 'refine_' + (str)(folder_id_count))
        if not os.path.exists(new_parameters_folder_path):
            os.makedirs(new_parameters_folder_path)
        cryowizard_settings = toolbox.readyaml(os.path.join(source_python_file_path, 'CryoWizard', 'cryowizard_settings.yml'))
        for item in [
            {'parameter_name': 'RestackParticles', 'file_name': 'restack_particles_parameters.json'},
            {'parameter_name': 'AbInitialReconstruction', 'file_name': 'abinit_parameters.json'},
            {'parameter_name': 'NonUniformRefinement_initial', 'file_name': 'nurefine_parameters_initial.json'},
            {'parameter_name': 'NonUniformRefinement_final', 'file_name': 'nurefine_parameters_final.json'},
            {'parameter_name': 'OrientationDiagnostics_initial', 'file_name': 'orientation_diagnostics_parameters_initial.json'},
            {'parameter_name': 'OrientationDiagnostics_final', 'file_name': 'orientation_diagnostics_parameters_final.json'}
        ]:
            toolbox.savetojson(cryowizard_settings['CryoSPARC_job_settings'][item['parameter_name']], os.path.join(new_parameters_folder_path, item['file_name']))
        type_info = {
            'parameters_type': parameter_info['type'],
            'input_type': ['cryoranker']
        }
        cmd_input_parameter_info_dict = {
            'source_cryoranker_job_uid': {'current_value': None},
            'symmetry': {'current_value': None},
        }
        toolbox.savetojson(type_info, os.path.join(new_parameters_folder_path, 'type.json'))
        toolbox.savetojson({'source_job_uid': []}, os.path.join(new_parameters_folder_path, 'source_cryoranker_job_uid.json'))
        toolbox.savetojson(cmd_input_parameter_info_dict, os.path.join(new_parameters_folder_path, 'cmd_input_parameter_info_dict.json'))
        toolbox.savetojson((int)(folder_id_count + 1), os.path.join(globaldir, 'parameters', 'refine', 'folder_id_count.json'))
        return new_parameters_folder_path
    elif (parameter_info['type'] == 'motion_and_ctf_refine_parameters'):
        if not os.path.exists(os.path.join(globaldir, 'parameters', 'postprocess')):
            os.makedirs(os.path.join(globaldir, 'parameters', 'postprocess'))
        if not os.path.exists(os.path.join(globaldir, 'parameters', 'postprocess', 'folder_id_count.json')):
            toolbox.savetojson(0, os.path.join(globaldir, 'parameters', 'postprocess', 'folder_id_count.json'))
        folder_id_count = toolbox.readjson(os.path.join(globaldir, 'parameters', 'postprocess', 'folder_id_count.json'))
        new_parameters_folder_path = os.path.join(globaldir, 'parameters', 'postprocess', 'postprocess_' + (str)(folder_id_count))
        if not os.path.exists(new_parameters_folder_path):
            os.makedirs(new_parameters_folder_path)
        cryowizard_settings = toolbox.readyaml(os.path.join(source_python_file_path, 'CryoWizard', 'cryowizard_settings.yml'))
        for item in [
            {'parameter_name': 'RestackParticles', 'file_name': 'restack_particles_parameters.json'},
            {'parameter_name': 'ReferenceMotionCorrection', 'file_name': 'reference_motion_correction_parameters.json'},
            {'parameter_name': 'CTFRefineGlobal', 'file_name': 'ctf_refine_global_parameters.json'},
            {'parameter_name': 'CTFRefineLocal', 'file_name': 'ctf_refine_local_parameters.json'},
            {'parameter_name': 'NonUniformRefinement_final', 'file_name': 'nurefine_parameters_final.json'}
        ]:
            toolbox.savetojson(cryowizard_settings['CryoSPARC_job_settings'][item['parameter_name']], os.path.join(new_parameters_folder_path, item['file_name']))
        type_info = {
            'parameters_type': parameter_info['type'],
            'input_type': ['particle', 'volume', 'mask']
        }
        cmd_input_parameter_info_dict = {
            'source_particle_job_uid': {'current_value': None},
            'source_volume_job_uid': {'current_value': None},
            'source_mask_job_uid': {'current_value': None},
            'symmetry': {'current_value': None},
            'gpu_num': {'current_value': None},
        }
        toolbox.savetojson(type_info, os.path.join(new_parameters_folder_path, 'type.json'))
        toolbox.savetojson({'source_job_uid': []}, os.path.join(new_parameters_folder_path, 'source_particle_job_uid.json'))
        toolbox.savetojson({'source_job_uid': []}, os.path.join(new_parameters_folder_path, 'source_volume_job_uid.json'))
        toolbox.savetojson({'source_job_uid': []}, os.path.join(new_parameters_folder_path, 'source_mask_job_uid.json'))
        toolbox.savetojson(cmd_input_parameter_info_dict, os.path.join(new_parameters_folder_path, 'cmd_input_parameter_info_dict.json'))
        toolbox.savetojson((int)(folder_id_count + 1), os.path.join(globaldir, 'parameters', 'postprocess', 'folder_id_count.json'))
        return new_parameters_folder_path

    # other elif

    else:
        print('Input type error...', flush=True)
        return None


def modify_parameters(cryowizard_data_dir, parameters_folder_name, args):
    parameters_folder_name_head = parameters_folder_name.split('_')[0]
    if (parameters_folder_name_head == 'base'):
        parameters_folder_path = os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', parameters_folder_name)
    elif (parameters_folder_name_head == 'import'):
        parameters_folder_path = os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', 'import', parameters_folder_name)
    elif (parameters_folder_name_head == 'preprocess'):
        parameters_folder_path = os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', 'preprocess', parameters_folder_name)
    elif (parameters_folder_name_head == 'cryoranker'):
        parameters_folder_path = os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', 'cryoranker', parameters_folder_name)
    elif (parameters_folder_name_head == 'refine'):
        parameters_folder_path = os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', 'refine', parameters_folder_name)
    elif (parameters_folder_name_head == 'postprocess'):
        parameters_folder_path = os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', 'postprocess', parameters_folder_name)

    # other elif

    else:
        print('parameters_folder_name wrong', flush=True)
        return

    # save used cmd parameters
    cmd_input_parameter_info_dict = toolbox.readjson(os.path.join(parameters_folder_path, 'cmd_input_parameter_info_dict.json'))
    for cmd_key, cmd_value in toolbox.args2dict(args).items():
        if ((cmd_key in cmd_input_parameter_info_dict) and (cmd_value is not None)):
            cmd_input_parameter_info_dict[cmd_key]['current_value'] = cmd_value
    toolbox.savetojson(cmd_input_parameter_info_dict, os.path.join(parameters_folder_path, 'cmd_input_parameter_info_dict.json'))

    # modify parameter
    ## caculate some parameters
    blob_pick_parameters_min_particle_diameter = None
    blob_pick_parameters_max_particle_diameter = None
    motion_correction_parameters_output_fcrop_factor = None
    extract_parameters_extraction_box_size = None
    if args.particle_diameter is not None:
        blob_pick_parameters_min_particle_diameter = (args.particle_diameter - 10) if ((args.particle_diameter - 10) >= 0) else 0
        blob_pick_parameters_max_particle_diameter = (args.particle_diameter + 10) if ((args.particle_diameter + 10) >= 0) else 0
        if args.raw_pixel_size is not None:
            if ((1.0 - args.raw_pixel_size) > np.fabs(1.0 - 2.0 * args.raw_pixel_size)) and os.path.exists(os.path.join(parameters_folder_path, 'patch_motion_correction_parameters.json')):
                motion_correction_parameters_output_fcrop_factor = '1/2'
                extract_parameters_extraction_box_size = (int)(math.floor((float)(args.particle_diameter) / (args.raw_pixel_size * 2.0) / 5.0) * 10.0)
            else:
                extract_parameters_extraction_box_size = (int)(math.floor((float)(args.particle_diameter) / args.raw_pixel_size / 5.0) * 10.0)
    ## modify parameters
    if os.path.exists(os.path.join(parameters_folder_path, 'parameters.json')):
        base_parameters = toolbox.readjson(os.path.join(parameters_folder_path, 'parameters.json'))
        if args.cryosparc_username is not None:
            base_parameters['cryosparc_username'] = args.cryosparc_username
        if args.cryosparc_password is not None:
            base_parameters['cryosparc_password'] = args.cryosparc_password
        if args.cryosparc_project is not None:
            base_parameters['project'] = args.cryosparc_project
        if args.cryosparc_workspace is not None:
            base_parameters['workspace'] = args.cryosparc_workspace
        if args.cryosparc_lane is not None:
            base_parameters['lane'] = args.cryosparc_lane
        if args.slurm is not None:
            if args.slurm in ['true', 'True', 'yes', 'Yes', 'y', 'Y']:
                base_parameters['if_slurm'] = True
            elif args.slurm in ['false', 'False', 'no', 'No', 'n', 'N']:
                base_parameters['if_slurm'] = False
        if args.inference_gpu_ids is not None:
            base_parameters['inference_gpu_ids'] = args.inference_gpu_ids
        toolbox.savetojson(base_parameters, os.path.join(parameters_folder_path, 'parameters.json'))
    if os.path.exists(os.path.join(parameters_folder_path, 'source_movie_job_uid.json')):
        if args.source_movie_job_uid is not None:
            toolbox.savetojson({'source_job_uid': args.source_movie_job_uid}, os.path.join(parameters_folder_path, 'source_movie_job_uid.json'))
    if os.path.exists(os.path.join(parameters_folder_path, 'source_micrograph_job_uid.json')):
        if args.source_micrograph_job_uid is not None:
            toolbox.savetojson({'source_job_uid': args.source_micrograph_job_uid}, os.path.join(parameters_folder_path, 'source_micrograph_job_uid.json'))
    if os.path.exists(os.path.join(parameters_folder_path, 'source_particle_job_uid.json')):
        if args.source_particle_job_uid is not None:
            toolbox.savetojson({'source_job_uid': args.source_particle_job_uid}, os.path.join(parameters_folder_path, 'source_particle_job_uid.json'))
    if os.path.exists(os.path.join(parameters_folder_path, 'source_template_job_uid.json')):
        if args.source_template_job_uid is not None:
            toolbox.savetojson({'source_job_uid': args.source_template_job_uid}, os.path.join(parameters_folder_path, 'source_template_job_uid.json'))
    if os.path.exists(os.path.join(parameters_folder_path, 'source_volume_job_uid.json')):
        if args.source_volume_job_uid is not None:
            toolbox.savetojson({'source_job_uid': args.source_volume_job_uid}, os.path.join(parameters_folder_path, 'source_volume_job_uid.json'))
    if os.path.exists(os.path.join(parameters_folder_path, 'source_mask_job_uid.json')):
        if args.source_mask_job_uid is not None:
            toolbox.savetojson({'source_job_uid': args.source_mask_job_uid}, os.path.join(parameters_folder_path, 'source_mask_job_uid.json'))
    if os.path.exists(os.path.join(parameters_folder_path, 'source_cryoranker_job_uid.json')):
        if args.source_cryoranker_job_uid is not None:
            toolbox.savetojson({'source_job_uid': args.source_cryoranker_job_uid}, os.path.join(parameters_folder_path, 'source_cryoranker_job_uid.json'))
    if os.path.exists(os.path.join(parameters_folder_path, 'get_top_particles_parameters.json')):
        if args.get_top_particles_num is not None:
            toolbox.savetojson({'get_type': 'num', 'cut_off_point': args.get_top_particles_num}, os.path.join(parameters_folder_path, 'get_top_particles_parameters.json'))
        if args.get_top_particles_score is not None:
            toolbox.savetojson({'get_type': 'score', 'cut_off_point': args.get_top_particles_score}, os.path.join(parameters_folder_path, 'get_top_particles_parameters.json'))
    if os.path.exists(os.path.join(parameters_folder_path, 'import_movies_parameters.json')):
        import_movies_parameters = toolbox.readjson(os.path.join(parameters_folder_path, 'import_movies_parameters.json'))
        if args.movies_data_path is not None:
            import_movies_parameters['Movies data path'] = args.movies_data_path
        if args.gain_reference_path is not None:
            import_movies_parameters['Gain reference path'] = args.gain_reference_path
        if args.raw_pixel_size is not None:
            import_movies_parameters['Raw pixel size (A)'] = args.raw_pixel_size
        if args.accelerating_voltage is not None:
            import_movies_parameters['Accelerating Voltage (kV)'] = args.accelerating_voltage
        if args.spherical_aberration is not None:
            import_movies_parameters['Spherical Aberration (mm)'] = args.spherical_aberration
        if args.total_exposure_dose is not None:
            import_movies_parameters['Total exposure dose (e/A^2)'] = args.total_exposure_dose
        toolbox.savetojson(import_movies_parameters, os.path.join(parameters_folder_path, 'import_movies_parameters.json'))
    if os.path.exists(os.path.join(parameters_folder_path, 'import_micrographs_parameters.json')):
        import_micrographs_parameters = toolbox.readjson(os.path.join(parameters_folder_path, 'import_micrographs_parameters.json'))
        if args.micrographs_data_path is not None:
            import_micrographs_parameters['Micrographs data path'] = args.micrographs_data_path
        if args.raw_pixel_size is not None:
            import_micrographs_parameters['Pixel size (A)'] = args.raw_pixel_size
        if args.accelerating_voltage is not None:
            import_micrographs_parameters['Accelerating Voltage (kV)'] = args.accelerating_voltage
        if args.spherical_aberration is not None:
            import_micrographs_parameters['Spherical Aberration (mm)'] = args.spherical_aberration
        if args.total_exposure_dose is not None:
            import_micrographs_parameters['Total exposure dose (e/A^2)'] = args.total_exposure_dose
        toolbox.savetojson(import_micrographs_parameters, os.path.join(parameters_folder_path, 'import_micrographs_parameters.json'))
    if os.path.exists(os.path.join(parameters_folder_path, 'import_particle_stack_parameters.json')):
        import_particle_stack_parameters = toolbox.readjson(os.path.join(parameters_folder_path, 'import_particle_stack_parameters.json'))
        if args.particles_meta_path is not None:
            import_particle_stack_parameters['Particle meta path'] = args.particles_meta_path
        if args.particles_data_path is not None:
            import_particle_stack_parameters['Particle data path'] = args.particles_data_path
        toolbox.savetojson(import_particle_stack_parameters, os.path.join(parameters_folder_path, 'import_particle_stack_parameters.json'))
    if os.path.exists(os.path.join(parameters_folder_path, 'import_volume_parameters.json')):
        import_volume_parameters = toolbox.readjson(os.path.join(parameters_folder_path, 'import_volume_parameters.json'))
        if args.volume_data_path is not None:
            import_volume_parameters['Volume data path'] = args.volume_data_path
        if args.volume_emdb_id is not None:
            import_volume_parameters['EMDB ID'] = args.volume_emdb_id
        if args.volume_import_type is not None:
            import_volume_parameters['Type of volume being imported'] = args.volume_import_type
        if args.volume_pixelsize is not None:
            import_volume_parameters['Pixel size (A)'] = args.volume_pixelsize
        toolbox.savetojson(import_volume_parameters, os.path.join(parameters_folder_path, 'import_volume_parameters.json'))
    if os.path.exists(os.path.join(parameters_folder_path, 'patch_motion_correction_parameters.json')):
        motion_correction_parameters = toolbox.readjson(os.path.join(parameters_folder_path, 'patch_motion_correction_parameters.json'))
        if motion_correction_parameters_output_fcrop_factor is not None:
            motion_correction_parameters['Output F-crop factor'] = motion_correction_parameters_output_fcrop_factor
        if args.gpu_num is not None:
            motion_correction_parameters['Number of GPUs to parallelize'] = args.gpu_num
        toolbox.savetojson(motion_correction_parameters, os.path.join(parameters_folder_path, 'patch_motion_correction_parameters.json'))
    if os.path.exists(os.path.join(parameters_folder_path, 'patch_ctf_estimation_parameters.json')):
        ctf_estimation_parameters = toolbox.readjson(os.path.join(parameters_folder_path, 'patch_ctf_estimation_parameters.json'))
        if args.gpu_num is not None:
            ctf_estimation_parameters['Number of GPUs to parallelize'] = args.gpu_num
        toolbox.savetojson(ctf_estimation_parameters, os.path.join(parameters_folder_path, 'patch_ctf_estimation_parameters.json'))
    if os.path.exists(os.path.join(parameters_folder_path, 'blob_picker_parameters.json')):
        blob_pick_parameters = toolbox.readjson(os.path.join(parameters_folder_path, 'blob_picker_parameters.json'))
        if blob_pick_parameters_min_particle_diameter is not None:
            blob_pick_parameters['Minimum particle diameter (A)'] = blob_pick_parameters_min_particle_diameter
        if blob_pick_parameters_max_particle_diameter is not None:
            blob_pick_parameters['Maximum particle diameter (A)'] = blob_pick_parameters_max_particle_diameter
        toolbox.savetojson(blob_pick_parameters, os.path.join(parameters_folder_path, 'blob_picker_parameters.json'))
    if os.path.exists(os.path.join(parameters_folder_path, 'template_picker_parameters.json')):
        template_pick_parameters = toolbox.readjson(os.path.join(parameters_folder_path, 'template_picker_parameters.json'))
        if args.particle_diameter is not None:
            template_pick_parameters['Particle diameter (A)'] = args.particle_diameter
        toolbox.savetojson(template_pick_parameters, os.path.join(parameters_folder_path, 'template_picker_parameters.json'))
    if os.path.exists(os.path.join(parameters_folder_path, 'extract_micrographs_parameters.json')):
        extract_parameters = toolbox.readjson(os.path.join(parameters_folder_path, 'extract_micrographs_parameters.json'))
        if extract_parameters_extraction_box_size is not None:
            extract_parameters['Extraction box size (pix)'] = extract_parameters_extraction_box_size
        if args.gpu_num is not None:
            extract_parameters['Number of GPUs to parallelize (0 for CPU-only)'] = args.gpu_num
        toolbox.savetojson(extract_parameters, os.path.join(parameters_folder_path, 'extract_micrographs_parameters.json'))
    if os.path.exists(os.path.join(parameters_folder_path, '2d_classification_parameters.json')):
        classification_2d_parameters = toolbox.readjson(os.path.join(parameters_folder_path, '2d_classification_parameters.json'))
        if args.gpu_num is not None:
            classification_2d_parameters['Number of GPUs to parallelize'] = args.gpu_num
        toolbox.savetojson(classification_2d_parameters, os.path.join(parameters_folder_path, '2d_classification_parameters.json'))
    if os.path.exists(os.path.join(parameters_folder_path, 'nurefine_parameters_final.json')):
        nurefine_parameters_final = toolbox.readjson(os.path.join(parameters_folder_path, 'nurefine_parameters_final.json'))
        if args.symmetry is not None:
            nurefine_parameters_final['Symmetry'] = args.symmetry
        toolbox.savetojson(nurefine_parameters_final, os.path.join(parameters_folder_path, 'nurefine_parameters_final.json'))
    if os.path.exists(os.path.join(parameters_folder_path, 'reference_motion_correction_parameters.json')):
        reference_motion_correction_parameters = toolbox.readjson(os.path.join(parameters_folder_path, 'reference_motion_correction_parameters.json'))
        if args.gpu_num is not None:
            reference_motion_correction_parameters['Number of GPUs'] = args.gpu_num
        toolbox.savetojson(reference_motion_correction_parameters, os.path.join(parameters_folder_path, 'reference_motion_correction_parameters.json'))
    if os.path.exists(os.path.join(parameters_folder_path, 'curate_exposures_parameters.json')):
        curate_exposures_parameters = toolbox.readjson(os.path.join(parameters_folder_path, 'curate_exposures_parameters.json'))
        if args.ctf_fit_resolution is not None:
            curate_exposures_parameters['CTF fit resolution (Å)'] = args.ctf_fit_resolution
        toolbox.savetojson(curate_exposures_parameters, os.path.join(parameters_folder_path, 'curate_exposures_parameters.json'))
    if os.path.exists(os.path.join(parameters_folder_path, 'orientation_diagnostics_parameters_final.json')):
        orientation_diagnostics_parameters_final = toolbox.readjson(os.path.join(parameters_folder_path, 'orientation_diagnostics_parameters_final.json'))
        if args.symmetry is not None:
            orientation_diagnostics_parameters_final['Symmetry'] = args.symmetry
        toolbox.savetojson(orientation_diagnostics_parameters_final, os.path.join(parameters_folder_path, 'orientation_diagnostics_parameters_final.json'))

    # other if




def make_pipeline(cryowizard_data_dir):
    if not os.path.exists(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', 'base_parameters')):
        print('Base parameters do not exist, please create base parameters first', flush=True)
        return None, None, None
    # get parameters folder info
    all_parameters_folder_info = []
    all_parameter_type_folder = os.listdir(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters'))
    for single_parameter_type_folder in all_parameter_type_folder:
        if single_parameter_type_folder in ['import', 'preprocess', 'cryoranker', 'refine', 'postprocess']:
            single_parameter_type_folder_files_list = os.listdir(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', single_parameter_type_folder))
            for single_parameters_folder in single_parameter_type_folder_files_list:
                single_parameters_folder_head = single_parameters_folder.split('_')[0]
                if (single_parameters_folder_head == single_parameter_type_folder):
                    source_job_uids = []
                    if_need_source_job_inputs_flag = False
                    if os.path.exists(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', single_parameter_type_folder, single_parameters_folder, 'source_movie_job_uid.json')):
                        if_need_source_job_inputs_flag = True
                        source_job_uids += toolbox.readjson(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', single_parameter_type_folder, single_parameters_folder, 'source_movie_job_uid.json'))['source_job_uid']
                    if os.path.exists(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', single_parameter_type_folder, single_parameters_folder, 'source_micrograph_job_uid.json')):
                        if_need_source_job_inputs_flag = True
                        source_job_uids += toolbox.readjson(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', single_parameter_type_folder, single_parameters_folder, 'source_micrograph_job_uid.json'))['source_job_uid']
                    if os.path.exists(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', single_parameter_type_folder, single_parameters_folder, 'source_particle_job_uid.json')):
                        if_need_source_job_inputs_flag = True
                        source_job_uids += toolbox.readjson(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', single_parameter_type_folder, single_parameters_folder, 'source_particle_job_uid.json'))['source_job_uid']
                    if os.path.exists(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', single_parameter_type_folder, single_parameters_folder, 'source_template_job_uid.json')):
                        if_need_source_job_inputs_flag = True
                        source_job_uids += toolbox.readjson(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', single_parameter_type_folder, single_parameters_folder, 'source_template_job_uid.json'))['source_job_uid']
                    if os.path.exists(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', single_parameter_type_folder, single_parameters_folder, 'source_volume_job_uid.json')):
                        if_need_source_job_inputs_flag = True
                        source_job_uids += toolbox.readjson(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', single_parameter_type_folder, single_parameters_folder, 'source_volume_job_uid.json'))['source_job_uid']
                    if os.path.exists(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', single_parameter_type_folder, single_parameters_folder, 'source_mask_job_uid.json')):
                        if_need_source_job_inputs_flag = True
                        source_job_uids += toolbox.readjson(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', single_parameter_type_folder, single_parameters_folder, 'source_mask_job_uid.json'))['source_job_uid']
                    if os.path.exists(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', single_parameter_type_folder, single_parameters_folder, 'source_cryoranker_job_uid.json')):
                        if_need_source_job_inputs_flag = True
                        source_job_uids += toolbox.readjson(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', single_parameter_type_folder, single_parameters_folder, 'source_cryoranker_job_uid.json'))['source_job_uid']
                    request_pipeline_jobs = []
                    for single_source_job_uid in source_job_uids:
                        single_source_job_uid_head = single_source_job_uid.split('_')[0]
                        if ((single_source_job_uid_head in ['import', 'preprocess', 'cryoranker', 'refine', 'postprocess']) or (single_source_job_uid_head[0] == 'J')):
                            request_pipeline_jobs.append(single_source_job_uid)
                    request_pipeline_jobs = list(set(request_pipeline_jobs))
                    all_parameters_folder_info.append({
                        'single_parameters_folder_name': single_parameters_folder,
                        'single_parameters_folder_type': toolbox.readjson(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', single_parameter_type_folder, single_parameters_folder, 'type.json'))['parameters_type'],
                        'single_parameters_folder_request_jobs': request_pipeline_jobs,
                        'single_parameters_folder_if_need_job_inputs': if_need_source_job_inputs_flag
                    })
    # set pipeline
    pipeline = []
    used_single_parameters_folder_name_list = []
    for step_count in range(99999):
        single_step_single_parameters_folder_list = []
        for single_parameters_folder_info_ptr in range(len(all_parameters_folder_info)):
            single_parameters_folder_name = all_parameters_folder_info[single_parameters_folder_info_ptr]['single_parameters_folder_name']
            single_parameters_folder_type = all_parameters_folder_info[single_parameters_folder_info_ptr]['single_parameters_folder_type']
            single_parameters_folder_request_jobs = all_parameters_folder_info[single_parameters_folder_info_ptr]['single_parameters_folder_request_jobs']
            single_parameters_folder_if_need_job_inputs = all_parameters_folder_info[single_parameters_folder_info_ptr]['single_parameters_folder_if_need_job_inputs']
            if single_parameters_folder_name in used_single_parameters_folder_name_list:
                continue
            single_parameters_folder_all_jobs_ready_flag = True
            if (single_parameters_folder_if_need_job_inputs and (len(single_parameters_folder_request_jobs) == 0)):
                single_parameters_folder_all_jobs_ready_flag = False
            else:
                for single_parameters_folder_single_request_job in single_parameters_folder_request_jobs:
                    if ((not (single_parameters_folder_single_request_job[0] == 'J')) and (single_parameters_folder_single_request_job not in used_single_parameters_folder_name_list)):
                        single_parameters_folder_all_jobs_ready_flag = False
                        break
            if single_parameters_folder_all_jobs_ready_flag:
                single_step_single_parameters_folder_list.append(single_parameters_folder_name)
        single_step_single_parameters_folder_list = sorted(list(set(single_step_single_parameters_folder_list)), reverse=False)
        if (len(single_step_single_parameters_folder_list) == 0):
            break
        else:
            pipeline.append({'step': step_count, 'nodes': single_step_single_parameters_folder_list})
            used_single_parameters_folder_name_list += single_step_single_parameters_folder_list
    toolbox.savetojson(pipeline, os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', 'base_parameters', 'pipeline.json'))
    return all_parameters_folder_info, used_single_parameters_folder_name_list, pipeline


def make_cryowizard_connections(cryosparc_username, cryosparc_password, project, cryowizard_job_uid):
    import cryowizardlib.CSLogin as CSLogin
    cryowizard_data_dir = get_cryowizard_job_data_path(cryosparc_username, cryosparc_password, project, cryowizard_job_uid)
    if not os.path.exists(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', 'base_parameters')):
        print('Base parameters do not exist, please create base parameters first', flush=True)
        return
    parameters = toolbox.readjson(os.path.join(cryowizard_data_dir, 'parameters', 'base_parameters', 'parameters.json'))
    cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(email=cryosparc_username, password=cryosparc_password)
    dealjobs = JobAPIs.DealJobs(cshandle, parameters['project'], parameters['workspace'], parameters['lane'])

    # get parameters folder info
    source_movie_job_uids = []
    source_micrograph_job_uids = []
    source_particle_job_uids = []
    source_template_job_uids = []
    source_volume_job_uids = []
    source_mask_job_uids = []
    source_cryoranker_job_uids = []
    all_parameter_type_folder = os.listdir(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters'))
    for single_parameter_type_folder in all_parameter_type_folder:
        if single_parameter_type_folder in ['import', 'preprocess', 'cryoranker', 'refine', 'postprocess']:
            single_parameter_type_folder_files_list = os.listdir(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', single_parameter_type_folder))
            for single_parameters_folder in single_parameter_type_folder_files_list:
                single_parameters_folder_head = single_parameters_folder.split('_')[0]
                if (single_parameters_folder_head == single_parameter_type_folder):
                    if os.path.exists(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', single_parameter_type_folder, single_parameters_folder, 'source_movie_job_uid.json')):
                        single_source_job_uids = toolbox.readjson(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', single_parameter_type_folder, single_parameters_folder, 'source_movie_job_uid.json'))['source_job_uid']
                        for single_source_job_uid in single_source_job_uids:
                            if (single_source_job_uid[0] == 'J'):
                                source_movie_job_uids.append(single_source_job_uid)
                    if os.path.exists(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', single_parameter_type_folder, single_parameters_folder, 'source_micrograph_job_uid.json')):
                        single_source_job_uids = toolbox.readjson(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', single_parameter_type_folder, single_parameters_folder, 'source_micrograph_job_uid.json'))['source_job_uid']
                        for single_source_job_uid in single_source_job_uids:
                            if (single_source_job_uid[0] == 'J'):
                                source_micrograph_job_uids.append(single_source_job_uid)
                    if os.path.exists(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', single_parameter_type_folder, single_parameters_folder, 'source_particle_job_uid.json')):
                        single_source_job_uids = toolbox.readjson(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', single_parameter_type_folder, single_parameters_folder, 'source_particle_job_uid.json'))['source_job_uid']
                        for single_source_job_uid in single_source_job_uids:
                            if (single_source_job_uid[0] == 'J'):
                                source_particle_job_uids.append(single_source_job_uid)
                    if os.path.exists(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', single_parameter_type_folder, single_parameters_folder, 'source_template_job_uid.json')):
                        single_source_job_uids = toolbox.readjson(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', single_parameter_type_folder, single_parameters_folder, 'source_template_job_uid.json'))['source_job_uid']
                        for single_source_job_uid in single_source_job_uids:
                            if (single_source_job_uid[0] == 'J'):
                                source_template_job_uids.append(single_source_job_uid)
                    if os.path.exists(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', single_parameter_type_folder, single_parameters_folder, 'source_volume_job_uid.json')):
                        single_source_job_uids = toolbox.readjson(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', single_parameter_type_folder, single_parameters_folder, 'source_volume_job_uid.json'))['source_job_uid']
                        for single_source_job_uid in single_source_job_uids:
                            if (single_source_job_uid[0] == 'J'):
                                source_volume_job_uids.append(single_source_job_uid)
                    if os.path.exists(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', single_parameter_type_folder, single_parameters_folder, 'source_mask_job_uid.json')):
                        single_source_job_uids = toolbox.readjson(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', single_parameter_type_folder, single_parameters_folder, 'source_mask_job_uid.json'))['source_job_uid']
                        for single_source_job_uid in single_source_job_uids:
                            if (single_source_job_uid[0] == 'J'):
                                source_mask_job_uids.append(single_source_job_uid)
                    if os.path.exists(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', single_parameter_type_folder, single_parameters_folder, 'source_cryoranker_job_uid.json')):
                        single_source_job_uids = toolbox.readjson(os.path.join(os.path.normpath(cryowizard_data_dir), 'parameters', single_parameter_type_folder, single_parameters_folder, 'source_cryoranker_job_uid.json'))['source_job_uid']
                        for single_source_job_uid in single_source_job_uids:
                            if (single_source_job_uid[0] == 'J'):
                                source_cryoranker_job_uids.append(single_source_job_uid)
    source_movie_job_uids = list(set(source_movie_job_uids))
    source_micrograph_job_uids = list(set(source_micrograph_job_uids))
    source_particle_job_uids = list(set(source_particle_job_uids))
    source_template_job_uids = list(set(source_template_job_uids))
    source_volume_job_uids = list(set(source_volume_job_uids))
    source_mask_job_uids = list(set(source_mask_job_uids))
    source_cryoranker_job_uids = list(set(source_cryoranker_job_uids))

    # connect cryowizard inputs
    cryowizard_job = cshandle.find_project(project).find_external_job(cryowizard_job_uid)
    if (cryowizard_job not in ['building']):
        cryowizard_cache_path = os.path.join(os.path.normpath(os.path.dirname(__file__)), 'cryowizardcache')
        toolbox.packtotargz(os.path.normpath(cryowizard_data_dir), False, False)
        shutil.move(os.path.normpath(cryowizard_data_dir) + '.tar.gz', os.path.join(cryowizard_cache_path, parameters['project'] + '_' + parameters['workspace'] + '_' + cryowizard_job_uid + '_cryowizard.tar.gz'))
        dealjobs.ClearJobSafely([cryowizard_job_uid])
        shutil.move(os.path.join(cryowizard_cache_path, parameters['project'] + '_' + parameters['workspace'] + '_' + cryowizard_job_uid + '_cryowizard.tar.gz'), os.path.normpath(cryowizard_data_dir) + '.tar.gz')
        toolbox.unpacktargz(os.path.normpath(cryowizard_data_dir) + '.tar.gz', True, False)
    cryowizard_job.disconnect('input_movies')
    cryowizard_job.disconnect('input_micrographs')
    cryowizard_job.disconnect('input_particles')
    cryowizard_job.disconnect('input_cryorankers')
    cryowizard_job.disconnect('input_templates')
    cryowizard_job.disconnect('input_volumes')
    cryowizard_job.disconnect('input_masks')
    for source_movie_job_uid in source_movie_job_uids:
        cryowizard_job.connect(target_input='input_movies', source_job_uid=JobAPIs.extract_source_job_ids(source_movie_job_uid), source_output=dealjobs.GetCryoSPARCJobOutputNames(source_movie_job_uid)['movie'])
    for source_micrograph_job_uid in source_micrograph_job_uids:
        cryowizard_job.connect(target_input='input_micrographs', source_job_uid=JobAPIs.extract_source_job_ids(source_micrograph_job_uid), source_output=dealjobs.GetCryoSPARCJobOutputNames(source_micrograph_job_uid)['micrograph'])
    for source_particle_job_uid in source_particle_job_uids:
        cryowizard_job.connect(target_input='input_particles', source_job_uid=JobAPIs.extract_source_job_ids(source_particle_job_uid), source_output=dealjobs.GetCryoSPARCJobOutputNames(source_particle_job_uid)['particle'])
    for source_template_job_uid in source_template_job_uids:
        cryowizard_job.connect(target_input='input_templates', source_job_uid=JobAPIs.extract_source_job_ids(source_template_job_uid), source_output=dealjobs.GetCryoSPARCJobOutputNames(source_template_job_uid)['template'])
    for source_volume_job_uid in source_volume_job_uids:
        cryowizard_job.connect(target_input='input_volumes', source_job_uid=JobAPIs.extract_source_job_ids(source_volume_job_uid), source_output=dealjobs.GetCryoSPARCJobOutputNames(source_volume_job_uid)['volume'])
    for source_mask_job_uid in source_mask_job_uids:
        cryowizard_job.connect(target_input='input_masks', source_job_uid=JobAPIs.extract_source_job_ids(source_mask_job_uid), source_output=dealjobs.GetCryoSPARCJobOutputNames(source_mask_job_uid)['mask'])
    for source_cryoranker_job_uid in source_cryoranker_job_uids:
        cryowizard_job.connect(target_input='input_cryorankers', source_job_uid=JobAPIs.extract_source_job_ids(source_cryoranker_job_uid), source_output=dealjobs.GetCryoSPARCJobOutputNames(source_cryoranker_job_uid)['particle'])







