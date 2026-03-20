#!/usr/bin/env python

import numpy as np
import os
import time
import shutil
from argparse import ArgumentParser, Namespace

import sys
sys.path.append(os.path.dirname(__file__))

import CryoWizard.cryowizardlib.Toolbox as toolbox



if __name__ == '__main__':
    # get config
    parser = ArgumentParser()

    # get created cryowizard job
    parser.add_argument('--cryowizard_job_uid', default=None, type=str)


    # cryowizard install
    parser.add_argument('--CryoWizardInstall', action="store_true")
    parser.add_argument('--cryosparc_username', default=None, type=str)
    parser.add_argument('--cryosparc_password', default=None, type=str)
    parser.add_argument('--cryosparc_license', default=None, type=str)
    parser.add_argument('--cryosparc_hostname', default=None, type=str)
    parser.add_argument('--cryosparc_port', default=None, type=str)
    parser.add_argument('--cryosparc_lane', default=None, type=str)
    parser.add_argument('--cryoranker_model_weight', default=None, type=str)
    parser.add_argument('--slurm', default=None, type=str)


    # create empty cryowizard job
    parser.add_argument('--CreateCryoWizardJob', action="store_true")
    # parser.add_argument('--cryosparc_username', default=None, type=str)   # repeat parameter
    # parser.add_argument('--cryosparc_password', default=None, type=str)   # repeat parameter
    parser.add_argument('--cryosparc_project', default=None, type=str)
    parser.add_argument('--cryosparc_workspace', default=None, type=str)
    # parser.add_argument('--cryosparc_lane', default=None, type=str)


    # create parameters
    parser.add_argument('--CreateParameterFiles', action="store_true")
    parser.add_argument('--parameter_type', default=None, type=str)


    # modify parameters
    parser.add_argument('--ModifyParameterFiles', action="store_true")
    parser.add_argument('--parameter_folder_name', default=None, type=str)
    ## base parameters
    # parser.add_argument('--cryosparc_username', default=None, type=str)   # repeat parameter
    # parser.add_argument('--cryosparc_password', default=None, type=str)   # repeat parameter
    # parser.add_argument('--cryosparc_project', default=None, type=str)   # repeat parameter
    # parser.add_argument('--cryosparc_workspace', default=None, type=str)   # repeat parameter
    # parser.add_argument('--cryosparc_lane', default=None, type=str)   # repeat parameter
    # parser.add_argument('--slurm', default=None, type=str)
    parser.add_argument('--inference_gpu_ids', default=None, type=str)
    ## source job uid parameters
    parser.add_argument('--source_movie_job_uid', nargs='*', default=None, type=str)
    parser.add_argument('--source_micrograph_job_uid', nargs='*', default=None, type=str)
    parser.add_argument('--source_particle_job_uid', nargs='*', default=None, type=str)
    parser.add_argument('--source_template_job_uid', nargs='*', default=None, type=str)
    parser.add_argument('--source_volume_job_uid', nargs='*', default=None, type=str)
    parser.add_argument('--source_mask_job_uid', nargs='*', default=None, type=str)
    parser.add_argument('--source_cryoranker_job_uid', nargs='*', default=None, type=str)
    ## movie/micrograph/particle parameters
    parser.add_argument('--movies_data_path', default=None, type=str)
    parser.add_argument('--gain_reference_path', default=None, type=str)
    parser.add_argument('--micrographs_data_path', default=None, type=str)
    parser.add_argument('--particles_data_path', default=None, type=str)
    parser.add_argument('--particles_meta_path', default=None, type=str)
    parser.add_argument('--raw_pixel_size', default=None, type=float)
    parser.add_argument('--accelerating_voltage', default=None, type=float)
    parser.add_argument('--spherical_aberration', default=None, type=float)
    parser.add_argument('--total_exposure_dose', default=None, type=float)
    parser.add_argument('--volume_data_path', default=None, type=str)
    parser.add_argument('--volume_emdb_id', default=None, type=int)
    parser.add_argument('--volume_import_type', default=None, type=str)
    parser.add_argument('--volume_pixelsize', default=None, type=float)
    ## preprocess parameters
    parser.add_argument('--symmetry', default=None, type=str)
    parser.add_argument('--particle_diameter', default=None, type=int)
    parser.add_argument('--gpu_num', default=None, type=int)
    parser.add_argument('--ctf_fit_resolution', default=None, type=str)
    ## get top particles parameters
    parser.add_argument('--get_top_particles_num', default=None, type=int)
    parser.add_argument('--get_top_particles_score', default=None, type=float)


    # make custom pipeline
    parser.add_argument('--MakePipeline', action="store_true")


    # make cryowizard input connections
    parser.add_argument('--MakeCryoWizardConnections', action="store_true")


    # create/modify used preset pipeline info
    parser.add_argument('--MakePresetPipelineInfo', action="store_true")
    # parser.add_argument('--preset_pipeline_type', default=None, type=str)


    # run/kill pipeline
    parser.add_argument('--RunPipeline', action="store_true")
    parser.add_argument('--KillPipeline', action="store_true")


    # clear cryowizard all/metadata
    parser.add_argument('--ClearAll', action="store_true")
    parser.add_argument('--ClearMetadata', action="store_true")
    parser.add_argument('--target_data_name', default=None, type=str)


    # create preset pipeline
    parser.add_argument('--CreatePresetPipeline', action="store_true")
    parser.add_argument('--preset_pipeline_type', default=None, type=str)


    # start cryowizard gui
    parser.add_argument('--CryoWizardGUI', action="store_true")
    parser.add_argument('--cryowizard_gui_port', default=None, type=int)


    # regenerate extension.zip
    parser.add_argument('--GenerateExtensionPackege', action="store_true")



    args = parser.parse_args()
    filedir = os.path.normpath(os.path.dirname(__file__))



    if args.CryoWizardInstall:
        print('Start installation...', flush=True)
        import CryoWizard.initialize as initialize
        default_parameters = toolbox.readyaml(os.path.join(filedir, 'CryoWizard', 'cryowizard_settings.yml'))
        initialize.install(
            args.cryosparc_username if (args.cryosparc_username is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_username'],
            args.cryosparc_password if (args.cryosparc_password is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_password'],
            args.cryosparc_license,
            args.cryosparc_hostname,
            args.cryosparc_port,
            args.cryoranker_model_weight,
            args
        )
        print('Installation done', flush=True)

    if args.CreateCryoWizardJob:
        print('Create CryoWizard job...', flush=True)
        import CryoWizard.initialize as initialize
        default_parameters = toolbox.readyaml(os.path.join(filedir, 'CryoWizard', 'cryowizard_settings.yml'))
        new_cryowizard_job_uid = initialize.create_cryowizard_job(
            args.cryosparc_username if (args.cryosparc_username is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_username'],
            args.cryosparc_password if (args.cryosparc_password is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_password'],
            args.cryosparc_project if (args.cryosparc_project is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['project'],
            args.cryosparc_workspace if (args.cryosparc_workspace is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['workspace'],
            args.cryosparc_lane if (args.cryosparc_lane is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['lane']
        )
        print('Create CryoWizard', new_cryowizard_job_uid, 'done', flush=True)

    if args.CreateParameterFiles:
        print('Create parameters...', flush=True)
        import CryoWizard.initialize as initialize
        default_parameters = toolbox.readyaml(os.path.join(filedir, 'CryoWizard', 'cryowizard_settings.yml'))
        if (
                ((args.cryosparc_username is not None) or (default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_username'] is not None)) and
                ((args.cryosparc_password is not None) or (default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_password'] is not None)) and
                ((args.cryosparc_project is not None) or (default_parameters['CryoWizard_settings']['BaseParameters']['project'] is not None)) and
                (args.cryowizard_job_uid is not None) and
                (args.parameter_type in [
                    'base_parameters',
                    'import_movie_file_parameters',
                    'import_micrograph_file_parameters',
                    'import_particle_file_parameters',
                    'import_volume_file_parameters',
                    'preprocess_movie_with_blob_pick_parameters',
                    'preprocess_movie_with_template_pick_parameters',
                    'preprocess_micrograph_with_blob_pick_parameters',
                    'preprocess_micrograph_with_template_pick_parameters',
                    'preprocess_particle_parameters',
                    'create_templates_parameters',
                    'reference_based_auto_select_2d',
                    'junk_detector',
                    'cryoranker_parameters',
                    'get_top_particles',
                    'refine_parameters',
                    'motion_and_ctf_refine_parameters'
                ])
        ):
            # create parameter
            cryowizard_data_dir = initialize.get_cryowizard_job_data_path(
                args.cryosparc_username if (args.cryosparc_username is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_username'],
                args.cryosparc_password if (args.cryosparc_password is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_password'],
                args.cryosparc_project if (args.cryosparc_project is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['project'],
                args.cryowizard_job_uid
            )
            new_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': args.parameter_type})
            print('Create parameters done, new parameter folder name:', os.path.basename(os.path.normpath(new_parameters_folder_path)),  flush=True)
        else:
            print('Create failed', flush=True)

    if args.ModifyParameterFiles:
        print('Modify parameters...', flush=True)
        import CryoWizard.initialize as initialize
        default_parameters = toolbox.readyaml(os.path.join(filedir, 'CryoWizard', 'cryowizard_settings.yml'))
        if (
                ((args.cryosparc_username is not None) or (default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_username'] is not None)) and
                ((args.cryosparc_password is not None) or (default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_password'] is not None)) and
                ((args.cryosparc_project is not None) or (default_parameters['CryoWizard_settings']['BaseParameters']['project'] is not None)) and
                (args.cryowizard_job_uid is not None) and
                (args.parameter_folder_name is not None)
        ):
            cryowizard_data_dir = initialize.get_cryowizard_job_data_path(
                args.cryosparc_username if (args.cryosparc_username is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_username'],
                args.cryosparc_password if (args.cryosparc_password is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_password'],
                args.cryosparc_project if (args.cryosparc_project is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['project'],
                args.cryowizard_job_uid
            )
            initialize.modify_parameters(cryowizard_data_dir, args.parameter_folder_name, args)
            print('Modify parameters done', flush=True)
        else:
            print('Modify parameters failed', flush=True)

    if args.MakePipeline:
        print('Make pipeline...', flush=True)
        import CryoWizard.initialize as initialize
        default_parameters = toolbox.readyaml(os.path.join(filedir, 'CryoWizard', 'cryowizard_settings.yml'))
        if (
                ((args.cryosparc_username is not None) or (default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_username'] is not None)) and
                ((args.cryosparc_password is not None) or (default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_password'] is not None)) and
                ((args.cryosparc_project is not None) or (default_parameters['CryoWizard_settings']['BaseParameters']['project'] is not None)) and
                (args.cryowizard_job_uid is not None)
        ):
            cryowizard_data_dir = initialize.get_cryowizard_job_data_path(
                args.cryosparc_username if (args.cryosparc_username is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_username'],
                args.cryosparc_password if (args.cryosparc_password is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_password'],
                args.cryosparc_project if (args.cryosparc_project is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['project'],
                args.cryowizard_job_uid
            )
            initialize.make_pipeline(cryowizard_data_dir)
            print('Make pipeline done', flush=True)
        else:
            print('Make pipeline failed', flush=True)

    if args.MakeCryoWizardConnections:
        print('Make CryoWizard connections...', flush=True)
        import CryoWizard.initialize as initialize
        default_parameters = toolbox.readyaml(os.path.join(filedir, 'CryoWizard', 'cryowizard_settings.yml'))
        if (
                ((args.cryosparc_username is not None) or (default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_username'] is not None)) and
                ((args.cryosparc_password is not None) or (default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_password'] is not None)) and
                ((args.cryosparc_project is not None) or (default_parameters['CryoWizard_settings']['BaseParameters']['project'] is not None)) and
                (args.cryowizard_job_uid is not None)
        ):
            initialize.make_cryowizard_connections(
                args.cryosparc_username if (args.cryosparc_username is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_username'],
                args.cryosparc_password if (args.cryosparc_password is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_password'],
                args.cryosparc_project if (args.cryosparc_project is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['project'],
                args.cryowizard_job_uid
            )
            print('Make CryoWizard connections done', flush=True)
        else:
            print('Make CryoWizard connections failed', flush=True)

    if args.MakePresetPipelineInfo:
        print('Make Preset Pipeline Info...', flush=True)
        import CryoWizard.initialize as initialize
        default_parameters = toolbox.readyaml(os.path.join(filedir, 'CryoWizard', 'cryowizard_settings.yml'))
        if (
                ((args.cryosparc_username is not None) or (default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_username'] is not None)) and
                ((args.cryosparc_password is not None) or (default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_password'] is not None)) and
                ((args.cryosparc_project is not None) or (default_parameters['CryoWizard_settings']['BaseParameters']['project'] is not None)) and
                (args.cryowizard_job_uid is not None) and
                (args.preset_pipeline_type is not None)
        ):
            cryowizard_data_dir = initialize.get_cryowizard_job_data_path(
                args.cryosparc_username if (args.cryosparc_username is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_username'],
                args.cryosparc_password if (args.cryosparc_password is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_password'],
                args.cryosparc_project if (args.cryosparc_project is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['project'],
                args.cryowizard_job_uid
            )
            initialize.modify_used_preset_pipeline_info(cryowizard_data_dir, args.preset_pipeline_type, args)
            print('Make preset pipeline info done', flush=True)
        else:
            print('Make preset pipeline info failed', flush=True)

    if args.RunPipeline:
        import CryoWizard.run as run
        default_parameters = toolbox.readyaml(os.path.join(filedir, 'CryoWizard', 'cryowizard_settings.yml'))
        if (
                ((args.cryosparc_username is not None) or (default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_username'] is not None)) and
                ((args.cryosparc_password is not None) or (default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_password'] is not None)) and
                ((args.cryosparc_project is not None) or (default_parameters['CryoWizard_settings']['BaseParameters']['project'] is not None)) and
                (args.cryowizard_job_uid is not None)
        ):
            run.cryowizard_run(
                args.cryosparc_username if (args.cryosparc_username is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_username'],
                args.cryosparc_password if (args.cryosparc_password is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_password'],
                args.cryosparc_project if (args.cryosparc_project is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['project'],
                args.cryowizard_job_uid
            )

    if args.KillPipeline:
        import CryoWizard.run as run
        default_parameters = toolbox.readyaml(os.path.join(filedir, 'CryoWizard', 'cryowizard_settings.yml'))
        if (
                ((args.cryosparc_username is not None) or (default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_username'] is not None)) and
                ((args.cryosparc_password is not None) or (default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_password'] is not None)) and
                ((args.cryosparc_project is not None) or (default_parameters['CryoWizard_settings']['BaseParameters']['project'] is not None)) and
                (args.cryowizard_job_uid is not None)
        ):
            run.cryowizard_kill(
                args.cryosparc_username if (args.cryosparc_username is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_username'],
                args.cryosparc_password if (args.cryosparc_password is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_password'],
                args.cryosparc_project if (args.cryosparc_project is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['project'],
                args.cryowizard_job_uid
            )

    if args.ClearAll:
        print('Clear CryoWizard files...', flush=True)
        import CryoWizard.initialize as initialize
        default_parameters = toolbox.readyaml(os.path.join(filedir, 'CryoWizard', 'cryowizard_settings.yml'))
        if (
                ((args.cryosparc_username is not None) or (default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_username'] is not None)) and
                ((args.cryosparc_password is not None) or (default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_password'] is not None)) and
                ((args.cryosparc_project is not None) or (default_parameters['CryoWizard_settings']['BaseParameters']['project'] is not None)) and
                (args.cryowizard_job_uid is not None)
        ):
            cryowizard_data_dir = initialize.get_cryowizard_job_data_path(
                args.cryosparc_username if (args.cryosparc_username is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_username'],
                args.cryosparc_password if (args.cryosparc_password is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_password'],
                args.cryosparc_project if (args.cryosparc_project is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['project'],
                args.cryowizard_job_uid
            )
            if args.target_data_name is not None:
                if args.target_data_name in ['base_parameters']:
                    if os.path.exists(os.path.join(cryowizard_data_dir, 'parameters', args.target_data_name)):
                        shutil.rmtree(os.path.join(cryowizard_data_dir, 'parameters', args.target_data_name))
                    if os.path.exists(os.path.join(cryowizard_data_dir, 'metadata', args.target_data_name)):
                        shutil.rmtree(os.path.join(cryowizard_data_dir, 'metadata', args.target_data_name))
                elif args.target_data_name.split('_')[0] in ['import', 'preprocess', 'cryoranker', 'refine', 'postprocess']:
                    if os.path.exists(os.path.join(cryowizard_data_dir, 'parameters', args.target_data_name.split('_')[0], args.target_data_name)):
                        shutil.rmtree(os.path.join(cryowizard_data_dir, 'parameters', args.target_data_name.split('_')[0], args.target_data_name))
                    if os.path.exists(os.path.join(cryowizard_data_dir, 'metadata', args.target_data_name.split('_')[0], args.target_data_name)):
                        shutil.rmtree(os.path.join(cryowizard_data_dir, 'metadata', args.target_data_name.split('_')[0], args.target_data_name))
                else:
                    print('Illegal target_data_name, clearing fail', flush=True)
            else:
                if os.path.exists(os.path.join(cryowizard_data_dir, 'parameters')):
                    shutil.rmtree(os.path.join(cryowizard_data_dir, 'parameters'))
                if os.path.exists(os.path.join(cryowizard_data_dir, 'metadata')):
                    shutil.rmtree(os.path.join(cryowizard_data_dir, 'metadata'))
            print('Clear CryoWizard files done', flush=True)
        else:
            print('Clear CryoWizard files failed', flush=True)

    if args.ClearMetadata:
        print('Clear CryoWizard metadata files...', flush=True)
        import CryoWizard.initialize as initialize
        default_parameters = toolbox.readyaml(os.path.join(filedir, 'CryoWizard', 'cryowizard_settings.yml'))
        if (
                ((args.cryosparc_username is not None) or (default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_username'] is not None)) and
                ((args.cryosparc_password is not None) or (default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_password'] is not None)) and
                ((args.cryosparc_project is not None) or (default_parameters['CryoWizard_settings']['BaseParameters']['project'] is not None)) and
                (args.cryowizard_job_uid is not None)
        ):
            cryowizard_data_dir = initialize.get_cryowizard_job_data_path(
                args.cryosparc_username if (args.cryosparc_username is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_username'],
                args.cryosparc_password if (args.cryosparc_password is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_password'],
                args.cryosparc_project if (args.cryosparc_project is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['project'],
                args.cryowizard_job_uid
            )
            if args.target_data_name is not None:
                if args.target_data_name in ['base_parameters']:
                    if os.path.exists(os.path.join(cryowizard_data_dir, 'metadata', args.target_data_name)):
                        shutil.rmtree(os.path.join(cryowizard_data_dir, 'metadata', args.target_data_name))
                elif args.target_data_name.split('_')[0] in ['import', 'preprocess', 'cryoranker', 'refine', 'postprocess']:
                    if os.path.exists(os.path.join(cryowizard_data_dir, 'metadata', args.target_data_name.split('_')[0], args.target_data_name)):
                        shutil.rmtree(os.path.join(cryowizard_data_dir, 'metadata', args.target_data_name.split('_')[0], args.target_data_name))
                else:
                    print('Illegal target_data_name, clearing fail', flush=True)
            else:
                if os.path.exists(os.path.join(cryowizard_data_dir, 'metadata')):
                    shutil.rmtree(os.path.join(cryowizard_data_dir, 'metadata'))
            print('Clear CryoWizard metadata files done', flush=True)
        else:
            print('Clear CryoWizard metadata files failed', flush=True)

    if args.CreatePresetPipeline:
        print('Creating preset pipeline...', flush=True)
        def include_args_keys(source_parser, source_args, include_keys_dict):
            subset_args_dict = {}
            source_args_dict = toolbox.args2dict(source_args)
            for key in source_args_dict.keys():
                if key in include_keys_dict:
                    subset_args_dict[key] = include_keys_dict[key]
                else:
                    subset_args_dict[key] = source_parser.get_default(key)
            subset_args = toolbox.dict2args(subset_args_dict)
            return subset_args
        def exclude_args_keys(source_parser, source_args, exclude_keys_list):
            subset_args_dict = {}
            source_args_dict = toolbox.args2dict(source_args)
            for key in source_args_dict.keys():
                if key not in exclude_keys_list:
                    subset_args_dict[key] = source_args_dict[key]
                else:
                    subset_args_dict[key] = source_parser.get_default(key)
            subset_args = toolbox.dict2args(subset_args_dict)
            return subset_args
        import CryoWizard.initialize as initialize
        import CryoWizard.cryowizardlib.CSLogin as CSLogin
        default_parameters = toolbox.readyaml(os.path.join(filedir, 'CryoWizard', 'cryowizard_settings.yml'))
        if (
                ((args.cryosparc_username is not None) or (default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_username'] is not None)) and
                ((args.cryosparc_password is not None) or (default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_password'] is not None)) and
                ((args.cryosparc_project is not None) or (default_parameters['CryoWizard_settings']['BaseParameters']['project'] is not None)) and
                (args.cryowizard_job_uid is not None) and
                (args.preset_pipeline_type is not None)
        ):
            cryowizard_data_dir = initialize.get_cryowizard_job_data_path(
                args.cryosparc_username if (args.cryosparc_username is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_username'],
                args.cryosparc_password if (args.cryosparc_password is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_password'],
                args.cryosparc_project if (args.cryosparc_project is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['project'],
                args.cryowizard_job_uid
            )

            if not os.path.exists(os.path.join(cryowizard_data_dir, 'parameters', 'base_parameters', 'cryowizard_preset_pipeline_info.json')):
                new_base_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'base_parameters'})
            else:
                new_base_parameters_folder_path = os.path.join(cryowizard_data_dir, 'parameters', 'base_parameters')

            if os.path.exists(os.path.join(cryowizard_data_dir, 'parameters', 'import')):
                shutil.rmtree(os.path.join(cryowizard_data_dir, 'parameters', 'import'))
            if os.path.exists(os.path.join(cryowizard_data_dir, 'metadata', 'import')):
                shutil.rmtree(os.path.join(cryowizard_data_dir, 'metadata', 'import'))
            if os.path.exists(os.path.join(cryowizard_data_dir, 'parameters', 'preprocess')):
                shutil.rmtree(os.path.join(cryowizard_data_dir, 'parameters', 'preprocess'))
            if os.path.exists(os.path.join(cryowizard_data_dir, 'metadata', 'preprocess')):
                shutil.rmtree(os.path.join(cryowizard_data_dir, 'metadata', 'preprocess'))
            if os.path.exists(os.path.join(cryowizard_data_dir, 'parameters', 'cryoranker')):
                shutil.rmtree(os.path.join(cryowizard_data_dir, 'parameters', 'cryoranker'))
            if os.path.exists(os.path.join(cryowizard_data_dir, 'metadata', 'cryoranker')):
                shutil.rmtree(os.path.join(cryowizard_data_dir, 'metadata', 'cryoranker'))
            if os.path.exists(os.path.join(cryowizard_data_dir, 'parameters', 'refine')):
                shutil.rmtree(os.path.join(cryowizard_data_dir, 'parameters', 'refine'))
            if os.path.exists(os.path.join(cryowizard_data_dir, 'metadata', 'refine')):
                shutil.rmtree(os.path.join(cryowizard_data_dir, 'metadata', 'refine'))
            if os.path.exists(os.path.join(cryowizard_data_dir, 'parameters', 'postprocess')):
                shutil.rmtree(os.path.join(cryowizard_data_dir, 'parameters', 'postprocess'))
            if os.path.exists(os.path.join(cryowizard_data_dir, 'metadata', 'postprocess')):
                shutil.rmtree(os.path.join(cryowizard_data_dir, 'metadata', 'postprocess'))

            cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(
                email=args.cryosparc_username if (args.cryosparc_username is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_username'],
                password=args.cryosparc_password if (args.cryosparc_password is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_password']
            )

            cryowizard_job = cshandle.find_external_job(args.cryosparc_project if (args.cryosparc_project is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['project'], args.cryowizard_job_uid)
            while True:
                if (cryowizard_job.status == 'building'):
                    break
                if cryowizard_job.status in ['launched', 'started', 'running', 'waiting']:
                    try:
                        cryowizard_job.kill()
                    except:
                        pass
                try:
                    cryowizard_job.clear()
                    cryowizard_job.wait_for_status('building', 5)
                    if (cryowizard_job.status == 'building'):
                        break
                except:
                    pass
                time.sleep(1)


            if (args.preset_pipeline_type == 'default'):
                if args.movies_data_path is not None:
                    new_import_movie_files_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'import_movie_file_parameters'})
                else:
                    new_import_movie_files_parameters_folder_path = None
                if args.micrographs_data_path is not None:
                    new_import_micrograph_files_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'import_micrograph_file_parameters'})
                else:
                    new_import_micrograph_files_parameters_folder_path = None
                if (args.particles_data_path is not None) or (args.particles_meta_path is not None):
                    new_import_particle_files_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'import_particle_file_parameters'})
                else:
                    new_import_particle_files_parameters_folder_path = None

                source_movie_jobs = []
                source_micrograph_jobs = []
                source_particle_jobs = []
                if args.source_movie_job_uid is not None:
                    source_movie_jobs += args.source_movie_job_uid
                if args.source_micrograph_job_uid is not None:
                    source_micrograph_jobs += args.source_micrograph_job_uid
                if args.source_particle_job_uid is not None:
                    source_particle_jobs += args.source_particle_job_uid
                if new_import_movie_files_parameters_folder_path is not None:
                    source_movie_jobs.append(os.path.basename(os.path.normpath(new_import_movie_files_parameters_folder_path)))
                if new_import_micrograph_files_parameters_folder_path is not None:
                    source_micrograph_jobs.append(os.path.basename(os.path.normpath(new_import_micrograph_files_parameters_folder_path)))
                if new_import_particle_files_parameters_folder_path is not None:
                    source_particle_jobs.append(os.path.basename(os.path.normpath(new_import_particle_files_parameters_folder_path)))

                if (len(source_movie_jobs) == 0) and (len(source_micrograph_jobs) == 0) and (len(source_particle_jobs) == 0):
                    print('No input found, exiting...', flush=True)
                if (len(source_movie_jobs) == 0) and (len(source_micrograph_jobs) == 0) and (len(source_particle_jobs) > 0):
                    new_preprocess_0_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'preprocess_particle_parameters'})
                    new_cryoranker_0_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'cryoranker_parameters'})
                    new_refine_0_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'refine_parameters'})
                    new_postprocess_0_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'motion_and_ctf_refine_parameters'})
                    # inputs
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_preprocess_0_parameters_folder_path)), include_args_keys(parser, args, {'source_particle_job_uid': source_particle_jobs}))
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_cryoranker_0_parameters_folder_path)), include_args_keys(parser, args, {'source_particle_job_uid': [os.path.basename(os.path.normpath(new_preprocess_0_parameters_folder_path))]}))
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_refine_0_parameters_folder_path)), include_args_keys(parser, args, {'source_cryoranker_job_uid': [os.path.basename(os.path.normpath(new_cryoranker_0_parameters_folder_path))]}))
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_postprocess_0_parameters_folder_path)), include_args_keys(parser, args, {'source_particle_job_uid': [os.path.basename(os.path.normpath(new_refine_0_parameters_folder_path))], 'source_volume_job_uid': [os.path.basename(os.path.normpath(new_refine_0_parameters_folder_path))], 'source_mask_job_uid': [os.path.basename(os.path.normpath(new_refine_0_parameters_folder_path))]}))
                    # other parameters
                    if new_import_particle_files_parameters_folder_path is not None:
                        initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_import_particle_files_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_base_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_preprocess_0_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_cryoranker_0_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_refine_0_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_postprocess_0_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                else:
                    preprocessed_micrographs_list = []
                    preprocessed_particles_list = []
                    new_preprocess_create_templates_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'create_templates_parameters'})
                    new_preprocess_template_pick_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'preprocess_micrograph_with_template_pick_parameters'})
                    if (len(source_movie_jobs) > 0):
                        new_preprocess_movie_0_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'preprocess_movie_with_blob_pick_parameters'})
                        preprocessed_micrographs_list.append(os.path.basename(os.path.normpath(new_preprocess_movie_0_parameters_folder_path)))
                        preprocessed_particles_list.append(os.path.basename(os.path.normpath(new_preprocess_movie_0_parameters_folder_path)))
                    else:
                        new_preprocess_movie_0_parameters_folder_path = None
                    if (len(source_micrograph_jobs) > 0):
                        new_preprocess_micrograph_0_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'preprocess_micrograph_with_blob_pick_parameters'})
                        preprocessed_micrographs_list.append(os.path.basename(os.path.normpath(new_preprocess_micrograph_0_parameters_folder_path)))
                        preprocessed_particles_list.append(os.path.basename(os.path.normpath(new_preprocess_micrograph_0_parameters_folder_path)))
                    else:
                        new_preprocess_micrograph_0_parameters_folder_path = None
                    if (len(source_particle_jobs) > 0):
                        new_preprocess_particle_0_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'preprocess_particle_parameters'})
                        preprocessed_particles_list.append(os.path.basename(os.path.normpath(new_preprocess_particle_0_parameters_folder_path)))
                    else:
                        new_preprocess_particle_0_parameters_folder_path = None
                    new_cryoranker_0_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'cryoranker_parameters'})
                    new_refine_0_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'refine_parameters'})
                    new_cryoranker_1_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'cryoranker_parameters'})
                    new_refine_1_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'refine_parameters'})
                    new_postprocess_0_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'motion_and_ctf_refine_parameters'})
                    # inputs
                    if new_preprocess_movie_0_parameters_folder_path is not None:
                        initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_preprocess_movie_0_parameters_folder_path)), include_args_keys(parser, args, {'source_movie_job_uid': source_movie_jobs}))
                    if new_preprocess_micrograph_0_parameters_folder_path is not None:
                        initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_preprocess_micrograph_0_parameters_folder_path)), include_args_keys(parser, args, {'source_micrograph_job_uid': source_micrograph_jobs}))
                    if new_preprocess_particle_0_parameters_folder_path is not None:
                        initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_preprocess_particle_0_parameters_folder_path)), include_args_keys(parser, args, {'source_particle_job_uid': source_particle_jobs}))
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_cryoranker_0_parameters_folder_path)), include_args_keys(parser, args, {'source_particle_job_uid': preprocessed_particles_list}))
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_refine_0_parameters_folder_path)), include_args_keys(parser, args, {'source_cryoranker_job_uid': [os.path.basename(os.path.normpath(new_cryoranker_0_parameters_folder_path))]}))
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_preprocess_create_templates_parameters_folder_path)), include_args_keys(parser, args, {'source_volume_job_uid': [os.path.basename(os.path.normpath(new_refine_0_parameters_folder_path))]}))
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_preprocess_template_pick_parameters_folder_path)), include_args_keys(parser, args, {'source_micrograph_job_uid': preprocessed_micrographs_list, 'source_template_job_uid': [os.path.basename(os.path.normpath(new_preprocess_create_templates_parameters_folder_path))]}))
                    if new_preprocess_particle_0_parameters_folder_path is not None:
                        initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_cryoranker_1_parameters_folder_path)), include_args_keys(parser, args, {'source_particle_job_uid': [os.path.basename(os.path.normpath(new_preprocess_template_pick_parameters_folder_path)), os.path.basename(os.path.normpath(new_preprocess_particle_0_parameters_folder_path))]}))
                    else:
                        initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_cryoranker_1_parameters_folder_path)), include_args_keys(parser, args, {'source_particle_job_uid': [os.path.basename(os.path.normpath(new_preprocess_template_pick_parameters_folder_path))]}))
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_refine_1_parameters_folder_path)), include_args_keys(parser, args, {'source_cryoranker_job_uid': [os.path.basename(os.path.normpath(new_cryoranker_1_parameters_folder_path))]}))
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_postprocess_0_parameters_folder_path)), include_args_keys(parser, args, {'source_particle_job_uid': [os.path.basename(os.path.normpath(new_refine_1_parameters_folder_path))], 'source_volume_job_uid': [os.path.basename(os.path.normpath(new_refine_1_parameters_folder_path))], 'source_mask_job_uid': [os.path.basename(os.path.normpath(new_refine_1_parameters_folder_path))]}))
                    # other parameters
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_base_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    if new_import_movie_files_parameters_folder_path is not None:
                        initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_import_movie_files_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    if new_import_micrograph_files_parameters_folder_path is not None:
                        initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_import_micrograph_files_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    if new_import_particle_files_parameters_folder_path is not None:
                        initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_import_particle_files_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    if new_preprocess_movie_0_parameters_folder_path is not None:
                        initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_preprocess_movie_0_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    if new_preprocess_micrograph_0_parameters_folder_path is not None:
                        initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_preprocess_micrograph_0_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    if new_preprocess_particle_0_parameters_folder_path is not None:
                        initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_preprocess_particle_0_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_cryoranker_0_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_refine_0_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_preprocess_create_templates_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_preprocess_template_pick_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    if (
                            (new_preprocess_movie_0_parameters_folder_path is not None) and
                            (args.particle_diameter is not None) and
                            (args.raw_pixel_size is not None) and
                            ((1.0 - args.raw_pixel_size) > np.fabs(1.0 - 2.0 * args.raw_pixel_size))
                    ):
                        initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_preprocess_template_pick_parameters_folder_path)), include_args_keys(parser, args, {'particle_diameter': args.particle_diameter, 'raw_pixel_size': args.raw_pixel_size * 2.0}))
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_cryoranker_1_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_refine_1_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_postprocess_0_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                initialize.modify_used_preset_pipeline_info(cryowizard_data_dir, args.preset_pipeline_type, args)
                initialize.make_pipeline(cryowizard_data_dir)
                initialize.make_cryowizard_connections(
                    args.cryosparc_username if (args.cryosparc_username is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_username'],
                    args.cryosparc_password if (args.cryosparc_password is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_password'],
                    args.cryosparc_project if (args.cryosparc_project is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['project'],
                    args.cryowizard_job_uid
                )
            elif (args.preset_pipeline_type == 'simpler'):
                if args.movies_data_path is not None:
                    new_import_movie_files_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'import_movie_file_parameters'})
                else:
                    new_import_movie_files_parameters_folder_path = None
                if args.micrographs_data_path is not None:
                    new_import_micrograph_files_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'import_micrograph_file_parameters'})
                else:
                    new_import_micrograph_files_parameters_folder_path = None
                if (args.particles_data_path is not None) or (args.particles_meta_path is not None):
                    new_import_particle_files_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'import_particle_file_parameters'})
                else:
                    new_import_particle_files_parameters_folder_path = None

                source_movie_jobs = []
                source_micrograph_jobs = []
                source_particle_jobs = []
                if args.source_movie_job_uid is not None:
                    source_movie_jobs += args.source_movie_job_uid
                if args.source_micrograph_job_uid is not None:
                    source_micrograph_jobs += args.source_micrograph_job_uid
                if args.source_particle_job_uid is not None:
                    source_particle_jobs += args.source_particle_job_uid
                if new_import_movie_files_parameters_folder_path is not None:
                    source_movie_jobs.append(os.path.basename(os.path.normpath(new_import_movie_files_parameters_folder_path)))
                if new_import_micrograph_files_parameters_folder_path is not None:
                    source_micrograph_jobs.append(os.path.basename(os.path.normpath(new_import_micrograph_files_parameters_folder_path)))
                if new_import_particle_files_parameters_folder_path is not None:
                    source_particle_jobs.append(os.path.basename(os.path.normpath(new_import_particle_files_parameters_folder_path)))

                if (len(source_movie_jobs) == 0) and (len(source_micrograph_jobs) == 0) and (len(source_particle_jobs) == 0):
                    print('No input found, exiting...', flush=True)
                else:
                    preprocessed_particles_list = []
                    if (len(source_movie_jobs) > 0):
                        new_preprocess_movie_0_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'preprocess_movie_with_blob_pick_parameters'})
                        preprocessed_particles_list.append(os.path.basename(os.path.normpath(new_preprocess_movie_0_parameters_folder_path)))
                    else:
                        new_preprocess_movie_0_parameters_folder_path = None
                    if (len(source_micrograph_jobs) > 0):
                        new_preprocess_micrograph_0_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'preprocess_micrograph_with_blob_pick_parameters'})
                        preprocessed_particles_list.append(os.path.basename(os.path.normpath(new_preprocess_micrograph_0_parameters_folder_path)))
                    else:
                        new_preprocess_micrograph_0_parameters_folder_path = None
                    if (len(source_particle_jobs) > 0):
                        new_preprocess_particle_0_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'preprocess_particle_parameters'})
                        preprocessed_particles_list.append(os.path.basename(os.path.normpath(new_preprocess_particle_0_parameters_folder_path)))
                    else:
                        new_preprocess_particle_0_parameters_folder_path = None
                    new_cryoranker_0_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'cryoranker_parameters'})
                    new_refine_0_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'refine_parameters'})
                    new_postprocess_0_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'motion_and_ctf_refine_parameters'})
                    # inputs
                    if new_preprocess_movie_0_parameters_folder_path is not None:
                        initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_preprocess_movie_0_parameters_folder_path)), include_args_keys(parser, args, {'source_movie_job_uid': source_movie_jobs}))
                    if new_preprocess_micrograph_0_parameters_folder_path is not None:
                        initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_preprocess_micrograph_0_parameters_folder_path)), include_args_keys(parser, args, {'source_micrograph_job_uid': source_micrograph_jobs}))
                    if new_preprocess_particle_0_parameters_folder_path is not None:
                        initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_preprocess_particle_0_parameters_folder_path)), include_args_keys(parser, args, {'source_particle_job_uid': source_particle_jobs}))
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_cryoranker_0_parameters_folder_path)), include_args_keys(parser, args, {'source_particle_job_uid': preprocessed_particles_list}))
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_refine_0_parameters_folder_path)), include_args_keys(parser, args, {'source_cryoranker_job_uid': [os.path.basename(os.path.normpath(new_cryoranker_0_parameters_folder_path))]}))
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_postprocess_0_parameters_folder_path)), include_args_keys(parser, args, {'source_particle_job_uid': [os.path.basename(os.path.normpath(new_refine_0_parameters_folder_path))], 'source_volume_job_uid': [os.path.basename(os.path.normpath(new_refine_0_parameters_folder_path))], 'source_mask_job_uid': [os.path.basename(os.path.normpath(new_refine_0_parameters_folder_path))]}))
                    # other parameters
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_base_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    if new_import_movie_files_parameters_folder_path is not None:
                        initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_import_movie_files_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    if new_import_micrograph_files_parameters_folder_path is not None:
                        initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_import_micrograph_files_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    if new_import_particle_files_parameters_folder_path is not None:
                        initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_import_particle_files_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    if new_preprocess_movie_0_parameters_folder_path is not None:
                        initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_preprocess_movie_0_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    if new_preprocess_micrograph_0_parameters_folder_path is not None:
                        initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_preprocess_micrograph_0_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    if new_preprocess_particle_0_parameters_folder_path is not None:
                        initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_preprocess_particle_0_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_cryoranker_0_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_refine_0_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_postprocess_0_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                initialize.modify_used_preset_pipeline_info(cryowizard_data_dir, args.preset_pipeline_type, args)
                initialize.make_pipeline(cryowizard_data_dir)
                initialize.make_cryowizard_connections(
                    args.cryosparc_username if (args.cryosparc_username is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_username'],
                    args.cryosparc_password if (args.cryosparc_password is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_password'],
                    args.cryosparc_project if (args.cryosparc_project is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['project'],
                    args.cryowizard_job_uid
                )
            elif (args.preset_pipeline_type == 'cryoranker_only'):
                if args.movies_data_path is not None:
                    new_import_movie_files_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'import_movie_file_parameters'})
                else:
                    new_import_movie_files_parameters_folder_path = None
                if args.micrographs_data_path is not None:
                    new_import_micrograph_files_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'import_micrograph_file_parameters'})
                else:
                    new_import_micrograph_files_parameters_folder_path = None
                if (args.particles_data_path is not None) or (args.particles_meta_path is not None):
                    new_import_particle_files_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'import_particle_file_parameters'})
                else:
                    new_import_particle_files_parameters_folder_path = None

                source_movie_jobs = []
                source_micrograph_jobs = []
                source_particle_jobs = []
                if args.source_movie_job_uid is not None:
                    source_movie_jobs += args.source_movie_job_uid
                if args.source_micrograph_job_uid is not None:
                    source_micrograph_jobs += args.source_micrograph_job_uid
                if args.source_particle_job_uid is not None:
                    source_particle_jobs += args.source_particle_job_uid
                if new_import_movie_files_parameters_folder_path is not None:
                    source_movie_jobs.append(os.path.basename(os.path.normpath(new_import_movie_files_parameters_folder_path)))
                if new_import_micrograph_files_parameters_folder_path is not None:
                    source_micrograph_jobs.append(os.path.basename(os.path.normpath(new_import_micrograph_files_parameters_folder_path)))
                if new_import_particle_files_parameters_folder_path is not None:
                    source_particle_jobs.append(os.path.basename(os.path.normpath(new_import_particle_files_parameters_folder_path)))

                if (len(source_movie_jobs) == 0) and (len(source_micrograph_jobs) == 0) and (len(source_particle_jobs) == 0):
                    print('No input found, exiting...', flush=True)
                else:
                    preprocessed_particles_list = []
                    if (len(source_movie_jobs) > 0):
                        new_preprocess_movie_0_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'preprocess_movie_with_blob_pick_parameters'})
                        preprocessed_particles_list.append(os.path.basename(os.path.normpath(new_preprocess_movie_0_parameters_folder_path)))
                    else:
                        new_preprocess_movie_0_parameters_folder_path = None
                    if (len(source_micrograph_jobs) > 0):
                        new_preprocess_micrograph_0_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'preprocess_micrograph_with_blob_pick_parameters'})
                        preprocessed_particles_list.append(os.path.basename(os.path.normpath(new_preprocess_micrograph_0_parameters_folder_path)))
                    else:
                        new_preprocess_micrograph_0_parameters_folder_path = None
                    if (len(source_particle_jobs) > 0):
                        new_preprocess_particle_0_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'preprocess_particle_parameters'})
                        preprocessed_particles_list.append(os.path.basename(os.path.normpath(new_preprocess_particle_0_parameters_folder_path)))
                    else:
                        new_preprocess_particle_0_parameters_folder_path = None
                    new_cryoranker_0_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'cryoranker_parameters'})
                    # inputs
                    if new_preprocess_movie_0_parameters_folder_path is not None:
                        initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_preprocess_movie_0_parameters_folder_path)), include_args_keys(parser, args, {'source_movie_job_uid': source_movie_jobs}))
                    if new_preprocess_micrograph_0_parameters_folder_path is not None:
                        initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_preprocess_micrograph_0_parameters_folder_path)), include_args_keys(parser, args, {'source_micrograph_job_uid': source_micrograph_jobs}))
                    if new_preprocess_particle_0_parameters_folder_path is not None:
                        initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_preprocess_particle_0_parameters_folder_path)), include_args_keys(parser, args, {'source_particle_job_uid': source_particle_jobs}))
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_cryoranker_0_parameters_folder_path)), include_args_keys(parser, args, {'source_particle_job_uid': preprocessed_particles_list}))
                    # other parameters
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_base_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    if new_import_movie_files_parameters_folder_path is not None:
                        initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_import_movie_files_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    if new_import_micrograph_files_parameters_folder_path is not None:
                        initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_import_micrograph_files_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    if new_import_particle_files_parameters_folder_path is not None:
                        initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_import_particle_files_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    if new_preprocess_movie_0_parameters_folder_path is not None:
                        initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_preprocess_movie_0_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    if new_preprocess_micrograph_0_parameters_folder_path is not None:
                        initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_preprocess_micrograph_0_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    if new_preprocess_particle_0_parameters_folder_path is not None:
                        initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_preprocess_particle_0_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_cryoranker_0_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                initialize.modify_used_preset_pipeline_info(cryowizard_data_dir, args.preset_pipeline_type, args)
                initialize.make_pipeline(cryowizard_data_dir)
                initialize.make_cryowizard_connections(
                    args.cryosparc_username if (args.cryosparc_username is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_username'],
                    args.cryosparc_password if (args.cryosparc_password is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_password'],
                    args.cryosparc_project if (args.cryosparc_project is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['project'],
                    args.cryowizard_job_uid
                )
            elif (args.preset_pipeline_type == 'cryoranker_get_top_particles'):
                if args.source_cryoranker_job_uid is None:
                    print('No input found, exiting...', flush=True)
                else:
                    new_get_top_particles_parameters_folder_path = initialize.create_parameters(cryowizard_data_dir, {'type': 'get_top_particles'})
                    # inputs
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_get_top_particles_parameters_folder_path)), include_args_keys(parser, args, {'source_cryoranker_job_uid': args.source_cryoranker_job_uid}))
                    # other parameters
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_base_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                    initialize.modify_parameters(cryowizard_data_dir, os.path.basename(os.path.normpath(new_get_top_particles_parameters_folder_path)), exclude_args_keys(parser, args, ['source_movie_job_uid', 'source_micrograph_job_uid', 'source_particle_job_uid', 'source_template_job_uid', 'source_volume_job_uid', 'source_mask_job_uid', 'source_cryoranker_job_uid']))
                initialize.modify_used_preset_pipeline_info(cryowizard_data_dir, args.preset_pipeline_type, args)
                initialize.make_pipeline(cryowizard_data_dir)
                initialize.make_cryowizard_connections(
                    args.cryosparc_username if (args.cryosparc_username is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_username'],
                    args.cryosparc_password if (args.cryosparc_password is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['cryosparc_password'],
                    args.cryosparc_project if (args.cryosparc_project is not None) else default_parameters['CryoWizard_settings']['BaseParameters']['project'],
                    args.cryowizard_job_uid
                )
            else:
                print('preset_pipeline_type parameter wrong, no pipeline would be created', flush=True)
            print('Create preset pipeline done', flush=True)
        else:
            print('Create preset pipeline failed', flush=True)

    if args.CryoWizardGUI:
        import CryoWizard.cryowizardgui.cryowizard_gui_server as cryowizard_gui_server
        cryowizard_gui_server.startup_gui(args.cryowizard_gui_port)

    if args.GenerateExtensionPackege:
        if os.path.exists(os.path.join(filedir, 'extension.zip')):
            os.remove(os.path.join(filedir, 'extension.zip'))
        toolbox.packtozip(os.path.join(filedir, 'CryoWizard', 'cryowizardgui', 'extension'), False, True)
        shutil.move(os.path.join(filedir, 'CryoWizard', 'cryowizardgui', 'extension.zip'), os.path.join(filedir, 'extension.zip'))












