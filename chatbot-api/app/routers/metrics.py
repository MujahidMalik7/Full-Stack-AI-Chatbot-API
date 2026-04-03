from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from ..dependencies import get_db, get_admin_user
from .. import models

router = APIRouter(prefix='/system', tags=['system'])

#Health Endpoint
@router.get("/health")
def health():
    """Returns the health status of the API."""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

@router.get("/metrics")
def get_metrics(_ = Depends(get_admin_user), db: Session = Depends(get_db)):
    """Queries the database for global usage statistics."""
    total_users = db.query(models.User).count()
    total_conversations = db.query(models.Conversation).count()
    total_messages = db.query(models.Message).count()

    return {
        "total_users": total_users,
        "total_conversations": total_conversations,
        "total_messages": total_messages
    }
