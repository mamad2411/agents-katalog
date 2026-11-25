---
name: email-subject-lines
description: "Use this skill to generate N catchy email subject lines from an email body or topic, optimized for open rate (curiosity, brevity, no spam words). Uses an LLM. Returns a list."
compatibility: ">=1.0"
---

# email-subject-lines

Use this skill to generate N catchy email subject lines from an email body or topic, optimized for open rate (curiosity, brevity, no spam words). Uses an LLM. Returns a list.

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
result = executor.execute("email-subject-lines", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Input text |
| `count` | number | no | How many subject lines (default 5) |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
