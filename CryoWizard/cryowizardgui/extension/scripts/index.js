


// session storage chrome_storage_paramters initial
chrome.storage.local.get([
    "server_address",
    "cryosparc_username",
    "cryosparc_password"
], function (result){
    var parameters = {
        "server_address": result.server_address,
        "cryosparc_username": result.cryosparc_username,
        "cryosparc_password": result.cryosparc_password
    };
    SetSessionStorageJsonItem("chrome_storage_paramters", parameters);

    var chrome_storage_paramters = GetSessionStorageJsonItem("chrome_storage_paramters");
    console.log("chrome_storage_paramters:");
    console.log(chrome_storage_paramters);
});

// // set temp var
// SetSessionStorageJsonItem("cryowizard_ui_parameters", {});

// set socket
var chrome_storage_paramters = GetSessionStorageJsonItem("chrome_storage_paramters");
var server_address = chrome_storage_paramters["server_address"];
const socket = io(server_address);
console.log("socketio created, server_address:", server_address);


// listen the changes of chrome.storage
chrome.storage.onChanged.addListener(function (changes, areaName) {

    chrome.storage.local.get([
        "server_address",
        "cryosparc_username",
        "cryosparc_password"
    ], function (result){
        var parameters = {
            "server_address": result.server_address,
            "cryosparc_username": result.cryosparc_username,
            "cryosparc_password": result.cryosparc_password
        };
        SetSessionStorageJsonItem("chrome_storage_paramters", parameters);
    });

    console.log("chrome.storage paramters change:");
    console.log(changes);

    var chrome_storage_paramters = GetSessionStorageJsonItem("chrome_storage_paramters");
    console.log("new chrome_storage_paramters:");
    console.log(chrome_storage_paramters);

    location.reload();

});


// main func, start after users opening Builder tab
waitForBuilderMenu((builder_elements) => {

    var chrome_storage_paramters = GetSessionStorageJsonItem("chrome_storage_paramters");
    var cryosparc_username = chrome_storage_paramters["cryosparc_username"];
    var cryosparc_password = chrome_storage_paramters["cryosparc_password"];

    // insert cryowizard buttons
    var elements = null;
    while (true) {
        elements = document.getElementsByClassName("custom-scrollbar");
        if (elements.length > 0) {
            break
        }
    }
    console.log(".custom-scrollbar found, list length:", elements.length);
    var target_element = elements[0].firstElementChild.firstElementChild;

    var new_li_cryowizard_class_string = `
    <li class="z-10 sticky top-0">
        <button type="button" class="w-full flex items-center justify-between border-t border-gray-300 bg-gray-100 px-3 py-1 text-xs font-medium text-gray-800 focus:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-offset-2 focus-visible:ring-blue-500">
            <svg xmlns="http://www.w3.org/2000/svg" class="inline-block w-4 h-4 text-gray-400" viewBox="0 0 16 16" fill="currentColor">
                <path fill-rule="evenodd" d="M2 7.75A.75.75 0 012.75 7h10a.75.75 0 010 1.5h-10A.75.75 0 012 7.75z"></path>
            </svg>
            <h3 class="font-bold">CryoWizard</h3>
            <span class="inline-flex text-gray-700">1</span>
        </button>
    </li>`;

    // cryowizard button
    var new_li_cryowizard_button_string = `
    <li id="job_builder_cryowizard" class="border-t border-gray-300" role="menuitem">
        <div class="flex">
            <button type="button" class="text-gray-900 hover:bg-gray-100 w-full flex items-center justify-between px-2 py-1.5 text-left" data-trigger="tooltip-trigger-22">
                <p class="text-sm">CryoWizard</p>
                <div class="flex flex-row-reverse items-center gap-1">
                    <span class="inline-flex items-center px-1 py-0.5 rounded-sm text-2xs leading-none font-medium bg-white border border-teal-400 text-teal-800">CryoWizard</span>
                </div>
            </button>
        </div>
    </li>`;

    const parser = new DOMParser();
    var new_li_cryowizard_class_doc = parser.parseFromString(new_li_cryowizard_class_string, "text/html");
    var new_li_cryowizard_button_doc = parser.parseFromString(new_li_cryowizard_button_string, "text/html");
    var new_li_cryowizard_class = new_li_cryowizard_class_doc.body.firstElementChild;
    var new_li_cryowizard_button = new_li_cryowizard_button_doc.body.firstElementChild;

    // add function to button
    new_li_cryowizard_button.firstElementChild.firstElementChild.onclick = (function (parameters) {
        return function (event) {
            if (checkURL())
            {
                var project_and_workspace = ParseProjectAndWorkspace();
                var project = project_and_workspace["project"];
                var workspace = project_and_workspace["workspace"];
                var cryosparc_username = parameters["cryosparc_username"];
                var cryosparc_password = parameters["cryosparc_password"];
                CreateCryowizardExternalJobAction(socket, cryosparc_username, cryosparc_password, project, workspace);
            }
        };
    })({
        "cryosparc_username": cryosparc_username,
        "cryosparc_password": cryosparc_password,
    });

    target_element.insertBefore(new_li_cryowizard_button, target_element.firstElementChild);
    target_element.insertBefore(new_li_cryowizard_class, target_element.firstElementChild);

});


