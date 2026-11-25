---
name: architecture
description: V0 архитектура с TOC bottleneck-анализом. Запускает architect (Fable 5.1). ≤10 компонентов, Mermaid диаграмма, invariants как constraints, top-3 риска. FAST + FULL обе используют. Триггеры — "/architecture", "архитектура", "spроектируй систему".
when_to_use: После интервью (FAST) или после /research (FULL). Создаёт docs/ARCHITECTURE.md как основу для choose-stack.
---

# /architecture

V0 архитектура через architect agent.

## Шаг 0 — ОБЯЗАТЕЛЬНЫЙ рисёрч (v6.2 F6; распоряжение владельца плагина 2026-06-10)

Перед архитектурой — детальный рисёрч best practices + GitHub-репо. Цена архитектурной
ошибки для непрограммиста выше цены рисёрча. **Hook блокирует запись docs/ARCHITECTURE*.md
без артефакта рисёрча** (architecture-research-gate).

```bash
# Маркер явного пропуска (его ставит ТОЛЬКО хук по фразе пользователя «пропусти рисёрч»):
if [ -f .harness/locks/research-skipped ]; then
  cat .harness/locks/research-skipped   # покажи цитату, потом ПОТРЕБИ маркер (одноразовый):
  rm .harness/locks/research-skipped
  # → рисёрч пропущен, иди к шагу 1
fi
```

Если маркера нет — запусти ПАРАЛЛЕЛЬНО двух агентов (они уже в плагине):
- `github-researcher` — ≥3 репо похожих систем, ≥1 клонировать и разобрать паттерны/анти-паттерны
- `best-practices-researcher` — ≥5 свежих практик по проблемным классам проекта

Сведи результаты в `docs/research/architecture-research.md`. Глубина по размеру проекта:
S (лендинг/прототип) — короткий обзор (по 1-2 источника на агента); M/L — полный.
НЕ спрашивай пользователя «делать ли рисёрч» — дефолт ДА; пропуск только его явной фразой.

## Что происходит

1. Subagent `architect` (Opus) читает CLAUDE.md, PRODUCT.md, domain-rules.yaml, **docs/research/*** (теперь и в FAST)
2. Identify bottleneck (TOC) — узкое место для главной функции
3. ≤10 компонентов (Karpathy Simplicity First)
4. Mermaid-диаграмма data flow
5. Invariants из domain-rules → архитектурные constraints
6. Top-3 риска с mitigation

## Output

- `docs/ARCHITECTURE.md`
- `docs/PRODUCT.md` (если ещё не было)

## Stage verifier check

После /architecture — `stage-verifier` подтверждает:
- Bottleneck явно указан
- Компонентов ≤10
- Mermaid присутствует

## Дальше

`/choose-stack` — стек под bottleneck.

## Quality Gate

Финальное сообщение без technical A/B. Прямой: «архитектура готова, узкое место — X, дальше /choose-stack».
