---
name: html-to-text
description: "Use this skill to convert HTML into clean plain text: removes script/style, turns block tags and <br> into newlines, strips remaining tags, unescapes HTML entities, and collapses whitespace. Deterministic, offline. The right first step before readability, word-count, or slop analysis on scraped or WordPress HTML."
compatibility: ">=1.0"
---

# html-to-text

Use this skill to convert HTML into clean plain text: removes script/style, turns block tags and <br> into newlines, strips remaining tags, unescapes HTML entities, and collapses whitespace. Deterministic, offline. The right first step before readability, word-count, or slop analysis on scraped or WordPress HTML.

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
python run.py --html <string>
```

**From a Python agent (ATEN runtime):**
```python
from skill_library import executor
result = executor.execute("html-to-text", {html=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `html` | string | yes | HTML string to convert |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
