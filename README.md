# Full Stack AI Chatbot API

A production-ready REST API for an AI-powered chatbot built with FastAPI, SQLAlchemy, and Claude (Anthropic). Features JWT authentication, conversation management, streaming responses, and rate limiting.

## Live Demo

**Deployed on Railway:** https://full-stack-ai-chatbot-api-production.up.railway.app/

---

## Tech Stack

- **Backend:** FastAPI (Python)
- **Database:** SQLite (local) / configurable via `DATABASE_URL`
- **AI Model:** Claude Haiku (Anthropic)
- **Auth:** JWT via `python-jose`, bcrypt password hashing
- **Rate Limiting:** SlowAPI
- **Deployment:** Railway + Docker

---

## Project Structure

```
FULL_STACK_AI_CHATBOT/
├── chatbot-api/
│   ├── app/
│   │   ├── routers/
│   │   │   ├── auth.py          # Signup & login endpoints
│   │   │   ├── chat.py          # Streaming chat endpoint
│   │   │   ├── conversations.py # Conversation CRUD
│   │   │   └── metrics.py       # Health & usage stats
│   │   ├── auth.py              # JWT & password utilities
│   │   ├── database.py          # SQLAlchemy engine & session
│   │   ├── dependencies.py      # Reusable FastAPI dependencies
│   │   ├── limiter.py           # Rate limiter setup
│   │   ├── main.py              # App entry point
│   │   ├── models.py            # Database models
│   │   └── schemas.py           # Pydantic schemas
│   ├── index.html               # Frontend (served by FastAPI)
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── requirements.txt
```

---

## API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/signup` | Register a new user |
| POST | `/auth/login` | Login and receive JWT token |

### Conversations
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/conversations/` | List all user conversations |
| POST | `/conversations/` | Create a new conversation |
| GET | `/conversations/{id}` | Get a specific conversation |
| GET | `/conversations/{id}/messages` | Get all messages in a conversation |
| DELETE | `/conversations/{id}` | Delete a conversation |

### Chat
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/chat/` | Send a message (streaming SSE response) |

### System
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/system/health` | Health check |
| GET | `/system/metrics` | Total users, conversations, messages |

---

## Getting Started

### Prerequisites

- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com/)

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd chatbot-api
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file**
   ```env
   ANTHROPIC_API_KEY=your_anthropic_api_key
   SECRET_KEY=your_secret_key_here
   DATABASE_URL=sqlite:///./chatbot.db
   ```

5. **Run the server**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Visit** `http://localhost:8000`

---

## Docker

```bash
docker-compose up --build
```

---

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key | Yes |
| `SECRET_KEY` | JWT signing secret | Yes |
| `DATABASE_URL` | Database connection string | No (defaults to SQLite) |

---

## Features

- **JWT Authentication** — Secure signup/login with bcrypt hashed passwords and 30-minute token expiry
- **Streaming Responses** — Claude's replies stream in real-time via Server-Sent Events (SSE)
- **Conversation History** — Last 20 messages are sent as context to the model on each request
- **Rate Limiting** — 20 requests/minute per IP on the chat endpoint
- **CORS** — Configured for the production Railway domain

---