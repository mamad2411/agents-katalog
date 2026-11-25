---
name: init-project
description: "Initialize a new project from scratch. Read spec from CONTEXT.md or ask interactively, scaffold directories, set up .gitignore and basic configs, create CONTEXT.md, commit. Use when starting a new project."
---

<!-- Delete when: native Claude Code project scaffolder with template library is available -->

# Init Project Skill

Initialize a new project. Works with any input: point to a CONTEXT.md file, read an existing project spec, or ask interactively if starting from scratch.

## When to Use
- User runs `/init-project` to start a new project
- Starting from a blank directory or existing repo

---

## Flow

### 1. Read or Build Spec

Check what exists:

**1A — CONTEXT.md already in repo root**: Read it. If it's complete (has Project, Stack, Key Decisions sections), skip to step 3.

Read `.attacca/focus.md` too if it exists — it tells you what's already underway, which changes what's worth scaffolding.

**1B — No CONTEXT.md**: Ask interactively:
```
1. What is the project name and one-sentence purpose?
2. What's the tech stack? (e.g., "Node.js + React + PostgreSQL")
3. Who are the main users or personas?
4. What are the 3–5 core features for v1?
5. Any hard constraints? (budget, compliance, deployment target)
```

Write answers interactively until you have enough to scaffold. Do NOT overthink — you can refine this later.

### 2. Scaffold Directory Structure

Create basic project structure:
```
project-root/
├── .gitignore
├── .attacca/
│   └── focus.md                 [committed session state]
├── .claude/
│   └── skills/                  [or wherever installed]
├── docs/
│   └── adr/                     [create lazily]
├── src/                         [language-specific]
├── tests/                       [language-specific]
└── CONTEXT.md
```

**.gitignore**: create one appropriate to the stack (always ignore `.env*`, dependency dirs, build output). For Attacca artifacts, ignore `.attacca/audits/` and `.attacca/sbom/` — **never bare `.attacca/`**, which would swallow the committed `focus.md`. Teams that want committed audit trails drop those two lines.

### 3. Create or Complete CONTEXT.md + .attacca/focus.md

Two files, split by rate of change (see `docs/CONTEXT-SCHEMA.md`). If they don't exist, create them:

`CONTEXT.md` at project root — stable, append-only, ~100 lines:

```markdown
# [Project Name]

[One paragraph: what it is, who uses it, why it matters]

## Stack

- Language: [primary language]
- Framework(s): [backend/frontend]
- Database: [if applicable]
- Deployment: [where it runs]

## Key Decisions

[Non-obvious choices, each with the alternative it beat. Append as decisions are made; never delete.]
```

`.attacca/focus.md` — disposable, rewritten each session, ~30 lines:

```markdown
# Focus

## Current Focus

[What you're building right now.]

## Next Steps

[Unblocking or upcoming work.]

## Blockers

[If any. "None" if clear.]
```

If either exists but is incomplete, fill in missing sections. If `CONTEXT.md` exists with `Current Focus` / `Next Steps` / `Blockers` sections (pre-4.3 layout), move them into `.attacca/focus.md` and drop them from `CONTEXT.md`.

### 4. First Commit

```bash
git add -A
git commit -m "feat: initialize project"
```

---

## Notes

- Keep CONTEXT.md lightweight — it's a map, not a spec. Session churn belongs in `.attacca/focus.md`.
- Domain glossary and ADRs live here; use them in all code and commit messages.
- Refine incrementally as you learn more about the project.
