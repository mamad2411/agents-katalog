---
name: deliver
description: Deliver an approved body of work as a fast, safe graph of pull requests, with durable owner threads and an explicit human merge gate for every PR.
disable-model-invocation: true
---

# Deliver

Deliver an approved body of work through a series of pull requests.

Follow these sections in order:

1. **Preparation** — understand the requirements and divide the work into PRs.
2. **Work loop** — orchestrate the threads that own each PR until every PR is ready for HITL loop.
3. **HITL loop** — wait while the PR-owning threads work with the user. When a thread reports back, update the delivery state and decide what happens next.

Finish when every PR is merged.

## 1. Preparation

### Read the contract

Read every file and path provided by the user. Ask about missing or conflicting requirements before continuing.

### Create the delivery plan

Group the requirements into PRs and make their dependencies explicit. Create a unique directory in the operating system's temporary directory and write the plan to `delivery.md`:

| PR | Covers | Blocked by | PR thread | State | PR link |
|---|---|---|---|---|---|

Initialize each PR as `planned`, with its PR thread and PR link `pending`. Keep the file's absolute path in the main task and use it as the single source of truth throughout delivery.

This step is complete when every requirement belongs to a PR in `delivery.md` and every blocked PR names its blockers.

## 2. Work loop

Act as the hub for persistent PR threads. PR threads own their implementation and PR through merge; the orchestrator owns coordination and `delivery.md`.

### Dispatch PR threads

Create one PR thread per planned PR. Run independent work in parallel and coordinate dependencies.

Send each thread a brief with:

- PR ID and title;
- covered requirements or tickets and relevant artifact paths;
- base and working branches;
- dependencies and their current states;
- the ready-for-HITL boundary: the PR exists and every task not requiring the user is complete;
- ownership through HITL and merge.

Record the PR thread in `delivery.md`.

### Route reports

Use hub-and-spoke communication throughout delivery. PR threads report:

- state changes, including ready for HITL and merged;
- decisions or cross-PR help they need;
- changes or HITL outcomes that may affect other PRs.

Every report identifies its PR, what changed, what it needs, and affected PRs. For each report, update `delivery.md`, forward relevant information to affected threads, and return resulting decisions to the reporting thread. The orchestrator is the single writer to `delivery.md`.

The work loop is complete when every PR thread reports ready for HITL and `delivery.md` records that state.

## 3. HITL loop

Each PR thread conducts HITL directly with the user. It announces readiness and works through questions, review comments, requirement changes, and resulting fixes. Explicit user approval is the merge gate; after approval, the PR thread merges.

Each PR thread decides which HITL outcomes affect delivery and sends those through **Route reports**. After a merge report, send the merged PR's state to dependent PR threads so they can rebase.

This loop is complete when `delivery.md` records every PR as merged.
