---
name: memory-bank-manager
description: Поддержание актуального состояния памяти проекта между сессиями.
user-invocable: true
allowed-tools:
  - Read
  - Bash(git *)
  - Bash(ls *)
  - Bash(find *)
  - Bash(grep *)
  - Bash(cat *)
  - Bash(npm *)
  - Bash(npx *)
  - Bash(curl *)
  - Bash(fuser *)
  - Bash(node *)
  - Bash(rg *)
  - Bash(jq *)
---

# Memory Bank Manager

## Objective
Keep `memory-bank/` concise and current.

## Protocols
1. `context.md`: текущий фокус, рабочий scope, next step.
2. `progress.md`: что сделано, что в работе, что дальше; rolling window до 15 записей.
3. `decisions.md`: ключевые решения и их последствия.

## No-Rot Rule
- Удалять устаревшие формулировки.
- Не дублировать один и тот же статус в разных местах.

## Handoff
- **Success condition**: `memory-bank/context.md` и `progress.md` актуальны, нет отживших формулировок.
- **Next**: возврат Control Tower (продолжение pipeline)
- **Auto-proceed**: 🟢 YES
- **Hard stop**: NO
