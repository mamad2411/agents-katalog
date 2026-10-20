# Project AI Instructions

## Project Overview

OpenLeukemia is a patient-centered platform for organizing leukemia-related medical data, tracking changes over time, extracting structured information from documents, and explaining validated model outputs in plain language.

The product must help patients understand their information without replacing a physician. Treat privacy, explicit consent, and non-diagnostic language as core requirements, not optional polish.

## Tech Stack

- Frontend: React 19, TypeScript, Vite, Vitest, ESLint
- Platform layer: Supabase Auth, Postgres, Storage, Row Level Security, Edge Functions
- AI service: Python 3.12, FastAPI, Pydantic, Uvicorn
- AI/ML: PyTorch, XGBoost, scikit-learn, Gemma or another LLM for extraction and explanation tasks
- Package manager: npm workspaces for the frontend; Python virtual environment for `ai-service`

## Repository Layout

- `frontend/`: React + TypeScript application
- `ai-service/`: Python FastAPI service for ML, extraction, parsing, and model-facing workloads
- `supabase/`: migrations, policies, storage-related platform logic, and Edge Functions
- `ml/`: machine learning workspace
- `docs/`: project documentation
- `PROJECT_CHARTER.md`: product principles and guardrails
- `ARCHITECTURE.md`: system design and data-flow guidance

## Setup

Install frontend dependencies from the repository root:

```sh
npm install
```

Create the AI-service virtual environment:

```sh
cd ai-service
python -m venv .venv
python -m pip install -e ".[dev]"
```

On Windows PowerShell, activate the environment with:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Development

Run the frontend from the repository root:

```sh
npm --workspace frontend run dev
```

Default frontend URL:

```text
http://127.0.0.1:5173
```

Run the AI service from `ai-service/`:

```sh
python -m uvicorn app.main:app --reload
```

Default AI-service URL:

```text
http://127.0.0.1:8000
```

Health check:

```text
http://127.0.0.1:8000/health
```

## Tests And Checks

Frontend checks:

```sh
npm run lint:frontend
npm run typecheck:frontend
npm test --workspace frontend
npm --workspace frontend run build
```

AI-service checks:

```sh
cd ai-service
python -m ruff check .
python -m pytest
python -m mypy app
```

Makefile shortcuts:

```sh
make frontend-lint
make frontend-typecheck
make ai-service-lint
make ai-service-test
```

Run the checks most relevant to the files you changed. If a check cannot be run, say why and name the command that should be run next.

## Code Style

- Follow the existing style in neighboring files before adding a new pattern.
- Prefer clear names over clever names.
- Keep functions small and responsibility-focused.
- Add comments only when they genuinely reduce reading effort.
- Use typed models and structured parsing instead of ad hoc string manipulation.
- Do not add dependencies unless the local implementation would be materially worse without them.
- Do not change public APIs, data contracts, routes, schemas, or consent behavior without an explicit reason.
- Keep patient-facing copy calm, careful, and non-diagnostic.

## Architecture Rules

- Use Supabase for routine product workflows: auth, CRUD, storage, consent records, and access-control paths.
- Keep Row Level Security and explicit consent central to data access.
- Use the Python AI service only when the task genuinely needs Python, ML, parsing, OCR, extraction, or heavier compute.
- Keep FastAPI route handlers thin. Put reusable Python logic in services and domain modules.
- Keep frontend code feature-oriented and reuse existing UI, layout, and testing patterns.
- Treat LLM output as explanation or candidate extraction, not as a medical decision.
- High-risk extracted medical values should be reviewable before becoming canonical records.
- Keep identity data and medical data conceptually separate.

## Product And Safety Rules

- Registration does not mean blanket consent.
- Patient data belongs to the patient.
- Every consent should be separate, explicit, auditable, and revocable.
- AI may summarize and explain, but must not diagnose, recommend treatment, or make urgent clinical judgments.
- Structured ML may support prediction and trend detection; LLMs may support extraction and explanation.
- Prefer minimal collection for privacy-sensitive workflows.

## Frontend Rules

- Build mobile-first responsive layouts.
- Maintain light and dark theme support.
- Preserve accessible interaction patterns for menus, forms, dialogs, and controls.
- Keep the public site lightweight; avoid unnecessary heavy animation, video, or large assets.
- Keep brand color usage centered on red without making every surface the same hue.

## AI-Service Rules

- Use explicit Pydantic schemas for request and response bodies.
- Keep domain behavior in `app/domains/`.
- Keep route modules focused on HTTP concerns.
- Maintain strict typing and pass `mypy` for `app`.
- Keep model outputs explainable and non-diagnostic.

## AI Agent Behavior

- Read nearby code, tests, and documentation before editing.
- Make minimal, focused changes that preserve existing architecture.
- Do not rewrite unrelated files or clean up unrelated churn.
- Respect uncommitted user changes.
- Add or update tests when behavior changes.
- After edits, run the most relevant checks when practical.
- When touching medical, consent, auth, or privacy-sensitive behavior, be extra conservative and call out any residual risk.
