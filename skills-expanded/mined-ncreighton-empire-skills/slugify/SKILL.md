---
name: slugify
description: "Use this skill whenever you need to convert an arbitrary string into a clean URL slug: lowercase, non-alphanumerics to single hyphens, collapse repeats, trim, optional max length on a word boundary. Deterministic, offline, no dependencies."
compatibility: ">=1.0"
---

# slugify

Use this skill whenever you need to convert an arbitrary string into a clean URL slug: lowercase, non-alphanumerics to single hyphens, collapse repeats, trim, optional max length on a word boundary. Deterministic, offline, no dependencies.

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
result = executor.execute("slugify", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Text to slugify |
| `max_length` | number | no | Max slug length (word-boundary trim) |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
