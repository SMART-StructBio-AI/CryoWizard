#!/usr/bin/env python

import numpy as np
import os

import sys
sys.path.append(os.path.dirname(__file__))

import cryowizardlib.CSLogin as CSLogin
import cryowizardlib.JobAPIs as JobAPIs
import cryowizardlib.Toolbox as toolbox



def motion_and_ctf_refine(cryowizardjob, cryowizardlog, project_dir, parameters_folder_name):
    filedir = os.path.normpath(os.path.dirname(__file__))
    globaldir = os.path.normpath(project_dir)
    parametersdir = os.path.join(globaldir, 'parameters', 'postprocess', parameters_folder_name)
    metadatadir = os.path.join(globaldir, 'metadata', 'postprocess', parameters_folder_name)

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

    source_mask_job_id_name_list = toolbox.readjson(os.path.join(parametersdir, 'source_mask_job_uid.json'))['source_job_uid']
    source_mask_job_id = JobAPIs.resolve_source_job_uids(globaldir, source_mask_job_id_name_list, 'mask')
    if (len(source_mask_job_id) > 0):
        source_mask_job_id = source_mask_job_id[0]
        source_mask_job_id_name = dealjobs.GetCryoSPARCJobOutputNames(source_mask_job_id)['mask']
    else:
        source_mask_job_id = None
        source_mask_job_id_name = None

    # source_job_list_with_alignment3D + source_job_list_without_alignment3D = source_job_id
    # source_job_list_with_location + source_job_list_without_location = source_job_list_with_alignment3D
    # source_job_list_with_motion_info + source_job_list_without_motion_info = source_job_list_with_location
    source_job_list_with_alignment3D, source_job_list_without_alignment3D = JobAPIs.split_particles_by_slots(dealjobs, source_job_id, dealjobs.GetCryoSPARCJobListOutputNames(source_job_id, 'particle'), ['alignments3D'], ['alignments3D/pose'])
    source_job_list_with_location, source_job_list_without_location = JobAPIs.split_particles_by_slots(dealjobs, source_job_list_with_alignment3D, dealjobs.GetCryoSPARCJobListOutputNames(source_job_list_with_alignment3D, 'particle'), ['location'], ['location/micrograph_path'])
    source_job_list_with_motion_info = []
    source_job_list_without_motion_info = []
    source_job_list_with_motion_info_micrograph_jobs = []
    for source_particle_job_ptr in range(len(source_job_list_with_location)):
        source_micrograph_jobs = []
        source_particle_job = dealjobs.cshandle.find_job(dealjobs.project, JobAPIs.extract_source_job_ids(source_job_list_with_location[source_particle_job_ptr]))
        loaded_dataset = source_particle_job.load_output(dealjobs.GetCryoSPARCJobOutputNames(source_job_list_with_location[source_particle_job_ptr])['particle'], slots=['blob', 'ctf', 'location', 'alignments3D'])
        for dataset_ptr in range(len(loaded_dataset)):
            single_source_micrograph_job = loaded_dataset[dataset_ptr]['location/micrograph_path'].split('/')[0]
            source_micrograph_jobs.append(single_source_micrograph_job)
        source_micrograph_jobs = list(set(source_micrograph_jobs))
        source_micrograph_jobs = [(single_source_micrograph_job + '_' + dealjobs.GetCryoSPARCJobOutputNames(single_source_micrograph_job)['micrograph']) for single_source_micrograph_job in source_micrograph_jobs]
        source_micrograph_job_list_with_motion_info, source_micrograph_job_list_without_motion_info = JobAPIs.split_particles_by_slots(dealjobs, source_micrograph_jobs, dealjobs.GetCryoSPARCJobListOutputNames(source_micrograph_jobs, 'micrograph'), ['movie_blob', 'rigid_motion', 'background_blob'], ['movie_blob/path', 'rigid_motion/idx', 'background_blob/idx'])
        if ((len(source_micrograph_job_list_without_motion_info) == 0) and (len(source_micrograph_job_list_with_motion_info) > 0)):
            source_job_list_with_motion_info.append(source_job_list_with_location[source_particle_job_ptr])
            source_job_list_with_motion_info_micrograph_jobs += source_micrograph_job_list_with_motion_info
        else:
            source_job_list_without_motion_info.append(source_job_list_with_location[source_particle_job_ptr])
    source_job_list_with_motion_info_micrograph_jobs = list(set(source_job_list_with_motion_info_micrograph_jobs))

    created_jobs_info = []
    restack_particles_class = JobAPIs.CreateRestackParticles(dealjobs)
    restack_particles_parameters = toolbox.readjson(os.path.join(parametersdir, 'restack_particles_parameters.json'))
    particle_sets_tool_class = JobAPIs.CreateParticleSetsTool(dealjobs)
    particle_sets_tool_parameters = toolbox.readyaml(os.path.join(filedir, 'cryowizard_settings.yml'))['CryoSPARC_job_settings']['ParticleSetsTool']
    particle_sets_tool_parameters['Split num. batches'] = 1
    particle_sets_tool_parameters['Split randomize'] = True
    nurefine_final_class = JobAPIs.CreateNonuniformRefine(dealjobs)
    nurefine_final_parameters = toolbox.readjson(os.path.join(parametersdir, 'nurefine_parameters_final.json'))
    reference_motion_correction_class = JobAPIs.CreateReferenceMotionCorrection(dealjobs)
    reference_motion_correction_parameters = toolbox.readjson(os.path.join(parametersdir, 'reference_motion_correction_parameters.json'))
    ctf_refine_global_class = JobAPIs.CreateCTFRefineGlobal(dealjobs)
    ctf_refine_global_parameters = toolbox.readjson(os.path.join(parametersdir, 'ctf_refine_global_parameters.json'))
    ctf_refine_local_class = JobAPIs.CreateCTFRefineLocal(dealjobs)
    ctf_refine_local_parameters = toolbox.readjson(os.path.join(parametersdir, 'ctf_refine_local_parameters.json'))
    source_ctf_refine_jobs = source_job_list_without_motion_info + source_job_list_without_location
    source_ctf_refine_jobs_names = dealjobs.GetCryoSPARCJobListOutputNames(source_ctf_refine_jobs, 'particle')
    if ((len(source_job_list_with_motion_info) > 0) and (len(source_job_list_with_motion_info_micrograph_jobs) > 0)):
        particle_sets_tool_job = particle_sets_tool_class.QueueParticleSetsToolJob(particle_sets_tool_parameters, JobAPIs.extract_source_job_ids(source_job_list_with_motion_info), dealjobs.GetCryoSPARCJobListOutputNames(source_job_list_with_motion_info, 'particle'))
        created_jobs_info.append(JobAPIs.create_created_jobs_info_item(particle_sets_tool_job.uid, parents=source_job_list_with_motion_info))
        JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Particle sets tool job created: ' + particle_sets_tool_job.uid)
        reference_motion_correction_job = reference_motion_correction_class.QueueReferenceMotionCorrectionJob(reference_motion_correction_parameters, JobAPIs.extract_source_job_ids(source_job_list_with_motion_info_micrograph_jobs), dealjobs.GetCryoSPARCJobListOutputNames(source_job_list_with_motion_info_micrograph_jobs, 'micrograph'), particle_sets_tool_job.uid, 'split_0', JobAPIs.extract_source_job_ids(source_volume_job_id), source_volume_job_id_name, JobAPIs.extract_source_job_ids(source_mask_job_id), source_mask_job_id_name)
        created_jobs_info.append(JobAPIs.create_created_jobs_info_item(reference_motion_correction_job.uid, parents=(source_job_list_with_motion_info_micrograph_jobs + ([source_volume_job_id, source_mask_job_id] if (source_mask_job_id is not None) else [source_volume_job_id])), gpu_need=reference_motion_correction_parameters['Number of GPUs']))
        JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Reference Motion Correction job created: ' + reference_motion_correction_job.uid)
        current_particles_job_uid = reference_motion_correction_job.uid
        current_particles_job_name = 'particles_0'
        if parameters['low_cache_mode']:
            restack_particles_job = restack_particles_class.QueueRestackJob(restack_particles_parameters, [current_particles_job_uid], [current_particles_job_name])
            created_jobs_info.append(JobAPIs.create_created_jobs_info_item(restack_particles_job.uid, parents=[current_particles_job_uid]))
            JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Restack Particles job created: ' + restack_particles_job.uid)
            current_particles_job_uid = restack_particles_job.uid
            current_particles_job_name = 'particles'
        nurefine_final_job = nurefine_final_class.QueueNonuniformRefineJob(nurefine_final_parameters, [current_particles_job_uid], [current_particles_job_name], JobAPIs.extract_source_job_ids(source_volume_job_id), source_volume_job_id_name)
        created_jobs_info.append(JobAPIs.create_created_jobs_info_item(nurefine_final_job.uid, parents=[current_particles_job_uid, source_volume_job_id], gpu_need=1))
        JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Final Non-uniform Refinement job created: ' + nurefine_final_job.uid)
        source_ctf_refine_jobs.append(nurefine_final_job.uid + '_particles')
        source_ctf_refine_jobs_names.append('particles')
        source_volume_job_id = nurefine_final_job.uid + '_volume'
        source_volume_job_id_name = 'volume'
        source_mask_job_id = nurefine_final_job.uid + '_mask'
        source_mask_job_id_name = 'mask'
    if (len(source_ctf_refine_jobs) > 0):
        ctf_refine_global_job = ctf_refine_global_class.QueueCTFRefineGlobalJob(ctf_refine_global_parameters, JobAPIs.extract_source_job_ids(source_ctf_refine_jobs), source_ctf_refine_jobs_names, JobAPIs.extract_source_job_ids(source_volume_job_id), source_volume_job_id_name, JobAPIs.extract_source_job_ids(source_mask_job_id), source_mask_job_id_name)
        created_jobs_info.append(JobAPIs.create_created_jobs_info_item(ctf_refine_global_job.uid, parents=(source_ctf_refine_jobs + ([source_volume_job_id, source_mask_job_id] if (source_mask_job_id is not None) else [source_volume_job_id])), gpu_need=1))
        JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Global CTF Refine job created: ' + ctf_refine_global_job.uid)
        ctf_refine_local_job = ctf_refine_local_class.QueueCTFRefineLocalJob(ctf_refine_local_parameters, [ctf_refine_global_job.uid], ['particles'], JobAPIs.extract_source_job_ids(source_volume_job_id), source_volume_job_id_name, JobAPIs.extract_source_job_ids(source_mask_job_id), source_mask_job_id_name)
        created_jobs_info.append(JobAPIs.create_created_jobs_info_item(ctf_refine_local_job.uid, parents=([ctf_refine_global_job.uid] + ([source_volume_job_id, source_mask_job_id] if (source_mask_job_id is not None) else [source_volume_job_id])), gpu_need=1))
        JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Local CTF Refine job created: ' + ctf_refine_local_job.uid)
        current_particles_job_uid = ctf_refine_local_job.uid
        current_particles_job_name = 'particles'
        if parameters['low_cache_mode']:
            restack_particles_job = restack_particles_class.QueueRestackJob(restack_particles_parameters, [current_particles_job_uid], [current_particles_job_name])
            created_jobs_info.append(JobAPIs.create_created_jobs_info_item(restack_particles_job.uid, parents=[current_particles_job_uid]))
            JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Restack Particles job created: ' + restack_particles_job.uid)
            current_particles_job_uid = restack_particles_job.uid
            current_particles_job_name = 'particles'
        nurefine_final_job = nurefine_final_class.QueueNonuniformRefineJob(nurefine_final_parameters, [current_particles_job_uid], [current_particles_job_name], JobAPIs.extract_source_job_ids(source_volume_job_id), source_volume_job_id_name)
        created_jobs_info.append(JobAPIs.create_created_jobs_info_item(nurefine_final_job.uid, parents=[current_particles_job_uid, source_volume_job_id], gpu_need=1))
        JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Final Non-uniform Refinement job created: ' + nurefine_final_job.uid)
        output_groups = JobAPIs.create_output_groups(particle=[nurefine_final_job.uid + '_particles'], volume=[nurefine_final_job.uid + '_volume'], mask=[nurefine_final_job.uid + '_mask'])
        toolbox.savetojson(output_groups, os.path.join(metadatadir, 'output_groups.json'), False)
    else:
        output_groups = JobAPIs.create_output_groups()
        toolbox.savetojson(output_groups, os.path.join(metadatadir, 'output_groups.json'), False)
    toolbox.savetojson(created_jobs_info, os.path.join(metadatadir, 'created_jobs_info.json'), False)











