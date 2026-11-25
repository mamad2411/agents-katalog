---
name: codex-optimize
description: Use when local .codex state needs maintenance — sessions/logs/worktrees/config bloat cleanup, thread metadata bloat detection, or provider metadata sync between SQLite and JSONL records. Covers both storage cleanup and metadata consistency.
---

# Codex Optimize

## Overview

Maintain local Codex state through two branches: **clean** (reduce storage bloat) and **sync** (fix provider metadata inconsistency). Both branches follow the same principle: inspect before mutating, back up before applying, archive or move instead of deleting.

## Shared Safety Rules

- Inspect before mutating. The first run must be report-only and must not write files, create backups, move folders, or change local state.
- Back up before applying changes. Archive or move files instead of deleting them — never permanently delete user chats, logs, worktrees, memories, skills, plugins, or automations.
- If Codex is running, default to report-only. Apply changes only after Codex is closed or when the user explicitly accepts waiting for Codex to exit.
- Never modify or copy credential files unless the user explicitly asks for that.
- Treat backup folders as private local artifacts — they can contain metadata including thread titles and first-message previews. Do not ask users to publish or share backups unless they have reviewed them first.
- Do not print raw thread IDs, chat titles, local paths, or process paths unless the user asks for details.
- Write manifests and restore scripts when sessions or worktrees are moved so changes are reversible.
- Before archiving any active repo chat the user may want to continue, require a handoff doc plus a reactivation prompt.

## Branch: Clean

Reduce local `.codex` storage bloat by archiving old sessions, moving stale worktrees, rotating oversized logs, pruning dead config entries, and reporting (optionally repairing) thread metadata bloat.

### Workflow

1. **Reassure.** Explain the first run is read-only and privacy-safe. When changes are later applied, the skill archives instead of deleting.
2. **Run report.**

   ```bash
   python scripts/codex_clean.py
   ```

