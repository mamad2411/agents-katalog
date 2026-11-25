---
name: humanize-duration
description: "Use this skill to convert a number of seconds into a human duration like '2h 5m 30s'. Deterministic, offline. For run-times, ETAs, video lengths."
compatibility: ">=1.0"
---

# humanize-duration

Use this skill to convert a number of seconds into a human duration like '2h 5m 30s'. Deterministic, offline. For run-times, ETAs, video lengths.

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
python run.py --seconds <number>
```

**From a Python agent (ATEN runtime):**
```python
from skill_library import executor
result = executor.execute("humanize-duration", {seconds=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `seconds` | number | yes | Duration in seconds |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
