# api/routes/chat.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from services.chat_service import ChatService
from api.middleware.auth import get_current_user
from database.models.user import User

router = APIRouter()
chat_service = ChatService()

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    sources: list
    message_id: str
    session_id: str

@router.post("/send", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Endpoint pour envoyer un message au chatbot
    
    - **message**: Message de l'utilisateur
    - **session_id**: ID de session (généré automatiquement si absent)
    """
    try:
        # Génération d'un session_id si absent
        session_id = request.session_id or f"session_{current_user.id}_{int(time.time())}"
        
        # Traitement du message
        result = await chat_service.process_message(
            user_id=str(current_user.id),
            message=request.message,
            session_id=session_id
        )
        
        return ChatResponse(
            response=result["response"],
            sources=result["sources"],
            message_id=result["message_id"],
            session_id=session_id
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du traitement : {str(e)}"
        )

@router.get("/history/{session_id}")
async def get_chat_history(
    session_id: str,
    current_user: User = Depends(get_current_user)
):
    """Récupère l'historique d'une session de chat"""
    # Implémentation à compléter
    pass
