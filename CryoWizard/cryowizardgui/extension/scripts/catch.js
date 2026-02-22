

// switch to Buider tab: On
function waitForBuilderMenu(callback) {
    if (checkURL())
    {
        var project_and_workspace = ParseProjectAndWorkspace();
        var project = project_and_workspace["project"];
        var workspace = project_and_workspace["workspace"];

        const observer = new MutationObserver(() => {
            var elements = document.getElementsByTagName("span");
            if (elements.length > 0) {
                for (var i = 0; i < elements.length; i++) {
                    if (elements[i].textContent.trim() == ("New Job in " + project + " " + workspace)) {
                        elements[i].textContent = "New job in " + project + " " + workspace;
                        // observer.disconnect();
                        callback(elements[i]);
                    }
                }
            }
        });
        observer.observe(document.body, {childList: true, subtree: true});
    }
}

// switch to CryoWizard building tab: On
function waitForCryoWizardBuildingMenu(callback) {
    const observer = new MutationObserver(() => {
        var elements = document.getElementsByTagName("p");
        var target_element = null;
        if (elements.length > 0) {
            for (var i=0; i<elements.length; i++) {
                try {
                    target_element = elements[i].parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
                    if (
                        (target_element.children[0].children[0].lastElementChild.textContent.trim() == "External results") &&
                        (target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[0].firstElementChild.firstElementChild.textContent.trim() == "Input Movie") &&
                        (target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[1].firstElementChild.firstElementChild.textContent.trim() == "Input Micrograph") &&
                        (target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[2].firstElementChild.firstElementChild.textContent.trim() == "Input Particle") &&
                        (target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[3].firstElementChild.firstElementChild.textContent.trim() == "Input CryoRanker") &&
                        (target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[4].firstElementChild.firstElementChild.textContent.trim() == "Input Template") &&
                        (target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[5].firstElementChild.firstElementChild.textContent.trim() == "Input Volume") &&
                        (target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[6].firstElementChild.firstElementChild.textContent.trim() == "Input Mask") &&
                        (target_element.lastElementChild.lastElementChild.textContent.trim() == "Queue Job")
                    ) {
                        target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[0].firstElementChild.firstElementChild.textContent = "Input Movies";
                        target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[1].firstElementChild.firstElementChild.textContent = "Input Micrographs";
                        target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[2].firstElementChild.firstElementChild.textContent = "Input Particles";
                        target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[3].firstElementChild.firstElementChild.textContent = "Input CryoRankers";
                        target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[4].firstElementChild.firstElementChild.textContent = "Input Templates";
                        target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[5].firstElementChild.firstElementChild.textContent = "Input Volumes";
                        target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[6].firstElementChild.firstElementChild.textContent = "Input Masks";
                        // observer.disconnect();
                        console.log("building");
                        callback(target_element);
                    }
                } catch {}
                try {
                    target_element = elements[i].parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
                    if (
                        (target_element.children[0].children[0].lastElementChild.textContent.trim() == "External results") &&
                        (target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[0].firstElementChild.firstElementChild.textContent.trim() == "Input Movie") &&
                        (target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[1].firstElementChild.firstElementChild.textContent.trim() == "Input Micrograph") &&
                        (target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[2].firstElementChild.firstElementChild.textContent.trim() == "Input Particle") &&
                        (target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[3].firstElementChild.firstElementChild.textContent.trim() == "Input CryoRanker") &&
                        (target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[4].firstElementChild.firstElementChild.textContent.trim() == "Input Template") &&
                        (target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[5].firstElementChild.firstElementChild.textContent.trim() == "Input Volume") &&
                        (target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[6].firstElementChild.firstElementChild.textContent.trim() == "Input Mask") &&
                        (target_element.lastElementChild.lastElementChild.textContent.trim() == "Queue Job")
                    ) {
                        target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[0].firstElementChild.firstElementChild.textContent = "Input Movies";
                        target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[1].firstElementChild.firstElementChild.textContent = "Input Micrographs";
                        target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[2].firstElementChild.firstElementChild.textContent = "Input Particles";
                        target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[3].firstElementChild.firstElementChild.textContent = "Input CryoRankers";
                        target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[4].firstElementChild.firstElementChild.textContent = "Input Templates";
                        target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[5].firstElementChild.firstElementChild.textContent = "Input Volumes";
                        target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[6].firstElementChild.firstElementChild.textContent = "Input Masks";
                        // observer.disconnect();
                        console.log("building");
                        callback(target_element);
                    }
                } catch {}
            }
        }
    });
    observer.observe(document.body, { childList: true, subtree: true });
}

