---
name: format-price
description: "Use this skill to format a numeric amount as a currency string with the correct symbol, thousands separators, and two decimals (USD, EUR, GBP, etc.). Handles ints, floats, and numeric strings. Deterministic, offline."
compatibility: ">=1.0"
---

# format-price

Use this skill to format a numeric amount as a currency string with the correct symbol, thousands separators, and two decimals (USD, EUR, GBP, etc.). Handles ints, floats, and numeric strings. Deterministic, offline.

- **Kind**: tool  |  **Niche**: reviews  |  **Cost tier**: free  |  **Version**: 0.1.0

## Empire Integration
```python
import sys
sys.path.insert(0, r'C:\D\Claude Code Projects\_SHARED')
import empire_bootstrap  # wires all shared paths
```

## Usage

**As a CLI:**
```bash
python run.py --amount <number>
```

**From a Python agent (ATEN runtime):**
```python
from skill_library import executor
result = executor.execute("format-price", {amount=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `amount` | number | yes | The amount |
| `currency` | string | no | ISO code (USD/EUR/GBP/JPY), default USD |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
