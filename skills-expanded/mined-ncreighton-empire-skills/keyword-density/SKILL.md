---
name: keyword-density
description: "Use this skill to compute how often a target keyword (or phrase) appears in a text, as a raw count and as a percentage of total words (0-100). Case-insensitive, whole-word matching, supports multi-word phrases. Deterministic, offline. Flags over-optimization above 3%."
compatibility: ">=1.0"
---

# keyword-density

Use this skill to compute how often a target keyword (or phrase) appears in a text, as a raw count and as a percentage of total words (0-100). Case-insensitive, whole-word matching, supports multi-word phrases. Deterministic, offline. Flags over-optimization above 3%.

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
python run.py --text <string> --keyword <string>
```

**From a Python agent (ATEN runtime):**
```python
from skill_library import executor
result = executor.execute("keyword-density", {text=..., keyword=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | The body text |
| `keyword` | string | yes | Keyword or phrase to measure |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
