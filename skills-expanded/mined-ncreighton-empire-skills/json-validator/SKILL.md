---
name: json-validator
description: "Use this skill to check whether a string is valid JSON and describe its shape: top-level type, key count (objects) or length (arrays), and the specific parse error with line/column if invalid. Deterministic, offline. Great for validating LLM output before using it."
compatibility: ">=1.0"
---

# json-validator

Use this skill to check whether a string is valid JSON and describe its shape: top-level type, key count (objects) or length (arrays), and the specific parse error with line/column if invalid. Deterministic, offline. Great for validating LLM output before using it.

- **Kind**: analyzer  |  **Niche**: ai  |  **Cost tier**: free  |  **Version**: 0.1.0

## Empire Integration
```python
import sys
sys.path.insert(0, r'C:\D\Claude Code Projects\_SHARED')
import empire_bootstrap  # wires all shared paths
```

## Usage

**As a CLI:**
```bash
python run.py --text <string>
```

**From a Python agent (ATEN runtime):**
```python
from skill_library import executor
result = executor.execute("json-validator", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | The JSON string to validate |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
