---
name: "keep-codex-fast"
description: "Use when Codex feels slow or bloated, when local sessions/logs/worktrees/config have grown over time, or when a user wants safe maintenance for Codex Desktop/CLI state. Provides a read-only report by default, backs up before applying changes, archives instead of deleting, normalizes Windows extended paths, prunes dead config projects, rotates large logs, and moves stale worktrees."
metadata:
  short-description: "Safe Codex local-state maintenance"
---

# Keep Codex Fast

Use this skill to inspect and safely maintain local Codex state. The goal is to reduce local drag without surprising the user or losing continuity.

Primary principle: preserve continuity before applying changes. For active repo chats the user may continue, recommend a comprehensive handoff document and reactivation prompt before archiving anything.

## Safety Rules

- Inspect before mutating.
- The first run must be report-only. Report mode must not write files, create backups, move folders, or change local Codex state.
- Back up before applying changes. Use `--backup-only` when the user wants backups without moving or changing local state.
- Archive or move files instead of deleting them. Do not permanently delete user chats, logs, worktrees, memories, skills, plugins, or automations.
- Write manifests and restore scripts when sessions/worktrees are moved.
- If Codex is running, default to report-only. Apply changes only after Codex is closed or when the user explicitly accepts waiting for Codex to exit.
- Never modify or copy credential files unless the user explicitly asks for that. Back up memory/skill/plugin/automation files before touching local state.
- Treat backup folders as private local artifacts because they can contain Codex metadata. Do not ask users to publish or share backups unless they have reviewed them first.
- Do not print raw thread IDs, chat titles, local paths, or process paths unless the user asks for details or runs `--details`.
- Before applying changes, tell the user to create handoff docs for active repo chats they may continue.
- Before archiving any active repo chat the user may want to continue, recommend creating a comprehensive handoff doc plus a reactivation prompt.
- Do not archive old-but-important active repo chats until the user either confirms a handoff exists or confirms they do not need one.

## Default Workflow

1. Reassure the user: the first run is read-only, privacy-safe, and the skill archives instead of deleting when changes are later applied.
2. Run the bundled script in report mode:

```bash
python scripts/keep_codex_fast.py
```

3. Summarize:
   - active session size
   - archived session size
   - largest active sessions
   - stale worktree candidates
   - log size
   - bad Windows `\\?\` path counts
   - config project prune candidates
   - top Node/dev processes
4. Before applying changes, recommend that the user create handoffs for all active repo chats they may continue. Explain that handoffs let them archive heavy chats and resume from docs in fresh threads.
5. Identify large/old active repo chats that may still matter. For each one the user wants to continue, create or update:
   - a repo-local handoff doc
   - a reactivation prompt that can start a fresh chat without losing the thread
6. If the user wants to apply the recommended maintenance, ask them to close Codex or use `--wait-for-codex-exit`, then run:

```bash
python scripts/keep_codex_fast.py --apply --archive-older-than-days 10 --worktree-older-than-days 7
```

7. Verify after applying:

```bash
python scripts/keep_codex_fast.py
```

8. Ask whether the user wants a recurring report-only reminder:
   - weekly for heavy Codex use across many repos/terminals
   - biweekly for lighter use
   - no reminder if they prefer manual maintenance

If the user wants automation and the Codex app automation tool is available, create only a recurring report/reminder automation. Do not recommend recurring mutating maintenance, because automation cannot know whether the user created handoffs. The prompt must say not to pass `--apply`, not to archive/move/prune/rotate/normalize/delete/mutate local state, and to remind the user that manual apply should happen only after handoffs are confirmed and Codex is closed.

## What Apply Does

- Backs up important metadata to `~/Documents/Codex/codex-backups/keep-codex-fast-*`.
- Archives old non-pinned sessions to `~/.codex/archived_sessions/`.
- Normalizes Windows extended paths like `\\?\C:\...` inside local SQLite text fields.
- Prunes missing/temp project blocks from `config.toml` and writes UTF-8 without BOM.
- Moves stale worktrees to `~/.codex/archived_worktrees/`.
- Rotates `logs_2.sqlite*` into `~/.codex/archived_logs/` only when above the threshold.
- Reports heavy Node processes without killing them.

Report mode does none of those mutations. It only prints counts and pseudonymous candidates. Use `--details` when raw IDs, titles, or paths are needed for diagnosis.

## Recommended Policy

- Keep only the last 7-10 days of non-pinned chats active.
- Use handoff docs for important old threads.
- Start fresh threads from handoff docs instead of repeatedly resuming giant chats.
- Run weekly maintenance if Codex is used daily across many repos/terminals.
- Offer weekly or biweekly report-only reminders after the first successful apply; do not assume the user wants recurring maintenance.
- When in doubt, leave a chat active or ask the user. Never archive a chat that is pinned, current, or explicitly marked as still needed without a handoff.

## Handoff Doc + Reactivation Prompt

For important active repo chats, create a handoff before archiving. Prefer a repo-local path such as `docs/codex-handoffs/YYYY-MM-DD-topic.md` or a user-approved docs location.

Use `references/handoff-template.md` when the user wants a concrete template.

A handoff document converts an old chat into durable project memory. It should let a fresh Codex thread continue after reading the repo and the handoff, without needing the original chat history.

Offer this prompt for each active repo chat the user may want to continue:

```text
Create a comprehensive handoff document for this repo/session before I archive Codex history.

