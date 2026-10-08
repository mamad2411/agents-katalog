# SKILL: Code Refactoring

> Architecture · Modularisation · Best Practices

## Purpose

Analyse and improve the structural quality of the codebase without changing observable
behaviour. Apply only when explicitly invoked or when a file exceeds the thresholds below.

---

## Thresholds that trigger this skill

- A component or module file exceeds **250 lines**
- A function has more than **3 levels of nesting** or more than **4 parameters**
- A single file carries more than **2 unrelated responsibilities**
- A feature folder lacks a consistent barrel export (`index.ts` / `__init__.py`)

---

## Steps

### 1 — Map the affected area

- List all files in the target folder
- State the single responsibility of each file in one sentence
- Flag any file carrying more than one responsibility

### 2 — Detect structural smells

**Client side:**
- God components mixing UI + API calls + business logic
- Deep prop drilling (>2 levels) that should be in a state store slice
- Inline magic strings / numbers that belong in a constants file
- Missing barrel exports (`index.ts`)

**Server side:**
- Routers containing business logic that belongs in a service layer
- Database calls outside the `db/` package (called directly from routers or services)
- Duplicated logic across files (>3 near-identical blocks)
- Missing module exports (`__init__.py` or equivalent)

### 3 — Propose the refactor plan

Describe what to extract and where it should live.

#### Recommended client layout

```md
src/
  pages/
    app/
      index.[ext]        ← search
      saved.[ext]        ← saved results
      deleted.[ext]      ← deleted/trash
      catalogue.[ext]    ← catalogue
  layouts/
    AppLayout.[ext]      ← authenticated shell with nav
    PublicLayout.[ext]   ← login, restricted, landing
  components/
    ui/                  ← component library primitives (never modify generated files)
    app/                 ← app-specific components
  [interactive]/
    SearchForm/          ← search island/component
    SearchResult/        ← result display component
    SavedList/           ← saved results browse component
    DeletedList/         ← deleted results browse component
    CatalogueGrid/       ← catalogue browse component
  store/
    auth.store.[ext]
    search.store.[ext]
  lib/
    api.[ext]            ← typed fetch wrapper with JWT forwarding
    auth-client.[ext]    ← auth provider client singleton
    constants.[ext]      ← domain constants, filter values
    types.[ext]          ← TypeScript interfaces mirroring API contract
```

#### Recommended server layout

```md
app/
  routers/
    search.[ext]         ← POST /search (thin)
    saved.[ext]          ← POST + GET /saved
    deleted.[ext]        ← POST /deleted/bin · GET + DELETE /deleted
    catalogue.[ext]      ← GET /catalogue
  services/
    rag.[ext]            ← chunk reassembly
    llm_client.[ext]     ← LLM call wrapper
    llm_parser.[ext]     ← response parsing + validation
    embeddings.[ext]     ← embedding model wrapper
    search_engine.[ext]  ← RAG pipeline orchestrator
    prompt_builder.[ext] ← system prompt + user message builders
  db/
    queries.[ext]        ← barrel re-export of all query functions
    search_queries.[ext] ← knowledge base vector search (read-only)
    saved_queries.[ext]  ← saved results CRUD
    deleted_queries.[ext]← trash CRUD + hard-delete
  models/
    schemas.[ext]        ← ALL request/response models
  core/
    config.[ext]         ← settings from environment
    auth.[ext]           ← admin assertion dependency/middleware
    db.[ext]             ← database client singleton
```

### 4 — Execute (only after plan is approved)

- Extract one piece at a time in atomic steps
- Keep original files as thin re-exports during transition
- Update all import paths
- Confirm zero type-check errors after each extraction

### 5 — Validate

**Client:** `[type-check command]` — zero errors
**Server:** `[type-check command]` — zero errors
Both: run existing tests; visually verify affected screens render correctly

---

## Project-specific conventions

### Client

- No raw database calls in any client file — use the `api.[ext]` fetch wrapper exclusively
- State stores are session-only; they do not persist between page loads
- Search result state is transient until the user explicitly saves it via `POST /saved`

### Server

- `app/db/` is the **only** location that calls the database client directly
- `app/services/` files orchestrate logic but do not call the database client directly
- `app/routers/` files are thin: validate → call service → return response
- The knowledge base table is read-only — never pass it to a write query function
