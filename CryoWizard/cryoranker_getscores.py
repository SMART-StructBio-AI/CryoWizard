#!/usr/bin/env python

import numpy as np
import cryosparc.dataset as csd
import datetime
import shutil
import os

from accelerate import Accelerator
from accelerate.utils import InitProcessGroupKwargs
from datetime import timedelta

import sys
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import CryoRanker.CryoRanker_inference as CryoRanker_inference
import cryowizardlib.CSLogin as CSLogin
import cryowizardlib.JobAPIs as JobAPIs
import cryowizardlib.Toolbox as toolbox



accelerator = Accelerator(kwargs_handlers=[InitProcessGroupKwargs(timeout=timedelta(seconds=96000))])

if accelerator.is_main_process:
    wholetimebegin = datetime.datetime.now()

# initial
cryorankerdir = os.path.normpath(os.getcwd())
globaldir = os.path.dirname(os.path.dirname(os.path.dirname(cryorankerdir)))
parameters = toolbox.readjson(os.path.join(globaldir, 'parameters', 'base_parameters', 'parameters.json'))
if_initial_orientation_balance = True
cshandle = CSLogin.cshandleclass.GetCryoSPARCHandle(email=parameters['cryosparc_username'], password=parameters['cryosparc_password'])
dealjobs = JobAPIs.DealJobs(cshandle, parameters['project'], parameters['workspace'], parameters['lane'])
model_cache_file_path = os.path.join(cryorankerdir, 'model_cache')
if accelerator.is_main_process:
    if os.path.exists(model_cache_file_path):
        shutil.rmtree(model_cache_file_path)
    os.makedirs(model_cache_file_path)

source_particle_job = toolbox.readjson(os.path.join(cryorankerdir, 'created_jobs_info.json'))[0]['jobuid']
restack_cs = csd.Dataset.load(os.path.join(dealjobs.GetProjectPath(), source_particle_job, 'restacked_particles.cs'))
passthrough_cs = csd.Dataset.load(os.path.join(dealjobs.GetProjectPath(), source_particle_job, source_particle_job + '_passthrough_particles.cs'))
source_particles_cs = csd.Dataset.innerjoin(restack_cs, passthrough_cs)

accelerator.print('Getting scores by model...', flush=True)
if accelerator.is_main_process:
    print(os.path.join(dealjobs.GetProjectPath(), source_particle_job), flush=True)
new_particles_cs, scores, features_all = CryoRanker_inference.cryoRanker_main(job_path=(os.path.join(dealjobs.GetProjectPath(), source_particle_job) + '/'), cache_file_path=model_cache_file_path, accelerator=accelerator, use_features=if_initial_orientation_balance, features_max_num=len(source_particles_cs))

if accelerator.is_main_process:
    if not (len(source_particles_cs) == len(new_particles_cs)):
        accelerator.print('Error! Source csfile length does not match new csfile...', flush=True)
        exit()
    if not (len(scores) == len(new_particles_cs)):
        accelerator.print('Error! Scores length does not match new csfile...', flush=True)
        exit()

    # new_info = [[] for _ in range(len(new_particles_cs))]
    new_info = []
    for i in range(len(new_particles_cs)):
        new_mrcfile = new_particles_cs[i]['blob/path']
        new_idx = new_particles_cs[i]['blob/idx']
        # new_info[i] = [new_mrcfile + (str)(new_idx), i]
        new_info.append([new_mrcfile + (str)(new_idx), i])
    new_info = sorted(new_info, key=lambda x: x[0])
    # source_info = [[] for _ in range(len(new_particles_cs))]
    source_info = []
    for i in range(len(source_particles_cs)):
        source_mrcfile = source_particles_cs[i]['blob/path']
        source_idx = source_particles_cs[i]['blob/idx']
        source_uid = source_particles_cs[i]['uid']
        # source_info[i] = [source_mrcfile + (str)(source_idx), (int)(source_uid)]
        source_info.append([source_mrcfile + (str)(source_idx), (int)(source_uid)])
    source_info = sorted(source_info, key=lambda x: x[0])
    score_dict = {}
    features_dict = {}
    for i in range(len(new_particles_cs)):
        if (new_info[i][0] == source_info[i][0]):
            if if_initial_orientation_balance:
                if new_info[i][1] in features_all:
                    features_dict[source_info[i][1]] = features_all[new_info[i][1]]
            score_dict[source_info[i][1]] = (float)(scores[new_info[i][1]])
        else:
            accelerator.print('Error! Source blob info does not match new blob info...', flush=True)
            exit()

    toolbox.savetojson(score_dict, os.path.join(cryorankerdir, 'scores.json'), False)
    if if_initial_orientation_balance:
        toolbox.savebypickle(features_dict, os.path.join(cryorankerdir, 'features_dict.pickle'), False)

    wholetimeend = datetime.datetime.now()
    accelerator.print('Getting scores completed! Time spent:', wholetimeend - wholetimebegin, flush=True)