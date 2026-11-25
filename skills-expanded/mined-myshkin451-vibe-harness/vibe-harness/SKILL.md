---
name: vibe-harness
description: Turn a human project plan into a lightweight agent-ready repository harness for sustainable AI coding. Use when bootstrapping a new project, retrofitting an existing repo for AI coding agents, creating or refreshing AGENTS.md/docs/index.md/progress.md, diagnosing context loss across sessions, designing verification loops, or coordinating multiple agents without heavyweight governance.
---

# Vibe Harness

## Overview

Vibe Harness translates a project plan into the smallest useful repository harness: a map, a state board, verification loops, and collaboration rules that help coding agents keep working across sessions.

The point is a runway, not a cage. Preserve the model's room to reason and implement; only encode the context, boundaries, evidence paths, and handoff habits that prevent drift.

## When To Use

Use this skill when the user wants to:

- initialize a new project from a plan, PRD, design note, or product idea
- make a repo agent-ready for Codex, Claude Code, Cursor, Copilot, Gemini, or similar coding agents
- create or refresh `AGENTS.md`, `docs/index.md`, `progress.md`, execution plans, or decision records
- fix repeated agent failures caused by stale context, weak verification, unclear ownership, or long-session handoff loss
- coordinate multiple agents or sessions without building a heavy governance system
- turn AI coding into a maintainable workflow, from vibe-coded prototypes to structured product work

Do not use this for a tiny one-off code edit in a repo that already has clear instructions and validation.

## Core Rules

1. Start from the user's intent, not from a template.
2. Inspect the current repo before claiming paths, commands, architecture, tests, or CI.
3. Keep `AGENTS.md` short: a table of contents and working map, not a manual.
4. Add only docs that have a job. If no one will read or update it, do not create it.
5. Prefer mechanical verification over prose rules once a pattern repeats.
6. Write unknowns explicitly instead of inventing tests, owners, or deployment facts.
7. Define human judgment points. The harness should route taste, priority, secrets, destructive actions, and product calls back to the user.

## Workflow

### 1. Build The Intent Brief

Read the project plan or ask the user for the missing essentials if they are unavailable:

- product goal and target users
- current stage: idea, prototype, first usable loop, production, or maintenance
- expected agent workflow: solo agent, many sessions, parallel agents, or async PR agents
- stack preferences and hard constraints
- definition of done and validation evidence
- known risks, non-goals, and human-only decisions

Capture this as a short working summary before editing files.

### 2. Inspect Repository Reality

If a repo exists, inspect only what is needed:

- top-level tree and package roots
- existing `AGENTS.md`, `README`, docs index, plans, and progress files
- build/test/lint commands from real config files
- CI workflows and deployment/runbook clues
- recent git history if stale docs or moved paths are likely

If the repo is empty, create a minimal harness that can evolve after the first product loop exists.

### 3. Choose The Harness Depth

Default to the lightest pack that solves the current problem:

- **Seed**: `AGENTS.md`, `docs/index.md`, `progress.md`
- **Working**: Seed plus `docs/architecture.md`, `docs/exec-plans/_template.md`, `docs/decisions/_template.md`
- **Mature**: Working plus `docs/harness.md`, drift checks, CI links, operator runbooks, and periodic cleanup plans

Do not create Mature artifacts on day one unless the repo already has enough complexity to justify them.

### 4. Write Or Refresh Artifacts

Use templates from `assets/templates/` as starting points, then adapt to the repo:

- `agents.md`: short agent entry map
- `docs-index.md`: source-of-truth router
- `progress.md`: high-signal state board
- `exec-plan.md`: scoped long-running work plan
- `decision.md`: durable decision record

For artifact selection and content rules, read `references/artifact-guide.md`.

### 5. Establish Verification Loops

Every harness needs at least one honest verification path:

- exact local command, if one exists
- manual browser/API/log evidence, if automated tests do not exist yet
- CI gate, if configured
- "not yet verified" note, if no reliable check exists

Never pretend a test exists. If validation is weak, make the first improvement obvious and small.

When auditing or refreshing an existing harness, run the bundled `scripts/audit.py` if available. It performs static checks for core files, broken Markdown links, stale inline paths, and validation commands that are not supported by repo config. Treat its output as evidence, not as a replacement for real tests.

### 6. Add Multi-Agent Coordination Only As Needed

For multi-session or multi-agent work, define:

- the shared state file
- work slice boundaries
- file ownership or disjoint write areas
- handoff expectations
- how conflicts are detected
- when agents may proceed autonomously
- when agents must ask the user

Avoid building role theater. Add specialist agents only when responsibilities are separable and useful.

### 7. Close With A Usable Result

Finish by reporting:

- artifacts created or changed
- how the user should invoke agents next time
- what validation or harness audit was run
- remaining gaps and the next smallest harness improvement

If the task includes publishing or adoption, read `references/product-launch.md`.
