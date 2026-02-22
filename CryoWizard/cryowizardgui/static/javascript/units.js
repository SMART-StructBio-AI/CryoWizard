

function GetSessionStorageJsonItem(session_storage_key)
{
    return JSON.parse(sessionStorage.getItem(session_storage_key));
}


function SetSessionStorageJsonItem(session_storage_key, json_value)
{
    sessionStorage.setItem(session_storage_key, JSON.stringify(json_value));
}


function PipelinePresetTypeNameChange(cmd_name)
{
    var name_change_dict = {
        "default": "CryoWizard pipeline default",
        "simpler": "CryoWizard pipeline simpler",
        "cryoranker_only": "CryoRanker only",
        "cryoranker_get_top_particles": "CryoRanker get top particles",
        "custom": "Custom",
    };
    return name_change_dict[cmd_name];
}


function SinglePipelineNodeNameChange(cmd_name)
{
    var name_change_dict = {
        "import_movie_file_parameters": "import movie files",
        "import_micrograph_file_parameters": "import micrograph files",
        "import_particle_file_parameters": "import particle files",
        "import_volume_file_parameters": "import volume file",
        "preprocess_movie_with_blob_pick_parameters": "preprocess movies (blob picker)",
        "preprocess_movie_with_template_pick_parameters": "preprocess movies (template picker)",
        "preprocess_micrograph_with_blob_pick_parameters": "preprocess micrographs (blob picker)",
        "preprocess_micrograph_with_template_pick_parameters": "preprocess micrographs (template picker)",
        "preprocess_particle_parameters": "preprocess particles",
        "create_templates_parameters": "create templates from volume",
        "reference_based_auto_select_2d": "reference based auto select 2D",
        "junk_detector": "junk detector",
        "cryoranker_parameters": "cryoranker",
        "get_top_particles": "cryoranker get top particles",
        "refine_parameters": "refine",
        "motion_and_ctf_refine_parameters": "motion and ctf refine",
    };
    return name_change_dict[cmd_name];
}


function PipelineParametersNameChange(cmd_name)
{
    var name_change_dict = {
        "cryosparc_lane": "CryoSPARC Lane",
        "slurm": "Inference on Slurm?",
        "inference_gpu_ids": "Inference GPU ids",
        "source_movie_job_uid": "Input movie jobs (e.g. J1 J2)",
        "source_micrograph_job_uid": "Input micrograph jobs (e.g. J1 J2)",
        "source_particle_job_uid": "Input particle jobs (e.g. J1 J2)",
        "source_template_job_uid": "Input template jobs (e.g. J1 J2)",
        "source_volume_job_uid": "Input volume jobs (e.g. J1 J2)",
        "source_mask_job_uid": "Input mask jobs (e.g. J1 J2)",
        "source_cryoranker_job_uid": "Input cryoranker jobs (e.g. J1 J2)",
        "movies_data_path": "Movies data path",
        "gain_reference_path": "Gain reference path",
        "micrographs_data_path": "Micrographs data path",
        "particles_data_path": "Particle data path",
        "particles_meta_path": "Particle meta path",
        "volume_data_path": "Volume data path",
        "volume_emdb_id": "Volume EMDB Id",
        "volume_import_type": "Volume import type",
        "volume_pixelsize": "Volume pixel size (A)",
        "accelerating_voltage": "Accelerating Voltage (kV)",
        "spherical_aberration": "Spherical Aberration (mm)",
        "total_exposure_dose": "Total exposure dose (e/A^2)",
        "raw_pixel_size": "Raw pixel size (A)",
        "particle_diameter": "Average Particle diameter (A)",
        "ctf_fit_resolution": "CTF fit resolution",
        "symmetry": "Symmetry",
        "gpu_num": "Number of GPUs for Multi-GPU CryoSPARC jobs",
        "get_top_particles_num": "Get top particles number",
        "get_top_particles_score": "Get top particles score",
    };
    return name_change_dict[cmd_name];
}


function PipelinePresetParametersList(preset_type)
{
    var target_parameters_list = null;
    if (preset_type == "default") {
        target_parameters_list = [
            "cryosparc_lane",
            "slurm",
            "inference_gpu_ids",
            "movies_data_path",
            "gain_reference_path",
            "micrographs_data_path",
            "particles_data_path",
            "particles_meta_path",
            "source_movie_job_uid",
            "source_micrograph_job_uid",
            "source_particle_job_uid",
            "accelerating_voltage",
            "spherical_aberration",
            "total_exposure_dose",
            "raw_pixel_size",
            "particle_diameter",
            "ctf_fit_resolution",
            "symmetry",
            "gpu_num",
        ];
        return target_parameters_list;
    }
    else if (preset_type == "simpler") {
        target_parameters_list = [
            "cryosparc_lane",
            "slurm",
            "inference_gpu_ids",
            "movies_data_path",
            "gain_reference_path",
            "micrographs_data_path",
            "particles_data_path",
            "particles_meta_path",
            "source_movie_job_uid",
            "source_micrograph_job_uid",
            "source_particle_job_uid",
            "accelerating_voltage",
            "spherical_aberration",
            "total_exposure_dose",
            "raw_pixel_size",
            "particle_diameter",
            "ctf_fit_resolution",
            "symmetry",
            "gpu_num",
        ];
        return target_parameters_list;
    }
    else if (preset_type == "cryoranker_only") {
        target_parameters_list = [
            "cryosparc_lane",
            "slurm",
            "inference_gpu_ids",
            "movies_data_path",
            "gain_reference_path",
            "micrographs_data_path",
            "particles_data_path",
            "particles_meta_path",
            "source_movie_job_uid",
            "source_micrograph_job_uid",
            "source_particle_job_uid",
            "accelerating_voltage",
            "spherical_aberration",
            "total_exposure_dose",
            "raw_pixel_size",
            "particle_diameter",
            "ctf_fit_resolution",
            "gpu_num",
        ];
        return target_parameters_list;
    }
    else if (preset_type == "cryoranker_get_top_particles") {
        target_parameters_list = [
            "cryosparc_lane",
            "slurm",
            "inference_gpu_ids",
            "source_cryoranker_job_uid",
            "get_top_particles_num",
            "get_top_particles_score",
        ];
        return target_parameters_list;
    }
    else if (preset_type == "custom") {
        target_parameters_list = [
            "cryosparc_lane",
            "slurm",
            "inference_gpu_ids",
        ];
        return target_parameters_list;
    }
    else
    {
        return null;
    }
}


