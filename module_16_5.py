from fastapi import FastAPI, HTTPException, Path, Request
from typing import List, Annotated
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int


def unique_user(username, users_db):
    user_not_found = True
    for current_user in users_db:
        current_username = current_user.username
        if current_username == username:
            user_not_found = False
    return user_not_found


@app.get("/")
async def get_main_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/user/{user_id}")
async def get_user(request: Request, user_id: int) -> HTMLResponse:
    not_found = True
    find_id = 0
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user": users[find_id]})
        find_id += 1
    if not_found:
        raise HTTPException(status_code=404, detail="User was not found")


@app.get("/users")
async def get_users() -> List[User]:
    return users


@app.post("/user/{username}/{age}")
async def create_user(username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username",
                                                    example="UrbanUser")],
                      age: Annotated[int, Path(ge=18, le=120, description="Enter age", example="24")]) -> User:
    new_id = max((u.id for u in users), default=0)+1
    user = User(id=new_id, username=username, age=age)
    if unique_user(username, users):
        users.append(user)
        return user
    else:
        message_output = f"The user with the name {username} already exists. Specify a different name"
        raise HTTPException(status_code=409, detail=message_output)


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: Annotated[int, Path(ge=1, description="Enter User ID", example="1")],
                      username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username",
                                                    example="UrbanUser")],
                      age: Annotated[int, Path(ge=18, le=120, description="Enter age", example="24")]) -> User:
    not_found = True
    for edit_user in users:
        if edit_user.id == user_id:
            edit_user.username = username
            edit_user.age = age
            not_found = False
            return edit_user
    if not_found:
        raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}")
async def delete_user(user_id: Annotated[int, Path(ge=1, description="Enter User ID", example="1")]) -> User:
    not_found = True
    del_user_index = 0
    for del_user in users:
        if del_user.id == user_id:
            users.pop(del_user_index)
            not_found = False
            return del_user
        del_user_index += 1
    if not_found:
        raise HTTPException(status_code=404, detail="User was not found")

# uvicorn module_16_5:app --reload
