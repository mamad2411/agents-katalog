---
name: openclaw-cron
description: Manage OpenClaw cron jobs safely without editing config files. Use when the user wants to create scheduled tasks, list cron jobs, enable/disable tasks, run tasks immediately for testing, or view cron job history. Provides safe wrappers around openclaw cron CLI commands with templates and best practices.
---

# OpenClaw Cron Manager

Safe management of OpenClaw cron jobs without touching configuration files.

## Quick Start

### List all cron jobs

```bash
openclaw cron list
```

### Add a new cron job

```bash
openclaw cron add \
  --name "任务名称" \
  --cron "0 9 * * 1" \
  --tz "Asia/Shanghai" \
  --agent main \
  --message "任务描述" \
  --announce \
  --channel telegram \
  --to "telegram:YOUR_CHAT_ID"
```

### Test run immediately

```bash
openclaw cron run <job-id>
```

### Disable/Enable a job

```bash
openclaw cron disable <job-id>
openclaw cron enable <job-id>
```

## Common Patterns

### Daily task (every day at 9 AM)

```bash
openclaw cron add \
  --name "每日检查" \
  --cron "0 9 * * *" \
  --tz "Asia/Shanghai" \
  --agent main \
  --message "执行每日检查任务" \
  --announce
```

### Weekly task (every Monday at 9 AM)

```bash
openclaw cron add \
  --name "周报" \
  --cron "0 9 * * 1" \
  --tz "Asia/Shanghai" \
  --agent main \
  --message "生成周报" \
  --announce
```

### Hourly task

```bash
openclaw cron add \
  --name "每小时检查" \
  --every "1h" \
  --agent main \
  --message "执行小时检查"
```

### One-time task (run once after 20 minutes)

```bash
openclaw cron add \
  --name "提醒" \
  --at "+20m" \
  --agent main \
  --message "20分钟后的提醒" \
  --delete-after-run \
  --announce
```

## Cron Expression Guide

Format: `minute hour day month weekday`

**Examples:**
- `0 9 * * *` - Every day at 9:00 AM
- `0 9 * * 1` - Every Monday at 9:00 AM
- `0 */2 * * *` - Every 2 hours
- `30 8 * * 1-5` - Weekdays at 8:30 AM
- `0 0 1 * *` - First day of every month at midnight

**Shortcuts:**
- `--every "10m"` - Every 10 minutes
- `--every "1h"` - Every hour
- `--every "1d"` - Every day
- `--at "+20m"` - Once, 20 minutes from now
- `--at "2026-03-02T09:00:00"` - Once, at specific time

## Key Options

### Scheduling

- `--cron <expr>` - Cron expression (5-field)
- `--every <duration>` - Interval (e.g., 10m, 1h, 1d)
- `--at <when>` - One-time: ISO timestamp or +duration
- `--tz <iana>` - Timezone (default: system, e.g., Asia/Shanghai)

### Agent & Session

- `--agent <id>` - Which agent runs the task (default: main)
- `--session <target>` - Session type: `main` or `isolated` (default: isolated)
- `--model <model>` - Model override for this job

### Delivery

- `--announce` - Send result summary to chat
- `--channel <channel>` - Delivery channel (telegram, whatsapp, etc.)
- `--to <dest>` - Destination (e.g., telegram:123456)
- `--no-deliver` - Don't send any notifications

### Task Content

- `--message <text>` - Message for agent to process
- `--system-event <text>` - System event payload

### Behavior

- `--disabled` - Create job disabled (enable later)
- `--delete-after-run` - Auto-delete after one-time job succeeds
- `--timeout-seconds <n>` - Task timeout (default: 30)
- `--thinking <level>` - Thinking level: off/minimal/low/medium/high

## Management Commands

### List jobs

```bash
# List all jobs
openclaw cron list

# List with JSON output
openclaw cron list --json
```

### View job details

```bash
openclaw cron status
```

### Run job immediately (testing)

```bash
openclaw cron run <job-id>
```

### View run history

```bash
openclaw cron runs <job-id>
```

### Edit job

```bash
openclaw cron edit <job-id> --name "新名称"
openclaw cron edit <job-id> --cron "0 10 * * *"
openclaw cron edit <job-id> --disabled
```

### Enable/Disable

```bash
openclaw cron disable <job-id>
openclaw cron enable <job-id>
```

### Delete job

```bash
openclaw cron rm <job-id>
```

## Real-World Examples

### ClawHub Skills Discovery (Weekly)

```bash
openclaw cron add \
  --name "ClawHub Skills 周报" \
  --cron "0 9 * * 1" \
  --tz "Asia/Shanghai" \
  --agent main \
  --message "请检查 ClawHub 上的新 skills 并推荐给我。使用 clawhub search 命令搜索不同类别的 skills。" \
  --announce \
  --channel telegram \
  --to "telegram:5223431061"
```

### Daily Backup

```bash
openclaw cron add \
  --name "每日备份" \
  --cron "0 2 * * *" \
  --tz "Asia/Shanghai" \
  --agent main \
  --message "创建 OpenClaw 配置备份并推送到 GitHub" \
  --announce
```

### GitHub Activity Report (Daily)

```bash
openclaw cron add \
  --name "GitHub 日报" \
  --cron "0 17 * * *" \
  --tz "Asia/Shanghai" \
  --agent main \
  --message "总结今天的 GitHub 活动：commits, PRs, issues" \
  --announce \
  --channel telegram
```

### Reminder (One-time)

```bash
openclaw cron add \
  --name "会议提醒" \
  --at "+30m" \
  --agent main \
  --message "30分钟后有会议" \
  --delete-after-run \
  --announce
```

## Best Practices

### ✅ Do

1. **Use `--announce`** for tasks that should notify you
2. **Set timezone** with `--tz` for cron expressions
3. **Test first** with `openclaw cron run <id>` before enabling
4. **Use isolated sessions** (default) for independent task execution
5. **Set reasonable timeouts** with `--timeout-seconds`
6. **Use descriptive names** for easy identification

### ❌ Don't

1. **Don't edit `openclaw.json` directly** - Use CLI commands
2. **Don't create too many frequent tasks** - Combine related checks
3. **Don't forget timezone** - Default may not match your location
4. **Don't use `main` session** unless you need conversation context
5. **Don't skip testing** - Always test with `cron run` first

## Troubleshooting

**Job not running:**
1. Check if enabled: `openclaw cron list`
2. Check next run time
3. Verify timezone setting
4. Test manually: `openclaw cron run <id>`

**Job fails:**
1. Check run history: `openclaw cron runs <id>`
2. Verify agent exists
3. Check timeout settings
4. Test message manually in chat

**Wrong schedule:**
1. Verify cron expression: https://crontab.guru
2. Check timezone setting
3. Edit schedule: `openclaw cron edit <id> --cron "..."`

## Reference

### Cron Expression Syntax

```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of week (0 - 6) (Sunday=0)
│ │ │ │ │
* * * * *
```

### Common Timezones

- `Asia/Shanghai` - China (UTC+8)
- `America/New_York` - US Eastern
- `Europe/London` - UK
- `UTC` - Universal Time

### Duration Format

- `s` - seconds (e.g., `30s`)
- `m` - minutes (e.g., `10m`)
- `h` - hours (e.g., `2h`)
- `d` - days (e.g., `1d`)

## See Also

- Official docs: https://docs.openclaw.ai/cli/cron
- Cron expression tester: https://crontab.guru
- Timezone list: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
