import asyncio
from typing import AsyncGenerator
from app.config import settings


class LlamaService:
    def __init__(self):
        self.process = None
        self.system_prompt = settings.llama.system_prompt

    async def start(self):
        self.process = await asyncio.create_subprocess_exec(
            settings.llama.main,
            "-m", settings.llama.model_path,
            "--ctx-size", "2048",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

    async def generate(self, prompt: str) -> str:
        full_prompt = f"{self.system_prompt}\n\nUser: {prompt}\nAssistant:"

        self.process.stdin.write(f"{full_prompt}\n".encode())
        await self.process.stdin.drain()

        output = await self.process.stdout.readline()
        return output.decode().strip()

    async def close(self):
        if self.process:
            self.process.terminate()
            await self.process.wait()


async def get_llama_service() -> AsyncGenerator[LlamaService, None]:
    service = LlamaService()
    await service.start()
    try:
        yield service
    finally:
        await service.close()