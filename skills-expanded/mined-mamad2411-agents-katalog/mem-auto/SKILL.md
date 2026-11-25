---
name: mem-auto
description: Run the automatic memory lifecycle on mem-auto, /mem-auto, or $mem-auto — resume open [Handoff] entries, capture verified [Candidate] notes, and delegate to mem-recall, mem-promote, mem-clean, and mem-sync.
metadata:
  related-skills: mem-recall, mem-promote, mem-clean, mem-sync
---

# mem-auto — Unified Memory Autopilot

Runs the automatic memory loop; delegate detailed work to the narrow mem-* skills.

## Memory Scopes

- Long-term memory: global durable instructions, preferences, facts, and reusable conventions in `~/.agents/AGENTS.md` (the canonical core read natively by every agent); project durable rules in `AGENTS.md` or `CLAUDE.md`.
- Short-term memory: daily `[Candidate]` logs in `~/.agents/memories/YYYY-MM-DD.md` and `.memories/YYYY-MM-DD.md`; active `[Handoff]` state lives in per-task files under `.memories/handoffs/` (one file per task). Both the daily logs and the `handoffs/` subdirectory sync through `/mem-sync`.

## Delegation

Use `/mem-recall` for short-term lookups, `/mem-promote` for durable promotion/prune,
`/mem-clean` for destructive cleanup, and `/mem-sync` for project log status/diff/pull/push.

## Autopilot Loop

- [ ] **Start / Handoff In**
  - In cross-device projects, run `/mem-sync` pull first.
  - **Legacy handoff migration runs at most once.** If the sentinel `.memories/.handoff-migrated` exists, skip this step — do not re-scan. Otherwise run the one-time migration in [references/handoff-migration.md](references/handoff-migration.md): it greps project and global daily logs for inline `[Handoff]` residue, migrates any found, and writes the sentinel so later sessions never re-check. Legacy handoffs that arrive later via `/mem-sync` are surfaced on demand by `/mem-recall`'s fallback grep, not by checking at every start.
  - Resolve handoffs by listing `.memories/handoffs/` — one file per active task, named `YYYY-MM-DD__<slug>.md`. Read only the relevant task file(s); do not load the whole `.memories/` tree into context. If several handoffs are open, list them and let the user pick.
  - If the handoff is stale or its branch is merged/gone, ask before resuming.
  - Treat auto-loaded `AGENTS.md` / `CLAUDE.md` as the normal source for durable instructions; use `/mem-recall` for short-term logs, and inspect durable files only when their loaded content seems incomplete or exact wording matters.
- [ ] **Capture**
  - Before writing task state, apply [references/security.md](references/security.md) and [references/session-handoff.md](references/session-handoff.md).
  - **Capture gate — write only if it passes.** Ask: would a fresh agent be wrong, blocked, or materially slower without this note? If not, write nothing. Capturing nothing is a valid and common outcome; never log just to fill the step.
  - **Never capture (avoids running-log noise):** routine successful steps, restatements of the task or request, or anything already recoverable from code, tests, `git log`, docs, or external trackers (e.g., GitHub/GitLab Issues). If a suitable external tracker is available, ask the user whether to open an issue instead of logging it.
  - At milestones, blockers, quota/context limits, or session boundaries, write or update the task's handoff file `.memories/handoffs/YYYY-MM-DD__<slug>.md` (date = creation day; `<slug>` an agent-chosen name fitting the task). Keep it a single live delta — update the file in place, do not stack entries — holding only what a fresh agent would need to continue: goal, progress, verification, next actions, blockers/assumptions, and suggested skills.
  - Reference existing artifacts by path or URL instead of duplicating contents.
  - Treat the handoff file as transient active state: not a `[Candidate]`, not promotable directly, and deleted on completion rather than promoted into durable memory.
  - Log verified durable insights to today's log (`.memories/YYYY-MM-DD.md` locally or `memories/` globally) as `[Candidate]` entries **with a daily time stamp** (e.g., `[HH:MM]`). A `[Candidate]` must generalize beyond the current task — good: a reusable convention, a non-obvious environment constraint, a gotcha that will recur; bad: one-off task progress or a past fix (that is `[Handoff]` or git history).
- [ ] **Sync**
  - Use `/mem-sync` for project daily-log Git operations. Its `mem-sync-git.sh status` and `diff` commands are read-only checks for local/remote `.memories/` differences.
  - Pull before reading remote handoffs; push at session end or after promotion/capture changes that should be available on other devices.
- [ ] **Manual Governance**
  - Delegate promotion/prune to `/mem-promote`; delegate expired logs and conflict copies to `/mem-clean`. Do not delete or rewrite history from `mem-auto`.
- [ ] **Closure**
  - When the task is achieved and verified, delete that task's handoff file from `.memories/handoffs/`. Active handoff state is transient — completion removes it; any durable insight should already be captured as a `[Candidate]` note.
