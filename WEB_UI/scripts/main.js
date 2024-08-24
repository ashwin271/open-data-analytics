const BASE_URL = "http://localhost:8000"; // Adjust this to your actual API base URL
let userID;
let currentJobsPage = 1;
let currentTemplatesPage = 1;
const itemsPerPage = 3; // Number of items per page for pagination

// Load initial content
window.onload = function () {
    while (!userID) {
        userID = prompt("Enter your User ID:").trim();
        if (!userID) {
            userID = null;
            alert("User ID is required to proceed.");
        }
    }
    loadNewJob(); // Default view on load
};

// Load New Job content
function loadNewJob() {
    document.getElementById('content').innerHTML = `
        <h2>Start New Job</h2>
        <input type="text" id="templateName" placeholder="Workflow Template Name">
        <div id="csvInputs"></div>
        <button class="button" onclick="fetchTemplate()">Fetch Template</button>
    `;
}

// Fetch template
async function fetchTemplate() {
    let templateName = document.getElementById("templateName").value.trim();
    if (!templateName) {
        alert("Please enter a workflow template name");
        return;
    }

    let response;

    try {
        response = await fetch(`${BASE_URL}/templates/${templateName}?uid=${userID}&visibility=private`);
        if (!response.ok) {
            response = await fetch(`${BASE_URL}/templates/${templateName}?uid=${userID}&visibility=public`);
        }
    } catch (error) {
        alert(`Error fetching template: ${error.message}`);
        return;
    }

    if (response.ok) {
        const workflowTemplate = await response.json();
        const sources = workflowTemplate.data.sources;
        const csvInputs = document.getElementById('csvInputs');
        csvInputs.innerHTML = '';

        for (let sourceKey in sources) {
            const sourceTemplateName = sources[sourceKey];
            csvInputs.innerHTML += `
                <div>
                    <label for="csv_${sourceKey}">Enter CSV file for ${sourceKey} (${sourceTemplateName}):</label>
                    <input type="file" id="csv_${sourceKey}" accept=".csv"><br>
                </div>
            `;
        }

        csvInputs.innerHTML += `<button class="button" onclick="startNewReconciliation()">Start Reconciliation</button>`;
    } else {
        alert(`Workflow template '${templateName}' not found.`);
    }
}

// Custom CSV processing logic
function processCSV(file, columnMappings) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = function (event) {
            const lines = event.target.result.split("\n").filter(line => line.trim());
            const headers = lines[0].split(",");
            const processedData = [];

            lines.slice(1).forEach(line => {
                const row = line.split(",");
                if (row.length !== headers.length) return;
                const entry = {};

                for (const key in columnMappings) {
                    const index = columnMappings[key] - 1; // Adjusted for 0-based index
                    if (index < row.length && row[index].trim()) {
                        entry[key] = row[index].trim();
                    } else {
                        return; // If any column is missing or empty, skip the line
                    }
                }

                if (Object.keys(entry).length === Object.keys(columnMappings).length) {
                    processedData.push(entry);
                }
            });

            resolve(processedData);
        };

        reader.onerror = function (event) {
            reject(event.target.error);
        };

        reader.readAsText(file);
    });
}

// Function to start new reconciliation
async function startNewReconciliation() {
    const templateName = document.getElementById("templateName").value;
    let reconciliationSources = {};

    try {
        let response = await fetch(`${BASE_URL}/templates/${templateName}?uid=${userID}&visibility=private`);
        if (!response.ok) {
            response = await fetch(`${BASE_URL}/templates/${templateName}?uid=${userID}&visibility=public`);
        }

        const workflowTemplate = await response.json();
        if (!workflowTemplate) {
            alert(`Workflow template '${templateName}' not found.`);
            return;
        }

        const sources = workflowTemplate.data.sources;
        for (const [sourceKey, baseTemplateName] of Object.entries(sources)) {
            // Fetch base template for each source
            let baseTemplateResponse = await fetch(`${BASE_URL}/templates/${baseTemplateName}?uid=${userID}&visibility=private`);
            if (!baseTemplateResponse.ok) {
                baseTemplateResponse = await fetch(`${BASE_URL}/templates/${baseTemplateName}?uid=${userID}&visibility=public`);
            }
            const baseTemplate = await baseTemplateResponse.json();
            if (!baseTemplate) {
                alert(`Base template '${baseTemplateName}' for source '${sourceKey}' not found.`);
                return;
            }

            const columnMappings = baseTemplate.data.column_mappings;
            if (!columnMappings || Object.keys(columnMappings).length === 0) {
                alert(`Invalid column mappings for ${sourceKey} using base template '${baseTemplateName}'.`);
                return;
            }

            const csvInput = document.getElementById(`csv_${sourceKey}`);
            if (!csvInput.files.length) {
                alert(`Please upload a CSV file for ${sourceKey}`);
                return;
            }

            const file = csvInput.files[0];
            const processedData = await processCSV(file, columnMappings);
            reconciliationSources[sourceKey] = processedData;
        }

        const reconciliationData = {
            uid: userID,
            workflow_template_name: templateName,
            sources: reconciliationSources,
        };

        response = await fetch(`${BASE_URL}/reconciliations`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(reconciliationData),
        });

        const result = await response.json();
        alert(`Reconciliation job started successfully! Job ID: ${result.job_id}`);
    } catch (error) {
        alert(`Error starting reconciliation job: ${error.message}`);
    }
}

