---
name: audit
description: 7-tuple оценка здоровья проекта (Instructions / State / Verification / Scope / Lifecycle / Learning / Cost-Safety) через ВНЕШНЕГО evaluator-agent (не self-bias). Бонус — error velocity, recurrence rate, top root-causes. Триггеры — "/audit", "оценка проекта", "состояние харнеса".
when_to_use: Раз в неделю или при подозрении что что-то «не так». Регулярный диагностический инструмент.
---

# /audit

Внешняя оценка здоровья проекта. Закрывает self-bias из критики v5.0.

## Главная защита: External Evaluator

`/audit` НЕ оценивает себя. Запускает отдельный subagent (Sonnet, fresh context) с **read-only** доступом к артефактам проекта. Этот subagent НЕ читает `.harness/assessment.json` от предыдущего аудита — иначе он будет подвержен self-bias.

### Subagent промпт-шаблон:
```
Ты — независимый аудитор проекта. Не работаешь с этой кодовой базой.
Прочитай ТОЛЬКО:
- CLAUDE.md
- README.md (для людей)
- feature_list.json
- SESSION.md
- domain-rules.yaml
- error-journal.md (если есть)
- docs/ARCHITECTURE.md, docs/PRODUCT.md
- .harness/tools-allowlist.yaml (если есть)
- последние 10 коммитов git log

НЕ читай: предыдущие assessment, прошлые audit results.

Оцени 7 подсистем по шкале 1-5:
- 1: отсутствует или вредна
- 2: weak, inconsistent
- 3: adequate, basics covered
- 4: good, minor gaps
- 5: exemplary, enforced

Для каждой — конкретное обоснование (1-2 строки).
Найди bottleneck (наименьший балл) — это первый приоритет улучшения.
```

## 7-tuple assessment

| # | Подсистема | Что проверяет |
|---|---|---|
| 1 | **Instructions** | CLAUDE.md ≤200 строк, domain-rules.yaml заполнен, нет монолита |
| 2 | **State** | feature_list.json валиден, SESSION.md свежий, нет дублирования |
| 3 | **Verification** | 4-layer применяется, negative-gate работает, dual critique для L фичей |
| 4 | **Scope** | WIP=1 не нарушено, affected_files указаны, no scope-leak |
| 5 | **Lifecycle** | init.sh чист, 5-dim clean-exit при handoff, cold-start test проходит |
| 6 | **Learning** | error-journal не дамп, lessons промотированы, recurrence_rate=0%, domain-rules не устарел |
| 7 | **Cost & Safety** | tools-allowlist enforced, pre-launch-checklist используется, нет секретов в git |

## Дополнительные метрики

### Error Velocity
```
errors_per_session_avg_last_7_days = ?
```
Тренд — растёт ли скорость ошибок?

### Recurrence Rate (CRITICAL)
```python
# % ошибок которые уже были раньше
recurrence_rate = recurring_errors / total_errors * 100
```
**Цель: 0%.** Если >0% — Learning subsystem недостаточна, урок не дошёл до памяти или памяти не читают.

### Top 3 Root-Cause Classes
Из error-journal — какие классы ошибок преобладают?
- `api_research` — закрыть через pre-launch-checklist
- `concurrent_write` — через tools-allowlist
- `domain_knowledge` — через update domain-rules.yaml
- `scope_leak` — через WIP=1 hook
- `state_drift` — через handoff discipline
- ...

### Freshness checks
- domain-rules.yaml `last_reviewed` — старше N сессий?
- CLAUDE.md — обновлялся в этой фазе проекта?
- README.md — соответствует ли текущей реальности?

## Cost snapshot
```
Cost this week: $X
Cost total in project: $X
Per-feature avg: $X
Trend: ↑ / ↓ / flat
```

## Единая цифра готовности харнеса (v8 L5-F5, c11)

Сведи здоровье в ОДИН показатель — чтобы владелец видел готовность одним взглядом, а не читал 7 баллов.

1. Запусти объективные метрики (детерминированы из файлов, без LLM):
```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/audit-health.sh"
```
Печатает `provenance_integrity` / `archive_evidence` / `budget_coverage` / `health_objective`.

2. **Единая цифра = МИНИМУМ** (узкое место, не среднее) двух осей:
   - `bottleneck 7-tuple × 20` (субъективная — мин. балл подсистемы от evaluator);
   - `health_objective` (объективная — провенанс/архив-целостность).

Провал provenance-integrity (дырявая история требований, c4) или отсутствие evidence у архивной фичи (c10) штрафует цифру напрямую. Экранные детекторы (clarity/secret-mask) — display-only, честно НЕ в enforcement-счёт и НЕ в эту цифру. **Диагностика, не гейт** — /audit не блокирует, а показывает.

## Output

### File: SESSION.md → секция "Last Audit"
```markdown
## Last Audit

**Date**: YYYY-MM-DD (by external evaluator, fresh context)

**7-tuple scores**:
- Instructions: 4/5 — CLAUDE.md норма, нет topic-files в docs/
- State: 3/5 — feature_list.json валиден, SESSION.md устарел на 3 дня
- Verification: 2/5 — bottleneck! negative-gate не используется
- Scope: 5/5 — WIP=1 enforced корректно
- Lifecycle: 4/5 — init.sh работает, cold-start.yaml не обновлён
- Learning: 3/5 — error-journal есть, lessons промотированы 60%
- Cost & Safety: 5/5 — tools-allowlist enforced, секретов в git нет

**Bottleneck**: Verification (2/5)
**Recommendation**: добавить negative-verification на текущей фиче перед /verify

**Recurrence rate**: 0% (good)
**Error velocity**: 3 ошибки за неделю (low)
**Cost trend**: $5/week, flat
```

### Bottleneck → действие
- Если Verification < 3: STOP, чинить тесты ДО любой новой фичи
- Если Learning > Recurrence Rate >0%: STOP, разбирать почему уроки не работают
- Если Cost & Safety < 4: STOP, security audit

## Anti-patterns

- ❌ Запускать `/audit` тем же агентом который работал в сессии (self-bias)
- ❌ Игнорировать bottleneck «потом починим»
- ❌ Усреднять оценки — bottleneck это самая слабая, не average
- ❌ Хранить assessment.json внутри проекта (закрывает self-bias — оно в SESSION.md)
