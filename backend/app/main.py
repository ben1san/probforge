from fastapi import FastAPI
from .database import engine, Base
from .models import Problem, Exam, ExamProblem

# テーブルの自動作成（本番環境ではAlembic等のマイグレーションツール推奨ですが、開発初期はこれでOK）
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ProbForge API")

@app.get("/")
def read_root():
    return {"message": "Welcome to ProbForge API backed by Supabase"}