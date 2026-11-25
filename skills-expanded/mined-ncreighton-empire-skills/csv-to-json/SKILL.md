---
name: csv-to-json
description: "Use this skill to convert CSV text into a list of JSON records, auto-detecting the delimiter (comma, semicolon, tab, or pipe) and using the first row as headers. Handles ragged rows. Deterministic, offline. The reliable first step before processing spreadsheet exports."
compatibility: ">=1.0"
---

# csv-to-json

Use this skill to convert CSV text into a list of JSON records, auto-detecting the delimiter (comma, semicolon, tab, or pipe) and using the first row as headers. Handles ragged rows. Deterministic, offline. The reliable first step before processing spreadsheet exports.

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
python run.py --csv <string>
```

**From a Python agent (ATEN runtime):**
```python
from skill_library import executor
result = executor.execute("csv-to-json", {csv=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `csv` | string | yes | CSV text to parse |
| `delimiter` | string | no | Force a delimiter (default: auto-detect) |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
