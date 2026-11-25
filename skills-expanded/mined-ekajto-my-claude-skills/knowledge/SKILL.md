---
name: knowledge
description: Use to exhaustively map a repository by reading every source file and produce a complete CONTEXT.md + memory files. Triggers: "map the project", "explore all the code", "generate the CONTEXT.md", "/knowledge".
---

# Project Knowledge Expert — Total Mapping

You are the absolute expert of this repository. You don't summarize — you map with surgical precision. Every source file is read, every important function is noted, every endpoint is documented. You produce an exhaustive source of truth that allows any developer to understand the project without opening a single file.

## ABSOLUTE RULE: ZERO SHORTCUTS

You are not allowed to:
- Skip a source file because it's "similar to the others"
- Write `...` or `etc.` in the tables — every row must be complete
- Summarize in one line what deserves a detailed table
- Infer the content of a file without having read it
- Limit yourself to a predefined list of files

If a file exceeds 300 lines → read in multiple passes (`offset` + `limit`). Never truncated.

---

## Phase 0 — Dynamic repository detection

Before any code reading, map the repo structure. The goal is to discover:
- The languages present
- The framework(s) used
- The folder structure (monorepo, single service, multi-package…)
- The root configuration files
- The existing documentation files

### Inventory commands (all mandatory)

```bash
# 1. General tree (2 levels, excluding .git / node_modules / .venv / __pycache__ / dist / build)
find . -maxdepth 2 \
  -not -path './.git/*' \
  -not -path '*/node_modules/*' \
  -not -path '*/.venv/*' \
  -not -path '*/__pycache__/*' \
  -not -path '*/dist/*' \
  -not -path '*/build/*' \
  -not -path '*/.next/*' \
  | sort

# 2. Detect languages present
find . -name "*.py" -not -path '*/.venv/*' -not -path '*/__pycache__/*' | wc -l
find . \( -name "*.ts" -o -name "*.tsx" \) -not -path '*/node_modules/*' -not -path '*/.next/*' | wc -l
find . -name "*.go" | wc -l
find . -name "*.rs" | wc -l
find . -name "*.java" | wc -l
find . -name "*.rb" | wc -l

# 3. Dependency files (framework detection)
find . -maxdepth 3 \( \
  -name "package.json" -o \
  -name "requirements.txt" -o \
  -name "pyproject.toml" -o \
  -name "Cargo.toml" -o \
  -name "go.mod" -o \
  -name "Gemfile" -o \
  -name "pom.xml" -o \
  -name "build.gradle" \
\) -not -path '*/node_modules/*' | sort

# 4. Root configuration files
find . -maxdepth 1 \( \
  -name "*.json" -o \
  -name "*.toml" -o \
  -name "*.yaml" -o \
  -name "*.yml" -o \
  -name "*.env.example" -o \
  -name "Dockerfile" -o \
  -name "docker-compose*.yml" -o \
  -name "*.config.*" \
\) | sort

# 5. Existing documentation files
find . -name "*.md" \
  -not -path '*/node_modules/*' \
  -not -path '*/.venv/*' \
  | sort

# 6. Migrations / DB schemas
find . \( -name "*.sql" -o -name "schema.*" \) \
  -not -path '*/node_modules/*' | sort
find . -path "*/migrations/*.py" -not -path '*/.venv/*' | sort
find . -path "*/alembic/versions/*.py" | sort

# 7. Complete source files (for Phase 1)
# Python
find . -name "*.py" \
  -not -path '*/.venv/*' \
  -not -path '*/__pycache__/*' \
  -not -path '*/migrations/*' \
  | sort

# TypeScript / TSX
find . \( -name "*.ts" -o -name "*.tsx" \) \
  -not -path '*/node_modules/*' \
  -not -path '*/.next/*' \
  -not -path '*/dist/*' \
  | sort

# Go
find . -name "*.go" -not -path '*/vendor/*' | sort

# 8. CI/CD and infra files
find . \( \
  -name "*.github" -o \
  -path "*/.github/workflows/*.yml" -o \
  -name "Dockerfile*" -o \
  -name "docker-compose*.yml" -o \
  -name "*.tf" \
\) -not -path '*/node_modules/*' | sort
```

### After the inventory: determine the repository's architecture

From the results, identify:

1. **Repo type**: monorepo / single service / multi-package / polyglot
2. **Main languages** (sort by file count)
3. **Detected frameworks**:
   - Python → FastAPI / Django / Flask / standalone scripts
   - TypeScript/JS → Next.js / Express / NestJS / React SPA / Node scripts
   - Go → gin / echo / stdlib
   - Rust → actix / axum / CLI
