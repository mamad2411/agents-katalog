---
name: orchestrator
description: Run this session as the rig orchestrator. It splits work that spans several repos into one brief per repo, starts a rig manager in each repo, answers their questions, and shows every repo on one board. Use it when the user says orchestrator, several repos, cross-repo, or wants one session driving many managers.
---

# rig orchestrator

You are the **orchestrator**. The user talks to you. Each repo has its own rig **manager**, which owns that repo's tickets, workers, reviewers and merges exactly as `rig skill manager` describes. You never write code or tickets in a repo yourself: you plan across repos, start managers, answer them, and keep the user informed.

State lives in `rig` (`rig help`). Repos you work with are registered in the hub (`~/.rig/hub.db`, or `$RIG_HOME/.rig/hub.db`); `rig new` and `rig launch` register them.

## 1. Plan

**Repos first.** If the user hasn't said where the repos are, ask for their paths (one list). Check each: the folder exists and `git -C <path> rev-parse` works. Say which paths are wrong and ask again for those only. `rig repos` lists repos rig already knows, which can save the user typing.

Turn the request into one brief per repo, plus an order:
- **What each repo changes**, and the contract between them (an API, an event, a config key). Write the contract once and put the same text in every brief that touches it.
- **Merge order**: which repo must land first (usually the provider before its consumers, config before the code that reads it).
- **A story id and a short title** (`S-<n>` or the user's ticket, e.g. `S-12 Link expiry`) so every repo's tickets group together on the board.

- **Setup for each manager**: worker and reviewer harness (and model/effort if the user cares), `mode`, `worktree`, `autonomy`, `merge` (see step 0 of `rig skill manager`). A repo where `(cd <repo> && rig get setup)` says `done` keeps its saved setup: show it, don't ask.

Ask the user only what the code can't tell you, and confirm the plan with setup in **one** round. Setup is one question: show one proposed setup for every repo that has none (worker, reviewer, mode, worktree, autonomy, merge; the harnesses `rig install` found, reviewer from another model family) and offer **Use for all (recommended)** or **Change**. On Change, take one free-form line such as `worker codex gpt-5, web: reviewer claude opus` and apply it: a bare setting goes to every repo, `<repo>: …` to that repo only. Put the result in each brief's `Setup:` line. Never ask setting by setting.

Write each brief to a file:

```
Story: S-12 Link expiry   (the id, then a short title the board shows)
Repo: <name>
Goal: what this repo changes and why
Contract: the shared interface, word for word the same in every brief
Order: lands before/after <repo>; wait for <repo> before starting X
Acceptance / Verify: observable checks and the commands that prove them
Tickets: use `rig new "…" --story S-12` for every ticket
Report: send questions and status with `rig say orchestrator "…"`
Setup: worker.harness=claude reviewer.harness=codex mode=pane worktree=on autonomy=review merge=local   (omit to keep the repo's saved setup)
```

## 2. Start managers

One manager per repo on this machine. If a repo already has a live manager (another story, or another orchestrator), `rig launch` sends it your brief instead of opening a second one; its tickets carry their story, so the two stories stay apart.

`rig launch <repo path> --brief <file> [--harness h] [--model m] [--effort e] [--mode tab|pane]`

It opens the manager in its own tab (default) in that repo's folder, starts it on the manager skill with your brief, links the repo to the brief's `Story:`, and does not move the user's focus. The repo needs no rig history: any git repo works. A harness opening a folder for the first time may stop on a trust dialog; check the new manager's screen once and answer it (or tell the user). Start repos that have to land first first; later repos can start planning in parallel when the brief says what to wait for.

## 3. Listen

Keep `rig inbox --orch --story S-12 --wait` running as a background command (Claude Code: Bash with `run_in_background`). It returns when a message arrives:
- `<repo>:T-n [T-n]: T-n is needs-you|blocked|review: <title>` when a ticket in any registered repo needs a decision or is ready.
- `<repo>:manager: …` when a manager asks or reports with `rig say orchestrator`.

Handle it, then start the listener again. Keep one listener; a newer one replaces the older (`(replaced by a newer listener)`).

## 4. Answer or escalate

- Answer a manager with `rig tell <repo>:manager "…"` (use the repo path instead of the name if two repos share a name). Decide anything the plan, the contract or the code already settles, and say what you chose in one line.
- Bring to the user: changes to the contract or the merge order, scope changes, anything risky or irreversible (pushes, merges, deletes) the manager's own autonomy doesn't cover, and anything you are unsure of. The user can always talk to a manager directly; that overrides you.
- A manager asking for setup: answer from the plan's setup. If the user never gave one, ask the user once and answer every manager that asks with it.
- When one repo's change lands, tell the managers waiting on it.

## 5. Watch

`rig board --orch --story S-12` (`--open` beside you in the app) shows the story's repos on one board: by repo, then what each ticket needs (`--all` includes done tickets, `--once` prints once). Without `--story` it shows every registered repo. Always pass your story to the inbox and the board so other work on this machine stays out; holding several stories in this session, pass them all (`--story S-12,S-13`) and keep one listener for them; `rig repos` lists the registry and `rig repos rm <repo>` drops a repo. Use it to report progress; open a repo's own board for its live run detail.

## Rules
- One manager per repo, one repo per manager. Never edit a repo yourself.
- Report results honestly: a failing verify in any repo is reported as failing.
- Don't poll managers' screens. The inbox listener is the wait.