function CreateSessionStorageProjectCardInfo(if_activate=true)
{
    var new_project_card_item = {
        "cryosparc_username": null,
        "cryosparc_password": null,
        "project": null,
        "workspace": null,
        "cryowizard_job_uid": null,
        "gui_info": {
            "cryowizard_job_part_disable_flag": null,
            "cryowizard_pipeline_part_disable_flag": null,
            "cryowizard_output_part_disable_flag": null
        },
        "pipeline_parameters": {
            "create_preset_pipeline_value": null,
            "create_pipeline_node_value": null
        }
    };

    var project_card_count = GetSessionStorageJsonItem("project_card_count");
    var project_card_dict = GetSessionStorageJsonItem("project_card_dict");
    var new_workflow_name = null;
    for (var i = 0; i < 9999; ++i)
    {
        project_card_count += 1;
        new_workflow_name = "Workflow-" + String(project_card_count);
        if (!(new_workflow_name in project_card_dict["project_card_info"]))
        {
            if (if_activate)
            {
                project_card_dict["active_workflow"] = new_workflow_name;
            }
            project_card_dict["project_card_info"][new_workflow_name] = new_project_card_item;
            SetSessionStorageJsonItem("project_card_count", project_card_count);
            SetSessionStorageJsonItem("project_card_dict", project_card_dict);
            CryoWizardJobPartEditButtonAction(new_workflow_name);
            return new_workflow_name;
        }
    }
}


function DeleteSessionStorageProjectCardInfo(workflow_name)
{
    var project_card_dict = GetSessionStorageJsonItem("project_card_dict");
    try
    {
        delete project_card_dict["project_card_info"][workflow_name];
        SetSessionStorageJsonItem("project_card_dict", project_card_dict);
        return true;
    }
    catch
    {
        return false;
    }
}


