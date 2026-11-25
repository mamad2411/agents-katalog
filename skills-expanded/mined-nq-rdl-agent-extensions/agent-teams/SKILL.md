---
license: CC-BY-4.0
description: >-
  Design and run Claude Code agent teams: parallel teammates with a shared task
  list who message and challenge each other. Use when the user asks for a team
  or teammates, wants parallel reviewers or investigators who debate findings,
  asks whether to use a team or subagents, or mentions teammate mode, team lead,
  or CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS.
argument-hint: "Describe the work to parallelize (e.g., 'review PR #42 for security and performance')"
compatibility: >-
  Requires Claude Code v2.1.178+ (implicit per-session team; TeamCreate and
  TeamDelete removed; teams first shipped in v2.1.32) with
  CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 and an interactive session. Split-pane
  mode requires tmux or iTerm2 with the it2 CLI. Checked against the
  agent-teams docs with Claude Code 2.1.284 on 2026-09-29.
user-invocable: true
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

## User Input

```text
$ARGUMENTS
```

When the user invokes `/agent-teams`, design an agent team for their request.
If `$ARGUMENTS` is empty, ask the user what work they want to parallelize.

Follow the **Team Design Workflow** below to produce a ready-to-execute team
plan, then offer to create the team.

---

## Team Design Workflow

When designing a team, follow these steps:

1. **Understand the work** — what is the user trying to accomplish?
2. **Identify parallel lanes** — which parts can run independently?
3. **Choose team vs subagents** — see [references/subagent-vs-team.rst](references/subagent-vs-team.rst) for the decision flowchart. Only recommend a team when teammates genuinely need to communicate with each other or coordinate via shared tasks.
4. **Size the team** — start with 3-5 teammates. More than 6 is rarely justified.
5. **Define roles and ownership** — each teammate needs a clear name, responsibility, and file ownership boundaries to prevent overwrites.
6. **Set dependency order** — which teammates must share interfaces before others can proceed?
7. **Choose display mode** — `in-process` (default, one terminal) or a split-pane mode (`auto`, `tmux`, `iterm2`); see *Display modes*.
8. **Consider quality gates** — recommend `TeammateIdle`, `TaskCreated`, or `TaskCompleted` hooks where appropriate.

### Output Format

Present the team design as:

```
## Team plan: <short title>

**Goal**: <one-sentence description>

### Teammates

| # | Name | Role | Owns | Model |
|---|------|------|------|-------|
| 1 | ... | ... | ... | ... |

### Dependency Order
<which teammate feeds into which>

### Prompt
<the natural-language prompt the user should give Claude to create this team>

### Configuration
<any settings needed — env vars, display mode, permissions>
```

See [references/examples.rst](references/examples.rst) for complete team
configurations across common workflows.

---

# Agent Teams — Parallel Claude Code Coordination

## Overview

Agent teams coordinate multiple independent Claude Code instances working in
parallel. One session acts as the **team lead**, coordinating work, assigning
tasks, and synthesizing results. **Teammates** work independently, each in its
own context window, and communicate directly with each other.

This is fundamentally different from subagents. Read
[references/subagent-vs-team.rst](references/subagent-vs-team.rst) for the full
comparison — it matters because choosing the wrong one wastes tokens or limits
capability.

## Prerequisites

Agent teams are **experimental and disabled by default**. Before using them:

1. Enable the feature flag
2. Verify the configuration is correct

### Enable agent teams

Add to your project or user `settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

**Settings file locations** (highest precedence first, below managed settings
and CLI flags):
- Project local: `<project>/.claude/settings.local.json`
- Project: `<project>/.claude/settings.json`
- User: `~/.claude/settings.json`

### Verify or toggle configuration

Run the bundled script from the project root (it needs `jq`). It reads the
settings files in precedence order and reports the effective value; a value
in any settings file overrides a shell export:

```bash
# Check current status
bash "${CLAUDE_SKILL_DIR}/scripts/check-config.sh"

