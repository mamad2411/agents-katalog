---
name: backlog
description: Use when the user asks to record or read the backlog ("put it in the backlog", "note it for later", "let's defer this", "what's in the backlog", "let's go through the backlog") OR when you (Claude) noticed — while working — an unrelated bug or an out-of-scope side task and want, WITH the user's consent, to defer it OR when running autonomously in the background and a task needs the user's decision. Records deferred tasks into docs/backlogs/ and reads them back. Never captures silently on your own; does NOT execute tasks.
---

# Backlog

Single reliable route for deferred tasks. Storage: `docs/backlogs/` in the current
project (the engine resolves the git root automatically). The engine owns the
format — always go through it, never hand-edit files.

Engine: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/backlog.py" <command>`

## When to record — three cases only

**You NEVER capture silently on your own.** Noticing that something diverges a
little from the current task is NOT a trigger. There are exactly three cases where
a backlog entry is created; outside them, do not touch the backlog:

1. **The user tells you to.** Explicit instruction to defer/record: "put it in
   the backlog / note it for later / let's defer this / out of scope for this PR
   — backlog it". Record right away, no re-confirmation.
2. **You noticed something while working — WITH the user's consent.** During the
   task you find either (a) a **bug unrelated to the current task** that cannot or
   should not be fixed in passing this session, or (b) an **out-of-scope side task**
   (refactor, extraction, improvement) beyond what you were asked to do. Do NOT
   record it yourself. Name the finding and **offer three options**: do it now
   (in this session) / record it in the backlog / skip. Write only if they pick
   the backlog; "skip" means drop it. No answer — repeat the offer once, so it
   is not lost by accident; still no answer — drop it.
3. **You are running autonomously and nobody can be asked.** The test is not
   which tool launched you — it is: **can you ask the user right now and get an
   answer before this session ends?** If yes, this is case 2, so ask. If no —
   a headless `claude -p` run, a scheduled run, a phase of a multi-session plan
   runner, a subagent with no interactive user — AND a task genuinely needs a
   decision you cannot make, record it so the decision is not lost. This is the
   ONLY path where you write without an explicit user go-ahead, and it exists
   precisely because no human is here to be asked.

Hypotheticals, passing remarks, and tasks that advance the current goal are not
backlog material. A task that belongs to the **currently open plan** stays in the
plan's own tracking (the active TodoWrite/Task list or the plan-doc checkboxes) —
never mirror it into the backlog.

### How to record (once one of the three cases applies)

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/backlog.py" add \
  --title "<short, precise title>" \
  --priority <low|medium|high> \
  --body "<enough context to resume without re-analysing the code:
what to do, why it was deferred, where — file:line references>"
```

Then tell the user: `recorded in the backlog #N: <title>`.

The body MUST contain enough context to act later without re-reading the whole
codebase — name the files and lines, state the decision and its rationale.

## Discovery / read

- "what's in the backlog" / review → `... backlog.py list` (defaults to open items, sorted
  by priority then age). Show the table.
- Taking an item into work → `... backlog.py show <id>`, then **re-read the actual
  code at the file:line references** before acting (guard against staleness). If
  the item is stale, already done, or no longer makes sense — stop and say so;
  do not execute blindly.
- This plugin does NOT execute tasks. Once you have the item, proceed with the
  user's normal workflow; the user decides batch vs one-by-one.

## Closing and editing

Closing an item **deletes its file** — the backlog holds open work only, and git
keeps the history of what was closed.

- `... backlog.py done <id>` — close as done and delete (you do not auto-close;
  the user decides).
- `... backlog.py cancel <id>` — close as cancelled and delete.
- `... backlog.py update <id> --title ... --priority ... --body ...` — edit fields.
- `... backlog.py prune` — list leftover `status: done|cancelled` entries written by
  plugin versions ≤ 0.4.0; `--yes` deletes them. Never run `--yes` without the
  user's explicit go-ahead. Those legacy entries stay put otherwise and remain
  visible in `list --all`.

## Version control

Files under `docs/backlogs/` are first-class tracked project artifacts, not stray
edits — they hold only task metadata and context (titles, priorities, `file:line`
references), never secrets. **Commit them by default.** When you create, update, or
close a backlog item and then make a commit, stage the changed `docs/backlogs/`
files instead of excluding them as "unrelated to my change" — include them with the
related code change, or as their own `chore(backlog): …` commit when there is no
related code. Do not add `docs/backlogs/` to `.gitignore`.

Stage with `git add docs/backlogs/` (the directory) or `git add -A`, never
`git add docs/backlogs/*.md`: closing an item **deletes** its file, and a shell glob
only expands to files that still exist, so the deletion would silently stay
unstaged. Committing the deletion is also what makes a closed task recoverable —
`docs/backlogs/` outside git means `done`/`cancel` destroy the task text for good.
