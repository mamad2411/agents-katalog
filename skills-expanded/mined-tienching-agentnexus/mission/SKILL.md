---
name: mission
description: "Autonomous mission execution system. Decomposes complex goals into milestones with DAG-scheduled tasks, role-based agents (planner/coder/reviewer/tester), and milestone validation. Use when the user describes a complex multi-step task that needs structured decomposition."
---

# Mission System (Autonomous Goal Execution)

You are a **Mission Controller**. You can decompose complex goals into structured plans with milestones, tasks, and role-based agents, then execute them autonomously with DAG scheduling.

> **When to use missions vs tasks:**
>
> | Scenario | Use |
> |----------|-----|
> | Single task, one agent | `orchestrator` skill |
> | Quick parallel tasks, flat structure | `orchestrator` skill (with `plan`) |
> | Complex goal needing decomposition | **`mission` skill** |
> | Multi-phase work with milestones | **`mission` skill** |
> | Need code review + testing built in | **`mission` skill** |

## Context Management Rules

Missions can produce extensive output. To avoid context blowup:

1. **Use `status`** — get compact progress summary (milestones + tasks + timing)
2. **Use `list`** — get 1-line-per-mission overview
3. **Use `log --tail N`** — only last N log entries
4. **Never dump full logs** — always use `--tail`
5. **Don't poll too frequently** — missions take minutes/hours, check every 2-5 minutes

---

## Tool: Mission CLI Script

All operations use the same script with subcommands:

```bash
python3 prompts/skills/mission/scripts/mission.py <command> [options]
```

---

## Commands Reference

### `plan` — Decompose Goal into Structured Plan

Generate a mission plan without executing. The user reviews the plan before approval.

```bash
python3 prompts/skills/mission/scripts/mission.py plan "Implement JWT auth with refresh tokens" \
  --workspace ~/Projects/api
```

Output shows milestones, tasks, roles, and dependencies. Status will be `planned`.

### `start` — Plan + Auto-Approve + Execute

Skip the review step — plan and immediately begin execution:

```bash
python3 prompts/skills/mission/scripts/mission.py start "Add comprehensive test suite" \
  --workspace ~/Projects/myapp
```

### `approve` — Approve a Planned Mission

After reviewing a plan, approve it to start execution:

```bash
python3 prompts/skills/mission/scripts/mission.py approve msn-a1b2c3d4
```

### `status` — Mission Progress

Get detailed progress with milestones, tasks, timing, and cost:

```bash
python3 prompts/skills/mission/scripts/mission.py status msn-a1b2c3d4
```

### `list` — List All Missions

Compact overview of all missions:

```bash
python3 prompts/skills/mission/scripts/mission.py list
python3 prompts/skills/mission/scripts/mission.py list --include-completed
```

### `cancel` — Cancel a Mission

```bash
python3 prompts/skills/mission/scripts/mission.py cancel msn-a1b2c3d4
```

### `pause` — Pause a Running Mission

```bash
python3 prompts/skills/mission/scripts/mission.py pause msn-a1b2c3d4
```

### `resume` — Resume a Paused Mission

```bash
python3 prompts/skills/mission/scripts/mission.py resume msn-a1b2c3d4
```

### `log` — View Mission Log

```bash
# Last 10 entries (recommended)
python3 prompts/skills/mission/scripts/mission.py log msn-a1b2c3d4 --tail 10

# All entries (use sparingly)
python3 prompts/skills/mission/scripts/mission.py log msn-a1b2c3d4
```

---

## Workflow Pattern

### Standard: Plan -> Review -> Approve -> Monitor -> Report

```bash
# 1. Decompose the goal
python3 .../mission.py plan "Implement user authentication with OAuth2" --workspace ~/Projects/api

# 2. Show the plan to the user, explain milestones and tasks
#    (The plan output includes milestone/task breakdown)

# 3. User approves -> start execution
python3 .../mission.py approve msn-XXXXXX

# 4. Monitor progress (every 2-5 minutes)
python3 .../mission.py status msn-XXXXXX

# 5. When complete, report the summary to the user
```

### Quick Start (trusted goals)

```bash
# Plan + execute in one step
python3 .../mission.py start "Refactor database layer to use connection pooling" --workspace ~/Projects/api

# Monitor
python3 .../mission.py status msn-XXXXXX
```

---

## Mission Structure

A mission consists of:

- **Milestones** — logical phases (e.g., "Setup", "Implementation", "Testing")
  - Milestones can depend on other milestones (DAG scheduling)
  - Each milestone has validation criteria and commands
- **Tasks** — individual work items within milestones
  - Each task has a **role**: `planner`, `coder`, `reviewer`, `tester`
  - Tasks can depend on other tasks within the same milestone
  - Tasks run in parallel when dependencies allow
- **Roles** — specialized agent behavior:
  - `planner`: Analyzes requirements, designs architecture
  - `coder`: Implements code changes
  - `reviewer`: Reviews code for quality and correctness
  - `tester`: Writes and runs tests

---

## Rules

1. **Always plan first** — use `plan` to generate the decomposition before executing
2. **Show plan to user** — always present the plan and ask for confirmation before `approve`
3. **Don't poll too frequently** — missions take minutes to hours; check every 2-5 minutes
4. **Use `--tail` on logs** — never dump full mission logs into context
5. **Report milestones** — when a milestone completes, report it to the user
6. **Handle failures** — if a mission fails, check the status and log for details before retrying

---

## Error Handling

| Error | Cause | Action |
|-------|-------|--------|
| `[ERROR] Mission not found` | Invalid mission ID | Check with `list` |
| `[ERROR] Import failed` | nexus not installed | Install with `pip install -e ../nexus` |
| `[ERROR] Mission not in planned status` | Already running/completed | Check `status` first |
| `[ERROR] API key not set` | Missing OPENAI_API_KEY | Set env var |

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | (required) | LLM API key |
| `OPENAI_API_BASE` | (OpenAI default) | API base URL |
| `NEXUS_MODEL` | `gpt-4o` | Default model for task execution |
| `NEXUS_WORKSPACE` | `~/Projects` | Default workspace directory |
