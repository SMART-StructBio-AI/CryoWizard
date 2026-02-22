
# (Optional) More Settings


## cryowizard_settings.yml

After installation, a configuration file named `cryowizard_settings.yml` can be found at `path/to/CryoWizard/CryoWizard`. This file defines the global settings for CryoWizard. When creating an individual pipeline, some types of parameters left unspecified will fall back to the default values defined in this file.

    CryoWizard_settings:
    # CryoWizard pipeline settings
        BaseParameters:
        # These parameters will be used to create parameters.json when creating base parameters
            cryosparc_username: null
            # Username to log in CryoSPARC
            cryosparc_password: null
            # Password to log in CryoSPARC
            project: null
            # Which CryoSPARC project you want to create CryoSPARC jobs
            workspace: null
            # Which CryoSPARC workspace you want to create CryoSPARC jobs
            lane: default
            # Which CryoSPARC lane you want to queue CryoSPARC jobs
    
            max_trying_time: 3
            # Maximum number of automatic retries if an individual CryoSPARC job fails to run.
            low_cache_mode: false
            # Set to true to minimize SSD cache usage if CryoSPARC SSD cache space is limited.
            if_slurm: false
            # Set to true to run model inference on Slurm
            inference_gpu_ids: null
            # If model inference (e.g., CryoRanker) is running locally rather than being submitted via Slurm, you can use this parameter to specify which GPUs to use. For example, entering "0,1" will allocate GPU 0 and GPU 1.
            accelerate_port_start: 28000
            accelerate_port_end: 30000
            # The range of ports that CryoWizard automatically searches for available connections when using accelerate for model inference.
    
            abinit_num: 2
            base_abinit_particle_num: 50000
            # abinit_num and base_abinit_particle_num: e.g. if base_abinit_particle_num = 50000 and abinit_num = 2, pipeline will create 2 abinit jobs and use top 50000 and top 100000 particles respectively when using refine block
            refine_grid_num_in_each_turn: [8,4,4]
            # List length means the iteration number, and each number in list means how many refine job will be created in each iteration. Need even number.
            min_refine_score: 0.8
            max_refine_score: 0.1
            min_refine_particle_num: 10000
            max_refine_particle_num: 1500000
            # These four parameters control refine search range when using refine block
    
            orientation_balance: false
            cfar_lower_bound: 0.15
            resolution_lower_bound: 4.0
            # These three parameters would not be used currently
    
        GUI:
            gui_port: 39080
            # CryoWizard GUI server port
            max_thread_num: 64
            # The number of CryoWizard GUI server threads

    CryoSPARC_job_settings:
    # default parameters of CryoSPARC jobs
        ImportMovies:
            ...