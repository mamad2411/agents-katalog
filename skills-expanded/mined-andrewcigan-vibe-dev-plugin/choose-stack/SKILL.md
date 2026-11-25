---
name: choose-stack
description: Выбор стека под bottleneck архитектуры. Запускает stack-advisor (Fable 5.1). Использует 2026 tech-updates (opendataloader-pdf, VoxCPM2, chrome-devtools-mcp). Выбирает один стек, объясняет последствия. Триггеры — "/choose-stack", "выбери стек", "tech stack".
when_to_use: После /architecture (FAST) или /prototype (FULL). Перед /detail-architecture. Решает технологические вопросы за пользователя.
---

# /choose-stack

Выбор стека через stack-advisor agent.

## Что происходит

1. Subagent `stack-advisor` (Opus) читает ARCHITECTURE.md, best-practices, domain-rules.runtime_constraints + cost_policy
2. Match tech к bottleneck из архитектуры
3. Compose стек (один, не 3 варианта)
4. Cost оценка в $/мес
5. Trade-offs честно

## Output

- `docs/stack.md`
- `init.sh` создаётся / обновляется под выбранный стек

## Дефолтный стек (если нет противопоказаний)

- Frontend: Next.js 15 + shadcn/ui + Tailwind v4 + Inter
- Backend: Next.js API routes
- DB: Supabase + pgvector
- LLM: Claude через подписку (Opus критичное, Sonnet routine)
- Parsing: opendataloader-pdf
- Tests: chrome-devtools-mcp + vitest

## Финальное сообщение (обязательный формат)

Финализируй шаблоном B (см. `rules/message-finalization.md`):

```
Готово. Стек выбран — docs/stack.md.
<краткая сводка: frontend / backend / DB / LLM / parsing / tests, одна строка каждое>
Cost оценочно: ~$X/мес (в твоём бюджете $Y).
Главный trade-off: <одной фразой>.

Вопросов от меня нет. Следующий шаг — /detail-architecture (FULL) или сразу /dev-plan → /feature loop (FAST). Согласен?
```

**Без technical A/B**. Если есть выбор — рекомендация на первом месте: «Беру X — для твоего кейса даёт Y. Альтернатива была бы быстрее в разработке, но просела бы качество. Quality first.»

См. `rules/no-human-days.md` — без оценок в днях.
