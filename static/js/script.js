const time = document.getElementById("time");
const analysis = document.getElementById("analysis");
const forecasting = document.getElementById("forecasting");
const strategy = document.getElementById("strategy");
const btn = document.getElementById("btn");

const drugSelect = document.getElementById("drug");
const timeRangeSelect = document.getElementById("time_range");

// Navigation Buttons
time.addEventListener("click", () => {
    window.location.href = "/";
    console.log("Index route");
});

analysis.addEventListener("click", () => {
    window.location.href = "/analysis";
});

forecasting.addEventListener("click", () => {
    window.location.href = "/forecasting";
});

strategy.addEventListener("click", () => {
    window.location.href = "/strategy";
});

// Submit Button (with drug + time range)
btn.addEventListener("click", () => {
    const selectedDrug = drugSelect.value;
    console.log(selectedDrug);
    const selectedTime = timeRangeSelect.value;

    if (!selectedDrug || !selectedTime || selectedDrug === "disabled selected" || selectedTime === "disabled selected") {
        alert("⚠️ Please select both a drug and a time range before submitting.");
        return;
    }

    // Redirect with query parameters
    window.location.href = `/analysis?drug=${selectedDrug}&time_range=${selectedTime}`;
});
