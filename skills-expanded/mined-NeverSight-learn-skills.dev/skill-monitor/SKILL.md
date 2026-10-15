---
name: skill-monitor
description: >-
  Monitor local Agent Skill usage, Rules/AGENTS.md context bloat, and Task /
  sub-agent startup cost (starts × system-prompt volume). Use for skill
  frequency, skill token estimates, unused skills, context bloat, AGENTS.md /
  rules size, subagent cost, backfill from transcripts, or project skill
  tracking. Also use for skill 监控, skill 统计, skill 频率, Rules 膨胀,
  AGENTS.md 体积, 子 Agent / Task 成本.
---

# Skill Monitor

Track skill usage, always-on context bloat, and sub-agent startup cost in the
project-local `data/` directory. Capture is best-effort.

## Quick setup

```bash
node .cursor/skills/skill-monitor/scripts/cli.mjs setup --project . --hooks
node .cursor/skills/skill-monitor/scripts/cli.mjs backfill
node .cursor/skills/skill-monitor/scripts/cli.mjs backfill-tasks
node .cursor/skills/skill-monitor/scripts/cli.mjs analyze --project . --write
node .cursor/skills/skill-monitor/scripts/cli.mjs bloat --project . --snapshot --write
node .cursor/skills/skill-monitor/scripts/cli.mjs analyze-tasks --project . --write
```

`setup --hooks` installs:

- `beforeReadFile` → record `SKILL.md` loads
- `subagentStart` + `preToolUse` (Task) → record sub-agent starts with Rules/AGENTS volume

## Commands

| Command | Purpose |
| --- | --- |
| `setup [--hooks]` | Init `data/`; merge Cursor hooks |
| `record --path <SKILL.md>` | Record one skill use |
| `analyze [--write]` | Skill frequency + est. tokens |
| `bloat [--snapshot] [--write]` | Rules / AGENTS.md bloat + budgets |
| `record-task --type <name>` | Record one Task / sub-agent start |
| `analyze-tasks [--write]` | Startup cost: starts × avg prompt volume |
| `backfill` | Skills from Cursor transcripts |
| `backfill-tasks` | Task/subagent starts from transcripts |
| `reestimate` | Refresh skill `estTokens` |
| `list-skills` / `summary` | Discovery / aggregates |

## Data layout

- `data/events.jsonl` — skill loads (`estTokens`)
- `data/summary.json` — skill aggregates
- `data/tasks.jsonl` — sub-agent starts (`systemPromptTokens`)
- `data/context-snapshots.jsonl` — optional bloat history
- `data/report.md` / `bloat-report.md` / `tasks-report.md`

## Agent workflow

1. Skill stats → `analyze --write`
2. Context inflation → `bloat --snapshot --write`
3. Sub-agent cost → `analyze-tasks --write` (after hooks or `backfill-tasks`)
4. Mention limits: estimates are not provider billing; hooks are strongest in Cursor.

## Manual fallbacks

```bash
node .cursor/skills/skill-monitor/scripts/cli.mjs record --path "C:/path/to/skill/SKILL.md"
node .cursor/skills/skill-monitor/scripts/cli.mjs record-task --type explore --project .
```
