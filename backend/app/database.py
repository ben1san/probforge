from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# .envから接続URLを取得
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Supabase(PostgreSQL)への接続エンジンを作成
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# DBセッションの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ベースモデル
Base = declarative_base()

# 依存性注入用（API作成時に使います）
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()