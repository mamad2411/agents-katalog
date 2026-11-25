---
name: extract-emails
description: "Use this skill to extract all valid email addresses from arbitrary text, de-duplicated and lowercased. Uses RFC-ish validation. Deterministic, offline. Useful for parsing scraped pages, contact forms, or documents for leads."
compatibility: ">=1.0"
---

# extract-emails

Use this skill to extract all valid email addresses from arbitrary text, de-duplicated and lowercased. Uses RFC-ish validation. Deterministic, offline. Useful for parsing scraped pages, contact forms, or documents for leads.

- **Kind**: analyzer  |  **Niche**: ai  |  **Cost tier**: free  |  **Version**: 0.1.0

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
result = executor.execute("extract-emails", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Text to scan for emails |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
