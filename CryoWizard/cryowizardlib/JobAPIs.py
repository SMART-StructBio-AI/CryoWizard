import cryosparc.tools as cst
import time
import os

import sys
sys.path.append(os.path.dirname(__file__))

import Toolbox as toolbox



# 提供基本的处理job的方法
class DealJobs():
    def __init__(self, cshandle, project, workspace, lane):
        self.cshandle = cshandle
        self.project = project
        self.workspace = workspace
        self.lane = lane

    # 获取Project路径
    def GetProjectPath(self):
        return os.path.normpath((str)(self.cshandle.find_project(self.project).dir()))

    # 安全地clear jobs，确保成功且不出现报错
    def ClearJobSafely(self, uids_waiting_for_clear):
        # uids_waiting_for_clear是一个list，里面包含的uid为str类型
        for uid in uids_waiting_for_clear:
            try:
                job = self.cshandle.find_job(self.project, uid)
            except:
                job = self.cshandle.find_external_job(self.project, uid)
            while True:
                if (job.status == 'building'):
                    break
                if job.status in ['launched', 'started', 'running', 'waiting']:
                    try:
                        job.kill()
                    except:
                        pass
                try:
                    job.clear()
                    job.wait_for_status('building', 5)
                    if (job.status == 'building'):
                        break
                except:
                    pass
                time.sleep(1)

    # 安全地kill jobs，确保成功且不出现报错
    def KillJobSafely(self, uids_waiting_for_clear):
        # uids_waiting_for_clear是一个list，里面包含的uid为str类型
        for uid in uids_waiting_for_clear:
            # handle queued jobs first
            try:
                job = self.cshandle.find_job(self.project, uid)
            except:
                job = self.cshandle.find_external_job(self.project, uid)
            if job.status in ['queued']:
                try:
                    job.clear()
                except:
                    pass
        for uid in uids_waiting_for_clear:
            # handle all jobs
            try:
                job = self.cshandle.find_job(self.project, uid)
            except:
                job = self.cshandle.find_external_job(self.project, uid)
            while True:
                if job.status in ['building', 'completed', 'killed', 'failed']:
                    break
                if job.status in ['launched', 'started', 'running', 'waiting']:
                    try:
                        job.kill()
                    except:
                        pass
                if job.status in ['queued']:
                    try:
                        job.clear()
                    except:
                        pass
                time.sleep(1)

    # 重启失败的作业
    def restartfailedjobs(self, uids_waiting_for_restart):
        # uids_waiting_for_restart是一个list，里面包含的uid为str类型
        restarted_uids = []
        for uid in uids_waiting_for_restart:
            job = self.cshandle.find_job(self.project, uid)
            if (job.status == 'failed'):
                job.clear()
                try:
                    job.queue(self.lane)
                except:
                    job.queue()
                restarted_uids.append(uid)
        return restarted_uids

    # 获取输出名
    def GetCryoSPARCJobOutputNames(self, jobuid):
        def check_output_existence_by_slots(source_job_uid, source_parameter_name):
            source_job = self.cshandle.find_job(self.project, source_job_uid)
            try:
                loaded_dataset = source_job.load_output(source_parameter_name)
                return True
            except:
                return False

        # check jobuid with parameter name
        if (len(jobuid.split('_')) > 1):
            parameter_name = jobuid[(len(jobuid.split('_')[0]) + 1):]
            return {'movie': parameter_name, 'micrograph': parameter_name, 'particle': parameter_name, 'template': parameter_name, 'volume': parameter_name, 'mask': parameter_name}

        try:
            jobjson = toolbox.readjson(os.path.join(self.GetProjectPath(), jobuid, 'job.json'))
        except:
            job = self.cshandle.find_job(self.project, jobuid)
            jobjson = job.doc

        # check external job (CryoWizard/CryoRanker/GetParticles)
        if (jobjson['title'] == 'CryoWizard'):
            if check_output_existence_by_slots(jobuid, 'best_volume'):
                return {'movie': None, 'micrograph': None, 'particle': None, 'template': None, 'volume': 'best_volume', 'mask': None}
            else:
                return {'movie': None, 'micrograph': None, 'particle': None, 'template': None, 'volume': None, 'mask': None}
        elif (jobjson['title'] == 'CryoRanker'):
            if check_output_existence_by_slots(jobuid, 'particles'):
                return {'movie': None, 'micrograph': None, 'particle': 'particles', 'template': None, 'volume': None, 'mask': None}
            else:
                return {'movie': None, 'micrograph': None, 'particle': None, 'template': None, 'volume': None, 'mask': None}
        elif (jobjson['title'] == 'GetParticles'):
            if check_output_existence_by_slots(jobuid, 'particles_selected'):
                return {'movie': None, 'micrograph': None, 'particle': 'particles_selected', 'template': None, 'volume': None, 'mask': None}
            else:
                return {'movie': None, 'micrograph': None, 'particle': None, 'template': None, 'volume': None, 'mask': None}


        # check cryosparc job
        if jobjson['job_type'] in ['import_movies']:
            return {'movie': 'imported_movies', 'micrograph': None, 'particle': None, 'template': None, 'volume': None, 'mask': None}
        elif jobjson['job_type'] in ['import_micrographs']:
            return {'movie': None, 'micrograph': 'imported_micrographs', 'particle': None, 'template': None, 'volume': None, 'mask': None}
        elif jobjson['job_type'] in ['import_particles']:
            return {'movie': None, 'micrograph': None, 'particle': 'imported_particles', 'template': None, 'volume': None, 'mask': None}
        elif jobjson['job_type'] in ['import_volumes']:
            if check_output_existence_by_slots(jobuid, 'imported_volume_1'):
                return {'movie': None, 'micrograph': None, 'particle': None, 'template': None, 'volume': 'imported_volume_1', 'mask': None}
            elif check_output_existence_by_slots(jobuid, 'imported_mask_1'):
                return {'movie': None, 'micrograph': None, 'particle': None, 'template': None, 'volume': None, 'mask': 'imported_mask_1'}
            else:
                return {'movie': None, 'micrograph': None, 'particle': None, 'template': None, 'volume': None, 'mask': None}
        elif jobjson['job_type'] in ['patch_motion_correction_multi']:
            return {'movie': None, 'micrograph': 'micrographs', 'particle': None, 'template': None, 'volume': None, 'mask': None}
        elif jobjson['job_type'] in ['patch_ctf_estimation_multi']:
            return {'movie': None, 'micrograph': 'exposures', 'particle': None, 'template': None, 'volume': None, 'mask': None}
        elif jobjson['job_type'] in ['blob_picker_gpu']:
            return {'movie': None, 'micrograph': 'micrographs', 'particle': 'particles', 'template': 'templates', 'volume': None, 'mask': None}
        elif jobjson['job_type'] in ['template_picker_gpu']:
            return {'movie': None, 'micrograph': 'micrographs', 'particle': 'particles', 'template': None, 'volume': None, 'mask': None}
        elif jobjson['job_type'] in ['create_templates']:
            return {'movie': None, 'micrograph': None, 'particle': None, 'template': 'templates', 'volume': None, 'mask': None}
        elif jobjson['job_type'] in ['extract_micrographs_multi']:
            return {'movie': None, 'micrograph': 'micrographs', 'particle': 'particles', 'template': None, 'volume': None, 'mask': None}
        elif jobjson['job_type'] in ['restack_particles']:
            return {'movie': None, 'micrograph': None, 'particle': 'particles', 'template': None, 'volume': None, 'mask': None}
        elif jobjson['job_type'] in ['class_2D_new']:
            return {'movie': None, 'micrograph': None, 'particle': 'particles', 'template': 'class_averages', 'volume': None, 'mask': None}
        elif jobjson['job_type'] in ['reference_select_2D']:
            return {'movie': None, 'micrograph': None, 'particle': 'particles_selected', 'template': 'templates_selected', 'volume': None, 'mask': None}
        elif jobjson['job_type'] in ['junk_detector_v1']:
            return {'movie': None, 'micrograph': 'exposures', 'particle': 'particles_accepted', 'template': None, 'volume': None, 'mask': None}
        elif jobjson['job_type'] in ['homo_abinit']:
            return {'movie': None, 'micrograph': None, 'particle': 'particles_all_classes', 'template': None, 'volume': 'volume_class_0', 'mask': None}
        elif jobjson['job_type'] in ['nonuniform_refine_new', 'nonuniform_refine']:
            return {'movie': None, 'micrograph': None, 'particle': 'particles', 'template': None, 'volume': 'volume', 'mask': 'mask'}
        elif jobjson['job_type'] in ['reference_motion_correction']:
            return {'movie': None, 'micrograph': 'micrograph', 'particle': 'particles_0', 'template': None, 'volume': None, 'mask': None}
        elif jobjson['job_type'] in ['ctf_refine_global']:
            return {'movie': None, 'micrograph': None, 'particle': 'particles', 'template': None, 'volume': None, 'mask': None}
        elif jobjson['job_type'] in ['ctf_refine_local']:
            return {'movie': None, 'micrograph': None, 'particle': 'particles', 'template': None, 'volume': None, 'mask': None}
        elif jobjson['job_type'] in ['particle_sets']:
            if check_output_existence_by_slots(jobuid, 'split_0'):
                return {'movie': None, 'micrograph': None, 'particle': 'split_0', 'template': None, 'volume': None, 'mask': None}
            else:
                return {'movie': None, 'micrograph': None, 'particle': None, 'template': None, 'volume': None, 'mask': None}
        elif jobjson['job_type'] in ['curate_exposures_v2']:
            if check_output_existence_by_slots(jobuid, 'exposures_accepted'):
                return {'movie': None, 'micrograph': None, 'particle': 'exposures_accepted', 'template': None, 'volume': None, 'mask': None}
            else:
                return {'movie': None, 'micrograph': None, 'particle': None, 'template': None, 'volume': None, 'mask': None}

        # elif jobjson['job_type'] in []:
        #     return {'movie': None, 'micrograph': None, 'particle': None, 'template': None, 'volume': None, 'mask': None}
        else:
            return None

    # 获取输出名，输入为list
    def GetCryoSPARCJobListOutputNames(self, job_uids_list, target_output_type):
        return [self.GetCryoSPARCJobOutputNames(job_uids_list[source_job_id_ptr])[target_output_type] for source_job_id_ptr in range(len(job_uids_list))]

    # 获取NU-Refine Job计算的最终的分辨率
    def GetNURefineFinalResolution(self, jobuid):
        try:
            jobjson = toolbox.readjson(os.path.join(self.GetProjectPath(), jobuid, 'job.json'))
        except:
            job = self.cshandle.find_job(self.project, jobuid)
            jobjson = job.doc
        fsc_final_resolution = -1.0
        for item in jobjson['output_result_groups']:
            if (item['type'] == 'volume'):
                fsc_final_resolution = item['latest_summary_stats']['fsc_info_best']['radwn_final_A']
                break
        if (fsc_final_resolution < 0):
            print('Reading resolution failed...', flush=True)
            exit()
        else:
            return fsc_final_resolution

    # 获取Reconstruct Only Job计算的最终的分辨率
    def GetReconstructOnlyFinalResolution(self, jobuid):
        try:
            jobjson = toolbox.readjson(os.path.join(self.GetProjectPath(), jobuid, 'job.json'))
        except:
            job = self.cshandle.find_job(self.project, jobuid)
            jobjson = job.doc
        fsc_final_resolution = -1.0
        for item in jobjson['output_result_groups']:
            if (item['type'] == 'volume'):
                fsc_final_resolution = item['latest_summary_stats']['fsc_info_best']['radwn_final_A']
                break
        if (fsc_final_resolution < 0):
            print('Reading resolution failed...', flush=True)
            exit()
        else:
            return fsc_final_resolution

    # 获取Orientation Diagnostics Job计算得到的CFAR值和SCF值
    def GetOrientationDiagnosticsCFARandSCF(self, jobuid, if_need_scf=True):
        try:
            jobjson = toolbox.readjson(os.path.join(self.GetProjectPath(), jobuid, 'job.json'))
        except:
            job = self.cshandle.find_job(self.project, jobuid)
            jobjson = job.doc
        cfar = jobjson['output_result_groups'][0]['latest_summary_stats']['cfar']
        if if_need_scf:
            scf = jobjson['output_result_groups'][0]['latest_summary_stats']['scf_star']
            return cfar, scf
        else:
            return cfar, None



