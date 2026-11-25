# AGENTS.md - Development Guide for Agentic Coding Agents

This document provides essential information for agentic coding agents (Cursor, Claude, Copilot, Windsurf, etc.) working on **Promptr**.

Promptr is a prompt testing & evaluation sandbox for AI agent builders. The platform is designed primarily to load custom scenarios, define constraints, and systematically stress-test prompts against adversarial workflows. It also features a curated curriculum of 25 missions across 5 progressive levels (Agent Basics → Tool Use → Workflow Control → Guardrails → Evals) as a secondary tool for users to level up their prompting skills.

**License:** MIT  
**Target audience:** Developers building AI agents who want to evaluate, stress-test, and write reliable, production-grade instruction prompts

---

## Codebase Structure (Monorepo)

```
promptr/
├── web/                            # Next.js Frontend
│   ├── src/app/                    # App Router pages
│   ├── src/components/             # React components
│   └── src/lib/                    # Utilities
├── server/                         # FastAPI Backend
│   ├── routers/                    # API Endpoints
│   ├── services/                   # AI logic (LLM service)
│   ├── schemas/                    # Pydantic models
│   └── tests/                      # Python unit & integration tests
├── Makefile                        # Root orchestrator
└── package.json                    # Root monorepo scripts
```

---

## Package Managers & Core Commands

MUST DO - ALWAYS ADD UNIT TESTS FOR EVERY NEW CODE ADDED

Always check for linting and formatting errors at the end

### Root (Monorepo)

```bash
# Install all dependencies
pnpm install

# Start both frontend and backend
pnpm dev

# Run all tests
pnpm test

# Format all codebases
pnpm format

# Lint all codebases
pnpm lint
```

### Frontend (Next.js + TypeScript)

Always use **pnpm** — never npm or yarn.

```bash
# Run from root
pnpm --filter web dev
pnpm --filter web build
pnpm --filter web test
pnpm --filter web lint
```

### Backend (FastAPI + Python)

The backend lives in `./server/`. Use `uv` for dependency management.

```bash
# Run from root
make -C server dev
make -C server test
make -C server format
make -C server lint
```

---

## Environment Variables

Copy `.env.example` to `.env` and fill in values.

| Variable           | Description                                               |
| ------------------ | --------------------------------------------------------- |
| `DATABASE_URL`      | MongoDB connection string                                 |
| `AUTH_SECRET`       | JWT secret for backend session token signing/validation  |
| `GITHUB_CLIENT_ID`  | GitHub OAuth App client ID                                |
| `GITHUB_CLIENT_SECRET` | GitHub OAuth App client secret                            |
| `OPENAI_API_KEY`    | OpenAI API key for backend evaluations                    |

---

## Code Style Guidelines

### TypeScript (Frontend)

- Strict mode enabled
- Functional components only
- Use Tailwind CSS with the **Cyber-Mint** palette (`#48d8a4`)
- Use **shadcn/ui** primitives
- Bold Normal Case for primary buttons

### Python (Backend)

- **Strict 300-line limit**: NO code file should ever exceed 300 lines. This ensures high readability and forces modularization of complex services (e.g., separating prompts into dedicated files).
- Try to always follow SOLID principles wherever possible
- Use Pydantic `BaseModel` for all request/response bodies
- Use `async def` for all route handlers
- Parse LLM JSON responses defensively using `_parse_llm_json`
- Return structured error messages via `HTTPException`
- Use `loguru` for beautiful logging

---

## Architectural Patterns

### Data Flow

```
User → Next.js frontend (App Router)
     → API Route (web/src/app/api/...)
     → FastAPI backend (POST /...)
     → OpenAI API (or other LLM)
     → Structured JSON response
     → Frontend renders feedback
```

### AI Integration

- **Backend**: uses `openai` Python SDK with GPT models.
- **JSON Output**: LLM responses **always** return JSON — strip fences before parsing using the shared utility.

---

## Testing Expectations

- **Frontend**: Vitest + React Testing Library. Run with `pnpm --filter web test`.
- **Backend**: pytest with mocked LLM API calls. Run with `make -C server test`.

---

## Debugging Tips

**Frontend**

- Next.js 404/Hydration errors? Run `pnpm clean`.
- Check `web/src/env.js` for environment variable schema validation.

**Backend**

- JSON parse failures? Check the stripping logic for ` ```json ` fences.
- Use `loguru` logs to trace AI reasoning and backend state.

---

Help make Promptr the best place to learn prompt engineering for AI agents. Contributions welcome at https://github.com/shreyansh232/promptr.
