---
name: classify-sentiment
description: "Use this skill to classify the sentiment of a short text as positive, negative, or neutral, with a one-line reason. Uses an LLM. For review/comment triage."
compatibility: ">=1.0"
---

# classify-sentiment

Use this skill to classify the sentiment of a short text as positive, negative, or neutral, with a one-line reason. Uses an LLM. For review/comment triage.

- **Kind**: analyzer  |  **Niche**: reviews  |  **Cost tier**: near_free  |  **Version**: 0.1.0

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
result = executor.execute("classify-sentiment", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Input text |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
