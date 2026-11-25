---
name: design-handoff
description: Бриф для Claude Design (claude.ai/design) по формуле C.R.O.P. Плагин не рисует UI сам — готовит handoff. Запускает design-handoff-builder (Opus). FAST этап 3 / FULL этап 11. Триггеры — "/design-handoff", "claude design бриф", "дизайн UI".
when_to_use: Когда нужен дизайн UI. Если проект без UI — skip. Пользователь открывает Claude Design, вставляет brief, получает дизайн, возвращается.
---

# /design-handoff

Подготовка дизайн-брифа через design-handoff-builder agent.

## Что происходит

1. Subagent `design-handoff-builder` (Opus) читает PRODUCT.md, ARCHITECTURE.md, user-stories
2. Identify UI scope (1-3 экрана FAST, 5-10 FULL)
3. User flows для каждого экрана
4. Components required (что нужно — header, cards, modals, etc.)
5. Design brief по C.R.O.P. (Context / Requirements / Output / Patterns)

## Output

- `docs/design-brief.md` — главный артефакт для Claude Design
- `docs/design-handoff/user-flows.md`
- `docs/design-handoff/components-required.md`

## Что делает пользователь

1. Открывает claude.ai/design
2. Создаёт проект
3. Прикрепляет 3 файла из docs/design-handoff/ + docs/design-brief.md
4. Просит: «Сделай дизайн по этому брифу. Покажи 3 главных экрана.»
5. Итерирует до результата

Когда дизайн готов:
- Скачивает экспорт (TSX / HTML)
- В src/components/ или скриншоты в docs/design-handoff/output/
- Сообщает: «дизайн готов»
- Продолжаем pipeline

## Skip когда

- Проект без UI (pure CLI / API / cron)
- Уже есть готовая дизайн-система

## Stack дефолт для дизайна

shadcn/ui + Tailwind v4 + Inter (cyrillic + latin)
