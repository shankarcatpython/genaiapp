function generateResponse() {
    var context = document.getElementById("contextWindow").value;

    fetch('/smart_prompt/process_context', {  // Update the URL to include the url_prefix
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'context=' + encodeURIComponent(context),
    })
    .then(response => response.json()) // Parse response as JSON
    .then(data => {
        var summarizeResponse = data.summarize_response;
        var suggestiveResponse = data.suggestive_response;
        document.getElementById('summary').innerText = summarizeResponse;
        document.getElementById('suggestion').innerText = suggestiveResponse;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
