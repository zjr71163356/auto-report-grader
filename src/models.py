"""
数据模型定义
"""
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class StudentSubmission:
    """学生提交信息"""
    student_id: str
    student_name: str
    folder_name: str
    folder_path: str


@dataclass
class ScoreResult:
    """评分结果"""
    student_id: str
    student_name: str
    folder_name: str
    score: float
    comment: str


@dataclass
class ProcessingResult:
    """处理结果"""
    submission: StudentSubmission
    content: str
    score_result: Optional[ScoreResult] = None
    errors: List[str] = field(default_factory=list)
