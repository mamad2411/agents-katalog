---
name: parse-any-date
description: "Use this skill to parse a date/time from almost any format (ISO 8601, GMT/RFC, epoch seconds or millis, common US/EU formats), normalize it to UTC, and get a humanized 'time ago' string plus age in hours. Deterministic, offline. Handles the messy timestamps agents get from APIs and scraped pages."
compatibility: ">=1.0"
---

# parse-any-date

Use this skill to parse a date/time from almost any format (ISO 8601, GMT/RFC, epoch seconds or millis, common US/EU formats), normalize it to UTC, and get a humanized 'time ago' string plus age in hours. Deterministic, offline. Handles the messy timestamps agents get from APIs and scraped pages.

- **Kind**: tool  |  **Niche**: ai  |  **Cost tier**: free  |  **Version**: 0.1.0

## Empire Integration
```python
import sys
sys.path.insert(0, r'C:\D\Claude Code Projects\_SHARED')
import empire_bootstrap  # wires all shared paths
```

## Usage

**As a CLI:**
```bash
python run.py --value <string>
```

**From a Python agent (ATEN runtime):**
```python
from skill_library import executor
result = executor.execute("parse-any-date", {value=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `value` | string | yes | A date/time in any common format (or epoch number) |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
