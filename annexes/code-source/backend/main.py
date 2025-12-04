# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import chat, audio, tickets, users

app = FastAPI(title="ZamaPay Assistant IA API", version="1.0")

# Configuration CORS pour communication Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend en développement
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enregistrement des routes
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])
app.include_router(audio.router, prefix="/api/v1/audio", tags=["Audio"])