// catch cryowizard building tab
waitForCryoWizardBuildingMenu((building_elements) => {

    var chrome_storage_paramters = GetSessionStorageJsonItem("chrome_storage_paramters");
    var cryosparc_username = chrome_storage_paramters["cryosparc_username"];
    var cryosparc_password = chrome_storage_paramters["cryosparc_password"];

    var project_and_job_string = building_elements.firstElementChild.firstElementChild.firstElementChild.firstElementChild.firstElementChild.textContent;
    var project = project_and_job_string.split(" ")[0].trim();
    var jobid = project_and_job_string.split(" ")[1].trim();

    var new_parameters_bar_string = `
        <button type="button" class="sticky top-0 z-11 flex-shrink-0 h-9 flex justify-between items-center font-medium px-3 bg-gray-100 hover:bg-gray-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-3 focus-visible:ring-offset-gray-100 focus-visible:ring-inset">
            <h2 class="font-medium">Parameters</h2>
            <div class="inline-flex items-center space-x-2">
                <span slot="badge" class="flex space-x-1"></span>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="heroicon heroicon--outline h-4 w-4 stroke-2 text-gray-600" width="100%" height="100%">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 15l7-7 7 7"></path>
                </svg>
            </div>
        </button>`;

    var new_parameters_string = `
        <div class="bg-white p-2">
            <div class="flex flex-col">
                <div class="section expanded">
                    <span class="sticky top-9 z-2 flex flex-wrap w-full">
                        <div class="w-full h-1 bg-white flex-shrink-0"></div>
                        <button type="button" class="bg-gray-100 hover:bg-gray-200 rounded-md border border-gray-300 flex w-full items-center justify-between py-1 px-1 text-left text-sm leading-4 font-medium text-gray-800 hover:text-gray-900 focus:outline-none focus-visible:ring-inset focus-visible:ring-offset-1 focus-visible:ring-2 focus-visible:ring-blue-500">
                            <span class="flex items-center space-x-1">
                                <svg class="h-4 w-4 text-gray-500 group-hover:text-gray-500 group-focus:text-gray-600" stroke="none" fill="currentColor" viewBox="0 0 16 16">
                                    <path d="M4.42678 9.57322L7.82326 6.17678C7.92089 6.07915 8.07918 6.07915 8.17681 6.17678L11.5732 9.57322C11.7307 9.73072 11.6192 10 11.3964 10L4.60356 10C4.38083 10 4.26929 9.73071 4.42678 9.57322Z"></path>
                                </svg>
                                <span slot="header">
                                    <p class="text-sm text-gray-600">Parameters</p>
                                </span>
                            </span>
                            <span slot="badge" class="flex space-x-1">
                                <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800 tabular-nums"></span>
                            </span>
                        </button>
                    </span>
                    <div class="bg-white p-2">
                        <div slot="content" class="parametergroupcontainer flex flex-col space-y-3 pb-2"></div>
                    </div>
                </div>
            </div>
        </div>`;

    var new_queue_job_button_string = `
        <button type="button" class="inline-flex items-center justify-center px-3 py-1.5 border border-transparent shadow-sm text-sm font-medium rounded-md text-purple-800 bg-purple-100 hover:bg-purple-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-purple-500">Queue Job</button>`;
    var new_continue_job_button_string = `
        <button type="button" class="inline-flex items-center justify-center px-3 py-1.5 border border-transparent shadow-sm text-sm font-medium rounded-md text-purple-800 bg-purple-100 hover:bg-purple-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-purple-500">Continue</button>`;


    const parser = new DOMParser();


    // modify bug parameters and add new parameters
    try {
        if (
            (building_elements.children[1].children[building_elements.children[1].children.length - 2].children[1].children[0].firstElementChild.firstElementChild.textContent.trim() == "Input Movies") &&
            (building_elements.children[1].children[building_elements.children[1].children.length - 2].children[1].children[1].firstElementChild.firstElementChild.textContent.trim() == "Input Micrographs") &&
            (building_elements.children[1].children[building_elements.children[1].children.length - 2].children[1].children[2].firstElementChild.firstElementChild.textContent.trim() == "Input Particles") &&
            (building_elements.children[1].children[building_elements.children[1].children.length - 2].children[1].children[3].firstElementChild.firstElementChild.textContent.trim() == "Input CryoRankers") &&
            (building_elements.children[1].children[building_elements.children[1].children.length - 2].children[1].children[4].firstElementChild.firstElementChild.textContent.trim() == "Input Templates") &&
            (building_elements.children[1].children[building_elements.children[1].children.length - 2].children[1].children[5].firstElementChild.firstElementChild.textContent.trim() == "Input Volumes") &&
            (building_elements.children[1].children[building_elements.children[1].children.length - 2].children[1].children[6].firstElementChild.firstElementChild.textContent.trim() == "Input Masks")
        ) {
            // modify bug parameters bar
            var building_parameters_part_element = building_elements.children[1].lastElementChild;
            var new_parameters_bar_doc = parser.parseFromString(new_parameters_bar_string, "text/html");
            var new_parameters_bar = new_parameters_bar_doc.body.firstElementChild;
            building_parameters_part_element.removeChild(building_parameters_part_element.firstElementChild);
            building_parameters_part_element.insertBefore(new_parameters_bar, building_parameters_part_element.firstElementChild);

            // add parameters input elements
            var building_parameters_element = building_elements.children[1].lastElementChild;
            var new_parameters_doc = parser.parseFromString(new_parameters_string, "text/html");
            var new_parameters = new_parameters_doc.body.firstElementChild;
            building_parameters_element.removeChild(building_parameters_element.lastElementChild);
            building_parameters_element.appendChild(new_parameters);
        }
    } catch {}
    try {
        if (
            (building_elements.children[1].children[building_elements.children[1].children.length - 3].children[1].children[0].firstElementChild.firstElementChild.textContent.trim() == "Input Movies") &&
            (building_elements.children[1].children[building_elements.children[1].children.length - 3].children[1].children[1].firstElementChild.firstElementChild.textContent.trim() == "Input Micrographs") &&
            (building_elements.children[1].children[building_elements.children[1].children.length - 3].children[1].children[2].firstElementChild.firstElementChild.textContent.trim() == "Input Particles") &&
            (building_elements.children[1].children[building_elements.children[1].children.length - 3].children[1].children[3].firstElementChild.firstElementChild.textContent.trim() == "Input CryoRankers") &&
            (building_elements.children[1].children[building_elements.children[1].children.length - 3].children[1].children[4].firstElementChild.firstElementChild.textContent.trim() == "Input Templates") &&
            (building_elements.children[1].children[building_elements.children[1].children.length - 3].children[1].children[5].firstElementChild.firstElementChild.textContent.trim() == "Input Volumes") &&
            (building_elements.children[1].children[building_elements.children[1].children.length - 3].children[1].children[6].firstElementChild.firstElementChild.textContent.trim() == "Input Masks")
        ) {
            // modify bug parameters bar
            var building_parameters_part_element = building_elements.children[1].children[building_elements.children[1].children.length - 2];
            var new_parameters_bar_doc = parser.parseFromString(new_parameters_bar_string, "text/html");
            var new_parameters_bar = new_parameters_bar_doc.body.firstElementChild;
            building_parameters_part_element.removeChild(building_parameters_part_element.firstElementChild);
            building_parameters_part_element.insertBefore(new_parameters_bar, building_parameters_part_element.firstElementChild);

            // add parameters input elements
            var building_parameters_element = building_elements.children[1].children[building_elements.children[1].children.length - 2];
            var new_parameters_doc = parser.parseFromString(new_parameters_string, "text/html");
            var new_parameters = new_parameters_doc.body.firstElementChild;
            building_parameters_element.removeChild(building_parameters_element.lastElementChild);
            building_parameters_element.appendChild(new_parameters);
        }
    } catch {}
    // add pipeline type parameter, for checking which rest parameters would be used
    AddParameterGroup(project, jobid, "pipeline_type", false);

    // add queue/continue job button onclick func
    var building_queue_job_button_element = building_elements.lastElementChild;
    var new_queue_job_button_doc = parser.parseFromString(new_queue_job_button_string, "text/html");
    var new_queue_job_button = new_queue_job_button_doc.body.firstElementChild;
    new_queue_job_button.onclick = (function(parameters) {
        return function(event) {
            var building_elements = parameters["building_elements"];
            var project = parameters["project"];
            var jobid = parameters["jobid"];
            var cryosparc_username = parameters["cryosparc_username"];
            var cryosparc_password = parameters["cryosparc_password"];

            try {var parameter_pipeline_type = document.getElementById(project + "_" + jobid + "_cryowizard_pipeline_type").value;} catch {var parameter_pipeline_type = "";}
            try {var parameter_pixelsize = document.getElementById(project + "_" + jobid + "_cryowizard_pixelsize").value;} catch {var parameter_pixelsize = "";}
            try {var parameter_diameter = document.getElementById(project + "_" + jobid + "_cryowizard_diameter").value;} catch {var parameter_diameter = "";}
            try {var parameter_ctf_resolution = document.getElementById(project + "_" + jobid + "_cryowizard_ctf_resolution").value;} catch {var parameter_ctf_resolution = "";}
            try {var parameter_symmetry = document.getElementById(project + "_" + jobid + "_cryowizard_symmetry").value;} catch {var parameter_symmetry = "";}
            try {var parameter_gpu_num = document.getElementById(project + "_" + jobid + "_cryowizard_gpu_num").value;} catch {var parameter_gpu_num = "";}
            try {var parameter_inference_gpu_ids = document.getElementById(project + "_" + jobid + "_cryowizard_inference_gpu_ids").value;} catch {var parameter_inference_gpu_ids = "";}
            try {var parameter_get_type = document.getElementById(project + "_" + jobid + "_cryowizard_get_type").value;} catch {var parameter_get_type = "";}
            try {var parameter_cutoff_condition = document.getElementById(project + "_" + jobid + "_cryowizard_particle_cutoff_condition").value;} catch {var parameter_cutoff_condition = "";}
            var building_card_parameters = {
                "pipeline_type": parameter_pipeline_type,
                "pixelsize": parameter_pixelsize,
                "diameter": parameter_diameter,
                "ctf_resolution": parameter_ctf_resolution,
                "symmetry": parameter_symmetry,
                "gpu_num": parameter_gpu_num,
                "inference_gpu_ids": parameter_inference_gpu_ids,
                "get_type": parameter_get_type,
                "cutoff_condition": parameter_cutoff_condition,
            }

            // close building page
            var building_close_button_element = building_elements.firstElementChild.lastElementChild;
            for (var iteration = 0; iteration < 5; iteration++) {
                try {
                    building_close_button_element.click();
                } catch {}
            }

            // inform cryowizard server to run
            QueueCryowizardExternalJobAction(socket, cryosparc_username, cryosparc_password, project, jobid, building_card_parameters);
        };
    })({
        "building_elements": building_elements,
        "project": project,
        "jobid": jobid,
        "cryosparc_username": cryosparc_username,
        "cryosparc_password": cryosparc_password
    });
    var new_continue_job_button_doc = parser.parseFromString(new_continue_job_button_string, "text/html");
    var new_continue_job_button = new_continue_job_button_doc.body.firstElementChild;
    new_continue_job_button.onclick = (function(parameters) {
        return function(event) {
            var building_elements = parameters["building_elements"];
            var project = parameters["project"];
            var jobid = parameters["jobid"];
            var cryosparc_username = parameters["cryosparc_username"];
            var cryosparc_password = parameters["cryosparc_password"];

            // close building page
            var building_close_button_element = building_elements.firstElementChild.lastElementChild;
            for (var iteration = 0; iteration < 5; iteration++) {
                try {
                    building_close_button_element.click();
                } catch {}
            }

            // inform cryowizard server to continue
            ContinueCryowizardExternalJobAction(socket, cryosparc_username, cryosparc_password, project, jobid);
        };
    })({
        "building_elements": building_elements,
        "project": project,
        "jobid": jobid,
        "cryosparc_username": cryosparc_username,
        "cryosparc_password": cryosparc_password
    });
    building_queue_job_button_element.removeChild(building_queue_job_button_element.lastElementChild);
    building_queue_job_button_element.appendChild(new_continue_job_button);
    building_queue_job_button_element.appendChild(new_queue_job_button);

    // get ui parameters
    var last_turn_type = null;
    var CheckCryoWizardBuildingMenuInputs_Interval= setInterval((function(parameters) {
        return function(event) {
            var project = parameters["project"];
            var jobid = parameters["jobid"];
            var building_elements_dict = CryoWizardBuildingMenu_setInterval_Use();
            var building_elements = building_elements_dict["target_element"];
            var building_elements_children_ptr_shift = building_elements_dict["children_ptr_shift"];
            if (building_elements == null) {
                clearInterval(CheckCryoWizardBuildingMenuInputs_Interval);
            }
            else {
                // check linked inputs
                last_turn_type = CheckCryoWizardBuildingMenuInputs(socket, building_elements.children[1].children[building_elements.children[1].children.length - building_elements_children_ptr_shift].children[1], cryosparc_username, cryosparc_password, project, jobid, false, last_turn_type);
            }
        };
    })({
        "building_elements": building_elements,
        "project": project,
        "jobid": jobid,
        "cryosparc_username": cryosparc_username,
        "cryosparc_password": cryosparc_password
    }),100);

});


