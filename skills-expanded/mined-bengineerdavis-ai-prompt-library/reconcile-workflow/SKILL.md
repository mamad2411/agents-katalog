---
name: reconcile-workflow
description: Reconcile established repository, worktree, and Backlog evidence before selecting and handing off one eligible implementation slice. Use when catching up, resolving competing task records or claims, locating unpublished work, or choosing the next usable task; not for implementing an already claimed, well-scoped task.
spec_hash: f6d3173103e3
license: MIT
metadata:
  version: 1.0.0
  supersedes:
---

# Reconcile Workflow

Route work from evidence, not from status labels or enthusiasm for the newest idea. Preserve what exists, use the configured Backlog adapter, and hand off one eligible vertical slice.

## 1. Establish the evidence map

Enumerate repository roots and worktrees before reading a queue. For each root, inspect:

- branch, upstream, dirty files, and aggregate diff;
- `backlog/config.yml`, the configured Backlog adapter, and native task records;
- native dependencies, active claims, stale leases, and validation issues;
- unpublished specifications, implementation evidence, and explicit ownership.

Prefer the configured `backlog-py` MCP tools. Fall back to its installed CLI. Check `backlog-py orchestration queue --json`, `eligible --json`, `claims --json`, and `stale-leases --json` where available. Inspect the actual installed surface before relying on a command or field.

Use `references/handoff.md` for the evidence-map and handoff shapes. Never describe unchecked ownership, publication, or test state as established.

## 2. Preserve established work

Compare aggregate content and task semantics, not only branch ancestry. Identify the canonical candidate from current contracts and merged records. Record unique requirements, semantic supersession, and unresolved ownership in Backlog.

A successful branch update or merge is transport, not semantic proof. If the combined result drops an approved requirement, reconciliation has failed.

Never discard, overwrite, stash, reset, or appropriate another session's or agent's work to make a queue or branch look clean. Do not recommend cleanup while real work or its ownership is unresolved.

## 3. Capture findings in Backlog

Use the configured Backlog adapter for task records, dependencies, claims, run history, decisions, and publication obligations. Create owned records for newly discovered usage blockers and deferred ideas. Link existing owners rather than absorbing their work.

Do not create a parallel `.scratch` queue, another scheduler or claim store, or a new durable handoff narrative. Keep routing evidence in the relevant task or decision record.

## 4. Reconcile claims, not just queues

A main checkout can report a task eligible while another worktree contains a claim or real work. Treat claims as evidence to inspect, not a global availability lock.

- Contrast expired and active claims.
- Respect active claims and multi-agent ownership; do not duplicate or appropriate their work.
- Distinguish an expired empty claim from a claim with uncommitted implementation.
- Record the evidence before cleanup. Only a verified empty stale claim is a cleanup candidate.

Example: main reports eligible; worktree A has an expired empty claim; agent B has an active claim with implementation. Preserve B's work and do not implement that task. A alone may be a cleanup candidate.

## 5. Bound the usable milestone

Write or locate a small MVP contract with:

1. first usable outcome;
1. one end-to-end workflow;
1. minimum inputs;
1. explicit non-goals;
1. feedback criteria.

Classify each new idea as **usage-blocking** or **deferred**. Keep deferred ideas visible in Backlog. Do not let them expand the active implementation contract.

## 6. Select one eligible vertical slice

Choose the smallest end-to-end task that satisfies the bounded outcome and has no unresolved dependency, ownership, preservation, or claim blocker.

Name its task ID, native dependency state, evidence of eligibility, and remaining risks. Explain briefly why alternatives are blocked or later. Do not expose every open task as equally actionable or implement from multiple queues.

## 7. Hand off, then stop routing

Give a fresh implementation session the selected task, authoritative requirements, preserved work, authorized scope, verification surface, and remaining owners. Tell it to claim through Backlog before editing and to record progress and completion through the configured adapter.

When the user names a destination for the route or handoff, write it there and leave a concise response pointing to that file. Do not substitute a chat-only summary for a requested file.

Do not silently turn the routing session into the implementation session.

## Never

- Never commit, push, merge, publish, create or remove worktrees, or edit implementation files without authorization for that specific action. Backlog routing records do not authorize implementation.
- Never silently choose an owner for a semantic conflict, describe stale status as active work, or claim unchecked validation passed.
- Never drop deferred ideas without an owned record.
