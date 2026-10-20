---
name: technical-discovery
description: Анализ структуры проекта и подготовка решений на основе текущих артефактов.
user-invocable: true
allowed-tools:
  - Read
  - Bash(git *)
  - Bash(ls *)
  - Bash(find *)
  - Bash(grep *)
  - Bash(cat *)
  - Bash(rg *)
  - Bash(jq *)
---

# Skill: Technical Discovery

## Triggers
- "исследуй", "проанализируй", "что уже есть"

## Workflow
1. Инвентаризация файлов через `rg --files`.
2. Чтение ключевых документов (`strategy`, `brand`, `ops`, `05_ai`).
3. Выявление пробелов, дубликатов, блокеров.
4. Подготовка короткого RFC/рекомендаций в `docs/research/` (если нужно; создать каталог on demand).

## Constraints
- Без правок кода/контента, только анализ.
- Все выводы должны иметь ссылку на конкретные файлы.

## Handoff
- **Success condition**: инвентаризация завершена, пробелы и блокеры документированы.
- **Next**: task-decomposition или Control Tower (планирование)
- **Auto-proceed**: 🟢 YES
- **Hard stop**: NO
