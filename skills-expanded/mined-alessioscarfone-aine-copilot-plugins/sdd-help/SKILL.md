---
name: sdd-help
description: 'Learn about the SDD process — get a quick overview, deep dives into each artifact type (PRD, architecture, UX, changes, specs), team roles, and available skill commands. Use when onboarding to SDD, looking up how a skill works, or asking about roles and process stages. Do not use for creating or editing SDD documents or implementing changes.'
---

Answer questions about the Specification-Driven Development (SDD) approach, its artifacts, and how to use the `sdd-team` skills effectively.

**This is a knowledge and reference skill — it does not create or modify any files.** Use it when you want to understand the workflow, explore what an artifact should contain, or figure out what to do next.

**Input**: The argument after `/sdd-help` is your question or topic, for example:
- `/sdd-help` — show the overview and navigation menu
- `/sdd-help artifacts` — explain every artifact type
- `/sdd-help process` — walk through the full SDD lifecycle
- `/sdd-help prd` — deep dive on a specific artifact
- `/sdd-help what's next` — suggest the next step based on what exists in `{ARTIFACT_MAIN_FOLDER}/`

---

## Entry point

1. **Read what already exists** — list `{ARTIFACT_MAIN_FOLDER}/` and `{ARTIFACT_MAIN_FOLDER}/{CHANGE_SUBFOLDER}/` (if they exist) to understand the project's current SDD state.

2. **Interpret the user's input** and load the relevant detail file only when needed:
   - No input or "overview" → display the **SDD Overview** and the **Navigation Menu** below
   - "process", phase name, or stage question → load <a>references/process.md</a>
   - "artifacts", artifact name, or "prd / ux / arch / proposal / design / tasks / spec" → load <a>references/artifacts.md</a>
   - "skills", "commands", or a skill name → load <a>references/skills-inventary.md</a>
   - "roles", "agents", or an agent name → load <a>references/roles.md</a>
   - "what's next" or "where am I" → assess current state using the **[6] What's Next** section below
   - Free-form question → answer from the overview or load the most relevant detail file

3. **Display the Navigation Menu** after any response longer than a quick answer, so the user can continue exploring:

```
📖 sdd-help — What would you like to explore?

[1] SDD Overview        — What SDD is and why it works         (this file)
[2] Full Process        — All 7 stages from idea to archive    → references/process.md
[3] Artifacts           — Every document type explained        → references/artifacts.md
[4] Skills & Commands   — When and how to use each command     → references/skills-inventary.md
[5] Team Roles          — Which agent to use for each task     → references/roles.md
[6] What's Next         — Assess project state and next step   (this file)
```

---

## [1] SDD Overview

**Specification-Driven Development (SDD)** is a workflow where every change starts with a written specification before any code is written.

### Core idea

```
Think → Write → Review → Implement → Verify → Archive
```

Instead of jumping straight to code, SDD captures decisions in structured documents. Those documents serve as the single source of truth for the entire team (human and AI alike).

### Why it works

| Traditional approach | SDD approach |
|---|---|
| Decisions live in chat, memory, or nowhere | Decisions live in versioned documents |
| AI agents guess what you want | Agents read specs before acting |
| Changes are hard to review | Every change has a traceable paper trail |
| Context is lost between sessions | `{ARTIFACT_MAIN_FOLDER}/` persists context across sessions |

### Key principle: specs before code

Every change travels through three layers:
1. **Shared documents** (`prd.md`, `ux.md`, `architecture.md`) — shared context for the whole project
2. **Change artifacts** (`proposal.md`, `design.md`, `tasks.md`) — scoped context for one change
3. **Capability specs** (`specs/<name>/spec.md`) — testable requirements for new capabilities

Agents read these files at the start of every session, so context is never lost.

---

## [6] What's Next

When the user asks "what's next", "where am I", or similar:

1. **Inspect the current state** of `{ARTIFACT_MAIN_FOLDER}/`:
   - Does `prd.md` exist?
   - Does `ux.md` exist?
   - Does `architecture.md` exist?
   - Are there active changes in `{ARTIFACT_MAIN_FOLDER}/{CHANGE_SUBFOLDER}/`? (excluding `archive/`)
   - Do any active changes have incomplete tasks in `tasks.md`?

2. **Recommend the next step** based on what you find:

| State | Recommendation |
|---|---|
| No `{ARTIFACT_MAIN_FOLDER}/` at all | Start with `/sdd-prd` to define your product |
| `prd.md` missing | Run `/sdd-prd` — required before proposing any change |
| `prd.md` exists, no `ux.md` or `architecture.md` | Run `/sdd-ux` then `/sdd-arch` to complete project setup |
| Setup complete, no active changes | Run `/sdd-propose <name>` to start your first change |
| Active change exists with no `tasks.md` | Run `/sdd-propose <name>` to generate missing artifacts |
| Active change with incomplete tasks | Run `/sdd-implement <name>` to continue implementation |
| All tasks complete, not verified | Run `/sdd-verify <name>` to confirm spec compliance |
| All tasks complete and verified | Run `/sdd-archive <name>` to close out the change |

3. **Show the user the state you found** so they can correct any misreading before acting.

---

## Guardrails

{SKILL_ASSETS_NOTICE}
- **Read-only skill** — never create, modify, or delete any file. If the user wants to create or update a document, direct them to the appropriate skill command.
- **Reference real paths** — when mentioning files, always use the actual path format (`{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/prd.md`, `{ARTIFACT_MAIN_FOLDER}/{CHANGE_SUBFOLDER}/<name>/proposal.md`).
- **Assess current state first** — always inspect `{ARTIFACT_MAIN_FOLDER}/` before answering "what's next" or making recommendations.
- **Stay factual** — describe the artifacts and process as they are defined in the skill files, not as general best practices.
- **Suggest, Do not act** — offer the next command to run; let the user decide when to switch skills.
