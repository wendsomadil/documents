# database/models/user.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    """Rôles utilisateur"""
    DEMO = "demo"               # Utilisateur démo (non enregistré)
    USER = "user"               # Utilisateur enregistré
    AGENT = "agent"             # Agent support
    ADMIN = "admin"             # Administrateur

class UserStatus(str, Enum):
    """Statuts de compte"""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DELETED = "deleted"

class User(BaseModel):
    """Modèle utilisateur"""
    id: Optional[str] = Field(None, alias="_id")
    email: EmailStr
    phone_number: str
    full_name: str
    hashed_password: str
    
    role: UserRole = UserRole.USER
    status: UserStatus = UserStatus.ACTIVE
    
    # Statistiques d'utilisation
    total_messages: int = 0
    total_sessions: int = 0
    
    # Dates
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    
    # Préférences
    preferred_language: str = "fr"
    tts_enabled: bool = True
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "phone_number": "+22670123456",
                "full_name": "Jean Dupont",
                "role": "user",
                "preferred_language": "fr"
            }
        }
        