3. **Summarize findings:** active session size, archived session size, largest active sessions, thread metadata bloat (title/preview character totals, max lengths, over-limit counts), stale worktree candidates, log size, bad Windows `\\?\` path counts, config project prune candidates, top Node/dev processes.
4. **Create handoffs** for active repo chats the user may continue. Explain that handoffs let them archive heavy chats and resume from docs in fresh threads. For each important chat, create a repo-local handoff doc and a reactivation prompt. Use `references/handoff-template.md` for the template.
5. **Apply with confirmation.** Ask the user to close Codex or use `--wait-for-codex-exit`, then run:

   ```bash
   python scripts/codex_clean.py --apply --archive-older-than-days 10 --worktree-older-than-days 7
   ```

6. **Verify** by re-running the report:

   ```bash
   python scripts/codex_clean.py
   ```

7. **Offer recurring reminder.** Ask whether the user wants a recurring report-only reminder (weekly for heavy use, biweekly for lighter use, or none). Recurring automation must never pass `--apply` or mutate local state — it can only run the report and remind the user to do manual maintenance after confirming handoffs exist and Codex is closed.

### What Apply Does

- Backs up important metadata and `state_5.sqlite` to `~/Documents/Codex/codex-backups/codex-clean-*`.
- Archives old non-pinned sessions to `~/.codex/archived_sessions/`.
- Normalizes Windows extended paths like `\\?\C:\...` inside `state_5.sqlite` text fields.
- Prunes missing/temp project blocks from `config.toml` and writes UTF-8 without BOM.
- Moves stale worktrees to `~/.codex/archived_worktrees/`.
- Rotates `logs_2.sqlite*` into `~/.codex/archived_logs/` only when above the threshold.
- Reports heavy Node processes without killing them.
- Reports pathological active thread titles and `first_user_message` previews. Repairs them only when the user explicitly opts in with `--repair-thread-metadata-bloat`.

Report mode does none of those mutations — it only prints counts and pseudonymous candidates.

### Recommended Policy

- Keep only the last 7–10 days of non-pinned chats active.
- Use handoff docs for important old threads and start fresh threads from them instead of repeatedly resuming giant chats.
- Run weekly maintenance if Codex is used daily across many repos/terminals.
- When in doubt, leave a chat active or ask the user. Never archive a chat that is pinned, current, or explicitly marked as still needed without a handoff.
- Treat title/preview repair as metadata repair only — the full rollout transcript remains in the session JSONL. Bounded SQLite fields are for list/navigation display.

### Thread Metadata Bloat

Codex can become slow when `threads.title` or `threads.first_user_message` stores a full prompt-sized value instead of a display title or preview. This affects the thread list/navigation path before the UI renders anything.

The script reports active thread count, total title/preview characters, maximum title/preview length, and counts of titles/previews over the configured limits.

Normal apply mode reports metadata-bloat candidates but does not repair them. If the user explicitly opts in, after backups and only when Codex is not running:

```bash
python scripts/codex_clean.py --apply --repair-thread-metadata-bloat
```

This bounds active `threads.title` (default 120 chars) and `threads.first_user_message` (default 240 chars), appends repaired titles to `session_index.jsonl`, and writes a targeted repair manifest with old values so the change can be reversed. Treat `thread-metadata-repairs.jsonl`, `restore-thread-metadata.py`, and the whole backup folder as private local artifacts.

### Handoff Template

Use `references/handoff-template.md` for the handoff doc structure. A handoff should capture: repo/path and branch, current goal, what was already done, key files touched or investigated, commands/tests already run, known failures or warnings, open decisions, next 3–7 concrete steps, and any constraints or "do not touch" areas.

Include a reactivation prompt:

```text
We are continuing from this handoff. Read this document first, inspect the current repo state, verify what still applies, and continue from the next steps without assuming the old chat context is available.
```

## Branch: Sync

Fix provider metadata inconsistency between `state_5.sqlite` and rollout JSONL files when thread lists omit unarchived records or `threads.model_provider` diverges from `config.toml`.

### Workflow

1. **Locate the active database.** Run `node <skill>/scripts/provider_sync.mjs inspect`. Prefer `~/.codex/sqlite/state_5.sqlite` when present. Treat root `~/.codex/state_5.sqlite` as legacy unless inspection proves it is active.
2. **Inspect and report.** The script reports: active DB path, current `config.toml` `model_provider`, provider distribution for `archived = 0`, and number of rows that would change.
3. **Confirm before writing.** Do not run write mode from assumption alone. The write command must include `apply --yes`.
4. **Apply.**

   ```bash
   node <skill>/scripts/provider_sync.mjs apply --yes
   ```

   The script backs up the SQLite DB before writing and only rewrites unarchived rows by default. After writing, verify that SQLite reports the expected `changes()` count.

   Add `--rewrite-rollouts` only when the user explicitly confirms mutating original `~/.codex/sessions/**/*.jsonl` metadata:

   ```bash
   node <skill>/scripts/provider_sync.mjs apply --yes --rewrite-rollouts
   ```

5. **Verify.** Re-run `inspect`. If the app-server still omits records after SQLite-only apply, explain that JSONL `session_meta.model_provider` can repair SQLite back to original values. Prefer `thread/list` with `modelProviders: []` for product code when the goal is all-provider display without mutating local history.

### Commands

- `--to openai|custom` — override the target provider (defaults to current `config.toml` provider).
- `--db /path/to/state_5.sqlite` — override DB path.
- `--include-archived` — include archived rows (avoid unless the user explicitly asks).
- `--rewrite-rollouts` — also back up and rewrite the first `session_meta` line in scoped JSONL rollouts whose `payload.model_provider` differs from the target provider.

### Sync-Specific Safety Rules

- Never edit `~/.codex/sessions/**/*.jsonl` unless the user explicitly asks to rewrite original rollout metadata via `--rewrite-rollouts`.
- Never delete Codex DB or JSONL files as part of provider normalization.
- Never write secrets from `config.toml` to output. Report only provider id and DB paths.
- Prefer `modelProviders: []` in app-server clients when the actual goal is all-provider display, because it avoids mutating local history.
