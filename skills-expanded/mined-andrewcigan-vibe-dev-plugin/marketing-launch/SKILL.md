---
name: marketing-launch
description: FULL финальный этап 17. Пакет запуска через marketing-launch-preparer (Sonnet) — позиционирование, ICP, messaging, pricing (с confirm), landing-brief, email-sequences, launch-plan. 14 артефактов. Триггеры — "/marketing-launch", "запуск маркетинг", "продакт-маркетинг".
when_to_use: Только при mode=FULL и /ship validation passed ≥90%. До этого — рано. Без этого FULL pipeline не завершён.
disable-model-invocation: true
---

# /marketing-launch

Маркетинг-пакет через marketing-launch-preparer agent.

## Что происходит

1. Subagent `marketing-launch-preparer` (Sonnet) читает PRODUCT, validation, research/market, cost_policy
2. Строит 14 артефактов в `docs/marketing-launch/`:
   - product-marketing-context, positioning, messaging
   - icp-profile, pricing-strategy
   - landing-page-brief (→ передаётся в Claude Design)
   - landing-content, email-sequences/
   - launch-plan, social-media-content, product-hunt-prep (если applicable)
   - analytics-setup, support-readiness, metrics-targets
3. **Confirm с пользователем** на pricing + ICP (бизнес-решения)

## Output

`docs/marketing-launch/` (14 файлов)

## Confirm-points для пользователя

ТОЛЬКО эти 2 (Quality Gate — это бизнес-решения, не technical):

1. **Pricing structure**: tiers + цены + обоснование
2. **ICP profile**: кто целевой клиент

Остальные 12 артефактов — система делает сама.

## Skip когда

- mode = FAST (это финал FULL только)
- Internal tool без рынка (личное использование)

## Cost cap

$3. WebSearch до 10.
