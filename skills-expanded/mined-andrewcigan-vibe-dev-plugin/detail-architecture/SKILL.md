---
name: detail-architecture
description: Детальная архитектура после выбора стека. Запускает architect + reordering-agent. API контракты, data models, обработка ошибок, secondary компоненты. DAG зависимостей для последующего dev-plan. Триггеры — "/detail-architecture", "детальная арх", "разверни архитектуру".
when_to_use: FULL pipeline этап 10. После /choose-stack. До /design-handoff.
---

# /detail-architecture

Детализация архитектуры через 2 агента.

## Что происходит

1. Subagent `architect` (Opus) расширяет V0:
   - API endpoint contracts (paths, methods, request/response schemas)
   - Data models (схемы БД)
   - Обработка ошибок (где и как)
   - Каждая абстракция обоснована ≥3 случаями

2. Subagent `reordering-agent` (Sonnet) строит DAG зависимостей:
   - Topological sort секций
   - Waves для параллельной разработки
   - Critical path

## Output

- `docs/architecture-detail.md`
- `docs/phases.md` (waves + DAG)

## Stage verifier

- Все компоненты детализированы
- API контракты
- Модели данных
- Каждая абстракция обоснована

## Дальше

`/design-handoff` (если UI) или `/dev-plan` (если нет UI).