def combine_cryoranker_scores(dealjobs_instance, cryoranker_jobs_list):
    # combine ranker scores
    cryoranker_jobs_list_order_info = []
    for jobuid in cryoranker_jobs_list:
        cryoranker_jobs_list_order_info.append({'jobuid': jobuid, 'uidnum': (int)(jobuid[1:])})
    sorted_cryoranker_jobs_list_order_info = sorted(cryoranker_jobs_list_order_info, key=lambda x: x['uidnum'], reverse=False)
    combined_scores = {}
    for sorted_jobuid_ptr in range(len(sorted_cryoranker_jobs_list_order_info)):
        sorted_jobuid = sorted_cryoranker_jobs_list_order_info[sorted_jobuid_ptr]['jobuid']
        sorted_job_scores = toolbox.readjson(os.path.join(dealjobs_instance.GetProjectPath(), sorted_jobuid, 'scores.json'))
        for particle_uid, score in sorted_job_scores.items():
            combined_scores[particle_uid] = score
    combined_scores_list = []
    for particle_uid, score in combined_scores.items():
        combined_scores_list.append({'uid': (int)(particle_uid), 'score': score})
    sorted_combined_scores_list = sorted(combined_scores_list, key=lambda x: x['score'], reverse=True)
    return sorted_combined_scores_list


