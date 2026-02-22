#!/usr/bin/env python

import numpy as np
import os

import sys
sys.path.append(os.path.dirname(__file__))

import cryowizardlib.CSLogin as CSLogin
import cryowizardlib.JobAPIs as JobAPIs
import cryowizardlib.Toolbox as toolbox



def movie_to_particle_with_blob_pick(cryowizardjob, cryowizardlog, project_dir, parameters_folder_name):
    globaldir = os.path.normpath(project_dir)
    parametersdir = os.path.join(globaldir, 'parameters', 'preprocess', parameters_folder_name)
    metadatadir = os.path.join(globaldir, 'metadata', 'preprocess', parameters_folder_name)

    # initialize
    if not os.path.exists(metadatadir):
        os.makedirs(metadatadir)
    parameters = toolbox.readjson(os.path.join(globaldir, 'parameters', 'base_parameters', 'parameters.json'))
    cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(email=parameters['cryosparc_username'], password=parameters['cryosparc_password'])
    dealjobs = JobAPIs.DealJobs(cshandle, parameters['project'], parameters['workspace'], parameters['lane'])

    # build jobs
    created_jobs_info = []
    source_job_id_name_list = toolbox.readjson(os.path.join(parametersdir, 'source_movie_job_uid.json'))['source_job_uid']
    source_job_id = JobAPIs.resolve_source_job_uids(globaldir, source_job_id_name_list, 'movie')

    motion_correction_class = JobAPIs.CreatePatchMotionCorrection(dealjobs)
    motion_correction_parameters = toolbox.readjson(os.path.join(parametersdir, 'patch_motion_correction_parameters.json'))
    ctf_estimation_class = JobAPIs.CreatePatchCtfEstimation(dealjobs)
    ctf_estimation_parameters = toolbox.readjson(os.path.join(parametersdir, 'patch_ctf_estimation_parameters.json'))
    curate_exposures_class = JobAPIs.CreateCurateExposures(dealjobs)
    curate_exposures_parameters = toolbox.readjson(os.path.join(parametersdir, 'curate_exposures_parameters.json'))
    blob_pick_class = JobAPIs.CreateBlobPicker(dealjobs)
    blob_pick_parameters = toolbox.readjson(os.path.join(parametersdir, 'blob_picker_parameters.json'))
    extract_class = JobAPIs.CreateExtractMicrographs(dealjobs)
    extract_parameters = toolbox.readjson(os.path.join(parametersdir, 'extract_micrographs_parameters.json'))
    motion_correction_job = motion_correction_class.QueuePatchMotionCorrectionJob(motion_correction_parameters, JobAPIs.extract_source_job_ids(source_job_id), dealjobs.GetCryoSPARCJobListOutputNames(source_job_id, 'movie'))
    created_jobs_info.append(JobAPIs.create_created_jobs_info_item(motion_correction_job.uid, parents=source_job_id, gpu_need=motion_correction_parameters['Number of GPUs to parallelize']))
    JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Patch Motion Correction job created: ' + motion_correction_job.uid)
    ctf_estimation_job = ctf_estimation_class.QueuePatchCtfEstimationJob(ctf_estimation_parameters, [motion_correction_job.uid], ['micrographs'])
    created_jobs_info.append(JobAPIs.create_created_jobs_info_item(ctf_estimation_job.uid, parents=[motion_correction_job.uid], gpu_need=ctf_estimation_parameters['Number of GPUs to parallelize']))
    JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Patch CTF Estimation job created: ' + ctf_estimation_job.uid)
    curate_exposures_job = curate_exposures_class.QueueCurateExposuresJob(curate_exposures_parameters, [ctf_estimation_job.uid], ['exposures'])
    created_jobs_info.append(JobAPIs.create_created_jobs_info_item(curate_exposures_job.uid, parents=[ctf_estimation_job.uid]))
    JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Curate Exposures job created: ' + curate_exposures_job.uid)
    blob_pick_job = blob_pick_class.QueueBlobPickerJob(blob_pick_parameters, [curate_exposures_job.uid], ['exposures_accepted'])
    created_jobs_info.append(JobAPIs.create_created_jobs_info_item(blob_pick_job.uid, parents=[curate_exposures_job.uid], gpu_need=1))
    JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Blob Picker job created: ' + blob_pick_job.uid)
    extract_job = extract_class.QueueExtractMicrographsJob(extract_parameters, [blob_pick_job.uid], ['micrographs'], [blob_pick_job.uid], ['particles'])
    created_jobs_info.append(JobAPIs.create_created_jobs_info_item(extract_job.uid, parents=[blob_pick_job.uid], gpu_need=extract_parameters['Number of GPUs to parallelize (0 for CPU-only)']))
    JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Extract From Micrographs job created: ' + extract_job.uid)
    toolbox.savetojson(created_jobs_info, os.path.join(metadatadir, 'created_jobs_info.json'), False)
    output_groups = JobAPIs.create_output_groups(movie=source_job_id, micrograph=[ctf_estimation_job.uid + '_exposures'], particle=[extract_job.uid + '_particles'], template=[blob_pick_job.uid + '_templates'])
    toolbox.savetojson(output_groups, os.path.join(metadatadir, 'output_groups.json'), False)


