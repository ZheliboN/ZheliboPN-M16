from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def get_main_page() -> str:
    return "Главная страница"


@app.get("/user/admin")
async def get_admin_page() -> str:
    return "Вы вошли как администратор"


@app.get("/user/{user_id}")
async def get_user_number(user_id: int) -> str:
    output_s = f"Вы вошли как пользователь №{user_id}"
    return output_s


@app.get("/user")
async def get_user_info(username: str = "pavel", age: int = 45) -> str:
    output_s = f"Информация о пользователе. Имя: {username}, Возраст: {age}"
    return output_s

# uvicorn module_16_1:app --reload
