# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a monorepo containing a FastAPI backend (Python) and React frontend (TypeScript) for a project called "Monthly". The project uses Clerk for authentication, PostgreSQL for database, and modern web technologies.

## Development Commands

### Backend (Python/FastAPI)
Navigate to `/backend` directory:

```bash
# Install dependencies (uses uv package manager)
uv sync

# Run the FastAPI development server
uv run uvicorn app.main:app --reload

# Run type checking
uv run basedpyright

# Run linting
uv run ruff check
uv run ruff format
```

### Frontend (React/TypeScript)
Navigate to `/frontend` directory:

```bash
# Install dependencies (uses pnpm)
pnpm install

# Run development server on port 3000
pnpm dev

# Build for production and check types
pnpm build

# Run tests
pnpm test

# Load environment variables from parent .env
pnpm with-env [command]
```

### Database
```bash
# Start PostgreSQL database with Docker
docker-compose up -d

# Stop database
docker-compose down
```

## Architecture

### Frontend (`/frontend`)
- **Framework**: React 19 with TypeScript
- **Routing**: TanStack Router with automatic code splitting
- **UI Components**: shadcn/ui + Tailwind CSS v4
- **Styling**: Tailwind CSS v4 with @tailwindcss/vite
- **Data Fetching**: TanStack Query (react-query) + ky for HTTP client
- **API Integration**: 
  - Auto-generated TypeScript types from FastAPI OpenAPI spec
  - Auto-generated React Query hooks for API endpoints
- **Authentication**: Clerk React integration
  - Email OTP authentication
  - Google Sign-in
- **Build Tool**: Vite with path alias `@/` for `src/`
- **Environment**: Uses @t3-oss/env-core for type-safe environment variables (prefix: `VITE_`)

Key files:
- `src/main.tsx`: Application entry point
- `src/routes/__root.tsx`: Root route with Clerk authentication wrapper
- `src/env.ts`: Environment variable validation
- `vite.config.ts`: Vite configuration with TanStack Router plugin

### Backend (`/backend`)
- **Framework**: FastAPI with automatic OpenAPI docs at `/docs`
- **ORM**: SQLModel for database models and queries
- **Database**: PostgreSQL with psycopg driver
- **Authentication**: Clerk Backend API (`clerk-backend-api` package)
  - Requests require Bearer token authentication
  - Token validation through Clerk API
- **Package Management**: uv (Python 3.12+)
- **Configuration**: Pydantic Settings with `.env` file support
- **API Documentation**: Auto-generated OpenAPI spec used for TypeScript type generation

Key files:
- `app/main.py`: FastAPI application entry
- `app/api.py`: API router definitions
- `app/core/config.py`: Settings and database configuration
- Environment variables loaded from parent `../.env`

### Database Configuration
PostgreSQL runs in Docker container with:
- Default port: 5432
- Health checks configured
- Persistent volume for data
- Network: monthly-network

## Environment Variables

Required in `.env` file at project root:
- `VITE_CLERK_PUBLISHABLE_KEY`: Clerk public key for frontend
- `POSTGRES_USER`: Database user
- `POSTGRES_PASSWORD`: Database password
- `POSTGRES_DB`: Database name
- `POSTGRES_SERVER`: Database host
- `POSTGRES_PORT`: Database port (default: 5432)

## Available MCP Tools

Claude Code has the following MCP (Model Control Protocol) servers enabled:

### context7
- Retrieves up-to-date documentation for any library or package
- Use for getting latest API references and examples
- Supports most popular libraries and frameworks

### playwright
- Enables browser automation and interaction
- Can navigate websites, fill forms, take screenshots
- Useful for testing UI flows or gathering web data