---
name: aa-help
description: Use when the user asks what Agent-Agile commands exist, wants a command reference or cheat sheet, is unsure which command to run next, or asks how the methodology works, for example "/aa-help", "what commands are there", "how does this system work".
license: MIT
metadata:
  system: agent-agile
---

# aa-help

Read-only. Answer directly from this file — never dispatch a subagent and never read a playbook for this command.

## The funnel

Every project moves through the same funnel, front door to first demo:

`rough idea → grill → intake → plan → panel → prereqs → waves → demo`

## Commands

| Command | Purpose |
|---|---|
| `/aa-grill` | Idea interrogation → IDEA.md (can reject the idea) |
| `/aa-new-project` | 8-question intake → OKRs → epics → Epic 1 stories |
| `/aa-import` | Existing plan: audit → gaps → panel → proceed/reshape/kill |
| `/aa-panel` | Run the critic panel on the current draft plan |
| `/aa-plan-epic` | Slice next epic: contracts scope + story cards + waves |
| `/aa-execute-epic` | Wave 0 → collision check → Wave 1 → Wave 2 |
| `/aa-review` | Present DEMO.md → approve/redo/replan |
| `/aa-autopilot` | Chain all epics; `--gate full-auto\|checkpoint` |
| `/aa-resume` | Read STATE.md, pick up the baton |
| `/aa-status` | Where are we; roadmap + KR progress |
| `/aa-help` | Command guide + methodology crash course |

## The methodology, in five lines

1. Work breaks down OKR → Initiative → Epic → Story and stops there — no level below a story, no story points, no burndown.
2. Every epic's definition of done is one demo sentence: "I can do X and see Y" — if you can't write that sentence, the epic isn't scoped yet.
3. A critic panel attacks the plan before execution, and a human shopping list (`PREREQS.md`) blocks any run that needs a key, account, or service it doesn't have yet.
4. Story cards are sized so a cheap-tier agent can finish one from just its card plus the frozen contracts — zero exploring, zero guessing intent.
5. Every epic ends at a review gate with exactly three outcomes: approve, redo (feedback becomes new acceptance checks, never a vague note), or replan (back to slicing).

If the user names a specific command, point them at it and its one-line purpose from the table above. If they're unsure where to start, point them at the front door that matches what they're bringing: a vague spark → `/aa-grill`, a clear idea → `/aa-new-project`, an existing plan or spec → `/aa-import`.