// catch cryowizard details tab
waitForCryoWizardDetailsMenu((building_elements) => {

    var chrome_storage_paramters = GetSessionStorageJsonItem("chrome_storage_paramters");
    var cryosparc_username = chrome_storage_paramters["cryosparc_username"];
    var cryosparc_password = chrome_storage_paramters["cryosparc_password"];

    var project_and_job_string = building_elements.firstElementChild.firstElementChild.firstElementChild.firstElementChild.firstElementChild.textContent;
    var project = project_and_job_string.split(" ")[0].trim();
    var jobid = project_and_job_string.split(" ")[1].trim();

    var new_parameters_bar_string = `
        <button type="button" class="sticky top-0 z-11 flex-shrink-0 h-9 flex justify-between items-center font-medium px-3 bg-gray-100 hover:bg-gray-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-3 focus-visible:ring-offset-gray-100 focus-visible:ring-inset">
            <h2 class="font-medium">Parameters</h2>
            <div class="inline-flex items-center space-x-2">
                <span slot="badge" class="flex space-x-1"></span>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="heroicon heroicon--outline h-4 w-4 stroke-2 text-gray-600" width="100%" height="100%">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 15l7-7 7 7"></path>
                </svg>
            </div>
        </button>`;

    var new_parameters_string = `
        <div class="bg-white p-2">
            <div class="flex flex-col">
                <div class="section expanded">
                    <span class="sticky top-9 z-2 flex flex-wrap w-full">
                        <div class="w-full h-1 bg-white flex-shrink-0"></div>
                        <button type="button" class="bg-gray-100 hover:bg-gray-200 rounded-md border border-gray-300 flex w-full items-center justify-between py-1 px-1 text-left text-sm leading-4 font-medium text-gray-800 hover:text-gray-900 focus:outline-none focus-visible:ring-inset focus-visible:ring-offset-1 focus-visible:ring-2 focus-visible:ring-blue-500">
                            <span class="flex items-center space-x-1">
                                <svg class="h-4 w-4 text-gray-500 group-hover:text-gray-500 group-focus:text-gray-600" stroke="none" fill="currentColor" viewBox="0 0 16 16">
                                    <path d="M4.42678 9.57322L7.82326 6.17678C7.92089 6.07915 8.07918 6.07915 8.17681 6.17678L11.5732 9.57322C11.7307 9.73072 11.6192 10 11.3964 10L4.60356 10C4.38083 10 4.26929 9.73071 4.42678 9.57322Z"></path>
                                </svg>
                                <span slot="header">
                                    <p class="text-sm text-gray-600">Parameters</p>
                                </span>
                            </span>
                            <span slot="badge" class="flex space-x-1">
                                <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800 tabular-nums"></span>
                            </span>
                        </button>
                    </span>
                    <div class="bg-white p-2">
                        <div slot="content" class="parametergroupcontainer flex flex-col space-y-3 pb-2"></div>
                    </div>
                </div>
            </div>
        </div>`;

    var new_continue_job_button_string = `
        <button type="button" class="inline-flex items-center justify-center px-3 py-1.5 border border-transparent shadow-sm text-sm font-medium rounded-md text-purple-800 bg-purple-100 hover:bg-purple-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-purple-500">Continue</button>`;

    const parser = new DOMParser();

    try {
        if (
            (building_elements.children[1].children[building_elements.children[1].children.length - 2].children[1].children[0].firstElementChild.firstElementChild.textContent.trim() == "Input Movies") &&
            (building_elements.children[1].children[building_elements.children[1].children.length - 2].children[1].children[1].firstElementChild.firstElementChild.textContent.trim() == "Input Micrographs") &&
            (building_elements.children[1].children[building_elements.children[1].children.length - 2].children[1].children[2].firstElementChild.firstElementChild.textContent.trim() == "Input Particles") &&
            (building_elements.children[1].children[building_elements.children[1].children.length - 2].children[1].children[3].firstElementChild.firstElementChild.textContent.trim() == "Input CryoRankers") &&
            (building_elements.children[1].children[building_elements.children[1].children.length - 2].children[1].children[4].firstElementChild.firstElementChild.textContent.trim() == "Input Templates") &&
            (building_elements.children[1].children[building_elements.children[1].children.length - 2].children[1].children[5].firstElementChild.firstElementChild.textContent.trim() == "Input Volumes") &&
            (building_elements.children[1].children[building_elements.children[1].children.length - 2].children[1].children[6].firstElementChild.firstElementChild.textContent.trim() == "Input Masks")
        ) {
            // modify bug parameters bar
            var building_parameters_part_element = building_elements.children[1].lastElementChild;
            var new_parameters_bar_doc = parser.parseFromString(new_parameters_bar_string, "text/html");
            var new_parameters_bar = new_parameters_bar_doc.body.firstElementChild;
            building_parameters_part_element.removeChild(building_parameters_part_element.firstElementChild);
            building_parameters_part_element.insertBefore(new_parameters_bar, building_parameters_part_element.firstElementChild);

            // add parameters input elements
            var building_parameters_element = building_elements.children[1].lastElementChild;
            var new_parameters_doc = parser.parseFromString(new_parameters_string, "text/html");
            var new_parameters = new_parameters_doc.body.firstElementChild;
            building_parameters_element.removeChild(building_parameters_element.lastElementChild);
            building_parameters_element.appendChild(new_parameters);
        }
    } catch {}
    try {
        if (
            (building_elements.children[1].children[building_elements.children[1].children.length - 3].children[1].children[0].firstElementChild.firstElementChild.textContent.trim() == "Input Movies") &&
            (building_elements.children[1].children[building_elements.children[1].children.length - 3].children[1].children[1].firstElementChild.firstElementChild.textContent.trim() == "Input Micrographs") &&
            (building_elements.children[1].children[building_elements.children[1].children.length - 3].children[1].children[2].firstElementChild.firstElementChild.textContent.trim() == "Input Particles") &&
            (building_elements.children[1].children[building_elements.children[1].children.length - 3].children[1].children[3].firstElementChild.firstElementChild.textContent.trim() == "Input CryoRankers") &&
            (building_elements.children[1].children[building_elements.children[1].children.length - 3].children[1].children[4].firstElementChild.firstElementChild.textContent.trim() == "Input Templates") &&
            (building_elements.children[1].children[building_elements.children[1].children.length - 3].children[1].children[5].firstElementChild.firstElementChild.textContent.trim() == "Input Volumes") &&
            (building_elements.children[1].children[building_elements.children[1].children.length - 3].children[1].children[6].firstElementChild.firstElementChild.textContent.trim() == "Input Masks")
        ) {
            // modify bug parameters bar
            var building_parameters_part_element = building_elements.children[1].children[building_elements.children[1].children.length - 2];
            var new_parameters_bar_doc = parser.parseFromString(new_parameters_bar_string, "text/html");
            var new_parameters_bar = new_parameters_bar_doc.body.firstElementChild;
            building_parameters_part_element.removeChild(building_parameters_part_element.firstElementChild);
            building_parameters_part_element.insertBefore(new_parameters_bar, building_parameters_part_element.firstElementChild);

            // add parameters input elements
            var building_parameters_element = building_elements.children[1].children[building_elements.children[1].children.length - 2];
            var new_parameters_doc = parser.parseFromString(new_parameters_string, "text/html");
            var new_parameters = new_parameters_doc.body.firstElementChild;
            building_parameters_element.removeChild(building_parameters_element.lastElementChild);
            building_parameters_element.appendChild(new_parameters);
        }
    } catch {}
    AddParameterGroup(project, jobid, "pipeline_type", true);
    CheckCryowizardExternalJobParametersAction(socket, cryosparc_username, cryosparc_password, project, jobid, true);

    // add continue job button onclick func
    var building_queue_job_button_element = building_elements.lastElementChild;
    var new_continue_job_button_doc = parser.parseFromString(new_continue_job_button_string, "text/html");
    var new_continue_job_button = new_continue_job_button_doc.body.firstElementChild;
    new_continue_job_button.onclick = (function(parameters) {
        return function(event) {
            var building_elements = parameters["building_elements"];
            var project = parameters["project"];
            var jobid = parameters["jobid"];
            var cryosparc_username = parameters["cryosparc_username"];
            var cryosparc_password = parameters["cryosparc_password"];

            // close building page
            var building_close_button_element = building_elements.firstElementChild.lastElementChild;
            for (var iteration = 0; iteration < 5; iteration++) {
                try {
                    building_close_button_element.click();
                } catch {}
            }

            // inform cryowizard server to continue
            ContinueCryowizardExternalJobAction(socket, cryosparc_username, cryosparc_password, project, jobid);
        };
    })({
        "building_elements": building_elements,
        "project": project,
        "jobid": jobid,
        "cryosparc_username": cryosparc_username,
        "cryosparc_password": cryosparc_password
    });
    building_queue_job_button_element.appendChild(new_continue_job_button);

    // get ui parameters
    var last_turn_type = null;
    var CheckCryoWizardBuildingMenuInputs_Interval= setInterval((function(parameters) {
        return function(event) {
            var project = parameters["project"];
            var jobid = parameters["jobid"];
            var building_elements_dict = CryoWizardBuildingMenu_setInterval_Use();
            var building_elements = building_elements_dict["target_element"];
            var building_elements_children_ptr_shift = building_elements_dict["children_ptr_shift"];
            if (building_elements == null) {
                clearInterval(CheckCryoWizardBuildingMenuInputs_Interval);
            }
            else {
                // check linked inputs
                last_turn_type = CheckCryoWizardBuildingMenuInputs(socket, building_elements.children[1].children[building_elements.children[1].children.length - building_elements_children_ptr_shift].children[1], cryosparc_username, cryosparc_password, project, jobid, true, last_turn_type);
            }
        };
    })({
        "building_elements": building_elements,
        "project": project,
        "jobid": jobid,
        "cryosparc_username": cryosparc_username,
        "cryosparc_password": cryosparc_password
    }),100);
});



















