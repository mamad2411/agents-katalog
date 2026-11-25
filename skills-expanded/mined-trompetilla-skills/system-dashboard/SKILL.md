# System Dashboard

Generates and sends a comprehensive system status dashboard to Feishu.
Consolidates metrics from OS, Logs, Evolver, and Cron into a single view.

## Features

- **System Health:** CPU load, Memory usage, Disk space, Uptime.
- **Log Analysis:** Recent error counts from `memory/logs/`.
- **Evolver Status:** Last run status, success rate (from `memory/events.jsonl`).
- **Cron Jobs:** Count of active/inactive jobs.
- **Skill Health:** Total skills vs broken skills.

## Usage

```bash
node skills/system-dashboard/index.js
```

## Options

- `--target <id>`: Feishu User/Group ID (optional, defaults to configured master).
- `--days <n>`: Look back N days for log analysis (default: 1).

## Output

Sends a Feishu Card with a color-coded header:
- **Green:** All systems nominal.
- **Orange:** Warnings (high load, disk > 80%, minor errors).
- **Red:** Critical (disk > 90%, major errors, evolver failure).
