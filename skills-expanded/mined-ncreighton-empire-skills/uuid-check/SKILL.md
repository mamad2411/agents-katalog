---
name: uuid-check
description: "Use this skill to validate whether a string is a well-formed UUID (v1-v5) and report its version. Deterministic, offline. For ID validation."
compatibility: ">=1.0"
---

# uuid-check

Use this skill to validate whether a string is a well-formed UUID (v1-v5) and report its version. Deterministic, offline. For ID validation.

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
python run.py --value <string>
```

**From a Python agent (ATEN runtime):**
```python
from skill_library import executor
result = executor.execute("uuid-check", {value=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `value` | string | yes | String to check |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
