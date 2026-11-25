---
name: context-clean-up
license: MIT
description: Audit and slim OpenClaw prompt context to prevent context overflow and reduce cost. Use when the user says /context-clean-up, or asks to reduce prompt bloat, shrink session history, digest/dismiss inactive sessions, tame noisy cron or heartbeat output, or investigate a Context overflow error.
allowed-tools:
  - read
  - write
  - edit
  - exec
  - process
  - cron
  - sessions_list
  - sessions_history
  - session_status
metadata:
  openclaw:
    emoji: "🧹"
---

# Context Clean Up

Runbook-style workflow to **audit** and (optionally) **apply safe fixes** that keep OpenClaw sessions lean.

Principle: the fastest way to lose to context overflow is letting **recurring automation** (cron/heartbeat/reporting) write long outputs back into the **same interactive session transcript**.

## Quick start

- User command:
  - `/context-clean-up` → audit + actionable plan (no changes)
  - `/context-clean-up apply` → apply *low-risk* changes (with backups / reversible patches)

## Workflow (audit → plan → apply)

### Step 0 — Determine scope
1. Identify the OpenClaw **workspace dir** (usually current directory).
2. Identify the OpenClaw **state dir** (usually `~/.openclaw`).

If unsure, run:

```bash
bash -lc 'echo "$HOME" && ls -ld ~/.openclaw'
```

### Step 1 — Audit what is actually bloating context
Run the bundled audit script (short stdout; writes detailed JSON to file):

```bash
bash -lc 'cd "${WORKDIR:-.}" && uv run --python 3.13 -- python skills/context-clean-up/scripts/context_cleanup_audit.py --out memory/context-cleanup-audit.json'
```

If the repo is not in the current workdir, adapt the path accordingly.

Interpretation:
- If you see huge entries under `toolResult` (exec/read/web_fetch): those are **transcript bloat**.
- If you see repeated `System: Cron:` lines: that is **automation bloat**.
- If workspace bootstrap docs are huge: that is **reinjected rules bloat**.

### Step 2 — Plan fixes (batch, lowest-risk first)
Create a short plan with:
- **Top offenders** (largest N transcript entries)
- **Noisiest cron jobs** (frequent + non-empty output)
- **Quick wins** (reversible)

Use these standard levers:

#### Lever A — Make no-op cron jobs truly silent
Goal: cron jobs that do maintenance should output exactly `NO_REPLY`.

Heuristic:
- If a cron job is `deliver=false`, it should **never** output long text.
- If a cron job is a “heartbeat” or “harvester” and has no anomalies, it should output `NO_REPLY`.

Implementation pattern: update the job prompt to end with:

- `Finally output ONLY: NO_REPLY`

#### Lever B — Keep scheduled reports, but avoid transcript injection
If the user wants notifications but you still want a lean interactive session:

- Prefer **out-of-band delivery** from the isolated worker:
  1) send a message (Telegram/Slack/etc.) using the platform tool
  2) output `NO_REPLY`

This keeps the main session transcript cleaner while the user still receives the report.

#### Lever C — Keep workspace bootstrap context small and stable
If the injected bootstrap docs are large:
- move “rarely-needed” notes into `memory/*.md` or `references/*.md`
- keep only **restart-critical rules** in `MEMORY.md`
- keep persona files short (`SOUL.md`, `USER.md`, etc.)

Always create `.bak.<date>` backups before edits.

#### Lever D — Session store hygiene (digest + dismiss inactive sessions)
Goal: keep `~/.openclaw/agents/main/sessions` from accumulating stale cron session keys and orphan transcript files.

Use bundled script:

```bash
bash -lc 'cd "${WORKDIR:-.}" && uv run --python 3.13 -- python skills/context-clean-up/scripts/session_gc.py --retention-days 7 --stale-days 3 --json --report-out memory/session-gc/latest-report.json'
```

Policy:
- Start with **dry-run report only**.
- Apply only after explicit confirmation.
- In apply mode, use **backup-first** and reversible moves (not hard delete).

Conservative apply example:

```bash
bash -lc 'cd "${WORKDIR:-.}" && uv run --python 3.13 -- python skills/context-clean-up/scripts/session_gc.py --retention-days 7 --active-cron-id <id1,id2,...> --apply --prune-stale-keys --move-orphan-jsonl --json --report-out memory/session-gc/latest-apply.json'
```

### Step 3 — Apply (only when user asked for apply)
If the user ran `/context-clean-up apply`:

1) Patch noisy cron jobs (safe edits only):
- Convert success/no-op outputs to `NO_REPLY`
- Leave user-facing reports alone unless the user explicitly agrees

2) Apply session-store hygiene (optional but recommended for long-running agents):
- Prune stale cron session keys from `sessions.json`
- Move old orphan `*.jsonl` to backup folder (do not hard delete)
- Record report JSON under `memory/session-gc/`

3) (Optional) Propose a bootstrap docs compaction PR:
- Only do this with explicit confirmation because it edits the user’s rules/persona.

### Step 4 — Verify
- Confirm the next cron run no longer injects `Cron: ok` / `Cron: HEARTBEAT_OK` noise.
- Confirm session GC changed the expected counts (stale keys/orphans) and preserved backups.
- Watch for compaction events in the session (context ratio should drop).

## Notes / best-practice hints
- Telegram auto-delete helps **your chat app**, but OpenClaw still has its own local session logs; auto-delete alone usually does **not** shrink the model prompt.
- For long-running agents, pair this with a memory layer (e.g., openclaw-mem) so you can retrieve state on demand instead of dragging the full transcript forward.

## References
- `references/out-of-band-delivery.md`
- `references/cron-noise-checklist.md`
- `references/session-store-hygiene.md`
