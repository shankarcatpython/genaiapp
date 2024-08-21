document.addEventListener("DOMContentLoaded", function() {
    // Example: Alert when a card is clicked
    const smartPromptCard = document.querySelector(".card-title:contains('SmartPrompt')");
    const anomalyGuardCard = document.querySelector(".card-title:contains('AnomalyGuard')");

    if (smartPromptCard) {
        smartPromptCard.addEventListener("click", function() {
            alert("SmartPrompt card clicked!");
        });
    }

    if (anomalyGuardCard) {
        anomalyGuardCard.addEventListener("click", function() {
            alert("AnomalyGuard card clicked!");
        });
    }
});
