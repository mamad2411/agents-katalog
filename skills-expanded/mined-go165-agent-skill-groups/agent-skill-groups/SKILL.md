---
name: agent-skill-groups
description: Manage large local Agent Skills libraries with runtime-aware scenario groups for Codex, Claude Code, OpenCode, GitHub Copilot, and generic SKILL.md roots.
---

# Agent Skill Groups

Use this skill when the user wants to inspect, group, profile, enable, disable,
or clean up local `SKILL.md` directories across agent runtimes.

## Workflow

1. Identify the runtime: `codex`, `claude-code`, `opencode`, or `generic`.
2. Inspect the current skill inventory before moving anything.
3. Generate or load a `groups.json` file.
4. Preview changes with `plan`.
5. Generate persistent agent instructions with `memory`.
6. Create a backup before moving directories.
7. Switch profiles only after the plan is understood.
8. Validate the final filesystem state.

For a safe end-to-end rehearsal, run `agent-skill-groups demo --json` first.
It creates sample active and disabled skill roots, writes `groups.json` and an
agent memory block, switches a profile, restores the backup, and reports
`ok: true` when the reversible workflow succeeds.

## Commands

```bash
agent-skill-groups runtimes
agent-skill-groups demo --json
agent-skill-groups analyze --runtime codex --json
agent-skill-groups suggest --runtime codex --json
agent-skill-groups init --runtime codex --output groups.json
agent-skill-groups status --config groups.json --runtime codex --json --details
agent-skill-groups route --config groups.json --runtime codex --task "solve a web CTF with IDOR" --json
agent-skill-groups route --config groups.json --runtime codex --task-file task.txt --emit-command session-load
agent-skill-groups plan --config groups.json --runtime codex research
agent-skill-groups memory --config groups.json --runtime codex --write AGENTS.md
agent-skill-groups backup --config groups.json --runtime codex
agent-skill-groups profile --config groups.json --runtime codex research
agent-skill-groups validate --config groups.json --runtime codex --json
agent-skill-groups discovery --json
```

Use `AGENT_SKILL_GROUPS_CONFIG` when scripts or hooks need a stable config path.

## Safety

- Do not edit skill contents during grouping.
- Do not delete skills as part of a profile switch.
- Keep `.system` and other protected skills in `core`.
- Prefer `--json` output when another agent or script consumes results.
