---
name: percent-change
description: "Use this skill to compute the percentage change from an old value to a new value, plus absolute change and direction. Handles old=0. Deterministic, offline. For metrics/analytics."
compatibility: ">=1.0"
---

# percent-change

Use this skill to compute the percentage change from an old value to a new value, plus absolute change and direction. Handles old=0. Deterministic, offline. For metrics/analytics.

- **Kind**: analyzer  |  **Niche**: reviews  |  **Cost tier**: free  |  **Version**: 0.1.0

## Empire Integration
```python
import sys
sys.path.insert(0, r'C:\D\Claude Code Projects\_SHARED')
import empire_bootstrap  # wires all shared paths
```

## Usage

**As a CLI:**
```bash
python run.py --old <number> --new <number>
```

**From a Python agent (ATEN runtime):**
```python
from skill_library import executor
result = executor.execute("percent-change", {old=..., new=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `old` | number | yes | Original value |
| `new` | number | yes | New value |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