def movie_to_particle_with_template_pick(cryowizardjob, cryowizardlog, project_dir, parameters_folder_name):
    globaldir = os.path.normpath(project_dir)
    parametersdir = os.path.join(globaldir, 'parameters', 'preprocess', parameters_folder_name)
    metadatadir = os.path.join(globaldir, 'metadata', 'preprocess', parameters_folder_name)

    # initialize
    if not os.path.exists(metadatadir):
        os.makedirs(metadatadir)
    parameters = toolbox.readjson(os.path.join(globaldir, 'parameters', 'base_parameters', 'parameters.json'))
    cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(email=parameters['cryosparc_username'], password=parameters['cryosparc_password'])
    dealjobs = JobAPIs.DealJobs(cshandle, parameters['project'], parameters['workspace'], parameters['lane'])

    # build jobs
    created_jobs_info = []
    source_job_id_name_list = toolbox.readjson(os.path.join(parametersdir, 'source_movie_job_uid.json'))['source_job_uid']
    source_job_id = JobAPIs.resolve_source_job_uids(globaldir, source_job_id_name_list, 'movie')

    source_template_job_id_name_list = toolbox.readjson(os.path.join(parametersdir, 'source_template_job_uid.json'))['source_job_uid']
    source_template_job_id = JobAPIs.resolve_source_job_uids(globaldir, source_template_job_id_name_list, 'template')

    motion_correction_class = JobAPIs.CreatePatchMotionCorrection(dealjobs)
    motion_correction_parameters = toolbox.readjson(os.path.join(parametersdir, 'patch_motion_correction_parameters.json'))
    ctf_estimation_class = JobAPIs.CreatePatchCtfEstimation(dealjobs)
    ctf_estimation_parameters = toolbox.readjson(os.path.join(parametersdir, 'patch_ctf_estimation_parameters.json'))
    curate_exposures_class = JobAPIs.CreateCurateExposures(dealjobs)
    curate_exposures_parameters = toolbox.readjson(os.path.join(parametersdir, 'curate_exposures_parameters.json'))
    template_pick_class = JobAPIs.CreateTemplatePicker(dealjobs)
    template_pick_parameters = toolbox.readjson(os.path.join(parametersdir, 'template_picker_parameters.json'))
    extract_class = JobAPIs.CreateExtractMicrographs(dealjobs)
    extract_parameters = toolbox.readjson(os.path.join(parametersdir, 'extract_micrographs_parameters.json'))
    motion_correction_job = motion_correction_class.QueuePatchMotionCorrectionJob(motion_correction_parameters, JobAPIs.extract_source_job_ids(source_job_id), dealjobs.GetCryoSPARCJobListOutputNames(source_job_id, 'movie'))
    created_jobs_info.append(JobAPIs.create_created_jobs_info_item(motion_correction_job.uid, parents=source_job_id, gpu_need=motion_correction_parameters['Number of GPUs to parallelize']))
    JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Patch Motion Correction job created: ' + motion_correction_job.uid)
    ctf_estimation_job = ctf_estimation_class.QueuePatchCtfEstimationJob(ctf_estimation_parameters, [motion_correction_job.uid], ['micrographs'])
    created_jobs_info.append(JobAPIs.create_created_jobs_info_item(ctf_estimation_job.uid, parents=[motion_correction_job.uid], gpu_need=ctf_estimation_parameters['Number of GPUs to parallelize']))
    JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Patch CTF Estimation job created: ' + ctf_estimation_job.uid)
    curate_exposures_job = curate_exposures_class.QueueCurateExposuresJob(curate_exposures_parameters, [ctf_estimation_job.uid], ['exposures'])
    created_jobs_info.append(JobAPIs.create_created_jobs_info_item(curate_exposures_job.uid, parents=[ctf_estimation_job.uid]))
    JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Curate Exposures job created: ' + curate_exposures_job.uid)
    template_pick_job = template_pick_class.QueueTemplatePickerJob(template_pick_parameters, [curate_exposures_job.uid], ['exposures_accepted'], JobAPIs.extract_source_job_ids(source_template_job_id), dealjobs.GetCryoSPARCJobListOutputNames(source_template_job_id, 'template'))
    created_jobs_info.append(JobAPIs.create_created_jobs_info_item(template_pick_job.uid, parents=([curate_exposures_job.uid] + source_template_job_id), gpu_need=1))
    JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Template Picker job created: ' + template_pick_job.uid)
    extract_job = extract_class.QueueExtractMicrographsJob(extract_parameters, [template_pick_job.uid], ['micrographs'], [template_pick_job.uid], ['particles'])
    created_jobs_info.append(JobAPIs.create_created_jobs_info_item(extract_job.uid, parents=[template_pick_job.uid], gpu_need=extract_parameters['Number of GPUs to parallelize (0 for CPU-only)']))
    JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Extract From Micrographs job created: ' + extract_job.uid)
    toolbox.savetojson(created_jobs_info, os.path.join(metadatadir, 'created_jobs_info.json'), False)
    output_groups = JobAPIs.create_output_groups(movie=source_job_id, micrograph=[ctf_estimation_job.uid + '_exposures'], particle=[extract_job.uid + '_particles'], template=source_template_job_id)
    toolbox.savetojson(output_groups, os.path.join(metadatadir, 'output_groups.json'), False)


