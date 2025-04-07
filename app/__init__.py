from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.liama.procces import LlamaService
from app.routers import generate

class App:
    def __init__(self):
        self.app = FastAPI(title="Liama", version="1.0.0", lifespan=lifespan)
        self._setup_cors()
        self._include_routers()


    def _setup_cors(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _include_routers(self):
        self.app.include_router(generate.router)


    def get_app(self):
        return self.app


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация сервиса при старте
    llama = LlamaService()
    await llama.start()
    app.state.llama = llama
    yield
    # Очистка при завершении
    await llama.close()


