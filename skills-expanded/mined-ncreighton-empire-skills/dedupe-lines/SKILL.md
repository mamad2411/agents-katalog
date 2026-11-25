---
name: dedupe-lines
description: "Use this skill to remove duplicate lines from text, preserving first-seen order by default (optionally sorted or case-insensitive). Deterministic, offline. Returns the deduped text plus kept/removed counts."
compatibility: ">=1.0"
---

# dedupe-lines

Use this skill to remove duplicate lines from text, preserving first-seen order by default (optionally sorted or case-insensitive). Deterministic, offline. Returns the deduped text plus kept/removed counts.

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
result = executor.execute("dedupe-lines", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Text with lines |
| `case_insensitive` | boolean | no | Treat lines differing only in case as duplicates |
| `keep_order` | boolean | no | Preserve first-seen order (else sorted) |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