def micrograph_to_particle_with_blob_pick(cryowizardjob, cryowizardlog, project_dir, parameters_folder_name):
    globaldir = os.path.normpath(project_dir)
    parametersdir = os.path.join(globaldir, 'parameters', 'preprocess', parameters_folder_name)
    metadatadir = os.path.join(globaldir, 'metadata', 'preprocess', parameters_folder_name)

    # initialize
    if not os.path.exists(metadatadir):
        os.makedirs(metadatadir)
    parameters = toolbox.readjson(os.path.join(globaldir, 'parameters', 'base_parameters', 'parameters.json'))
    cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(email=parameters['cryosparc_username'], password=parameters['cryosparc_password'])
    dealjobs = JobAPIs.DealJobs(cshandle, parameters['project'], parameters['workspace'], parameters['lane'])

    # build jobs
    created_jobs_info = []
    source_job_id_name_list = toolbox.readjson(os.path.join(parametersdir, 'source_micrograph_job_uid.json'))['source_job_uid']
    source_job_id = JobAPIs.resolve_source_job_uids(globaldir, source_job_id_name_list, 'micrograph')

    ctf_estimation_class = JobAPIs.CreatePatchCtfEstimation(dealjobs)
    ctf_estimation_parameters = toolbox.readjson(os.path.join(parametersdir, 'patch_ctf_estimation_parameters.json'))
    curate_exposures_class = JobAPIs.CreateCurateExposures(dealjobs)
    curate_exposures_parameters = toolbox.readjson(os.path.join(parametersdir, 'curate_exposures_parameters.json'))
    blob_pick_class = JobAPIs.CreateBlobPicker(dealjobs)
    blob_pick_parameters = toolbox.readjson(os.path.join(parametersdir, 'blob_picker_parameters.json'))
    extract_class = JobAPIs.CreateExtractMicrographs(dealjobs)
    extract_parameters = toolbox.readjson(os.path.join(parametersdir, 'extract_micrographs_parameters.json'))
    ctf_estimation_job = ctf_estimation_class.QueuePatchCtfEstimationJob(ctf_estimation_parameters, JobAPIs.extract_source_job_ids(source_job_id), dealjobs.GetCryoSPARCJobListOutputNames(source_job_id, 'micrograph'))
    created_jobs_info.append(JobAPIs.create_created_jobs_info_item(ctf_estimation_job.uid, parents=source_job_id, gpu_need=ctf_estimation_parameters['Number of GPUs to parallelize']))
    JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Patch CTF Estimation job created: ' + ctf_estimation_job.uid)
    curate_exposures_job = curate_exposures_class.QueueCurateExposuresJob(curate_exposures_parameters, [ctf_estimation_job.uid], ['exposures'])
    created_jobs_info.append(JobAPIs.create_created_jobs_info_item(curate_exposures_job.uid, parents=[ctf_estimation_job.uid]))
    JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Curate Exposures job created: ' + curate_exposures_job.uid)
    blob_pick_job = blob_pick_class.QueueBlobPickerJob(blob_pick_parameters, [curate_exposures_job.uid], ['exposures_accepted'])
    created_jobs_info.append(JobAPIs.create_created_jobs_info_item(blob_pick_job.uid, parents=[curate_exposures_job.uid], gpu_need=1))
    JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Blob Picker job created: ' + blob_pick_job.uid)
    extract_job = extract_class.QueueExtractMicrographsJob(extract_parameters, [blob_pick_job.uid], ['micrographs'], [blob_pick_job.uid], ['particles'])
    created_jobs_info.append(JobAPIs.create_created_jobs_info_item(extract_job.uid, parents=[blob_pick_job.uid], gpu_need=extract_parameters['Number of GPUs to parallelize (0 for CPU-only)']))
    JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Extract From Micrographs job created: ' + extract_job.uid)
    toolbox.savetojson(created_jobs_info, os.path.join(metadatadir, 'created_jobs_info.json'), False)
    output_groups = JobAPIs.create_output_groups(micrograph=[ctf_estimation_job.uid + '_exposures'], particle=[extract_job.uid + '_particles'], template=[blob_pick_job.uid + '_templates'])
    toolbox.savetojson(output_groups, os.path.join(metadatadir, 'output_groups.json'), False)


