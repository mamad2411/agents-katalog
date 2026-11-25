---
name: readability-grade
description: "Use this skill to score text readability with the correct Flesch Reading Ease (0-100) and Flesch-Kincaid grade-level formulas, plus a plain-language difficulty band. Deterministic, offline, no dependencies. Grade a draft before publishing to check it matches your audience."
compatibility: ">=1.0"
---

# readability-grade

Use this skill to score text readability with the correct Flesch Reading Ease (0-100) and Flesch-Kincaid grade-level formulas, plus a plain-language difficulty band. Deterministic, offline, no dependencies. Grade a draft before publishing to check it matches your audience.

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
python run.py --text <string>
```

**From a Python agent (ATEN runtime):**
```python
from skill_library import executor
result = executor.execute("readability-grade", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Text to grade |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
