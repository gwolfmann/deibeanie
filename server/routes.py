from typing import List,Any,Dict

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Depends
from .models import Ingredient, Recipe, MealPlan, FoodInMealPlan, StatusModel, Statuses
from .models import get_recipe_by_name, foods_dict_to_list


ingredients_router= APIRouter()
recipes_router= APIRouter()
mealplans_router= APIRouter()


#######################################
######  INGREDIENT   ########
#######################################
async def get_ingredient(ingredient_id: PydanticObjectId) -> Ingredient:
    ingredient = await Ingredient.get(ingredient_id)
    if ingredient is None:
        raise HTTPException(status_code=404, detail="ingredient not found")
    return ingredient


    
#######  GET  ##########
@ingredients_router.get("/ingredients/{ingredient_id}", response_model=Ingredient)
async def get_ingredient_by_id(ingredient: Ingredient = Depends(get_ingredient)):
    return ingredient

@ingredients_router.get("/ingredients/", response_model=List[Ingredient])
async def get_all_ingredients():
    return await Ingredient.find_all().to_list()
    
#######  POST  ##########
@ingredients_router.post("/ingredients/", response_model=Ingredient)
async def create_ingredient(ingredient: Ingredient):   
    await ingredient.create()
    return ingredient

#######  PUT  ##########
# Complete replace
@ingredients_router.put("/ingredients/{ingredient_id}", response_model=Ingredient)
async def update_ingredient(ingredient_data: Ingredient, ingredient: Ingredient = Depends(get_ingredient)):
    fields_to_update = ingredient_data.dict()
    fields_to_update.pop("_id",None) 
    ingredient_updated = await ingredient.update({"$set": fields_to_update})
    return ingredient_updated

# Partial replace
@ingredients_router.put("/ingredients/{ingredient_id}/update", response_model=Ingredient)
async def update_ingredient(ingredient_id: PydanticObjectId, ingredient_data: Dict[str, Any]):
    ingredient = await Ingredient.get(ingredient_id)   
    await ingredient.update({"$set": ingredient_data})
    return ingredient


#######  DELETE  ##########
@ingredients_router.delete("/ingredients/{ingredient_id}", response_model=StatusModel)
async def delete_ingredient(ingredient: Ingredient = Depends(get_ingredient)):
    await ingredient.delete()
    return StatusModel(status=Statuses.DELETED)

#######################################
######  RECIPE   ########
#######################################
async def get_recipe(recipe_id: PydanticObjectId) -> Recipe:
    recipe = await Recipe.get(recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="recipe not found")
    return recipe

async def check_recipe_exists(recipe_name: str) -> bool:
    recipe = await get_recipe_by_name(recipe_name)
    return not(recipe is None)

    
#######  GET  ##########
@recipes_router.get("/recipes/{recipe_id}", response_model=Recipe)
async def get_recipe_by_id(recipe: Recipe = Depends(get_recipe)):
    return recipe

@recipes_router.get("/recipes/", response_model=List[Recipe])
async def get_all_recipes():
    return await Recipe.find_all().to_list()
    
#######  POST  ##########
@recipes_router.post("/recipes/", response_model=Recipe)
async def create_recipe(recipe: Recipe):   
    await recipe.create()
    return recipe

#######  PUT  ##########
# Complete replace
@recipes_router.put("/recipes/{recipe_id}", response_model=Recipe)
async def update_recipe(recipe_data: Recipe, recipe: Recipe = Depends(get_recipe)):
    fields_to_update = recipe_data.dict()
    fields_to_update.pop("_id",None) 
    await recipe.update({"$set": {"ingredients": []}})
    recipe_updated = await recipe.update({"$set": fields_to_update})
    return recipe_updated

# Partial replace
@recipes_router.put("/recipes/{recipe_id}/update", response_model=Recipe)
async def update_recipe(recipe_id: PydanticObjectId, recipe_data: Dict[str, Any]):
    recipe = await Recipe.get(recipe_id)   
    await recipe.update({"$set": recipe_data})
    return recipe


#######  DELETE  ##########
@recipes_router.delete("/recipes/{recipe_id}", response_model=StatusModel)
async def delete_recipe(recipe: Recipe = Depends(get_recipe)):
    await recipe.delete()
    return StatusModel(status=Statuses.DELETED)

#######################################
######  MEALPLAN   ########
#######################################
async def get_mealplan(mealplan_id: PydanticObjectId) -> MealPlan:
    mealplan = await MealPlan.get(mealplan_id)
    if mealplan is None:
        raise HTTPException(status_code=404, detail="mealplan not found")
    return mealplan

   
async def check_recipes_ok(foods:List[FoodInMealPlan]) -> bool:
    result = True
    for foods_value in foods:
        result = result and await check_recipe_exists(foods_value.recipe_name)
    return result
    
#######  GET  ##########
@mealplans_router.get("/mealplans/{mealplan_id}", response_model=MealPlan)
async def get_mealplan_by_id(mealplan: MealPlan = Depends(get_mealplan)):
    return mealplan

@mealplans_router.get("/mealplans/", response_model=List[MealPlan])
async def get_all_mealplans():
    return await MealPlan.find_all().to_list()
    
#######  POST  ##########
@mealplans_router.post("/mealplans/", response_model=MealPlan)
async def create_mealplan(mealplan: MealPlan):      
    recipe_name_ok = await check_recipes_ok(mealplan.foods)
    if not recipe_name_ok:
        raise HTTPException(status_code=404, detail="mealplan contains a recipe undefined")
    await mealplan.create()
    return mealplan

#######  PUT  ##########
# Complete replace
@mealplans_router.put("/mealplans/{mealplan_id}", response_model=MealPlan)
async def update_mealplan(mealplan_data: MealPlan, mealplan: MealPlan = Depends(get_mealplan)):
    fields_to_update = mealplan_data.dict()
    fields_to_update.pop("_id",None) 
    await mealplan.update({"$set": {"foods": []}})
    mealplan_updated = await mealplan.update({"$set": fields_to_update})
    return mealplan_updated

# Partial replace
@mealplans_router.put("/mealplans/{mealplan_id}/update", response_model=MealPlan)
async def update_mealplan(mealplan_id: PydanticObjectId, mealplan_data: Dict[str, Any]):
    mealplan = await MealPlan.get(mealplan_id)      
    if mealplan_data.get('foods') != None:
        recipe_name_ok = await check_recipes_ok(foods_dict_to_list(mealplan_data.get('foods')))
        if not recipe_name_ok:
            raise HTTPException(status_code=404, detail="mealplan contains a recipe undefined")
    await mealplan.update({"$set": mealplan_data})
    return mealplan

#Put for add a meal to a plan
@mealplans_router.put("/mealplans/{mealplan_id}/addmeal", response_model=MealPlan)
async def add_mealplan(mealplan_id: PydanticObjectId, mealplan_data: Dict[str, Any]):
    mealplan = await MealPlan.get(mealplan_id)
    if mealplan_data.get('foods') != None:
        recipe_name_ok = await check_recipes_ok(foods_dict_to_list(mealplan_data.get('foods')))
        if not recipe_name_ok:
            raise HTTPException(status_code=404, detail="meal plan contains a recipe undefined")
    await mealplan.update({"$push": {"foods": {"$each": foods_dict_to_list(mealplan_data.get("foods"))}}})
    return mealplan
#######  DELETE  ##########
@mealplans_router.delete("/mealplans/{mealplan_id}", response_model=StatusModel)
async def delete_mealplan(mealplan: MealPlan = Depends(get_mealplan)):
    await mealplan.delete()
    return StatusModel(status=Statuses.DELETED)
