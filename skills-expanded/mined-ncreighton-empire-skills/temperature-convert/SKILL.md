---
name: temperature-convert
description: "Use this skill to convert a temperature between Celsius, Fahrenheit, and Kelvin (from_unit/to_unit = C/F/K). Deterministic, offline."
compatibility: ">=1.0"
---

# temperature-convert

Use this skill to convert a temperature between Celsius, Fahrenheit, and Kelvin (from_unit/to_unit = C/F/K). Deterministic, offline.

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
python run.py --value <number>
```

**From a Python agent (ATEN runtime):**
```python
from skill_library import executor
result = executor.execute("temperature-convert", {value=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `value` | number | yes | Temperature value |
| `from_unit` | string | no | C/F/K (default C) |
| `to_unit` | string | no | C/F/K (default F) |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
