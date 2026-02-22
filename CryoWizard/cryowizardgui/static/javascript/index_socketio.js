

// create cryowizard external job action
function WebCreateCryowizardExternalJobAction(socket, target_workflow_name, cryosparc_username, cryosparc_password, project, workspace)
{
    socket.emit("web_create_cryowizard_external_job_action", target_workflow_name, cryosparc_username, cryosparc_password, project, workspace);

    // create cryowizard external job action backinfo
    socket.once("js_web_create_cryowizard_external_job_action_" + target_workflow_name, (res) => {
        var new_cryowizard_jobid = res["new_cryowizard_jobid"];

        var project_card_dict = GetSessionStorageJsonItem("project_card_dict");
        project_card_dict["project_card_info"][target_workflow_name]["cryowizard_job_uid"] = new_cryowizard_jobid;
        SetSessionStorageJsonItem("project_card_dict", project_card_dict);
        UpdateProjectCard(target_workflow_name);
    });
}


// check cryowizard external job existence action
function WebCheckCryowizardExternalJobExistenceAction(socket, target_workflow_name, cryosparc_username, cryosparc_password, project, jobuid)
{
    socket.emit("web_check_cryowizard_external_job_existence_action", target_workflow_name, cryosparc_username, cryosparc_password, project, jobuid);

    // check cryowizard external job existence action backinfo
    socket.once("js_web_check_cryowizard_external_job_existence_action_" + target_workflow_name, (res) => {
        var cryowizard_existence = res["cryowizard_existence"];

        if (!cryowizard_existence)
        {
            var project_card_dict = GetSessionStorageJsonItem("project_card_dict");
            project_card_dict["project_card_info"][target_workflow_name]["gui_info"]["cryowizard_job_part_disable_flag"] = false;
            project_card_dict["project_card_info"][target_workflow_name]["gui_info"]["cryowizard_pipeline_part_disable_flag"] = true;
            project_card_dict["project_card_info"][target_workflow_name]["gui_info"]["cryowizard_output_part_disable_flag"] = true;
            SetSessionStorageJsonItem("project_card_dict", project_card_dict);
            UpdateProjectCard(target_workflow_name);
            alert("Connecting to " + jobuid + " failed!");
        }
        else
        {
            alert("Connected!");
            UpdateProjectCard(target_workflow_name);
        }
    });
}


// check preset pipeline info action
function WebCheckPresetPipelineInfoAction(socket, target_workflow_name, cryosparc_username, cryosparc_password, project, workspace, jobuid, preset_pipeline_type)
{
    socket.emit("web_check_preset_pipeline_info_action", target_workflow_name, cryosparc_username, cryosparc_password, project, workspace, jobuid, preset_pipeline_type);

    // check preset pipeline info action backinfo
    socket.once("js_web_check_preset_pipeline_info_action_" + target_workflow_name, (res) => {
        var preset_pipeline_info = res["preset_pipeline_info"];

        var target_parameters_list = PipelinePresetParametersList(preset_pipeline_type);
        for (var i = 0; i < target_parameters_list.length; ++i)
        {
            if (preset_pipeline_info["preset_pipeline_args"][target_parameters_list[i]] != null)
            {
                if (["source_movie_job_uid", "source_micrograph_job_uid", "source_particle_job_uid", "source_template_job_uid", "source_volume_job_uid", "source_mask_job_uid", "source_cryoranker_job_uid"].includes(target_parameters_list[i]))
                {
                    document.getElementById(target_workflow_name + "_" + target_parameters_list[i]).value = preset_pipeline_info["preset_pipeline_args"][target_parameters_list[i]].join(" ");
                }
                else
                {
                    document.getElementById(target_workflow_name + "_" + target_parameters_list[i]).value = String(preset_pipeline_info["preset_pipeline_args"][target_parameters_list[i]]);
                }
            }
            document.getElementById(target_workflow_name + "_" + target_parameters_list[i]).disabled = false;
            document.getElementById(target_workflow_name + "_" + target_parameters_list[i]).placeholder = "";
        }
    });
}