def micrograph_to_particle_with_template_pick(cryowizardjob, cryowizardlog, project_dir, parameters_folder_name):
    globaldir = os.path.normpath(project_dir)
    parametersdir = os.path.join(globaldir, 'parameters', 'preprocess', parameters_folder_name)
    metadatadir = os.path.join(globaldir, 'metadata', 'preprocess', parameters_folder_name)

    # initialize
    if not os.path.exists(metadatadir):
        os.makedirs(metadatadir)
    parameters = toolbox.readjson(os.path.join(globaldir, 'parameters', 'base_parameters', 'parameters.json'))
    cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(email=parameters['cryosparc_username'], password=parameters['cryosparc_password'])
    dealjobs = JobAPIs.DealJobs(cshandle, parameters['project'], parameters['workspace'], parameters['lane'])

    # build jobs
    created_jobs_info = []
    source_job_id_name_list = toolbox.readjson(os.path.join(parametersdir, 'source_micrograph_job_uid.json'))['source_job_uid']
    source_job_id = JobAPIs.resolve_source_job_uids(globaldir, source_job_id_name_list, 'micrograph')

    source_template_job_id_name_list = toolbox.readjson(os.path.join(parametersdir, 'source_template_job_uid.json'))['source_job_uid']
    source_template_job_id = JobAPIs.resolve_source_job_uids(globaldir, source_template_job_id_name_list, 'template')

    ctf_estimation_class = JobAPIs.CreatePatchCtfEstimation(dealjobs)
    ctf_estimation_parameters = toolbox.readjson(os.path.join(parametersdir, 'patch_ctf_estimation_parameters.json'))
    curate_exposures_class = JobAPIs.CreateCurateExposures(dealjobs)
    curate_exposures_parameters = toolbox.readjson(os.path.join(parametersdir, 'curate_exposures_parameters.json'))
    template_pick_class = JobAPIs.CreateTemplatePicker(dealjobs)
    template_pick_parameters = toolbox.readjson(os.path.join(parametersdir, 'template_picker_parameters.json'))
    extract_class = JobAPIs.CreateExtractMicrographs(dealjobs)
    extract_parameters = toolbox.readjson(os.path.join(parametersdir, 'extract_micrographs_parameters.json'))
    ctf_estimation_job = ctf_estimation_class.QueuePatchCtfEstimationJob(ctf_estimation_parameters, JobAPIs.extract_source_job_ids(source_job_id), dealjobs.GetCryoSPARCJobListOutputNames(source_job_id, 'micrograph'))
    created_jobs_info.append(JobAPIs.create_created_jobs_info_item(ctf_estimation_job.uid, parents=source_job_id, gpu_need=ctf_estimation_parameters['Number of GPUs to parallelize']))
    JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Patch CTF Estimation job created: ' + ctf_estimation_job.uid)
    curate_exposures_job = curate_exposures_class.QueueCurateExposuresJob(curate_exposures_parameters, [ctf_estimation_job.uid], ['exposures'])
    created_jobs_info.append(JobAPIs.create_created_jobs_info_item(curate_exposures_job.uid, parents=[ctf_estimation_job.uid]))
    JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Curate Exposures job created: ' + curate_exposures_job.uid)
    template_pick_job = template_pick_class.QueueTemplatePickerJob(template_pick_parameters, [curate_exposures_job.uid], ['exposures_accepted'], JobAPIs.extract_source_job_ids(source_template_job_id), dealjobs.GetCryoSPARCJobListOutputNames(source_template_job_id, 'template'))
    created_jobs_info.append(JobAPIs.create_created_jobs_info_item(template_pick_job.uid, parents=([curate_exposures_job.uid] + source_template_job_id), gpu_need=1))
    JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Template Picker job created: ' + template_pick_job.uid)
    extract_job = extract_class.QueueExtractMicrographsJob(extract_parameters, [template_pick_job.uid], ['micrographs'], [template_pick_job.uid], ['particles'])
    created_jobs_info.append(JobAPIs.create_created_jobs_info_item(extract_job.uid, parents=[template_pick_job.uid], gpu_need=extract_parameters['Number of GPUs to parallelize (0 for CPU-only)']))
    JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Extract From Micrographs job created: ' + extract_job.uid)
    toolbox.savetojson(created_jobs_info, os.path.join(metadatadir, 'created_jobs_info.json'), False)
    output_groups = JobAPIs.create_output_groups(micrograph=[ctf_estimation_job.uid + '_exposures'], particle=[extract_job.uid + '_particles'], template=source_template_job_id)
    toolbox.savetojson(output_groups, os.path.join(metadatadir, 'output_groups.json'), False)


