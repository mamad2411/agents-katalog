---
name: ordinal
description: "Use this skill to convert an integer to its ordinal string (1->1st, 22->22nd, 113->113th). Deterministic, offline. For ranks and dates."
compatibility: ">=1.0"
---

# ordinal

Use this skill to convert an integer to its ordinal string (1->1st, 22->22nd, 113->113th). Deterministic, offline. For ranks and dates.

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
python run.py --number <number>
```

**From a Python agent (ATEN runtime):**
```python
from skill_library import executor
result = executor.execute("ordinal", {number=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `number` | number | yes | Integer to convert |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
