---
name: dev-plan
description: Wave-план разработки через dev-planner (Fable 5.1) + reordering-agent (Sonnet 5). Каждая секция → feature в feature_list.json с affected_files, verification, business_invariant, size_estimate. ROADMAP.md + waves. Триггеры — "/dev-plan", "wave план", "план разработки".
when_to_use: FAST после /detail-architecture / /choose-stack. FULL после /design-handoff. Превращает архитектуру в выполнимый план через feature_list.json.
---

# /dev-plan

Wave-план через dev-planner agent.

## Что происходит

1. Subagent `dev-planner` (Opus) читает architecture-detail.md, phases.md, domain-rules
2. Map sections → features в feature_list.json
3. Каждая feature получает:
   - id, name, description, wave
   - dependencies (от каких других)
   - size_estimate (S/M/L → light/heavy path в /feature)
   - affected_files явно
   - verification (4-layer)
   - business_invariant ссылка на domain-rules.invariants
   - budget_usd
4. `reordering-agent` валидирует DAG (нет циклов)

## Output

- Обновлённый `feature_list.json` (captured + up_next)
- `docs/ROADMAP.md`

## Stage verifier

- Все features имеют affected_files
- Все features имеют verification
- DAG без циклов
- Total budget ≤ monthly_total_budget_usd

## Дальше

`/validation-sample` — строим эталонную выборку.

После — `/feature feat-001` (первая фича из Wave 1).

## Финальное сообщение (обязательный формат)

Финализируй шаблоном B (см. `rules/message-finalization.md`):

```
Готово. Wave-план: 8 фичей в 3 волнах, docs/ROADMAP.md обновлён.

Волна 1 (parallel, 2 фичи): foundation (database + auth)
Волна 2 (зависит от 1, 3 фичи): API + business logic
Волна 3 (зависит от 2, 3 фичи): UI + integrations

Объём: 8 фичей (5×M + 3×L). Critical path: 5 фичей.
LLM-cost оценочно: ~$X на all features.
Внешняя рамка поставки клиенту: <из cost_policy / domain-rules>.

Вопросов от меня нет. Следующий шаг — /validation-sample (эталонная выборка 50-100 сценариев). Согласен?
```

**НЕ оценивать в человеко-днях.** См. `rules/no-human-days.md` — используем количество фичей + size_estimate (S/M/L). Внешний дедлайн клиента в днях — допустим только как «внешняя рамка поставки», не «бюджет нашей работы».
