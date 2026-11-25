---
name: prototype
description: HTML/CSS прототип для проверки user stories ДО реального кода. Запускает prototype-builder (Sonnet). Один главный flow, mock data, кликабельно. FULL этап 9. Триггеры — "/prototype", "клик прототип", "html макет".
when_to_use: FULL только, после /architecture. Дешёвая UX-валидация — пользователь подтверждает концепцию до того как пишем production-код.
---

# /prototype

HTML-прототип через prototype-builder agent.

## Что происходит

1. Subagent `prototype-builder` (Sonnet) читает PRODUCT.md, user-stories, ARCHITECTURE.md
2. Identify главный user flow (один!)
3. Build `prototype/index.html` (HTML + Tailwind CDN + inline mock data)
4. 1-3 экрана связанных, главный flow работает
5. Пользователь открывает в браузере и тестирует

## Output

- `prototype/index.html`
- (опц.) `prototype/screen-2.html`, `screen-3.html`

## НЕ делаем

- Финальный дизайн (для этого /design-handoff → Claude Design)
- Реальный backend (это не MVP)
- Все экраны (один flow)

## Дальше

После confirm пользователя — `/choose-stack`.

## Cost

$1.50. Без external API.
