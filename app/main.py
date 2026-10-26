import os
from contextlib import asynccontextmanager

import psycopg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from psycopg.rows import dict_row


def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST", "db"),
        port=int(os.getenv("DB_PORT", "5432")),
        dbname=os.getenv("DB_NAME", "taskdb"),
        user=os.getenv("DB_USER", "taskuser"),
        password=os.getenv("DB_PASSWORD", "devpassword"),
        row_factory=dict_row,
    )


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id BIGSERIAL PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                done BOOLEAN NOT NULL DEFAULT FALSE,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
        """)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="TaskBox API",
    description="TaskBox API - automatic reload works, wooooow!",
    version="1.0.0",
    lifespan=lifespan,
)


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)


@app.get("/")
def home():
    return {
        "app": "TaskBox API",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def list_tasks():
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT id, title, done, created_at
            FROM tasks
            ORDER BY id DESC
        """).fetchall()

    return rows


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    with get_connection() as conn:
        row = conn.execute(
            """
            INSERT INTO tasks (title)
            VALUES (%s)
            RETURNING id, title, done, created_at
            """,
            (task.title,),
        ).fetchone()

    return row


@app.patch("/tasks/{task_id}/done")
def complete_task(task_id: int):
    with get_connection() as conn:
        row = conn.execute(
            """
            UPDATE tasks
            SET done = TRUE
            WHERE id = %s
            RETURNING id, title, done, created_at
            """,
            (task_id,),
        ).fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return row

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    with get_connection() as conn:
        row = conn.execute(
            """
            DELETE FROM tasks
            WHERE id = %s
            RETURNING id, title, done, created_at
            """,
            (task_id,),
        ).fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return {"deleted": row}