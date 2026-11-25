---
name: shell-context-guard
description: Защита от смешивания shell-контекстов (PowerShell vs bash) и быстрый переход к корректному формату команд для VPS/Linux задач.
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

# Skill: Shell Context Guard

## Triggers
- "команда не работает в PowerShell"
- "No such file or directory" при Linux-пути в Windows shell
- "head/sed/set -euo" не распознаны
- "процесс терминала завершен с кодом 1/127/128" после copy-paste

## Objective
Сразу определить shell-контекст и выдавать команды только в корректном синтаксисе, чтобы избежать ложных ошибок исполнения.

## Workflow
1. Определить контекст исполнения:
   - локальный PowerShell (`PS C:\\...>`)
   - SSH Linux shell (`user@host:~$`)
2. Не смешивать диалекты:
   - для PowerShell: только PowerShell-команды;
   - для Linux/VPS: только `bash`-совместимые команды.
3. Если задача Linux-only, сначала дать шаг подключения:
   - `ssh user@host`
   - затем отдельный блок Linux-команд.
4. Для длинных сценариев давать диагностический режим с `run()`/`RC`, чтобы локализовать первый failing step.
5. Явно указывать ожидаемый prompt перед выполнением блока.

## Constraints
- Запрещено выдавать mixed-блоки (`bash` + PowerShell в одном snippet).
- Не предполагать наличие Unix-утилит (`head`, `sed`) в PowerShell.
- Не считать `exit 1/128` доказательством ошибки логики до проверки shell-контекста.

## Output
- Корректный набор команд под текущий shell.
- Явный маркер: "выполнять только после входа в SSH Linux shell" (если требуется).
- Короткая диагностика причины сбоя и next step.

## Handoff
- **Success condition**: shell-контекст определён, команды выданы в правильном синтаксисе.
- **Next**: возврат к вызывающему агенту
- **Auto-proceed**: 🟢 YES
- **Hard stop**: NO
