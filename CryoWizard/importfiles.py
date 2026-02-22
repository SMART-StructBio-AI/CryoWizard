#!/usr/bin/env python

import numpy as np
import os

import sys
sys.path.append(os.path.dirname(__file__))

import cryowizardlib.CSLogin as CSLogin
import cryowizardlib.JobAPIs as JobAPIs
import cryowizardlib.Toolbox as toolbox



def import_movie(cryowizardjob, cryowizardlog, project_dir, parameters_folder_name):
    globaldir = os.path.normpath(project_dir)
    parametersdir = os.path.join(globaldir, 'parameters', 'import', parameters_folder_name)
    metadatadir = os.path.join(globaldir, 'metadata', 'import', parameters_folder_name)

    # initialize
    if not os.path.exists(metadatadir):
        os.makedirs(metadatadir)
    parameters = toolbox.readjson(os.path.join(globaldir, 'parameters', 'base_parameters', 'parameters.json'))
    cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(email=parameters['cryosparc_username'], password=parameters['cryosparc_password'])
    dealjobs = JobAPIs.DealJobs(cshandle, parameters['project'], parameters['workspace'], parameters['lane'])

    created_jobs_info = []
    import_movies_class = JobAPIs.CreateImportMovies(dealjobs)
    import_movies_parameters = toolbox.readjson(os.path.join(parametersdir, 'import_movies_parameters.json'))
    import_movies_job = import_movies_class.QueueImportMoviesJob(import_movies_parameters)
    created_jobs_info.append(JobAPIs.create_created_jobs_info_item(import_movies_job.uid))
    JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Import Movies job created: ' + import_movies_job.uid)
    toolbox.savetojson(created_jobs_info, os.path.join(metadatadir, 'created_jobs_info.json'), False)
    output_groups = JobAPIs.create_output_groups(movie=[import_movies_job.uid + '_imported_movies'])
    toolbox.savetojson(output_groups, os.path.join(metadatadir, 'output_groups.json'), False)


def import_micrograph(cryowizardjob, cryowizardlog, project_dir, parameters_folder_name):
    globaldir = os.path.normpath(project_dir)
    parametersdir = os.path.join(globaldir, 'parameters', 'import', parameters_folder_name)
    metadatadir = os.path.join(globaldir, 'metadata', 'import', parameters_folder_name)

    # initialize
    if not os.path.exists(metadatadir):
        os.makedirs(metadatadir)
    parameters = toolbox.readjson(os.path.join(globaldir, 'parameters', 'base_parameters', 'parameters.json'))
    cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(email=parameters['cryosparc_username'], password=parameters['cryosparc_password'])
    dealjobs = JobAPIs.DealJobs(cshandle, parameters['project'], parameters['workspace'], parameters['lane'])

    created_jobs_info = []
    import_micrographs_class = JobAPIs.CreateImportMicrographs(dealjobs)
    import_mircrographs_parameters = toolbox.readjson(os.path.join(parametersdir, 'import_micrographs_parameters.json'))
    import_micrographs_job = import_micrographs_class.QueueImportMicrographsJob(import_mircrographs_parameters)
    created_jobs_info.append(JobAPIs.create_created_jobs_info_item(import_micrographs_job.uid))
    JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Import Micrographs job created: ' + import_micrographs_job.uid)
    toolbox.savetojson(created_jobs_info, os.path.join(metadatadir, 'created_jobs_info.json'), False)
    output_groups = JobAPIs.create_output_groups(micrograph=[import_micrographs_job.uid + '_imported_micrographs'])
    toolbox.savetojson(output_groups, os.path.join(metadatadir, 'output_groups.json'), False)


def import_particle(cryowizardjob, cryowizardlog, project_dir, parameters_folder_name):
    globaldir = os.path.normpath(project_dir)
    parametersdir = os.path.join(globaldir, 'parameters', 'import', parameters_folder_name)
    metadatadir = os.path.join(globaldir, 'metadata', 'import', parameters_folder_name)

    # initialize
    if not os.path.exists(metadatadir):
        os.makedirs(metadatadir)
    parameters = toolbox.readjson(os.path.join(globaldir, 'parameters', 'base_parameters', 'parameters.json'))
    cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(email=parameters['cryosparc_username'], password=parameters['cryosparc_password'])
    dealjobs = JobAPIs.DealJobs(cshandle, parameters['project'], parameters['workspace'], parameters['lane'])

    created_jobs_info = []
    import_particles_class = JobAPIs.CreateImportParticleStack(dealjobs)
    import_particles_parameters = toolbox.readjson(os.path.join(parametersdir, 'import_particle_stack_parameters.json'))
    import_particles_job = import_particles_class.QueueImportParticleStackJob(import_particles_parameters)
    created_jobs_info.append(JobAPIs.create_created_jobs_info_item(import_particles_job.uid))
    JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Import Particles job created: ' + import_particles_job.uid)
    toolbox.savetojson(created_jobs_info, os.path.join(metadatadir, 'created_jobs_info.json'), False)
    output_groups = JobAPIs.create_output_groups(particle=[import_particles_job.uid + '_imported_particles'])
    toolbox.savetojson(output_groups, os.path.join(metadatadir, 'output_groups.json'), False)


def import_volume(cryowizardjob, cryowizardlog, project_dir, parameters_folder_name):
    globaldir = os.path.normpath(project_dir)
    parametersdir = os.path.join(globaldir, 'parameters', 'import', parameters_folder_name)
    metadatadir = os.path.join(globaldir, 'metadata', 'import', parameters_folder_name)

    # initialize
    if not os.path.exists(metadatadir):
        os.makedirs(metadatadir)
    parameters = toolbox.readjson(os.path.join(globaldir, 'parameters', 'base_parameters', 'parameters.json'))
    cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(email=parameters['cryosparc_username'], password=parameters['cryosparc_password'])
    dealjobs = JobAPIs.DealJobs(cshandle, parameters['project'], parameters['workspace'], parameters['lane'])

    created_jobs_info = []
    import_volume_class = JobAPIs.CreateImportVolume(dealjobs)
    import_volume_parameters = toolbox.readjson(os.path.join(parametersdir, 'import_volume_parameters.json'))
    import_volume_job = import_volume_class.QueueImportVolumeJob(import_volume_parameters)
    created_jobs_info.append(JobAPIs.create_created_jobs_info_item(import_volume_job.uid))
    JobAPIs.cryowizard_log(cryowizardjob, cryowizardlog, 'Import Volume job created: ' + import_volume_job.uid)
    toolbox.savetojson(created_jobs_info, os.path.join(metadatadir, 'created_jobs_info.json'), False)
    if import_volume_parameters['Type of volume being imported'] in ['map', 'map_sharp', 'map_half_A', 'map_half_B', 'map_locres']:
        output_groups = JobAPIs.create_output_groups(volume=[import_volume_job.uid + '_imported_volume_1'])
        toolbox.savetojson(output_groups, os.path.join(metadatadir, 'output_groups.json'), False)
    elif import_volume_parameters['Type of volume being imported'] in ['mask']:
        output_groups = JobAPIs.create_output_groups(mask=[import_volume_job.uid + '_imported_mask_1'])
        toolbox.savetojson(output_groups, os.path.join(metadatadir, 'output_groups.json'), False)
    else:
        output_groups = JobAPIs.create_output_groups()
        toolbox.savetojson(output_groups, os.path.join(metadatadir, 'output_groups.json'), False)
        JobAPIs.cryowizard_log('Warning: Unsupported input types, output groups would be None')



