from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from database import get_connection, init_db

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_methods=["*"],
    allow_headers=["*"],
)
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


@app.put("/applications/{app_id}")
def update_application(app_id: int, item: ApplicationIn):
    conn = get_connection()
    cursor = conn.execute(
        "UPDATE applications "
        "SET company = ?, role = ?, status = ?, applied_date = ?, notes = ? "
        "WHERE id = ?",
        (item.company, item.role, item.status, item.applied_date, item.notes, app_id),
    )
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    if updated == 0:
        raise HTTPException(status_code=404, detail="Application not found")
    return {"id": app_id, **item.model_dump()}


@app.delete("/applications/{app_id}")
def delete_application(app_id: int):
    conn = get_connection()
    cursor = conn.execute("DELETE FROM applications WHERE id = ?", (app_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Application not found")
    return {"message": "Deleted", "id": app_id}