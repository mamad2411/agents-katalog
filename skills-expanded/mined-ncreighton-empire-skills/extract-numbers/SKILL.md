---
name: extract-numbers
description: "Use this skill to pull all numbers (ints, decimals, thousands-separated) from text, with their sum. Deterministic, offline. For parsing prices, stats, and quantities out of copy."
compatibility: ">=1.0"
---

# extract-numbers

Use this skill to pull all numbers (ints, decimals, thousands-separated) from text, with their sum. Deterministic, offline. For parsing prices, stats, and quantities out of copy.

- **Kind**: analyzer  |  **Niche**: reviews  |  **Cost tier**: free  |  **Version**: 0.1.0

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
result = executor.execute("extract-numbers", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Input text |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
