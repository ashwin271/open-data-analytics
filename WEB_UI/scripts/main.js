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
// async function viewReconciliationJob() {
//     let jobID = document.getElementById("jobID").value;
//     if (!jobID) {
//         alert("Please enter a Job ID");
//         return;
//     }

//     try {
//         const response = await fetch(`${BASE_URL}/reconciliations/${jobID}?uid=${userID}`);
//         const job = await response.json();

//         let jobDetails = `
//             <p>Job ID: ${job.job_id}</p>
//             <p>User ID: ${job.uid}</p>
//             <p>Workflow Template: ${job.workflow_template_name}</p>
//             <p>Status: ${job.status}</p>
//             <p>Created At: ${job.created_at}</p>
//             <p>Completed At: ${job.completed_at || 'N/A'}</p>
//             <p>Sources: ${JSON.stringify(job.sources, null, 2)}</p>
//             <p>Report: ${JSON.stringify(job.report, null, 2)}</p>
//         `;
//         document.getElementById('jobDetails').innerHTML = jobDetails;
//     } catch (error) {
//         alert(`Error viewing job: ${error.message}`);
//     }
// }

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

    async function viewReconciliationJob(jobID) {
        // if (!jobID) {
        //     alert("Please enter a Job ID");
        //     return;
        // }

        try {
            // const response = await fetch(`${BASE_URL}/reconciliations/${jobID}?uid=${userID}`);
            // if (!response.ok) {
            //     alert("Error retrieving job details.");
            //     return;
            // }
            // const job = await response.json();
            // const report = job.report;

            // if (!report) {
            //     alert("Report not found for the specified job.");
            //     return;
            // }

            const report = {
                export_table: {
                    "daily_operations": [
                        {"date": "2024-08-01", "food_sales": 1500, "beverage_sales": 600, "dessert_sales": 400, "appetizer_sales": 300},
                        {"date": "2024-08-02", "food_sales": 1600, "beverage_sales": 700, "dessert_sales": 420, "appetizer_sales": 320},
                        {"date": "2024-08-03", "food_sales": 1700, "beverage_sales": 750, "dessert_sales": 430, "appetizer_sales": 340},
                        {"date": "2024-08-04", "food_sales": 1400, "beverage_sales": 650, "dessert_sales": 415, "appetizer_sales": 310},
                        {"date": "2024-08-05", "food_sales": 1550, "beverage_sales": 620, "dessert_sales": 405, "appetizer_sales": 305}
                    ],
                    "monthly_expenses": [
                        {"month": "2024-07", "rent": 2000, "utilities": 350, "salaries": 5000, "marketing": 800},
                        {"month": "2024-08", "rent": 2000, "utilities": 360, "salaries": 5200, "marketing": 850},
                        {"month": "2024-09", "rent": 2100, "utilities": 370, "salaries": 5300, "marketing": 900}
                    ],
                    "customer_feedback": [
                        {"date": "2024-08-01", "positive_feedback": 50, "negative_feedback": 5},
                        {"date": "2024-08-02", "positive_feedback": 60, "negative_feedback": 7},
                        {"date": "2024-08-03", "positive_feedback": 70, "negative_feedback": 6},
                        {"date": "2024-08-04", "positive_feedback": 55, "negative_feedback": 8},
                        {"date": "2024-08-05", "positive_feedback": 65, "negative_feedback": 5}
                    ],
                    "inventory_management": [
                        {"inventory_date": "2024-08-01", "ingredients_cost": 750, "beverages_cost": 150},
                        {"inventory_date": "2024-08-02", "ingredients_cost": 780, "beverages_cost": 160},
                        {"inventory_date": "2024-08-03", "ingredients_cost": 790, "beverages_cost": 170},
                        {"inventory_date": "2024-08-04", "ingredients_cost": 760, "beverages_cost": 140},
                        {"inventory_date": "2024-08-05", "ingredients_cost": 770, "beverages_cost": 155}
                    ]
                },
                analytics: [
                    {
                        'axes': { 'x_label': 'Quarter', 'y_label': 'Revenue' },
                        'data': {
                            'x': ['Q1', 'Q2', 'Q3', 'Q4'],
                            'y': [
                                { 'label': 'Product A', 'values': [30000, 45000, 56000, 70000] },
                                { 'label': 'Product B', 'values': [20000, 30000, 40000, 35000] },
                                { 'label': 'Product C', 'values': [15000, 25000, 30000, 45000] }
                            ]
                        },
                        'title': 'Quarterly Revenue for Products',
                        'type': 'bar'
                    },
                    {
                        'axes': { 'x_label': 'Week', 'y_label': 'Users' },
                        'data': {
                            'x': ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5'],
                            'y': [
                                { 'label': 'Active Users', 'values': [120, 200, 180, 300, 290] },
                                { 'label': 'New Users', 'values': [50, 80, 110, 90, 100] }
                            ]
                        },
                        'title': 'Weekly Active and New Users',
                        'type': 'line'
                    },
                    {
                        'axes': { 'x_label': 'Rainfall (mm)', 'y_label': 'Crop Growth (cm)' },
                        'data': {
                            'x': [20, 30, 40, 50, 60, 70],
                            'y': [
                                { 'label': 'Wheat', 'values': [4, 5, 5.5, 6, 6.5, 7] },
                                { 'label': 'Corn', 'values': [3.5, 4.5, 5, 5.5, 6, 6.2] }
                            ]
                        },
                        'title': 'Rainfall vs Crop Growth',
                        'type': 'scatter'
                    },
                    {
                        'data': {
                            'labels': ['Excellent', 'Good', 'Average', 'Poor'],
                            'percentages': [40, 35, 15, 10]
                        },
                        'title': 'Customer Satisfaction Levels',
                        'type': 'pie'
                    }
                ]
            };

            // Destructure the report for charts and tables
            const { analytics, export_table } = report;
            console.log(export_table)

            // Create charts
            if (analytics) {
                // document.getElementById('chartContainer').innerHTML = '';
                analytics.forEach(createChart);
            }

            // Create tables
            if (export_table) {
                document.getElementById('dataTables').innerHTML = '';
                Object.keys(export_table).forEach(section => createTableForSection(section, export_table[section]));
            }
        } catch (error) {
            console.error("Error fetching job details:", error);
            alert(`Error viewing job: ${error.message}`);
        }
    }


