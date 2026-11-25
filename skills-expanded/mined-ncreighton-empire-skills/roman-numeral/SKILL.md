---
name: roman-numeral
description: "Use this skill to convert an integer (1-3999) to a Roman numeral, or a Roman numeral back to an integer (to=roman|int). Deterministic, offline."
compatibility: ">=1.0"
---

# roman-numeral

Use this skill to convert an integer (1-3999) to a Roman numeral, or a Roman numeral back to an integer (to=roman|int). Deterministic, offline.

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
result = executor.execute("roman-numeral", {value=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `value` | string | yes | Integer or roman numeral |
| `to` | string | no | roman (default) or int |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
