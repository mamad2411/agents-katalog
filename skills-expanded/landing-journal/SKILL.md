---
name: landing-journal
description: Аудит-журнал изменений лендингов и A/B-экспериментов — «память об изменениях». Записывает и показывает структурированную историю событий (создание лендинга, добавление варианта, запуск теста, сбор статистики, решение, раскат). Использовать, когда нужно зафиксировать изменение по лендингу/эксперименту или посмотреть полную историю для аудита. Другие landing-скиллы вызывают его скрипт log_event.py.
---

# landing-journal — память об изменениях (аудит)

Сквозной журнал по всем лендингам и экспериментам. Отвечает на вопросы аудита: **что менялось,
когда, кто, почему и с каким результатом**. Это фундамент для `landing-experiment` и будущих
`landing-ads` / `landing-stats` — они дописывают сюда свои события.

## Где лежат данные

- `experiments/journal.jsonl` — **источник правды**, append-only (по JSON-строке на событие).
- `experiments/journal.md` — та же лента, читаемая людьми (автогенерируется, не редактировать).
- `experiments/<experiment-id>/` — карточки конкретных экспериментов (ведёт `landing-experiment`).
- **git** — нижний слой аудита: каждое событие фиксируется коммитом, его хеш попадает в запись.

## Записать событие

```bash
python3 .claude/skills/landing-journal/scripts/log_event.py \
  --event <тип> --summary "что произошло" \
  [--landing <slug>] [--experiment <id>] [--actor <кто>] [--details "<текст|json>"]
```

Типы событий: `landing_created`, `variant_added`, `experiment_designed`, `launched`, `paused`,
`stats_collected`, `decided`, `rolled_out`, `rolled_back`, `changed`, `note`.

**Правило:** каждое значимое действие над лендингом/экспериментом сопровождается записью в
журнал — желательно тем же коммитом, что и само изменение (чтобы хеш в записи указывал на него).

## Посмотреть историю

```bash
python3 .claude/skills/landing-journal/scripts/show_history.py \
  [--landing <slug>] [--experiment <id>] [--event <тип>] [--limit N]
```

## Как это используют другие скиллы

- `new-landing` → `landing_created` после создания лендинга.
- `landing-experiment` → `experiment_designed` / `variant_added` / `launched` / `decided` / `rolled_out`.
- `landing-stats` (будущее) → `stats_collected` с цифрами по вариантам.
- `landing-ads` (будущее) → `changed`/`note` о подготовленных кампаниях/UTM.

## Принцип

«Ничего не теряется»: незавершённые эксперименты остаются в журнале с последним статусом и
следующим шагом. История неизменяема (append-only + git) — записи не переписываем, при ошибке
добавляем корректирующую запись (`note`).
