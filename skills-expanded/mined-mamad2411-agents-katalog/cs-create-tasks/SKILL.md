---
name: cs-create-tasks
description: >
  Turn a CodeSpring feature's notes + PRDs into a numbered, prioritized Kanban
  task list linked to that feature. Reads the feature, its sub-features, its
  PRDs, and any features that link to it, then writes ordered tasks that are
  safe to build in parallel — each with what/why/what-it-touches/what-not-to-
  touch/dependencies. Use when the user has a feature planned and wants a build
  plan. Triggers, "create tasks", "make a task list", "break this feature into
  tasks", "generate a build plan", "turn my PRD into tasks", "what do I build
  first".
allowed-tools: Bash(codespring:*) Bash(npx @codespring-app/cli:*)
metadata:
  author: codespring
  version: "0.2"
---

# Create a task list for a feature

Turn a feature's plan into a numbered Kanban task list that an agent (or a fleet of sub-agents) can build safely. See the `codespring` skill's `references/task-workflow.md`, `references/prd-management.md`, `references/pitfalls.md`.

This skill READS the CodeSpring plan and WRITES tasks. It does not modify the codebase.

## 0. Connect first
`codespring auth status` + `codespring status` (use the LOCAL project config; print the projectId).

## 1. Pick the feature
```bash
codespring features        # core features are the root features
```
Ask the user which feature to create tasks for.

## 2. Load the FULL context for that feature
Before writing any task, gather everything CodeSpring knows so the tasks are safe:
- The feature's **note** (how it works) and its **Frontend + Backend PRDs** (`codespring prds`, then `codespring prd <id>`).
- Its **sub-features** (`codespring features --parent <featureId>`).
- **Other features that link to it** — read the whole mindmap and the notes/PRDs of features referenced by this one (and that reference it). The Backend PRD's shared-systems + dependency map is the key input.
- If PRDs are missing, stop and tell the user to generate them first (run `cs-create-prd`, or generate in the web app — see `references/codespring-docs.md`). Do not invent tasks without the PRDs.

## 3. Work out the numbering
CodeSpring tasks are numbered like `X.Y.Z` (e.g. `0.1.0`, `0.1.1`). Continue the existing sequence — do not restart at 0:
```bash
codespring tasks --json    # or: codespring tasks --status todo / in_progress / on_hold / done
```
Scan tasks in ALL states (todo, in_progress, on_hold, done) for this feature, find the **highest number already used**, and start the new tasks at the next increment (e.g. existing max `0.1.2` → new tasks `0.1.3`, `0.1.4`, …). Put the number at the start of each task title.

## 4. Break the work into tasks (ordered + parallelizable)
Derive tasks from the PRDs. A task = one deliverable a person/agent can finish and verify (not a whole feature). Rules:
- **Foundations first:** data model / migrations → shared backend/services → API routes → UI that consumes them.
- **Parallel-safe:** group tasks so independent ones can run at the same time by different sub-agents; sequence only true dependencies. Note which tasks can run concurrently.
- **Flag shared systems:** any task touching a shared API route, shared table, credits/payments/jobs/storage/auth from the Backend PRD must say so.

For EACH task write a detailed description containing:
- **What** it builds and **why**.
- **What it may touch** (files/routes/tables).
- **What it must NOT touch** (out of scope; protected shared systems).
- **What already exists to reuse** (from the PRD reuse map) so it isn't rebuilt.
- **Dependencies / break-risk:** what else depends on the code it changes, so it doesn't silently break another feature.

## 5. Create the tasks — always linked to the feature
```bash
codespring task create --title "0.1.3 Add users table + migration" --priority high --feature <featureId> --description "..."
codespring task create --title "0.1.4 POST /api/login (auth + validation)" --priority high --feature <featureId> --description "..."
codespring task create --title "0.1.5 Login form UI + client validation" --priority medium --feature <featureId> --description "..."
```
- Always pass `--feature <featureId>` so the task is linked to the feature.
- Sub-features are also features (they have ids); linking a task to a sub-feature via `--feature <subFeatureId>` may work — try it and confirm it attaches correctly, otherwise link to the parent core feature and name the sub-feature in the title.
- Set priorities (`urgent|high|medium|low`). New tasks land in `todo`.

## 6. Confirm
```bash
codespring tasks --status todo --feature <featureId>
```
Report the numbered list and the recommended build order (and which can run in parallel). Point the user to the Kanban board in CodeSpring (see `references/codespring-docs.md`). Hand off to `cs-build-feature` to actually build them.

## What good looks like
- A numbered, prioritized set of tasks in `todo`, linked to the feature, continuing the existing numbering.
- Foundations sequenced before dependents; independent tasks marked parallel-safe.
- Every task states what to reuse, what not to touch, and what it could break — so a fleet of agents can build without duplicating or breaking shared systems.
