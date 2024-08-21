document.getElementById('symptomForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent form from submitting normally

    const symptoms = document.getElementById('symptoms').value;

    // Display a loading message
    document.getElementById('diagnosisResults').innerHTML = '<p>Processing symptoms, please wait...</p>';

    // Make an AJAX request to the server to get the diagnosis and prescription
    fetch('/local_trainer/get_diagnosis', {  // Update the endpoint to include the prefix
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ symptoms: symptoms })
    })
    .then(response => response.json())
    .then(data => {
        // Display the diagnosis and prescription
        document.getElementById('diagnosisResults').innerHTML = `<p><strong>Diagnosis:</strong> ${data.diagnosis}</p>
        <p><strong>Prescription:</strong> ${data.prescription}</p>`;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('diagnosisResults').innerHTML = '<p>Error processing symptoms. Please try again later.</p>';
    });
});
