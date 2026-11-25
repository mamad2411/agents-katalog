---
name: claude-stats
description: |
  Claude Code使用統計を集計。Usage: /claude-stats [period] [type]
  period: today|week|month|all | type: summary|full|tools|skills|tokens|hourly|models|web|projects
allowed-tools: Bash
user-invocable: true
---

# Claude Code Usage Statistics

`~/.claude/projects/` 配下の transcript JSONL から統計を集計して表示する。

## Usage

```
/claude-stats [period] [type]
```

**period**: `today` | `week` | `month` | `all` (default)

**type**: `summary` (default) | `full` | `tools` | `skills` | `subagents` | `sessions` | `files` | `mcp` | `models` | `tokens` | `web` | `projects` | `thinking` | `hourly`

## Examples

```
/claude-stats              # 全期間サマリー
/claude-stats today tools  # 今日のツール別
/claude-stats week skills  # 過去7日間のSkill別
/claude-stats week full    # 過去7日間の全統計
/claude-stats month tokens # 過去30日間のトークン使用量
/claude-stats week hourly  # 過去7日間の時間帯別使用
```

## Execution

引数をパースし、以下を実行:

```bash
python3 scripts/aggregate.py --period {period} --type {type}
```