4. **Database**: PostgreSQL (SQLAlchemy/asyncpg) / SQLite / MongoDB / Redis / none
5. **Folder structure**: name each sub-project or package identified

**This analysis ENTIRELY guides Phase 1 and Phase 2.** Never apply a hardcoded structure — adapt to the realities of the repo.

---

## Phase 1 — Full reading of every source file

### Reading order (adapt to the structure detected in Phase 0)

**Group A — Documentation and configuration (always first)**
- All `.md` files found: `CLAUDE.md`, `README.md`, `ARCHITECTURE.md`, `CONTEXT.md`, `TODO.md`, `LOGS.md`, and all those detected
- All `.env.example` files (never the real `.env`)
- All dependency files: `requirements.txt`, `pyproject.toml`, `package.json`, `go.mod`, `Cargo.toml`…
- All root config files: `docker-compose.yml`, `Dockerfile`, CI/CD workflows

**Group B — Schemas and migrations**
- All `.sql` files found
- All Alembic migration files (`alembic/versions/*.py`) or Django
- ORM schema definition files (`models.py`, `schema.py`, `entities/*.ts`…)

**Group C — Entrypoints and application configuration**
- The `main.py` / `app.py` / `__main__.py` / `server.py` / `index.ts` / `main.ts` files
- The `config.py` / `settings.py` / `config.ts` / `.env.example` files
- The global routing files: `routes.py`, `router.ts`, `app/layout.tsx`

**Group D — Full source code** (read EVERY file identified in Phase 0)
- All Python `.py` files except `.venv` / `__pycache__` / migrations
- All TypeScript `.ts` / `.tsx` files except `node_modules` / `.next` / `dist`
- All Go `.go` files except `vendor`
- All other source files according to detected languages

**Group E — Memory and skills files**
- All files in `memory/` (if present)
- All files in `.claude/commands/` (the other skills)
- `tasks/todo.md` or any task tracking file

### Reading rules

- Each file: read **in full**, not as an excerpt
- File > 300 lines → successive passes with `offset` + `limit`
- Use `Grep` to find patterns when in doubt (`grep -rn "pattern" .`)
- Count exactly how many files were read — report it in Phase 4

---

## Phase 2 — Generate / update `CONTEXT.md`

**Location**: check if a `CONTEXT.md` already exists in the repo (root, `.claude/`, `docs/`). If it exists, **rewrite it entirely**. If not, **create it at the root** (or in `.claude/` if that folder exists).

This file must be complete enough that a developer who has never seen the project understands in detail how everything works without opening a single source file.

### Mandatory structure (adapt the sections to the real architecture)

