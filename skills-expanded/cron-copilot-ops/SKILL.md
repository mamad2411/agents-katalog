---
name: cron-copilot-ops
description: "Install, configure, and operate CronCopilot — a Python-based scheduled task management system for cron jobs, scripts, monitoring, and alerts."
license: MIT
metadata:
  author: eden2f
  version: "1.0.0"
---

# CronCopilot Operations Skill

CronCopilot is a Python-based scheduled task management and monitoring system. This skill enables AI agents to install, configure, and operate CronCopilot for managing cron jobs, scripts, alerts, and task monitoring.

- **GitHub**: https://github.com/eden2f/cron-copilot
- **Gitee**: https://gitee.com/eden2f/cron-copilot

## When to Use This Skill

> **Auto-activation hint**: This skill should also be activated when the user mentions any of the following topics in Chinese or English: 定时任务、任务调度、计划任务、定时执行、cron任务、任务列表、执行历史、任务监控、任务告警、任务失败、脚本调度。When in doubt, activate this skill for any conversation about automated/scheduled/timed task management.

Activate this skill when the user needs to:

- **Set up scheduled tasks** — create, modify, or delete cron jobs
- **Manage scripts** — register, remove, or inspect scripts for task execution
- **Monitor task execution** — check task status, view execution history, diagnose failures
- **Configure alerting & notifications** — set up failure alerts, performance threshold alerts, email notifications
- **Troubleshoot scheduled tasks** — debug failing tasks, resolve dependency issues, handle stuck processes

## System Requirements

| Requirement | Detail |
|---|---|
| Python | 3.10+ |
| OS | Linux / macOS (Windows via WSL2) |
| Database | SQLite (built-in, no external DB needed) |

## Quick Start

```bash
# Clone the repository
git clone https://gitee.com/eden2f/cron-copilot
cd cron-copilot

# Production install (recommended for deployment)
pip install .

# Development install (editable mode, changes take effect immediately)
pip install -e .

# Development install with dev dependencies
pip install -e ".[dev]"

# Initialize CronCopilot (creates config and database)
croncopilot init
```

After initialization, start the scheduler:

```bash
croncopilot start          # foreground mode
croncopilot start --daemon # background daemon mode
```

## Upgrade CronCopilot

```bash
# Production upgrade
pip install --upgrade .
croncopilot stop && croncopilot start --daemon

# Development mode (editable install): just pull latest code and restart
git pull
croncopilot stop && croncopilot start --daemon

# Update Chinese holiday data
pip install -U chinesecalendar
```

## Core CLI Commands

### Initialization & Lifecycle

```bash
croncopilot init              # Initialize config and database
croncopilot start             # Start scheduler (foreground)
croncopilot start --foreground # Explicitly start in foreground mode
croncopilot start --daemon    # Start scheduler (daemon mode)
croncopilot stop              # Stop the scheduler
croncopilot status            # Show scheduler status
croncopilot health            # Perform system health check
```

**Notes on lifecycle commands**:
- `croncopilot start` automatically stops any existing running instance before starting (single-instance protection)
- PID file is written to `~/.croncopilot/croncopilot.pid` (both foreground and daemon mode)
- Foreground mode prints logs to stdout/stderr, press `Ctrl+C` to stop gracefully

### Global Options

| Option | Short | Description |
|---|---|---|
| `--config <path>` | `-c` | Specify a custom configuration file path (default: `~/.croncopilot/config.yaml`) |
| `--verbose` | `-v` | Enable verbose output for debugging |

### Task Management

```bash
croncopilot task add [OPTIONS]      # Add a new scheduled task
croncopilot task update <name> [OPTIONS] # Update an existing task
croncopilot task remove <name>      # Remove a task by name
croncopilot task remove <name> -f   # Force remove (skip confirmation)
croncopilot task list               # List all tasks
croncopilot task list -c <category> # Filter by category
croncopilot task list -s <status>   # Filter by status (enabled/disabled)
croncopilot task run <name>         # Manually trigger a task
croncopilot task history <name>           # View execution history of a task
croncopilot task history <name> -d 7      # View last 7 days
croncopilot task history <name> -l 50     # Show latest 50 records
croncopilot task history <name> --stats-only  # Show statistics summary only
```

