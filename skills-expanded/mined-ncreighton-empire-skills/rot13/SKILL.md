---
name: rot13
description: "Use this skill to apply the ROT13 cipher to text (its own inverse). Deterministic, offline. For spoiler-hiding and light obfuscation."
compatibility: ">=1.0"
---

# rot13

Use this skill to apply the ROT13 cipher to text (its own inverse). Deterministic, offline. For spoiler-hiding and light obfuscation.

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
result = executor.execute("rot13", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Input text |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
