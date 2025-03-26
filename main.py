from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import csv

app = FastAPI(
    title="FastAPI",
    version="0.1.0",
    servers=[
        {"url": "https://gpt-api-9qur.onrender.com", "description": "Render deployment"}
    ]
)


# CORS（カスタムGPTからのアクセスを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# フェイスシートモデル
class FaceSheet(BaseModel):
    name: str
    birthdate: str
    notes: str

# 仮のデータベース（Renderでも動く）
db: List[FaceSheet] = []

@app.post("/register")
def register_face_sheet(sheet: FaceSheet):
    db.append(sheet)
    return {"message": "登録しました"}

@app.get("/list", response_model=List[FaceSheet])
def list_face_sheets():
    return db

@app.get("/export")
def export_csv():
    with open("export.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["name", "birthdate", "notes"])
        for item in db:
            writer.writerow([item.name, item.birthdate, item.notes])
    return {"message": "CSV出力しました"}