// Load View Jobs content
function loadViewJobs() {
    document.getElementById('content').innerHTML = `
        <h2>View Reconciliation Jobs</h2>
        <button class="button" onclick="listReconciliationJobs(currentJobsPage)">List Jobs</button><br>
        <label for="jobID">Enter Job ID:</label>
        <input type="text" id="jobID" placeholder="Job ID"><br>
        <button class="button" onclick="viewReconciliationJob()">View Job</button>
        <div id="jobDetails"></div>
    `;
}

// Function to list reconciliation jobs with pagination
async function listReconciliationJobs(page) {
    try {
        const response = await fetch(`${BASE_URL}/reconciliations?uid=${userID}&page=${page}&count=${itemsPerPage}`);
        const data = await response.json();

        let jobList = "<h3>Job List:</h3>";
        data.result.forEach(job => {
            jobList += `
                <p>Job ID: ${job.job_id}</p>
                <p>Workflow Template: ${job.workflow_template_name}</p>
                <p>Status: ${job.status}</p>
                <p>Created At: ${job.created_at}</p>
                <p>Completed At: ${job.completed_at || 'N/A'}</p>
                <hr>
            `;
        });
        jobList += `
            <div>
                <button class="button" onclick="listReconciliationJobs(${data.page - 1})" ${data.page <= 1 ? 'disabled' : ''}>Previous</button>
                <button class="button" onclick="listReconciliationJobs(${data.page + 1})" ${data.page >= data.total_pages ? 'disabled' : ''}>Next</button>
                <p>Page ${data.page} of ${data.total_pages}</p>
            </div>
        `;
        document.getElementById('jobDetails').innerHTML = jobList;
    } catch (error) {
        alert(`Error listing jobs: ${error.message}`);
    }
}

// Function to view specific reconciliation job
async function viewReconciliationJob() {
    let jobID = document.getElementById("jobID").value;
    if (!jobID) {
        alert("Please enter a Job ID");
        return;
    }

    try {
        const response = await fetch(`${BASE_URL}/reconciliations/${jobID}?uid=${userID}`);
        const job = await response.json();

        let jobDetails = `
            <p>Job ID: ${job.job_id}</p>
            <p>User ID: ${job.uid}</p>
            <p>Workflow Template: ${job.workflow_template_name}</p>
            <p>Status: ${job.status}</p>
            <p>Created At: ${job.created_at}</p>
            <p>Completed At: ${job.completed_at || 'N/A'}</p>
            <p>Sources: ${JSON.stringify(job.sources, null, 2)}</p>
            <p>Report: ${JSON.stringify(job.report, null, 2)}</p>
        `;
        document.getElementById('jobDetails').innerHTML = jobDetails;
    } catch (error) {
        alert(`Error viewing job: ${error.message}`);
    }
}

// Load Template Manager content
function loadTemplateManager() {
    document.getElementById('content').innerHTML = `
        <h2>Template Manager</h2>
        <button class="button" onclick="loadCreateTemplate()">Create Template</button>
        <button class="button" onclick="loadBulkCreateTemplate()">Bulk Create Templates</button>
        <button class="button" onclick="loadFilterTemplates()">Filter Templates</button>
        <button class="button" onclick="loadViewTemplate()">View Template</button>
        <button class="button" onclick="loadEditTemplate()">Edit Template</button>
        <button class="button" onclick="loadDeleteTemplate()">Delete Template</button>
        <div id="templateDetails"></div>
    `;
}

// Load Create Template form
function loadCreateTemplate() {
    document.getElementById('templateDetails').innerHTML = `
        <h3>Create Template</h3>
        <textarea id="templateData" placeholder='{"name": "templateName", "type": "templateType", "data": {...}}'></textarea><br>
        <button class="button" onclick="createTemplate()">Submit</button>
    `;
}

