import uuid
from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class Problem(Base):
    __tablename__ = "problems"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), index=True) # Supabaseのauth.usersのID
    
    # 自己参照 (親問題のID)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("problems.id"), nullable=True)
    
    content_text = Column(Text, nullable=False)   # 問題文
    content_latex = Column(Text, nullable=False)  # 数式部分
    solution_text = Column(Text, nullable=True)   # 解説文
    solution_latex = Column(Text, nullable=True)  # 解答数式
    
    subject = Column(String, nullable=False)      # math, physics
    difficulty = Column(Integer, default=1)       # 1-5
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # リレーション定義
    children = relationship("Problem", backref="parent", remote_side=[id])
    exam_links = relationship("ExamProblem", back_populates="problem")

class Exam(Base):
    __tablename__ = "exams"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), index=True)
    
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    is_published = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # リレーション
    problem_links = relationship("ExamProblem", back_populates="exam")

class ExamProblem(Base):
    __tablename__ = "exam_problems"

    exam_id = Column(UUID(as_uuid=True), ForeignKey("exams.id"), primary_key=True)
    problem_id = Column(UUID(as_uuid=True), ForeignKey("problems.id"), primary_key=True)
    
    order_index = Column(Integer, nullable=False) # 問題順序

    exam = relationship("Exam", back_populates="problem_links")
    problem = relationship("Problem", back_populates="exam_links")