// create html project card elements (including show saved parameters)
function CreateProjectCardElements(new_workflow_name)
{
    var project_card_dict = GetSessionStorageJsonItem("project_card_dict");
    var project_card_workflow_info = project_card_dict["project_card_info"][new_workflow_name];
    var project_card_active_workflow = project_card_dict["active_workflow"];

    var active_class = "";
    if (project_card_active_workflow == new_workflow_name)
    {
        active_class = " active";
    }

    var new_project_card_content_nav = `
        <li onclick="UpdateProjectCard('` + new_workflow_name + `')">
            <a href="#` + new_workflow_name + `" class="nav-link text-white` + active_class + `" data-bs-toggle="tab">
                <div class="btn-group m-0 p-0">
                    <button type="button" class="btn text-white" style="width: 150px; text-align: left">` + new_workflow_name + `</button>
                    <button type="button" class="btn text-white" style="width: 40px" onclick="DeleteProjectCard('` + new_workflow_name + `');"><i class="bi bi-trash"></i></button>
                </div>
            </a>
        </li>`;
    var new_project_card_content_tab = `
        <div class="tab-pane container` + active_class + ` w-100 h-100" id="` + new_workflow_name + `">
            <!-- cryowizard job -->
            <div class="row w-100 m-0 p-0">
                <div class="col mb-3 mt-3">
                    <div class="mb-3">
                        <label for="` + new_workflow_name + `_cryosparc_username" class="form-label col-form-label-sm">CryoSPARC Username</label>
                        <div class="m-0 p-0">
                            <input type="text" class="form-control form-control-sm" id="` + new_workflow_name + `_cryosparc_username" placeholder="Enter CryoSPARC username" name="` + new_workflow_name + `_cryosparc_username">
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="` + new_workflow_name + `_cryosparc_password" class="form-label col-form-label-sm">CryoSPARC Password</label>
                        <div class="m-0 p-0">
                            <input type="password" class="form-control form-control-sm" id="` + new_workflow_name + `_cryosparc_password" placeholder="Enter CryoSPARC password" name="` + new_workflow_name + `_cryosparc_password">
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="` + new_workflow_name + `_cryowizard_project" class="form-label col-form-label-sm">CryoWizard Project</label>
                        <div class="m-0 p-0">
                            <input type="text" class="form-control form-control-sm" id="` + new_workflow_name + `_cryowizard_project" placeholder="Enter CryoSPARC project where CryoWizard job is located, e.g. P1" name="` + new_workflow_name + `_cryowizard_project">
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="` + new_workflow_name + `_cryowizard_workspace" class="form-label col-form-label-sm">CryoWizard Workspace</label>
                        <div class="m-0 p-0">
                            <input type="text" class="form-control form-control-sm" id="` + new_workflow_name + `_cryowizard_workspace" placeholder="Enter CryoSPARC workspace where CryoWizard job is located, e.g. W1" name="` + new_workflow_name + `_cryowizard_workspace">
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="` + new_workflow_name + `_cryowizard_jobuid" class="form-label col-form-label-sm">CryoWizard Job</label>
                        <div class="m-0 p-0">
                            <input type="text" class="form-control form-control-sm" id="` + new_workflow_name + `_cryowizard_jobuid" placeholder="Enter CryoWizard job id, e.g. J1" name="` + new_workflow_name + `_cryowizard_jobuid">
                        </div>
                    </div>
                    <br>
                    <div class="row m-0 p-0">
                        <button type="button" class="col btn btn-primary btn-sm" id="` + new_workflow_name + `_edit_cryowizard_job_info" onclick="CryoWizardJobPartEditButtonAction('` + new_workflow_name + `')">Edit CryoWizard Job Info</button>
                        <button type="button" class="col btn btn-primary btn-sm" id="` + new_workflow_name + `_create_cryowizard_job_info" onclick="CryoWizardJobPartCreateButtonAction('` + new_workflow_name + `')">Create New CryoWizard Job</button>
                        <button type="button" class="col btn btn-primary btn-sm" id="` + new_workflow_name + `_save_cryowizard_job_info" onclick="CryoWizardJobPartSaveButtonAction('` + new_workflow_name + `')">Connect to CryoWizard Job</button>
                    </div>
                </div>
            </div>
            <br>
            <hr>
            <br>
            <!-- cryowizard pipeline info -->
            <div class="row w-100 m-0 p-0">
                <div class="col mb-3 mt-3">
                    <div class="mb-3">
                        <label class="form-label col-form-label-sm">CryoWizard Pipeline</label>
                        <div class="row w-100 m-0 p-0">
                            <div class="col bg-light border border-1 rounded rounded-5 w-100 m-0 p-3 overflow-auto" style="height: 1000px;" id="` + new_workflow_name + `_pipeline_panel"></div>
                            <div class="col-md-1 m-0 p-0"></div>
                            <div class="col-md-3 m-0 p-0">
                                <label class="form-label col-form-label-sm">Create Preset Pipeline</label>
                                <div class="w-100 m-0 p-0">
                                    <select class="form-select" id="` + new_workflow_name + `_preset_pipeline_choose">
                                        <option value="default">` + PipelinePresetTypeNameChange("default") + `</option>
                                        <option value="simpler">` + PipelinePresetTypeNameChange("simpler") + `</option>
                                        <option value="cryoranker_only">` + PipelinePresetTypeNameChange("cryoranker_only") + `</option>
                                        <option value="cryoranker_get_top_particles">` + PipelinePresetTypeNameChange("cryoranker_get_top_particles") + `</option>
                                        <option value="custom">` + PipelinePresetTypeNameChange("custom") + `</option>
                                    </select>
                                </div>
                                <div class="w-100 m-0 p-0">
                                    <button type="button" class="w-100 btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#` + new_workflow_name + `_create_preset_pipeline_modal" id="` + new_workflow_name + `_create_preset_pipeline_create_button" onclick="AddPresetPipelineCreateButtonOnclick('` + new_workflow_name + `')">Create</button>
                                </div>
                                <div class="modal fade" id="` + new_workflow_name + `_create_preset_pipeline_modal">
                                    <div class="modal-dialog modal-lg">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <h4 class="modal-title">Modify Preset Pipeline Parameters</h4>
                                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                                            </div>
                                            <div class="modal-body" id="` + new_workflow_name + `_create_preset_pipeline_parameters_div"></div>
                                            <div class="modal-footer">
                                                <button type="button" class="btn btn-primary" data-bs-dismiss="modal" onclick="AddPresetPipeline('` + new_workflow_name + `')">Create Pipeline</button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <br>
                                <label class="form-label col-form-label-sm">Create Single Pipeline Node</label>
                                <div class="w-100 m-0 p-0">
                                    <select class="form-select" id="` + new_workflow_name + `_pipeline_block_choose">
                                        <option value="import_movie_file_parameters">` + SinglePipelineNodeNameChange("import_movie_file_parameters") + `</option>
                                        <option value="import_micrograph_file_parameters">` + SinglePipelineNodeNameChange("import_micrograph_file_parameters") + `</option>
                                        <option value="import_particle_file_parameters">` + SinglePipelineNodeNameChange("import_particle_file_parameters") + `</option>
                                        <option value="import_volume_file_parameters">` + SinglePipelineNodeNameChange("import_volume_file_parameters") + `</option>
                                        <option value="preprocess_movie_with_blob_pick_parameters">` + SinglePipelineNodeNameChange("preprocess_movie_with_blob_pick_parameters") + `</option>
                                        <option value="preprocess_movie_with_template_pick_parameters">` + SinglePipelineNodeNameChange("preprocess_movie_with_template_pick_parameters") + `</option>
                                        <option value="preprocess_micrograph_with_blob_pick_parameters">` + SinglePipelineNodeNameChange("preprocess_micrograph_with_blob_pick_parameters") + `</option>
                                        <option value="preprocess_micrograph_with_template_pick_parameters">` + SinglePipelineNodeNameChange("preprocess_micrograph_with_template_pick_parameters") + `</option>
                                        <option value="preprocess_particle_parameters">` + SinglePipelineNodeNameChange("preprocess_particle_parameters") + `</option>
                                        <option value="create_templates_parameters">` + SinglePipelineNodeNameChange("create_templates_parameters") + `</option>
                                        <option value="reference_based_auto_select_2d">` + SinglePipelineNodeNameChange("reference_based_auto_select_2d") + `</option>
                                        <option value="junk_detector">` + SinglePipelineNodeNameChange("junk_detector") + `</option>
                                        <option value="cryoranker_parameters">` + SinglePipelineNodeNameChange("cryoranker_parameters") + `</option>
                                        <option value="get_top_particles">` + SinglePipelineNodeNameChange("get_top_particles") + `</option>
                                        <option value="refine_parameters">` + SinglePipelineNodeNameChange("refine_parameters") + `</option>
                                        <option value="motion_and_ctf_refine_parameters">` + SinglePipelineNodeNameChange("motion_and_ctf_refine_parameters") + `</option>
                                    </select>
                                </div>
                                <div class="w-100 m-0 p-0">
                                    <button type="button" class="w-100 btn btn-primary btn-sm" id="` + new_workflow_name + `_create_pipeline_block_create_button" onclick="AddPipelineNode('` + new_workflow_name + `')">Create</button>
                                </div>
                                <br>
                                <label class="form-label col-form-label-sm">Modify Pipeline Base Parameters</label>
                                <div class="w-100 m-0 p-0">
                                    <button type="button" class="w-100 btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#` + new_workflow_name + `_modify_base_parameters_modal" id="` + new_workflow_name + `_modify_base_parameters">Modify Base Parameters</button>
                                </div>
                                <div class="modal fade" id="` + new_workflow_name + `_modify_base_parameters_modal">
                                    <div class="modal-dialog modal-lg">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <h4 class="modal-title">Modify Base Parameters</h4>
                                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                                            </div>
                                            <div class="modal-body" id="` + new_workflow_name + `_modify_base_parameters_modal_div"></div>
                                            <div class="modal-footer">
                                                <button type="button" class="btn btn-primary" data-bs-dismiss="modal" onclick="PipelineNodeSaveParameters('` + new_workflow_name + `', 'base_parameters', ['cryosparc_lane', 'slurm', 'inference_gpu_ids'])">Save</button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <br>
                                <label class="form-label col-form-label-sm">Used Pipeline Parameters</label>
                                <div class="w-100 m-0 p-0" id="` + new_workflow_name + `_used_pipeline_parameters_show"></div>
                            </div>
                        </div>
                    </div>
                    <br>
                    <div class="row m-0 p-0">
                        <button type="button" class="col btn btn-primary btn-sm" id="` + new_workflow_name + `_edit_cryowizard_pipeline" onclick="CryoWizardPipelinePartEditButtonAction('` + new_workflow_name + `')">Edit CryoWizard Pipeline</button>
                        <button type="button" class="col btn btn-primary btn-sm" id="` + new_workflow_name + `_save_cryowizard_pipeline" onclick="CryoWizardPipelinePartSaveButtonAction('` + new_workflow_name + `')">Save CryoWizard Pipeline</button>
                    </div>
                </div>
            </div>
            <br>
            <hr>
            <br>
            <!-- output panel -->
            <div class="row w-100 m-0 p-0">
                <div class="col mb-3 mt-3">
                    <div class="mb-3">
                        <label class="form-label col-form-label-sm">Output Panel</label>
                        <div class="row w-100 m-0 p-0">
                            <div class="col bg-dark text-white w-100 m-0 p-3 overflow-auto" style="height: 800px;" id="` + new_workflow_name + `_output_panel"></div>
                            <div class="col-md-1 m-0 p-0"></div>
                            <div class="col-md-3 m-0 p-0">
                                <div class="row w-100 m-0 p-0"><button type="button" class="col btn btn-primary btn-sm" id="` + new_workflow_name + `_result_panel_run" onclick="RunCryoWizardJob('` + new_workflow_name + `')">Run</button></div>
                                <br>
                                <div class="row w-100 m-0 p-0"><button type="button" class="col btn btn-primary btn-sm" id="` + new_workflow_name + `_result_panel_continue" onclick="ContinueCryoWizardJob('` + new_workflow_name + `')">Continue</button></div>
                                <br>
                                <div class="row w-100 m-0 p-0"><button type="button" class="col btn btn-primary btn-sm" id="` + new_workflow_name + `_result_panel_kill" onclick="KillCryoWizardJob('` + new_workflow_name + `')">Kill</button></div>
                                <br>
                                <div class="row w-100 m-0 p-0"><button type="button" class="col btn btn-primary btn-sm" id="` + new_workflow_name + `_result_panel_clear" onclick="ClearCryoWizardMetadata('` + new_workflow_name + `')">Clear</button></div>
                                <br>
                                <div class="row w-100 m-0 p-0"><button type="button" class="col btn btn-primary btn-sm" id="` + new_workflow_name + `_result_panel_download_map" onclick="DownloadCryoWizardFinalVolume('` + new_workflow_name + `')">Download Map</button></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>`;

    return {"new_project_card_content_nav_str": new_project_card_content_nav, "new_project_card_content_tab_str": new_project_card_content_tab};
}


