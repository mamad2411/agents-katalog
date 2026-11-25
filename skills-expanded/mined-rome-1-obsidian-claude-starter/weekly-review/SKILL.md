---
name: weekly-review
description: Drafts a weekly review in Journal/ from what actually changed in the vault this week (git history, notes updated, meetings held), every unchecked action item, stale active projects, people with overdue follow-ups, inbox leftovers and open feedback-log entries; then helps the user pick next week's focus. Use when the user says "weekly review", "review my week", "what did I do this week", "what's open", "plan next week", or runs /weekly-review.
---

# Weekly review

Build the draft from evidence in the vault, then let the user edit it. Do not invent accomplishments.

## 1. Collect

Default window: the last 7 days. Use these sources, and say in the draft which ones you used:

- **Changes**: `git log --since="7 days ago" --name-only --format="%ad %s" --date=short` if the vault is a git repo; otherwise notes whose `updated:` falls in the window.
- **Meetings**: notes in `Meetings/` dated in the window.
- **Open action items**: unchecked boxes across the vault, excluding templates and examples:
  `grep -rnE --include="*.md" --exclude-dir=".*" "^[[:space:]]*- \[ \]" . | grep -v -e "System/Templates" -e "_examples"`
- **Stale projects**: `status: active` with `updated:` older than 30 days.
- **People**: `next_action` set and `last_contact` older than 30 days.
- **Inbox**: files in `Inbox/` other than `README.md`.
- **Feedback**: lines in `System/agent-feedback.md` still marked `[status: open]`.
- **Beads** (only if `.beads/` exists): `bd ready` and anything closed this week.

A count of zero is a finding only if the search could have found something; if a source was unavailable (no git, no beads), say so instead of reporting zero.

## 2. Draft

Create `Journal/YYYY-Www-Review.md` (ISO week, e.g. `2026-W03`) from `System/Templates/Weekly-Review.md`:

- **What happened**: the main things, grouped by project, with links. Short.
- **Projects**: one line per active project: moved, stalled, or done.
- **Open loops**: action items grouped by project, stale projects, overdue follow-ups, inbox count.
- **Next week's focus**: leave for the user; suggest two or three candidates based on the open loops.
- **Notes on the system**: open feedback entries, plus anything you noticed (a template field nobody fills, a skill that did not fit).

## 3. Review with the user

Show the open loops and ask, in one message:

- Which items are done, dropped, or still on? (Check off or remove them in their source notes, not only in the review.)
- Which stale projects should be paused or archived? (Set `status: paused`, or move to `Archive/`, with a yes.)
- What are next week's two or three priorities?

Then fill in the focus section, set `updated:` on notes you changed, run `python3 scripts/check_vault.py`, and commit if the user agreed to agent commits.
If the inbox is not empty, offer `/inbox-triage`. If feedback entries are open, offer `/log-feedback` to work through them.
