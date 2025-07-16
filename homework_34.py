import asyncio
import time
import uvicorn
from pydantic import BaseModel, Field

from fastapi import FastAPI, HTTPException, Response, Path, Query
import httpx

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import status

app = FastAPI(debug=True)

class Task(BaseModel):
    id:int = Field(gt=0)
    task:str = Field(description="Завдання та можливо його опис")
task1 = Task(id=1, task='Do homework').model_dump()

tasks = []

tasks.append(task1)

@app.post('/add_task/')
async def add_task(new_task: Task):
    if any(task["id"] == new_task.id for task in tasks):
        raise HTTPException(status_code=400, detail="Завдання з таким ID вже існує.")
    tasks.append(new_task.dict())
    return {
        "Відгук:": "Завдання успішно додано до списку!.",
        "Оновлений список завдань: ": tasks
    }

@app.get("/tasks/")
async def get_tasks():
    return tasks


@app.put("/editing/{task_id}", status_code=status.HTTP_200_OK)
async def edit_task(
        task_id: int = Path(..., gt=0, description="ID існуючого завдання"),
        new_task: str = Query(..., description="Нове формулювання завдання")
):
    for task in tasks:
        if task["id"] == task_id:
            task["task"] = new_task
            return {"message": f"Завдання з ID {task_id} оновлено", "updated_task": task}
    raise HTTPException(status_code=404, detail=f"Завдання з ID {task_id} не знайдено")

@app.delete("/delete/{task_id}", status_code=status.HTTP_200_OK)
async def delete_task(task_id: int = Path(..., gt=0, description="ID завдання для видалення")):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            deleted = tasks.pop(i)
            return {"message": f"Завдання з ID {task_id} видалено.", "deleted_task": deleted}
    raise HTTPException(status_code=404, detail=f"Завдання з ID {task_id} не знайдено.")

@app.get("/task/{task_id}", status_code=status.HTTP_200_OK)
async def get_task(task_id: int = Path(..., gt=0, description="ID завдання для перегляду")):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task:
        return task
    raise HTTPException(status_code=404, detail=f"Завдання з ID {task_id} не знайдено.")

if __name__ == "__main__":
    uvicorn.run("__main__:app", reload=True)