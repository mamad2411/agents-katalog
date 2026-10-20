# OpenLeukemia Claude Memory

OpenLeukemia is a patient-centered platform for organizing leukemia-related medical data, tracking changes over time, extracting structured information from documents, and explaining validated model outputs in plain language.

## Stack

- Frontend: React 19, TypeScript, Vite, Vitest, ESLint
- Platform: Supabase Auth, Postgres, Storage, RLS, Edge Functions
- AI service: Python 3.12, FastAPI, Pydantic, Uvicorn
- Package manager: npm workspaces for `frontend`; Python virtualenv for `ai-service`

## Core Rules

- Patient data belongs to the patient.
- Registration is not blanket consent.
- Consent must be separate, explicit, auditable, and revocable.
- AI may summarize, extract, and explain; it must not diagnose, recommend treatment, or make urgent clinical judgments.
- Treat LLM extraction as candidate data until validated or confirmed.
- Prefer Supabase for routine product workflows; use `ai-service/` for Python, ML, OCR, extraction, parsing, and heavier compute.

## Commands

Frontend, from repo root:

```sh
npm install
npm --workspace frontend run dev
npm run lint:frontend
npm run typecheck:frontend
npm test --workspace frontend
npm --workspace frontend run build
```

AI service, from `ai-service/`:

```sh
python -m venv .venv
python -m pip install -e ".[dev]"
python -m uvicorn app.main:app --reload
python -m ruff check .
python -m pytest
python -m mypy app
```

## Working Style

- Read nearby code and docs before editing.
- Make minimal, focused changes and preserve existing architecture.
- Do not rewrite unrelated files or add dependencies without clear need.
- Use typed models and structured parsing instead of ad hoc string handling.
- Keep patient-facing text calm, plain, and non-diagnostic.
- Run the most relevant checks after edits when practical; otherwise name the skipped check.
- Directory-specific `CLAUDE.md` files add local rules when working in those subtrees.

## Claude Workflow Patterns

- Optimize for the user's intended outcome, not a literal step list; find the relevant files yourself when the request is behavioral.
- For unfamiliar code, first explain architecture, data flow, and dependencies before editing.
- Before deleting or broadly refactoring, identify callers, downstream effects, and the files likely to change.
- For multi-file or risky changes, plan the touched files and verification path before editing.
- Match existing patterns by reading a nearby implementation the project already accepts.
- When the user provides an error, log, screenshot, plan output, issue, or file, treat that artifact as primary evidence.
- Build self-check loops into implementation work: write/run tests, build, lint, typecheck, render, compare, or otherwise verify.
- Use measurable targets when available: coverage threshold, latency goal, bundle size, visual delta, or exact API behavior.
- If the user corrects the same mistake or asks to preserve a convention, turn that correction into a durable `CLAUDE.md` rule.