function CryoWizardJobPartEditButtonAction(target_workflow_name)
{
    var project_card_dict = GetSessionStorageJsonItem("project_card_dict");
    project_card_dict["project_card_info"][target_workflow_name]["gui_info"]["cryowizard_job_part_disable_flag"] = false;
    project_card_dict["project_card_info"][target_workflow_name]["gui_info"]["cryowizard_pipeline_part_disable_flag"] = true;
    project_card_dict["project_card_info"][target_workflow_name]["gui_info"]["cryowizard_output_part_disable_flag"] = true;
    SetSessionStorageJsonItem("project_card_dict", project_card_dict);
    UpdateProjectCard(target_workflow_name);
}


function CryoWizardJobPartCreateButtonAction(target_workflow_name)
{
    var project_card_dict = GetSessionStorageJsonItem("project_card_dict");
    project_card_dict["project_card_info"][target_workflow_name]["cryosparc_username"] = document.getElementById(target_workflow_name + "_cryosparc_username").value;
    project_card_dict["project_card_info"][target_workflow_name]["cryosparc_password"] = document.getElementById(target_workflow_name + "_cryosparc_password").value;
    project_card_dict["project_card_info"][target_workflow_name]["project"] = document.getElementById(target_workflow_name + "_cryowizard_project").value;
    project_card_dict["project_card_info"][target_workflow_name]["workspace"] = document.getElementById(target_workflow_name + "_cryowizard_workspace").value;
    project_card_dict["project_card_info"][target_workflow_name]["gui_info"]["cryowizard_job_part_disable_flag"] = false;
    project_card_dict["project_card_info"][target_workflow_name]["gui_info"]["cryowizard_pipeline_part_disable_flag"] = true;
    project_card_dict["project_card_info"][target_workflow_name]["gui_info"]["cryowizard_output_part_disable_flag"] = true;
    SetSessionStorageJsonItem("project_card_dict", project_card_dict);
    UpdateProjectCard(target_workflow_name);

    var cryosparc_username = document.getElementById(target_workflow_name + "_cryosparc_username").value;
    var cryosparc_password = document.getElementById(target_workflow_name + "_cryosparc_password").value;
    var cryosparc_project = document.getElementById(target_workflow_name + "_cryowizard_project").value;
    var cryosparc_workspace = document.getElementById(target_workflow_name + "_cryowizard_workspace").value;
    document.getElementById(target_workflow_name + "_create_cryowizard_job_info").innerHTML = "Creating...";
    document.getElementById(target_workflow_name + "_create_cryowizard_job_info").disabled = true;
    WebCreateCryowizardExternalJobAction(socket, target_workflow_name, cryosparc_username, cryosparc_password, cryosparc_project, cryosparc_workspace);
}


function CryoWizardJobPartSaveButtonAction(target_workflow_name)
{
    var project_card_dict = GetSessionStorageJsonItem("project_card_dict");
    project_card_dict["project_card_info"][target_workflow_name]["cryosparc_username"] = document.getElementById(target_workflow_name + "_cryosparc_username").value;
    project_card_dict["project_card_info"][target_workflow_name]["cryosparc_password"] = document.getElementById(target_workflow_name + "_cryosparc_password").value;
    project_card_dict["project_card_info"][target_workflow_name]["project"] = document.getElementById(target_workflow_name + "_cryowizard_project").value;
    project_card_dict["project_card_info"][target_workflow_name]["workspace"] = document.getElementById(target_workflow_name + "_cryowizard_workspace").value;
    project_card_dict["project_card_info"][target_workflow_name]["cryowizard_job_uid"] = document.getElementById(target_workflow_name + "_cryowizard_jobuid").value;
    project_card_dict["project_card_info"][target_workflow_name]["gui_info"]["cryowizard_job_part_disable_flag"] = true;
    project_card_dict["project_card_info"][target_workflow_name]["gui_info"]["cryowizard_pipeline_part_disable_flag"] = false;
    project_card_dict["project_card_info"][target_workflow_name]["gui_info"]["cryowizard_output_part_disable_flag"] = true;
    SetSessionStorageJsonItem("project_card_dict", project_card_dict);
    UpdateProjectCard(target_workflow_name);

    var cryosparc_username = document.getElementById(target_workflow_name + "_cryosparc_username").value;
    var cryosparc_password = document.getElementById(target_workflow_name + "_cryosparc_password").value;
    var cryosparc_project = document.getElementById(target_workflow_name + "_cryowizard_project").value;
    var cryowizard_job_uid = document.getElementById(target_workflow_name + "_cryowizard_jobuid").value;
    document.getElementById(target_workflow_name + "_save_cryowizard_job_info").innerHTML = "Connecting...";
    document.getElementById(target_workflow_name + "_save_cryowizard_job_info").disabled = true;
    WebCheckCryowizardExternalJobExistenceAction(socket, target_workflow_name, cryosparc_username, cryosparc_password, cryosparc_project, cryowizard_job_uid);
}


