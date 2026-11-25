# test1 Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-12-22

## Active Technologies
- TypeScript 5.5.3, React 18.3.1 (005-improve-frontend-ui)
- N/A (UI-only feature, no data persistence changes) (005-improve-frontend-ui)
- Python 3.12 + FastAPI, SQLAlchemy 2.0 (async), Alembic, Pydantic 2.0, psycopg (async), Supabase PostgreSQL (006-supabase-migration)
- Local PostgreSQL → Supabase PostgreSQL (cloud) (006-supabase-migration)
- Python 3.12 (FastAPI backend), TypeScript/React frontend + FastAPI, SQLAlchemy, Supabase Python client, psycopg (PostgreSQL driver), React, Vite (002-supabase-migration)
- Supabase (cloud-hosted PostgreSQL) as primary persistent store, replacing local PostgreSQL (002-supabase-migration)

- TypeScript 5.x (latest stable), React 18.x (latest stable), Node.js 18+ (LTS recommended) (001-init-react-app)

## Project Structure

```text
backend/
frontend/
tests/
```

## Commands

npm test && npm run lint

## Code Style

TypeScript 5.x (latest stable), React 18.x (latest stable), Node.js 18+ (LTS recommended): Follow standard conventions

## Recent Changes
- 002-supabase-migration: Added Python 3.12 (FastAPI backend), TypeScript/React frontend + FastAPI, SQLAlchemy, Supabase Python client, psycopg (PostgreSQL driver), React, Vite
- 006-supabase-migration: Added Python 3.12 + FastAPI, SQLAlchemy 2.0 (async), Alembic, Pydantic 2.0, psycopg (async), Supabase PostgreSQL
- 005-improve-frontend-ui: Added TypeScript 5.5.3, React 18.3.1


<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
