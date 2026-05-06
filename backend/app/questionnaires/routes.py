from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.deps import get_current_user_id
from app.questionnaires.schemas import AnswerIn, Question
from app.schemas.common import MessageResponse
from app.storage.repository import get_repository

router = APIRouter()

QUESTIONS = [
    Question(id=1, text="Por que tu interes en este curso?"),
    Question(id=2, text="Cual es tu expectativa en este curso?"),
    Question(
        id=3,
        text="Crees necesario que el CUGDL tenga materia de verano en programacion y base de datos?",
    ),
    Question(
        id=4,
        text="Cuales son tus recomendaciones acerca de lo que sucede con las materias y temas en el CUGDL?",
    ),
]


@router.get("/questions", response_model=list[Question])
def get_questions() -> list[Question]:
    return QUESTIONS


@router.post("/responses", response_model=MessageResponse)
def submit_responses(answers: list[AnswerIn], user_id: str = Depends(get_current_user_id)) -> MessageResponse:
    repo = get_repository()
    if len(answers) != len(QUESTIONS):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debes responder las 4 preguntas",
        )

    expected = {q.id for q in QUESTIONS}
    received = {a.question_id for a in answers}
    if expected != received:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="IDs de preguntas invalidos o repetidos",
        )

    payload = [
        {"question_id": a.question_id, "answer": a.answer.strip()}
        for a in sorted(answers, key=lambda x: x.question_id)
    ]
    repo.save_questionnaire(user_id=user_id, answers=payload)
    return MessageResponse(message="Respuestas guardadas correctamente")


@router.get("/my-responses")
def get_my_responses(user_id: str = Depends(get_current_user_id)) -> dict:
    repo = get_repository()
    return {"answers": repo.get_questionnaire(user_id)}

