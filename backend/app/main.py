from fastapi import FastAPI, HTTPException
from typing import List
from .database import supabase
from .models.schemas import ProblemCreate, ProblemResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ProbForge API")

# ↓↓ 追加 2: CORS設定 ↓↓
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to ProbForge API (Supabase Client Version)"}

# --- 問題 (Problems) のCRUD ---

@app.post("/problems/", response_model=ProblemResponse)
def create_problem(problem: ProblemCreate):
    # データを挿入 (insert)
    # data, count = supabase.table('problems').insert({...}).execute() の形式
    try:
        response = supabase.table("problems").insert(problem.dict()).execute()
        
        # 成功すると response.data にリストで結果が入る
        if not response.data:
            raise HTTPException(status_code=400, detail="Failed to create problem")
            
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/problems/", response_model=List[ProblemResponse])
def get_problems():
    # 全件取得 (select)
    try:
        response = supabase.table("problems").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/problems/{problem_id}", response_model=ProblemResponse)
def get_problem(problem_id: str):
    # ID指定で取得 (eq)
    try:
        response = supabase.table("problems").select("*").eq("id", problem_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Problem not found")
            
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/problems/{problem_id}/generate", response_model=ProblemResponse)
def generate_similar_problem(problem_id: str):
    # 1. 元の問題をSupabaseから取得
    original_res = supabase.table("problems").select("*").eq("id", problem_id).execute()
    if not original_res.data:
        raise HTTPException(status_code=404, detail="Original problem not found")
    
    original = original_res.data[0]

    # 2. AIに類題を作らせる
    try:
        generated_data = generate_variant(
            original["content_text"], 
            original["content_latex"], 
            original["subject"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}")

    # 3. 生成された類題をDBに保存 (parent_id を設定)
    new_problem = {
        **generated_data,
        "subject": original["subject"],
        "difficulty": original["difficulty"], # いったん同じ難易度
        "parent_id": problem_id, # ここが重要！親問題と紐付ける
        "user_id": original["user_id"] # 同じユーザーのものとする
    }

    insert_res = supabase.table("problems").insert(new_problem).execute()
    
    return insert_res.data[0]