function CryoWizardPipelinePartEditButtonAction(target_workflow_name)
{
    var project_card_dict = GetSessionStorageJsonItem("project_card_dict");
    project_card_dict["project_card_info"][target_workflow_name]["gui_info"]["cryowizard_job_part_disable_flag"] = true;
    project_card_dict["project_card_info"][target_workflow_name]["gui_info"]["cryowizard_pipeline_part_disable_flag"] = false;
    project_card_dict["project_card_info"][target_workflow_name]["gui_info"]["cryowizard_output_part_disable_flag"] = true;
    SetSessionStorageJsonItem("project_card_dict", project_card_dict);
    UpdateProjectCard(target_workflow_name);
}


function CryoWizardPipelinePartSaveButtonAction(target_workflow_name)
{
    var project_card_dict = GetSessionStorageJsonItem("project_card_dict");
    project_card_dict["project_card_info"][target_workflow_name]["gui_info"]["cryowizard_job_part_disable_flag"] = true;
    project_card_dict["project_card_info"][target_workflow_name]["gui_info"]["cryowizard_pipeline_part_disable_flag"] = true;
    project_card_dict["project_card_info"][target_workflow_name]["gui_info"]["cryowizard_output_part_disable_flag"] = false;
    SetSessionStorageJsonItem("project_card_dict", project_card_dict);
    UpdateProjectCard(target_workflow_name);
}


function UpdateProjectCardElementsValue(target_workflow_name)
{
    var project_card_dict = GetSessionStorageJsonItem("project_card_dict");
    var project_card_workflow_info = project_card_dict["project_card_info"][target_workflow_name];
    var project_card_active_workflow = project_card_dict["active_workflow"];

    if (project_card_workflow_info["gui_info"]["cryowizard_job_part_disable_flag"])
    {
        document.getElementById(target_workflow_name + "_cryosparc_username").disabled = true;
        document.getElementById(target_workflow_name + "_cryosparc_password").disabled = true;
        document.getElementById(target_workflow_name + "_cryowizard_project").disabled = true;
        document.getElementById(target_workflow_name + "_cryowizard_workspace").disabled = true;
        document.getElementById(target_workflow_name + "_cryowizard_jobuid").disabled = true;
        document.getElementById(target_workflow_name + "_edit_cryowizard_job_info").disabled = false;
        document.getElementById(target_workflow_name + "_create_cryowizard_job_info").disabled = true;
        document.getElementById(target_workflow_name + "_save_cryowizard_job_info").disabled = true;
    }
    else
    {
        document.getElementById(target_workflow_name + "_cryosparc_username").disabled = false;
        document.getElementById(target_workflow_name + "_cryosparc_password").disabled = false;
        document.getElementById(target_workflow_name + "_cryowizard_project").disabled = false;
        document.getElementById(target_workflow_name + "_cryowizard_workspace").disabled = false;
        document.getElementById(target_workflow_name + "_cryowizard_jobuid").disabled = false;
        document.getElementById(target_workflow_name + "_edit_cryowizard_job_info").disabled = true;
        document.getElementById(target_workflow_name + "_create_cryowizard_job_info").disabled = false;
        document.getElementById(target_workflow_name + "_save_cryowizard_job_info").disabled = false;
    }

    if (project_card_workflow_info["gui_info"]["cryowizard_pipeline_part_disable_flag"])
    {
        document.getElementById(target_workflow_name + "_preset_pipeline_choose").disabled = true;
        document.getElementById(target_workflow_name + "_create_preset_pipeline_create_button").disabled = true;
        document.getElementById(target_workflow_name + "_pipeline_block_choose").disabled = true;
        document.getElementById(target_workflow_name + "_create_pipeline_block_create_button").disabled = true;
        document.getElementById(target_workflow_name + "_modify_base_parameters").disabled = true;
        document.getElementById(target_workflow_name + "_edit_cryowizard_pipeline").disabled = false;
        document.getElementById(target_workflow_name + "_save_cryowizard_pipeline").disabled = true;
        CheckPipelineNodes(target_workflow_name, true);
        project_card_dict = GetSessionStorageJsonItem("project_card_dict");
        project_card_workflow_info = project_card_dict["project_card_info"][target_workflow_name];
        project_card_active_workflow = project_card_dict["active_workflow"];
    }
    else
    {
        document.getElementById(target_workflow_name + "_preset_pipeline_choose").disabled = false;
        document.getElementById(target_workflow_name + "_create_preset_pipeline_create_button").disabled = false;
        document.getElementById(target_workflow_name + "_pipeline_block_choose").disabled = false;
        document.getElementById(target_workflow_name + "_create_pipeline_block_create_button").disabled = false;
        document.getElementById(target_workflow_name + "_modify_base_parameters").disabled = false;
        document.getElementById(target_workflow_name + "_edit_cryowizard_pipeline").disabled = true;
        document.getElementById(target_workflow_name + "_save_cryowizard_pipeline").disabled = false;
        CheckPipelineNodes(target_workflow_name, false);
        project_card_dict = GetSessionStorageJsonItem("project_card_dict");
        project_card_workflow_info = project_card_dict["project_card_info"][target_workflow_name];
        project_card_active_workflow = project_card_dict["active_workflow"];
    }

    if (project_card_workflow_info["gui_info"]["cryowizard_output_part_disable_flag"])
    {
        document.getElementById(target_workflow_name + "_result_panel_run").disabled = true;
        document.getElementById(target_workflow_name + "_result_panel_continue").disabled = true;
        document.getElementById(target_workflow_name + "_result_panel_kill").disabled = true;
        document.getElementById(target_workflow_name + "_result_panel_clear").disabled = true;
        document.getElementById(target_workflow_name + "_result_panel_download_map").disabled = true;
    }
    else
    {
        document.getElementById(target_workflow_name + "_result_panel_run").disabled = false;
        document.getElementById(target_workflow_name + "_result_panel_continue").disabled = false;
        document.getElementById(target_workflow_name + "_result_panel_kill").disabled = false;
        document.getElementById(target_workflow_name + "_result_panel_clear").disabled = false;
        document.getElementById(target_workflow_name + "_result_panel_download_map").disabled = false;
    }


    if (project_card_workflow_info["cryosparc_username"] != null)
    {
        document.getElementById(target_workflow_name + "_cryosparc_username").value = project_card_workflow_info["cryosparc_username"];
    }
    if (project_card_workflow_info["cryosparc_password"] != null)
    {
        document.getElementById(target_workflow_name + "_cryosparc_password").value = project_card_workflow_info["cryosparc_password"];
    }
    if (project_card_workflow_info["project"] != null)
    {
        document.getElementById(target_workflow_name + "_cryowizard_project").value = project_card_workflow_info["project"];
    }
    if (project_card_workflow_info["workspace"] != null)
    {
        document.getElementById(target_workflow_name + "_cryowizard_workspace").value = project_card_workflow_info["workspace"];
    }
    if (project_card_workflow_info["cryowizard_job_uid"] != null)
    {
        document.getElementById(target_workflow_name + "_cryowizard_jobuid").value = project_card_workflow_info["cryowizard_job_uid"];
    }

    if (project_card_workflow_info["pipeline_parameters"]["create_preset_pipeline_value"] != null)
    {
        document.getElementById(target_workflow_name + "_preset_pipeline_choose").value = project_card_workflow_info["pipeline_parameters"]["create_preset_pipeline_value"];
    }
    if (project_card_workflow_info["pipeline_parameters"]["create_pipeline_node_value"] != null)
    {
        document.getElementById(target_workflow_name + "_pipeline_block_choose").value = project_card_workflow_info["pipeline_parameters"]["create_pipeline_node_value"];
    }


}


