from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from .models import Ingredient, Recipe
from .routes import ingredients_router,recipes_router

app = FastAPI()

@app.on_event("startup")
async def start_beanie():
    # CREATE MOTOR CLIENT
    client = AsyncIOMotorClient( "mongodb://localhost:27017/dei0" )

    await init_beanie(client.dei0, document_models=[Ingredient, Recipe])
    app.include_router(ingredients_router, prefix="/meals", tags=["ingredient"])
    app.include_router(recipes_router, prefix="/meals", tags=["recipes"])

@app.get("/", tags=["Root"])
async def index() -> dict:
    return {"message": "Welcome to dei0 server crud!"}