def create_get_particles_by_score_job(dealJobs_instance, source_particle_job_list, source_particle_parameter_name_list, sorted_combined_scores_list, target_particle_num=None, target_score=None):

    project = dealJobs_instance.cshandle.find_project(dealJobs_instance.project)
    get_particle_job = project.create_external_job(dealJobs_instance.workspace, title='GetParticles')

    add_input_name = 'input_cryoranker'
    get_particle_job.add_input(type='particle', name=add_input_name, min=0, slots=['blob', 'ctf'], title='Input CryoRanker')
    for source_particle_job_ptr in range(len(source_particle_job_list)):
        get_particle_job.connect(target_input=add_input_name, source_job_uid=source_particle_job_list[source_particle_job_ptr], source_output=source_particle_parameter_name_list[source_particle_job_ptr])

    get_particle_job_path = os.path.normpath(os.path.join(dealJobs_instance.GetProjectPath(), get_particle_job.uid))
    if target_particle_num is not None:
        toolbox.savetojson({'get_type': 'num', 'cut_off_point': target_particle_num}, os.path.join(get_particle_job_path, 'get_top_particles_parameters.json'), False)
    elif target_score is not None:
        toolbox.savetojson({'get_type': 'score', 'cut_off_point': target_score}, os.path.join(get_particle_job_path, 'get_top_particles_parameters.json'), False)
    else:
        toolbox.savetojson({'get_type': 'score', 'cut_off_point': 0.6}, os.path.join(get_particle_job_path, 'get_top_particles_parameters.json'), False)
    get_top_particles_parameters = toolbox.readjson(os.path.join(get_particle_job_path, 'get_top_particles_parameters.json'))

    input_particles_dataset = get_particle_job.load_input(name=add_input_name)
    with get_particle_job.run():
        selected_uids = []
        if (get_top_particles_parameters['get_type'] == 'num'):
            safe_max_num = get_top_particles_parameters['cut_off_point'] if (get_top_particles_parameters['cut_off_point'] <= len(sorted_combined_scores_list)) else len(sorted_combined_scores_list)
            for score_ptr in range(safe_max_num):
                selected_uids.append(sorted_combined_scores_list[score_ptr]['uid'])
        elif (get_top_particles_parameters['get_type'] == 'score'):
            for score_ptr in range(len(sorted_combined_scores_list)):
                if (sorted_combined_scores_list[score_ptr]['score'] >= get_top_particles_parameters['cut_off_point']):
                    selected_uids.append(sorted_combined_scores_list[score_ptr]['uid'])
        else:
            get_particle_job.log('get_top_particles_parameters wrong, return None')
            return

        output_particles_dataset = input_particles_dataset.query({'uid': selected_uids})

        add_output_name = 'particles_selected'
        get_particle_job.add_output(type='particle', name=add_output_name, slots=['blob', 'ctf'], passthrough=add_input_name)
        get_particle_job.save_output(add_output_name, output_particles_dataset)

    return get_particle_job


def split_particles_by_slots(dealJobs_instance, source_job_list, source_parameter_name_list, target_slots, target_slots_example_items):
    accept_job_list = []
    reject_job_list = []
    for source_job_ptr in range(len(source_job_list)):
        source_job = dealJobs_instance.cshandle.find_job(dealJobs_instance.project, extract_source_job_ids(source_job_list[source_job_ptr]))
        try:
            loaded_dataset = source_job.load_output(source_parameter_name_list[source_job_ptr], slots=target_slots)
            for example_item in target_slots_example_items:
                test_item = loaded_dataset[0][example_item]
            accept_job_list.append(source_job_list[source_job_ptr])
        except:
            reject_job_list.append(source_job_list[source_job_ptr])
    return accept_job_list, reject_job_list


def check_cryosparc_tools_version(min_version):
    cryosparc_tools_version = cst.__version__.split('.')
    target_min_version = min_version.split('.')
    for version_level_ptr in range(len(target_min_version) if (len(target_min_version) <= len(cryosparc_tools_version)) else len(cryosparc_tools_version)):
        if ((int)(cryosparc_tools_version[version_level_ptr]) > (int)(target_min_version[version_level_ptr])):
            return True
        if ((int)(cryosparc_tools_version[version_level_ptr]) < (int)(target_min_version[version_level_ptr])):
            return False
    return True


