---
name: project-template
description: Scaffold a new project with CLAUDE.md, agents, skills, rules, and hooks pre-configured for the project type. Triggers on "new project", "scaffold project", "create template", "init project", "bootstrap project". Provide the project type as argument (python, nextjs, fullstack, api, flutter).
argument-hint: "<type> [name]"
user-invocable: true
---

# Project Template Generator

Scaffold a new project at the current directory with production-ready Claude Code configuration.

**Arguments:** `$ARGUMENTS`

Parse the arguments to extract:
- **type**: python | nextjs | fullstack | api | flutter | generic
- **name**: optional project name (defaults to directory name)

## What Gets Created

Every template generates this structure:

```
project/
├── .claude/
│   ├── settings.json         # Permissions, hooks (project-level)
│   └── CLAUDE.md             # Project-specific instructions
├── CLAUDE.md                 # Root project guidelines
├── README.md                 # Project README
└── [project files]           # Stack-specific scaffold
```

## Template: Python (`python`)

### CLAUDE.md Content

```markdown
# [Project Name]

## Build Commands
- `uv run python -m pytest` — Run tests
- `ruff check .` — Lint
- `ruff format .` — Format
- `uv run python -m mypy .` — Type check

## Tech Stack
- Python 3.13+, uv package manager
- pytest for testing, ruff for linting
- Type hints required on all functions

## Project Rules
- Follow src/ layout with `src/[package]/` structure
- Use pydantic for data validation at boundaries
- Async code uses asyncio (no threading for I/O)
- Tests in `tests/` mirroring src/ structure
```

### .claude/settings.json

```json
{
  "permissions": {
    "allow": [
      "Bash(uv *)",
      "Bash(pytest *)",
      "Bash(ruff *)",
      "Bash(python *)"
    ],
    "deny": [
      "Read(.env)",
      "Bash(rm -rf *)"
    ]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "FILE=$(echo \"$TOOL_INPUT\" | python3 -c \"import sys,json; print(json.load(sys.stdin).get('file_path',''))\" 2>/dev/null); if [ -n \"$FILE\" ] && echo \"$FILE\" | grep -qE '\\.py$'; then ruff check --fix --quiet \"$FILE\" 2>/dev/null; ruff format --quiet \"$FILE\" 2>/dev/null; fi; exit 0",
            "timeout": 10000,
            "statusMessage": "Auto-formatting Python..."
          }
        ]
      }
    ]
  }
}
```

### Scaffold Files
- `pyproject.toml` with project metadata, ruff config, pytest config
- `src/[name]/__init__.py`, `src/[name]/main.py`
- `tests/__init__.py`, `tests/conftest.py`
- `.gitignore` (Python)
- `justfile` with common recipes

---

## Template: Next.js (`nextjs`)

### CLAUDE.md Content

```markdown
# [Project Name]

## Build Commands
- `npm run dev` — Dev server
- `npm run build` — Production build
- `npm run lint` — Lint check
- `npx tsc --noEmit` — Type check

## Tech Stack
- Next.js 16, React 19, TypeScript strict
- Tailwind CSS v4, shadcn/ui
- Biome for formatting/linting

## Project Rules
- Server Components by default
- "use client" only for event handlers, hooks, browser APIs
- Named exports only
- Mobile-first responsive design
- All images use next/image with alt text
```

### .claude/settings.json

```json
{
  "permissions": {
    "allow": [
      "Bash(npm *)",
      "Bash(npx *)",
      "Bash(node *)"
    ],
    "deny": [
      "Read(.env.local)",
      "Bash(rm -rf *)"
    ]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "FILE=$(echo \"$TOOL_INPUT\" | python3 -c \"import sys,json; print(json.load(sys.stdin).get('file_path',''))\" 2>/dev/null); case \"$FILE\" in *.ts|*.tsx|*.js|*.jsx|*.json|*.css) npx biome check --fix \"$FILE\" 2>/dev/null ;; esac; exit 0",
            "timeout": 10000,
            "statusMessage": "Auto-formatting..."
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "if [ -d node_modules ] && [ -f node_modules/.bin/tsc ]; then npx tsc --noEmit --pretty false 2>&1 | head -10; fi; exit 0",
            "timeout": 30000,
            "statusMessage": "Type checking..."
          }
        ]
      }
    ]
  }
}
```

---

## Template: Full-Stack (`fullstack`)

Combines Python backend + Next.js frontend:

### Structure
```
project/
├── backend/          # Python API (FastAPI)
│   ├── src/
│   ├── tests/
│   └── pyproject.toml
├── frontend/         # Next.js app
│   ├── src/
│   └── package.json
├── docker-compose.yml
├── CLAUDE.md
└── justfile
```

### CLAUDE.md adds:
- `docker compose up` for full stack
- `just dev-backend` / `just dev-frontend` shortcuts
- API contract: backend serves at `/api/`, frontend proxies

---

## Template: API (`api`)

Python FastAPI backend only:

### Structure
```
project/
├── src/[name]/
│   ├── api/routes/
│   ├── core/config.py
│   ├── db/models.py
│   ├── schemas/
│   └── main.py
├── tests/
├── alembic/
├── docker-compose.yml
└── pyproject.toml
```

### CLAUDE.md adds:
- `uvicorn src.[name].main:app --reload` dev command
- Alembic migration commands
- API design rules (REST, status codes, error format)

---

## Template: Flutter (`flutter`)

### CLAUDE.md Content

```markdown
# [Project Name]

## Build Commands
- `flutter run` — Run app
- `flutter test` — Run tests
- `flutter analyze` — Static analysis
- `dart format .` — Format code

## Tech Stack
- Flutter 3.41, Dart 3.11
- Riverpod 3 for state management
- GoRouter for navigation
- Material 3 theming

## Project Rules
- StatelessWidget by default
- const constructors everywhere
- Semantics on all interactive widgets
- Feature-first folder structure
```

---

## Template: Generic (`generic`)

Minimal template with just CLAUDE.md and rules — for any project type.

---

## Execution Steps

1. Detect project type from `$ARGUMENTS`
2. If directory is empty, scaffold the full project
3. If directory has existing code, add only the `.claude/` configuration (don't overwrite existing files)
4. Create CLAUDE.md at project root
5. Create `.claude/settings.json` with stack-appropriate hooks and permissions
6. Initialize git if not already a repo
7. Verify: check that the project builds/lints after scaffolding

## Reference

The altmemy template pattern is at: `~/Projects/ai-website-cloner-template/` (example of a Next.js template with full Claude Code config).
