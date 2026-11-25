---
name: deployment-safety
description: Safe shipping to production on any platform (Render, Vercel, AWS, Docker, bare VM). Use when deploying, releasing, configuring CI/CD, writing Dockerfiles or infra config, running migrations against production, or when the user says "deploy", "release", "go live", "ship", "rollback", or "production".
---

# Deployment Safety

A deploy is a bet that new code behaves in an environment you've never run it in. This skill makes the bet survivable: every deploy must be **verifiable** (you can tell if it worked) and **reversible** (you can undo it faster than users notice).

## The two questions before any deploy

1. **"How will I know within 5 minutes if this broke something?"** — if the answer is "users will tell us", stop and add the signal first (health check, error rate, a smoke request you'll run).
2. **"What is the undo?"** — redeploy previous image/commit? feature flag off? config revert? If the undo involves a database, see the migration rules below, because *code rolls back; data does not*.

## Gates

### Gate 1: Build determinism
- The artifact deployed is the artifact tested: build once, promote the same image/bundle through environments. Rebuilding per-environment invites "works in staging" drift.
- Pin versions: base images by tag (ideally digest), lockfiles committed and honored (`npm ci`, `pip install -r` with pins). A deploy should not change behavior because a dependency released overnight.
- Know your build-time vs run-time config split. Anything baked at build (e.g. `NEXT_PUBLIC_*`) cannot be fixed by editing env vars later — document which is which.

### Gate 2: Config & secrets parity
- Every env var the code reads exists in the target environment. Diff code's required config against the platform's actual config *before* deploying, not after the crash loop.
- Fail fast and loud on missing/invalid config at boot — a clear startup error beats a 3 a.m. NullPointerException.
- Verify the deployed commit: expose a version/commit fingerprint endpoint or log line so you can confirm what's actually running (never assume the deploy took).

### Gate 3: Database migrations — the irreversible part
- **Expand → migrate → contract.** Never deploy a migration and the code that requires it as one atomic hope. Order: (1) additive migration (new nullable column/table) → (2) code that writes both/reads either → (3) backfill → (4) code that uses only new → (5) drop old, releases later.
- Destructive operations (DROP, ALTER TYPE, DELETE, renames) get: a stated rollback plan, a backup/snapshot taken first, and explicit user confirmation. A rename is a drop in disguise — do add+backfill+drop instead.
- Migrations must be safe to run twice (idempotent or guarded) and safe while old code is still running (the previous version and new schema coexist during rollout).
- Long locks kill production: on Postgres, add indexes `CONCURRENTLY`, avoid full-table rewrites in peak hours, set `lock_timeout`.

### Gate 4: Rollout
- Health checks must check *readiness* (can serve: DB reachable, migrations applied) not just liveness (process up). Zero-downtime deploys are only as good as the readiness probe.
- Prefer progressive exposure for risky changes: feature flag, canary instance, or percentage rollout. The flag default must be the old behavior.
- Graceful shutdown: handle SIGTERM, drain in-flight requests, stop accepting new work (critical for workers/queues — a killed job must be re-runnable).

### Gate 5: Post-deploy verification (non-optional)
Within minutes of the deploy, actually do — don't just plan to do:
1. Confirm the running version fingerprint matches what you shipped.
2. Hit the golden path end-to-end (login → one core read → one core write) against production.
3. Watch error rate/logs for the first minutes; compare to pre-deploy baseline.
4. Only then report "deployed". A deploy without verification is a deploy that *might* have happened.

## Rollback discipline
- Practice the rollback path before you need it; a documented-but-never-run rollback is fiction.
- Roll back on *symptom*, investigate on *stable* — don't debug forward in production while users bleed unless rollback is impossible.
- After any incident-driven rollback, the fix re-ships with a test or guard that would have caught it.

## Anti-patterns to refuse
- "Just SSH in and edit it" — snowflake changes that the next deploy silently reverts.
- Deploying Friday-evening/holiday-eve changes that touch auth, money, or migrations without explicit user acknowledgment.
- `latest` tags, unpinned deps, or `--force` pushes to the deploy branch.
- Secrets pasted into CI logs, Dockerfiles (`ENV SECRET=...` is baked into layers), or shell history when a secret store exists.
