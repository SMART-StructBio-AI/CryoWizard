
// create cryowizard external job action
function CreateCryowizardExternalJobAction(socket, cryosparc_username, cryosparc_password, project, workspace)
{
    socket.emit("create_cryowizard_external_job_action", cryosparc_username, cryosparc_password, project, workspace);

    // // create cryowizard external job action backinfo
    // socket.once("js_create_cryowizard_external_job_action", (res) => {
    //     var project = res["project"];
    //     var workspace = res["workspace"];
    //     var new_external_jobid = res["new_external_jobid"];
    // });
}

// // modify cryowizard external job action
// function ModifyCryowizardExternalJobAction(socket, cryosparc_username, cryosparc_password, project, jobid, parameters)
// {
//     socket.emit("modify_cryowizard_external_job_action", cryosparc_username, cryosparc_password, project, jobid, parameters);
//
//     // // create cryowizard external job action backinfo
//     // socket.once("js_modify_cryowizard_external_job_action", (res) => {
//     //     var project = res["project"];
//     //     var workspace = res["workspace"];
//     //     var new_external_jobid = res["new_external_jobid"];
//     // });
// }

// check cryowizard external job parameters action
function CheckCryowizardExternalJobParametersAction(socket, cryosparc_username, cryosparc_password, project, jobid, pipeline_type=false)
{
    socket.emit("check_cryowizard_external_job_parameters_action", cryosparc_username, cryosparc_password, project, jobid);

    // check cryowizard external job parameters action backinfo
    socket.once("js_check_cryowizard_external_job_parameters_action", (res) => {
        var project = res["project"];
        var jobid = res["jobid"];
        var parameters = res["parameters"];

        if (pipeline_type)
        {
            try {document.getElementById(project + "_" + jobid + "_cryowizard_pipeline_type").value = parameters["preset_pipeline_type"];} catch {}
        }
        else
        {
            try {document.getElementById(project + "_" + jobid + "_cryowizard_pixelsize").value = parameters['preset_pipeline_args']["raw_pixel_size"];} catch {}
            try {document.getElementById(project + "_" + jobid + "_cryowizard_diameter").value = parameters['preset_pipeline_args']["particle_diameter"];} catch {}
            try {document.getElementById(project + "_" + jobid + "_cryowizard_ctf_resolution").value = parameters['preset_pipeline_args']["ctf_fit_resolution"];} catch {}
            try {document.getElementById(project + "_" + jobid + "_cryowizard_symmetry").value = parameters['preset_pipeline_args']["symmetry"];} catch {}
            try {document.getElementById(project + "_" + jobid + "_cryowizard_gpu_num").value = parameters['preset_pipeline_args']["gpu_num"];} catch {}
            try {document.getElementById(project + "_" + jobid + "_cryowizard_inference_gpu_ids").value = parameters['preset_pipeline_args']["inference_gpu_ids"];} catch {}

            if (parameters["preset_pipeline_args"]["get_top_particles_num"] != null)
            {
                try {document.getElementById(project + "_" + jobid + "_cryowizard_get_type").value = "num";} catch {}
                try {document.getElementById(project + "_" + jobid + "_cryowizard_particle_cutoff_condition").value = parameters["preset_pipeline_args"]["get_top_particles_num"];} catch {}
            }
            else if (parameters["preset_pipeline_args"]["get_top_particles_score"] != null)
            {
                try {document.getElementById(project + "_" + jobid + "_cryowizard_get_type").value = "score";} catch {}
                try {document.getElementById(project + "_" + jobid + "_cryowizard_particle_cutoff_condition").value = parameters["preset_pipeline_args"]["get_top_particles_score"];} catch {}
            }
        }
    });
}


// queue cryowizard external job action
function QueueCryowizardExternalJobAction(socket, cryosparc_username, cryosparc_password, project, jobid, gui_parameters)
{
    socket.emit("queue_cryowizard_external_job_action", cryosparc_username, cryosparc_password, project, jobid, gui_parameters);

    // // queue cryowizard external job action backinfo
    // socket.once("js_queue_cryowizard_external_job_action", (res) => {
    //     var project = res["project"];
    //     var workspace = res["workspace"];
    //     var new_external_jobid = res["new_external_jobid"];
    // });
}

// continue cryowizard external job action
function ContinueCryowizardExternalJobAction(socket, cryosparc_username, cryosparc_password, project, jobid)
{
    socket.emit("continue_cryowizard_external_job_action", cryosparc_username, cryosparc_password, project, jobid);

    // // continue cryowizard external job action backinfo
    // socket.once("js_continue_cryowizard_external_job_action", (res) => {
    //     var project = res["project"];
    //     var workspace = res["workspace"];
    //     var new_external_jobid = res["new_external_jobid"];
    // });
}



