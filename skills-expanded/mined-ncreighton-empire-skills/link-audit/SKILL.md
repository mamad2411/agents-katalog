---
name: link-audit
description: "Use this skill to audit markdown links: counts internal vs external (by site_domain) and checks the 3-5 internal-links-per-post convention. Deterministic, offline. For SEO link hygiene."
compatibility: ">=1.0"
---

# link-audit

Use this skill to audit markdown links: counts internal vs external (by site_domain) and checks the 3-5 internal-links-per-post convention. Deterministic, offline. For SEO link hygiene.

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
result = executor.execute("link-audit", {markdown=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `markdown` | string | yes | Markdown/HTML content |
| `site_domain` | string | no | Your domain, e.g. wealthfromai.com |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