function AddPresetPipelineCreateButtonOnclick(target_workflow_name)
{
    var project_card_dict = GetSessionStorageJsonItem("project_card_dict");
    var cryosparc_username = project_card_dict["project_card_info"][target_workflow_name]["cryosparc_username"];
    var cryosparc_password = project_card_dict["project_card_info"][target_workflow_name]["cryosparc_password"];
    var cryosparc_project = project_card_dict["project_card_info"][target_workflow_name]["project"];
    var cryosparc_workspace = project_card_dict["project_card_info"][target_workflow_name]["workspace"];
    var cryowizard_job_uid = project_card_dict["project_card_info"][target_workflow_name]["cryowizard_job_uid"];

    if (
        (cryosparc_username != null) &&
        (cryosparc_username.length > 0) &&
        (cryosparc_password != null) &&
        (cryosparc_password.length > 0) &&
        (cryosparc_project != null) &&
        (cryosparc_project.length > 0) &&
        (cryosparc_workspace != null) &&
        (cryosparc_workspace.length > 0) &&
        (cryowizard_job_uid != null) &&
        (cryowizard_job_uid.length > 0)
    )
    {
        var preset_pipeline_type = document.getElementById(target_workflow_name + "_preset_pipeline_choose").value;

        const parser = new DOMParser();

        var create_preset_pipeline_parameters_div = document.getElementById(target_workflow_name + "_create_preset_pipeline_parameters_div");
        create_preset_pipeline_parameters_div.replaceChildren();

        var create_preset_pipeline_parameters_div_single_parameter_str = null;
        var create_preset_pipeline_parameters_div_single_parameter_doc = null;
        var create_preset_pipeline_parameters_div_single_parameter = null;
        var target_parameters_list = PipelinePresetParametersList(preset_pipeline_type);
        for (var i = 0; i < target_parameters_list.length; ++i) {
            create_preset_pipeline_parameters_div_single_parameter_str = `
            <div class="row m-0 p-1">
                <div class="col m-0 p-0 text-nowrap overflow-hidden">` + PipelineParametersNameChange(target_parameters_list[i]) + `:</div>
                <div class="col m-0 p-0">
                    <input type="text" class="form-control form-control-sm" id="` + target_workflow_name + "_" + target_parameters_list[i] + `"  placeholder="Loading..." disabled>
                </div>
            </div>`;
            create_preset_pipeline_parameters_div_single_parameter_doc = parser.parseFromString(create_preset_pipeline_parameters_div_single_parameter_str, "text/html");
            create_preset_pipeline_parameters_div_single_parameter = create_preset_pipeline_parameters_div_single_parameter_doc.body.firstElementChild;
            create_preset_pipeline_parameters_div.appendChild(create_preset_pipeline_parameters_div_single_parameter);
        }

        WebCheckPresetPipelineInfoAction(socket, target_workflow_name, cryosparc_username, cryosparc_password, cryosparc_project, cryosparc_workspace, cryowizard_job_uid, preset_pipeline_type);
    }
}


function AddPresetPipeline(target_workflow_name)
{
    var project_card_dict = GetSessionStorageJsonItem("project_card_dict");
    var cryosparc_username = project_card_dict["project_card_info"][target_workflow_name]["cryosparc_username"];
    var cryosparc_password = project_card_dict["project_card_info"][target_workflow_name]["cryosparc_password"];
    var cryosparc_project = project_card_dict["project_card_info"][target_workflow_name]["project"];
    var cryosparc_workspace = project_card_dict["project_card_info"][target_workflow_name]["workspace"];
    var cryowizard_job_uid = project_card_dict["project_card_info"][target_workflow_name]["cryowizard_job_uid"];

    if (
        (cryosparc_username != null) &&
        (cryosparc_username.length > 0) &&
        (cryosparc_password != null) &&
        (cryosparc_password.length > 0) &&
        (cryosparc_project != null) &&
        (cryosparc_project.length > 0) &&
        (cryosparc_workspace != null) &&
        (cryosparc_workspace.length > 0) &&
        (cryowizard_job_uid != null) &&
        (cryowizard_job_uid.length > 0)
    )
    {
        var preset_pipeline_type = document.getElementById(target_workflow_name + "_preset_pipeline_choose").value;
        var target_parameters_list = PipelinePresetParametersList(preset_pipeline_type);

        var preset_pipeline_parameters = {}
        var single_preset_pipeline_parameter_value = null;
        for (var i = 0; i < target_parameters_list.length; ++i) {
            single_preset_pipeline_parameter_value = document.getElementById(target_workflow_name + "_" + target_parameters_list[i]).value;
            if ((single_preset_pipeline_parameter_value != null) && (single_preset_pipeline_parameter_value.length > 0)) {
                preset_pipeline_parameters[target_parameters_list[i]] = single_preset_pipeline_parameter_value;
            } else {
                preset_pipeline_parameters[target_parameters_list[i]] = null;
            }
        }

        WebAddPresetPipelineAction(socket, target_workflow_name, cryosparc_username, cryosparc_password, cryosparc_project, cryosparc_workspace, cryowizard_job_uid, preset_pipeline_type, preset_pipeline_parameters);

        document.getElementById(target_workflow_name + "_create_preset_pipeline_create_button").innerHTML = "Creating...";
        document.getElementById(target_workflow_name + "_create_preset_pipeline_create_button").disabled = true;
        document.getElementById(target_workflow_name + "_preset_pipeline_choose").disabled = true;
    }
}


