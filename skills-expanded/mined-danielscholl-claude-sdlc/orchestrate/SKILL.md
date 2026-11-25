---
name: orchestrate
description: |
  Runtime orchestration of agent teams for parallel work. Use when the user says "create a team",
  "/orchestrate", or wants multiple Claude instances working together. Supports patterns: review
  (parallel code review), debate (competing hypotheses), plan (explore + plan + critique),
  build (parallel implementation), research (parallel investigation),
  cross-agent (multi-engine comparison via CLI bridges like Codex), and custom teams.

  This skill handles live team coordination at runtime — distinct from cadre:init which
  bootstraps static team definitions and agent configurations for a project.

  TRIGGERS - Use this skill when user says:
  - "/orchestrate review src/" or "review this code with a team"
  - "/orchestrate debate 'why does X fail'" or "investigate this bug with competing theories"
  - "/orchestrate plan 'add authentication'" or "plan this feature with a team"
  - "/orchestrate build 'calculator module'" or "build this with a team"
  - "/orchestrate research 'compare React vs Vue'" or "research this topic in parallel"
  - "/orchestrate cleanup" or "shut down the team"
  - Any request to create an agent team or coordinate multiple Claude instances
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, Teammate, SendMessage, TaskCreate, TaskUpdate, TaskList
---

# Agent Team Skill

Orchestrate teams of Claude Code sessions for parallel work. Parse user input to determine
the pattern and target, then execute the appropriate team workflow.

## Input Parsing

Parse `$ARGUMENTS` to determine:
1. **Pattern**: first word (review, debate, plan, build, research, custom, cleanup)
2. **Target**: remaining text (file path, description, or quoted string)

If no pattern is recognized, ask the user which pattern to use.

## Prerequisites Check

Before creating any team, verify the environment:
```bash
echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS
```
If not `1`, tell the user to enable it and stop.

## Pattern Workflows

Each pattern follows the same lifecycle:
1. Create team with `Teammate(spawnTeam)`
2. Create tasks with `TaskCreate`
3. Spawn teammates with `Task` tool (team_name + name params)
4. Monitor progress via `TaskList` and incoming messages
5. Synthesize results when all teammates report back
6. Shutdown and cleanup

For pattern-specific teammate prompts, task structures, and configurations,
see [reference/patterns.md](reference/patterns.md).

## Teammate Prompt Template

Every teammate prompt MUST include these steps (learned from testing):

```
You are "{name}", a {role} on the {team-name} team.

Your task: {specific task description with file paths}

Steps:
1. Check TaskList and claim task #{n} (set owner to your name, mark in_progress)
2. {Pattern-specific work steps}
3. Mark task #{n} as completed
4. Send a message to the team lead with a brief summary of your findings
```

For debate/plan patterns, add:
```
5. Send messages to {other teammates by name} to {challenge/review/discuss} their findings
```

## Model Selection

Default to `sonnet` for teammates to manage token costs. Use `opus` only when the user
explicitly requests it or the task requires deep reasoning (architecture, complex debugging).

Pass the model parameter when spawning: `model: "sonnet"` in the Task tool call.

## Shutdown Sequence

Reliable shutdown (handles the known flaky behavior):

1. Send `shutdown_request` to each teammate via SendMessage
2. Wait for `shutdown_approved` messages (up to 30 seconds)
3. If a teammate doesn't respond:
   - Send a direct message nudging them to shut down
   - Send another `shutdown_request`
4. Run `Teammate(cleanup)`
5. If cleanup fails with "active members":
   - Run `rm -rf ~/.claude/teams/{team-name} ~/.claude/tasks/{team-name}`
   - Inform the user that manual cleanup was needed

## Cleanup Command

When `$ARGUMENTS` is "cleanup":
1. Run the shutdown sequence above for all active teammates
2. Report what was cleaned up

## Error Handling

- If `spawnTeam` fails with "already leading team": run `Teammate(cleanup)` first, retry
- If a teammate gets stuck: send Escape hint to user, offer to spawn replacement
- If tasks appear stuck: check if work is done, manually update task status

## Cost Warning

Before spawning teams with 4+ teammates, warn the user:
"This will spawn {N} teammates, each using its own context window. Token usage scales
linearly with team size. Proceed?"
