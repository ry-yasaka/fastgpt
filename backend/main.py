from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from pydantic import BaseModel

import uvicorn

class UserLogin(BaseModel):
    username: str
    password: str

# MySQLデータベースへの接続
DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/User"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

# CORSミドルウェアの設定（必要に応じて）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SQLAlchemyモデルの作成
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(255))

# テーブルの作成
Base.metadata.create_all(bind=engine)

# ログイン用のエンドポイント
@app.post("/login")
def login(user: UserLogin): #def login(username: str, password: str): では上手くいかない
    username = user.username
    password = user.password

    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()

    if not user or user.password != password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # 認証が成功した場合は、トークンやセッション情報を返すなどの適切な処理を行う
    return {"message": "Login successful"}

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)