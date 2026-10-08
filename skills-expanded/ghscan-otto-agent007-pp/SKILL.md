---
name: pest-patrol-rebuild-orchestrator
description: Use when selecting, reconciling, or preparing one Pest Patrol controlled-rebuild graph node for bounded execution.
---

# Pest Patrol Rebuild Orchestrator

Treat `docs/rebuild/graph.json` as the scheduler and
`docs/rebuild/README.md` as the sole detailed operating contract. Do not
reimplement graph eligibility, lifecycle, ownership, evidence, or package
manager algorithms in prose.

## Reconcile one node

1. Read the root and `docs/AGENTS.md`, the runbook, graph,
   `docs/CODEX_OPERATING_PLAN.md`, `tasks/in-progress.md`, and protected
   worktree status.
2. Run `pnpm rebuild:graph:check` and
   `pnpm rebuild:graph:reconcile -- --offline`. When PR or merge state matters,
   run live reconciliation with read-only GitHub credentials and a bounded
   timeout. Stop on any failed or unavailable required fact.
3. Reconcile the existing running node first. If none exists, use the graph's
   validated `preferredPrOrder` and the canonical runbook to propose at most
   one candidate. Never silently edit state or invent empty fields.

## Bounded handoff

Report the selected node, command exits, live versus local facts, goal,
deliverables, ownership, exclusions, intended base and branch, exact checks,
risks, approvals, and any missing execution-ready fields. End with `blocked`,
`planning-ready`, or `controller-approval-required`.

Only the controller may authorize implementation, commits, pushes, PRs,
migrations, security decisions, provider changes, environment or preview
changes, or production actions. The handoff never supplies that authority.
