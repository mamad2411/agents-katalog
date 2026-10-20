# GitHub Copilot Instructions

OpenLeukemia is a patient-centered leukemia data platform. It organizes medical data, tracks changes over time, extracts structured information from documents, and explains validated model outputs in plain language.

## Always Follow

- Preserve explicit consent, privacy-by-default behavior, and patient ownership of data.
- Registration is not blanket consent.
- AI output may summarize, extract, and explain; it must not diagnose, recommend treatment, or make urgent clinical judgments.
- Treat LLM extraction as candidate data until validated or confirmed.
- Prefer minimal, focused changes that match nearby code.
- Do not introduce dependencies, API changes, schema changes, or consent-flow changes without clear need.
- Add or update tests when behavior changes.
- Run or recommend the relevant check after changes.

## Stack And Commands

- Frontend: React 19, TypeScript, Vite, Vitest, ESLint.
- Platform: Supabase Auth, Postgres, Storage, RLS, Edge Functions.
- AI service: Python 3.12, FastAPI, Pydantic, Uvicorn.
- Frontend checks: `npm run lint:frontend`, `npm run typecheck:frontend`, `npm test --workspace frontend`, `npm --workspace frontend run build`.
- AI-service checks from `ai-service/`: `python -m ruff check .`, `python -m pytest`, `python -m mypy app`.

## Workflow

- Read nearby files before editing and follow the existing pattern.
- For multi-file or risky changes, identify touched files and verification steps before implementation.
- Use artifacts as primary evidence: errors, logs, screenshots, issues, plans, and referenced files.
- Verify work with tests, build, lint, typecheck, or visual comparison when practical.
