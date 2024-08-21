document.getElementById('inputForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way
    const userInput = document.getElementById('user_input').value; // Get the user's input

    // Make a POST request to the '/process' route
    fetch('/gen_retrieve/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded', // Indicate that we're sending form data
        },
        body: 'user_input=' + encodeURIComponent(userInput) // Send the user's input
    })
    .then(response => response.json()) // Parse the JSON response from the server
    .then(data => {
        // Update the HTML content with the returned summary and prompt
        document.getElementById('summary').textContent = data.summary; 
        document.getElementById('prompt').textContent = data.prompt;
    })
    .catch(error => console.error('Error:', error)); // Log any errors that occur during the fetch
});