def resolve_source_job_uids(globaldir, source_job_uid_name_list, target_output_type):
    source_job_id = []
    for source_job_id_name in source_job_uid_name_list:
        source_job_id_head = source_job_id_name.split('_')[0]
        if (source_job_id_head == 'import'):
            output_groups = toolbox.readjson(os.path.join(globaldir, 'metadata', 'import', source_job_id_name, 'output_groups.json'))
            if output_groups[target_output_type] is not None:
                source_job_id += output_groups[target_output_type]
        elif (source_job_id_head == 'preprocess'):
            output_groups = toolbox.readjson(os.path.join(globaldir, 'metadata', 'preprocess', source_job_id_name, 'output_groups.json'))
            if output_groups[target_output_type] is not None:
                source_job_id += output_groups[target_output_type]
        elif (source_job_id_head == 'cryoranker'):
            output_groups = toolbox.readjson(os.path.join(globaldir, 'metadata', 'cryoranker', source_job_id_name, 'output_groups.json'))
            if output_groups[target_output_type] is not None:
                source_job_id += output_groups[target_output_type]
        elif (source_job_id_head == 'refine'):
            output_groups = toolbox.readjson(os.path.join(globaldir, 'metadata', 'refine', source_job_id_name, 'output_groups.json'))
            if output_groups[target_output_type] is not None:
                source_job_id += output_groups[target_output_type]
        elif (source_job_id_head == 'postprocess'):
            output_groups = toolbox.readjson(os.path.join(globaldir, 'metadata', 'postprocess', source_job_id_name, 'output_groups.json'))
            if output_groups[target_output_type] is not None:
                source_job_id += output_groups[target_output_type]

        # other elif

        elif (source_job_id_head[0] == 'J'):
            source_job_id.append(source_job_id_name)
    return source_job_id


def extract_source_job_ids(source_job_uid):
    if isinstance(source_job_uid, str):
        return source_job_uid.split('_')[0]
    elif isinstance(source_job_uid, list):
        return [source_job_uid[source_job_uid_ptr].split('_')[0] for source_job_uid_ptr in range(len(source_job_uid))]
    else:
        return None


def cryowizard_log(cryowizardjob, cryowizardlog, loginfo):
    cryowizardjob.log(loginfo)
    with open(cryowizardlog, 'a') as f:
        f.write(loginfo + '\n')


def get_job_connected_inputs(job):
    job_inputs_info = {}
    for i in range(len(job.doc['input_slot_groups'])):
        input_group_name = job.doc['input_slot_groups'][i]['name']
        input_group_info = []
        for single_input_ptr in range(len(job.doc['input_slot_groups'][i]['connections'])):
            single_input_info = job.doc['input_slot_groups'][i]['connections'][single_input_ptr]
            input_group_info.append({'index': single_input_ptr, 'job_uid': single_input_info['job_uid'], 'job_output_name': single_input_info['group_name']})
        job_inputs_info[input_group_name] = input_group_info
    return job_inputs_info


# created_jobs_info: used to run, continue and restart cryosparc job, do not add external job into it
def create_created_jobs_info_item(jobuid, parents=[], gpu_need=0):
    return {'jobuid': jobuid, 'parents': parents, 'gpu_need': gpu_need}


def create_created_cryoranker_jobs_info_item(jobuid, parents=[]):
    return {'jobuid': jobuid, 'parents': parents}


# output_groups: used to record output jobs uids list
def create_output_groups(movie=None, micrograph=None, particle=None, template=None, volume=None, mask=None, ranker=None):
    return {'movie': movie, 'micrograph': micrograph, 'particle': particle, 'template': template, 'volume': volume, 'mask': mask, 'ranker': ranker}


def run_all_created_jobs(dealjobs_instance, parameters, all_created_jobs_info_list):
    # return while all jobs done
    for single_created_job_info in all_created_jobs_info_list:
        single_created_job = dealjobs_instance.cshandle.find_job(parameters['project'], single_created_job_info['jobuid'])
        if (single_created_job.status in ['building']):
            try:
                single_created_job.queue(parameters['lane'])
            except:
                single_created_job.queue()
        elif not (single_created_job.status in ['queued', 'launched', 'started', 'running', 'completed']):
            # continue run jobs
            dealjobs_instance.ClearJobSafely([single_created_job_info['jobuid']])
            try:
                single_created_job.queue(parameters['lane'])
            except:
                single_created_job.queue()
    for single_created_job_info in all_created_jobs_info_list:
        single_created_job = dealjobs_instance.cshandle.find_job(parameters['project'], single_created_job_info['jobuid'])
        single_created_job.wait_for_done()
        trying_time = 0
        while (trying_time < parameters['max_trying_time']):
            # auto restart failed jobs
            if not (single_created_job.status in ['completed']):
                trying_time += 1
                dealjobs_instance.ClearJobSafely([single_created_job_info['jobuid']])
                try:
                    single_created_job.queue(parameters['lane'])
                except:
                    single_created_job.queue()
                single_created_job.wait_for_done()
                if single_created_job.status in ['completed']:
                    break
            else:
                break
        if single_created_job.status not in ['completed']:
            raise Exception(single_created_job.uid + ' did not complete')


def kill_all_created_jobs(dealjobs_instance, all_created_jobs_info_list):
    # return while all jobs done
    job_uids_list = []
    for single_created_job_info in all_created_jobs_info_list:
        job_uids_list.append(single_created_job_info['jobuid'])
    dealjobs_instance.KillJobSafely(job_uids_list)



class CreateImportMovies():
    def __init__(self, DealJobs_instance):
        self.dealjobtools = DealJobs_instance

    def QueueImportMoviesJob(self, parameters, build_only=False):
        filedir = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
        job = self.dealjobtools.cshandle.create_job(self.dealjobtools.project, self.dealjobtools.workspace, toolbox.readjson(os.path.join(filedir, 'parameters', 'import_movies_job_name.json')))

        parameters_map = toolbox.readjson(os.path.join(filedir, 'parameters', 'import_movies_parameters_map.json'))
        for param_title in parameters:
            job.set_param(parameters_map[param_title], parameters[param_title])

        if not build_only:
            job.queue(self.dealjobtools.lane)
        return job


