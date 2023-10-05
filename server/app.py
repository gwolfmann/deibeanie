from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from .models import Ingredient, Recipe, MealPlan, User
from .routes import ingredients_router, recipes_router, mealplans_router, users_router

app = FastAPI()

@app.on_event("startup")
async def start_beanie():
    # CREATE MOTOR CLIENT
    client = AsyncIOMotorClient( "mongodb://localhost:27017/dei0" )
    await init_beanie(client.dei0, document_models=[Ingredient, Recipe, MealPlan, User])
 
    app.include_router(ingredients_router, prefix="/meals", tags=["ingredient"])  
    app.include_router(recipes_router, prefix="/meals", tags=["recipe"])  
    app.include_router(mealplans_router, prefix="/meals", tags=["meal_plan"])  
    app.include_router(users_router, prefix="/meals", tags=["user"]) 

@app.get("/", tags=["Root"])
async def index() -> dict:
    return {"message": "Welcome to dei0 server crud!"}