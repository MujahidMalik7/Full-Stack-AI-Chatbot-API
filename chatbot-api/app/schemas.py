from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

#Authentication Schemas
class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool
    created_at:  datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str


#Conversation Schemas
class ConversationCreate(BaseModel):
    title: Optional[str] = None

class ConversationResponse(BaseModel):
    id: int
    title: Optional[str] = None
    user_id: int
    created_at: datetime 

    class Config:
        from_attributes = True

#Message Schemas
class MessageCreate(BaseModel):
    role: str
    content: str

class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    conversation_id: int
    created_at: datetime

    class Config:
        from_attributes = True

#Chat Schemas
class ChatRequest(BaseModel):
    conversation_id: int
    message: str = Field(min_length=1, max_length=2000)
    
class ChatResponse(BaseModel): 
    message: str
    conversation_id: int