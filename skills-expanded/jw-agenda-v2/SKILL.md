---
name: jw-agenda-v2
description: "Agenda management / 日程管理: daily todo, daily log, weekly plan, weekly review, monthly review, planning sync. Trigger phrases: 今天计划、日报、周规划、周总结、月总结、同步规划、today plan、weekly review、monthly review"
metadata:
  author: Jing Wu
  version: "1.4.0"
  updated: "2026-07-08"
---

# jw-agenda-v2

Six agenda management modes in one: Daily Todo, Daily Log, Weekly Plan, Weekly Review, Monthly Review, Planning Sync.

## Execution Flow

1. **Route**: Match the target mode based on the trigger phrase table below
2. **Load conventions**: Read `assets/conventions.md` for shared rules; load `assets/conventions-marks.md` and/or `assets/conventions-cascade.md` per mode pre-conditions
3. **Execute mode**: Read the corresponding `references/mode-*.md` and follow its instructions

## Trigger Phrase Mapping

Matching is case-insensitive and ignores leading/trailing whitespace. Two tiers: **exact** (direct trigger) and **fuzzy** (context-dependent, confirm if needed).

| Mode              | Exact Triggers                                                                                                              | Fuzzy / Colloquial Triggers                                 | Instruction File                                |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- | ----------------------------------------------- |
| **Daily Todo**    | `生成今天的计划`、`today plan`、`today's plan`、`加一项`、`add a task`、`把 X 移到`、`move X to`、`推迟到`、`postpone to`、`明天要`、`tomorrow need`、`本周要`、`下周要`、`daily-todo` | `帮我安排今天`、`今日计划`、`今天做什么`、`help me plan today`、`plan today`、`what to do today` | `references/mode-daily-todo.md`                 |
| **Daily Log**     | `整理日志`、`总结昨天`、`summarize yesterday`、`汇报今天`、`report today`、`记录一下`、`log it`、`我完成了`、`I finished`、`daily log`、`daily-log` | `日报`、`今天的总结`、`recap today`、`今天干了什么`、`daily report`、`what did I do today` | `references/mode-daily-log.md`                  |
| **Weekly Plan**   | `生成本周计划`、`周规划`、`weekly plan`、`weekly-plan`                                                                      | `规划本周`、`规划下周`、`plan this week`、`plan next week`  | `references/mode-weekly-plan.md`                |
| **Weekly Review** | `周总结`、`本周回顾`、`上周回顾`、`weekly review`、`weekly-review`                                                          | `这周怎么样`、`review this week`、`上周总结`、`how was this week`、`last week summary` | `references/mode-weekly-review.md`              |
| **Monthly Review**| `月总结`、`本月回顾`、`上月回顾`、`monthly review`、`monthly-review`                                                        | `月报`、`recap this month`、`Q1总结`–`Q4总结`、`Q1 review`–`Q4 review` | `references/mode-monthly-review.md`             |
| **Planning Sync** | `同步规划`、`检查一致性`、`planning sync`、`planning-sync`                                                                  | `检查规划`、`sync plans`、`规划有没有对齐`、`are plans aligned` | `references/mode-planning-sync.md`              |
| **Archive Logs**  | `归档日志`、`归档 daily`、`archive daily`、`archive logs`、`清理 daily 目录`                                                | —                                                           | `references/mode-weekly-review.md` (Step 6 only)|

**Add/Move Task** (Mode 1 Sub-mode C): `加一项`、`add a task`、`明天要`、`tomorrow need`、`移到周三`、`move to Wednesday`、`推迟到 2.10`、`postpone to 2.10` → see `references/mode-add-or-move.md`.

## Matching Priority

1. **Exact command** > fuzzy match
2. **Key action words**: `加一项`/`add a task`/`移到`/`move to` → Daily Todo; `完成了`/`I finished` → Daily Log
3. **Time scope words**: `今天`/`today` → day-level; `本周/上周`/`this week/last week` → week-level; `本月/上月`/`this month/last month`/`Q1–Q4` → month-level
4. **When ambiguous**, ask the user to clarify intent

## Mode 1 Sub-mode Routing

| Sub-mode                 | Trigger Scenario                                         |
| ------------------------ | -------------------------------------------------------- |
| A: Generate Daily Todo   | `生成今天的计划`、`today plan`                            |
| B1: Query Progress       | `完成得怎么样`、`还剩哪些`、`how's it going`、`what's left` |
| B2: Update Status        | `不做了`、`取消`、`推迟`、`cancel it`、`postpone` (no target date) |
| C: Add/Move Task         | `加一项`、`add a task`、`明天要`、`移到周三`、`move to Wednesday`、`推迟到 2.10` |

Shared conventions: see `assets/conventions.md`.
