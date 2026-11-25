---
name: portfolio-pnl-calculator
description: Deterministic Decimal oracle for MarketScope portfolio valuation and P&L. Used to independently verify generated financial logic.
---

# Portfolio P&L Calculator

Use this skill as an independent numerical oracle during planning, TDD, evaluation, and self-healing.

It calculates:

- `total_invested`
- `current_value`
- `absolute_pnl`
- `percent_pnl`

## Fixed-point contract

- Decimal only
- scale: 4 decimal places
- rounding: ROUND_HALF_UP
- no binary floating-point conversion

## Invocation

```bash
python .claude/skills/portfolio-pnl-calculator/pnl_calculator.py --input <json-file>
```

Input:

```json
{
  "holdings": [
    {
      "quantity": "10.0000",
      "average_buy_price": "100.0000",
      "current_price": "110.0000"
    }
  ]
}
```

All financial outputs are strings with four decimal places.
