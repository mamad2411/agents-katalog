---
name: trim
description: '"Бюджет горит" режим. Система берёт backlog, определяет MVP-минимум и предлагает что срезать. Триггеры — "/trim", "ужми scope", "бюджет горит", "режим экономии".'
when_to_use: Когда пользователь говорит что бюджет/время поджимает и нужно ужать scope до критического минимума.
disable-model-invocation: true
---

# /trim

Закрывает боль «бюджет горит, не знаю что выкинуть».

## Что происходит

### Шаг 1: Прочитать текущий состав backlog

```python
import json
d = json.load(open('feature_list.json'))

all_features = []
for state in ['captured', 'up_next', 'active_list', 'done']:
    all_features.extend(d['features'][state])
```

### Шаг 2: Subagent делает MVP-анализ

Subagent (Sonnet) с инструкцией:

```
Прочитай:
- docs/PRODUCT.md (главная функция, ценность)
- domain-rules.yaml → product_semantics, invariants
- feature_list.json все фичи
- SESSION.md → последние решения

Задача: определить MVP-минимум для главной ценности продукта.

Раздели фичи на:
- **MUST**: критично для главной функции. Без них продукта нет.
- **SHOULD**: улучшают, но MVP без них работает.
- **NICE**: красиво иметь, не нужны для MVP.

Для каждой группы — короткое обоснование.
```

### Шаг 3: Предложение пользователю

**Format (по Quality Gate — НЕ technical A/B):**

```
Слышу, бюджет жмёт. Прошёлся по 12 фичам:

MVP-минимум (5 фичей, ~$X, ~2 недели):
✓ feat-001 — Загрузка документов
✓ feat-003 — Базовый поиск
✓ feat-005 — Главный экран
✓ feat-008 — Авторизация
✓ feat-010 — Push-уведомления

Можно срезать без потери главной ценности (7 фичей, экономия ~$Y, ~3 недели):
✗ feat-002 — Bulk-импорт (можно вручную пока)
✗ feat-004 — Расширенные фильтры
✗ feat-006 — Темы оформления
✗ feat-007 — Экспорт в Excel
✗ feat-009 — Аналитика
✗ feat-011 — Multi-tenant
✗ feat-012 — API для партнёров

Моя рекомендация: режем 7. Получаем MVP за 2 недели вместо 5.
По завершении MVP — можем добавить срезанные одну за другой по приоритету.

Согласен? (д / нет / поправь)
```

### Шаг 4: Применить (если confirm)

```python
# Перевести фичи в superseded или сохранить как captured с пониженным приоритетом
for feat_id in to_trim:
    d['features']['captured'].append(d['features'][source_state].pop(feat_id))
    d['features'][feat_id]['state'] = 'captured'
    d['features'][feat_id]['notes'] = 'trimmed for MVP, return later'
    d['features'][feat_id]['trimmed_at'] = today
```

Записать в `docs/decisions/`:
```markdown
# decision-<n>: MVP trim YYYY-MM-DD

## Context
Бюджет/время поджимает. Решили ужать scope до MVP-минимума.

## Decision
Оставлены: feat-001/003/005/008/010 (главная ценность).
Срезаны на потом: feat-002/004/006/007/009/011/012.

## Consequences
- MVP за ~2 недели (vs ~5)
- Срезанные фичи в captured, вернёмся после ship MVP
- Экономия $Y
```

### Шаг 5: Auto-commit

```bash
git add feature_list.json docs/decisions/
git commit -m "trim: MVP scope (7 features postponed)"
```

### Шаг 6: Обновить SESSION.md
- Active feature → первая из MUST (если ещё не выбрана)
- Notes for Next Session: «MVP trim применён, идём по 5 фичам до /ship»

## Что НЕ делать

- ❌ Сразу удалять срезанные фичи — они в captured с пометкой trimmed
- ❌ Trim без confirm пользователя
- ❌ Trim во время active фичи — сначала /handoff
- ❌ Trim если режим LIGHT и фич мало (<5)

## Anti-patterns

- Предлагать «вариант A: режем X, вариант B: режем Y» — Quality Gate ловит. Делаешь сам и объясняешь.
- Прятать срезанные фичи (удалять из json) — они в captured «trimmed»
- Не давать оценку экономии в $ / днях
