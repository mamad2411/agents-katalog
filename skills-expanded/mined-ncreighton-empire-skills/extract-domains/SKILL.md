---
name: extract-domains
description: "Use this skill to extract and normalize the domains of all URLs in a text: strips www, ports, and paths, de-duplicates, and counts links per domain. Deterministic, offline. Ideal for auditing outbound/affiliate links in an article or checking link diversity."
compatibility: ">=1.0"
---

# extract-domains

Use this skill to extract and normalize the domains of all URLs in a text: strips www, ports, and paths, de-duplicates, and counts links per domain. Deterministic, offline. Ideal for auditing outbound/affiliate links in an article or checking link diversity.

- **Kind**: analyzer  |  **Niche**: reviews  |  **Cost tier**: free  |  **Version**: 0.1.0

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
result = executor.execute("extract-domains", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Text containing URLs |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
