---
name: swarm
description: "Spawn and orchestrate parallel coding agents (Codex, Claude Code, Gemini) for software development tasks. Use when: (1) building new features, (2) fixing bugs, (3) parallel work on independent tasks, (4) any coding task on project repos. NOT for: simple one-line edits, reading/reviewing code, non-coding tasks, or work in ~/clawd workspace."
metadata:
  { "openclaw": { "emoji": "🐝" } }
---

# Agent Swarm Orchestration

You are the **orchestrator**. You hold all business context (memory, project history, customer needs, architecture decisions). Coding agents hold only code context. Your job is to bridge the gap.

## The Workflow

### Step 1: Scope with the user
When the user describes what they want, **discuss it first**. Don't jump to spawning. Ask clarifying questions if needed. Reference what you know from MEMORY.md, project docs, and prior conversations. Agree on scope and acceptance criteria together.

### Step 2: Enrich context
Before writing the agent prompt, gather everything the agent will need:
- Read relevant source files from the repo
- Check existing patterns (how similar features were built)
- Pull schema/API context if needed
- Review the repo's AGENTS.md / CLAUDE.md for repo-specific conventions
- Check `~/Projects/antigravity-awesome-skills/skills/` for relevant skill patterns

### Step 3: Write the prompt
Translate business context + technical context into a precise, self-contained prompt. The agent should be able to complete the task **without asking questions**. Include:
- What to build (specific, unambiguous)
- Where the relevant code lives (file paths)
- Acceptance criteria
- Constraints (TDD required, don't touch X, follow existing patterns)
- Why this matters (business context that helps the agent make judgment calls)

### Step 4: Spawn
Choose agent(s) and spawn:

```bash
~/.clawdbot/spawn-agent.sh \
  <task-id> \
  <repo-path> \
  <branch-name> \
  <agent: codex|claude|gemini> \
  <model> \
  <thinking: low|medium|high|xhigh> \
  "<prompt>"
```

**Which agent:**

Codex is the **primary workhorse** — most tasks go here. Claude Code and Gemini are specialists.

| Agent | Model | Flags | Best For |
|---|---|---|---|
| **codex** | `gpt-5.4` | `--dangerously-bypass-approvals-and-sandbox`, `model_reasoning_effort=high` | Default for most tasks. Fast, autonomous, great at JS/TS/Python. Use for feature implementation, bug fixes, CRUD, API endpoints, UI components. The bulk of your swarm. |
| **claude** | `claude-opus-4-7` | `--dangerously-skip-permissions -p` | Complex architectural work, security-sensitive code, nuanced refactors where judgment matters. Use opus for critical/production code, sonnet for standard work. Better at understanding existing patterns and maintaining consistency. |
| **gemini** | `gemini-2.5-pro` | `--yolo -p` | Large codebase analysis, broad multi-file refactors, tasks requiring huge context windows. Good when you need to read and understand a lot of code before making changes. |

**Selection heuristic:**
1. Can Codex handle this? Or is it related to the backend?  → **Codex** (default, ~60-70% of tasks)
2. Is it security/auth/complex architecture? Or is it a UI/UX/Frontend problem? → **Claude**
3. Does it need massive context or cross-cutting analysis? → **Gemini**
4. Not sure? → **Codex** first, respawn with Claude if it fails

**Parallel swarm pattern (from the diagram):**
We can run multiple Codex agents in parallel (Agent 1, 2, 3...) for independent features, with Claude Code and Gemini as single specialist agents. The typical swarm is 3-5 Codex + 1 Claude or Gemini when needed.

**How many:**
- Trivial → edit directly, no agent
- Single feature → 1 agent
- Independent parallel tasks → 1 agent each (max 5-7 simultaneous)

Tell the user what you're spawning and why.

### Step 5: Monitor & steer

**Enable the swarm monitor cron when spawning agents:**
```
cron(action='update', jobId='04380832-9e24-48ba-af0c-439c42c0c4df', patch={enabled: true})
```
This runs every 3 minutes, announces completions to the maintainer, and **auto-disables itself** when all tasks are done/failed. Zero token waste when idle.

You can also manually check:

```bash
# Check all agents
bash ~/.clawdbot/check-agents.sh

# View agent output
tail -f ~/.clawdbot/logs/<task-id>.log

# Steer mid-task (redirect without killing)
tmux send-keys -t agent-<task-id> "Stop. Focus on X first." Enter

# Kill if needed
tmux kill-session -t agent-<task-id>
```

### Step 6: Report
When agents complete, review the PR and report to the user. Include what was built, what tests were added, and whether CI passed.

## Infrastructure Reference

| Item | Path |
|---|---|
| Spawn script | `~/.clawdbot/spawn-agent.sh` |
| Monitor script | `~/.clawdbot/check-agents.sh` |
| Cleanup script | `~/.clawdbot/cleanup-task.sh` |
| Task registry | `~/.clawdbot/active-tasks.json` |
| Logs | `~/.clawdbot/logs/<task-id>.log` |
| Worktrees | `<repo>/.worktrees/<branch>/` |
| Global agent instructions | `~/.clawdbot/AGENTS.md` |
| Skills library | `~/Projects/antigravity-awesome-skills/skills/` |

## Repo Paths

Configure your repo paths in `~/.clawdbot/.env` via `CLAWDBOT_PROJECTS_ROOT` and `CLAWDBOT_REPO_MAP`.

## Branch Naming
- `feat/<short-description>`, `fix/<short-description>`, `refactor/<short-description>`

## Rules
1. **Never spawn agents in `~/.openclaw/workspace/`**
2. **Never overwrite repo-specific AGENTS.md or CLAUDE.md**
3. **Always scope with the user first** — don't auto-spawn on vague requests
4. **Fetch latest main** before creating worktrees
5. **Report what you're spawning** — task, agent, repo, branch
6. **Max 5-7 concurrent agents** on DGX
7. **PATH must include** `~/.nvm/versions/node/v24.13.0/bin`

After PR is merged: `~/.clawdbot/cleanup-task.sh <task-id>`