def import_particles(cryowizardjob, cryowizardlog, project_dir, parameters_folder_name):
    globaldir = os.path.normpath(project_dir)
    parametersdir = os.path.join(globaldir, 'parameters', 'preprocess', parameters_folder_name)
    metadatadir = os.path.join(globaldir, 'metadata', 'preprocess', parameters_folder_name)

    # initialize
    if not os.path.exists(metadatadir):
        os.makedirs(metadatadir)
    parameters = toolbox.readjson(os.path.join(globaldir, 'parameters', 'base_parameters', 'parameters.json'))
    cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(email=parameters['cryosparc_username'], password=parameters['cryosparc_password'])
    dealjobs = JobAPIs.DealJobs(cshandle, parameters['project'], parameters['workspace'], parameters['lane'])

    # build jobs
    created_jobs_info = []
    source_job_id_name_list = toolbox.readjson(os.path.join(parametersdir, 'source_particle_job_uid.json'))['source_job_uid']
    source_job_id = JobAPIs.resolve_source_job_uids(globaldir, source_job_id_name_list, 'particle')

    toolbox.savetojson(created_jobs_info, os.path.join(metadatadir, 'created_jobs_info.json'), False)
    output_groups = JobAPIs.create_output_groups(particle=source_job_id)
    toolbox.savetojson(output_groups, os.path.join(metadatadir, 'output_groups.json'), False)


