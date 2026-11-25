---
name: strip-markdown
description: "Use this skill to strip markdown formatting from text and return clean plain text: removes headings, bold/italic, links (keeps link text), code fences, list markers, and blockquotes. Deterministic, offline. Great for generating previews or plain-text excerpts."
compatibility: ">=1.0"
---

# strip-markdown

Use this skill to strip markdown formatting from text and return clean plain text: removes headings, bold/italic, links (keeps link text), code fences, list markers, and blockquotes. Deterministic, offline. Great for generating previews or plain-text excerpts.

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
python run.py --markdown <string>
```

**From a Python agent (ATEN runtime):**
```python
from skill_library import executor
result = executor.execute("strip-markdown", {markdown=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `markdown` | string | yes | Markdown text |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
