---
name: quickstart
description: "Welcome guide for new users. Assesses your setup, explains what Attacca does, points to first action. Run this first if you're new."
---

<!-- Delete when: native Claude Code interactive onboarding workflow is available -->

# Quickstart

Welcome to Attacca.

## What is This?

Attacca is a system for building software with AI agents. You describe what you want. Agents plan, code, review, audit, and ship.

## Your First Step

**Starting a new project?**
→ Run `/init-project`

**Working on an existing project?**
→ Run `/retrofit` to set up documentation and configuration

**Want to understand the system first?**
→ Read CONTEXT.md in the repo root (or this project's `.dev/` if no CONTEXT.md exists yet)

---

## What Happens Next

When you start a project:

1. You describe what you want (a PRD, an issue, a sketch)
2. The system scaffolds:
   - Project structure
   - CONTEXT.md with overview and conventions
   - .gitignore and basic configs
3. You commit and start building
4. Agents assist with planning, coding, review, and security

---

## Key Skills

- `/init-project` — scaffold a new project from scratch
- `/retrofit` — set up documentation on an existing project
- `/mvp` — ship a minimum viable product fast
- `/quality-gate` — lint, type-check, test, security scan before pushing
- `/code-review` — review code changes for quality and correctness
- `/diagnose` — debug hard problems systematically
- `/improve-codebase-architecture` — refactor and deepen modules

Full list: explore the skills/ directories in plugins/attacca-*/

---

## Get Started

```bash
# New project
/init-project

# Existing project
/retrofit

# Questions?
# Read CONTEXT.md for project-specific info
# Read docs/adr/ for architectural decisions
```
