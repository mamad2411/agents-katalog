---
name: kos-runner-disk-hygiene
description: Prevent self-hosted runner disk-exhaustion failures (No space left on device) during zai workflow runs by using the ensure-disk-space actions and pruning caches.
user-invocable: true
when_to_use: "When a workflow run failed with 'No space left on device', or when hardening a workflow that installs deps / pulls images on a self-hosted runner."
category: utilities
argument-hint: "[workflow or run-id]"
keywords: [disk, space, no-space-left, runner, self-hosted, cache, prune, docker]
related: [kos-zai-run-failure-prevention, kos-gh-automation-tooling]
metadata:
  author: kos-workflow-improvement
  attribution: distilled from audit-fix run 28097503249 (No space left on device) + ensure-disk-space actions
  license: repo
  version: "1.0"
---

# Idea

These workflows run on self-hosted runners (`runs-on: [self-hosted, big]` or `self-hosted`). They install npm deps, restore action caches, and sometimes pull Docker images. Over time the runner disk fills and a run dies mid-setup with `No space left on device` — observed killing an `audit-fix` run during action cache restore. The repo ships `ensure-disk-space` and `ensure-docker-disk-space` actions for exactly this; the skill is knowing when they must precede the heavy step.

## When to invoke this skill directly

- A run failed with `No space left on device` / `ENOSPC` / cache-restore disk error.
- You are adding/editing a workflow that does `npm ci`, restores large caches, or pulls images on a self-hosted runner.

## References

- `.github/actions/ensure-disk-space/` — free disk before heavy steps.
- `.github/actions/ensure-docker-disk-space/` — free Docker storage before image jobs.
- `setup-environment` action — shared setup that runs first in most workflows.
- Symptom line shape: `##[error]No space left on device : '.../node_modules/...'`.

## Communication Style

Name the failing step, confirm it is disk (not OOM), then point at the single ensure-disk-space step to insert before it.

## Core Principles

YAGNI / KISS / DRY. Reuse the existing ensure-disk-space actions; do not hand-roll `rm -rf`. Only prune what the runner actually accumulates (stale caches, old images).

## Your Approach

1. Confirm the error is disk (the path ends in `node_modules/...` or a cache/image dir), not memory.
2. Find the first heavy step (action cache restore, `npm ci`, image pull) in the job.
3. Insert/confirm `ensure-disk-space` (and `ensure-docker-disk-space` for image jobs) **before** that step.
4. If it recurs, prune stale local-cache entries / old Docker images on the runner.

## Process Flow (Authoritative)

1. Grep the failed log for `No space left on device` / `ENOSPC`.
2. Identify the step that was running (usually setup/cache restore).
3. Ensure an ensure-disk-space step precedes the job's heavy work.
4. Re-dispatch; track whether recurrence demands runner-side cleanup.

## Output Format

```text
DISK_FULL at <step>  =>  ensure <action> runs before <heavy-step>  (runner cleanup if recurring)
```

## Critical Constraints

- `ensure-disk-space` must run **before** the step that needs the space, not after.
- Do not delete caches blindly — prune by age/staleness; some caches are expensive to rebuild.
- Distinguish disk-exhaustion (this skill) from `turn_limit_hit`/rate-limit (other modes) — they look similar from the conclusion alone.
