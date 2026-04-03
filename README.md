# Full Stack AI Chatbot API

A production-ready REST API for an AI-powered chatbot built with **FastAPI**, **PostgreSQL**, and **Claude by Anthropic**. Features JWT authentication, real-time streaming responses via SSE, conversation management, admin access control, and rate limiting — deployed on Railway.

## Live Demo

**🚀 Deployed:** [https://full-stack-ai-chatbot-api-mujahid.up.railway.app](https://full-stack-ai-chatbot-api-mujahid.up.railway.app)

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI (Python 3.10+) |
| Database | SQLite (local) / PostgreSQL (production) |
| AI Model | Claude Haiku 4.5 (Anthropic) |
| Auth | JWT (`python-jose`) + bcrypt password hashing |
| Streaming | Server-Sent Events (SSE) |
| Rate Limiting | SlowAPI |
| Deployment | Railway + Docker |

---

## Project Structure

```
FULL_STACK_AI_CHATBOT/
├── chatbot-api/
│   ├── app/
│   │   ├── routers/
│   │   │   ├── auth.py           # Signup & login endpoints
│   │   │   ├── chat.py           # Streaming chat endpoint
│   │   │   ├── conversations.py  # Conversation CRUD
│   │   │   └── metrics.py        # Health & usage stats (admin only)
│   │   ├── auth.py               # JWT creation & password hashing utilities
│   │   ├── database.py           # SQLAlchemy engine & session factory
│   │   ├── dependencies.py       # Reusable FastAPI dependencies (auth, db, admin)
│   │   ├── limiter.py            # Rate limiter setup
│   │   ├── main.py               # App entry point & middleware
│   │   ├── models.py             # SQLAlchemy ORM models
│   │   └── schemas.py            # Pydantic request/response schemas
│   ├── index.html                # Frontend UI (served by FastAPI)
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── requirements.txt
```

---

## API Endpoints

### Auth
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/signup` | None | Register a new user |
| POST | `/auth/login` | None | Login and receive JWT token |

### Conversations
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/conversations/` | JWT | List all user conversations |
| POST | `/conversations/` | JWT | Create a new conversation |
| GET | `/conversations/{id}` | JWT | Get a specific conversation |
| GET | `/conversations/{id}/messages` | JWT | Get all messages in a conversation |
| DELETE | `/conversations/{id}` | JWT | Delete a conversation |

### Chat
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/chat/` | JWT | Send a message — streams response via SSE |

### System
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/system/health` | None | Health check |
| GET | `/system/metrics` | JWT + Admin | Total users, conversations, messages |

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
| `ANTHROPIC_API_KEY` | Your Anthropic API key | ✅ Yes |
| `SECRET_KEY` | JWT signing secret (use a long random string) | ✅ Yes |
| `DATABASE_URL` | Database connection string | ❌ No (defaults to SQLite) |

**PostgreSQL example:**
```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

---

## Features

### Security
- **JWT Authentication** — Secure signup/login with bcrypt hashed passwords and 30-minute token expiry
- **Role-Based Access Control** — `is_admin` flag on users; admin-only dependency protects sensitive endpoints
- **Input Validation** — Message length capped via Pydantic `Field` constraints to prevent token abuse
- **Rate Limiting** — 20 requests/minute per IP on the chat endpoint via SlowAPI
- **CORS** — Locked to the production Railway domain

### AI & Streaming
- **Real-Time Streaming** — Claude's replies stream token by token via Server-Sent Events (SSE) for instant feedback
- **Sliding Window Context** — Last 20 messages sent as history to Claude on each request, balancing context quality and API cost
- **Async Streaming** — Uses `AsyncAnthropic` client with `async for` to avoid blocking the event loop under concurrent users
- **Graceful Error Handling** — Stream failures trigger `db.rollback()` and return a clean error event to the client

### Database
- **SQLAlchemy ORM** — Python-level models with automatic SQL injection protection
- **PostgreSQL in Production** — Full connection pooling via Railway-managed Postgres
- **Ordered History** — Messages fetched ordered by `(created_at, id)` to prevent timestamp collision bugs

---

## Architecture Notes

**Why two `auth.py` files?**
`app/auth.py` contains pure utility functions (hashing, JWT). `app/routers/auth.py` contains FastAPI route handlers. Keeping them separate avoids circular imports and follows the Single Responsibility Principle.

**Why `yield` in `get_db()`?**
FastAPI's dependency injection supports generator functions. `yield` pauses the function, hands the DB session to the route, then the `finally` block guarantees the session closes — even if an exception occurs mid-request.

**Why stream instead of a normal response?**
LLM responses can take 5–10 seconds to complete. Streaming sends tokens as they're generated, giving users instant feedback instead of a blank screen.

---

## Interactive API Docs

FastAPI provides auto-generated docs at:
- **Swagger UI:** `/docs`
- **ReDoc:** `/redoc`