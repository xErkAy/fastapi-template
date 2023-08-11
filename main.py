from fastapi import FastAPI, Body
from tortoise import Tortoise
from models import User

app = FastAPI()


@app.get("/user/")
async def get_users():
    message = {}
    async for user in User.all():
        message[user.id] = {
            'username': user.username
        }
    return message


@app.get("/user/{user_id}")
async def get_users(user_id: int):
    user = await User.get(pk=user_id)
    return {
        user_id: {
            'username': user.username
        }
    }


@app.post("/user/")
async def create_user(payload: dict = Body(...)):
    return await User.create(username=payload.get('username'))


@app.on_event("startup")
async def start_up():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={
            'models': ['models']
        }
    )
    await Tortoise.generate_schemas(safe=True)


@app.on_event("shutdown")
async def shut_down():
    return await Tortoise.close_connections()
