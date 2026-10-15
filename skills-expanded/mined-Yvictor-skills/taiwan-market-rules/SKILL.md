---
name: taiwan-market-rules
description: Route, scope, and compare Taiwan market-rule questions across TWSE centralized securities, TPEx OTC and emerging markets, and TAIFEX futures and options. Use when the user does not identify the owning exchange, asks a cross-market question, compares 上市/上櫃/興櫃/期貨, or needs source selection across TWSE, TPEx, and TAIFEX. This is a thin router; use the exchange-specific skill for authoritative detail.
---

# Taiwan Market Rules

Route every question to its owning market before interpreting terminology. Do not duplicate the exchange-specific corpora in this skill.

Read `references/routing-matrix.md` for ambiguous terms, checked-in corpus routes, and multi-market comparisons. Use `references/cross-market-system-map.md` when the question crosses security order/settlement and derivatives position/margin/clearing models.

## Routing workflow

1. Extract product, venue, actor, account, lifecycle, and protocol clues.
2. Route the question:
   - TWSE, 上市, 集中市場, TWSE `O-xxx` manuals: use `../twse-market-rules/SKILL.md`.
   - TPEx, 櫃買, 上櫃, 興櫃, TPEx bonds or systems: use `../tpex-market-rules/SKILL.md`.
   - TAIFEX, 期交所, futures, options, TMP, positions, margin, or clearing: use `../taifex-market-rules/SKILL.md`.
3. If clues remain ambiguous, ask which venue applies or provide clearly separated venue-specific answers. Never silently choose one.
4. For comparisons, consult every relevant exchange-specific skill and current official sources.
5. Present common concepts first, then a per-market table with differences, source owner, document/version/date, and implementation impact.

## Source discipline

- Attach every precise rule to its owning exchange.
- Do not infer TPEx behavior from a TWSE manual merely because brokers share infrastructure or concepts.
- Do not infer TAIFEX position, margin, or clearing behavior from securities terminology.
- Browse official sources when freshness matters. State when a conclusion is a cross-source inference.
- Prefer `TWSE`, `TPEx`, and `TAIFEX` labels over the ambiguous phrase “交易所規定”.

## Cross-market output

Use a compact comparison table when two or more venues are involved. Include at least: venue, product/system, controlling source, terminology difference, and engineering consequence.

## Maintenance

After refreshing any child corpus, update snapshot counts and run:

```bash
uv run python scripts/audit_router.py
```