// add preset pipeline action
function WebAddPresetPipelineAction(socket, target_workflow_name, cryosparc_username, cryosparc_password, project, workspace, jobuid, preset_pipeline_type, preset_pipeline_parameters)
{
    socket.emit("web_add_preset_pipeline_action", target_workflow_name, cryosparc_username, cryosparc_password, project, workspace, jobuid, preset_pipeline_type, preset_pipeline_parameters);

    // add single pipeline node action backinfo
    socket.once("js_web_add_preset_pipeline_action_" + target_workflow_name, (res) => {
        UpdateProjectCard(target_workflow_name);
    });
}


// add single pipeline node action
function WebAddSinglePipelineNodeAction(socket, target_workflow_name, cryosparc_username, cryosparc_password, project, jobuid, pipeline_node_type)
{
    socket.emit("web_add_single_pipeline_node_action", target_workflow_name, cryosparc_username, cryosparc_password, project, jobuid, pipeline_node_type);

    // add single pipeline node action backinfo
    socket.once("js_web_add_single_pipeline_node_action_" + target_workflow_name, (res) => {
        var project_card_dict = GetSessionStorageJsonItem("project_card_dict");
        project_card_dict["project_card_info"][target_workflow_name]["pipeline_parameters"]["create_pipeline_node_value"] = pipeline_node_type;
        SetSessionStorageJsonItem("project_card_dict", project_card_dict);
        UpdateProjectCard(target_workflow_name);
    });
}


// delete single pipeline node action
function WebDeleteSinglePipelineNodeAction(socket, target_workflow_name, cryosparc_username, cryosparc_password, project, jobuid, pipeline_node_name)
{
    socket.emit("web_delete_single_pipeline_node_action", target_workflow_name, cryosparc_username, cryosparc_password, project, jobuid, pipeline_node_name);

    // add single pipeline node action backinfo
    socket.once("js_web_delete_single_pipeline_node_action_" + target_workflow_name, (res) => {
        UpdateProjectCard(target_workflow_name);
    });
}


// pipeline node save parameters action
function WebPipelineNodeSaveParametersAction(socket, target_workflow_name, cryosparc_username, cryosparc_password, project, jobuid, pipeline_node_name, pipeline_node_parameters)
{
    socket.emit("web_pipeline_node_save_parameters_action", target_workflow_name, cryosparc_username, cryosparc_password, project, jobuid, pipeline_node_name, pipeline_node_parameters);

    // add single pipeline node action backinfo
    socket.once("js_web_pipeline_node_save_parameters_action_" + target_workflow_name, (res) => {
        UpdateProjectCard(target_workflow_name);
    });
}


