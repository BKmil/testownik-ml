from pydantic import BaseModel
from typing import List


class Answer(BaseModel):
    id: str
    order: int
    text: str
    is_correct: bool


class Question(BaseModel):
    id: str
    order: int
    text: str
    explanation: str
    multiple: bool
    answers: List[Answer]


class Quiz(BaseModel):
    title: str
    description: str
    version: int
    questions: List[Question]
