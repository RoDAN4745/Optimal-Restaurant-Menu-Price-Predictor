document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("predict-form");
  const resultBox = document.getElementById("result");
  const predictionText = document.getElementById("prediction-text");

  form.addEventListener("submit", async (e) => {
    e.preventDefault(); // Prevent page reload

    const city = document.getElementById("city").value.trim();
    const cuisine = document.getElementById("cuisine").value.trim();
    const rating = parseFloat(document.getElementById("rating").value);

    // Basic front-end validation
    if (!city || !cuisine || isNaN(rating)) {
      alert("Please fill in all fields correctly.");
      return;
    }

    // Prepare data payload
    const payload = { city, cuisine, rating };

    try {
      // Send POST request to /predict
      const response = await fetch("/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`Server returned ${response.status}`);
      }

      const data = await response.json();
      if (data.predicted_price === undefined) {
        throw new Error("Unexpected server response format");
      }

      // Display the prediction
      predictionText.textContent = `₹${data.predicted_price.toFixed(2)}`;
      resultBox.style.display = "block";

    } catch (err) {
      console.error("Prediction request failed:", err);
      alert("Sorry, could not get a prediction. Please try again.");
    }
  });
});