Include:
- repo/path and branch
- current goal
- what we already completed
- files touched or investigated
- commands/tests already run
- known errors, warnings, or failing checks
- open decisions
- constraints, user preferences, and do-not-touch areas
- the next 3-7 concrete steps

Also include a reactivation prompt I can paste into a fresh Codex chat so it can continue from this handoff without relying on the old chat context.

Save the handoff in a sensible repo-local place like docs/codex-handoffs/YYYY-MM-DD-topic.md unless this repo already has a better handoff location.
```

The handoff should capture:

- repo/path and branch
- current goal
- what was already done
- key files touched or investigated
- commands/tests already run
- known failures or warnings
- open decisions
- next 3-7 concrete steps
- any constraints, user preferences, or "do not touch" areas

Add a reactivation prompt at the top or bottom:

```text
We are continuing from this handoff. Read this document first, inspect the current repo state, verify what still applies, and continue from the next steps without assuming the old chat context is available.
```

## Automation Reminder Prompt

Offer this after the first report/apply/verify cycle:

```text
Use $keep-codex-fast to create a recurring Codex maintenance reminder.

Schedule it weekly if I use Codex heavily, or biweekly if that seems safer.

The reminder should:
- run the keep-codex-fast report first
- never pass --apply or run mutating maintenance automatically
- never archive, move, prune, rotate, normalize, delete, or mutate local Codex state
- remind me to create comprehensive handoff docs and reactivation prompts for active repo chats before any manual apply
- summarize active session size, archived session size, extended path candidates, old session candidates, worktree candidates, log size, and top Node/dev processes
- report heavy Node/dev processes without killing them
- tell me that manual apply should only happen after I confirm handoffs exist or are not needed and Codex is closed
```

## Anti-Patterns

Avoid these behaviors:

- deleting sessions, logs, worktrees, memories, plugins, or skills permanently
- applying changes while Codex is actively writing the DB
- archiving important repo chats before creating handoff docs
- treating active history size as "bad" without checking whether the user needs continuity
- killing Node/dev processes automatically
- rewriting `config.toml` without a backup and parse check
- writing UTF-8 TOML with a BOM on Windows
- promising speed gains as universal fact; frame improvements as local-state maintenance results
- making users feel like they did something wrong by using Codex heavily

## User-Facing Caution

Tell users this does not permanently delete chats, worktrees, or logs. It moves them into archive folders and writes restore helpers. The only removed content is stale metadata, such as project entries pointing to folders that no longer exist, and even that happens after backing up `config.toml`.

Also tell users backup folders can contain private local Codex metadata. They should keep backups local and avoid publishing or sharing them unless they have reviewed what is inside.
