from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # This allows your frontend to communicate with the backend

# Initialize OpenAI client
api_key = os.getenv("General") if os.getenv("General") else os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Store favorites in memory (in a real app, you'd use a database)
favorites = []

@app.route('/generate-recipe', methods=['POST'])
def generate_recipe():
    data = request.json
    ingredients = data.get('ingredients', '')
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": """You are an expert cook, generating recipes for users based on their ingredients.
                Generate a detailed recipe in JSON format with the following structure:
                {
                    "recipe": {
                        "name": "Recipe Name",
                        "prep_time": "XX minutes",
                        "servings": "X servings",
                        "ingredients": [
                            {"name": "ingredient", "quantity": "amount", "preparation": "prep method"}
                        ],
                        "steps": [
                            {"description": "step description"}
                        ],
                        "nutrition": {
                            "calories": "XXX",
                            "protein": "XX",
                            "carbs": "XX",
                            "fat": "XX"
                        }
                    }
                }"""},
                {"role": "user", "content": f"I have the following ingredients:\n{ingredients}"}
            ]
        )
        
        # Parse the response to ensure it's valid JSON
        content = response.choices[0].message.content
        try:
            # Try to parse the entire content as JSON
            recipe_data = json.loads(content)
        except json.JSONDecodeError:
            # If that fails, try to extract JSON from markdown code blocks
            import re
            json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
            if json_match:
                recipe_data = json.loads(json_match.group(1).strip())
            else:
                raise ValueError("Could not parse recipe data")
        
        return jsonify(recipe_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/favorites', methods=['GET'])
def get_favorites():
    return jsonify(favorites)

@app.route('/favorites', methods=['POST'])
def add_favorite():
    recipe = request.json
    recipe['saved_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Check if recipe already exists
    if not any(f['recipe']['name'] == recipe['recipe']['name'] for f in favorites):
        favorites.append(recipe)
        return jsonify({"message": "Recipe saved to favorites!", "success": True})
    return jsonify({"message": "Recipe already in favorites!", "success": False})

if __name__ == '__main__':
    app.run(debug=True) 