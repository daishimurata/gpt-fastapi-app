from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import csv
import os

app = FastAPI()

# データ保存用（簡易メモリDB）
users = []

# Pydanticモデル
class User(BaseModel):
    name: str
    birthdate: str
    sex: str
    address: str

@app.post("/register-user")
def register_user(user: User):
    users.append(user)
    return {"status": "registered", "user": user}

@app.get("/list-users", response_model=List[User])
def list_users():
    return users

@app.get("/export-users")
def export_users():
    filename = "users.csv"
    with open(filename, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Birthdate", "Sex", "Address"])
        for u in users:
            writer.writerow([u.name, u.birthdate, u.sex, u.address])
    return {"status": "exported", "file": filename}

@app.get("/")
def root():
    return {"message": "Hello from Render + FastAPI!"}
