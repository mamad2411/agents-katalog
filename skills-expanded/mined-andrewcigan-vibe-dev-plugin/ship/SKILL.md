---
name: ship
description: Финальная доставка проекта — валидационная выборка ≥90% + ретроспектива всех уроков + (для FULL) marketing-launch пакет. Триггеры — "/ship", "запускаем продукт", "финал", "доставляем".
when_to_use: Когда все feature_list.json фичи в passing и пользователь готов финализировать. Это последний этап pipeline FAST (этап 5) и FULL (этап 10).
---

# /ship

Финальная доставка. Закрывает проект на текущей фазе или выпускает продукт.

## Pre-flight checks

### Check 1: Все фичи passing
```python
# feature_list.json
all_done = all(f['state'] == 'passing' for f in features['active_list'] + features['up_next'])
captured_can_be_postponed = len(features['captured']) >= 0  # captured допустимо
```

Если есть active без passing → STOP, продолжать /feature.

### Check 2: Build / Tests зелёные
```bash
./init.sh  # должен пройти полностью
```

## Validation Sample (≥90% gate)

**Это главный gate ship.** Без 90% — нет доставки.

### Если нет валидационной выборки

`validation-sample-builder` subagent создаёт:
- 50-100 реалистичных сценариев (синтетика ≤20%)
- Категории: базовый интент 60-70% / edge 15-20% / error 10-15%
- Ground truth для каждого
- Бинарная оценка yes/no

→ `docs/validation-sample.md` + `docs/validation-scenarios/S-*.md`

### Прогон

Запустить выборку на текущей сборке:
```bash
./validation-runs/run.sh
# или
python eval/run_validation.py
```

Результат:
- Pass rate: X%
- Per-category breakdown
- Failed scenarios → 5-Whys на каждый

### Gate
- **≥90% pass** → можно ship
- **<90%** → НЕ ship. Failed scenarios записать в backlog как новые фичи. Пользователю сказать прямо: «не дотянули до 90%, надо ещё N итераций».

## Retrospective (полная)

Запустить skill `claude-code-meta:retrospective` или собрать вручную:

### Что собирается
- Все error-journal записи проекта
- Все feedback_*.md из memory проекта
- Все stuck-statements
- Все decisions

### Структура retrospective.md
```markdown
# Retrospective: <project-name>
Date: YYYY-MM-DD
Duration: Started YYYY-MM-DD → Shipped YYYY-MM-DD (внешний календарь)
Features shipped: N (из N запланированных в Roadmap)

## Что получилось
- Features shipped: X
- Validation rate: Y%
- User satisfaction: <если есть метрика>

## Топ-3 повторяющиеся ошибки
1. <ошибка> — N раз — корневая причина — что зафиксировали в память
2. ...
3. ...

## Топ-3 удачных решений
1. <решение> — что сэкономило / улучшило

## Метрики харнеса
- Cold-start fail rate: X%
- /handoff compliance: Y%
- Auto-stuck triggers: Z (vs. ручных N)
- Cost overruns: <count>
- Recurrence rate: %

## Уроки для системы (предложение в ~/CLAUDE.md)
- <урок 1> — если confirm → промоушн в глобальные правила
- <урок 2>
```

Сохранить в `~/.vibe-dev/retrospectives/YYYY-MM-DD-<project>/retrospective.md`.

Обновить `~/.vibe-dev/retrospectives/INDEX.md` строкой:
```
| YYYY-MM-DD | [project](YYYY-MM-DD-<project>/retrospective.md) | Главный урок |
```

## Marketing Launch (только FULL режим)

Если режим = FULL, дополнительно запустить `marketing-launch-preparer` subagent.

Создаёт пакет в `docs/marketing-launch/`:
- product-marketing-context.md (ICP + позиционирование)
- messaging.md
- pricing-strategy.md
- landing-page-brief.md (для Claude Design)
- email-sequences.md
- launch-plan.md
- ...

Подтвердить с пользователем 1-2 ключевых решения (pricing, ICP) — ОДНО за раз.

## Delta-мёрж спеки + архивация (v8 L3-F6, OpenSpec archive)

Когда фичи завершены (passing → done) — влить их изменения в спеку и вынести в архив, чтобы «что зафиксировано» догоняло «что задумано», а горячий контекст оставался тонким.

### Шаг 1: Delta-мёрж в docs/ARCHITECTURE.md
Для каждой завершённой фичи собрать delta из провенанс-лога (`op`: ADDED/MODIFIED/REMOVED/RENAMED) и влить в `docs/ARCHITECTURE.md` в порядке **RENAMED → REMOVED → MODIFIED → ADDED** с валидацией конфликтов (одно требование не может быть в одной волне и MODIFIED, и REMOVED). Спека растёт органически.

### Шаг 2: Change-контекст в decisions
Папку детализации `docs/changes/<feat-id>/` (proposal/design/tasks) перенести в `docs/decisions/<YYYY-MM-DD>-<feat-id>/` — история решения сохраняется.

### Шаг 3: Ротация в архив (гейт)
```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/archive-features.sh" "$(pwd)"   # done/superseded/rejected с evidence → архив + индекс-стаб
```
**Гейт (block-архивации):** фича с незакрытыми tasks (`docs/changes/<id>/tasks.md` содержит `- [ ]`) НЕ архивируется — доделай задачи (OpenSpec `archive_tasks_incomplete`). done без evidence тоже не архивируется (доказательство обязательно, c10). Горячий `feature_list.json` остаётся тонким (индекс-стабы), тела — в `feature_list.archive.json`. git pre-commit блок 6 сверяет `evidence_hash` стаба с телом архива.

## Final commit

```bash
git tag v1.0.0
git commit -m "ship: v1.0.0

Validation rate: X%
Features shipped: Y
Retrospective: ~/.vibe-dev/retrospectives/YYYY-MM-DD-<project>/"
```

## Финальное сообщение пользователю

```
✓ /ship завершён

📊 Validation: X% (≥90 ✓ / <90 ✗)
✓ Features: Y shipped
📚 Retrospective: ~/.vibe-dev/retrospectives/YYYY-MM-DD-<project>/
💰 Total cost: $X
⏱️  Duration: N days

[Если FULL]
📢 Marketing pack: docs/marketing-launch/ (14 артефактов)

Проект отгружен. Если хочешь — могу:
- Запустить /audit финальный
- Начать новый проект (/new-project)
- Перевести этот в архив (/archive)
```

## Anti-patterns

- ❌ Ship без 90% validation
- ❌ Ship с кэптированными фичами в high priority
- ❌ Считать unit tests как validation
- ❌ Скип retrospective «у нас всё ок»
- ❌ Запуск marketing-launch без подтверждения pricing/ICP
