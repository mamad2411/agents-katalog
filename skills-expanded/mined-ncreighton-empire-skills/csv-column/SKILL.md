---
name: csv-column
description: "Use this skill to extract a single column's values from CSV text by header name or index. Deterministic, offline. For pulling one field out of a spreadsheet export."
compatibility: ">=1.0"
---

# csv-column

Use this skill to extract a single column's values from CSV text by header name or index. Deterministic, offline. For pulling one field out of a spreadsheet export.

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
python run.py --csv <string> --column <string>
```

**From a Python agent (ATEN runtime):**
```python
from skill_library import executor
result = executor.execute("csv-column", {csv=..., column=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `csv` | string | yes | CSV text |
| `column` | string | yes | Header name or 0-based index |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
