from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class ProblemBase(BaseModel):
    content_text: str
    content_latex: str
    solution_text: Optional[str] = None
    solution_latex: Optional[str] = None
    subject: str = "math"
    difficulty: int = 1
    parent_id: Optional[UUID] = None

class ProblemCreate(ProblemBase):
    pass

class ProblemResponse(ProblemBase):
    id: UUID
    # ↓↓ ここを変更しました（Optional と = None を追加） ↓↓
    user_id: Optional[UUID] = None 
    created_at: datetime

    class Config:
        from_attributes = True