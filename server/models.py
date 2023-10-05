from beanie import Document, Indexed
from pydantic.fields import Field
from pydantic import BaseModel, EmailStr, validator
from enum import Enum
from typing import Optional, List
from datetime import datetime


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

class Statuses(str,Enum): 
    DELETED = 'DELETED'  

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
    MM = 'mm'  
    MA = 'ma'  
    OT = 'ot'  

class FoodInMealPlan(BaseModel):  
    portion: float
    measure_unit: MeasureUnit
    recipe_name: str
    kom: KindOfMeal
    dow: Optional[DayOfWeek] = None

def foods_dict_to_list(foods_dict: dict) -> List[FoodInMealPlan]:
    foods = []
    for food in foods_dict:
        food_model = FoodInMealPlan(
            portion=food['portion'],
            measure_unit=food['measure_unit'],
            recipe_name=food['recipe_name'],
            kom=KindOfMeal(food['kom']),
            dow=DayOfWeek(food['dow']) if food['dow'] is not None else None,
        )
        foods.append(food_model)
    return food

class MealPlan(Document):  
    name: Indexed(str, unique=True)
    foods: Optional[List[FoodInMealPlan]]
    obser: str
    created_at: datetime = Field(default_factory=datetime.utcnow, auto_now_add=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow, auto_now=True)


class USAStates(str,Enum): 
    AL = 'Alabama'  
    AK = 'Alaska'  
    AZ = 'Arizona'  
    AR = 'Arkansas'  
    CA = 'California'  
    CO = 'Colorado'  
    CT = 'Connecticut'  
    DE = 'Delaware'  
    FL = 'Florida'  
    GA = 'Georgia'  
    HI = 'Hawaii'  
    ID = 'Idaho'  
    IL = 'Illinois'  
    IN = 'Indiana'  
    IA = 'Iowa'  
    KS = 'Kansas'  
    KY = 'Kentucky'  
    LA = 'Louisiana'  
    ME = 'Maine'  
    MD = 'Maryland'  
    MA = 'Massachusetts'  
    MI = 'Michigan'  
    MN = 'Minnesota'  
    MS = 'Mississippi'  
    MO = 'Missouri'  
    MT = 'Montana'  
    NE = 'Nebraska'  
    NV = 'Nevada'  
    NH = 'New Hampshire'  
    NJ = 'New Jersey'  
    NM = 'New Mexico'  
    NY = 'New York'  
    NC = 'North Carolina'  
    ND = 'North Dakota'  
    OH = 'Ohio'  
    OK = 'Oklahoma'  
    OR = 'Oregon'  
    PA = 'Pennsylvania'  
    RI = 'Rhode Island'  
    SC = 'South Carolina'  
    SD = 'South Dakota'  
    TN = 'Tennessee'  
    TX = 'Texas'  
    UT = 'Utah'  
    VT = 'Vermont'  
    VA = 'Virginia'  
    WA = 'Washington'  
    WV = 'West Virginia'  
    WI = 'Wisconsin'  
    WY = 'Wyoming'  

class MeasuresUnit(str,Enum): 
    DECIMAL = 'DECIMAL'  
    IMPERIAL = 'IMPERIAL'  

class MeasureUnit(BaseModel):  
    measures: MeasuresUnit


class UserRole(str,Enum): 
    ADMIN = 'ADMIN'  
    GESTOR = 'GESTOR'  
    APPUSER = 'APPUSER'  

class User(Document):  
    name: str
    surname: str
    alias: Indexed(str, unique=True)
    password: str
    email: EmailStr
    role: UserRole
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow, auto_now_add=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow, auto_now=True)

    