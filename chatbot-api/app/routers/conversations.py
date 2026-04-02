from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..dependencies import get_db, get_current_user

router = APIRouter(prefix = 
'/conversations', tags = ['conversations'])

@router.get("/", response_model = list[schemas.ConversationResponse])
def list_conversations(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    conversations = db.query(models.Conversation).filter(models.Conversation.user_id == current_user.id).all()
    return conversations

@router.get("/{conversation_id}/messages", response_model=list[schemas.MessageResponse])
def get_messages(conversation_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    conversation = db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    if conversation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    messages = db.query(models.Message).filter(
        models.Message.conversation_id == conversation_id
    ).order_by(models.Message.created_at).all()
    return messages

@router.get("/{conversation_id}", response_model = schemas.ConversationResponse)
def get_conversation(conversation_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    conversation = db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    if conversation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this conversation")

    return conversation

@router.post("/", response_model = schemas.ConversationResponse)
def create_conversation(conversation: schemas.ConversationCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_conversation = models.Conversation(
        title = conversation.title,
        user_id = current_user.id
    )
    db.add(new_conversation)
    db.commit()
    db.refresh(new_conversation)
    return new_conversation


@router.delete("/{conversation_id}")
def delete_conversation(conversation_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    conversation = db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    if conversation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this conversation")

    db.delete(conversation)
    db.commit()
    return {"detail": "Conversation deleted successfully"}