```
# [Project name] — Complete Context
> Updated on [DATE] by /knowledge — [N] source files read

---

## 0. Project snapshot ([DATE])

┌──────────────────────────────────────────────────────┬──────────┬──────────────────────────────────────────┐
│ Feature / Module                                     │ State    │ Notes                                    │
├──────────────────────────────────────────────────────┼──────────┼──────────────────────────────────────────┤
│ [every real feature/module found in the code]       │ ✅/🟡/🔴 │ [what blocks, what is WIP, mocks]        │
└──────────────────────────────────────────────────────┴──────────┴──────────────────────────────────────────┘

---

## 1. Vision & functional scope

[Narrative description of the project: what it does, for whom, why.
At least 3 paragraphs. Complete sentences, no vague bullet points.]

---

## 2. Global architecture

[ASCII diagram of the full flow: services, ports, protocols, external dependencies]

[Narrative explanation of each component]

---

## 3. Repository structure

[ASCII tree of the repo (excluding node_modules / .venv / dist / build / .git)]
Each file/folder annotated with its role on the same line.

Example:
monrepo/
├── backend/                    — Python FastAPI API
│   ├── api/                    — FastAPI routers
│   ├── models/                 — SQLAlchemy models
│   ├── services/               — business logic
│   ├── alembic/                — PostgreSQL migrations
│   └── main.py                 — entrypoint, CORS, lifespan
├── web/                        — Next.js frontend
│   ├── app/                    — App Router pages
│   ├── components/             — React components
│   └── lib/                    — utilities, types, API client
├── agent/                      — background workers/agents
└── tasks/todo.md               — task tracking

---

## 4. [Sub-project / Service A] — Complete architecture

> Adapt this section for each sub-project or service detected.
> E.g., "Backend FastAPI", "Frontend Next.js", "Agent Worker", "CLI", "Package shared"…

### 4.1 Annotated file tree

[ASCII tree of all files in the sub-project with annotations]

### 4.2 Configuration and environment variables

┌──────────────────────────┬──────────┬────────────────────┬────────────────────────────────────────┐
│ Variable / Parameter     │ Type     │ Default            │ Usage                                  │
├──────────────────────────┼──────────┼────────────────────┼────────────────────────────────────────┤
│ [each real env var]      │ str/int… │ [value or —]       │ [what it controls in the code]         │
└──────────────────────────┴──────────┴────────────────────┴────────────────────────────────────────┘

### 4.3 API endpoints (if applicable)

> One table per router/route group.

┌────────────────────────────────────────┬────────┬──────────────────────────────┬────────────────────────────────────────────┬──────┐
│ Path                                   │ Method │ Parameters                   │ Real behavior                              │ State│
├────────────────────────────────────────┼────────┼──────────────────────────────┼────────────────────────────────────────────┼──────┤
│ [each route found in the code]         │ GET…   │ [query/path/body params]     │ [what the function REALLY does]            │ ✅/🟡│
└────────────────────────────────────────┴────────┴──────────────────────────────┴────────────────────────────────────────────┴──────┘

### 4.4 Data models / Types

> One table per Pydantic model / TypeScript interface / Go struct / entity…

┌──────────────────────────┬────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Model / Type             │ Fields (name: type [= default / nullable])                                                      │
├──────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────┤
│ [ModelName]              │ [field1: type1, field2: type2, ...]                                                             │
└──────────────────────────┴────────────────────────────────────────────────────────────────────────────────────────────────┘

### 4.5 Database schema (if applicable)

> One section per table / collection.

#### Table `[table_name]`
┌──────────────────┬─────────────────┬──────────────────────────────────────────────────────────┐
│ Column           │ SQL type        │ Description + constraints                                │
├──────────────────┼─────────────────┼──────────────────────────────────────────────────────────┤
│ [column]         │ [type]          │ [role + nullable/unique/FK/default]                      │
└──────────────────┴─────────────────┴──────────────────────────────────────────────────────────┘
Indexes: [list]
Relations: [FKs and their target table]

### 4.6 Services / Key functions

> For each service/utility file: list all exposed functions.

#### `[path/file]`
┌───────────────────────────────────────────┬────────────────────────────────────────────────────────────┐
│ Function / Export                         │ What it does                                               │
├───────────────────────────────────────────┼────────────────────────────────────────────────────────────┤
│ functionName(param: Type) → ReturnType    │ [precise description of the logic]                         │
└───────────────────────────────────────────┴────────────────────────────────────────────────────────────┘

### 4.7 Pages / Screens (if frontend)

┌──────────────────────────────────┬────────────────────┬──────────────────────────────────────────────────────────────────┐
│ File                             │ URL route          │ Role + data loaded + API calls                                   │
├──────────────────────────────────┼────────────────────┼──────────────────────────────────────────────────────────────────┤
│ [page file]                      │ /[route]           │ [what the page does, its fetches, its key states]                │
└──────────────────────────────────┴────────────────────┴──────────────────────────────────────────────────────────────────┘

### 4.8 Dependencies

┌─────────────────────────────────┬─────────────────┬──────────────────────────────────────────────────┐
│ Package                         │ Version         │ Usage in the project                             │
├─────────────────────────────────┼─────────────────┼──────────────────────────────────────────────────┤
│ [package]                       │ [version]       │ [what it brings concretely]                      │
└─────────────────────────────────┴─────────────────┴──────────────────────────────────────────────────┘

> Repeat Section 4 for each sub-project / service identified in Phase 0.

---

## 5. Data flows & interactions between services

[ASCII diagrams of the main flows: who calls whom, in what order, with what data]

[E.g.: Frontend → API → Service → DB; Worker → Redis → API; etc.]

---

## 6. Authentication & security (if applicable)

[Auth stack: JWT / OAuth2 / sessions / API keys / mTLS]
[Full flow with ASCII diagram]
[Auth-related env variables]
[What is implemented vs. what is planned]

---

## 7. Infrastructure & deployment (if applicable)

[Docker / docker-compose: defined services, exposed ports, volumes]
[CI/CD: triggers, steps, artifacts]
[Production vs. dev env variables]

---

## 8. State of mocks / WIP / technical debt

> For each not-yet-finalized element found in the code.

┌─────────────────────────────────────────────────┬──────────────┬───────────────────────────────────────────────────────┐
│ Feature / Endpoint / Component                  │ State        │ Reason / Blocker / TODO                               │
├─────────────────────────────────────────────────┼──────────────┼───────────────────────────────────────────────────────┤
│ [element]                                       │ 🟡 WIP/Mocked│ [why, what's missing, external dependency]            │
└─────────────────────────────────────────────────┴──────────────┴───────────────────────────────────────────────────────┘

---

## 9. Task tracking — TODO summary

> Structured summary of the task tracking file (tasks/todo.md or equivalent).

┌──────────────────────────────────────────────┬───────────┬──────────────────────────────────────────────────┐
│ Task / Feature                               │ State     │ Remaining sub-tasks                              │
├──────────────────────────────────────────────┼───────────┼──────────────────────────────────────────────────┤
│ [section title]                              │ ❌/🟡/✅  │ [what remains to do]                             │
└──────────────────────────────────────────────┴───────────┴──────────────────────────────────────────────────┘

---

## 10. Open questions & pending decisions

> Everything marked `[?]`, `TODO`, `FIXME`, `to confirm`, `to define` in the code and the doc.

1. [Question / decision] — *Context: [file:line or doc where it's mentioned]*
2. …
```

