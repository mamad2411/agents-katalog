# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A full-stack daily log/tracking application consisting of:
- **Frontend**: React + TypeScript + Vite (in `client/`)
- **Backend**: Python FastAPI with PostgreSQL (in `Backend/`)
- **Data Pipeline**: Rust for processing Joplin notes (in `Backend/Pipeline/`)

The frontend communicates with the backend at `http://127.0.0.1:8000`.

## Common Commands

### Frontend (client/)
```bash
cd client
npm run dev       # Start development server (http://localhost:5173)
npm run build     # Build for production
npm run lint      # Run ESLint
npm run preview   # Preview production build
```

### Backend (Backend/)
```bash
cd Backend
# Activate virtual environment
source .venv/bin/activate

# Run FastAPI server
uvicorn main:app --reload --host 127.0.0.1 --port 8000

# Run database migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"
```

### Rust Pipeline (Backend/Pipeline/)
```bash
cd Backend/Pipeline
cargo build        # Build the pipeline
cargo run          # Run the pipeline
cargo test        # Run tests
```

## Architecture

### Frontend (`client/`)
- **Routing**: React Router v6 with `createBrowserRouter` in `src/main.tsx`
- **API Client**: Axios instance in `src/API.ts` with automatic Bearer token injection from localStorage
- **Styling**: Tailwind CSS v4 (configured via `@tailwindcss/vite` plugin)
- **State**: React hooks for local component state

**Key Routes:**
| Path | Component |
|------|-----------|
| `/` | App (WelcomePage) |
| `/SignUpPage` | RegisterPage |
| `/Login` | LoginBox |
| `/Home` | Home (authenticated) |
| `/Nodes`, `/Sessions`, `/Decision_Log`, `/Dashboard` | Placeholders |

**Auth Flow:**
- Signup: POST to `/v1/authentication/SignUp` with `{username, email, password}`
- Login: POST to `/v1/authentication/Login` with `{username, password}`
- Token stored in `localStorage` under `access_token`
- API interceptor in `src/API.ts` automatically attaches `Authorization: Bearer <token>` to requests

### Backend (`Backend/app/`)
```
Backend/app/
├── core/        # Configuration (app/core/config.py)
├── database/    # SQLAlchemy DB connection
├── models/      # SQLAlchemy ORM models
├── router/v1/   # API routes (authentication, user, notes)
├── schemas/     # Pydantic request/response models
└── services/    # Business logic (auth, notes)
```

**API Endpoints:**
- `/v1/authentication/signup` - User registration
- `/v1/authentication/login` - User login
- `/v1/user` - User management
- `/v1/notes` - Notes CRUD (integrates with Joplin API)

**Database:**
- PostgreSQL via SQLAlchemy ORM
- Alembic for migrations
- Configuration via `app/core/config.py` and `.env` file

**Environment Variables (Backend/.env):**
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT signing key
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiry time
- `JOPLIN_TOKEN` - Joplin API token for notes integration

### Rust Pipeline (`Backend/Pipeline/`)
- Early-stage data processing pipeline for Joplin notes
- Uses Serde for serialization
- Configurable via environment variables