function AddPipelineNode(target_workflow_name)
{
    var project_card_dict = GetSessionStorageJsonItem("project_card_dict");
    var cryosparc_username = project_card_dict["project_card_info"][target_workflow_name]["cryosparc_username"];
    var cryosparc_password = project_card_dict["project_card_info"][target_workflow_name]["cryosparc_password"];
    var cryosparc_project = project_card_dict["project_card_info"][target_workflow_name]["project"];
    // var cryosparc_workspace = project_card_dict["project_card_info"][target_workflow_name]["workspace"];
    var cryowizard_job_uid = project_card_dict["project_card_info"][target_workflow_name]["cryowizard_job_uid"];

    if (
        (cryosparc_username != null) &&
        (cryosparc_username.length > 0) &&
        (cryosparc_password != null) &&
        (cryosparc_password.length > 0) &&
        (cryosparc_project != null) &&
        (cryosparc_project.length > 0) &&
        (cryowizard_job_uid != null) &&
        (cryowizard_job_uid.length > 0)
    )
    {
        var pipeline_node_type = document.getElementById(target_workflow_name + "_pipeline_block_choose").value;

        WebAddSinglePipelineNodeAction(socket, target_workflow_name, cryosparc_username, cryosparc_password, cryosparc_project, cryowizard_job_uid, pipeline_node_type);

        document.getElementById(target_workflow_name + "_create_pipeline_block_create_button").innerHTML = "Creating...";
        document.getElementById(target_workflow_name + "_create_pipeline_block_create_button").disabled = true;
        document.getElementById(target_workflow_name + "_pipeline_block_choose").disabled = true;
    }
}


function DeletePipelineNode(target_workflow_name, target_pipeline_node_name)
{
    var project_card_dict = GetSessionStorageJsonItem("project_card_dict");
    var cryosparc_username = project_card_dict["project_card_info"][target_workflow_name]["cryosparc_username"];
    var cryosparc_password = project_card_dict["project_card_info"][target_workflow_name]["cryosparc_password"];
    var cryosparc_project = project_card_dict["project_card_info"][target_workflow_name]["project"];
    // var cryosparc_workspace = project_card_dict["project_card_info"][target_workflow_name]["workspace"];
    var cryowizard_job_uid = project_card_dict["project_card_info"][target_workflow_name]["cryowizard_job_uid"];

    if (
        (cryosparc_username != null) &&
        (cryosparc_username.length > 0) &&
        (cryosparc_password != null) &&
        (cryosparc_password.length > 0) &&
        (cryosparc_project != null) &&
        (cryosparc_project.length > 0) &&
        (cryowizard_job_uid != null) &&
        (cryowizard_job_uid.length > 0)
    )
    {
        WebDeleteSinglePipelineNodeAction(socket, target_workflow_name, cryosparc_username, cryosparc_password, cryosparc_project, cryowizard_job_uid, target_pipeline_node_name);

        document.getElementById(target_workflow_name + "_" + target_pipeline_node_name + "_delete_button").innerHTML = "Deleting...";
        document.getElementById(target_workflow_name + "_" + target_pipeline_node_name + "_input_button").disabled = true;
        document.getElementById(target_workflow_name + "_" + target_pipeline_node_name + "_parameter_button").disabled = true;
        document.getElementById(target_workflow_name + "_" + target_pipeline_node_name + "_delete_button").disabled = true;
    }
}


function PipelineNodeSaveParameters(target_workflow_name, target_pipeline_node_name, parameter_names_list)
{
    var project_card_dict = GetSessionStorageJsonItem("project_card_dict");
    var cryosparc_username = project_card_dict["project_card_info"][target_workflow_name]["cryosparc_username"];
    var cryosparc_password = project_card_dict["project_card_info"][target_workflow_name]["cryosparc_password"];
    var cryosparc_project = project_card_dict["project_card_info"][target_workflow_name]["project"];
    // var cryosparc_workspace = project_card_dict["project_card_info"][target_workflow_name]["workspace"];
    var cryowizard_job_uid = project_card_dict["project_card_info"][target_workflow_name]["cryowizard_job_uid"];

    if (
        (cryosparc_username != null) &&
        (cryosparc_username.length > 0) &&
        (cryosparc_password != null) &&
        (cryosparc_password.length > 0) &&
        (cryosparc_project != null) &&
        (cryosparc_project.length > 0) &&
        (cryowizard_job_uid != null) &&
        (cryowizard_job_uid.length > 0)
    )
    {
        var parameters = {};
        var single_parameter_value = null;
        for (var i = 0; i < parameter_names_list.length; ++i)
        {
            single_parameter_value = document.getElementById(target_workflow_name + "_" + target_pipeline_node_name + "_" + parameter_names_list[i]).value;
            if ((single_parameter_value != null) && (single_parameter_value.length > 0))
            {
                parameters[parameter_names_list[i]] = single_parameter_value;
            }
            else
            {
                parameters[parameter_names_list[i]] = null;
            }
        }
        WebPipelineNodeSaveParametersAction(socket, target_workflow_name, cryosparc_username, cryosparc_password, cryosparc_project, cryowizard_job_uid, target_pipeline_node_name, parameters);
    }
}


function CheckPipelineNodes(target_workflow_name, if_disable=false)
{
    var project_card_dict = GetSessionStorageJsonItem("project_card_dict");
    var cryosparc_username = project_card_dict["project_card_info"][target_workflow_name]["cryosparc_username"];
    var cryosparc_password = project_card_dict["project_card_info"][target_workflow_name]["cryosparc_password"];
    var cryosparc_project = project_card_dict["project_card_info"][target_workflow_name]["project"];
    var cryosparc_workspace = project_card_dict["project_card_info"][target_workflow_name]["workspace"];
    var cryowizard_job_uid = project_card_dict["project_card_info"][target_workflow_name]["cryowizard_job_uid"];

    if (
        (cryosparc_username != null) &&
        (cryosparc_username.length > 0) &&
        (cryosparc_password != null) &&
        (cryosparc_password.length > 0) &&
        (cryosparc_project != null) &&
        (cryosparc_project.length > 0) &&
        (cryosparc_workspace != null) &&
        (cryosparc_workspace.length > 0) &&
        (cryowizard_job_uid != null) &&
        (cryowizard_job_uid.length > 0)
    )
    {
        WebCheckPipelineNodesAction(socket, target_workflow_name, cryosparc_username, cryosparc_password, cryosparc_project, cryosparc_workspace, cryowizard_job_uid, if_disable);
    }
}


function RunCryoWizardJob(target_workflow_name)
{
    var project_card_dict = GetSessionStorageJsonItem("project_card_dict");
    var cryosparc_username = project_card_dict["project_card_info"][target_workflow_name]["cryosparc_username"];
    var cryosparc_password = project_card_dict["project_card_info"][target_workflow_name]["cryosparc_password"];
    var cryosparc_project = project_card_dict["project_card_info"][target_workflow_name]["project"];
    // var cryosparc_workspace = project_card_dict["project_card_info"][target_workflow_name]["workspace"];
    var cryowizard_job_uid = project_card_dict["project_card_info"][target_workflow_name]["cryowizard_job_uid"];
    if (
        (cryosparc_username != null) &&
        (cryosparc_username.length > 0) &&
        (cryosparc_password != null) &&
        (cryosparc_password.length > 0) &&
        (cryosparc_project != null) &&
        (cryosparc_project.length > 0) &&
        (cryowizard_job_uid != null) &&
        (cryowizard_job_uid.length > 0)
    )
    {
        WebRunCryowizardExternalJobAction(socket, target_workflow_name, cryosparc_username, cryosparc_password, cryosparc_project, cryowizard_job_uid);
    }
}


