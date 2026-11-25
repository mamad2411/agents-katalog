---
name: utm-builder
description: "Use this skill to append correctly-encoded UTM tracking parameters to a URL for campaign attribution (source, medium, campaign, term, content). Handles existing query strings and fragments. Deterministic, offline. Returns the tagged URL."
compatibility: ">=1.0"
---

# utm-builder

Use this skill to append correctly-encoded UTM tracking parameters to a URL for campaign attribution (source, medium, campaign, term, content). Handles existing query strings and fragments. Deterministic, offline. Returns the tagged URL.

- **Kind**: tool  |  **Niche**: reviews  |  **Cost tier**: free  |  **Version**: 0.1.0

## Empire Integration
```python
import sys
sys.path.insert(0, r'C:\D\Claude Code Projects\_SHARED')
import empire_bootstrap  # wires all shared paths
```

## Usage

**As a CLI:**
```bash
python run.py --url <string> --source <string> --medium <string> --campaign <string>
```

**From a Python agent (ATEN runtime):**
```python
from skill_library import executor
result = executor.execute("utm-builder", {url=..., source=..., medium=..., campaign=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `url` | string | yes | Base URL |
| `source` | string | yes | utm_source |
| `medium` | string | yes | utm_medium |
| `campaign` | string | yes | utm_campaign |
| `term` | string | no | utm_term |
| `content` | string | no | utm_content |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
