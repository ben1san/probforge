from fastapi import FastAPI, HTTPException
from typing import List
from .database import supabase
from .models.schemas import ProblemCreate, ProblemResponse
from fastapi.middleware.cors import CORSMiddleware
from .services.ai import generate_variant

app = FastAPI(title="ProbForge API")

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
    original_res = supabase.table("problems").select("*").eq("id", problem_id).execute()
    if not original_res.data:
        raise HTTPException(status_code=404, detail="Original problem not found")
    
    original = original_res.data[0]

    try:
        generated_data = generate_variant(
            original["content"],
            original["subject"]
        )
    except Exception as e:
        import traceback
        traceback.print_exc() 
        raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}")

    # 3. 保存
    new_problem = {
        "content": generated_data["content"],
        "solution": generated_data.get("solution"),
        "subject": original["subject"],
        "difficulty": original["difficulty"],
        "parent_id": problem_id,
        "user_id": original["user_id"]
    }

    insert_res = supabase.table("problems").insert(new_problem).execute()
    
    return insert_res.data[0]