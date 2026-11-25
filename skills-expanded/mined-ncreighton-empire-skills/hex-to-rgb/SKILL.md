---
name: hex-to-rgb
description: "Use this skill to convert a hex color (#rrggbb or #rgb) to RGB values and a css rgb() string. Deterministic, offline."
compatibility: ">=1.0"
---

# hex-to-rgb

Use this skill to convert a hex color (#rrggbb or #rgb) to RGB values and a css rgb() string. Deterministic, offline.

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
python run.py --hex <string>
```

**From a Python agent (ATEN runtime):**
```python
from skill_library import executor
result = executor.execute("hex-to-rgb", {hex=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `hex` | string | yes | Hex color, e.g. #1a2b3c |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
