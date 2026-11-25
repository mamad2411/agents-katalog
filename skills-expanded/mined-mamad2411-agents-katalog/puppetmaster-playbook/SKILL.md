---
name: puppetmaster-playbook
description: >-
  Operator method for Puppetmaster. Use when the user says playbook,
  orchestrate, session pilot, swarm, or asks how to dispatch Puppetmaster
  workers. Pilot stays in chat; workers are durable jobs that communicate
  via artifacts.
---

# Puppetmaster playbook

A playbook is one named work shape (verb + gates). The method is the
rest of the stack. Match one playbook; do not treat this skill as a
bundle of every tool.

`METHOD.md` and `playbooks/` sit next to this file after
`scripts/install_cursor.py`. In the pack repo they live at the root
and in `playbooks/`.

## Pilot loop

1. Inspect active and recent Puppetmaster jobs. Reuse valid artifacts.
   Do not duplicate a live or completed slice.
2. CodeGraph first. Wiki next if one is connected and the question is
   historical.
3. Match one playbook. Copy its steps. Skip only with `skip: <reason>`.
4. Build the smallest useful slices. Every worker prompt states
   objective, scope, owned files, dependencies, expected artifact, and
   verification.
5. Scale workers with independent work. One implement owner per
   coupled feature. One writer per checkout.
6. Dispatch with a 3–6 word label. Await durable completion. Read
   typed artifacts, not job status.
7. At each wave: review the actual diff, run focused tests, then plan
   the next wave.

## Verb pick

| Work | Verb | Playbook |
| --- | --- | --- |
| Audit / find-all / how | `start_swarm` | `investigation` |
| Coupled fix | `start_implement` or `edit` | `bug-fix` |
| Coupled feature | `start_implement` | `feature` |
| Adversarial review | `start_review` | `interrogate` |
| One metric | `start_implement` | `hillclimb` |
| Where is X | CodeGraph | (none) |
| Cost / verb dry-run | `route_task` | (none) |

Last-mile on a dirty tree is `edit`. Implement branches a clean
worktree and will miss uncommitted work.

## Evidence

A started job, heartbeat, `complete`, or $0 receipt is not success.
Empty, stale, degraded, or missing-patch output is a blocker.

This skill does not authorize commits, pushes, tags, releases,
credential changes, or destructive operations unless the human
explicitly asked.
