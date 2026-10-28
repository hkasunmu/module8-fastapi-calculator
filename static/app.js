const form = document.getElementById("calculator-form");
const resultValue = document.getElementById("result-value");
const errorMessage = document.getElementById("error-message");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  resultValue.textContent = "Calculating...";
  errorMessage.textContent = "";

  const payload = {
    operation: document.getElementById("operation").value,
    a: Number(document.getElementById("a").value),
    b: Number(document.getElementById("b").value),
  };

  try {
    const response = await fetch("/calculate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Calculation failed");
    resultValue.textContent = String(Number(data.result.toPrecision(12)));
  } catch (error) {
    resultValue.textContent = "—";
    errorMessage.textContent = error.message;
  }
});
