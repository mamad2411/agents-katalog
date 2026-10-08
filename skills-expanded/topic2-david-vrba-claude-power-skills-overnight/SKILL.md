---
name: overnight
description: Schedule the current task to run unattended overnight (default 2 AM) via headless `claude -p`, isolated on a git branch, with results auto-surfaced in your next morning session. Use when the user says "do this at 2am", "run this while I sleep", or "queue this for tonight".
---

# Overnight runner

Captures **the task being discussed right now**, schedules a Windows Task
Scheduler job that runs `claude -p` headless at the chosen time (the machine
wakes itself), and writes a result that the morning session shows automatically.

Files: scripts live in `~/.claude/overnight/bin/`. You orchestrate; the
PowerShell does the work.

## Steps

### 1. Settle the parameters
Infer from the conversation; ask only if genuinely ambiguous.

- **Schedule → `RunAt`** (local `yyyy-MM-dd HH:mm`). Default **next 02:00**
  (tomorrow if 2 AM already passed today). Parse "in 90m", "tonight", "at 3",
  "tomorrow 04:00" relative to the current date/time in context. Must be in the
  future.
- **Mode**: `build` if the task writes code/files; `research` if it only
  investigates/reads/searches and produces a written report.
- **ProjectDir**: the current working directory (absolute path).
- **MaxTurns**: default 60; raise for large build tasks, lower (1–3) for trivial
  ones.
- **Goal**: one crisp human-readable line (shown in the morning summary).

### 2. Write a self-contained brief
The overnight run starts **fresh** — it sees only this brief plus the project
files, NOT this conversation. So the brief must stand alone. Write it to a temp
file (e.g. `~/.claude/overnight/_brief_tmp.md`) containing:

- **Objective** — what to accomplish.
- **Context** — everything relevant from this conversation: decisions made,
  constraints, paths, prior findings, links.
- **Deliverables** — concrete outputs (files to create/modify, or the report to
  produce).
- **Definition of done** — how the run knows it succeeded.
- **Guardrails** — what NOT to touch. For build tasks, instruct it to **leave
  changes in the working tree and NOT run git commit/push** — the runner commits
  to an isolated branch automatically. Telling it to commit wastes turns and can
  hit the turn limit.

Be generous and explicit — under-specifying is the main failure mode.

### 3. Schedule it
Run (Windows, pwsh):

```
pwsh -NoProfile -File "$HOME/.claude/overnight/bin/new-job.ps1" `
  -Goal "<one line>" `
  -BriefPath "$HOME/.claude/overnight/_brief_tmp.md" `
  -RunAt "2026-01-01 02:00" `
  -Mode build `
  -ProjectDir "<cwd>" `
  -MaxTurns 60
```

Optional: `-Model opus`, `-AllowedTools "Read Edit Write Glob Grep Bash"`,
`-NoWorktree` (build directly in the project with no branch isolation — only if
the user insists).

### 4. Confirm
Relay the script's confirmation block (id, fire time, mode, branch, wake status).
Then delete the temp brief. Tell the user: results appear automatically at the
start of their next session; build work lands on branch `overnight/<id>` (review
with `git checkout`), main untouched.

## Reliability notes (mention only if asked)
- Machine wakes via Task Scheduler `-WakeToRun`; missed starts run on next wake
  (`-StartWhenAvailable`).
- One retry on failure, then a lighter-model fallback on overload; a `result.md`
  is **always** written, even on crash.
- Runs serialized (global mutex) so two jobs never contend.
- Cancel: `Unregister-ScheduledTask 'OvernightClaude-<id>'`.
  List: `Get-ScheduledTask 'OvernightClaude-*'`.
- On subscription plans, headless `claude -p` may draw from a separate Agent SDK
  credit pool — check your plan's current terms before relying on heavy
  unattended runs.
