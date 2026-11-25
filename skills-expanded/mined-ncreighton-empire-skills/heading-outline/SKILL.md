---
name: heading-outline
description: "Use this skill to extract the heading outline (H1-H6) from markdown and check hierarchy health: flags multiple H1s and level jumps (H2->H4). Deterministic, offline. For SEO structure audits."
compatibility: ">=1.0"
---

# heading-outline

Use this skill to extract the heading outline (H1-H6) from markdown and check hierarchy health: flags multiple H1s and level jumps (H2->H4). Deterministic, offline. For SEO structure audits.

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
python run.py --markdown <string>
```

**From a Python agent (ATEN runtime):**
```python
from skill_library import executor
result = executor.execute("heading-outline", {markdown=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `markdown` | string | yes | Markdown/HTML content |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