**Key options for `task add`**:

| Option | Short | Description | Example |
|---|---|---|---|
| `--name` | `-n` | Task name (unique identifier, required) | `--name daily-backup` |
| `--script` | `-s` | Script path to execute (required) | `--script /opt/scripts/backup.py` |
| `--schedule-type` | `-t` | Schedule type (required): `cron`, `daily`, `weekly`, `monthly`, `interval` | `--schedule-type cron` |
| `--schedule` | `-S` | Schedule expression (required) | `--schedule "0 2 * * *"` |
| `--priority` | `-p` | Priority 1-10 (higher = more important, default: 5) | `--priority 8` |
| `--max-instances` | | Max concurrent instances (default: 1) | `--max-instances 1` |
| `--depends-on` | | Dependency task name(s) (can specify multiple times) | `--depends-on pre-check` |
| `--holiday-mode` | | Holiday handling mode (default: `none`) | `--holiday-mode workday_only` |
| `--timeout` | | Execution timeout in seconds (default: 3600) | `--timeout 3600` |
| `--max-retries` | | Max retry attempts on failure (default: 3) | `--max-retries 3` |
| `--description` | | Human-readable description of the task | `--description "Daily backup job"` |
| `--category` | | Task category for organization | `--category data-pipeline` |

**Key options for `task update`**:

Only specified fields are updated. After modification, the running scheduler is automatically notified to reload tasks via SIGHUP.

| Option | Description | Example |
|---|---|---|
| `--new-name` | New task name | `--new-name daily-backup-new` |
| `--script` | New script path | `--script /opt/scripts/backup-v2.py` |
| `--schedule-type` | New schedule type | `--schedule-type daily` |
| `--schedule` | New schedule expression | `--schedule "03:00"` |
| `--priority` | New priority 1-10 | `--priority 7` |
| `--max-instances` | New max concurrent instances | `--max-instances 2` |
| `--holiday-mode` | New holiday mode | `--holiday-mode workday_only` |
| `--timeout` | New timeout in seconds | `--timeout 7200` |
| `--max-retries` | New max retry attempts | `--max-retries 5` |
| `--category` | New category (empty string to clear) | `--category ""` |
| `--description` | New description (empty string to clear) | `--description ""` |
| `--enable / --disable` | Enable or disable the task | `--disable` |

**Notes on task commands**:
- `task add/update/remove` automatically notify the running daemon to reload tasks (via SIGHUP)
- `task run` skips holiday checks and executes the task immediately
- `task list` output columns: Name, Schedule Type, Schedule, Priority, Status, Holiday Mode, Category

### Script Management

```bash
croncopilot script add [OPTIONS]    # Register a new script
croncopilot script remove <name>              # Remove a registered script
croncopilot script remove <name> --delete-file  # Also delete the script file
croncopilot script list               # List all registered scripts
croncopilot script list -c <category> # Filter by category
croncopilot script update <name> [OPTIONS] # Update script file or metadata
croncopilot script info <name>      # Show script details and version history
```

**Key options for `script add`**:

| Option | Description | Example |
|---|---|---|
| `--path` | Path to the script file (required) | `--path /opt/scripts/backup.py` |
| `--name` | Script name (defaults to filename if not specified) | `--name my-backup` |
| `--venv` | Python virtual environment path | `--venv /opt/venvs/backup` |
| `--author` | Script author | `--author "eden2f"` |
| `--description` | Script description | `--description "ETL pipeline script"` |
| `--category` | Script category | `--category etl` |

**Key options for `script update`**:

Only specified fields are updated. When `--path` is given, the new script file replaces the old one and the previous version is auto-backed up.

| Option | Description | Example |
|---|---|---|
| `--path` | New script file path | `--path /opt/scripts/backup-v2.py` |
| `--author` | Author name | `--author "eden2f"` |
| `--description` | Script description | `--description "Updated pipeline"` |
| `--category` | Script category | `--category production` |
| `--venv` | Python virtual environment path | `--venv /opt/venvs/backup-v2` |

## Schedule Types

### Cron Expression (5-field standard format)

Format: `minute hour day month weekday`

```
┌───────────── minute (0-59)
│ ┌───────────── hour (0-23)
│ │ ┌───────────── day of month (1-31)
│ │ │ ┌───────────── month (1-12)
│ │ │ │ ┌───────────── day of week (0-6, 0=Sunday)
│ │ │ │ │
* * * * *
```

Examples: `0 2 * * *` (daily 2 AM), `*/5 * * * *` (every 5 min), `0 9 * * 1-5` (weekdays 9 AM)

### Interval

Use shorthand: `5m` (5 minutes), `1h` (1 hour), `1d` (1 day), `90s` (90 seconds)

### Preset Types

- `daily`: Once per day, format `HH:MM` (e.g., `08:00`)
- `weekly`: Once per week, format `DAY@HH:MM` where DAY is `mon/tue/wed/thu/fri/sat/sun` (e.g., `mon@08:00`)
- `monthly`: Once per month, format `DAY@HH:MM` where DAY is 1-31 (e.g., `1@08:00`)

## Holiday Awareness

CronCopilot supports Chinese statutory holiday recognition. Configure via `--holiday-mode`:

| Mode | Behavior |
|---|---|
| `none` | Execute regardless of holidays (default) |
| `workday_only` | Execute only on working days (skips weekends & holidays, includes adjusted workdays/调休) |
| `holiday_only` | Execute only on holidays and weekends (skips workdays and adjusted workdays) |
| `skip_holiday` | Skip statutory holidays but run on weekends and workdays |
| `skip_workday` | Execute only on non-workdays (skips regular workdays and adjusted workdays, runs on weekends & holidays) |

Example:

```bash
croncopilot task add --name daily-report \
  --schedule "0 9 * * *" \
  --schedule-type cron \
  --script /opt/scripts/report.py \
  --holiday-mode workday_only
```

## Task Dependencies & Priority

### Priority

Tasks have priority levels 1–10 (higher = higher priority). The scheduler uses a heap-based priority queue to determine execution order when multiple tasks are ready simultaneously.

### Dependencies

Tasks can declare dependencies on other tasks using `--depends-on` (specify multiple times for multiple dependencies). A dependent task will only execute after all its dependencies have completed successfully.

```bash
croncopilot task add --name data-export \
  --schedule "0 3 * * *" \
  --schedule-type cron \
  --script export.py \
  --depends-on data-cleanup \
  --priority 5
```

### Concurrency Control

Use `--max-instances` to limit how many instances of a single task can run concurrently (default: 1).

## Alerting & Self-Healing

### Alert Types

- **Immediate failure alert** — triggered on any task failure (default: `failure_immediate: true`)
- **Consecutive failure alert** — triggered after N consecutive failures (default: 3)
- **Cooldown period** — prevents alert spam for the same task (default: 300 seconds)

### Email Notification

Configure email alerts in the CronCopilot config file (`~/.croncopilot/config.yaml`):

```yaml
alert:
  failure_immediate: true
  consecutive_failure_threshold: 3
  cooldown_seconds: 300

  email:
    enabled: true
    smtp_host: smtp.example.com
    smtp_port: 587
    use_tls: true
    username: alerts@example.com
    password: "your-password"
    sender: "CronCopilot <alerts@example.com>"
    recipients:
      - admin@example.com
```

