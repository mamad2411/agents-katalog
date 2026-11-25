---
name: initials
description: "Use this skill to get the initials of a name/phrase (first letter of each word, uppercased, capped at max). Deterministic, offline. For avatars/monograms."
compatibility: ">=1.0"
---

# initials

Use this skill to get the initials of a name/phrase (first letter of each word, uppercased, capped at max). Deterministic, offline. For avatars/monograms.

- **Kind**: tool  |  **Niche**: lifestyle  |  **Cost tier**: free  |  **Version**: 0.1.0

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
result = executor.execute("initials", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Input text |
| `max` | number | no | Max initials (default 3) |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
