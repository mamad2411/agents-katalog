---
name: smart-truncate
description: "Use this skill to truncate text to a max length at a word boundary with an ellipsis, without cutting words in half. Ideal for meta descriptions (155 chars), social previews, and card summaries. Deterministic, offline."
compatibility: ">=1.0"
---

# smart-truncate

Use this skill to truncate text to a max length at a word boundary with an ellipsis, without cutting words in half. Ideal for meta descriptions (155 chars), social previews, and card summaries. Deterministic, offline.

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
result = executor.execute("smart-truncate", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Text to truncate |
| `max_length` | number | no | Max length incl ellipsis (default 155) |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
