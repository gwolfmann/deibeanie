from beanie import Document, Indexed
from pydantic import BaseModel
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
    name: Indexed(str)
    ingredients: List[IngredientInRecipe]
    preparation: str

class Statuses(str, Enum):
    DELETED = "DELETED"

class StatusModel(BaseModel):
    status: Statuses