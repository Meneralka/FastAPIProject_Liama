import httpx
from fastapi import HTTPException
from pydantic import BaseModel

from app.config import settings


class CompletionRequest(BaseModel):
    prompt: str
    temperature: float = 0.7
    max_tokens: int = 200

async def generate_text(text: str):
    try:
        request = CompletionRequest(prompt=text)
        full_prompt = f"{settings.llama.system_prompt}\n\nUser: {request.prompt}\nAssistant:"
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.llama.llama_url}/completion",
                json={
                    "prompt": full_prompt,
                    "temperature": request.temperature,
                    "n_predict": request.max_tokens
                },
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Ошибка подключения к Llama: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка")