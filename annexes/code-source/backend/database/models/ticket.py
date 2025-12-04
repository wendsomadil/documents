# database/models/ticket.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

class TicketStatus(str, Enum):
    """Statuts de ticket"""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

class TicketPriority(str, Enum):
    """Priorités de ticket"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class Ticket(BaseModel):
    """Modèle de ticket de support"""
    id: Optional[str] = Field(None, alias="_id")
    ticket_number: str  # Format : TKT-20251203-0001
    
    user_id: str
    user_email: str
    user_name: str
    
    subject: str
    category: str  # "transaction", "account", "technical", "other"
    
    status: TicketStatus = TicketStatus.OPEN
    priority: TicketPriority = TicketPriority.MEDIUM
    
    assigned_to: Optional[str] = None  # ID de l'agent assigné
    
    # Messages associés
    message_ids: List[str] = []
    
    # Résolution
    resolution_notes: Optional[str] = None
    resolved_at: Optional[datetime] = None
    
    # Dates
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Métriques
    first_response_time: Optional[int] = None  # En secondes
    resolution_time: Optional[int] = None      # En secondes
    
    class Config:
        populate_by_name = True
        