class CreateImportMicrographs():
    def __init__(self, DealJobs_instance):
        self.dealjobtools = DealJobs_instance

    def QueueImportMicrographsJob(self, parameters, source_movie_job_list=None, source_movie_parameter_name_list=None, build_only=False):
        filedir = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
        job = self.dealjobtools.cshandle.create_job(self.dealjobtools.project, self.dealjobtools.workspace, toolbox.readjson(os.path.join(filedir, 'parameters', 'import_micrographs_job_name.json')))
        if source_movie_job_list is not None:
            for i in range(len(source_movie_job_list)):
                job.connect('movies', source_movie_job_list[i], source_movie_parameter_name_list[i])

        parameters_map = toolbox.readjson(os.path.join(filedir, 'parameters', 'import_micrographs_parameters_map.json'))
        for param_title in parameters:
            job.set_param(parameters_map[param_title], parameters[param_title])

        if not build_only:
            job.queue(self.dealjobtools.lane)
        return job


class CreateImportParticleStack():
    def __init__(self, DealJobs_instance):
        self.dealjobtools = DealJobs_instance

    def QueueImportParticleStackJob(self, parameters, source_exposure_job_list=None, source_exposure_parameter_name_list=None, build_only=False):
        filedir = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
        job = self.dealjobtools.cshandle.create_job(self.dealjobtools.project, self.dealjobtools.workspace, toolbox.readjson(os.path.join(filedir, 'parameters', 'import_particle_stack_job_name.json')))
        if source_exposure_job_list is not None:
            for i in range(len(source_exposure_job_list)):
                job.connect('movies', source_exposure_job_list[i], source_exposure_parameter_name_list[i])

        parameters_map = toolbox.readjson(os.path.join(filedir, 'parameters', 'import_particle_stack_parameters_map.json'))
        for param_title in parameters:
            job.set_param(parameters_map[param_title], parameters[param_title])

        if not build_only:
            job.queue(self.dealjobtools.lane)
        return job


class CreateImportVolume():
    def __init__(self, DealJobs_instance):
        self.dealjobtools = DealJobs_instance

    def QueueImportVolumeJob(self, parameters, build_only=False):
        filedir = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
        job = self.dealjobtools.cshandle.create_job(self.dealjobtools.project, self.dealjobtools.workspace, toolbox.readjson(os.path.join(filedir, 'parameters', 'import_volume_job_name.json')))

        parameters_map = toolbox.readjson(os.path.join(filedir, 'parameters', 'import_volume_parameters_map.json'))
        for param_title in parameters:
            job.set_param(parameters_map[param_title], parameters[param_title])

        if not build_only:
            job.queue(self.dealjobtools.lane)
        return job


class CreatePatchMotionCorrection():
    def __init__(self, DealJobs_instance):
        self.dealjobtools = DealJobs_instance

    def QueuePatchMotionCorrectionJob(self, parameters, source_movie_job_list, source_movie_parameter_name_list, source_doseweight_job=None, source_doseweight_parameter_name=None, hostname=None, gpus=None, build_only=False):
        filedir = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
        job = self.dealjobtools.cshandle.create_job(self.dealjobtools.project, self.dealjobtools.workspace, toolbox.readjson(os.path.join(filedir, 'parameters', 'patch_motion_correction_job_name.json')))
        for i in range(len(source_movie_job_list)):
            job.connect('movies', source_movie_job_list[i], source_movie_parameter_name_list[i])
        if source_doseweight_job is not None:
            job.connect('doseweights', source_doseweight_job, source_doseweight_parameter_name)

        parameters_map = toolbox.readjson(os.path.join(filedir, 'parameters', 'patch_motion_correction_parameters_map.json'))
        for param_title in parameters:
            job.set_param(parameters_map[param_title], parameters[param_title])

        if not build_only:
            if hostname is not None:
                job.queue(self.dealjobtools.lane, hostname, gpus)
            else:
                job.queue(self.dealjobtools.lane)
        return job


class CreatePatchCtfEstimation():
    def __init__(self, DealJobs_instance):
        self.dealjobtools = DealJobs_instance

    def QueuePatchCtfEstimationJob(self, parameters, source_exposure_job_list, source_exposure_parameter_name_list, hostname=None, gpus=None, build_only=False):
        filedir = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
        job = self.dealjobtools.cshandle.create_job(self.dealjobtools.project, self.dealjobtools.workspace, toolbox.readjson(os.path.join(filedir, 'parameters', 'patch_ctf_estimation_job_name.json')))
        for i in range(len(source_exposure_job_list)):
            job.connect('exposures', source_exposure_job_list[i], source_exposure_parameter_name_list[i])

        parameters_map = toolbox.readjson(os.path.join(filedir, 'parameters', 'patch_ctf_estimation_parameters_map.json'))
        for param_title in parameters:
            job.set_param(parameters_map[param_title], parameters[param_title])

        if not build_only:
            if hostname is not None:
                job.queue(self.dealjobtools.lane, hostname, gpus)
            else:
                job.queue(self.dealjobtools.lane)
        return job


class CreateBlobPicker():
    def __init__(self, DealJobs_instance):
        self.dealjobtools = DealJobs_instance

    def QueueBlobPickerJob(self, parameters, source_micrograph_job_list, source_micrograph_parameter_name_list, hostname=None, gpus=None, build_only=False):
        filedir = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
        job = self.dealjobtools.cshandle.create_job(self.dealjobtools.project, self.dealjobtools.workspace, toolbox.readjson(os.path.join(filedir, 'parameters', 'blob_picker_job_name.json')))
        for i in range(len(source_micrograph_job_list)):
            job.connect('micrographs', source_micrograph_job_list[i], source_micrograph_parameter_name_list[i])

        parameters_map = toolbox.readjson(os.path.join(filedir, 'parameters', 'blob_picker_parameters_map.json'))
        for param_title in parameters:
            job.set_param(parameters_map[param_title], parameters[param_title])

        if not build_only:
            if hostname is not None:
                job.queue(self.dealjobtools.lane, hostname, gpus)
            else:
                job.queue(self.dealjobtools.lane)
        return job


