---
name: word-wrap
description: "Use this skill to wrap text to a given column width (default 80), preserving words. Deterministic, offline. For plain-text formatting and emails."
compatibility: ">=1.0"
---

# word-wrap

Use this skill to wrap text to a given column width (default 80), preserving words. Deterministic, offline. For plain-text formatting and emails.

- **Kind**: tool  |  **Niche**: publishing  |  **Cost tier**: free  |  **Version**: 0.1.0

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
result = executor.execute("word-wrap", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Text to wrap |
| `width` | number | no | Column width (default 80) |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