def create_templates(cryowizardjob, cryowizardlog, project_dir, parameters_folder_name):
    globaldir = os.path.normpath(project_dir)
    parametersdir = os.path.join(globaldir, 'parameters', 'preprocess', parameters_folder_name)
    metadatadir = os.path.join(globaldir, 'metadata', 'preprocess', parameters_folder_name)

    # initialize
    if not os.path.exists(metadatadir):
        os.makedirs(metadatadir)
    parameters = toolbox.readjson(os.path.join(globaldir, 'parameters', 'base_parameters', 'parameters.json'))
    cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(email=parameters['cryosparc_username'], password=parameters['cryosparc_password'])
    dealjobs = JobAPIs.DealJobs(cshandle, parameters['project'], parameters['workspace'], parameters['lane'])

    # build jobs
    created_jobs_info = []
    source_volume_job_id_name_list = toolbox.readjson(os.path.join(parametersdir, 'source_volume_job_uid.json'))['source_job_uid']
    source_volume_job_id = JobAPIs.resolve_source_job_uids(globaldir, source_volume_job_id_name_list, 'volume')
    if (len(source_volume_job_id) > 0):
        source_volume_job_id = source_volume_job_id[0]
        source_volume_job_id_name = dealjobs.GetCryoSPARCJobOutputNames(source_volume_job_id)['volume']
    else:
        source_volume_job_id = None
        source_volume_job_id_name = None

    created_jobs_info = []
    create_templates_class = JobAPIs.CreateCreateTemplates(dealjobs)
    create_templates_parameters = toolbox.readjson(os.path.join(parametersdir, 'create_templates_parameters.json'))
    create_templates_job = create_templates_class.QueueCreateTemplatesJob(create_templates_parameters, JobAPIs.extract_source_job_ids(source_volume_job_id), source_volume_job_id_name)
    created_jobs_info.append(JobAPIs.create_created_jobs_info_item(create_templates_job.uid, parents=[source_volume_job_id]))
    JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Create Templates job created: ' + create_templates_job.uid)
    toolbox.savetojson(created_jobs_info, os.path.join(metadatadir, 'created_jobs_info.json'), False)
    output_groups = JobAPIs.create_output_groups(template=[create_templates_job.uid + '_templates'])
    toolbox.savetojson(output_groups, os.path.join(metadatadir, 'output_groups.json'), False)


