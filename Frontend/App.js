const API_URL = "http://127.0.0.1:5000/recipes";

// Elements
const randomBtn = document.getElementById("randomBtn");
const randomRecipeDiv = document.getElementById("randomRecipe");
const recipeList = document.getElementById("recipeList");
const addForm = document.getElementById("addForm");
const nameInput = document.getElementById("name");
const ingredientsInput = document.getElementById("ingredients");
const instructionsInput = document.getElementById("instructions");

// Load all recipes
async function loadRecipes() {
    const res = await fetch(API_URL);
    const recipes = await res.json();
    recipeList.innerHTML = "";
    recipes.forEach(r => {
        const li = document.createElement("li");
        li.textContent = `${r.name} - Ingredients: ${r.ingredients.join(", ")}`;
        recipeList.appendChild(li);
    });
}

// Get a random recipe
async function getRandomRecipe() {
    const res = await fetch(`${API_URL}/random`);
    const recipe = await res.json();
    randomRecipeDiv.innerHTML = `<h3>${recipe.name}</h3>
                                 <p><strong>Ingredients:</strong> ${recipe.ingredients.join(", ")}</p>
                                 <p><strong>Instructions:</strong> ${recipe.instructions}</p>`;
}

// Add a new recipe
async function addRecipe(event) {
    event.preventDefault();
    const name = nameInput.value;
    const ingredients = ingredientsInput.value.split(",").map(s => s.trim());
    const instructions = instructionsInput.value;

    const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, ingredients, instructions })
    });

    if (res.ok) {
        alert("Recipe added!");
        addForm.reset();
        loadRecipes();
    } else {
        alert("Error adding recipe");
    }
}

// Event listeners
randomBtn.addEventListener("click", getRandomRecipe);
addForm.addEventListener("submit", addRecipe);

// Initial load
loadRecipes();