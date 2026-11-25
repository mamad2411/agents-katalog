---
name: title-to-path
description: "Use this skill to turn a title or breadcrumb (split on / \\ > | or arrows) into a clean lowercase URL path with slugged segments. Deterministic, offline. For building nested URLs from titles."
compatibility: ">=1.0"
---

# title-to-path

Use this skill to turn a title or breadcrumb (split on / \ > | or arrows) into a clean lowercase URL path with slugged segments. Deterministic, offline. For building nested URLs from titles.

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
result = executor.execute("title-to-path", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Input text |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