class CreateTemplatePicker():
    def __init__(self, DealJobs_instance):
        self.dealjobtools = DealJobs_instance

    def QueueTemplatePickerJob(self, parameters, source_micrograph_job_list, source_micrograph_parameter_name_list, source_template_job_list, source_template_parameter_name_list, hostname=None, gpus=None, build_only=False):
        filedir = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
        job = self.dealjobtools.cshandle.create_job(self.dealjobtools.project, self.dealjobtools.workspace, toolbox.readjson(os.path.join(filedir, 'parameters', 'template_picker_job_name.json')))
        for i in range(len(source_micrograph_job_list)):
            job.connect('micrographs', source_micrograph_job_list[i], source_micrograph_parameter_name_list[i])
        for i in range(len(source_template_job_list)):
            job.connect('templates', source_template_job_list[i], source_template_parameter_name_list[i])

        parameters_map = toolbox.readjson(os.path.join(filedir, 'parameters', 'template_picker_parameters_map.json'))
        for param_title in parameters:
            job.set_param(parameters_map[param_title], parameters[param_title])

        if not build_only:
            if hostname is not None:
                job.queue(self.dealjobtools.lane, hostname, gpus)
            else:
                job.queue(self.dealjobtools.lane)
        return job


class CreateCreateTemplates():
    def __init__(self, DealJobs_instance):
        self.dealjobtools = DealJobs_instance

    def QueueCreateTemplatesJob(self, parameters, source_volume_job, source_volume_parameter_name, build_only=False):
        filedir = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
        job = self.dealjobtools.cshandle.create_job(self.dealjobtools.project, self.dealjobtools.workspace, toolbox.readjson(os.path.join(filedir, 'parameters', 'create_templates_job_name.json')))
        job.connect('volume', source_volume_job, source_volume_parameter_name)

        parameters_map = toolbox.readjson(os.path.join(filedir, 'parameters', 'create_templates_parameters_map.json'))
        for param_title in parameters:
            job.set_param(parameters_map[param_title], parameters[param_title])

        if not build_only:
            job.queue(self.dealjobtools.lane)
        return job


class CreateExtractMicrographs():
    def __init__(self, DealJobs_instance):
        self.dealjobtools = DealJobs_instance

    def QueueExtractMicrographsJob(self, parameters, source_micrograph_job_list, source_micrograph_parameter_name_list, source_particle_job_list, source_particle_parameter_name_list, hostname=None, gpus=None, build_only=False):
        filedir = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
        job = self.dealjobtools.cshandle.create_job(self.dealjobtools.project, self.dealjobtools.workspace, toolbox.readjson(os.path.join(filedir, 'parameters', 'extract_micrographs_job_name.json')))
        for i in range(len(source_micrograph_job_list)):
            job.connect('micrographs', source_micrograph_job_list[i], source_micrograph_parameter_name_list[i])
        for i in range(len(source_particle_job_list)):
            job.connect('particles', source_particle_job_list[i], source_particle_parameter_name_list[i])

        parameters_map = toolbox.readjson(os.path.join(filedir, 'parameters', 'extract_micrographs_parameters_map.json'))
        for param_title in parameters:
            job.set_param(parameters_map[param_title], parameters[param_title])

        if not build_only:
            if hostname is not None:
                job.queue(self.dealjobtools.lane, hostname, gpus)
            else:
                job.queue(self.dealjobtools.lane)
        return job


class CreateRestackParticles():
    def __init__(self, DealJobs_instance):
        self.dealjobtools = DealJobs_instance

    def QueueRestackJob(self, parameters, source_particle_job_list, source_particle_parameter_name_list, build_only=False):
        filedir = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
        job = self.dealjobtools.cshandle.create_job(self.dealjobtools.project, self.dealjobtools.workspace, toolbox.readjson(os.path.join(filedir, 'parameters', 'restack_particles_job_name.json')))
        for i in range(len(source_particle_job_list)):
            job.connect('particles', source_particle_job_list[i], source_particle_parameter_name_list[i])

        parameters_map = toolbox.readjson(os.path.join(filedir, 'parameters', 'restack_particles_parameters_map.json'))
        for param_title in parameters:
            job.set_param(parameters_map[param_title], parameters[param_title])

        if not build_only:
            job.queue(self.dealjobtools.lane)
        return job


class Create2DClassification():
    def __init__(self, DealJobs_instance):
        self.dealjobtools = DealJobs_instance

    def Queue2DClassificationJob(self, parameters, source_particle_job_list, source_particle_parameter_name_list, hostname=None, gpus=None, build_only=False):
        filedir = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
        job = self.dealjobtools.cshandle.create_job(self.dealjobtools.project, self.dealjobtools.workspace, toolbox.readjson(os.path.join(filedir, 'parameters', '2d_classification_job_name.json')))
        for i in range(len(source_particle_job_list)):
            job.connect('particles', source_particle_job_list[i], source_particle_parameter_name_list[i])

        parameters_map = toolbox.readjson(os.path.join(filedir, 'parameters', '2d_classification_parameters_map.json'))
        for param_title in parameters:
            job.set_param(parameters_map[param_title], parameters[param_title])

        if not build_only:
            if hostname is not None:
                job.queue(self.dealjobtools.lane, hostname, gpus)
            else:
                job.queue(self.dealjobtools.lane)
        return job


class CreateReferenceBasedAutoSelect2D():
    def __init__(self, DealJobs_instance):
        self.dealjobtools = DealJobs_instance

    def QueueReferenceBasedAutoSelect2DJob(self, parameters, source_particle_job, source_particle_parameter_name, source_2d_average_job, source_2d_average_parameter_name, source_volume_job, source_volume_parameter_name, hostname=None, gpus=None, build_only=False):
        filedir = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
        job = self.dealjobtools.cshandle.create_job(self.dealjobtools.project, self.dealjobtools.workspace, toolbox.readjson(os.path.join(filedir, 'parameters', 'reference_select_2d_job_name.json')))
        job.connect('particles', source_particle_job, source_particle_parameter_name)
        job.connect('templates', source_2d_average_job, source_2d_average_parameter_name)
        job.connect('volume', source_volume_job, source_volume_parameter_name)

        parameters_map = toolbox.readjson(os.path.join(filedir, 'parameters', 'reference_select_2d_parameters_map.json'))
        for param_title in parameters:
            job.set_param(parameters_map[param_title], parameters[param_title])

        if not build_only:
            if hostname is not None:
                job.queue(self.dealjobtools.lane, hostname, gpus)
            else:
                job.queue(self.dealjobtools.lane)
        return job


