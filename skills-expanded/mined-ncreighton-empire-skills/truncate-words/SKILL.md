---
name: truncate-words
description: "Use this skill to truncate text to a max number of words with an ellipsis (default 50). Deterministic, offline. For excerpts and previews."
compatibility: ">=1.0"
---

# truncate-words

Use this skill to truncate text to a max number of words with an ellipsis (default 50). Deterministic, offline. For excerpts and previews.

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
result = executor.execute("truncate-words", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Input text |
| `words` | number | no | Max words (default 50) |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
