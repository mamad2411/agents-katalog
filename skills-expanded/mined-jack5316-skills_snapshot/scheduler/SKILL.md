---
name: scheduler
description: Automate and schedule tasks (skills/pipelines) to run automatically. Uses launchd on macOS. Use when user asks to schedule tasks, automate execution, run skills automatically, cron, or /scheduler.
---

# Scheduler Skill

Schedule skills and pipelines to run automatically via launchd on macOS (checks due tasks every 15 min).

## Usage

```bash
python3 _scripts/scheduler.py add org-daily --schedule daily --time 09:00
python3 _scripts/scheduler.py add org-weekly --schedule weekly --day monday --time 10:00
python3 _scripts/scheduler.py list
python3 _scripts/scheduler.py install   # generate launchd plist
```

## Commands

| Command | Description |
|---------|-------------|
| `add <target>` | Add a scheduled task |
| `list` | List all scheduled tasks |
| `remove <id>` | Remove a task by ID |
| `run` | Check and run due tasks (called by launchd) |
| `wake` | Run overdue tasks now |
| `install` | Generate launchd plist for macOS |

## Schedule Types

- `--schedule daily --time HH:MM`
- `--schedule weekly --day monday --time HH:MM`
- `--schedule cron --cron "0 8 * * 1-5"`

After `install`: `cp _config/com.pai.scheduler.plist ~/Library/LaunchAgents/ && launchctl load ...`

## Output

Config: `_config/schedule.json` | State: `_config/schedule_state.json` | Logs: `_logs/scheduler_*.log`
