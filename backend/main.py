from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from database import get_connection, init_db

app = FastAPI()
init_db()


class ApplicationIn(BaseModel):
    company: str
    role: str
    status: str = "Applied"
    applied_date: Optional[str] = None
    notes: Optional[str] = None


@app.get("/")
def home():
    return {"message": "Job Tracker API is running"}


@app.post("/applications", status_code=201)
def create_application(item: ApplicationIn):
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO applications (company, role, status, applied_date, notes) "
        "VALUES (?, ?, ?, ?, ?)",
        (item.company, item.role, item.status, item.applied_date, item.notes),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {"id": new_id, **item.model_dump()}


@app.get("/applications")
def list_applications():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM applications ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]