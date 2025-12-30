from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime

# 共通のベースモデル
class ProblemBase(BaseModel):
    content_text: str
    content_latex: str
    solution_text: Optional[str] = None
    solution_latex: Optional[str] = None
    subject: str = "math"
    difficulty: int = 1
    parent_id: Optional[UUID] = None

# 作成時のリクエストモデル
class ProblemCreate(ProblemBase):
    pass

# DBから返ってくるレスポンスモデル
class ProblemResponse(ProblemBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True