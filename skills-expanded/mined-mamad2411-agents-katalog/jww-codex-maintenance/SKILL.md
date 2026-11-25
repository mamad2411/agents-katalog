---
name: jww-codex-maintenance
description: Audit and reduce Codex desktop and CLI local-state bloat without deleting history or editing private app state. Use when Codex feels slow, logs or sessions consume substantial disk space, stale task worktrees accumulate, configuration contains dead project paths, or the user wants a repeatable maintenance report. Default to a read-only audit; perform archival or rotation only when the user explicitly requests cleanup.
compatibility: >-
  Requires OpenAI Codex in the ChatGPT desktop app or Codex CLI; not intended
  for Claude Code, GitHub Copilot, or other agent harnesses.
---

# Maintain Codex Local State

Separate diagnosis from cleanup. Large local state can correlate with a slow app,
but do not treat file size as proof of the cause or promise a speedup.

## Select the Mode

- **Audit** is the default. Inspect and report without changing tasks, files,
  configuration, processes, or scheduled tasks.
- **Apply** requires an explicit cleanup request. Back up affected state, present
  the resolved targets, and make only the approved reversible changes.
- **Automate** creates a recurring audit and report. Do not schedule unattended
  mutation of live Codex files.

If the request is ambiguous, complete the audit and stop with a proposed cleanup
set rather than interpreting “make Codex faster” as permission to mutate state.

## Inventory the Current State

1. Resolve `CODEX_HOME` from the environment when it is set; otherwise use
   `~/.codex`. Do not redefine `HOME`, `CODEX_HOME`, or another common system
   variable in shell commands.
2. Determine whether the desktop app, Codex CLI, scheduled runs, or other Codex
   processes are active. Report them; do not stop them automatically.
3. Record sizes, file counts, oldest and newest modification times, and largest
   files for:
   - active and archived session transcripts
   - Codex and desktop-app logs
   - app-managed and Git worktrees
   - configuration and profile files
   - local databases and their `-wal` and `-shm` sidecars
   - memories, skills, plugins, and scheduled-task metadata when present
4. Use host-supported task operations to list task status, pinning, age, and
   project association when available. Do not infer pinning or task state by
   rewriting an index or querying an undocumented database schema.
5. Inspect heavy development processes, especially long-lived language servers
   and dev servers, but report their command, working directory, age, and memory
   use instead of killing them.

On macOS, include `~/Library/Logs/com.openai.codex/YYYY/MM/DD`. Codex session
transcripts normally live in `$CODEX_HOME/sessions`, archived transcripts in
`$CODEX_HOME/archived_sessions`, and CLI logs in `$CODEX_HOME/log`. Discover
other locations from the running installation rather than assuming a private
layout.

## Classify Candidates

Classify each item and explain the evidence:

- **Task archival:** old, unpinned, inactive tasks with no running work. Treat an
  age threshold such as 7–10 days as a user preference, not a universal rule.
- **Large active task:** an unusually large transcript that may benefit from a
  handoff and a fresh task. Size alone does not make it safe to archive.
- **Scheduled-run worktree:** an old unpinned run whose task can be archived
  through the app. Frequent scheduled tasks can intentionally create many
  worktrees.
- **Repository worktree:** clean, unused, and associated with completed work.
  Confirm its branch and repository ownership before proposing removal.
- **Rotatable log:** an old or oversized log that is not currently being
  written.
- **Dead configuration path:** a configured project path that does not exist.
  Distinguish temporarily unavailable volumes from genuinely obsolete paths.
- **Path alias:** two spellings that resolve to the same location. On Windows,
  compare regular and extended-length paths canonically, but do not rewrite app
  state merely to normalize display text.

Exclude pinned tasks, active goals, running scheduled tasks, dirty worktrees,
current logs, and uncertain paths from automatic cleanup.

## Back Up Before Applying

1. Resolve a timestamped backup directory outside the live source directories.
   Confirm that enough free space exists before copying.
2. Back up only the state that the approved cleanup can affect, plus the config
   and indexes needed to restore it. Create a manifest with source paths, sizes,
   timestamps, and checksums.
3. Treat transcripts, logs, memories, configuration, and databases as sensitive.
   Do not place them in a repository, shared folder, or cloud-synced destination
   without explicit approval. Do not copy authentication credentials unless the
   user specifically requests an encrypted credential backup.
4. When a database is live, use a supported backup operation. Otherwise require
   Codex to be closed and copy the database together with relevant sidecars. Do
   not assume copying one live SQLite file creates a consistent backup.
5. Verify that the backup can be read before changing the source.

If the desktop app is open, limit the apply phase to supported task or scheduled
run operations. For log rotation, database maintenance, or direct app-owned file
movement, provide the exact offline runbook and wait for the user to quit the app
or continue from a separate CLI session.

## Apply Reversible Cleanup

Perform only the approved categories:

1. For a large task that must remain resumable, invoke `$jww-handoff` when it is
   available and write the canonical handoff in the task's project. Verify the
   handoff against current source before archiving the task.
2. Archive tasks and scheduled runs through host-supported operations. Never
   simulate archival by moving session JSONL files or changing the local state
   database. Preserve pinned tasks.
3. Archive app-managed worktrees by archiving their owning task or run. For
   ordinary Git worktrees, inspect `git worktree list --porcelain` and
   `git worktree prune --dry-run`; do not move worktree directories manually.
   Remove a clean worktree only when the user explicitly approves that target.
4. With Codex stopped, move rotatable logs into the backup/archive directory and
   leave the expected live log directory in place. Prefer rotation or
   compression to deletion.
5. Patch dead project entries in the documented config source only after the
   user approves each entry. Preserve comments and unrelated settings, then
   parse the resulting TOML.
6. Do not vacuum, edit, rebuild, or replace a Codex database unless the user
   explicitly requests database repair and an official procedure supports it.
7. Do not kill background processes. Give the user the exact candidates and let
   them decide which processes to stop.

## Verify and Report

Repeat the inventory and compare it with the baseline. Verify, as applicable:

- configuration still parses
- databases open read-only and pass a non-mutating integrity check
- intended tasks or scheduled runs are archived and pinned tasks are unchanged
- active-session bytes fell only by the intended archival amount
- archived-session bytes and counts changed consistently
- worktrees still registered with Git exist, and no dirty worktree was removed
- live log directories exist and fresh logs can be created after relaunch
- path-alias and dead-path findings are resolved without unrelated config edits

Ask the user to relaunch the desktop app and confirm the sidebar, active tasks,
scheduled tasks, and normal startup. Report measured disk-space changes
separately from perceived performance; never repeat an anecdotal “10x faster”
claim as an expected result.

The final report must include the mode, baseline, candidate set, excluded items,
backup location, exact changes, validation results, remaining risks, and restore
instructions.

## Automate the Audit

Create or update a scheduled task only when the user asks. Make the recurring
task read-only: inventory sizes and counts, identify archival candidates, flag
large logs and stale worktrees, and return a report for review. Test the prompt
manually before scheduling it.

Keep local scheduled-task constraints explicit: the computer and desktop app
must be running to access local projects, and frequent scheduled runs can create
additional worktrees. Use a standalone scheduled task for independent weekly
reports, avoid pinning routine runs, and archive reviewed runs through supported
operations.

Do not schedule offline log rotation or database copying from the desktop app;
those steps require the app to be stopped and therefore belong in an explicit
interactive maintenance run.
