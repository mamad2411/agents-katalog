---
name: levenshtein-distance
description: "Use this skill to compute the Levenshtein edit distance between two strings plus a 0-1 similarity ratio. Deterministic, offline. For fuzzy matching and typo detection."
compatibility: ">=1.0"
---

# levenshtein-distance

Use this skill to compute the Levenshtein edit distance between two strings plus a 0-1 similarity ratio. Deterministic, offline. For fuzzy matching and typo detection.

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
python run.py --a <string> --b <string>
```

**From a Python agent (ATEN runtime):**
```python
from skill_library import executor
result = executor.execute("levenshtein-distance", {a=..., b=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `a` | string | yes | First string |
| `b` | string | yes | Second string |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