//  Used by setInterval in waitForCryoWizardBuildingMenu()
function CryoWizardBuildingMenu_setInterval_Use() {
    var elements = document.getElementsByTagName("p");
    var target_element = null;
    if (elements.length > 0) {
        for (var i=0; i<elements.length; i++) {
            try {
                target_element = elements[i].parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
                if (
                    (target_element.children[0].children[0].lastElementChild.textContent.trim() == "External results") &&
                    (target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[0].firstElementChild.firstElementChild.textContent.trim() == "Input Movies") &&
                    (target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[1].firstElementChild.firstElementChild.textContent.trim() == "Input Micrographs") &&
                    (target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[2].firstElementChild.firstElementChild.textContent.trim() == "Input Particles") &&
                    (target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[3].firstElementChild.firstElementChild.textContent.trim() == "Input CryoRankers") &&
                    (target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[4].firstElementChild.firstElementChild.textContent.trim() == "Input Templates") &&
                    (target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[5].firstElementChild.firstElementChild.textContent.trim() == "Input Volumes") &&
                    (target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[6].firstElementChild.firstElementChild.textContent.trim() == "Input Masks")
                ) {
                    console.log("building setInterval");
                    return {"target_element": target_element, "children_ptr_shift": 2};
                }
            } catch {}
            try {
                target_element = elements[i].parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
                if (
                    (target_element.children[0].children[0].lastElementChild.textContent.trim() == "External results") &&
                    (target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[0].firstElementChild.firstElementChild.textContent.trim() == "Input Movies") &&
                    (target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[1].firstElementChild.firstElementChild.textContent.trim() == "Input Micrographs") &&
                    (target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[2].firstElementChild.firstElementChild.textContent.trim() == "Input Particles") &&
                    (target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[3].firstElementChild.firstElementChild.textContent.trim() == "Input CryoRankers") &&
                    (target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[4].firstElementChild.firstElementChild.textContent.trim() == "Input Templates") &&
                    (target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[5].firstElementChild.firstElementChild.textContent.trim() == "Input Volumes") &&
                    (target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[6].firstElementChild.firstElementChild.textContent.trim() == "Input Masks")
                ) {
                    console.log("building setInterval");
                    return {"target_element": target_element, "children_ptr_shift": 3};
                }
            } catch {}
        }
    }
    return null;
}

// switch to CryoWizard details tab: On
function waitForCryoWizardDetailsMenu(callback) {
    const observer = new MutationObserver(() => {
        var elements = document.getElementsByTagName("p");
        var target_element = null;
        if (elements.length > 0) {
            for (var i=0; i<elements.length; i++) {
                try {
                    target_element = elements[i].parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
                    if (
                        (target_element.children[0].children[0].lastElementChild.textContent.trim() == "External results") &&
                        (target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[0].firstElementChild.firstElementChild.textContent.trim() == "Input Movie") &&
                        (target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[1].firstElementChild.firstElementChild.textContent.trim() == "Input Micrograph") &&
                        (target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[2].firstElementChild.firstElementChild.textContent.trim() == "Input Particle") &&
                        (target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[3].firstElementChild.firstElementChild.textContent.trim() == "Input CryoRanker") &&
                        (target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[4].firstElementChild.firstElementChild.textContent.trim() == "Input Template") &&
                        (target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[5].firstElementChild.firstElementChild.textContent.trim() == "Input Volume") &&
                        (target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[6].firstElementChild.firstElementChild.textContent.trim() == "Input Mask") &&
                        (!(target_element.lastElementChild.lastElementChild.textContent.trim() == "Queue Job"))
                    ) {
                        target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[0].firstElementChild.firstElementChild.textContent = "Input Movies";
                        target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[1].firstElementChild.firstElementChild.textContent = "Input Micrographs";
                        target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[2].firstElementChild.firstElementChild.textContent = "Input Particles";
                        target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[3].firstElementChild.firstElementChild.textContent = "Input CryoRankers";
                        target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[4].firstElementChild.firstElementChild.textContent = "Input Templates";
                        target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[5].firstElementChild.firstElementChild.textContent = "Input Volumes";
                        target_element.children[1].children[target_element.children[1].children.length - 2].children[1].children[6].firstElementChild.firstElementChild.textContent = "Input Masks";
                        // observer.disconnect();
                        console.log("detail");
                        callback(target_element);
                    }
                } catch {}
                try {
                    target_element = elements[i].parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
                    if (
                        (target_element.children[0].children[0].lastElementChild.textContent.trim() == "External results") &&
                        (target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[0].firstElementChild.firstElementChild.textContent.trim() == "Input Movie") &&
                        (target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[1].firstElementChild.firstElementChild.textContent.trim() == "Input Micrograph") &&
                        (target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[2].firstElementChild.firstElementChild.textContent.trim() == "Input Particle") &&
                        (target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[3].firstElementChild.firstElementChild.textContent.trim() == "Input CryoRanker") &&
                        (target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[4].firstElementChild.firstElementChild.textContent.trim() == "Input Template") &&
                        (target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[5].firstElementChild.firstElementChild.textContent.trim() == "Input Volume") &&
                        (target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[6].firstElementChild.firstElementChild.textContent.trim() == "Input Mask") &&
                        (!(target_element.lastElementChild.lastElementChild.textContent.trim() == "Queue Job"))
                    ) {
                        target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[0].firstElementChild.firstElementChild.textContent = "Input Movies";
                        target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[1].firstElementChild.firstElementChild.textContent = "Input Micrographs";
                        target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[2].firstElementChild.firstElementChild.textContent = "Input Particles";
                        target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[3].firstElementChild.firstElementChild.textContent = "Input CryoRankers";
                        target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[4].firstElementChild.firstElementChild.textContent = "Input Templates";
                        target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[5].firstElementChild.firstElementChild.textContent = "Input Volumes";
                        target_element.children[1].children[target_element.children[1].children.length - 3].children[1].children[6].firstElementChild.firstElementChild.textContent = "Input Masks";
                        // observer.disconnect();
                        console.log("detail");
                        callback(target_element);
                    }
                } catch {}
            }
        }
    });
    observer.observe(document.body, { childList: true, subtree: true });
}



// catch target element by textContent
function CatchTargetTextElement(element_tag_name, element_text_content)
{
    var target_element_dom = null;
    // while (true)
    for (var iteration = 0; iteration < 99999; iteration++)
    {
        var elements = document.getElementsByTagName(element_tag_name);
        if (elements.length > 0)
        {
            for (var i = 0; i < elements.length; i++)
            {
                if (elements[i].textContent.trim() == element_text_content)
                {
                    target_element_dom = elements[i];
                    break;
                }
            }
        }
        if (target_element_dom != null)
            break;
    }
    return target_element_dom;
}


