from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from .models import Ingredient, Recipe, MealPlan, User, UserProfile
from .routes import ingredients_router, recipes_router, mealplans_router, users_router, userprofiles_router
from fastapi import Depends
from .models import UserCreate, UserRead, UserUpdate
from .users import auth_backend, current_active_user, fastapi_users

app = FastAPI()

class Settings:
    #mongodb_url = "mongodb://localhost:27017/dei0"
    mongodb_url = "mongodb+srv://gwolfmann:mBmtB6Hyx0MN4mQd@turnero.nmyvwbj.mongodb.net/?retryWrites=true&w=majority"


@app.on_event("startup")
async def start_beanie():
    # CREATE MOTOR CLIENT
    client = AsyncIOMotorClient( Settings.mongodb_url, uuidRepresentation="standard" )
    await init_beanie(client.dei0, document_models=[Ingredient, Recipe, MealPlan, User, UserProfile])
 
    app.include_router(ingredients_router, prefix="/meals", tags=["ingredient"],dependencies=[Depends(current_active_user)])  
    app.include_router(recipes_router, prefix="/meals", tags=["recipe"],dependencies=[Depends(current_active_user)])  
    app.include_router(mealplans_router, prefix="/meals", tags=["meal_plan"],dependencies=[Depends(current_active_user)])  
    app.include_router(users_router, prefix="/meals", tags=["user"],dependencies=[Depends(current_active_user)])  
    app.include_router(userprofiles_router, prefix="/meals", tags=["user_profile"],dependencies=[Depends(current_active_user)]) 

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}

@app.get("/", tags=["Root"])
async def index() -> dict:
    return {"message": "Welcome to dei0 server crud!"}