# Enable agent teams (sets the flag to "1" in user settings; add --project for .claude/settings.json)
bash "${CLAUDE_SKILL_DIR}/scripts/check-config.sh" --enable

# Disable agent teams (sets the flag to "0")
bash "${CLAUDE_SKILL_DIR}/scripts/check-config.sh" --disable
```

## When to Use Teams (Not Subagents)

Teams add real value when:

- **Teammates need to talk to each other** — subagents report back to the
  parent; teammates share a task list, message each other, challenge findings,
  and converge on answers together
- **Work benefits from parallel exploration** — multiple independent agents
  investigating different angles of a problem simultaneously
- **Tasks are large and independent** — each teammate owns a distinct piece
  of work (different files, modules, or domains)
- **You want competing hypotheses** — agents actively try to disprove each
  other's theories, like a scientific debate

Teams are **NOT** the right choice when:

- Tasks are sequential (A must finish before B starts)
- Multiple agents would edit the same files (causes overwrites)
- You just need a quick focused worker that reports back (use subagent)
- The coordination overhead exceeds the benefit of parallelism

## How to Create a Team

Tell Claude what you want in natural language. Be specific about roles:

```text
Create an agent team to review PR #142. Spawn three reviewers:
- One focused on security implications
- One checking performance impact
- One validating test coverage
Have them each review and report findings.
```

Every session has one implicit team (v2.1.178+); Claude spawns teammates
directly with the Agent tool's `name` — there is no team-creation step.

While teams are enabled, any subagent that Claude names launches as a
teammate, so a team can form during ordinary delegation. Set
`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` to `"0"` to get subagents back. Teammates
are never spawned in `-p` mode or Agent SDK sessions; named subagents run as
ordinary subagents there.

### Team sizing guidance

| Team size | Best for |
|-----------|----------|
| 3 | Focused tasks: review, investigate, prototype (the usual start) |
| 4-5 | Complex features: frontend + backend + tests + docs |
| 6+ | Rarely justified — coordination overhead dominates |

Aim for **5-6 tasks per teammate** to keep everyone productive. If you have
15 independent tasks, 3 teammates is a good starting point.

### Display modes

| Mode | Setting | When to use |
|------|---------|-------------|
| `in-process` | Default | All teammates in one terminal; select them in the agent panel. |
| `auto` | Opt-in | Split panes when already in tmux (or iTerm2 with `it2`), in-process otherwise. |
| `tmux` | Requires tmux or iTerm2 | Each teammate gets its own pane. |
| `iterm2` | Requires the `it2` CLI | iTerm2 native split panes. |

Set `teammateMode` in `~/.claude/settings.json`:

```json
{
  "teammateMode": "auto"
}
```

Or per session: `claude --teammate-mode auto` (an experimental flag, hidden from `--help`).

### Specify teammates and models

Claude decides the number of teammates based on your task, or you can specify:

```text
Create a team with 4 teammates to refactor these modules in parallel.
Use Sonnet for each teammate.
```

### Require plan approval for teammates

Put the lead in plan mode before spawning; the teammate then works read-only
until its plan is ready:

```text
Spawn an architect teammate to refactor the authentication module.
```

Claude Code approves the teammate's plan as soon as it arrives, **without the
lead reviewing it** — plan mode is not a review gate. The teammate's edits and
commands still go through permission prompts in the lead session.

### Use subagent definitions for teammates

Reference a subagent type from the project, user, or managed scope when
spawning a teammate. The teammate gets the definition's `tools` and `model`, and
its body (appended to the default prompt in-process, replacing it in split
panes). The definition's `skills` are not applied, and `mcpServers` apply only
to split-pane teammates:

```text
Spawn a teammate using the security-reviewer agent type to audit the auth module.
```

## Interacting with Teams

### Message teammates directly

- **In-process mode**: select a teammate in the agent panel with the up/down
  arrows, press Enter to view its session and type to message it; Escape
  interrupts, `x` stops it, Ctrl+T toggles the task list.
- **Split-pane mode**: Click into a teammate's pane

### Task coordination

The shared task list coordinates work. Tasks have three states:
`pending` -> `in progress` -> `completed`. Tasks can have dependencies —
a pending task with unresolved dependencies cannot be claimed.

The lead can assign tasks explicitly, or teammates can self-claim the next
unassigned, unblocked task after finishing their current one. Task claiming uses
file locking to prevent race conditions.

### Quality gates with hooks

Three hooks enforce quality:

- **`TeammateIdle`**: runs when a teammate is about to go idle. Exit code 2
  sends feedback and keeps the teammate working.
- **`TaskCreated`**: runs when a task is being created. Exit code 2 prevents
  creation and sends feedback.
- **`TaskCompleted`**: runs when a task is being marked complete. Exit code 2
  prevents completion and sends feedback.

### Shut down and clean up

```text
Ask the researcher teammate to shut down
```

There is no separate team cleanup step: the team config directory is removed
when the session ends, and the task list persists for resumed sessions.

## Architecture

| Component | Role |
|-----------|------|
| **Team lead** | Main session; its implicit team exists from startup; spawns and coordinates teammates |
| **Teammates** | Separate Claude Code instances working on assigned tasks |
| **Task list** | Shared work items at `~/.claude/tasks/{team-name}/` |
| **Mailbox** | Inter-agent messaging system |

Team config lives at `~/.claude/teams/{team-name}/config.json` (auto-generated,
do not edit by hand — runtime state is overwritten on each update). The team
name is `session-` plus the first eight characters of the session ID.

### Context rules

- Teammates load project context (CLAUDE.md, MCP servers, skills) automatically
- Teammates do **NOT** inherit the lead's conversation history
- The lead's spawn prompt is the only initial context
- Include task-specific details in spawn prompts (file paths, constraints)

### Permissions

Teammates start with the lead's permission mode, except `dontAsk`, which they
do not inherit; if the lead skips permissions, so do all teammates. Their
permission prompts surface in the lead session. Pre-approve common operations
to reduce interruptions:

```json
{
  "permissions": {
    "allow": [
      "Read", "Glob", "Grep",
      "Bash(git *)",
      "Bash(npm test *)",
      "Bash(go test *)"
    ]
  }
}
```

### Token usage

Agent teams use significantly more tokens than a single session. Each teammate
has its own context window, and usage scales linearly with active teammates.
For research, review, and new feature work, the extra tokens are usually
worthwhile. For routine tasks, a single session is more cost-effective.

## Common Issues

| Issue | Fix |
|-------|-----|
| Teammates not appearing | Look in the agent panel (idle rows hide or collapse); check task was complex enough |
| Too many permission prompts | Pre-approve common operations in permission settings |
| Teammates stopping on errors | Message them directly with additional instructions |
| Lead implements instead of delegating | Say "Wait for teammates to complete before proceeding" |
| Task status lagging | Check manually; tell lead to nudge the teammate |
| Orphaned tmux sessions | `tmux ls` then `tmux kill-session -t <name>` |

## Limitations (Experimental)

- No session resumption for in-process teammates (`/resume` and `/rewind` do not restore them)
- One implicit team per session; you can't create additional teams
- No nested teams (teammates cannot spawn their own teams)
- Lead is fixed for the lifetime of the team
- Split panes require tmux or iTerm2 (not VS Code terminal, Windows Terminal, Ghostty)
- Behaviour here assumes v2.1.178+ — see `compatibility` and verify against
  <https://code.claude.com/docs/en/agent-teams> when being wrong would mislead

## References

- [references/subagent-vs-team.rst](references/subagent-vs-team.rst) — detailed
  comparison with decision flowchart
- [references/examples.rst](references/examples.rst) — complete team
  configurations for common workflows

## Skill Commands

| Command | Description |
|---------|-------------|
| `bash scripts/check-config.sh` | Check if agent teams are enabled |
| `bash scripts/check-config.sh --enable` | Enable agent teams in user settings |
| `bash scripts/check-config.sh --disable` | Set the flag to "0" in user settings |