---

## Phase 3 — Memory update

Create or update the memory files in `memory/` (look for this folder dynamically — it may be at the root, in `.claude/`, or to be created).

### Files to write or update

**`memory/project_status.md`**
- ✅/🟡/🔴 state of each feature/module
- Precise list of what is mocked/WIP and why
- Active bugs and identified blockers

**`memory/project_architecture.md`**
- Complete tech stack with versions
- Data flow schematized (ASCII)
- DB structure (tables + key columns)
- Services and their responsibilities

**`memory/backend_routes.md`** (or equivalent depending on stack)
- Exhaustive catalog of all API routes
- Method, path, parameters, real behavior, state for each route

**`memory/frontend_screens.md`** (if frontend present)
- All screens/pages with their URL routes
- Key components and their roles
- API calls made by component

**`memory/open_questions.md`**
- Open questions found in the code and the doc
- Pending decisions
- Blocking dependencies (external or internal)

Mandatory frontmatter format for each file:
```markdown
---
name: [short explicit name]
description: [one sentence — file content, used to decide if relevant]
type: project
---
```

### Update `memory/MEMORY.md`

Rebuild the full index. One line per memory file, format:
```
- [Title](file.md) — [short hook describing the content in < 100 chars]
```

---

## Phase 4 — Summary report

Display this report in the conversation at the end:

```
╔══════════════════════════════════════════════════════════════════════╗
║           /knowledge — [PROJECT] — [DATE]                           ║
╠══════════════════════════════════════════════════════════════════════╣
║  Files read          : [exact N — per language]                     ║
║  Files written       : [N — CONTEXT.md + memories]                  ║
╠══════════════════════════════════════════════════════════════════════╣
║  DETECTED STACK                                                      ║
║  [Language 1] : [N] files — [detected framework]                    ║
║  [Language 2] : [N] files — [detected framework]                    ║
║  DB: [DB type + ORM if applicable]                                  ║
╠══════════════════════════════════════════════════════════════════════╣
║  FEATURE STATE                                                       ║
║  ✅ Operational : [list]                                             ║
║  🟡 WIP / Mocked: [list with short reason]                           ║
║  🔴 Blocker     : [list]                                             ║
╠══════════════════════════════════════════════════════════════════════╣
║  READING COVERAGE                                                    ║
║  [Language]  : [N read] / [N found] files                           ║
╠══════════════════════════════════════════════════════════════════════╣
║  NOTABLE DISCOVERIES                                                 ║
║  [Undocumented points, doc vs code divergences,                     ║
║   technical debt, unexpected behaviors]                              ║
╠══════════════════════════════════════════════════════════════════════╣
║  UPDATED DOCUMENTS                                                   ║
║  [path/file] — [created / updated]                                  ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

## Absolute rules

**Reading:**
- Read EACH source file identified in Phase 0 — no exception
- File > 300 lines → read in multiple passes — never truncated
- Never infer content without having read it
- Use `Grep` to find patterns if in doubt

**Writing:**
- `...` and `etc.` forbidden in tables
- Every table = as many rows as real elements found in the code
- The described behaviors must match the code read, not what the doc says
- Mark `[?]` anything ambiguous rather than inventing

**Adaptation to the repo:**
- No hardcoded structure — everything is discovered dynamically in Phase 0
- If the repo has no frontend → remove the frontend sections
- If it's a monorepo with 5 services → create one Section 4 per service
- If it's a CLI with no API → adapt the "Endpoints" sections to "CLI commands"
- If it's a library package → document the public exported API
- The section names, file paths and structures ALWAYS adapt to the reality of the repo

**Never read:**
- `.env` files (secrets)
- `node_modules/`, `.venv/`, `__pycache__/`, `dist/`, `build/`, `.next/`, `.git/` folders
- Lock files: `package-lock.json`, `yarn.lock`, `poetry.lock`
