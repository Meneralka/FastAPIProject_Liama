from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import generate

class App:
    def __init__(self):
        self.app = FastAPI(title="Liama", version="1.0.0")
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

