from fastapi import FastAPI, Path
from typing import Annotated


app = FastAPI()
users = {'1': 'Имя: Example, возраст: 18'}


def unique_user(username, users_db):
    user_not_found = True
    for key, value in users_db.items():
        current_username = value[5:value.index(',')]
        if current_username == username:
            user_not_found = False
    return user_not_found


@app.get("/users")
async def get_users() -> dict:
    return users


@app.post("/user/{username}/{age}")
async def post_user(username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username",
                                                  example="UrbanUser")],
                    age: Annotated[int, Path(ge=18, le=120, description="Enter age", example="24")]) -> str:
    current_index = str(int(max(users, key=int))+1)
    if unique_user(username, users):
        users[current_index] = f"Имя: {username}, возраст {age}"
        message_output = f"User {current_index} is registered."
    else:
        message_output = f"The user with the name {username} already exists. Specify a different name"
    return message_output


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: Annotated[int, Path(ge=1, description="Enter User ID", example="1")],
                      username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username",
                                                    example="UrbanUser")],
                      age: Annotated[int, Path(ge=18, le=120, description="Enter age", example="24")]
                      ) -> str:
    list_user_id = list(users.keys())
    if str(user_id) in list_user_id:
        users[user_id] = f"Имя: {username}, возраст {age}"
        output_s = f"The user {user_id} is updated"
    else:
        output_s = f"The user {user_id} not found"
    return output_s


@app.delete("/user/{user_id}")
async def delete_user(user_id: Annotated[int, Path(ge=1, description="Enter User ID", example="2")]) -> str:
    list_user_id = list(users.keys())
    if str(user_id) in list_user_id:
        users.pop(str(user_id))
        output_s = f"User {user_id} has been deleted"
    else:
        output_s = f"The user {user_id} not found"
    return output_s

# uvicorn module_16_3:app --reload