// Function to create a template
async function createTemplate() {
    const templateData = document.getElementById("templateData").value;
    try {
        const parsedData = JSON.parse(templateData);
        if (!parsedData.name || !parsedData.type) {
            alert("Invalid template data. 'name' and 'type' are required fields.");
            return;
        }

        const response = await fetch(`${BASE_URL}/templates`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                uid: userID,
                name: parsedData.name,
                type: parsedData.type,
                data: parsedData
            }),
        });

        if (response.ok) {
            alert(`Template '${parsedData.name}' created successfully.`);
        } else {
            const errorText = await response.text();
            alert(`Error creating template: ${errorText}`);
        }
    } catch (error) {
        alert(`Error creating template: ${error.message}`);
    }
}

// Load Bulk Create Template form
function loadBulkCreateTemplate() {
    document.getElementById('templateDetails').innerHTML = `
        <h3>Bulk Create Templates</h3>
        <input type="file" id="templateFiles" accept=".json" multiple><br>
        <button class="button" onclick="bulkCreateTemplates()">Submit</button>
    `;
}

// Function to bulk create templates
async function bulkCreateTemplates() {
    const files = document.getElementById("templateFiles").files;
    if (files.length === 0) {
        alert("Please select at least one file.");
        return;
    }

    for (const file of files) {
        try {
            const text = await file.text();
            const parsedData = JSON.parse(text);
            if (!parsedData.name || !parsedData.type) {
                alert(`Invalid template data in file '${file.name}'. 'name' and 'type' are required fields.`);
                continue;
            }

            const response = await fetch(`${BASE_URL}/templates`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    uid: userID,
                    name: parsedData.name,
                    type: parsedData.type,
                    data: parsedData
                }),
            });

            if (response.ok) {
                alert(`Template '${parsedData.name}' created successfully.`);
            } else {
                const errorText = await response.text();
                alert(`Error creating template '${parsedData.name}': ${errorText}`);
            }
        } catch (error) {
            alert(`Error processing file '${file.name}': ${error.message}`);
        }
    }
}

// Load Filter Templates form
function loadFilterTemplates() {
    document.getElementById('templateDetails').innerHTML = `
        <h3>Filter Templates</h3>
        <label for="templateType">Template Type:</label>
        <select id="templateType">
            <option value="">All</option>
            <option value="base">Base</option>
            <option value="comparison">Comparison</option>
            <option value="workflow">Workflow</option>
        </select><br>
        <label for="nameSubstring">Name Substring:</label>
        <input type="text" id="nameSubstring" placeholder="Name Substring"><br>
        <label for="visibility">Visibility:</label>
        <select id="visibility">
            <option value="">All</option>
            <option value="public">Public</option>
            <option value="private">Private</option>
        </select><br>
        <button class="button" onclick="filterTemplates(currentTemplatesPage)">Filter</button>
        <div id="templateList"></div>
    `;
}

// Function to filter templates with pagination
async function filterTemplates(page) {
    const templateType = document.getElementById("templateType").value;
    const nameSubstring = document.getElementById("nameSubstring").value;
    const visibility = document.getElementById("visibility").value;

    let query = `${BASE_URL}/templates?uid=${userID}&page=${page}&count=${itemsPerPage}`;
    if (templateType) query += `&template_type=${templateType}`;
    if (nameSubstring) query += `&name_substring=${nameSubstring}`;
    if (visibility) query += `&visibility=${visibility}`;

    try {
        const response = await fetch(query);
        const data = await response.json();

        let templateList = "<h3>Template List:</h3>";
        data.result.forEach(template => {
            templateList += `
                <p>UID: ${template.uid}</p>
                <p>Name: ${template.name}</p>
                <p>Type: ${template.type}</p>
                <hr>
            `;
        });
        templateList += `
            <div>
            <button class="button" onclick="filterTemplates(${data.page - 1})" ${data.page <= 1 ? 'disabled' : ''}>Previous</button>
            <button class="button" onclick="filterTemplates(${data.page + 1})" ${data.page >= data.total_pages ? 'disabled' : ''}>Next</button>
            <p>Page ${data.page} of ${data.total_pages}</p>
        </div>
    `;
        document.getElementById('templateList').innerHTML = templateList;
    } catch (error) {
        alert(`Error filtering templates: ${error.message}`);
    }
}

// Load View Template form
function loadViewTemplate() {
    document.getElementById('templateDetails').innerHTML = `
    <h3>View Template</h3>
    <label for="viewTemplateName">Template Name:</label>
    <input type="text" id="viewTemplateName" placeholder="Template Name"><br>
    <label for="viewVisibility">Visibility:</label>
    <select id="viewVisibility">
        <option value="public">Public</option>
        <option value="private">Private</option>
    </select><br>
    <button class="button" onclick="viewTemplate()">View</button>
    <div id="templateData"></div>
`;
}

