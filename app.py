from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# 🔑 Hugging Face API setup
HF_API_KEY = os.getenv("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")  
API_URL = "https://router.huggingface.co/hf-inference/models/google/flan-t5-large"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

def query_huggingface(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 500},
        "options": {"wait_for_model": True}
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()

    if isinstance(result, list):
        return result[0].get("generated_text", "No response generated.")
    elif isinstance(result, dict) and "error" in result:
        return f"Model error: {result['error']}"
    else:
        return str(result)



@app.route("/generate-diet", methods=["POST"])
def generate_diet():
    try:
        data = request.json

        weight = float(data["weight"])
        height = float(data["height"])
        age = int(data["age"])
        goal = data["goal"]
        food = data["food"]
        budget = int(data["budget"])

        # --- Calorie calculation ---
        calories = 10 * weight + 6.25 * height - 5 * age + 5

        if goal == "Fat Loss":
            calories -= 300
        elif goal == "Muscle Gain":
            calories += 300

        protein = round(weight * 1.8)

        # --- AI Prompt ---
        prompt = f"""
You are an expert Indian nutritionist.

Create a {data['meals']}-meal Indian diet plan.

Person Details:
Age: {age}
Gender: {data['gender']}
Height: {height} cm
Weight: {weight} kg
Goal: {goal}
Activity Level: {data['activity']}
Food Preference: {food}
Budget: ₹{budget} per day
Allergies: {data['allergy']}
Cuisine Preference: {data['indian']}

Nutrition Targets:
Calories: {calories} kcal
Protein: {protein} g

Requirements:
- Indian foods only
- Mention portion sizes
- Divide into {data['meals']} meals
- Add calories & protein per meal
- Avoid listed allergies
- Briefly explain why this suits the goal
"""

        ai_output = query_huggingface(prompt)

        return jsonify({
            "calories": round(calories),
            "protein": protein,
            "ai_plan": ai_output
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
