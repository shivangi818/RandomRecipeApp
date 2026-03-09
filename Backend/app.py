from flask import Flask, jsonify, request
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)
# ----------------------------
# In-memory "database"
# ----------------------------
recipes = [
    {
        "id": 1,
        "name": "Pasta Carbonara",
        "ingredients": ["pasta", "eggs", "cheese", "bacon"],
        "instructions": "Boil pasta. Cook bacon. Mix eggs & cheese. Combine all."
    },
    {
        "id": 2,
        "name": "Grilled Cheese Sandwich",
        "ingredients": ["bread", "cheese", "butter"],
        "instructions": "Butter bread. Put cheese inside. Grill until golden."
    }
]

# ----------------------------
# GET all recipes
# ----------------------------
@app.route("/recipes", methods=["GET"])
def get_recipes():
    return jsonify(recipes), 200

# ----------------------------
# GET a random recipe
# ----------------------------
@app.route("/recipes/random", methods=["GET"])
def get_random_recipe():
    return jsonify(random.choice(recipes)), 200

# ----------------------------
# POST a new recipe
# ----------------------------
@app.route("/recipes", methods=["POST"])
def add_recipe():
    data = request.get_json()
    new_id = max([r["id"] for r in recipes]) + 1 if recipes else 1
    new_recipe = {
        "id": new_id,
        "name": data.get("name"),
        "ingredients": data.get("ingredients", []),
        "instructions": data.get("instructions", "")
    }
    recipes.append(new_recipe)
    return jsonify(new_recipe), 201

# ----------------------------
# PUT update a recipe by id
# ----------------------------
@app.route("/recipes/<int:recipe_id>", methods=["PUT"])
def update_recipe(recipe_id):
    data = request.get_json()
    for r in recipes:
        if r["id"] == recipe_id:
            r["name"] = data.get("name", r["name"])
            r["ingredients"] = data.get("ingredients", r["ingredients"])
            r["instructions"] = data.get("instructions", r["instructions"])
            return jsonify(r), 200
    return jsonify({"error": "Recipe not found"}), 404

# ----------------------------
# DELETE a recipe by id
# ----------------------------
@app.route("/recipes/<int:recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id):
    global recipes
    recipes = [r for r in recipes if r["id"] != recipe_id]
    return jsonify({"message": "Deleted"}), 200

# ----------------------------
# Run the server
# ----------------------------
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)