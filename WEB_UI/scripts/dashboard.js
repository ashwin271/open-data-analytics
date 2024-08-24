document.addEventListener('DOMContentLoaded', () => {
    async function viewReconciliationJob(jobID) {
        if (!jobID) {
            alert("Please enter a Job ID");
            return;
        }

        try {
            const response = await fetch(`${BASE_URL}/reconciliations/${jobID}?uid=${userID}`);
            if (!response.ok) {
                alert("Error retrieving job details.");
                return;
            }
            const job = await response.json();
            const report = job.report;

            if (!report) {
                alert("Report not found for the specified job.");
                return;
            }

            // Destructure the report for charts and tables
            const { analytics, export_table } = report;

            // Create charts
            if (analytics) {
                document.getElementById('chartContainer').innerHTML = '';
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
});

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
