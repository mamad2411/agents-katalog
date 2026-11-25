---
name: validate
description: FULL этап 6 — автономная валидация бизнес-модели Top-3 идей. Запускает idea-validator (Sonnet) — TAM, конкуренты, monetization, риски. Validation score 0-100, gate ≥60. Триггеры — "/validate", "валидируй идеи", "проверка бизнес-модели".
when_to_use: После /critique. Проверяет жизнеспособность бизнес-модели до того как тратить время на architecture.
---

# /validate

Валидация бизнес-модели через idea-validator agent.

## Что происходит

1. Subagent `idea-validator` (Sonnet) читает critique-log.md → Top-3
2. WebSearch конкурентов (3 прямых + 3 косвенных)
3. Pricing анализ
4. Риски (регуляторные, технологические, конкурентные)
5. Validation score 0-100 для каждой

## Output

- `docs/validation.md`

## Пороги

- ≥80: ✓ двигаем в /research
- 60-79: 🟡 двигаем с оговорками
- <60: ❌ stop, переосмыслить

## Дальше

`/research` — параллельный ресёрч top-1-2 идей.

## Quality Gate

Финальное сообщение пользователю без technical A/B. Прямая рекомендация: «Берём C, A — следующая итерация».
