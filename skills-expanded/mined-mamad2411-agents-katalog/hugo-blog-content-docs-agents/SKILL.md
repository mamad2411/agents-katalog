# AGENTS.md

> Master index for the Harness engineering workflow. Every agent reads this file first before taking any action.

---

## 1. Project Overview

**OfficeKit** is a lightweight, no-login web-based office utility platform built for teams of 20+ users. It provides a collection of browser-accessible mini-tools for everyday office tasks — starting with PDF manipulation (merge, split, compress) and expanding iteratively to image processing (compress/convert) and QR/barcode generation.

The stack is **Next.js 15 + TypeScript + Tailwind CSS**, deployed on a self-hosted VPS via Docker. File processing runs entirely server-side using **pdf-lib** (PDF operations) and **sharp** (image operations) — no third-party cloud APIs, no user authentication required.

The product follows an **iterative release strategy**: MVP ships with the PDF module, with image tools and QR/barcode generation added in subsequent phases. The UI is English-first.

**Current phase: Phase 0 — Bootstrapping (0 → 1)**

---

## 2. Document Map & Responsibilities

```
                  ┌─────────────────┐
                  │   AGENTS.md     │  ← You are here. Read first, always.
                  └────────┬────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   STRATEGY LAYER    EXECUTION LAYER    FEEDBACK LAYER
        │                  │                  │
   ARCHITECTURE.md     TODO.md            STATUS.md
   PLAN.md             TASKS.md           LOGS.md
```

| Document | Layer | Purpose | Read when… | Update when… | Owner |
|---|---|---|---|---|---|
| **AGENTS.md** | Index | Master entry point and doc map | Always — read first | The doc model itself changes | Lead agent / human reviewer |
| **ARCHITECTURE.md** | Strategy | System design, module boundaries, data flow, tech stack decisions, file-processing pipeline | Starting any task that touches API routes, file handling, or adding a new tool module | A new module is added, a library decision changes, or the folder structure is revised | Design agent / human architect |
| **PLAN.md** | Strategy | Milestones, phases, module rollout sequence, success criteria per phase | Planning a new sprint or phase, or when scope changes | A phase is completed or a milestone shifts | Lead agent / PM |
| **TODO.md** | Execution | Backlog of all planned work — features, refactors, fixes not yet started | Picking up new work; checking what's next | New work is identified, scoped, or deprioritized | Any agent |
| **TASKS.md** | Execution | In-flight tasks with acceptance criteria, assignee, and status | Starting a task; checking what is actively being worked | Promoting an item from TODO, changing task status (in-progress → blocked → done) | Executing agent |
| **STATUS.md** | Feedback | Current snapshot: what's done, what's blocked, what's next | A human or new agent joins and needs to orient quickly | End of every work session; after any task state change | Executing agent |
| **LOGS.md** | Feedback | Append-only chronological record of decisions, actions, and outcomes | Investigating why a past decision was made | Any non-trivial action completes — append only, never edit history | Any agent |
| **DEPLOYER.md** | Execution | Git commit, feature branch management, GitHub PR creation, CI triggering | Before pushing the tasks that have passed the Evaluator's review to GitHub | Update STATUS.md and LOGS.md after PR merge | Deployer agent |
| **DESIGN.md** | Strategy | Website Visual Design Guidelines - Color System, Fonts, Spacing, Component Styles, Animations, Prohibitions | 执Before performing any tasks related to UI components, pages, or styles | When the design style is adjusted, new component specifications are added, or prohibited items are updated | Human / lead agent |

---

## 3. Agent Workflow (Read → Act → Write)

Follow this sequence for every unit of work without exception.

1. **Orient** — Read `AGENTS.md` (this file), then `STATUS.md` to get the current project snapshot. Do not skip this even if you think you know the state.

2. **Plan** — Consult `PLAN.md` for the active phase and milestone. If the task touches any API route, the file-processing pipeline, or the module registry in `src/modules/`, read the relevant section of `ARCHITECTURE.md` before writing any code.

3. **Pick** — Pull the next prioritized item from `TODO.md`. Promote it into `TASKS.md` with:
   - Clear acceptance criteria (what "done" looks like)
   - Estimated scope (S / M / L)
   - Any blockers or dependencies noted upfront

