---
name: expand-ideas
description: FULL pipeline этап 3 — генерация идей в 2 раунда. Запускает idea-generator (Opus), создаёт ideas-round-1.md с 10+ идей с обоснованием и 2-3 интерпретациями каждая. Триггеры — "/expand-ideas", "идеи R1", "генерируй идеи".
when_to_use: После /new-project в FULL режиме. Перед /critique. Создаёт long-list идей для последующего отсева.
---

# /expand-ideas

Генерация идей через idea-generator agent.

## Что происходит

1. Запускается subagent `idea-generator` (Opus)
2. Читает: CLAUDE.md, PRODUCT.md, domain-rules.yaml
3. Создаёт `docs/ideas-round-1.md` (10+ идей)
4. Просит пользователя пометить «берём / не берём» (1 простой вопрос)
5. После фидбэка — Round 2 (углубление выбранных)

## Output

- `docs/ideas-round-1.md`
- `docs/ideas-round-2.md` (после фидбэка)

## Дальше

`/critique` — автономный отсев long-list.

## Когда skip

- FAST режим (там сразу к /architecture)
- Уже есть чёткая идея от пользователя
