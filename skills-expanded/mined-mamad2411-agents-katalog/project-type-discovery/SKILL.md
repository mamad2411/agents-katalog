---
name: project-type-discovery
description: Interactive project type identification and profile generation. Defines type, stack, design approach, agent selection, and Flyee integration. Used by new-project, legacy-project, discovery, and enhance workflows.
---

# Project Type Discovery

> Identify project type and generate a **Project Profile** that controls which agents, skills, phases, and templates are activated.

---

## 🚦 When to Use

| Workflow | Trigger |
|----------|---------|
| `/new-project` | Gate 0 — runs BEFORE any phase |
| `/legacy-project` | Initial analysis — identify existing project type |
| `/discovery` | Project identification |
| `/new-task` | Detect feature context (frontend, backend, fullstack) |

> [!CAUTION]
> This gate runs BEFORE any phase, including Brainstorm.
> **Exception:** `--resume` (Project Profile already saved in PROJECT-PROGRESS.md).

---

## 📋 Discovery Flow (4 Questions)

### Question 1: Project Type (MANDATORY)

```markdown
## 🚦 What type of project do you want to create?

| # | Type | Example | Phases Activated |
|---|------|---------|-----------------|
| **1** | 🌐 Institutional Site / Landing Page | Portfolio, product LP | PRD → Design System → Content → Stitch → Implementation |
| **2** | 🖥️ Web App (SaaS / Dashboard) | Admin panel, SaaS, platform | PRD → TDD → Design System → Breakdown → TDD Method → Implementation |
| **3** | 🔌 API / Backend | REST API, microservices, BFF | PRD → TDD → Breakdown → TDD Method → Implementation |
| **4** | 📱 Mobile App | React Native, Flutter, native | PRD → TDD → Design System (mobile) → Breakdown → Implementation |
| **5** | 🧩 Fullstack (Web App + API) | Complete app with frontend and backend | PRD → TDD → Design System → Breakdown → TDD Method → Implementation |
| **6** | 📦 Package / Library | npm package, SDK, utility | PRD → TDD → TDD Method → Implementation |

Which number?
```

**WAIT** for user response.

---

### Question 2: Stack (Contextual to Type)

After the type, ask follow-up questions **specific to the chosen type:**

#### Type 1 (Institutional Site / LP)

| Option | Stack | When to use |
|--------|-------|-------------|
| **A** | Next.js (App Router) + CSS Modules | Multi-page sites, SEO, dynamic routes |
| **B** | Next.js (App Router) + Tailwind | Fast sites with visual prototyping |
| **C** | HTML/CSS/JS vanilla | Simple sites, no framework |
| **D** | Other (specify) | Already defined stack |

#### Type 2 (Web App / SaaS)

| Option | Stack | When to use |
|--------|-------|-------------|
| **A** | Next.js + shadcn/ui + Tailwind | Modern apps with ready components |
| **B** | Next.js + CSS Modules | Apps with custom design system |
| **C** | Vite + React + Tailwind | SPAs without SSR |
| **D** | Other (specify) | Already defined stack |

**Additional questions:** Auth provider? Database? Deploy platform?

#### Type 3 (API / Backend)

| Option | Stack | When to use |
|--------|-------|-------------|
| **A** | Node.js + Express/Fastify | Simple REST APIs |
| **B** | NestJS + Prisma | Enterprise APIs with DI |
| **C** | Next.js API Routes | API coupled to frontend |
| **D** | Python (FastAPI / Django) | Python APIs |
| **E** | Other (specify) | Already defined stack |

**Additional questions:** Protocol (REST/GraphQL/tRPC/gRPC)? Database?

#### Type 4 (Mobile)

| Option | Stack | When to use |
|--------|-------|-------------|
| **A** | React Native + Expo | Fast cross-platform |
| **B** | Flutter | Cross-platform with native UI |
| **C** | SwiftUI (native iOS) | iOS only |
| **D** | Kotlin (native Android) | Android only |

#### Type 5 (Fullstack)

Combination of frontend + backend. Ask both:
- **Frontend:** same options as Type 2
- **Backend:** same options as Type 3, or integrated API Routes?

#### Type 6 (Package / Library)

| Option | Stack | When to use |
|--------|-------|-------------|
| **A** | TypeScript + tsup/unbuild | Modern npm packages |
| **B** | TypeScript + Rollup/Vite lib | Libs with tree-shaking |
| **C** | Python + setuptools/poetry | PyPI packages |