(SMTP username and password can also be set via environment variables `CRONCOPILOT_SMTP_USER` and `CRONCOPILOT_SMTP_PASSWORD`, which take precedence over config file values.)

### Self-Healing

- **Auto-retry with exponential backoff**: Configured via `--max-retries` (default: 3)
- **Health check**: Periodic scheduler self-diagnosis (default: every 60 seconds)
- **Deadlock detection**: Identifies and terminates stuck tasks automatically
- **Timeout enforcement**: Kills tasks exceeding `--timeout` value (default: 3600s)

## Configuration Hot Reload

### Automatic Reload on Task Changes

When you use `croncopilot task add/update/remove`, the CLI automatically sends a SIGHUP signal to the running daemon, which reloads all tasks from the database without restarting.

### Manual Reload via SIGHUP

You can also manually trigger a reload by sending SIGHUP directly:

```bash
kill -HUP $(cat ~/.croncopilot/croncopilot.pid)
```

The scheduler reloads configuration and tasks immediately.

**What can be reloaded without restart**:
- Task definitions (add/update/remove)
- Alert configuration
- Log level
- Recovery/health check settings

**What requires a full restart**:
- Database path
- PID file path
- Scheduler `max_workers`
- Watchdog file monitoring setup

## System Service Deployment

CronCopilot does **not** expose a `croncopilot service` CLI command in v0.1.0. To deploy as a system service, use the Python API or manual configuration files from the `deploy/` directory in the source repository.

### Using the Python API

```python
from croncopilot.deploy.service import ServiceGenerator

generator = ServiceGenerator()
# Generates and prints service config + instructions for your OS
config_path = generator.generate()
print(f"Generated config at: {config_path}")
```

### Manual Configuration

Templates are available in the `deploy/` directory of the CronCopilot source:
- `deploy/croncopilot.service`: systemd service (Linux)
- `deploy/com.croncopilot.plist`: launchd plist (macOS)

These templates need placeholders replaced with actual paths (Python binary, home directory, etc.).

## Common Usage Examples

### 1. Add a Daily Backup Task at 2 AM

```bash
croncopilot task add \
  --name daily-backup \
  --schedule "0 2 * * *" \
  --schedule-type cron \
  --script /opt/scripts/backup.sh \
  --priority 8 \
  --max-retries 3 \
  --timeout 7200
```

### 2. Update an Existing Task

Change the schedule, disable temporarily, etc.:

```bash
# Change schedule to 3 AM
croncopilot task update daily-backup --schedule "0 3 * * *"

# Temporarily disable the task
croncopilot task update daily-backup --disable

# Re-enable and change priority
croncopilot task update daily-backup --enable --priority 10
```

### 3. Add a Workday-Only Report Task

```bash
croncopilot task add \
  --name morning-report \
  --schedule "0 9 * * *" \
  --schedule-type cron \
  --script /opt/scripts/gen_report.py \
  --holiday-mode workday_only \
  --priority 6
```

### 4. Register a Script with Virtual Environment

```bash
croncopilot script add \
  --name etl-pipeline \
  --path /opt/scripts/etl.py \
  --venv /opt/venvs/etl-env

croncopilot task add \
  --name nightly-etl \
  --schedule "0 1 * * *" \
  --schedule-type cron \
  --script etl-pipeline
```

### 5. Configure Task Dependencies

```bash
# Step 1: cleanup task runs first
croncopilot task add \
  --name data-cleanup \
  --schedule "0 0 * * *" \
  --schedule-type cron \
  --script cleanup.py \
  --priority 9

# Step 2: export task depends on cleanup
croncopilot task add \
  --name data-export \
  --schedule "0 1 * * *" \
  --schedule-type cron \
  --script export.py \
  --depends-on data-cleanup \
  --priority 7
```

### 6. Start as Daemon and Check Status

```bash
croncopilot start --daemon
croncopilot status
croncopilot task list
```
