---
name: chunk-list
description: "Use this skill to split a list (or comma string) into fixed-size chunks. Deterministic, offline. For batching, pagination, grid layouts."
compatibility: ">=1.0"
---

# chunk-list

Use this skill to split a list (or comma string) into fixed-size chunks. Deterministic, offline. For batching, pagination, grid layouts.

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
python run.py --items <array>
```

**From a Python agent (ATEN runtime):**
```python
from skill_library import executor
result = executor.execute("chunk-list", {items=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `items` | array | yes | List or comma-separated string |
| `size` | number | no | Chunk size (default 3) |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
