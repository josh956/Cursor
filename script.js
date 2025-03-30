// Initialize favorites from localStorage
let favorites = JSON.parse(localStorage.getItem('favorites')) || [];

// Tab switching functionality
document.querySelectorAll('.tab-btn').forEach(button => {
    button.addEventListener('click', () => {
        // Remove active class from all tabs
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
        
        // Add active class to clicked tab
        button.classList.add('active');
        document.getElementById(button.dataset.tab).classList.add('active');
    });
});

// Generate recipe functionality
document.getElementById('generateBtn').addEventListener('click', async () => {
    const ingredients = document.getElementById('ingredients').value;
    if (!ingredients.trim()) {
        alert('Please enter some ingredients');
        return;
    }

    try {
        const recipe = await generateRecipe(ingredients);
        displayRecipe(recipe);
    } catch (error) {
        console.error('Error generating recipe:', error);
        alert('Error generating recipe. Please try again.');
    }
});

// Function to generate recipe (replace with your API call)
async function generateRecipe(ingredients) {
    // This is where you would normally make an API call to your backend
    // For now, we'll return a sample recipe
    return {
        recipe: {
            name: "Mediterranean Salad",
            prep_time: "15 minutes",
            servings: "4 servings",
            ingredients: ingredients.split(',').map(ingredient => ({
                name: ingredient.trim(),
                quantity: "1",
                preparation: "chopped"
            })),
            steps: [
                { description: "Chop all vegetables" },
                { description: "Mix ingredients in a bowl" },
                { description: "Season to taste" }
            ],
            nutrition: {
                calories: "150",
                protein: "3",
                carbs: "12",
                fat: "8"
            }
        }
    };
}

// Function to display recipe
function displayRecipe(recipeData) {
    const recipe = recipeData.recipe;
    const recipeHtml = `
        <div class="recipe-card">
            <div class="recipe-header">
                <h2>${recipe.name}</h2>
            </div>
            <div class="recipe-meta">
                <div class="meta-item">
                    <p>⏱️ Prep Time: ${recipe.prep_time}</p>
                </div>
                <div class="meta-item">
                    <p>👥 Servings: ${recipe.servings}</p>
                </div>
            </div>
            <div class="ingredients-list">
                <h3>📝 Ingredients</h3>
                <ul>
                    ${recipe.ingredients.map(ingredient => 
                        `<li>${ingredient.quantity} ${ingredient.name} (${ingredient.preparation})</li>`
                    ).join('')}
                </ul>
            </div>
            <div class="steps-list">
                <h3>👩‍🍳 Instructions</h3>
                <ol>
                    ${recipe.steps.map(step => 
                        `<li>${step.description}</li>`
                    ).join('')}
                </ol>
            </div>
            <div class="nutrition-info">
                <h3>🥗 Nutritional Information (per serving)</h3>
                <div class="nutrition-grid">
                    <div class="nutrition-item">
                        <h4>Calories</h4>
                        <p>${recipe.nutrition.calories} kcal</p>
                    </div>
                    <div class="nutrition-item">
                        <h4>Protein</h4>
                        <p>${recipe.nutrition.protein}g</p>
                    </div>
                    <div class="nutrition-item">
                        <h4>Carbs</h4>
                        <p>${recipe.nutrition.carbs}g</p>
                    </div>
                    <div class="nutrition-item">
                        <h4>Fat</h4>
                        <p>${recipe.nutrition.fat}g</p>
                    </div>
                </div>
            </div>
            <button class="primary-btn" onclick="saveRecipe(${JSON.stringify(recipeData)})">
                ❤️ Save to Favorites
            </button>
        </div>
    `;
    document.getElementById('recipe-display').innerHTML = recipeHtml;
}

// Function to save recipe to favorites
function saveRecipe(recipe) {
    if (!favorites.find(r => r.recipe.name === recipe.recipe.name)) {
        recipe.saved_date = new Date().toLocaleString();
        favorites.push(recipe);
        localStorage.setItem('favorites', JSON.stringify(favorites));
        updateFavoritesList();
        alert('Recipe saved to favorites!');
    } else {
        alert('This recipe is already in your favorites!');
    }
}

// Function to update favorites list
function updateFavoritesList() {
    const favoritesList = document.getElementById('favorites-list');
    if (favorites.length === 0) {
        favoritesList.innerHTML = '<p class="no-favorites">No saved recipes yet. Generate and save some recipes!</p>';
        return;
    }

    const favoritesHtml = favorites.map(recipe => `
        <div class="favorite-recipe" onclick="displayRecipe(${JSON.stringify(recipe)})">
            <h3>${recipe.recipe.name}</h3>
            <p>Saved on: ${recipe.saved_date}</p>
        </div>
    `).join('');

    favoritesList.innerHTML = favoritesHtml;
}

// Initialize favorites list
updateFavoritesList(); 