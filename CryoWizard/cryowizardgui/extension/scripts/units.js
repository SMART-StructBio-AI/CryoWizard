

// session storage get
function GetSessionStorageJsonItem(session_storage_key)
{
    return JSON.parse(sessionStorage.getItem(session_storage_key));
}

// session storage set
function SetSessionStorageJsonItem(session_storage_key, json_value)
{
    sessionStorage.setItem(session_storage_key, JSON.stringify(json_value));
}

// check url dynamically
function checkURL()
{
    console.log("Current url:", window.location.href);

    // if (window.location.protocol !== 'http:') {
    //     return false;
    // }

    var pathsplit = window.location.pathname.split("/");
    if (pathsplit.length < 3)
    {
        return false;
    }
    var PWJsplit = pathsplit[2].split("-");
    if ((PWJsplit.length != 3) || (PWJsplit[0][0] != "P") || (PWJsplit[1][0] != "W") || (PWJsplit[2][0] != "J"))
    {
        return false;
    }

    return true;
}

// get project id and workspace id from url
function ParseProjectAndWorkspace()
{
    var pathname = window.location.pathname;

    let path_split = pathname.split("/");
    var project_and_workspace = path_split[2];

    let project_and_workspace_split = project_and_workspace.split("-");
    var project = project_and_workspace_split[0];
    var workspace = project_and_workspace_split[1];

    return {"project": project, "workspace": workspace};
}