def reference_based_auto_select_2D(cryowizardjob, cryowizardlog, project_dir, parameters_folder_name):
    filedir = os.path.normpath(os.path.dirname(__file__))
    globaldir = os.path.normpath(project_dir)
    parametersdir = os.path.join(globaldir, 'parameters', 'preprocess', parameters_folder_name)
    metadatadir = os.path.join(globaldir, 'metadata', 'preprocess', parameters_folder_name)

    # initialize
    if not os.path.exists(metadatadir):
        os.makedirs(metadatadir)
    parameters = toolbox.readjson(os.path.join(globaldir, 'parameters', 'base_parameters', 'parameters.json'))
    cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(email=parameters['cryosparc_username'], password=parameters['cryosparc_password'])
    dealjobs = JobAPIs.DealJobs(cshandle, parameters['project'], parameters['workspace'], parameters['lane'])

    source_job_id_name_list = toolbox.readjson(os.path.join(parametersdir, 'source_particle_job_uid.json'))['source_job_uid']
    source_job_id = JobAPIs.resolve_source_job_uids(globaldir, source_job_id_name_list, 'particle')

    source_volume_job_id_name_list = toolbox.readjson(os.path.join(parametersdir, 'source_volume_job_uid.json'))['source_job_uid']
    source_volume_job_id = JobAPIs.resolve_source_job_uids(globaldir, source_volume_job_id_name_list, 'volume')
    if (len(source_volume_job_id) > 0):
        source_volume_job_id = source_volume_job_id[0]
        source_volume_job_id_name = dealjobs.GetCryoSPARCJobOutputNames(source_volume_job_id)['volume']
    else:
        source_volume_job_id = None
        source_volume_job_id_name = None

    particle_num = 0
    resolution = None
    pixelsize = None
    for single_source_job_uid in source_job_id:
        single_source_job = dealjobs.cshandle.find_job(dealjobs.project, JobAPIs.extract_source_job_ids(single_source_job_uid))
        single_source_job_particle_dataset = single_source_job.load_output(dealjobs.GetCryoSPARCJobOutputNames(single_source_job_uid)['particle'])
        if ((resolution is None) or (pixelsize is None)):
            resolution = (int)(single_source_job_particle_dataset[0]['blob/shape'][0])
            pixelsize = (float)(single_source_job_particle_dataset[0]['blob/psize_A'])
        particle_num += len(single_source_job_particle_dataset)
    if (particle_num > 1000000):
        split_num = (int)(np.ceil((float)(particle_num) / 1000000.0))
        split_each_count = (int)(np.floor((float)(particle_num) / (float)(split_num)))
    else:
        split_num = 1
        split_each_count = particle_num

    created_jobs_info = []
    restack_particles_class = JobAPIs.CreateRestackParticles(dealjobs)
    restack_particles_parameters = toolbox.readjson(os.path.join(parametersdir, 'restack_particles_parameters.json'))
    particle_sets_tool_class = JobAPIs.CreateParticleSetsTool(dealjobs)
    particle_sets_tool_parameters = toolbox.readyaml(os.path.join(filedir, 'cryowizard_settings.yml'))['CryoSPARC_job_settings']['ParticleSetsTool']
    particle_sets_tool_parameters['Split num. batches'] = split_num
    particle_sets_tool_parameters['Split randomize'] = True
    classification_2d_class = JobAPIs.Create2DClassification(dealjobs)
    classification_2d_parameters = toolbox.readjson(os.path.join(parametersdir, '2d_classification_parameters.json'))
    if (split_each_count < 15000):
        classification_2d_parameters['Number of 2D classes'] = 16
    elif (split_each_count < 50000):
        classification_2d_parameters['Number of 2D classes'] = 32
    elif (split_each_count < 100000):
        classification_2d_parameters['Number of 2D classes'] = 64
    elif (split_each_count < 150000):
        classification_2d_parameters['Number of 2D classes'] = 96
    elif (split_each_count < 350000):
        classification_2d_parameters['Number of 2D classes'] = 128
    elif (split_each_count < 650000):
        classification_2d_parameters['Number of 2D classes'] = 256
    else:
        classification_2d_parameters['Number of 2D classes'] = 384
    reference_select_2d_class = JobAPIs.CreateReferenceBasedAutoSelect2D(dealjobs)
    reference_select_2d_parameters = toolbox.readjson(os.path.join(parametersdir, 'reference_select_2d_parameters.json'))
    reference_select_2d_parameters['Circular mask diameter (A)'] = (int)(np.round(np.floor(pixelsize * resolution * 0.85 / 10.0) * 10.0))

    particle_sets_tool_job = particle_sets_tool_class.QueueParticleSetsToolJob(particle_sets_tool_parameters, JobAPIs.extract_source_job_ids(source_job_id), dealjobs.GetCryoSPARCJobListOutputNames(source_job_id, 'particle'))
    created_jobs_info.append(JobAPIs.create_created_jobs_info_item(particle_sets_tool_job.uid, parents=source_job_id))
    JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Particle sets tool job created: ' + particle_sets_tool_job.uid)
    classification_2d_jobs_uid_list = []
    reference_select_2d_jobs_uid_list_output_particles = []
    reference_select_2d_jobs_uid_list_output_templates = []
    for split_ptr in range(split_num):
        current_particles_job_uid = particle_sets_tool_job.uid
        current_particles_job_name = 'split_' + (str)(split_ptr)
        if parameters['low_cache_mode']:
            restack_particles_job = restack_particles_class.QueueRestackJob(restack_particles_parameters, [current_particles_job_uid], [current_particles_job_name])
            created_jobs_info.append(JobAPIs.create_created_jobs_info_item(restack_particles_job.uid, parents=[current_particles_job_uid]))
            JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Restack Particles job created: ' + restack_particles_job.uid)
            current_particles_job_uid = restack_particles_job.uid
            current_particles_job_name = 'particles'
        classification_2d_job = classification_2d_class.Queue2DClassificationJob(classification_2d_parameters, [current_particles_job_uid], [current_particles_job_name])
        created_jobs_info.append(JobAPIs.create_created_jobs_info_item(classification_2d_job.uid, parents=[current_particles_job_uid], gpu_need=classification_2d_parameters['Number of GPUs to parallelize']))
        JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, '2D Classification job created: ' + classification_2d_job.uid)
        classification_2d_jobs_uid_list.append(classification_2d_job.uid)
        reference_select_2d_job = reference_select_2d_class.QueueReferenceBasedAutoSelect2DJob(reference_select_2d_parameters, classification_2d_job.uid, 'particles', classification_2d_job.uid, 'class_averages', JobAPIs.extract_source_job_ids(source_volume_job_id), source_volume_job_id_name)
        created_jobs_info.append(JobAPIs.create_created_jobs_info_item(reference_select_2d_job.uid, parents=[classification_2d_job.uid, source_volume_job_id], gpu_need=1))
        JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Reference Based Auto Select 2D job created: ' + reference_select_2d_job.uid)
        reference_select_2d_jobs_uid_list_output_particles.append(reference_select_2d_job.uid + '_particles_selected')
        reference_select_2d_jobs_uid_list_output_templates.append(reference_select_2d_job.uid + '_templates_selected')
    toolbox.savetojson(created_jobs_info, os.path.join(metadatadir, 'created_jobs_info.json'), False)
    output_groups = JobAPIs.create_output_groups(particle=reference_select_2d_jobs_uid_list_output_particles, template=reference_select_2d_jobs_uid_list_output_templates, volume=[source_volume_job_id])
    toolbox.savetojson(output_groups, os.path.join(metadatadir, 'output_groups.json'), False)


