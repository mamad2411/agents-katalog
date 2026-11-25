---
name: simplify-text
description: "Use this skill to rewrite complex text in plain, simple language at a roughly 8th-grade reading level while preserving meaning. Uses an LLM."
compatibility: ">=1.0"
---

# simplify-text

Use this skill to rewrite complex text in plain, simple language at a roughly 8th-grade reading level while preserving meaning. Uses an LLM.

- **Kind**: tool  |  **Niche**: publishing  |  **Cost tier**: near_free  |  **Version**: 0.1.0

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
result = executor.execute("simplify-text", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Input text |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
