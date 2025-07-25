from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List
from pydantic import BaseModel
from datetime import date
app = FastAPI()

class Todo(BaseModel):
    id:int
    task:str
    due:date


templates = Jinja2Templates(directory="templates")

# Temporary storage for todos (in-memory)
todos: List[Todo] = []

@app.get("/delete/{id}")
def delete_todo(id: int):
    global todos
    todos = [t for t in todos if t.id != id]
    return RedirectResponse("/", status_code=303)

@app.get("/edit/{id}", response_class=HTMLResponse)
def edit_todo_page(request: Request, id: int):
    for t in todos:
        if t.id == id:
            return templates.TemplateResponse("edit.html", {"request": request, "todo": t})
    return RedirectResponse("/", status_code=303)

@app.post("/edit/{id}")
def edit_todo(id: int, task: str = Form(...), due: date = Form(...)):
    for t in todos:
        if t.id == id:
            t.task = task
            t.due = due
            break
    return RedirectResponse("/", status_code=303)

@app.get("/upcoming", response_class=HTMLResponse)
def get_upcoming_todos(request: Request):
    today = date.today()
    upcoming = [t for t in todos if t.due >= today]
    return templates.TemplateResponse("upcoming.html", {"request": request, "todos": upcoming})
