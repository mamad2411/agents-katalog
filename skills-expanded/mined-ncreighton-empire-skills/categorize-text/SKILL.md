---
name: categorize-text
description: "Use this skill to assign the single best category to a text from a provided list of candidate categories, with a confidence note. Uses an LLM. For routing, tagging, and triage."
compatibility: ">=1.0"
---

# categorize-text

Use this skill to assign the single best category to a text from a provided list of candidate categories, with a confidence note. Uses an LLM. For routing, tagging, and triage.

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
python run.py --text <string> --categories <array>
```

**From a Python agent (ATEN runtime):**
```python
from skill_library import executor
result = executor.execute("categorize-text", {text=..., categories=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Input text |
| `categories` | array | yes | Candidate categories (list or comma string) |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
