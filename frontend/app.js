const API_URL = window.__API_URL__ || "";

const analyzeButton = document.getElementById("analyze");
const errorInput = document.getElementById("error");
const languageInput = document.getElementById("language");
const status = document.getElementById("status");
const result = document.getElementById("result");

analyzeButton.addEventListener("click", async () => {
  const rawLog = errorInput.value.trim();
  if (!rawLog) {
    status.textContent = "Please paste an error first.";
    return;
  }

  analyzeButton.disabled = true;
  status.textContent = "Analyzing error...";
  result.classList.add("hidden");

  try {
    const response = await fetch(`${API_URL}/api/v1/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ raw_log: rawLog, language: languageInput.value || null }),
    });

    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Analysis failed");

    document.getElementById("category").textContent = data.category.replaceAll("_", " ");
    document.getElementById("summary").textContent = data.summary;
    document.getElementById("rootCause").textContent = data.root_cause;
    document.getElementById("suggestedFix").textContent = data.suggested_fix;
    document.getElementById("confidence").textContent = `${Math.round(data.confidence * 100)}%`;

    const sources = document.getElementById("sources");
    sources.replaceChildren();
    for (const source of data.sources || []) {
      const item = document.createElement("li");
      item.textContent = `${source.source} (${source.relevance.toFixed(3)})`;
      sources.appendChild(item);
    }

    result.classList.remove("hidden");
    status.textContent = "Analysis complete.";
  } catch (error) {
    status.textContent = error.message;
  } finally {
    analyzeButton.disabled = false;
  }
});
