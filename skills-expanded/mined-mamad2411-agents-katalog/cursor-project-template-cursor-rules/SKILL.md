# Cursor Rules (Project Governance)

Purpose: keep AI + humans aligned, avoid hallucinated requirements, and maintain a clear paper trail.

## Operating Principles
- Always consult `/docs` before major recommendations or changes.
- Treat `business-context/` and `resource-library/` as read-only reference inputs.
- If guidance is derived from the reference folders, explicitly say it is **"informed by the reference library"** (never name files).
- Never invent product requirements. If ambiguous, ask or log an open question in `QUESTIONS.md`.
- Keep a running decision log in `DECISIONS.md`.
- Record assumptions in `ASSUMPTIONS.md` with confidence and validation plan.
- Maintain open questions in `QUESTIONS.md` with owner and impact.
- Prefer small, reviewable changes over large rewrites.
- Maintain traceability: when scope changes, update `SCOPE.md` and note the decision.

## Non-negotiables
- Always consult `/docs` first, then consult `/business-context/` and `/resource-library/` as read-only references.
- Never name or rely on specific filenames from those reference folders.
- If information is missing or ambiguous, log it to `QUESTIONS.md` instead of guessing.
- Keep edits small; update `DECISIONS.md` when a direction is chosen.
- Before any product code changes, ensure `PROJECT.md + SCOPE.md + docs/03-requirements/REQUIREMENTS.md` have minimum viable clarity.

## Working Checklist (Before Major Output)
- Review `/docs` for current brief, requirements, and architecture.
- Scan `DECISIONS.md`, `ASSUMPTIONS.md`, `QUESTIONS.md`, and `SCOPE.md`.
- Reference `business-context/` and `resource-library/` for constraints and best practices.
- If a recommendation depends on those references, label it as **informed by the reference library**.

## Output Standards
- Provide changes in small, reviewable chunks.
- Keep comments concise and purposeful.
- Avoid introducing stack-specific assumptions unless documented.
