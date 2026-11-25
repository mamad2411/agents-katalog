---
name: research
description: FULL этап 7 — параллельный ресёрч через 3 subagent'а одновременно (github + market + best-practices). Через git worktrees для изоляции. Результаты собирает synthesizer. Триггеры — "/research", "ресерч", "глубокий анализ".
when_to_use: После /validate в FULL режиме. До /architecture. Дольёт реальные практики и аналоги в дизайн.
---

# /research

Параллельный многоисточниковый ресёрч.

## Что происходит

Запускаются **параллельно** через git worktrees:

1. **github-researcher** (Sonnet) → `docs/research/github-repos.md`
   - 3+ репо найдено, ≥1 клонирован
   - Архитектурные паттерны + anti-patterns

2. **market-researcher** (Sonnet) → `docs/research/market.md`
   - 3 прямых конкурента + 3 косвенных
   - Pricing landscape
   - UX-инсайты из отзывов

3. **best-practices-researcher** (Sonnet) → `docs/research/best-practices.md`
   - 5+ best practices из 2026
   - Tech-updates применимы к нам

После завершения всех 3 — `synthesizer` собирает в `docs/research/SUMMARY.md`.

## Output

- `docs/research/github-repos.md`
- `docs/research/market.md`
- `docs/research/best-practices.md`
- `docs/research/SUMMARY.md` (синтез)
- `.planning/RESEARCH.md` (краткий выжимка)

## Параллелизация

```bash
# 3 worktree для 3 субагентов
git worktree add ../worktrees/research-github -b research-github
git worktree add ../worktrees/research-market -b research-market
git worktree add ../worktrees/research-best -b research-best
```

## Cost

Total cap: ~$5 на ресёрч (3 × ~$1.50).

## Дальше

`/architecture` — V0 архитектура с учётом research findings.
