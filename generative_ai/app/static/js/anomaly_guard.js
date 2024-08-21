let chartInstance;

// Enable/disable the fetch button based on selections
function updateFetchButtonState() {
    const tableSelected = document.getElementById('table-select').value !== '';
    const featureSelected = document.getElementById('feature-select').value !== '';
    document.getElementById('fetch-data').disabled = !(tableSelected && featureSelected);
}

// Fetch table names and populate the select element
fetch('/anomaly_guard/api/tables')
    .then(response => response.json())
    .then(data => {
        const tableSelect = document.getElementById('table-select');
        data.forEach(table => {
            const option = document.createElement('option');
            option.value = table;
            option.textContent = table;
            tableSelect.appendChild(option);
        });
        updateFetchButtonState();
    });

// Fetch features for the selected table
document.getElementById('table-select').addEventListener('change', () => {
    const tableName = document.getElementById('table-select').value;
    const featureSelect = document.getElementById('feature-select');
    featureSelect.innerHTML = '<option value="" disabled selected>Select Feature</option>'; // Clear previous options and add default
    featureSelect.disabled = true;

    if (tableName) {
        fetch(`/anomaly_guard/api/features?table_name=${tableName}`)
            .then(response => response.json())
            .then(data => {
                data.forEach(feature => {
                    const option = document.createElement('option');
                    option.value = feature.feature_name;
                    option.textContent = feature.feature_name;
                    featureSelect.appendChild(option);
                });
                featureSelect.disabled = false;
                updateFetchButtonState();
            });
    } else {
        updateFetchButtonState();
    }
});

// Fetch data and display chart and details
document.getElementById('fetch-data').addEventListener('click', () => {
    const tableName = document.getElementById('table-select').value;
    const featureName = document.getElementById('feature-select').value;

    fetch(`/anomaly_guard/api/features?table_name=${tableName}`)
        .then(response => response.json())
        .then(data => {
            const selectedFeature = data.find(feature => feature.feature_name === featureName);
            const labels = ['Mean', 'Median', 'Std Dev', 'Min Value', 'Max Value', 'Anomaly Count'];
            const dataValues = [
                selectedFeature.mean,
                selectedFeature.median,
                selectedFeature.std_dev,
                selectedFeature.min_value,
                selectedFeature.max_value,
                selectedFeature.anomaly_count
            ];

            if (chartInstance) {
                chartInstance.destroy();
            }

            const ctx = document.getElementById('anomalyChart').getContext('2d');
            chartInstance = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: featureName,
                        data: dataValues,
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    },
                    plugins: {
                        legend: {
                            display: true,
                            labels: {
                                color: '#333'
                            }
                        },
                        tooltip: {
                            backgroundColor: 'rgba(0, 0, 0, 0.7)',
                            titleColor: '#fff',
                            bodyColor: '#fff'
                        }
                    }
                }
            });

            // Call OpenAI to generate a summary
            fetch('/anomaly_guard/api/generate_summary', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    feature_name: selectedFeature.feature_name,
                    mean: selectedFeature.mean,
                    median: selectedFeature.median,
                    std_dev: selectedFeature.std_dev,
                    min_value: selectedFeature.min_value,
                    max_value: selectedFeature.max_value,
                    anomaly_count: selectedFeature.anomaly_count
                })
            })
            .then(response => response.json())
            .then(summaryData => {
                // Update the summary section with the generated text
                document.getElementById('summary-text').innerHTML = summaryData.summary;
            });

            // Update details table
            const detailsBody = document.getElementById('details-body');
            detailsBody.innerHTML = ''; // Clear previous details

            const anomalies = JSON.parse(selectedFeature.anomalies);
            anomalies.forEach(anomaly => {
                const row = document.createElement('tr');
                const cell = document.createElement('td');
                cell.textContent = JSON.stringify(anomaly, null, 2);
                row.appendChild(cell);
                detailsBody.appendChild(row);
            });
        });
});

document.getElementById('feature-select').addEventListener('change', updateFetchButtonState);
