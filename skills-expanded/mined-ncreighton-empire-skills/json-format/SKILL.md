---
name: json-format
description: "Use this skill to pretty-print or minify a JSON string (mode=pretty|minify, optional sort_keys). Validates first. Deterministic, offline."
compatibility: ">=1.0"
---

# json-format

Use this skill to pretty-print or minify a JSON string (mode=pretty|minify, optional sort_keys). Validates first. Deterministic, offline.

- **Kind**: tool  |  **Niche**: ai  |  **Cost tier**: free  |  **Version**: 0.1.0

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
result = executor.execute("json-format", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Input text |
| `mode` | string | no | pretty (default) or minify |
| `sort_keys` | boolean | no | sort object keys |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
