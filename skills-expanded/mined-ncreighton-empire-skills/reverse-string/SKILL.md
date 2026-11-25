---
name: reverse-string
description: "Use this skill to reverse a string character by character. Deterministic offline."
compatibility: ">=1.0"
---

# reverse-string

Use this skill to reverse a string character by character. Deterministic offline.

- **Kind**: tool  |  **Niche**: general  |  **Cost tier**: free  |  **Version**: 0.1.0

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
result = executor.execute("reverse-string", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | text to reverse |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
