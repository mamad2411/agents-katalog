---
name: extract-meeting-actions
description: Extract tasks, questions, risks, and a compact task register from raw meeting notes for the workshop exercise.
---

# Extract Meeting Actions

## Goal

Из сырого текста встречи выделить задачи, вопросы и риски, а затем собрать короткий реестр задач в структурированном markdown.

## Inputs

- `examples/meeting_raw.txt`
- или вставленный сырой текст встречи

## Outputs

- черновик результата в `drafts/exercise/meeting_actions_draft.md`
- финальный результат в `outputs/exercise/meeting_actions.md`

Финальный файл должен содержать разделы:
- `Задачи`
- `Вопросы`
- `Риски`
- `Реестр задач`

## Success Criteria

- результат читается без дополнительного контекста
- задачи отделены от вопросов и рисков
- реестр задач пригоден для отправки в Telegram

## Out of Scope

- полная project management система
- автоматическое исполнение задач
- глубокий анализ meeting dynamics

## Procedure

1. Прочитай сырой текст встречи.
2. Отдели:
   - конкретные задачи
   - открытые вопросы
   - риски и блокеры
3. Для задач собери короткий реестр:
   - задача
   - владелец, если он явно понятен
   - срок, если он явно указан
4. Сначала собери черновик.
5. Сохрани черновик в `drafts/exercise/meeting_actions_draft.md`.
6. После подтверждения сохрани финальный результат в `outputs/exercise/meeting_actions.md`.

## Human Review

Если формулировка неоднозначна, лучше отметить неопределённость, чем придумывать владельца или срок.

## Example Usage

`Разбери meeting notes и выдели задачи, вопросы и риски`
