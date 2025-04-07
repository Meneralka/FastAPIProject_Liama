from fastapi import APIRouter, HTTPException, Depends
from pydantic import ValidationError
from app.liama.procces import LlamaService, get_llama_service
from app.liama.liama import UserQuery

print("Загрузка роутера")
router = APIRouter(prefix='/generate', tags=['API для генерации с помощью Liama'])


@router.post("/byUserPrompt")
async def generate(prompt: UserQuery, llama: LlamaService = Depends(get_llama_service)):
    """
    :param llama: Зависимость для генерации текста
    :param prompt: Промпт для генерации текста
    :return: Текст сгенерированный нейросетью
    """
    try:
        query = prompt.prompt
        response = await llama.generate(query)
        return {'text': response}

    except ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Недопустимый запрос: {str(e)}"
        )