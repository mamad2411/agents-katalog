---
name: extract-action-items
description: "Use this skill to extract a clean list of concrete action items / to-dos from meeting notes or a message thread. Uses an LLM. Returns a list of short imperative tasks."
compatibility: ">=1.0"
---

# extract-action-items

Use this skill to extract a clean list of concrete action items / to-dos from meeting notes or a message thread. Uses an LLM. Returns a list of short imperative tasks.

- **Kind**: analyzer  |  **Niche**: ai  |  **Cost tier**: near_free  |  **Version**: 0.1.0

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
result = executor.execute("extract-action-items", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Input text |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