const colorPalette = [
    'rgba(54, 162, 235, 0.7)',
    'rgba(255, 99, 132, 0.7)',
    'rgba(255, 206, 86, 0.7)',
    'rgba(75, 192, 192, 0.7)',
    'rgba(153, 102, 255, 0.7)',
    'rgba(255, 159, 64, 0.7)',
    'rgba(201, 203, 207, 0.7)',
    'rgba(255, 105, 180, 0.7)',
    'rgba(60, 180, 75, 0.7)',
    'rgba(230, 25, 75, 0.7)',
];

function getColor(index) {
    return colorPalette[index % colorPalette.length];
}

function createChart(chartData) {
    const chartTile = document.createElement('div');
    chartTile.className = 'chart-tile';

    const title = document.createElement('div');
    title.className = 'section-title';
    title.textContent = chartData.title;

    const chartContent = document.createElement('div');
    chartContent.className = 'chart-content';

    const canvas = document.createElement('canvas');

    chartContent.appendChild(canvas);
    chartTile.appendChild(title);
    chartTile.appendChild(chartContent);

    document.getElementById('chartContainer').appendChild(chartTile);

    const ctx = canvas.getContext('2d');
    const config = createChartConfig(chartData);
    new Chart(ctx, config);

    chartTile.addEventListener('click', () => openFullscreen(config, chartData.title));
}

function createChartConfig(chartData) {
    const config = {
        type: chartData.type,
        data: {},
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: false // Custom title already displayed
                }
            },
            scales: {}
        }
    };

    if (['bar', 'line', 'scatter'].includes(chartData.type)) {
        config.data.labels = chartData.data.x;
        config.data.datasets = chartData.data.y.map((series, i) => ({
            label: series.label,
            data: series.values,
            backgroundColor: getColor(i),
            borderColor: getColor(i),
            borderWidth: 1,
        }));

        config.options.scales.x = { title: { display: true, text: chartData.axes.x_label } };
        config.options.scales.y = { title: { display: true, text: chartData.axes.y_label } };
    }

    if (chartData.type === 'pie') {
        config.data.labels = chartData.data.labels;
        config.data.datasets = [{
            data: chartData.data.percentages,
            backgroundColor: chartData.data.labels.map((_, i) => getColor(i)),
            borderColor: chartData.data.labels.map((_, i) => getColor(i)),
        }];
    }

    return config;
}

function openFullscreen(config, title) {
    const overlay = document.querySelector('.fullscreen-overlay');
    const fullscreenCanvas = document.getElementById('fullscreenChart');
    const closeBtn = document.querySelector('.close-btn');

    overlay.style.display = 'flex';

    const newCanvas = fullscreenCanvas.cloneNode(true);
    fullscreenCanvas.replaceWith(newCanvas);

    const ctx = newCanvas.getContext('2d');
    new Chart(ctx, {
        type: config.type,
        data: config.data,
        options: {
            ...config.options,
            plugins: {
                title: {
                    display: true,
                    text: title
                }
            }
        }
    });

    closeBtn.onclick = () => {
        overlay.style.display = 'none';
    };
}

function createTableForSection(sectionName, sectionData) {
    const container = document.createElement('div');
    container.className = 'section';

    const header = document.createElement('div');
    header.className = 'section-title';
    header.textContent = sectionName.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
    container.appendChild(header);

    const tableContainer = document.createElement('div');
    tableContainer.className = 'section-content';

    const table = document.createElement('table');

    const thead = document.createElement('thead');
    const headRow = document.createElement('tr');
    const columnNames = Object.keys(sectionData[0]);
    columnNames.forEach(columnName => {
        const th = document.createElement('th');
        th.textContent = columnName.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
        headRow.appendChild(th);
    });
    thead.appendChild(headRow);
    table.appendChild(thead);

    const tbody = document.createElement('tbody');
    sectionData.forEach(rowData => {
        const row = document.createElement('tr');
        columnNames.forEach(columnName => {
            const td = document.createElement('td');
            td.textContent = rowData[columnName];
            row.appendChild(td);
        });
        tbody.appendChild(row);
    });
    table.appendChild(tbody);

    tableContainer.appendChild(table);
    container.appendChild(tableContainer);
    document.getElementById('dataTables').appendChild(container);
}
