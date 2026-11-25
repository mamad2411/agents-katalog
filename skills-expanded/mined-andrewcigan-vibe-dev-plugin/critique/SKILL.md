---
name: critique
description: FULL этап 5 — автономный critique long-list идей. Запускает idea-critic (Sonnet), который отсеивает hard-filters и оставляет Top-3-5 по score. Триггеры — "/critique", "отсей идеи", "критика".
when_to_use: После /expand-ideas. Автономный — не задаёт вопросов на каждой идее. Производит Top-3-5 для /validate.
---

# /critique

Автономная критика идей через idea-critic agent.

## Что происходит

1. Subagent `idea-critic` (Sonnet) читает ideas-round-1.md + round-2.md + domain-rules.yaml
2. Hard filters: отсев противоречащих invariants / anti-patterns / target_markets / budget
3. Scoring 5 критериев (1-5 каждый, max 25)
4. Top-3-5 на выход

## Output

- `docs/critique-log.md`

## Дальше

`/validate` — проверка бизнес-модели Top-3.

## Принцип

Не спрашивает пользователя на каждой идее. Решает автономно по критериям. Финальный отчёт — Top-3 с рекомендацией.
