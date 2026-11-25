---
name: suggest-titles
description: "Use this skill to generate N catchy, SEO-aware title options for an article given its topic or first paragraph. Uses an LLM."
compatibility: ">=1.0"
---

# suggest-titles

Use this skill to generate N catchy, SEO-aware title options for an article given its topic or first paragraph. Uses an LLM.

- **Kind**: tool  |  **Niche**: publishing  |  **Cost tier**: near_free  |  **Version**: 0.1.0

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
result = executor.execute("suggest-titles", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Input text |
| `count` | number | no | How many titles (default 5) |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
