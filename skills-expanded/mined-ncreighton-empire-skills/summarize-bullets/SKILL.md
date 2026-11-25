---
name: summarize-bullets
description: "Use this skill to summarize a block of text into N concise bullet points capturing the key ideas. Uses an LLM. Good for TL;DRs and article recaps."
compatibility: ">=1.0"
---

# summarize-bullets

Use this skill to summarize a block of text into N concise bullet points capturing the key ideas. Uses an LLM. Good for TL;DRs and article recaps.

- **Kind**: tool  |  **Niche**: ai  |  **Cost tier**: near_free  |  **Version**: 0.1.0

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
result = executor.execute("summarize-bullets", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Input text |
| `count` | number | no | Number of bullets (default 3) |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
