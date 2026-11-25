---
name: case-convert
description: "Use this skill to convert an identifier between snake_case, camelCase, PascalCase, and kebab-case (to=snake|camel|pascal|kebab). Deterministic, offline. For code/config transforms."
compatibility: ">=1.0"
---

# case-convert

Use this skill to convert an identifier between snake_case, camelCase, PascalCase, and kebab-case (to=snake|camel|pascal|kebab). Deterministic, offline. For code/config transforms.

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
python run.py --text <string>
```

**From a Python agent (ATEN runtime):**
```python
from skill_library import executor
result = executor.execute("case-convert", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Input text |
| `to` | string | no | snake\|camel\|pascal\|kebab (default snake) |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