4. **Execute** — Do the work. Follow the module boundary conventions in `ARCHITECTURE.md`. Do not silently deviate from the established folder structure or API contract — if a deviation is needed, update `ARCHITECTURE.md` first and log the decision in `LOGS.md`.For any UI-related task, read `DESIGN.md` before writing any component or style code.

5. **Record** — After completing or blocking on a task:
   - Mark the task done/blocked in `TASKS.md`
   - Append a timestamped entry to `LOGS.md` (what was done, key decisions made, why)
   - Overwrite `STATUS.md` with the new snapshot (prior state must already be in `LOGS.md`)

6. **Hand off** — Leave `STATUS.md` in a state where the next agent or a team member can orient in under 60 seconds. Include: last completed task, current blocker (if any), and the single next recommended action.

7. **Deploy** — After the Evaluator issues a PASS, the Deployer agent takes over: create a feature branch → commit → push → open a PR → wait for CI to turn green → squash merge → synchronize the documentation

---

## 4. Update Rules

```
ARCHITECTURE.md  — updated by: design agent / human architect
                   when: a new tool module is scaffolded, a library is added/swapped,
                         or the file-processing pipeline changes
                   cadence: low frequency; deliberate, reviewed changes only

PLAN.md          — updated by: lead agent / human PM
                   when: a phase boundary is crossed or milestone scope shifts
                   cadence: per phase; not during active execution sprints

TODO.md          — updated by: any agent
                   when: new work is identified, scoped, or removed from scope
                   cadence: continuous; the backlog is always the source of next work

TASKS.md         — updated by: the executing agent
                   when: a task is promoted from TODO, changes state, or is completed/blocked
                   cadence: continuous during active development

STATUS.md        — updated by: the executing agent
                   when: end of every work session or after any task state change
                   cadence: at minimum once per working day during active development

LOGS.md          — updated by: any agent
                   when: any non-trivial action completes (code merged, decision made,
                         blocker hit, architecture revised)
                   cadence: append-only — entries are never edited or deleted

AGENTS.md        — updated by: lead agent / human reviewer
                   when: the document model itself changes (new doc added, workflow revised)
                   cadence: rare; treat as a breaking change

DESIGN.md        — updated by: lead agent / human designer
                   when: design style or component spec changes
                   cadence: rare; treat as a breaking change
                   note: must be read before any UI-related task
```

**Protective rules:**

1. **LOGS.md is append-only.** Never edit or delete past entries. `STATUS.md` is a mutable snapshot — overwrite freely, but the superseded state must already be captured in `LOGS.md`.

2. **One source of truth per fact.** If two documents conflict, the layer hierarchy resolves it:
   `ARCHITECTURE.md / PLAN.md / DESIGN.md` > `TASKS.md / TODO.md` > `STATUS.md / LOGS.md`
---

## 5. Commands & Tooling

```bash
# ── Setup ────────────────────────────────────────────────
npm install                        # Install all dependencies
cp .env.example .env.local         # Configure environment variables

# ── Development ──────────────────────────────────────────
npm run dev                        # Start Next.js dev server (http://localhost:3000)

# ── Type checking & Lint ─────────────────────────────────
npm run type-check                 # tsc --noEmit
npm run lint                       # ESLint via next lint
npm run lint:fix                   # Auto-fix lint issues

# ── Testing ──────────────────────────────────────────────
npm run test                       # Run unit tests (Vitest / Jest)
npm run test:watch                 # Watch mode

# ── Build & Production ───────────────────────────────────
npm run build                      # Next.js production build
npm run start                      # Start production server

# ── Docker (VPS deployment) ──────────────────────────────
docker build -t officekit .        # Build Docker image
docker compose up -d               # Start all services (app + optional reverse proxy)
docker compose down                # Stop services
docker compose logs -f app         # Tail application logs
```

> ⚠️ TBD — Specific environment variables (e.g. `MAX_FILE_SIZE`, `UPLOAD_DIR`) and the Dockerfile have not yet been defined. Add them to `ARCHITECTURE.md` once decided during Phase 0 bootstrapping.

---

