from pydantic import BaseModel, field_validator

import re


class UserQuery(BaseModel):
    prompt: str

    @field_validator('prompt')
    def check_malicious(cls, v: str) -> str:
        malicious_patterns = [
            r"(игнорируй|ignore).*(инструкции|rules)",
            r"(секрет|пароль|ключ)\b",
            r"(jailbreak|безопасность|отключи.*защиту)",
            r"(внутренн(яя|ей)|confidential)",
            r"(экспорт|выгрузи|exfiltrate).*(данн|data)"]

        for pattern in malicious_patterns:
            if re.search(pattern, v, re.IGNORECASE):
                raise ValueError(f"Обнаружен вредоносный паттерн")

        return v