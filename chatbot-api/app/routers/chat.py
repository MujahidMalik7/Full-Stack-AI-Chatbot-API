import os
import anthropic
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import desc
from sqlalchemy.orm import Session
from .. import models, schemas
from ..dependencies import get_db, get_current_user
from ..limiter import limiter
from fastapi import Request

router = APIRouter(prefix='/chat', tags=['chat'])
client = anthropic.AsyncAnthropic(api_key = os.getenv("ANTHROPIC_API_KEY")) 

@router.post("/")
@limiter.limit("20/minute")
async def chat(request: Request, body: schemas.ChatRequest, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    conversation = db.query(models.Conversation).filter(models.Conversation.id == body.conversation_id).first()
    #Checking Authentication
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    if conversation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this conversation")

    #Save User Message to DB 
    user_message = models.Message(
        role = "user",
        conversation_id = body.conversation_id,
        content = body.message
    )
    db.add(user_message)
    db.commit()

    #Fetch Conversation History
    messages = db.query(models.Message).filter(models.Message.conversation_id == body.conversation_id).order_by(desc(models.Message.created_at), models.Message.id).limit(20).all()
    history = [
        {"role": m.role, "content": m.content} for m in reversed(messages)
    ]

    #Call Anthropic API
    async def stream_response(db):
        full_response_content = ""
        try:
            async with client.messages.stream(
                model="claude-haiku-4-5",
                max_tokens = 1024, 
                messages = history
            ) as stream:
                async for text_chunk in stream.text_stream:
                    full_response_content += text_chunk
                    yield f"data: {text_chunk}\n\n"
        
            #Save Assistant Response to DB
            assistant_message = models.Message(
                role = "assistant",
                conversation_id = body.conversation_id,
                content = full_response_content        
            )
            db.add(assistant_message)
            db.commit()
        except Exception as e:
            yield f"data: [ERROR] {str(e)}\n\n"
            db.rollback()
        finally:
            yield "data: [DONE]\n\n"

    #Return ChatResponse
    return StreamingResponse(content=stream_response(db), media_type="text/event-stream")