---
name: meta-description
description: "Use this skill to generate a clean SEO meta description from article body text: strips markdown/URLs, collapses whitespace, truncates to a max length (default 155) on a word boundary. Deterministic, offline."
compatibility: ">=1.0"
---

# meta-description

Use this skill to generate a clean SEO meta description from article body text: strips markdown/URLs, collapses whitespace, truncates to a max length (default 155) on a word boundary. Deterministic, offline.

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
result = executor.execute("meta-description", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Input text |
| `max_length` | number | no | Max chars (default 155) |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
