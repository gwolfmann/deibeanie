from typing import List,Any,Dict

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Depends

from .models import Ingredient, Recipe, StatusModel, Statuses

ingredients_router = APIRouter()
recipes_router = APIRouter()

async def get_ingredient(ingredient_id: PydanticObjectId) -> Ingredient:
    ingredient = await Ingredient.get(ingredient_id)
    if ingredient is None:
        raise HTTPException(status_code=404, detail="ingredient not found")
    return ingredient

# CRUD

@ingredients_router.post("/ingredients/", response_model=Ingredient)
async def create_ingredient(ingredient: Ingredient):
    await ingredient.create()
    return ingredient


@ingredients_router.get("/ingredients/{ingredient_id}", response_model=Ingredient)
async def get_ingredient_by_id(ingredient: Ingredient = Depends(get_ingredient)):
    return ingredient


@ingredients_router.put("/ingredients/{ingredient_id}", response_model=Ingredient)
async def update_ingredient(ingredient_data: Ingredient, ingredient: Ingredient = Depends(get_ingredient)):
    fields_to_update = ingredient_data.dict()
    # Remove the _id field from the ingredient_data_copy dictionary
    fields_to_update.pop("_id",None)
    ingredient_updated = await ingredient.update({"$set": fields_to_update})
    return ingredient_updated


@ingredients_router.delete("/ingredients/{ingredient_id}", response_model=StatusModel)
async def delete_ingredient(ingredient: Ingredient = Depends(get_ingredient)):
    await ingredient.delete()
    return StatusModel(status=Statuses.DELETED)

# LISTS

@ingredients_router.get("/ingredients/", response_model=List[Ingredient])
async def get_all_ingredients():
    return await Ingredient.find_all().to_list()


@ingredients_router.get("/ingredients/by_uuid/{uuid}", response_model=List[Ingredient])
async def filter_notes_by_uuid(uuid: str):
    return await Ingredient.find_many({"uuid": uuid}).to_list()

# Get a recipe by ID
async def get_recipe(recipe_id: PydanticObjectId) -> Recipe:
    recipe = await Recipe.get(recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="recipe not found")
    return recipe


# Create a new recipe
@recipes_router.post("/recipes/", response_model=Recipe)
async def create_recipe(recipe: Recipe):
    await recipe.create()
    return recipe


# Update a recipe
@recipes_router.put("/recipes/{recipe_id}", response_model=Recipe)
async def update_recipe(recipe_data: Recipe, recipe: Recipe = Depends(get_recipe)):
#async def update_ingredient(ingredient_data: Ingredient, ingredient: Ingredient = Depends(get_ingredient)):
    fields_to_update = recipe_data.dict()
    # Remove the _id field from the ingredient_data_copy dictionary
    fields_to_update.pop("_id",None)
    await recipe.update({"$set": {"ingredients": []}})
    recipe_updated = await recipe.update({"$set": fields_to_update})
    return recipe_updated

@recipes_router.put("/recipes/{recipe_id}/update", response_model=Recipe)
async def update_recipe(recipe_id: PydanticObjectId, recipe_data: Dict[str, Any]):
    recipe = await Recipe.get(recipe_id)
    await recipe.update({"$set": recipe_data})
    return recipe


# Delete a recipe
@recipes_router.delete("/recipes/{recipe_id}", response_model=StatusModel)
async def delete_recipe(recipe: Recipe = Depends(get_recipe)):
    await recipe.delete()
    return StatusModel(status=Statuses.DELETED)

@recipes_router.get("/recipes/{recipe_id}", response_model=Recipe)
async def get_recipe_by_id(recipe: Recipe = Depends(get_recipe)):
    return recipe

# Get all recipes
@recipes_router.get("/recipes/", response_model=List[Recipe])
async def get_all_recipes():
    return await Recipe.find_all().to_list()
