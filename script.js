function nextPage(n) {
  document.querySelectorAll(".page").forEach(p => p.classList.remove("active"));
  document.getElementById("page" + n).classList.add("active");
}

async function generatePlan() {
  const data = {
    age: +document.getElementById("age").value,
    gender: document.getElementById("gender").value,
    height: +document.getElementById("height").value,
    weight: +document.getElementById("weight").value,
    goal: document.getElementById("goal").value,
    activity: document.getElementById("activity").value,
    budget: +document.getElementById("budget").value,
    food: document.getElementById("food").value,
    allergy: document.getElementById("allergy").value,
    meals: +document.getElementById("meals").value,
    indian: document.getElementById("indian").value
  };

  if (!data.age || !data.height || !data.weight || !data.budget) {
    alert("Please fill all required fields.");
    return;
  }

  document.getElementById("output").innerHTML = "<p>Generating your AI diet plan... ⏳</p>";
  nextPage(3);

  try {
    const response = await fetch("http://127.0.0.1:5000/generate-diet", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    });

    const result = await response.json();

    if (result.error) {
      document.getElementById("output").innerHTML =
        `<p style="color:red;">Error: ${result.error}</p>`;
      return;
    }

    document.getElementById("output").innerHTML = `
      <h3>Daily Targets</h3>
      <p><b>Calories:</b> ${result.calories} kcal</p>
      <p><b>Protein:</b> ${result.protein} g</p>

      <h3>AI Diet Plan</h3>
      <div class="meal-plan">${result.ai_plan.replace(/\n/g, "<br>")}</div>
    `;

  } catch (error) {
    document.getElementById("output").innerHTML =
      `<p style="color:red;">Server not responding. Make sure Flask is running.</p>`;
  }
}