// Function to view a template
async function viewTemplate() {
    const templateName = document.getElementById("viewTemplateName").value;
    const visibility = document.getElementById("viewVisibility").value;

    try {
        const response = await fetch(`${BASE_URL}/templates/${templateName}?uid=${userID}&visibility=${visibility}`);
        const template = await response.json();

        const templateData = `
        <h3>${template.name}</h3>
        <p>Type: ${template.type}</p>
        <pre>${JSON.stringify(template.data, null, 2)}</pre>
    `;
        document.getElementById('templateData').innerHTML = templateData;
    } catch (error) {
        alert(`Error viewing template: ${error.message}`);
    }
}

// Load Edit Template form
function loadEditTemplate() {
    document.getElementById('templateDetails').innerHTML = `
    <h3>Edit Template</h3>
    <textarea id="editTemplateData" placeholder='{"name": "templateName", "type": "templateType", "data": {...}}'></textarea><br>
    <button class="button" onclick="editTemplate()">Submit</button>
`;
}

// Function to edit a template
async function editTemplate() {
    const templateData = document.getElementById("editTemplateData").value;
    try {
        const parsedData = JSON.parse(templateData);
        if (!parsedData.name || !parsedData.type) {
            alert("Invalid template data. 'name' and 'type' are required fields.");
            return;
        }

        const response = await fetch(`${BASE_URL}/templates/${parsedData.name}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                uid: userID,
                name: parsedData.name,
                type: parsedData.type,
                data: parsedData
            }),
        });

        if (response.ok) {
            alert(`Template '${parsedData.name}' updated successfully.`);
        } else if (response.status === 404) {
            alert(`Error: Template '${parsedData.name}' not found.`);
        } else {
            const errorText = await response.text();
            alert(`Error updating template: ${errorText}`);
        }
    } catch (error) {
        alert(`Error updating template: ${error.message}`);
    }
}

// Load Delete Template form
function loadDeleteTemplate() {
    document.getElementById('templateDetails').innerHTML = `
    <h3>Delete Template</h3>
    <label for="deleteTemplateName">Template Name:</label>
    <input type="text" id="deleteTemplateName" placeholder="Template Name"><br>
    <button class="button" onclick="deleteTemplate()">Delete</button>
`;
}

// Function to delete a template
async function deleteTemplate() {
    const templateName = document.getElementById("deleteTemplateName").value;
    if (!templateName) {
        alert("Please enter a template name");
        return;
    }

    const confirmDelete = confirm(`Are you sure you want to delete the template '${templateName}'?`);
    if (!confirmDelete) return;

    try {
        const response = await fetch(`${BASE_URL}/templates/${templateName}?uid=${userID}`, {
            method: 'DELETE',
        });

        if (response.ok) {
            alert("Template deleted successfully");
        } else {
            const errorText = await response.text();
            alert(`Error deleting template: ${errorText}`);
        }
    } catch (error) {
        alert(`Error deleting template: ${error.message}`);
    }
}

// Load User Data Manager content
function loadUserDataManager() {
    document.getElementById('content').innerHTML = `
    <h2>User Data Manager</h2>
    <button class="button" onclick="fetchUserData()">Fetch User Data</button>
    <button class="button" onclick="loadUpdateUserData()">Update User Data</button>
    <div id="userDataDetails"></div>
`;
}

// Function to fetch user data
async function fetchUserData() {
    try {
        const response = await fetch(`${BASE_URL}/userdata/fetch?uid=${userID}`);
        const data = await response.json();
        document.getElementById('userDataDetails').innerHTML = `
        <pre>${JSON.stringify(data, null, 2)}</pre>
    `;
    } catch (error) {
        alert(`Error fetching user data: ${error.message}`);
    }
}

// Load Update User Data form
function loadUpdateUserData() {
    document.getElementById('userDataDetails').innerHTML = `
    <h3>Update User Data</h3>
    <textarea id="updateUserData" placeholder='{"key": "value", ...}'></textarea><br>
    <button class="button" onclick="updateUserData()">Submit</button>
`;
}

// Function to update user data
async function updateUserData() {
    const userData = document.getElementById("updateUserData").value;
    try {
        const parsedData = JSON.parse(userData);

        const response = await fetch(`${BASE_URL}/userdata/update`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ uid: userID, data: parsedData }),
        });

        if (response.ok) {
            alert("User data updated successfully");
        } else {
            const errorText = await response.text();
            alert(`Error updating user data: ${errorText}`);
        }
    } catch (error) {
        alert(`Error updating user data: ${error.message}`);
    }
}

// Function to initialize the database
async function initDB() {
    try {
        const response = await fetch(`${BASE_URL}/setup_db`, {
            method: 'POST'
        });

        if (response.ok) {
            alert("Database initialized successfully");
        } else {
            const errorText = await response.text();
            alert(`Error initializing database: ${errorText}`);
        }
    } catch (error) {
        alert(`Error initializing database: ${error.message}`);
    }
}

