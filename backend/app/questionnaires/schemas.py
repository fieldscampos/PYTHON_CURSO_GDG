from pydantic import BaseModel, Field


class Question(BaseModel):
    id: int
    text: str
    type: str = "texto_libre"


class AnswerIn(BaseModel):
    question_id: int = Field(ge=1, le=4)
    answer: str = Field(min_length=1, max_length=3000)