// add crywizard gui parameter group
function AddParameterGroup(project, jobid, parameter_group_type, disable=false)
{
    var parameter_group_container_element = document.getElementsByClassName("parametergroupcontainer")[0];
    var new_parameter_group_string = "";
    var disable_str = "";
    if (disable == true)
    {
        disable_str = "disabled";
    }

    if (parameter_group_type == "pipeline_type")
    {
        new_parameter_group_string = `
            <div class="group">
                <div class="flex justify-between">
                    <label for="` + project + "_" + jobid + `_cryowizard_pipeline_type" class="block text-xs font-medium text-gray-700">CryoWizard pipeline type</label>
                </div>
                <div class="mt-1 flex items-center">
                    <select name="` + project + "_" + jobid + `_cryowizard_pipeline_type" id="` + project + "_" + jobid + `_cryowizard_pipeline_type" class="mr-0.5 block w-full pl-2 pr-10 py-1 text-xs focus:outline-none rounded border-gray-300 focus:ring-blue-500 focus:border-blue-500" data-trigger="tooltip-trigger-3077" ` + disable_str + `>
                        <option value="default">cryowizard pipeline default</option>
                        <option value="simpler">cryowizard pipeline simpler</option>
                        <option value="cryoranker_only">cryoranker only</option>
                        <option value="cryoranker_get_top_particles">cryoranker get top particles</option>
                        <option value="custom">custom</option>
                    </select>
                    <div class="flex flex-shrink-0 items-center ml-auto">
                        <button type="button" class="inline-flex items-center px-0.5 py-0.5 border border-transparent text-xs font-medium rounded-full text-gray-400 bg-white hover:bg-gray-100 hover:text-gray-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-gray-500 opacity-0 group-hover:opacity-100 focus:opacity-100 transition-opacity duration-150">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="heroicon heroicon--solid h-5 w-5 " width="100%" height="100%">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }
    else if (parameter_group_type == "pixelsize")
    {
        new_parameter_group_string = `
            <div class="group">
                <div class="flex justify-between">
                    <label for="` + project + "_" + jobid + `_cryowizard_pixelsize" class="block text-xs font-medium text-gray-700">Pixel Size (A)</label>
                </div>
                <div class="mt-1 flex items-center">
                    <input type="number" name="` + project + "_" + jobid + `_cryowizard_pixelsize" id="` + project + "_" + jobid + `_cryowizard_pixelsize" class="mr-0.5 block w-full pl-2 py-1 text-xs rounded border-gray-300 focus:ring-blue-500 focus:border-blue-500" placeholder="Not set" title="" ` + disable_str + `>
                    <div class="flex flex-shrink-0 items-center ml-auto">
                        <button type="button" class="inline-flex items-center px-0.5 py-0.5 border border-transparent text-xs font-medium rounded-full text-gray-400 bg-white hover:bg-gray-100 hover:text-gray-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-gray-500 opacity-0 group-hover:opacity-100 focus:opacity-100 transition-opacity duration-150">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="heroicon heroicon--solid h-5 w-5 " width="100%" height="100%">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }
    else if (parameter_group_type == "diameter")
    {
        new_parameter_group_string = `
            <div class="group">
                <div class="flex justify-between">
                    <label for="` + project + "_" + jobid + `_cryowizard_diameter" class="block text-xs font-medium text-gray-700">Average Particle diameter (A)</label>
                </div>
                <div class="mt-1 flex items-center">
                    <input type="number" name="` + project + "_" + jobid + `_cryowizard_diameter" id="` + project + "_" + jobid + `_cryowizard_diameter" class="mr-0.5 block w-full pl-2 py-1 text-xs rounded border-gray-300 focus:ring-blue-500 focus:border-blue-500" placeholder="Not set" title="" ` + disable_str + `>
                    <div class="flex flex-shrink-0 items-center ml-auto">
                        <button type="button" class="inline-flex items-center px-0.5 py-0.5 border border-transparent text-xs font-medium rounded-full text-gray-400 bg-white hover:bg-gray-100 hover:text-gray-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-gray-500 opacity-0 group-hover:opacity-100 focus:opacity-100 transition-opacity duration-150">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="heroicon heroicon--solid h-5 w-5 " width="100%" height="100%">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }
    else if (parameter_group_type == "ctf_resolution")
    {
        new_parameter_group_string = `
            <div class="group">
                <div class="flex justify-between">
                    <label for="` + project + "_" + jobid + `_cryowizard_ctf_resolution" class="block text-xs font-medium text-gray-700">CTF fit resolution</label>
                </div>
                <div class="mt-1 flex items-center">
                    <input type="text" name="` + project + "_" + jobid + `_cryowizard_ctf_resolution" id="` + project + "_" + jobid + `_cryowizard_ctf_resolution" class="mr-0.5 block w-full pl-2 py-1 text-xs rounded border-gray-300 focus:ring-blue-500 focus:border-blue-500" placeholder="Not set" title="" ` + disable_str + `>
                    <div class="flex flex-shrink-0 items-center ml-auto">
                        <button type="button" class="inline-flex items-center px-0.5 py-0.5 border border-transparent text-xs font-medium rounded-full text-gray-400 bg-white hover:bg-gray-100 hover:text-gray-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-gray-500 opacity-0 group-hover:opacity-100 focus:opacity-100 transition-opacity duration-150" data-trigger="tooltip-trigger-574">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="heroicon heroicon--solid h-5 w-5 " width="100%" height="100%">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }
    else if (parameter_group_type == "symmetry")
    {
        new_parameter_group_string = `
            <div class="group">
                <div class="flex justify-between">
                    <label for="` + project + "_" + jobid + `_cryowizard_symmetry" class="block text-xs font-medium text-gray-700">Symmetry</label>
                </div>
                <div class="mt-1 flex items-center">
                    <input type="text" name="` + project + "_" + jobid + `_cryowizard_symmetry" id="` + project + "_" + jobid + `_cryowizard_symmetry" class="mr-0.5 block w-full pl-2 py-1 text-xs rounded border-gray-300 focus:ring-blue-500 focus:border-blue-500" placeholder="Not set" title="" ` + disable_str + `>
                    <div class="flex flex-shrink-0 items-center ml-auto">
                        <button type="button" class="inline-flex items-center px-0.5 py-0.5 border border-transparent text-xs font-medium rounded-full text-gray-400 bg-white hover:bg-gray-100 hover:text-gray-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-gray-500 opacity-0 group-hover:opacity-100 focus:opacity-100 transition-opacity duration-150" data-trigger="tooltip-trigger-574">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="heroicon heroicon--solid h-5 w-5 " width="100%" height="100%">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }
    else if (parameter_group_type == "gpu_num")
    {
        new_parameter_group_string = `
            <div class="group">
                <div class="flex justify-between">
                    <label for="` + project + "_" + jobid + `_cryowizard_gpu_num" class="block text-xs font-medium text-gray-700">Number of GPUs for Multi-GPU CryoSPARC jobs</label>
                </div>
                <div class="mt-1 flex items-center">
                    <input type="number" name="` + project + "_" + jobid + `_cryowizard_gpu_num" id="` + project + "_" + jobid + `_cryowizard_gpu_num" class="mr-0.5 block w-full pl-2 py-1 text-xs rounded border-gray-300 focus:ring-blue-500 focus:border-blue-500" placeholder="Not set" title="" ` + disable_str + `>
                    <div class="flex flex-shrink-0 items-center ml-auto">
                        <button type="button" class="inline-flex items-center px-0.5 py-0.5 border border-transparent text-xs font-medium rounded-full text-gray-400 bg-white hover:bg-gray-100 hover:text-gray-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-gray-500 opacity-0 group-hover:opacity-100 focus:opacity-100 transition-opacity duration-150">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="heroicon heroicon--solid h-5 w-5 " width="100%" height="100%">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }
    else if (parameter_group_type == "inference_gpu_ids")
    {
        new_parameter_group_string = `
            <div class="group">
                <div class="flex justify-between">
                    <label for="` + project + "_" + jobid + `_cryowizard_inference_gpu_ids" class="block text-xs font-medium text-gray-700">Inference GPU ids</label>
                </div>
                <div class="mt-1 flex items-center">
                    <input type="text" name="` + project + "_" + jobid + `_cryowizard_inference_gpu_ids" id="` + project + "_" + jobid + `_cryowizard_inference_gpu_ids" class="mr-0.5 block w-full pl-2 py-1 text-xs rounded border-gray-300 focus:ring-blue-500 focus:border-blue-500" placeholder="Not set" title="" ` + disable_str + `>
                    <div class="flex flex-shrink-0 items-center ml-auto">
                        <button type="button" class="inline-flex items-center px-0.5 py-0.5 border border-transparent text-xs font-medium rounded-full text-gray-400 bg-white hover:bg-gray-100 hover:text-gray-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-gray-500 opacity-0 group-hover:opacity-100 focus:opacity-100 transition-opacity duration-150" data-trigger="tooltip-trigger-574">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="heroicon heroicon--solid h-5 w-5 " width="100%" height="100%">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }
    else if (parameter_group_type == "get_type")
    {
        new_parameter_group_string = `
            <div class="group">
                <div class="flex justify-between">
                    <label for="` + project + "_" + jobid + `_cryowizard_get_type" class="block text-xs font-medium text-gray-700">Get type</label>
                </div>
                <div class="mt-1 flex items-center">
                    <select name="` + project + "_" + jobid + `_cryowizard_get_type" id="` + project + "_" + jobid + `_cryowizard_get_type" class="mr-0.5 block w-full pl-2 pr-10 py-1 text-xs focus:outline-none rounded border-gray-300 focus:ring-blue-500 focus:border-blue-500" data-trigger="tooltip-trigger-3077" ` + disable_str + `>
                        <option value="num">Number</option>
                        <option value="score">Score</option>
                    </select>
                    <div class="flex flex-shrink-0 items-center ml-auto">
                        <button type="button" class="inline-flex items-center px-0.5 py-0.5 border border-transparent text-xs font-medium rounded-full text-gray-400 bg-white hover:bg-gray-100 hover:text-gray-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-gray-500 opacity-0 group-hover:opacity-100 focus:opacity-100 transition-opacity duration-150">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="heroicon heroicon--solid h-5 w-5 " width="100%" height="100%">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }
    else if (parameter_group_type == "cutoff_condition")
    {
        new_parameter_group_string = `
            <div class="group">
                <div class="flex justify-between">
                    <label for="` + project + "_" + jobid + `_cryowizard_particle_cutoff_condition" class="block text-xs font-medium text-gray-700">Particle cut-off point</label>
                </div>
                <div class="mt-1 flex items-center">
                    <input type="number" name="` + project + "_" + jobid + `_cryowizard_particle_cutoff_condition" id="` + project + "_" + jobid + `_cryowizard_particle_cutoff_condition" class="mr-0.5 block w-full pl-2 py-1 text-xs rounded border-gray-300 focus:ring-blue-500 focus:border-blue-500" placeholder="Not set" title="" ` + disable_str + `>
                    <div class="flex flex-shrink-0 items-center ml-auto">
                        <button type="button" class="inline-flex items-center px-0.5 py-0.5 border border-transparent text-xs font-medium rounded-full text-gray-400 bg-white hover:bg-gray-100 hover:text-gray-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-gray-500 opacity-0 group-hover:opacity-100 focus:opacity-100 transition-opacity duration-150">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="heroicon heroicon--solid h-5 w-5 " width="100%" height="100%">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }
    const parser = new DOMParser();
    var new_parameter_group_doc = parser.parseFromString(new_parameter_group_string, "text/html");
    var new_parameter_group = new_parameter_group_doc.body.firstElementChild;
    parameter_group_container_element.appendChild(new_parameter_group);
}

// check building tab input type
function CheckCryoWizardBuildingMenuInputs(socket, Inputs_element, cryosparc_username, cryosparc_password, project, jobid, disable, last_turn_type=null) {
    var input_movies_num = Number(Inputs_element.children[0].firstElementChild.lastElementChild.lastElementChild.textContent.trim());
    var input_micrographs_num = Number(Inputs_element.children[1].firstElementChild.lastElementChild.lastElementChild.textContent.trim());
    var input_particles_num = Number(Inputs_element.children[2].firstElementChild.lastElementChild.lastElementChild.textContent.trim());
    var input_cryorankers_num = Number(Inputs_element.children[3].firstElementChild.lastElementChild.lastElementChild.textContent.trim());
    var input_templates_num = Number(Inputs_element.children[4].firstElementChild.lastElementChild.lastElementChild.textContent.trim());
    var input_volumes_num = Number(Inputs_element.children[5].firstElementChild.lastElementChild.lastElementChild.textContent.trim());
    var input_masks_num = Number(Inputs_element.children[6].firstElementChild.lastElementChild.lastElementChild.textContent.trim());

    var cryowizard_pipeline_type = document.getElementById(project + "_" + jobid + "_cryowizard_pipeline_type").value;

    var this_turn_type = null;
    if (
        ((cryowizard_pipeline_type == "default") || (cryowizard_pipeline_type == "simpler")) &&
        ((input_movies_num == 0) && (input_micrographs_num == 0) && (input_particles_num > 0))
    ) {
        this_turn_type = 1;
        if (last_turn_type != this_turn_type)
        {
            // clear parameter groups except pipeline type
            var parameter_group_container_element = document.getElementsByClassName("parametergroupcontainer")[0];
            parameter_group_container_element.replaceChildren();
            AddParameterGroup(project, jobid, "pipeline_type", disable);
            document.getElementById(project + "_" + jobid + "_cryowizard_pipeline_type").value = cryowizard_pipeline_type;
            // add parameter groups
            AddParameterGroup(project, jobid, "symmetry", disable);
            AddParameterGroup(project, jobid, "gpu_num", disable);
            AddParameterGroup(project, jobid, "inference_gpu_ids", disable);
            // get ui parameters
            CheckCryowizardExternalJobParametersAction(socket, cryosparc_username, cryosparc_password, project, jobid, false);
        }
        return this_turn_type;
    }
    else if (
        ((cryowizard_pipeline_type == "default") || (cryowizard_pipeline_type == "simpler")) &&
        (!((input_movies_num == 0) && (input_micrographs_num == 0) && (input_particles_num > 0)))
    ) {
        this_turn_type = 2;
        if (last_turn_type != this_turn_type)
        {
            // clear parameter groups except pipeline type
            var parameter_group_container_element = document.getElementsByClassName("parametergroupcontainer")[0];
            parameter_group_container_element.replaceChildren();
            AddParameterGroup(project, jobid, "pipeline_type", disable);
            document.getElementById(project + "_" + jobid + "_cryowizard_pipeline_type").value = cryowizard_pipeline_type;
            // add parameter groups
            AddParameterGroup(project, jobid, "pixelsize", disable);
            AddParameterGroup(project, jobid, "diameter", disable);
            AddParameterGroup(project, jobid, "ctf_resolution", disable);
            AddParameterGroup(project, jobid, "symmetry", disable);
            AddParameterGroup(project, jobid, "gpu_num", disable);
            AddParameterGroup(project, jobid, "inference_gpu_ids", disable);
            // get ui parameters
            CheckCryowizardExternalJobParametersAction(socket, cryosparc_username, cryosparc_password, project, jobid, false);
        }
        return this_turn_type;
    }
    else if (
        (cryowizard_pipeline_type == "cryoranker_only") &&
        ((input_movies_num == 0) && (input_micrographs_num == 0) && (input_particles_num > 0))
    ) {
        this_turn_type = 3;
        if (last_turn_type != this_turn_type)
        {
            // clear parameter groups except pipeline type
            var parameter_group_container_element = document.getElementsByClassName("parametergroupcontainer")[0];
            parameter_group_container_element.replaceChildren();
            AddParameterGroup(project, jobid, "pipeline_type", disable);
            document.getElementById(project + "_" + jobid + "_cryowizard_pipeline_type").value = cryowizard_pipeline_type;
            // add parameter groups
            AddParameterGroup(project, jobid, "gpu_num", disable);
            AddParameterGroup(project, jobid, "inference_gpu_ids", disable);
            // get ui parameters
            CheckCryowizardExternalJobParametersAction(socket, cryosparc_username, cryosparc_password, project, jobid, false);
        }
        return this_turn_type;
    }
    else if (
        (cryowizard_pipeline_type == "cryoranker_only") &&
        (!((input_movies_num == 0) && (input_micrographs_num == 0) && (input_particles_num > 0)))
    ) {
        this_turn_type = 4;
        if (last_turn_type != this_turn_type)
        {
            // clear parameter groups except pipeline type
            var parameter_group_container_element = document.getElementsByClassName("parametergroupcontainer")[0];
            parameter_group_container_element.replaceChildren();
            AddParameterGroup(project, jobid, "pipeline_type", disable);
            document.getElementById(project + "_" + jobid + "_cryowizard_pipeline_type").value = cryowizard_pipeline_type;
            // add parameter groups
            AddParameterGroup(project, jobid, "pixelsize", disable);
            AddParameterGroup(project, jobid, "diameter", disable);
            AddParameterGroup(project, jobid, "ctf_resolution", disable);
            AddParameterGroup(project, jobid, "gpu_num", disable);
            AddParameterGroup(project, jobid, "inference_gpu_ids", disable);
            // get ui parameters
            CheckCryowizardExternalJobParametersAction(socket, cryosparc_username, cryosparc_password, project, jobid, false);
        }
        return this_turn_type;
    }
    else if (
        (cryowizard_pipeline_type == "cryoranker_get_top_particles")
    ) {
        this_turn_type = 5;
        if (last_turn_type != this_turn_type)
        {
            // clear parameter groups except pipeline type
            var parameter_group_container_element = document.getElementsByClassName("parametergroupcontainer")[0];
            parameter_group_container_element.replaceChildren();
            AddParameterGroup(project, jobid, "pipeline_type", disable);
            document.getElementById(project + "_" + jobid + "_cryowizard_pipeline_type").value = cryowizard_pipeline_type;
            // add parameter groups
            AddParameterGroup(project, jobid, "get_type", disable);
            AddParameterGroup(project, jobid, "cutoff_condition", disable);
            // get ui parameters
            CheckCryowizardExternalJobParametersAction(socket, cryosparc_username, cryosparc_password, project, jobid, false);
        }
        return this_turn_type;
    }
    else if (
        (cryowizard_pipeline_type == "custom")
    ) {
        this_turn_type = 6;
        if (last_turn_type != this_turn_type)
        {
            // clear parameter groups except pipeline type
            var parameter_group_container_element = document.getElementsByClassName("parametergroupcontainer")[0];
            parameter_group_container_element.replaceChildren();
            AddParameterGroup(project, jobid, "pipeline_type", disable);
            document.getElementById(project + "_" + jobid + "_cryowizard_pipeline_type").value = cryowizard_pipeline_type;
            // get ui parameters
            CheckCryowizardExternalJobParametersAction(socket, cryosparc_username, cryosparc_password, project, jobid, false);
        }
        return this_turn_type;
    }
    else {
        return null;
    }
}