def micrograph_junk_detector(cryowizardjob, cryowizardlog, project_dir, parameters_folder_name):
    filedir = os.path.normpath(os.path.dirname(__file__))
    globaldir = os.path.normpath(project_dir)
    parametersdir = os.path.join(globaldir, 'parameters', 'preprocess', parameters_folder_name)
    metadatadir = os.path.join(globaldir, 'metadata', 'preprocess', parameters_folder_name)

    # initialize
    if not os.path.exists(metadatadir):
        os.makedirs(metadatadir)
    parameters = toolbox.readjson(os.path.join(globaldir, 'parameters', 'base_parameters', 'parameters.json'))
    cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(email=parameters['cryosparc_username'], password=parameters['cryosparc_password'])
    dealjobs = JobAPIs.DealJobs(cshandle, parameters['project'], parameters['workspace'], parameters['lane'])

    source_job_id_name_list = toolbox.readjson(os.path.join(parametersdir, 'source_particle_job_uid.json'))['source_job_uid']
    source_job_id = JobAPIs.resolve_source_job_uids(globaldir, source_job_id_name_list, 'particle')

    source_job_list_with_location, source_job_list_without_location = JobAPIs.split_particles_by_slots(dealjobs, source_job_id, dealjobs.GetCryoSPARCJobListOutputNames(source_job_id, 'particle'), ['location'], ['location/micrograph_path'])
    source_micrograph_jobs = []
    for source_particle_job_ptr in range(len(source_job_list_with_location)):
        source_particle_job = dealjobs.cshandle.find_job(dealjobs.project, JobAPIs.extract_source_job_ids(source_job_list_with_location[source_particle_job_ptr]))
        loaded_dataset = source_particle_job.load_output(dealjobs.GetCryoSPARCJobOutputNames(source_job_list_with_location[source_particle_job_ptr])['particle'], slots=['blob', 'ctf', 'location'])
        for dataset_ptr in range(len(loaded_dataset)):
            single_source_micrograph_job = loaded_dataset[dataset_ptr]['location/micrograph_path'].split('/')[0]
            source_micrograph_jobs.append(single_source_micrograph_job)
    source_micrograph_jobs = list(set(source_micrograph_jobs))
    source_micrograph_jobs = [(single_source_micrograph_job + '_' + dealjobs.GetCryoSPARCJobOutputNames(single_source_micrograph_job)['micrograph']) for single_source_micrograph_job in source_micrograph_jobs]

    created_jobs_info = []
    junk_detector_class = JobAPIs.CreateMicrographJunkDetector(dealjobs)
    junk_detector_parameters = toolbox.readjson(os.path.join(parametersdir, 'junk_detector_parameters.json'))
    junk_detector_job = junk_detector_class.QueueMicrographJunkDetectorJob(junk_detector_parameters, JobAPIs.extract_source_job_ids(source_micrograph_jobs), dealjobs.GetCryoSPARCJobListOutputNames(source_micrograph_jobs, 'micrograph'), JobAPIs.extract_source_job_ids(source_job_list_with_location), dealjobs.GetCryoSPARCJobListOutputNames(source_job_list_with_location, 'particle'))
    created_jobs_info.append(JobAPIs.create_created_jobs_info_item(junk_detector_job.uid, parents=(source_micrograph_jobs + source_job_list_with_location), gpu_need=1))
    JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Micrograph Junk Detector job created: ' + junk_detector_job.uid)
    toolbox.savetojson(created_jobs_info, os.path.join(metadatadir, 'created_jobs_info.json'), False)
    output_groups = JobAPIs.create_output_groups(micrograph=[junk_detector_job.uid + '_exposures'], particle=([junk_detector_job.uid + '_particles_accepted'] + source_job_list_without_location))
    toolbox.savetojson(output_groups, os.path.join(metadatadir, 'output_groups.json'), False)










