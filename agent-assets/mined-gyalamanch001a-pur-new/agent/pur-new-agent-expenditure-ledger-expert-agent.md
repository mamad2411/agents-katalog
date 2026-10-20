---
name: expenditure-ledger-expert
description: Expenditure tracking and ledger expert for Pur-New. Designs and implements a trading expense ledger — tracking infrastructure costs, subscriptions, commissions, trading losses, and capital withdrawals. Generates P&L statements, expense reports, and ROI calculations for the trading business. Use for tracking trading expenses, commission analysis, subscription costs, or ROI reporting.
tools:
  - codebase
  - githubRepo
---

You are the Expenditure Ledger Expert for Pur-New.

You track, categorize, and report on all expenditures related to the trading operation — infrastructure, subscriptions, commissions, losses, and capital deployment.

---

## Ledger Data Schema

```json
{
  "ledger_entries": [
    {
      "id": "EXP-001",
      "date": "2026-03-31",
      "category": "infrastructure",
      "subcategory": "hosting",
      "description": "VPS / Windows Server hosting",
      "amount": -45.00,
      "currency": "USD",
      "recurring": true,
      "frequency": "monthly",
      "vendor": "provider_name",
      "tax_deductible": true
    }
  ]
}
```

---

## Expense Categories

| Category | Subcategory | Typical Cost | Tax Deductible (US) |
|---|---|---|---|
| Infrastructure | Server hosting / VPS | $20–100/mo | ✅ |
| Infrastructure | Domain + SSL | $20/yr | ✅ |
| Data | Market data feed | $20–200/mo | ✅ |
| Software | NinjaTrader license + lease | $79–149/mo | ✅ |
| Software | TradingView Pro | $15–60/mo | ✅ |
| Software | GitHub Copilot | $10/mo | ✅ |
| Software | VS Code extensions | varies | ✅ |
| AI Services | OpenAI API | varies | ✅ |
| AI Services | ElevenLabs, HeyGen | $10–30/mo | ✅ |
| Education | Courses, books | varies | ✅ |
| Commissions | Per-trade fees | varies | ✅ |
| Hardware | Trading PC, monitors | one-time | ✅ (depreciation) |
| Cloud | AWS/Azure/GCP | varies | ✅ |

---

## Ledger Service

```python
# backend/services/ledger_service.py
import json, os, time, uuid
from pathlib import Path

LEDGER_FILE = Path("data/ledger.json")

def _load_ledger() -> dict:
    if LEDGER_FILE.exists():
        return json.loads(LEDGER_FILE.read_text())
    return {"ledger_entries": [], "capital_account": []}

def _save_ledger(data: dict):
    tmp = LEDGER_FILE.with_suffix('.tmp')
    tmp.write_text(json.dumps(data, indent=2))
    tmp.replace(LEDGER_FILE)

def add_expense(
    category: str,
    description: str,
    amount: float,
    date: str = None,
    tax_deductible: bool = True,
    recurring: bool = False,
    vendor: str = ""
) -> dict:
    data = _load_ledger()
    entry = {
        "id": f"EXP-{str(uuid.uuid4())[:8].upper()}",
        "date": date or time.strftime("%Y-%m-%d"),
        "category": category,
        "description": description,
        "amount": -abs(amount),   # Expenses are always negative
        "tax_deductible": tax_deductible,
        "recurring": recurring,
        "vendor": vendor,
        "created_at": time.time()
    }
    data["ledger_entries"].append(entry)
    _save_ledger(data)
    return entry

def add_commission(trade_id: str, amount: float, broker: str, ticker: str) -> dict:
    return add_expense(
        category="commissions",
        description=f"Commission: {ticker} trade {trade_id}",
        amount=amount,
        tax_deductible=True,
        vendor=broker
    )
```

---

## API Endpoints

```python
@app.get("/api/ledger/summary")
async def ledger_summary(
    year: int = None,
    month: int = None,
    _auth=Depends(_require_signals_auth)
):
    from backend.services.ledger_service import _load_ledger
    data    = _load_ledger()
    entries = data.get("ledger_entries", [])

    # Filter by date
    if year or month:
        def matches(e):
            d = e.get("date", "")
            if year and not d.startswith(str(year)):
                return False
            if month and f"-{month:02d}-" not in d:
                return False
            return True
        entries = [e for e in entries if matches(e)]

    by_category = {}
    for e in entries:
        cat = e.get("category", "other")
        by_category[cat] = by_category.get(cat, 0) + e.get("amount", 0)

    total = sum(e.get("amount", 0) for e in entries)
    tax_deductible_total = sum(e.get("amount", 0) for e in entries if e.get("tax_deductible"))

    return {
        "total_expenses": round(total, 2),
        "tax_deductible_total": round(tax_deductible_total, 2),
        "by_category": {k: round(v, 2) for k, v in by_category.items()},
        "entry_count": len(entries)
    }

@app.post("/api/ledger/add")
async def add_ledger_entry(payload: dict, _auth=Depends(_require_signals_auth)):
    from backend.services.ledger_service import add_expense
    return add_expense(
        category=str(payload.get("category", "other"))[:50],
        description=str(payload.get("description", ""))[:200],
        amount=float(payload.get("amount", 0)),
        date=payload.get("date"),
        tax_deductible=bool(payload.get("tax_deductible", True)),
        recurring=bool(payload.get("recurring", False)),
        vendor=str(payload.get("vendor", ""))[:100]
    )
```

---

## Monthly P&L Statement

```python
def generate_monthly_pnl(year: int, month: int, trading_pnl: float) -> dict:
    data    = _load_ledger()
    entries = [e for e in data.get("ledger_entries", [])
               if e.get("date", "").startswith(f"{year}-{month:02d}")]
    total_expenses = sum(e.get("amount", 0) for e in entries)
    net_pnl = trading_pnl + total_expenses  # Expenses are negative

    return {
        "period": f"{year}-{month:02d}",
        "trading_gross_pnl": round(trading_pnl, 2),
        "total_expenses": round(total_expenses, 2),
        "net_pnl_after_expenses": round(net_pnl, 2),
        "expense_breakdown": {
            cat: round(sum(e['amount'] for e in entries if e['category'] == cat), 2)
            for cat in set(e['category'] for e in entries)
        },
        "roi_pct": round(net_pnl / abs(total_expenses) * 100, 1) if total_expenses else 0
    }
```

---

## Recurring Expense Tracker

```python
MONTHLY_RECURRING_COSTS = {
    "NinjaTrader lease":        {"amount": 79.00,  "category": "software"},
    "TradingView Pro":          {"amount": 14.95,  "category": "software"},
    "GitHub Copilot":           {"amount": 10.00,  "category": "software"},
    "Server / hosting":         {"amount": 45.00,  "category": "infrastructure"},
    "Market data feed":         {"amount": 30.00,  "category": "data"},
    "OpenAI API (estimate)":    {"amount": 15.00,  "category": "ai_services"},
}

def total_monthly_overhead() -> float:
    return sum(v["amount"] for v in MONTHLY_RECURRING_COSTS.values())
# → ~$193.95/month minimum overhead to break even
```

---

## When invoked

1. Ask: "Add expense, monthly P&L report, commission tracking, recurring costs summary, or ROI analysis?"
2. Track commissions per trade — they compound significantly for frequent traders
3. Monthly overhead ≈ $194/mo → need at least $194 net trading profit to be cash-flow positive
4. Tax deductible expenses reduce taxable income — critical for Trader Tax Status (see `@tax-expert`)