// check pipeline nodes action
function WebCheckPipelineNodesAction(socket, target_workflow_name, cryosparc_username, cryosparc_password, project, workspace, jobuid, if_disable=false)
{
    socket.emit("web_check_pipeline_nodes_action", target_workflow_name, cryosparc_username, cryosparc_password, project, workspace, jobuid);

    // check pipeline nodes action backinfo
    socket.once("js_web_check_pipeline_nodes_action_" + target_workflow_name, (res) => {
        var pipeline = res["pipeline"];
        var preset_pipeline_info = res["preset_pipeline_info"];
        var all_single_parameters_folder_type_info = res["all_single_parameters_folder_type_info"];
        var used_single_parameters_folder_name_list = res["used_single_parameters_folder_name_list"];
        var unused_single_parameters_folder_name_list = res["unused_single_parameters_folder_name_list"];
        var source_inputs_info = res["source_inputs_info"];


        const parser = new DOMParser();


        var pipeline_panel = document.getElementById(target_workflow_name + "_pipeline_panel");
        pipeline_panel.replaceChildren();

        var single_pipeline_step_str = null;
        var single_pipeline_step_doc = null;
        var single_pipeline_step = null;
        var single_pipeline_node_str = null;
        var single_pipeline_node_doc = null;
        var single_pipeline_node = null;
        var single_pipeline_node_modal_parameter_str = null;
        var single_pipeline_node_modal_parameter_doc = null;
        var single_pipeline_node_modal_parameter = null;
        var single_pipeline_node_name = null;
        var single_pipeline_step_div_dom = null;
        var single_pipeline_node_modal_div_dom = null;
        var single_pipeline_node_parameter_names_list_str = null;

        var disable = "";
        if (if_disable)
        {
            disable = " disabled";
        }

        // unused pipeline nodes
        single_pipeline_step_str = `<label for="` + target_workflow_name + `_unused_pipeline_nodes" class="form-label col-form-label-sm">Unused Pipeline Nodes</label>`;
        single_pipeline_step_doc = parser.parseFromString(single_pipeline_step_str, "text/html");
        single_pipeline_step = single_pipeline_step_doc.body.firstElementChild;
        pipeline_panel.appendChild(single_pipeline_step);
        single_pipeline_step_str = `<div class="row m-0 p-0 overflow-auto" id="` + target_workflow_name + `_unused_pipeline_nodes"></div>`;
        single_pipeline_step_doc = parser.parseFromString(single_pipeline_step_str, "text/html");
        single_pipeline_step = single_pipeline_step_doc.body.firstElementChild;
        pipeline_panel.appendChild(single_pipeline_step);

        single_pipeline_step_div_dom = document.getElementById(target_workflow_name + "_unused_pipeline_nodes");
        for (var i = 0; i < unused_single_parameters_folder_name_list.length; ++i)
        {
            // add pipeline nodes
            single_pipeline_node_name = unused_single_parameters_folder_name_list[i];
            single_pipeline_node_parameter_names_list_str = "[";
            if (Object.keys(source_inputs_info[single_pipeline_node_name]).length > 0)
            {
                for (var single_node_parameter_key in source_inputs_info[single_pipeline_node_name])
                {
                    single_pipeline_node_parameter_names_list_str += "'" + single_node_parameter_key + "', ";
                }
            }
            single_pipeline_node_parameter_names_list_str += "]";
            single_pipeline_node_str = `
                <div class="col-md-1 m-1 p-0 border border-3 rounded rounded-5 bg-light overflow-auto" style="width: 450px;">
                    <label class="p-3 pb-0 text-center w-100 form-label col-form-label-sm">` + single_pipeline_node_name + `</label>
                    <label class="p-3 text-center w-100 form-label col-form-label-sm"><kbd>Node type: ` + SinglePipelineNodeNameChange(all_single_parameters_folder_type_info[single_pipeline_node_name]) + `</kbd></label>
                    <div class="row m-0 p-0 overflow-auto">
                        <button type="button" class="col btn btn-primary btn-sm rounded rounded-5" data-bs-toggle="modal" data-bs-target="#` + target_workflow_name + `_` + single_pipeline_node_name + `_parameter_button" onclick=""` + disable + `>Edit</button>
                        <button type="button" class="col btn btn-primary btn-sm rounded rounded-5" id="` + target_workflow_name + `_` + single_pipeline_node_name + `_delete_button" onclick="DeletePipelineNode('` + target_workflow_name + `', '` + single_pipeline_node_name + `')"` + disable + `>Delete</button>
                            
                        <div class="modal fade" id="` + target_workflow_name + `_` + single_pipeline_node_name + `_parameter_button">
                            <div class="modal-dialog modal-lg">
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <h4 class="modal-title">Modify ` + single_pipeline_node_name + ` parameters</h4>
                                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                                    </div>
                                    <div class="modal-body" id="` + target_workflow_name + `_modify_` + single_pipeline_node_name + `_parameters_div"></div>
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-primary" data-bs-dismiss="modal" onclick="PipelineNodeSaveParameters('` + target_workflow_name + `', '` + single_pipeline_node_name + `', ` + single_pipeline_node_parameter_names_list_str + `)">Save</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                    </div>
                </div>`;
            single_pipeline_node_doc = parser.parseFromString(single_pipeline_node_str, "text/html");
            single_pipeline_node = single_pipeline_node_doc.body.firstElementChild;
            single_pipeline_step_div_dom.appendChild(single_pipeline_node);
            // add pipeline nodes modal parameters
            single_pipeline_node_modal_div_dom = document.getElementById(target_workflow_name + "_modify_" + single_pipeline_node_name + "_parameters_div");
            if (Object.keys(source_inputs_info[single_pipeline_node_name]).length > 0)
            {
                for (var single_node_parameter_key in source_inputs_info[single_pipeline_node_name])
                {
                    single_pipeline_node_modal_parameter_str = `
                        <div class="row m-0 p-1">
                            <div class="col m-0 p-0 text-nowrap overflow-hidden">` + PipelineParametersNameChange(single_node_parameter_key) + `:</div>
                            <div class="col m-0 p-0">
                                <input type="text" class="form-control form-control-sm" id="` + target_workflow_name + "_" + single_pipeline_node_name + "_" + single_node_parameter_key + `">
                            </div>
                        </div>`;
                    single_pipeline_node_modal_parameter_doc = parser.parseFromString(single_pipeline_node_modal_parameter_str, "text/html");
                    single_pipeline_node_modal_parameter = single_pipeline_node_modal_parameter_doc.body.firstElementChild;
                    single_pipeline_node_modal_div_dom.appendChild(single_pipeline_node_modal_parameter);
                    if (source_inputs_info[single_pipeline_node_name][single_node_parameter_key]["current_value"] != null)
                    {
                        if (["source_movie_job_uid", "source_micrograph_job_uid", "source_particle_job_uid", "source_template_job_uid", "source_volume_job_uid", "source_mask_job_uid", "source_cryoranker_job_uid"].includes(single_node_parameter_key))
                        {
                            document.getElementById(target_workflow_name + "_" + single_pipeline_node_name + "_" + single_node_parameter_key).value = source_inputs_info[single_pipeline_node_name][single_node_parameter_key]["current_value"].join(" ");
                        }
                        else
                        {
                            document.getElementById(target_workflow_name + "_" + single_pipeline_node_name + "_" + single_node_parameter_key).value = String(source_inputs_info[single_pipeline_node_name][single_node_parameter_key]["current_value"]);
                        }
                    }
                }
            }
        }

        // pipeline steps
        var step_count = null;
        for (var i = 0; i < pipeline.length; ++i)
        {
            step_count = pipeline[i]["step"];

            single_pipeline_step_str = `<hr>`;
            single_pipeline_step_doc = parser.parseFromString(single_pipeline_step_str, "text/html");
            single_pipeline_step = single_pipeline_step_doc.body.firstElementChild;
            pipeline_panel.appendChild(single_pipeline_step);
            single_pipeline_step_str = `<label for="` + target_workflow_name + `_pipeline_step_` + String(step_count) + `" class="form-label col-form-label-sm">Pipeline Step ` + String(step_count) + `</label>`;
            single_pipeline_step_doc = parser.parseFromString(single_pipeline_step_str, "text/html");
            single_pipeline_step = single_pipeline_step_doc.body.firstElementChild;
            pipeline_panel.appendChild(single_pipeline_step);
            single_pipeline_step_str = `<div class="row m-0 p-0 overflow-auto" id="` + target_workflow_name + `_pipeline_step_` + String(step_count) + `"></div>`;
            single_pipeline_step_doc = parser.parseFromString(single_pipeline_step_str, "text/html");
            single_pipeline_step = single_pipeline_step_doc.body.firstElementChild;
            pipeline_panel.appendChild(single_pipeline_step);

            single_pipeline_step_div_dom = document.getElementById(target_workflow_name + "_pipeline_step_" + String(step_count));
            for (var j = 0; j < pipeline[i]["nodes"].length; ++j)
            {
                // add pipeline nodes
                single_pipeline_node_name = pipeline[i]["nodes"][j];
                single_pipeline_node_parameter_names_list_str = "[";
                if (Object.keys(source_inputs_info[single_pipeline_node_name]).length > 0)
                {
                    for (var single_node_parameter_key in source_inputs_info[single_pipeline_node_name])
                    {
                        single_pipeline_node_parameter_names_list_str += "'" + single_node_parameter_key + "', ";
                    }
                }
                single_pipeline_node_parameter_names_list_str += "]";
                single_pipeline_node_str = `
                    <div class="col-md-1 m-1 p-0 border border-3 rounded rounded-5 bg-light overflow-auto" style="width: 450px;">
                        <label class="p-3 pb-0 text-center w-100 form-label col-form-label-sm">` + single_pipeline_node_name + `</label>
                        <label class="p-3 text-center w-100 form-label col-form-label-sm"><kbd>Node type: ` + SinglePipelineNodeNameChange(all_single_parameters_folder_type_info[single_pipeline_node_name]) + `</kbd></label>
                        <div class="row m-0 p-0 overflow-auto">
                            <button type="button" class="col btn btn-primary btn-sm rounded rounded-5" data-bs-toggle="modal" data-bs-target="#` + target_workflow_name + `_` + single_pipeline_node_name + `_parameter_button" onclick=""` + disable + `>Edit</button>
                            <button type="button" class="col btn btn-primary btn-sm rounded rounded-5" id="` + target_workflow_name + `_` + single_pipeline_node_name + `_delete_button" onclick="DeletePipelineNode('` + target_workflow_name + `', '` + single_pipeline_node_name + `')"` + disable + `>Delete</button>
                            
                            <div class="modal fade" id="` + target_workflow_name + `_` + single_pipeline_node_name + `_parameter_button">
                                <div class="modal-dialog modal-lg">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h4 class="modal-title">Modify ` + single_pipeline_node_name + ` parameters</h4>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                                        </div>
                                        <div class="modal-body" id="` + target_workflow_name + `_modify_` + single_pipeline_node_name + `_parameters_div"></div>
                                        <div class="modal-footer">
                                            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" onclick="PipelineNodeSaveParameters('` + target_workflow_name + `', '` + single_pipeline_node_name + `', ` + single_pipeline_node_parameter_names_list_str + `)">Save</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                        </div>
                    </div>`;
                single_pipeline_node_doc = parser.parseFromString(single_pipeline_node_str, "text/html");
                single_pipeline_node = single_pipeline_node_doc.body.firstElementChild;
                single_pipeline_step_div_dom.appendChild(single_pipeline_node);
                // add pipeline nodes modal parameters
                single_pipeline_node_modal_div_dom = document.getElementById(target_workflow_name + "_modify_" + single_pipeline_node_name + "_parameters_div");
                if (Object.keys(source_inputs_info[single_pipeline_node_name]).length > 0)
                {
                    for (var single_node_parameter_key in source_inputs_info[single_pipeline_node_name])
                    {
                        single_pipeline_node_modal_parameter_str = `
                            <div class="row m-0 p-1">
                                <div class="col m-0 p-0 text-nowrap overflow-hidden">` + PipelineParametersNameChange(single_node_parameter_key) + `:</div>
                                <div class="col m-0 p-0">
                                    <input type="text" class="form-control form-control-sm" id="` + target_workflow_name + "_" + single_pipeline_node_name + "_" + single_node_parameter_key + `">
                                </div>
                            </div>`;
                        single_pipeline_node_modal_parameter_doc = parser.parseFromString(single_pipeline_node_modal_parameter_str, "text/html");
                        single_pipeline_node_modal_parameter = single_pipeline_node_modal_parameter_doc.body.firstElementChild;
                        single_pipeline_node_modal_div_dom.appendChild(single_pipeline_node_modal_parameter);
                        if (source_inputs_info[single_pipeline_node_name][single_node_parameter_key]["current_value"] != null)
                        {
                            if (["source_movie_job_uid", "source_micrograph_job_uid", "source_particle_job_uid", "source_template_job_uid", "source_volume_job_uid", "source_mask_job_uid", "source_cryoranker_job_uid"].includes(single_node_parameter_key))
                            {
                                document.getElementById(target_workflow_name + "_" + single_pipeline_node_name + "_" + single_node_parameter_key).value = source_inputs_info[single_pipeline_node_name][single_node_parameter_key]["current_value"].join(" ");
                            }
                            else
                            {
                                document.getElementById(target_workflow_name + "_" + single_pipeline_node_name + "_" + single_node_parameter_key).value = String(source_inputs_info[single_pipeline_node_name][single_node_parameter_key]["current_value"]);
                            }
                        }
                    }
                }
            }
        }

        // preset pipeline parameters
        var used_preset_pipeline_parameters_div = document.getElementById(target_workflow_name + "_used_pipeline_parameters_show");
        used_preset_pipeline_parameters_div.replaceChildren();

        var used_preset_pipeline_single_parameter_str = null;
        var used_preset_pipeline_single_parameter_doc = null;
        var used_preset_pipeline_single_parameter = null;

        if (preset_pipeline_info["preset_pipeline_type"] != null)
        {
            // check pipeline type
            if (PipelinePresetParametersList(preset_pipeline_info["preset_pipeline_type"]) != null)
            {
                var project_card_dict = GetSessionStorageJsonItem("project_card_dict");
                project_card_dict["project_card_info"][target_workflow_name]["pipeline_parameters"]["create_preset_pipeline_value"] = preset_pipeline_info["preset_pipeline_type"];
                SetSessionStorageJsonItem("project_card_dict", project_card_dict);
                document.getElementById(target_workflow_name + "_preset_pipeline_choose").value = preset_pipeline_info["preset_pipeline_type"];
            }
            else
            {
                var project_card_dict = GetSessionStorageJsonItem("project_card_dict");
                project_card_dict["project_card_info"][target_workflow_name]["pipeline_parameters"]["create_preset_pipeline_value"] = "custom";
                SetSessionStorageJsonItem("project_card_dict", project_card_dict);
                document.getElementById(target_workflow_name + "_preset_pipeline_choose").value = "custom";
            }
            // show preset pipeline parameters
            used_preset_pipeline_single_parameter_str = `
                <div class="row m-0 p-0">
                    <div class="col m-0 p-0 text-nowrap overflow-hidden">Preset type:</div>
                    <div class="col m-0 p-0"><input type="text" class="form-control form-control-sm" value="` + PipelinePresetTypeNameChange(String(preset_pipeline_info["preset_pipeline_type"])) + `" disabled></div>
                </div>`;
            used_preset_pipeline_single_parameter_doc = parser.parseFromString(used_preset_pipeline_single_parameter_str, "text/html");
            used_preset_pipeline_single_parameter = used_preset_pipeline_single_parameter_doc.body.firstElementChild;
            used_preset_pipeline_parameters_div.appendChild(used_preset_pipeline_single_parameter);
            if (Object.keys(preset_pipeline_info["preset_pipeline_args"]).length > 0)
            {
                for (var parameter_key in preset_pipeline_info["preset_pipeline_args"])
                {
                    if (preset_pipeline_info["preset_pipeline_args"][parameter_key] != null)
                    {
                        if (["source_movie_job_uid", "source_micrograph_job_uid", "source_particle_job_uid", "source_template_job_uid", "source_volume_job_uid", "source_mask_job_uid", "source_cryoranker_job_uid"].includes(parameter_key))
                        {
                            used_preset_pipeline_single_parameter_str = `
                                <div class="row m-0 p-0">
                                    <div class="col m-0 p-0 text-nowrap overflow-hidden">` + PipelineParametersNameChange(parameter_key) + `:</div>
                                    <div class="col m-0 p-0"><input type="text" class="form-control form-control-sm" value="` + preset_pipeline_info["preset_pipeline_args"][parameter_key].join(" ") + `" disabled></div>
                                </div>`;
                        }
                        else
                        {
                            used_preset_pipeline_single_parameter_str = `
                                <div class="row m-0 p-0">
                                    <div class="col m-0 p-0 text-nowrap overflow-hidden">` + PipelineParametersNameChange(parameter_key) + `:</div>
                                    <div class="col m-0 p-0"><input type="text" class="form-control form-control-sm" value="` + String(preset_pipeline_info["preset_pipeline_args"][parameter_key]) + `" disabled></div>
                                </div>`;
                        }
                        used_preset_pipeline_single_parameter_doc = parser.parseFromString(used_preset_pipeline_single_parameter_str, "text/html");
                        used_preset_pipeline_single_parameter = used_preset_pipeline_single_parameter_doc.body.firstElementChild;
                        used_preset_pipeline_parameters_div.appendChild(used_preset_pipeline_single_parameter);
                    }
                }
            }
        }

        // base parameters modal content
        single_pipeline_node_name = "base_parameters";
        single_pipeline_node_modal_div_dom = document.getElementById(target_workflow_name + "_modify_base_parameters_modal_div");
        if (Object.keys(source_inputs_info[single_pipeline_node_name]).length > 0)
        {
            for (var single_node_parameter_key in source_inputs_info[single_pipeline_node_name])
            {
                single_pipeline_node_modal_parameter_str = `
                    <div class="row m-0 p-1">
                        <div class="col m-0 p-0 text-nowrap overflow-hidden">` + PipelineParametersNameChange(single_node_parameter_key) + `:</div>
                        <div class="col m-0 p-0">
                            <input type="text" class="form-control form-control-sm" id="` + target_workflow_name + "_" + single_pipeline_node_name + "_" + single_node_parameter_key + `">
                        </div>
                    </div>`;
                single_pipeline_node_modal_parameter_doc = parser.parseFromString(single_pipeline_node_modal_parameter_str, "text/html");
                single_pipeline_node_modal_parameter = single_pipeline_node_modal_parameter_doc.body.firstElementChild;
                single_pipeline_node_modal_div_dom.appendChild(single_pipeline_node_modal_parameter);
                if (source_inputs_info[single_pipeline_node_name][single_node_parameter_key]["current_value"] != null)
                {
                    if (["source_movie_job_uid", "source_micrograph_job_uid", "source_particle_job_uid", "source_template_job_uid", "source_volume_job_uid", "source_mask_job_uid", "source_cryoranker_job_uid"].includes(single_node_parameter_key))
                    {
                        document.getElementById(target_workflow_name + "_" + single_pipeline_node_name + "_" + single_node_parameter_key).value = source_inputs_info[single_pipeline_node_name][single_node_parameter_key]["current_value"].join(" ");
                    }
                    else
                    {
                        document.getElementById(target_workflow_name + "_" + single_pipeline_node_name + "_" + single_node_parameter_key).value = String(source_inputs_info[single_pipeline_node_name][single_node_parameter_key]["current_value"]);
                    }
                }
            }
        }

    });
}


