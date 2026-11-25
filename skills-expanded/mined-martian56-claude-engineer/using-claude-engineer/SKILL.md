---
name: using-claude-engineer
description: Use at the start of, and throughout, any work that builds or finishes a full software project with claude-engineer. Establishes the project lifecycle, the iron laws, and which skill to invoke at each stage. Auto-injected at session start.
---

# Using Claude-Engineer

**Announce at start:** "I'm using claude-engineer to drive this project's lifecycle."

Claude-Engineer is a **lifecycle orchestrator** for building full **greenfield** web apps end-to-end.
It is opinionated: **React or Next.js + Tailwind + a DESIGN.md-driven custom design system** on the
front, **FastAPI + SQLAlchemy 2.0 + Alembic + Pydantic v2** on the back, a **polyglot monorepo**,
**Docker for stateful services only**, and **hard quality gates**.

It does NOT reimplement general engineering discipline - it **calls into `superpowers`** for that and
adds the whole-project glue superpowers lacks (intake → phased plan → autonomous build → finish, plus
durable cross-session memory).

## Iron Laws (violating the letter is violating the spirit)
1. **Plan-gated.** No build work before the user signs off on the phased plan. Heavy alignment up front, then autonomous.
2. **Greenfield only.** Claude-Engineer scaffolds NEW projects on its opinionated stack. It does not onboard existing codebases.
3. **Customer experience first.** Build in this order: DESIGN.md → frontend shells/components → backend APIs → integration.
4. **Hard quality gates for "done."** ALL of: tests + coverage; Playwright E2E with ZERO console errors; WCAG AA; strict types + lint clean. Enforced at the commit gate and at finish.
5. **Services in Docker, app runs native.** Postgres/Redis/MinIO/Mailpit in Docker; frontend & backend run natively in separate shells.
6. **Trust the ledger.** `.claude-engineer/progress.md` + `memory.md` + `git log` over your own recollection (survives compaction).

## The lifecycle and which skill to invoke

| Stage | claude-engineer skill | calls into superpowers |
|---|---|---|
| 0. Conventions/setup | `claude-engineer:project-conventions` | - |
| 1. Intake (brief) | `claude-engineer:intake-project` | `brainstorming` |
| 2. Plan (sign-off gate) | `claude-engineer:plan-project` | `writing-plans` |
| 3. Memory init | `claude-engineer:project-memory` | - |
| 4. Build (autonomous) | `claude-engineer:execute-build` | `using-git-worktrees`, `subagent-driven-development` (each task: `test-driven-development`), `dispatching-parallel-agents`, `executing-plans` (fallback), `systematic-debugging` |
| - design system | `claude-engineer:design-system` | - |
| - frontend | `claude-engineer:frontend-development` | - |
| - backend | `claude-engineer:backend-development` | - |
| - monorepo/tooling | `claude-engineer:monorepo-and-tooling` | - |
| - local services | `claude-engineer:docker-dev-environment` | - |
| 5. Verify/review | `claude-engineer:testing-and-quality` | `requesting-code-review`, `receiving-code-review`, `verification-before-completion` |
| 6. CI + finish | `claude-engineer:ci-cd-pipeline`, then `finishing-a-development-branch` | `finishing-a-development-branch` |

**Guided path:** the `/claude-engineer:engineer` command walks stages 0→6 in order.
**Per-stage path:** invoke any skill above directly (e.g. `/claude-engineer:plan-project`).

## Rules of engagement
- If a stage's skill exists, USE it; don't freelance the stage.
- Reference a skill's `references/` docs on demand (read by path) - do not paste them wholesale.
- Update `.claude-engineer/progress.md` after each task and `.claude-engineer/memory.md` on key decisions.
- When unsure whether a claude-engineer skill applies: it does. Invoke it.