class CreateMicrographJunkDetector():
    def __init__(self, DealJobs_instance):
        self.dealjobtools = DealJobs_instance

    def QueueMicrographJunkDetectorJob(self, parameters, source_exposure_job_list, source_exposure_parameter_name_list, source_particle_job_list=None, source_particle_parameter_name_list=None, hostname=None, gpus=None, build_only=False):
        filedir = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
        job = self.dealjobtools.cshandle.create_job(self.dealjobtools.project, self.dealjobtools.workspace, toolbox.readjson(os.path.join(filedir, 'parameters', 'junk_detector_job_name.json')))
        for i in range(len(source_exposure_job_list)):
            job.connect('exposures', source_exposure_job_list[i], source_exposure_parameter_name_list[i])
        if source_particle_job_list is not None:
            for i in range(len(source_particle_job_list)):
                job.connect('particles', source_particle_job_list[i], source_particle_parameter_name_list[i])

        parameters_map = toolbox.readjson(os.path.join(filedir, 'parameters', 'junk_detector_parameters_map.json'))
        for param_title in parameters:
            job.set_param(parameters_map[param_title], parameters[param_title])

        if not build_only:
            if hostname is not None:
                job.queue(self.dealjobtools.lane, hostname, gpus)
            else:
                job.queue(self.dealjobtools.lane)
        return job


class CreateHomoAbinit():
    def __init__(self, DealJobs_instance):
        self.dealjobtools = DealJobs_instance

    def QueueHomoAbinitJob(self, parameters, source_particle_job_list, source_particle_parameter_name_list, hostname=None, gpus=None, build_only=False):
        filedir = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
        job = self.dealjobtools.cshandle.create_job(self.dealjobtools.project, self.dealjobtools.workspace, toolbox.readjson(os.path.join(filedir, 'parameters', 'abinit_job_name.json')))
        for i in range(len(source_particle_job_list)):
            job.connect('particles', source_particle_job_list[i], source_particle_parameter_name_list[i])

        parameters_map = toolbox.readjson(os.path.join(filedir, 'parameters', 'abinit_parameters_map.json'))
        for param_title in parameters:
            job.set_param(parameters_map[param_title], parameters[param_title])

        if not build_only:
            if hostname is not None:
                job.queue(self.dealjobtools.lane, hostname, gpus)
            else:
                job.queue(self.dealjobtools.lane)
        return job


class CreateNonuniformRefine():
    def __init__(self, DealJobs_instance):
        self.dealjobtools = DealJobs_instance

    def QueueNonuniformRefineJob(self, parameters, source_particle_job_list, source_particle_parameter_name_list, source_map_job, source_map_parameter_name, source_mask_job=None, source_mask_parameter_name=None, hostname=None, gpus=None, build_only=False):
        filedir = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
        job = self.dealjobtools.cshandle.create_job(self.dealjobtools.project, self.dealjobtools.workspace, toolbox.readjson(os.path.join(filedir, 'parameters', 'nurefine_job_name.json')))
        for i in range(len(source_particle_job_list)):
            job.connect('particles', source_particle_job_list[i], source_particle_parameter_name_list[i])
        job.connect('volume', source_map_job, source_map_parameter_name)
        if source_mask_job is not None:
            job.connect('mask', source_mask_job, source_mask_parameter_name)

        parameters_map = toolbox.readjson(os.path.join(filedir, 'parameters', 'nurefine_parameters_map.json'))
        for param_title in parameters:
            job.set_param(parameters_map[param_title], parameters[param_title])

        if not build_only:
            if hostname is not None:
                job.queue(self.dealjobtools.lane, hostname, gpus)
            else:
                job.queue(self.dealjobtools.lane)
        return job


class CreateReferenceMotionCorrection():
    def __init__(self, DealJobs_instance):
        self.dealjobtools = DealJobs_instance

    def QueueReferenceMotionCorrectionJob(self, parameters, source_exposures_job_list, source_exposures_parameter_name_list, source_particle_job, source_particle_parameter_name, source_map_job, source_map_parameter_name, source_mask_job=None, source_mask_parameter_name=None, source_hyper_parameters_job=None, source_hyper_parameters_parameter_name=None, hostname=None, gpus=None, build_only=False):
        filedir = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
        job = self.dealjobtools.cshandle.create_job(self.dealjobtools.project, self.dealjobtools.workspace, toolbox.readjson(os.path.join(filedir, 'parameters', 'reference_motion_correction_job_name.json')))
        for i in range(len(source_exposures_job_list)):
            job.connect('micrograph', source_exposures_job_list[i], source_exposures_parameter_name_list[i])
        job.connect('particles_0', source_particle_job, source_particle_parameter_name)
        job.connect('volume_0', source_map_job, source_map_parameter_name)
        if source_mask_job is not None:
            job.connect('mask_0', source_mask_job, source_mask_parameter_name)
        if source_hyper_parameters_job is not None:
            job.connect('hyperparameters', source_hyper_parameters_job, source_hyper_parameters_parameter_name)

        parameters_map = toolbox.readjson(os.path.join(filedir, 'parameters', 'reference_motion_correction_parameters_map.json'))
        for param_title in parameters:
            job.set_param(parameters_map[param_title], parameters[param_title])

        if not build_only:
            if hostname is not None:
                job.queue(self.dealjobtools.lane, hostname, gpus)
            else:
                job.queue(self.dealjobtools.lane)
        return job


