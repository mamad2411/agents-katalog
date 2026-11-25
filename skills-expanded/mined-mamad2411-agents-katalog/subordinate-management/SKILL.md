---
name: subordinate-management
description: >-
  Supervisor operations for subordinate Anima. Perform suspension, resumption, model changes, restart, task delegation, status reading, and auditing.
  Use when: Use when: you need to disable or re-enable subordinates, change the main or BG model, restart processes, delegate tasks, or check the organization dashboard.
---


# Skill: Subordinate Management (Supervisor Tools)

A set of supervisor tools automatically enabled for Anima instances with subordinates. Perform suspension, resumption, model changes, background model changes, restart, and status checks for all descendants (children, grandchildren, great-grandchildren, etc.), as well as task delegation and progress tracking for direct subordinates.

## Available Tools

### Operable on all subordinates (children, grandchildren, great-grandchildren, etc.)

| Tool | Purpose |
|--------|------|
| `disable_subordinate` | Request root to configure status.json `enabled: false` (process shutdown + prevent automatic restart) |
| `enable_subordinate` | Restore dormant subordinates |
| `set_subordinate_model` | Request root to update the main model for status.json and reload running processes |
| `set_subordinate_background_model` | Request root to update the model for heartbeat/cron. Applied from the next background task (clear with empty string) |
| `restart_subordinate` | Restart subordinate processes (status.json `restart_requested` flag. Reconciliation restarts within about 30 seconds) |
| `delegate_task` | Delegate tasks to direct subordinates (queue addition + DM send + create tracking entry on your side) |
| `org_dashboard` | Display process status, last activity, current task, and task count for all subordinates in a tree view |
| `ping_subordinate` | Check subordinate liveness (all at once if `name` is omitted, single if specified) |
| `read_subordinate_state` | Read subordinate's `current_state.md` |
| `audit_subordinate` | Comprehensive audit of subordinate's recent activity (activity summary, task status, error frequency, tool usage statistics, communication patterns) |

### Delegated Task Tracking

| Tool | Purpose |
|------|---------|
| `task_tracker` | Track progress of tasks delegated via `delegate_task` from the subordinate's queue (`status`: all / active / completed. Default: active) |

The delegator's tracking card references the delegate's authoritative task record. Use `task_tracker` to check status.

## Important: Difference Between disable_subordinate and send_message

- **disable_subordinate**: Changes status.json to `enabled: false`. Reconciliation will not auto-resume. **Use this one**
- Simply telling a subordinate to "rest" via send_message **does not stop the process**. Even if a message is sent, Reconciliation will restart it

## Usage

### Suspension and Resumption

When suspending multiple people, call `disable_subordinate` one at a time:

```
disable_subordinate(name="aoi", reason="業務縮小のため一時休止")
disable_subordinate(name="taro", reason="業務縮小のため一時休止")
enable_subordinate(name="aoi")
```

### Model Change and Restart

These tools request root-owned updates from root `status.json`. Do not edit directly from the Anima process. The main model is reloaded into the running process, and a stopped Anima reads the new configuration at next startup:

```
set_subordinate_model(name="aoi", model="claude-sonnet-5-5", reason="負荷分散のため")
```

The background model (for heartbeat/cron) takes effect from the next task runner startup, and running tasks complete as-is:

```
set_subordinate_background_model(name="aoi", model="claude-sonnet-5-5", reason="heartbeat負荷軽減")
```

To clear the background model and return to the main model:

```
set_subordinate_background_model(name="aoi", model="", reason="メインモデルに統一")
```

Only use `restart_subordinate` separately when a full process restart is truly necessary.

### Status Check and Audit

```
org_dashboard()                         # 配下全体のダッシュボード
ping_subordinate()                      # 全配下の生存確認
ping_subordinate(name="aoi")            # 単一の生存確認
read_subordinate_state(name="aoi")      # 現在タスク・保留タスクの内容
audit_subordinate(name="aoi")           # 直近1日の包括監査レポート
audit_subordinate(name="aoi", days=7)   # 直近7日間の監査（days は 1〜30）
audit_subordinate(since="09:00")        # 全配下の今日9時以降の監査
audit_subordinate(name="aoi", since="13:00")  # aoi の今日13時以降
```

Also executable from the CLI (useful when using via Bash in S/C/D/G-mode):

```bash
animaworks anima audit aoi              # 直近1日の監査
animaworks anima audit aoi --days 7     # 直近7日間の監査
animaworks anima audit --all --since 09:00  # 全Anima、今日9時以降
```

### Task Delegation

```
delegate_task(name="aoi", instruction="週次レポートをまとめて", summary="週次レポート作成")
# 必須: `name`, `instruction`。任意: `summary`, `workspace`, `acceptance_criteria`, `model`
# workspace を指定すると委譲先がそのワークスペースで作業する（workspace-manager スキル参照）
task_tracker(status="active")      # 委譲タスクの進捗確認（status: all / active / completed）
```

For workspace assignment to subordinates (specifying the primary working directory), refer to the `workspace-manager` skill.

## Permissions

- **All descendants (children, grandchildren, great-grandchildren, etc., recursive)**: Status check and management tools available
- **Direct subordinates only**: `delegate_task` (task delegation)
- Cannot operate on yourself
