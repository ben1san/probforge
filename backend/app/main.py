from fastapi import FastAPI, HTTPException
from typing import List
from .database import supabase
from .models.schemas import ProblemCreate, ProblemResponse

app = FastAPI(title="ProbForge API")

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