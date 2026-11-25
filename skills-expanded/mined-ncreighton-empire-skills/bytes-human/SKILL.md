---
name: bytes-human
description: "Use this skill to format a byte count as a human-readable size (B/KB/MB/GB/TB/PB). Deterministic, offline. For file sizes and quotas."
compatibility: ">=1.0"
---

# bytes-human

Use this skill to format a byte count as a human-readable size (B/KB/MB/GB/TB/PB). Deterministic, offline. For file sizes and quotas.

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
python run.py --bytes <number>
```

**From a Python agent (ATEN runtime):**
```python
from skill_library import executor
result = executor.execute("bytes-human", {bytes=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `bytes` | number | yes | Number of bytes |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
