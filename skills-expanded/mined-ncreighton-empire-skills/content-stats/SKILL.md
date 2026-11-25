---
name: content-stats
description: "Use this skill to get objective stats for a piece of text: word count, character count, sentence count, paragraph count, and estimated reading time in minutes (at 220 wpm). Deterministic, offline, no dependencies. Good for grading draft length before publishing."
compatibility: ">=1.0"
---

# content-stats

Use this skill to get objective stats for a piece of text: word count, character count, sentence count, paragraph count, and estimated reading time in minutes (at 220 wpm). Deterministic, offline, no dependencies. Good for grading draft length before publishing.

- **Kind**: analyzer  |  **Niche**: publishing  |  **Cost tier**: free  |  **Version**: 0.1.0

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
result = executor.execute("content-stats", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Text to analyze |
| `wpm` | number | no | Reading speed (default 220) |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
