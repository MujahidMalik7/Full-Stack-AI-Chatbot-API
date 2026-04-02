from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from .database import Base, engine
from .routers import auth, conversations, chat, metrics
from .limiter import limiter
from fastapi.responses import FileResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = "Full Stack AI Chatbot API",
    )

@app.get("/")
def serve_frontend():
    return FileResponse("index.html")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

#CORS
app. add_middleware(
    CORSMiddleware,
    allow_origins=["https://full-stack-ai-chatbot-api-mujahid.up.railway.app/"],
    allow_methods=["*"],
    allow_headers=["*"],
)

#Include Routers
app.include_router(auth.router)
app.include_router(conversations.router)
app.include_router(chat.router)

app.include_router(metrics.router)