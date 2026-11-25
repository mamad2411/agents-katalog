---
name: keyword-seo-check
description: "Use this skill to check whether a target keyword appears in the title and slug (and at the title start) and returns an SEO placement score. Deterministic, offline. For on-page SEO validation."
compatibility: ">=1.0"
---

# keyword-seo-check

Use this skill to check whether a target keyword appears in the title and slug (and at the title start) and returns an SEO placement score. Deterministic, offline. For on-page SEO validation.

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
python run.py --keyword <string>
```

**From a Python agent (ATEN runtime):**
```python
from skill_library import executor
result = executor.execute("keyword-seo-check", {keyword=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `keyword` | string | yes | Target keyword |
| `title` | string | no | Post title |
| `slug` | string | no | Post slug |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