function ContinueCryoWizardJob(target_workflow_name)
{
    var project_card_dict = GetSessionStorageJsonItem("project_card_dict");
    var cryosparc_username = project_card_dict["project_card_info"][target_workflow_name]["cryosparc_username"];
    var cryosparc_password = project_card_dict["project_card_info"][target_workflow_name]["cryosparc_password"];
    var cryosparc_project = project_card_dict["project_card_info"][target_workflow_name]["project"];
    // var cryosparc_workspace = project_card_dict["project_card_info"][target_workflow_name]["workspace"];
    var cryowizard_job_uid = project_card_dict["project_card_info"][target_workflow_name]["cryowizard_job_uid"];
    if (
        (cryosparc_username != null) &&
        (cryosparc_username.length > 0) &&
        (cryosparc_password != null) &&
        (cryosparc_password.length > 0) &&
        (cryosparc_project != null) &&
        (cryosparc_project.length > 0) &&
        (cryowizard_job_uid != null) &&
        (cryowizard_job_uid.length > 0)
    )
    {
        WebContinueCryowizardExternalJobAction(socket, target_workflow_name, cryosparc_username, cryosparc_password, cryosparc_project, cryowizard_job_uid);
    }
}


function KillCryoWizardJob(target_workflow_name)
{
    var project_card_dict = GetSessionStorageJsonItem("project_card_dict");
    var cryosparc_username = project_card_dict["project_card_info"][target_workflow_name]["cryosparc_username"];
    var cryosparc_password = project_card_dict["project_card_info"][target_workflow_name]["cryosparc_password"];
    var cryosparc_project = project_card_dict["project_card_info"][target_workflow_name]["project"];
    // var cryosparc_workspace = project_card_dict["project_card_info"][target_workflow_name]["workspace"];
    var cryowizard_job_uid = project_card_dict["project_card_info"][target_workflow_name]["cryowizard_job_uid"];

    if (
        (cryosparc_username != null) &&
        (cryosparc_username.length > 0) &&
        (cryosparc_password != null) &&
        (cryosparc_password.length > 0) &&
        (cryosparc_project != null) &&
        (cryosparc_project.length > 0) &&
        (cryowizard_job_uid != null) &&
        (cryowizard_job_uid.length > 0)
    )
    {
        WebKillCryowizardExternalJobAction(socket, target_workflow_name, cryosparc_username, cryosparc_password, cryosparc_project, cryowizard_job_uid);
    }
}


function ClearCryoWizardMetadata(target_workflow_name)
{
    var project_card_dict = GetSessionStorageJsonItem("project_card_dict");
    var cryosparc_username = project_card_dict["project_card_info"][target_workflow_name]["cryosparc_username"];
    var cryosparc_password = project_card_dict["project_card_info"][target_workflow_name]["cryosparc_password"];
    var cryosparc_project = project_card_dict["project_card_info"][target_workflow_name]["project"];
    // var cryosparc_workspace = project_card_dict["project_card_info"][target_workflow_name]["workspace"];
    var cryowizard_job_uid = project_card_dict["project_card_info"][target_workflow_name]["cryowizard_job_uid"];

    if (
        (cryosparc_username != null) &&
        (cryosparc_username.length > 0) &&
        (cryosparc_password != null) &&
        (cryosparc_password.length > 0) &&
        (cryosparc_project != null) &&
        (cryosparc_project.length > 0) &&
        (cryowizard_job_uid != null) &&
        (cryowizard_job_uid.length > 0)
    )
    {
        WebClearCryowizardExternalJobMetadataAction(socket, target_workflow_name, cryosparc_username, cryosparc_password, cryosparc_project, cryowizard_job_uid);
    }
}


function ShowCryoWizardJobResults()
{
    var project_card_dict = GetSessionStorageJsonItem("project_card_dict");
    var target_workflow_name = project_card_dict["active_workflow"];
    var cryosparc_username = project_card_dict["project_card_info"][target_workflow_name]["cryosparc_username"];
    var cryosparc_password = project_card_dict["project_card_info"][target_workflow_name]["cryosparc_password"];
    var cryosparc_project = project_card_dict["project_card_info"][target_workflow_name]["project"];
    // var cryosparc_workspace = project_card_dict["project_card_info"][target_workflow_name]["workspace"];
    var cryowizard_job_uid = project_card_dict["project_card_info"][target_workflow_name]["cryowizard_job_uid"];

    if (
        (cryosparc_username != null) &&
        (cryosparc_username.length > 0) &&
        (cryosparc_password != null) &&
        (cryosparc_password.length > 0) &&
        (cryosparc_project != null) &&
        (cryosparc_project.length > 0) &&
        (cryowizard_job_uid != null) &&
        (cryowizard_job_uid.length > 0)
    )
    {
        WebShowCryowizardExternalJobResultsAction(socket, target_workflow_name, cryosparc_username, cryosparc_password, cryosparc_project, cryowizard_job_uid);
    }
}


function DownloadCryoWizardFinalVolume(target_workflow_name)
{
    var project_card_dict = GetSessionStorageJsonItem("project_card_dict");
    var cryosparc_username = project_card_dict["project_card_info"][target_workflow_name]["cryosparc_username"];
    var cryosparc_password = project_card_dict["project_card_info"][target_workflow_name]["cryosparc_password"];
    var cryosparc_project = project_card_dict["project_card_info"][target_workflow_name]["project"];
    // var cryosparc_workspace = project_card_dict["project_card_info"][target_workflow_name]["workspace"];
    var cryowizard_job_uid = project_card_dict["project_card_info"][target_workflow_name]["cryowizard_job_uid"];

    if (
        (cryosparc_username != null) &&
        (cryosparc_username.length > 0) &&
        (cryosparc_password != null) &&
        (cryosparc_password.length > 0) &&
        (cryosparc_project != null) &&
        (cryosparc_project.length > 0) &&
        (cryowizard_job_uid != null) &&
        (cryowizard_job_uid.length > 0)
    )
    {
        var download_map_url = window.location.href + "/DownloadMap?username=" + cryosparc_username + "&password=" + cryosparc_password + "&project=" + cryosparc_project + "&jobuid=" + cryowizard_job_uid;
        window.open(download_map_url);
    }
}

