from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from Render + FastAPI!"}

# OpenAPIスキーマに servers を手動追加
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FastAPI",
        version="1.0.0",
        description="Custom GPT連携用API",
        routes=app.routes,
    )
    openapi_schema["servers"] = [
        {"url": "https://gpt-api-9qur.onrender.com"}
    ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


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