// run cryowizard job action
function WebRunCryowizardExternalJobAction(socket, target_workflow_name, cryosparc_username, cryosparc_password, project, jobuid)
{
    socket.emit("web_run_cryowizard_external_job_action", target_workflow_name, cryosparc_username, cryosparc_password, project, jobuid);

    // // run cryowizard job action backinfo
    // socket.once("js_web_run_cryowizard_external_job_action_" + target_workflow_name, (res) => {
    //
    // });
}


// continue cryowizard job action
function WebContinueCryowizardExternalJobAction(socket, target_workflow_name, cryosparc_username, cryosparc_password, project, jobuid)
{
    socket.emit("web_continue_cryowizard_external_job_action", target_workflow_name, cryosparc_username, cryosparc_password, project, jobuid);

    // // continue cryowizard job action backinfo
    // socket.once("js_web_continue_cryowizard_external_job_action_" + target_workflow_name, (res) => {
    //
    // });
}


// kill cryowizard job action
function WebKillCryowizardExternalJobAction(socket, target_workflow_name, cryosparc_username, cryosparc_password, project, jobuid)
{
    socket.emit("web_kill_cryowizard_external_job_action", target_workflow_name, cryosparc_username, cryosparc_password, project, jobuid);

    // // kill cryowizard job action backinfo
    // socket.once("js_web_kill_cryowizard_external_job_action_" + target_workflow_name, (res) => {
    //
    // });
}


// clear cryowizard job metadata action
function WebClearCryowizardExternalJobMetadataAction(socket, target_workflow_name, cryosparc_username, cryosparc_password, project, jobuid)
{
    socket.emit("web_clear_cryowizard_external_job_metadata_action", target_workflow_name, cryosparc_username, cryosparc_password, project, jobuid);

    // // kill cryowizard job action backinfo
    // socket.once("js_web_clear_cryowizard_external_job_metadata_action_" + target_workflow_name, (res) => {
    //
    // });
}


// show cryowizard job results action
function WebShowCryowizardExternalJobResultsAction(socket, target_workflow_name, cryosparc_username, cryosparc_password, project, jobuid)
{
    socket.emit("web_show_cryowizard_external_job_results_action", target_workflow_name, cryosparc_username, cryosparc_password, project, jobuid);

    // show cryowizard job results action backinfo
    socket.once("js_web_show_cryowizard_external_job_results_action_" + target_workflow_name, (res) => {
        var response_data = res["response"];
        document.getElementById(target_workflow_name + "_output_panel").innerHTML = response_data.join("<br>");
    });
}



