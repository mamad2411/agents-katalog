---
name: alt-text-check
description: "Use this skill to audit image alt text in markdown: counts images, missing alt, and alt over 125 chars. Deterministic, offline. For accessibility + SEO image compliance."
compatibility: ">=1.0"
---

# alt-text-check

Use this skill to audit image alt text in markdown: counts images, missing alt, and alt over 125 chars. Deterministic, offline. For accessibility + SEO image compliance.

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
result = executor.execute("alt-text-check", {markdown=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `markdown` | string | yes | Markdown/HTML content |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
