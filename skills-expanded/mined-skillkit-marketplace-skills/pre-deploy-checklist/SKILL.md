---
name: pre-deploy-checklist
description: >
  Intelligent pre-deployment QA checklist generator. Explores the codebase,
  confirms project understanding with user, spawns parallel domain subagents
  to deeply analyze each layer (frontend, backend, database, security, etc.),
  then produces a complete human-executable checklist in docs/.
  USE WHEN: User says "pre-deploy check", "deploy checklist", "ready to deploy?",
  "generate QA checklist", or any request to verify project readiness before deployment.
allowed-tools: Read, Glob, Bash, Task, Write
category: deployment
---

# Pre-Deploy Checklist

Generates a **thorough, measurable QA checklist** tailored to your actual project — not a generic template.

**Two-phase flow:**
1. Understand the project → confirm with user
2. Deep parallel domain analysis → produce docs/pre-deploy-checklist.md

---

## Phase 1: Project Discovery

**Goal:** Know what the project is before generating any checklist.

### Step 1.1 — Map the project structure

Use `Glob` and `Bash` to explore — **exclude build artifacts**:

```bash
# Exclude these patterns: node_modules/, target/, dist/, build/, .next/, out/,
# __pycache__/, .git/, vendor/, coverage/, .turbo/, .cache/
find . -maxdepth 3 -not \( -path '*/node_modules/*' -o -path '*/target/*' \
  -o -path '*/dist/*' -o -path '*/.git/*' -o -path '*/__pycache__/*' \
  -o -path '*/build/*' -o -path '*/.next/*' \) -type f | head -80
```

Then read in this priority order:
1. `README.md` or `README.rst` → read fully
2. If no README → read: `package.json` / `Cargo.toml` / `pyproject.toml` / `go.mod`
3. Read 2-3 entry point files (e.g., `src/main.rs`, `src/app.tsx`, `server.ts`, `main.py`)
4. Scan for: `docker-compose.yml`, `.env.example`, `Makefile`, CI configs (`.github/workflows/`)

### Step 1.2 — Confirm understanding with user

After reading, **STOP** and present this confirmation block:

```
## Pemahaman Saya tentang Project Ini

**Tipe project:** [Web App / REST API / CLI / Mobile Backend / Library / Monorepo]
**Stack utama:** [e.g., Next.js 14 + TypeScript + PostgreSQL + Prisma]
**Fitur utama:**
- [fitur 1]
- [fitur 2]
- [fitur 3]

**Domain yang akan saya analisis:**
- [ ] Frontend (ada UI)
- [ ] Backend/API (ada server logic)
- [ ] Database (ada schema/migrations)
- [ ] Authentication (ada auth flow)
- [ ] Infrastructure (ada Docker/CI/cloud config)
- [ ] Security (selalu dianalisis)
- [ ] Performance (selalu dianalisis)

**Yang belum jelas:** [sebutkan jika ada, atau "Semua sudah cukup jelas"]

Apakah pemahaman ini sudah benar? Ada yang perlu dikoreksi atau perlu investigasi lebih lanjut?
```

**⚠️ WAIT for user approval before proceeding to Phase 2.**
If user asks to investigate more, do additional reads before re-confirming.

---

## Phase 2: Parallel Domain Analysis

**Only run after user explicitly approves the understanding.**

### Step 2.1 — Spawn parallel subagents

Use `Task` tool with `subagent_type: Explore` for **each relevant domain simultaneously**.
All subagents run in **parallel** (not sequential).

**Load prompts from:** [references/domain-prompts.md](references/domain-prompts.md)

Typical domains for common project types:

| Project Type | Spawn these subagents |
|---|---|
| Full-stack web | frontend, backend, database, security, performance |
| API-only | backend, database, security, performance |
| Frontend-only | frontend, state-management (if applicable), security, performance |
| CLI tool | backend, security, performance |
| Mobile app | frontend (mobile), backend, database, security |

### Step 2.2 — Collect and merge reports

Wait for ALL subagents to return. Each report has:
- What the domain code does
- What it's for (business purpose)
- What MUST be tested before deploy (with reasoning)
- Red flags found during analysis

---

## Phase 3: Generate the Checklist

### Step 3.1 — Create docs/ if needed

```bash
mkdir -p docs/
```

### Step 3.2 — Write docs/pre-deploy-checklist.md

Use the template in [references/checklist-template.md](references/checklist-template.md).

**Checklist quality standards (must meet ALL):**

| Standard | Example of BAD | Example of GOOD |
|---|---|---|
| Measurable | "test login" | "Login with valid email → redirected to /dashboard in <2s" |
| Actionable | "check performance" | "Run 100 concurrent users → p95 response time <500ms" |
| Specific | "test error handling" | "Submit form with missing email field → error message shows below input" |
| Prioritized | all items same weight | 🔴 Critical / 🟡 Important / 🟢 Nice-to-have |
| Project-specific | generic items | Only items relevant to this actual stack |

**Item severity guide:**

- 🔴 **Critical** — If broken, deploy is BLOCKED (auth failure, data corruption, crashes)
- 🟡 **Important** — Affects significant UX/functionality (slow pages, visual bugs on main flows)
- 🟢 **Nice-to-have** — Polish and future improvements (minor edge cases, optimization opportunities)

**For complete checklist categories by domain:** [references/checklist-categories.md](references/checklist-categories.md)

---

## Output

Final file: docs/pre-deploy-checklist.md (inside the user's project, not this skill)

The file should contain:
- Project metadata (name, date, stack, domains analyzed)
- Usage instructions (how to use the checklist)
- Categorized items by domain with 🔴/🟡/🟢 priority
- Sign-off section at the bottom

**Target:** 30-80 checklist items (varies by project complexity).
Too few = not thorough enough. Too many = not actionable.
