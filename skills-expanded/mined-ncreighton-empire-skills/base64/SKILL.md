---
name: base64
description: "Use this skill to base64-encode or -decode text (mode=encode|decode). Deterministic, offline. For tokens, data URIs, and encoding payloads."
compatibility: ">=1.0"
---

# base64

Use this skill to base64-encode or -decode text (mode=encode|decode). Deterministic, offline. For tokens, data URIs, and encoding payloads.

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
result = executor.execute("base64", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Input text |
| `mode` | string | no | encode (default) or decode |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
