

// html add new project card
function AddProjectCard()
{
    var new_workflow_name = CreateSessionStorageProjectCardInfo(true);
    UpdateProjectCard(new_workflow_name);
}

// html delete project card
function DeleteProjectCard(target_workflow_name)
{
    var session_storage_delete_results = DeleteSessionStorageProjectCardInfo(target_workflow_name);
    var project_card_dict = GetSessionStorageJsonItem("project_card_dict");
    var project_card_workflow_info_dict = project_card_dict["project_card_info"];
    var project_card_active_workflow = project_card_dict["active_workflow"];

    var next_active_work_flow_name = null;
    if (!(project_card_active_workflow in project_card_workflow_info_dict))
    {
        if (Object.keys(project_card_workflow_info_dict).length > 0)
        {
            for (var workflow_name in project_card_workflow_info_dict)
            {
                next_active_work_flow_name = workflow_name;
                break
            }
        }
    }
    UpdateProjectCard(next_active_work_flow_name);
}


// update html project card info
function UpdateProjectCard(active_workflow_name=null)
{
    var project_card_dict = GetSessionStorageJsonItem("project_card_dict");
    if (active_workflow_name != null)
    {
        project_card_dict["active_workflow"] = active_workflow_name;
        SetSessionStorageJsonItem("project_card_dict", project_card_dict);
        project_card_dict = GetSessionStorageJsonItem("project_card_dict");
    }

    var project_card_workflow_info_dict = project_card_dict["project_card_info"];
    var project_card_active_workflow = project_card_dict["active_workflow"];
    var project_card_elements = null;
    var project_card_content_div_nav = document.getElementById("project_card_content_div_nav");
    var project_card_content_div_tab = document.getElementById("project_card_content_div_tab");
    var project_card_elements_nav_doc = null;
    var project_card_elements_nav = null;
    var project_card_elements_tab_doc = null;
    var project_card_elements_tab = null;
    const parser = new DOMParser();

    project_card_content_div_nav.replaceChildren();
    project_card_content_div_tab.replaceChildren();
    if (Object.keys(project_card_workflow_info_dict).length > 0)
    {
        for (var workflow_name in project_card_workflow_info_dict)
        {
            project_card_elements = CreateProjectCardElements(workflow_name);

            project_card_elements_nav_doc = parser.parseFromString(project_card_elements["new_project_card_content_nav_str"], "text/html");
            project_card_elements_nav = project_card_elements_nav_doc.body.firstElementChild;
            project_card_content_div_nav.appendChild(project_card_elements_nav);
            project_card_elements_tab_doc = parser.parseFromString(project_card_elements["new_project_card_content_tab_str"], "text/html");
            project_card_elements_tab = project_card_elements_tab_doc.body.firstElementChild;
            project_card_content_div_tab.appendChild(project_card_elements_tab);

            UpdateProjectCardElementsValue(workflow_name);
        }
    }


    var project_card_count = GetSessionStorageJsonItem("project_card_count");
    project_card_dict = GetSessionStorageJsonItem("project_card_dict");
    console.log(project_card_count);
    console.log(project_card_dict);

}