**Additional questions:** Publish to npm/PyPI? Internal use? Monorepo?

**WAIT** for user response.

---

### Question 3: Design (Only for types with UI: 1, 2, 4, 5)

```markdown
### Design Approach:

| Option | Description |
|--------|-------------|
| **A** | I have visual references (Figma, screenshots, inspiration sites) |
| **B** | I want agent recommendations based on the segment |
| **C** | I'll define manually (I have colors, fonts, etc.) |
| **D** | Combination: references + adjustments with recommendations |

Which option?
```

> [!NOTE]
> The answer to this question **replaces** Phase 2.45 (Visual Reference Collection).
> If the user answers here, Phase 2.45 uses this choice directly without asking again.

---

### Question 4: Flyee Integration (MANDATORY after Project Profile)

> Run AFTER the Project Profile is saved, BEFORE starting Phase 0/1.

**Check** `flyee.json`:
- If `opted_out: true` → Skip silently
- If `enabled: true` → Skip silently (already configured)
- If `enabled: false` AND `opted_out: false` → Present question:

```markdown
## 🔗 Flyee Platform Integration

Flyee can track documents, decisions, and progress for this project.

| Option | Description |
|--------|-------------|
| **A) Configure now** | Connect to Flyee (list/create project + register docs) |
| **B) Later** | Skip (configure later with `python .agent/flyee-bridge/bridge.py --setup`) |
| **C) No thanks** | Disable permanently |
```

- **If A:** Execute Flyee Bridge Setup Flow (see below)
- **If B:** Continue without bridge (`enabled: false`)
- **If C:** Set `opted_out: true` in `config.json`

---

## 🔗 Flyee Bridge Setup Flow

> Referenced by: Gate 0 (Question 4) and `--resume` (Step 4).

**Step 1: Authentication**
- Request API URL (default: `https://flyee-api.flyeelab.com`)
- Request API Key (obtained in Settings → API Keys)

**Step 2: Project Selection or Creation**
- List existing projects via `GET /flyee/projects/`
- Present options (existing projects + "Create new")
- If new: suggest name from directory or PROJECT-PROGRESS.md

**Step 3: Register Existing Documentation**
- Scan `docs/` for: `PRD-*.md`, `TDD-*.md`, `BREAKDOWN-*.md`, `PROJECT-PROGRESS.md`
- Register each via `POST /flyee/projects/{id}/documents`

**Step 4: Save Config**
- Update `config.json` with `api_url`, `project_id`, `api_key`, `enabled: true`

> [!TIP]
> **CLI commands available:**
> - `python .agent/flyee-bridge/bridge.py --setup` → full interactive setup
> - `python .agent/flyee-bridge/bridge.py --list-projects` → list projects
> - `python .agent/flyee-bridge/bridge.py --register-docs` → register existing docs

---

## 📋 Project Profile Output

After all questions, generate and save to `PROJECT-PROGRESS.md`:

```markdown
## 🚦 Project Profile

| Field | Value |
|-------|-------|
| Type | {chosen type} |
| Stack | {defined stack} |
| Primary Agent | {selected agent} |
| Design Approach | {A/B/C/D or N/A} |
| Has UI? | Yes / No |
| Has Backend? | Yes / No |
| Phases Activated | {list} |
| Phases Skipped | {list} |
```

### Type → Configuration Mapping

| Type | Primary Agent | Skipped Phases | Extra Skills |
|------|--------------|----------------|-------------|
| Institutional Site | `frontend-specialist` | — | `content-strategy`, `seo-fundamentals` |
| Web App | `frontend-specialist` + `backend-specialist` | Content Strategy (optional) | `shadcn-ui` (if applicable) |
| API / Backend | `backend-specialist` | Design System, Content, Stitch, Page Specs | `api-patterns`, `database-design` |
| Mobile | `mobile-developer` | Stitch, Content | `mobile-design` |
| Fullstack | `orchestrator` | — | Combines frontend + backend |
| Package / Library | `backend-specialist` | Design System, Content, Stitch, Page Specs | `testing-patterns` |

---

## 🔴 Exit Gate

```markdown
[ ] Project type defined
[ ] Stack confirmed by user
[ ] Design approach defined (if has UI)
[ ] Project Profile saved in PROJECT-PROGRESS.md
[ ] Flyee integration resolved (configured, skipped, or opted out)
```

> [!CAUTION]
> **BLOCKER:** Do not start any phase (not even Brainstorm) without the Project Profile defined.
