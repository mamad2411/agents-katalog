---
name: agent-kit-team
description: Run a team of Claude Code role agents on a loop, each taking its own GitHub issue in its own worktree and handing work on only through labels and PR comments, so any session (or another tool) can pick it up. The main session is the lead (`/team-tick`, `/loop /team-tick`); workers open draft PRs; a reviewer and, for games, a playtester move them to ready-for-owner; the owner merges. Ships `team.py` (doctor, board, next, claim, release, --selftest). Use WHENEVER the work is "agent team", "agentic loop", "orchestrate agents", "multi-agent workflow on issues", "agents work their own tasks", "lead agent", "hand off between agents", "agent interop", "/team-tick", "ทีม agent", "ให้ agent ทำงานเอง".
---

# Agent team

A long job (a game, an app) split into GitHub issues, worked by role agents in a loop. Taken from a
working setup: five role agents on a Roblox game, with a lead loop in the main session.

## Why it's shaped like this

| Choice | Reason |
|---|---|
| The **lead is the main session**, not an agent | subagents can't spawn subagents (Claude Code docs) |
| **State on GitHub** (labels, PR comments), never in chat | any session, a /loop wake-up or another tool can resume; the owner sees everything |
| **One role, one definition** in `.claude/agents/<role>.md` | `model`, `isolation: worktree`, `skills` (preloaded in full), `maxTurns`, `tools` per role |
| **Worktree per worker** | parallel agents never touch each other's files (Cursor's best practice too) |
| **Draft PR after the first commit** | work is visible from minute one; a stuck agent leaves a trail |
| **Finish line per role** (a command and its output) | an agent with no check loops (`../cost/SKILL.md` rule 3) |
| **Owner merges, never an agent** | the one irreversible step stays human |
| **A deterministic script picks work** (`team.py`) | the same board for every session; testable; no tokens spent sorting issues |

## Setup (once per repo)

1. **Tools first.** List every tool each role needs in `.claude/team.json` → `"needs"`, then run
   `uv run --script <agent-kit>/team/scripts/team.py doctor`. Every `NEED` row is the owner's
   step. Until it's done, the board shows that role's issues as waiting "needs X on this machine".
2. **Config** `.claude/team.json`: `roles` is an ordered label→role list, `needs` is role→tools on PATH, and
   `workers` lists the roles the lead may start on new issues.
3. **Labels:** `agent:<role>` per role; `status:in-progress`, `status:needs-review`,
   `status:changes-requested`, `status:ready-for-owner` (+ `status:needs-playtest`,
   `status:playtesting` for games); `blocked`.
4. **Issues:** one per feature, with a "Done when" checklist and `Depends on #N` lines; milestones
   named `M1 …`, `M2 …` set the order.
5. **Agents:** one file per role from [`references/role-agent.md`](references/role-agent.md).
6. **Lead skill:** copy [`references/team-tick.md`](references/team-tick.md) to
   `.claude/skills/team-tick/SKILL.md` and adjust the roles.
7. **Hooks:** the `../cost` PreToolUse hook on `Agent`; an allowlist for reads, tests and `gh … view|list`.
8. **Restart Claude Code in the repo folder.** Project agents load at session start; a session
   started elsewhere reports "Agent type '<role>' not found".

## Handoff protocol

```
issue (open, no status) ──lead: team.py claim──▶ agent:<role> + status:in-progress
worker: branch → first commit → draft PR "Closes #N" → work to its finish line → label:
   code that runs  ─▶ status:needs-playtest ──playtester──▶ needs-review | changes-requested (+ bug issues)
   everything else ─▶ status:needs-review
status:needs-review ──reviewer──▶ status:ready-for-owner | status:changes-requested
status:changes-requested ──lead──▶ the same role fixes (SendMessage if alive, else a new agent on the PR)
status:ready-for-owner ──owner──▶ merge
stuck twice ──lead: team.py release --blocked──▶ blocked + a comment naming what's needed
```

Stacked PRs (base isn't the default branch) don't get GitHub's closing links, so `team.py` also
reads `Closes #N` from PR bodies. Otherwise their issues look ready, and two agents take the same work.

## Rules for the lead

- At most **2 workers** at once, and **1 playtest** (one Studio or one device). More costs more
  than it saves on small issues (`../cost`).
- Briefs come from `../prompt-cache` `pcache.py brief`: the outline first, the task last, so sibling
  agents share one cached prefix.
- `/loop /team-tick` wakes every ~1200 s while agents run and never waits more than 3600 s (cache TTL).
  **Stop rule:** nothing ready, nothing to review, nothing running → stop the loop and list what needs the owner.
- Spawn only the project's role agents; their model is in their definition.
- The same GitHub account can't approve its own PR: the reviewer **comments** and sets labels.

## Other tools (Cursor, Codex)

The protocol is the interop layer: any tool that can run `gh` and follow a role file can take part.
Rules go in `AGENTS.md` (Claude Code reads it only when there's no CLAUDE.md, so put `@AGENTS.md`
at the top of CLAUDE.md). Skills follow the Agent Skills standard: install with
`npx skills@latest add th3r-dev/th3-skills --skill <name>` or copy to `.cursor/skills/`. A role file's body becomes a
Cursor command or a `codex exec` prompt run in a worktree. It claims with `team.py claim` like
any agent, and the reviewer treats its PR the same.

## Games: an agentic playtester

For Roblox, a `playtester` role plays the PR in Studio through Studio's MCP server and posts a
PASS/FAIL table with screenshots: `../../game-dev/roblox/references/agentic-playtest.md`.

## Check

`uv run --script scripts/team.py --selftest`. A real run is checked by the trail: every handoff shows
as a label change or comment on the issue and PR, with no step that exists only in a chat.
