from http.client import responses

from fastapi import APIRouter, HTTPException, Depends
from pydantic import ValidationError
from app.liama.procces import generate_text, CompletionRequest
from app.liama.liama import UserQuery

print("Загрузка роутера")
router = APIRouter(prefix='/generate', tags=['API для генерации с помощью Liama'])


@router.post("/byUserPrompt")
async def generate(prompt: UserQuery):
    """
    :param llama: Зависимость для генерации текста
    :param prompt: Промпт для генерации текста
    :return: Текст сгенерированный нейросетью
    """
    try:
        query = prompt.prompt
        response = await generate_text(query)
        return {'text': response}

    except ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Недопустимый запрос: {str(e)}"
        )