class CreateCTFRefineGlobal():
    def __init__(self, DealJobs_instance):
        self.dealjobtools = DealJobs_instance

    def QueueCTFRefineGlobalJob(self, parameters, source_particle_job_list, source_particle_parameter_name_list, source_volume_job, source_volume_parameter_name, source_mask_job=None, source_mask_parameter_name=None, hostname=None, gpus=None, build_only=False):
        filedir = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
        job = self.dealjobtools.cshandle.create_job(self.dealjobtools.project, self.dealjobtools.workspace, toolbox.readjson(os.path.join(filedir, 'parameters', 'ctf_refine_global_job_name.json')))
        for i in range(len(source_particle_job_list)):
            job.connect('particles', source_particle_job_list[i], source_particle_parameter_name_list[i])
        job.connect('volume', source_volume_job, source_volume_parameter_name)
        if source_mask_job is not None:
            job.connect('mask', source_mask_job, source_mask_parameter_name)

        parameters_map = toolbox.readjson(os.path.join(filedir, 'parameters', 'ctf_refine_global_parameters_map.json'))
        for param_title in parameters:
            job.set_param(parameters_map[param_title], parameters[param_title])

        if not build_only:
            if hostname is not None:
                job.queue(self.dealjobtools.lane, hostname, gpus)
            else:
                job.queue(self.dealjobtools.lane)
        return job


class CreateCTFRefineLocal():
    def __init__(self, DealJobs_instance):
        self.dealjobtools = DealJobs_instance

    def QueueCTFRefineLocalJob(self, parameters, source_particle_job_list, source_particle_parameter_name_list, source_volume_job, source_volume_parameter_name, source_mask_job=None, source_mask_parameter_name=None, hostname=None, gpus=None, build_only=False):
        filedir = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
        job = self.dealjobtools.cshandle.create_job(self.dealjobtools.project, self.dealjobtools.workspace, toolbox.readjson(os.path.join(filedir, 'parameters', 'ctf_refine_local_job_name.json')))
        for i in range(len(source_particle_job_list)):
            job.connect('particles', source_particle_job_list[i], source_particle_parameter_name_list[i])
        job.connect('volume', source_volume_job, source_volume_parameter_name)
        if source_mask_job is not None:
            job.connect('mask', source_mask_job, source_mask_parameter_name)

        parameters_map = toolbox.readjson(os.path.join(filedir, 'parameters', 'ctf_refine_local_parameters_map.json'))
        for param_title in parameters:
            job.set_param(parameters_map[param_title], parameters[param_title])

        if not build_only:
            if hostname is not None:
                job.queue(self.dealjobtools.lane, hostname, gpus)
            else:
                job.queue(self.dealjobtools.lane)
        return job


class CreateParticleSetsTool():
    def __init__(self, DealJobs_instance):
        self.dealjobtools = DealJobs_instance

    def QueueParticleSetsToolJob(self, parameters, source_particle_job_list_A, source_particle_parameter_name_list_A, source_particle_job_list_B=None, source_particle_parameter_name_list_B=None, build_only=False):
        filedir = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
        job = self.dealjobtools.cshandle.create_job(self.dealjobtools.project, self.dealjobtools.workspace, toolbox.readjson(os.path.join(filedir, 'parameters', 'particle_set_tools_job_name.json')))
        for i in range(len(source_particle_job_list_A)):
            job.connect('particles_A', source_particle_job_list_A[i], source_particle_parameter_name_list_A[i])
        if source_particle_job_list_B is not None:
            for i in range(len(source_particle_job_list_B)):
                job.connect('particles_B', source_particle_job_list_B[i], source_particle_parameter_name_list_B[i])

        parameters_map = toolbox.readjson(os.path.join(filedir, 'parameters', 'particle_set_tools_parameters_map.json'))
        for param_title in parameters:
            job.set_param(parameters_map[param_title], parameters[param_title])

        if not build_only:
            job.queue(self.dealjobtools.lane)
        return job


class CreateCurateExposures():
    def __init__(self, DealJobs_instance):
        self.dealjobtools = DealJobs_instance

    def QueueCurateExposuresJob(self, parameters, source_exposures_job_list, source_exposures_parameter_name_list, source_particle_job_list=None, source_particle_parameter_name_list=None, build_only=False):
        filedir = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
        job = self.dealjobtools.cshandle.create_job(self.dealjobtools.project, self.dealjobtools.workspace, toolbox.readjson(os.path.join(filedir, 'parameters', 'curate_exposures_job_name.json')))
        for i in range(len(source_exposures_job_list)):
            job.connect('exposures', source_exposures_job_list[i], source_exposures_parameter_name_list[i])
        if source_particle_job_list is not None:
            for i in range(len(source_particle_job_list)):
                job.connect('particles', source_particle_job_list[i], source_particle_parameter_name_list[i])

        parameters_map = toolbox.readjson(os.path.join(filedir, 'parameters', 'curate_exposures_parameters_map.json'))
        for param_title in parameters:
            job.set_param(parameters_map[param_title], parameters[param_title])

        if not build_only:
            job.queue()
        return job


class CreateOrientationDiagnostics():
    def __init__(self, DealJobs_instance):
        self.dealjobtools = DealJobs_instance

    def QueueOrientationDiagnosticsJob(self, parameters, source_volume_job, source_volume_parameter_name, source_particle_job_list=None, source_particle_parameter_name_list=None, source_mask_job=None, source_mask_parameter_name=None, hostname=None, gpus=None, build_only=False):
        filedir = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
        job = self.dealjobtools.cshandle.create_job(self.dealjobtools.project, self.dealjobtools.workspace, toolbox.readjson(os.path.join(filedir, 'parameters', 'orientation_diagnostics_job_name.json')))
        job.connect('volume', source_volume_job, source_volume_parameter_name)
        if source_particle_job_list is not None:
            for i in range(len(source_particle_job_list)):
                job.connect('particles', source_particle_job_list[i], source_particle_parameter_name_list[i])
        if source_mask_job is not None:
            job.connect('mask', source_mask_job, source_mask_parameter_name)

        parameters_map = toolbox.readjson(os.path.join(filedir, 'parameters', 'orientation_diagnostics_parameters_map.json'))
        for param_title in parameters:
            job.set_param(parameters_map[param_title], parameters[param_title])

        if not build_only:
            if hostname is not None:
                job.queue(self.dealjobtools.lane, hostname, gpus)
            else:
                job.queue(self.dealjobtools.lane)
        return job