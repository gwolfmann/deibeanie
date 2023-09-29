from beanie import Document, Indexed#, Link
from pydantic import BaseModel, validator
from enum import Enum
from typing import Optional, List

class IngredientType(str,Enum):
    GLUTEN = 'gluten'
    FAT = 'fat'
    SODIUM = 'sodium'
    SUGAR = 'sugar'
    OTHER = 'other'

class Ingredient(Document):
    name: Indexed(str)
    aliment_types: List[IngredientType]

class MeasureUnit(str,Enum):
    KG = 'kg'
    LT = 'lt'
    GR = 'gr'
    UNIT = 'unit'

class IngredientInRecipe(BaseModel):
    ingredient: Ingredient
    quantity: float
    measure_unit: MeasureUnit
    
class Recipe(Document):
    name: Indexed(str,unique=True)
    ingredients: List[IngredientInRecipe]
    preparation: str

async def get_recipe_by_name(name: str) -> Recipe:
    recipe = await Recipe.find_one(Recipe.name == name)
    if recipe is None:
        return None
    return recipe

class Statuses(str, Enum):
    DELETED = "DELETED"

class StatusModel(BaseModel):
    status: Statuses

class DayOfWeek(str,Enum):
    MO = 'mo'
    TU = 'tu'
    WE = 'we'
    TH = 'th'
    FR = 'fr'
    SA = 'sa'
    SU = 'su'

class KindOfMeal(str,Enum):
    BR = 'br'
    LU = 'lu'
    DI = 'di'
    MM = 'mm'  #midle morning
    MA = 'ma'  #midle afternoon
    OT = 'ot'  #other

class FoodInMealPlan(BaseModel):
    portion : float
    measure_unit : MeasureUnit
    recipe_name : str
    kom : KindOfMeal
    dow : Optional[DayOfWeek] = None

def foods_dict_to_list(foods_dict: dict) -> List[FoodInMealPlan]:
    foods = []
    for food in foods_dict:
        food_model = FoodInMealPlan(
            portion=food["portion"],
            measure_unit=food["measure_unit"],
            recipe_name=food["recipe_name"],
            kom=KindOfMeal(food["kom"]),
            dow=DayOfWeek(food["dow"]) if food["dow"] is not None else None,
        )
        foods.append(food_model)
    return foods

class MealPlan(Document):
    name: Indexed(str, unique=True)
    foods: Optional[List[FoodInMealPlan]]
    obser: str
