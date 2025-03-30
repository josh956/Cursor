from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
import json
import re
from datetime import datetime

app = Flask(__name__)
CORS(app)  # This allows your frontend to communicate with the backend

# Initialize OpenAI client
api_key = os.getenv("General") if os.getenv("General") else os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def load_favorites():
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []

def save_recipe(recipe):
    if recipe not in st.session_state.favorites:
        recipe['saved_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.favorites.append(recipe)
        st.success("Recipe saved to favorites!")
    else:
        st.warning("This recipe is already in your favorites!")

def display_recipe(recipe_data):
    recipe = recipe_data['recipe']
    
    # Display recipe header
    st.header(recipe['name'])
    
    # Display preparation time and serving size
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"⏱️ Prep Time: {recipe.get('prep_time', 'N/A')}")
    with col2:
        st.info(f"👥 Servings: {recipe.get('servings', 'N/A')}")
    
    # Display ingredients
    st.subheader("📝 Ingredients")
    for ingredient in recipe.get('ingredients', []):
        st.write(f"• {ingredient['quantity']} {ingredient['name']} ({ingredient['preparation']})")
    
    # Display instructions
    st.subheader("👩‍🍳 Instructions")
    for i, step in enumerate(recipe.get('steps', []), 1):
        st.write(f"{i}. {step['description']}")
    
    # Display nutritional information
    if 'nutrition' in recipe:
        st.subheader("🥗 Nutritional Information (per serving)")
        nutrition = recipe['nutrition']
        cols = st.columns(4)
        with cols[0]:
            st.metric("Calories", f"{nutrition.get('calories', 'N/A')} kcal")
        with cols[1]:
            st.metric("Protein", f"{nutrition.get('protein', 'N/A')} g")
        with cols[2]:
            st.metric("Carbs", f"{nutrition.get('carbs', 'N/A')} g")
        with cols[3]:
            st.metric("Fat", f"{nutrition.get('fat', 'N/A')} g")
    
    # Save to favorites button
    if st.button("❤️ Save to Favorites"):
        save_recipe(recipe_data)

def display_favorites():
    if st.session_state.favorites:
        st.subheader("❤️ Saved Recipes")
        for recipe in st.session_state.favorites:
            with st.expander(f"{recipe['recipe']['name']} - Saved on {recipe['saved_date']}"):
                display_recipe(recipe)
    else:
        st.info("No saved recipes yet. Generate and save some recipes!")

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
        return jsonify(response.choices[0].message.content)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)