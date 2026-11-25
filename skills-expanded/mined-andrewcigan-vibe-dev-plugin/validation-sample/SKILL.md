---
name: validation-sample
description: Эталонная валидационная выборка 50-100 реалистичных сценариев. Запускает validation-sample-builder (Sonnet). Категории basic/edge/error, leak-prevention, bin yes/no. Финальный gate ≥90% перед /ship. Триггеры — "/validation-sample", "построй выборку", "эталон тесты".
when_to_use: FAST этап 8 после /dev-plan. FULL этап 13. До /feature loop. Также автоматически вызывается в /ship для финальной проверки.
---

# /validation-sample

Построение эталонной выборки через validation-sample-builder agent.

## Что происходит

1. Subagent `validation-sample-builder` (Sonnet) читает PRODUCT, ARCHITECTURE, domain-rules
2. Identify источники реалистичных сценариев:
   - User-provided data (приоритет)
   - Voice/chat logs old projects
   - Competitor reviews (WebSearch)
   - User-perspective-critic generated
   - Synthetic (≤20%)
3. Строит 50-100 scenarios в категориях:
   - basic_intent 60-70%
   - edge 15-20%
   - error 10-15%
4. **Leak prevention**:
   - `docs/validation-scenarios/inputs/` — только input
   - `docs/validation-scenarios/ground-truth/` — expected (только judge видит)
5. Запускает baseline run на текущей сборке (если есть код)

## Output

- `docs/validation-sample.md` — сводка
- `docs/validation-scenarios/inputs/*.md` — 50-100 сценариев
- `docs/validation-scenarios/ground-truth/*.md` — expected
- `./validation-runs/run-<ts>.jsonl` — результаты

## Critical gotchas

- **Leak prevention**: expected НЕ в одном файле с input
- **Judge contains rule**: YES если expected appears anywhere в Got, не exact match
- **Truncate Got >500 chars запрещён**

## Pass thresholds

- ≥90% → ✓ /ship
- 80-89% → 🟡 /ship с warnings, failed → backlog
- <80% → ❌ stop, 5 Why на failed scenarios

## Дальше

- Если pre-/feature loop — запоминаем baseline, /feature feat-001
- Если в /ship — финальный gate

## Cost cap

$3. Может занять до часа compute на judge.
