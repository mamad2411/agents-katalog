---
name: new-app-bootstrap
description: Creates the initial structure for a new application with README, VERSION, dependencies, Docker, ER diagram, and tests. Use when the user asks to create a new app, bootstrap a project, scaffold, or set up initial project structure.
---

# New App Bootstrap

When creating a new application from scratch, ensure all of the following exist. Do not show code to the user unless asked; apply changes via tools.

## Mandatory checklist

Copy and complete:

```
- [ ] README.md with installation and run instructions
- [ ] VERSION file at project root (semver, e.g. 0.1.0)
- [ ] requirements.txt or package.json with dependencies
- [ ] .env.example with all variables and short explanations
- [ ] docker-compose.yml (full stack)
- [ ] docker-compose.app-only.yml (app only)
- [ ] Dockerfile for the app
- [ ] .dockerignore for the app/language
- [ ] diagrama_er.md (Mermaid.js ER diagram) at app root
- [ ] funcoes.md at project root (list and explain functions)
- [ ] tests/ with test_<module>.py (pytest)
```

## File purposes

| File / folder | Purpose |
|---------------|---------|
| `README.md` | Installation, run, and build commands |
| `VERSION` | Single source of truth for version; display in UI or `/version` |
| `requirements.txt` / `poetry.lock` | Locked dependencies |
| `.env.example` | Required env vars; no secrets |
| `docker-compose.yml` | Full stack |
| `docker-compose.app-only.yml` | App only (existing DB/services) |
| `Dockerfile` | App image build |
| `diagrama_er.md` | Mermaid ER diagram; update when schema changes |
| `funcoes.md` | List and brief description of all functions |
| `tests/` | pytest; `test_<module>.py`; aim 80% coverage |

## Conventions

- **DB**: PK `id_nome_da_tabela`, FK `id_nome_da_tabela_key`. Use transactions for multi-table changes.
- **Python**: 3.12+, venv/uv/poetry per project, type hints, Google-style docstrings.
- **Code**: Write directly in the target file; add docstrings and concise comments.

## Optional for technical work

- `analise.md`: Critical points, decisions, Q&A (Markdown).
- `plano.md`: Small, detailed tasks; base on analise.md and funcoes.md; update as done.

Do not invent paths or files; confirm with the user if the project root or app name is unclear.
