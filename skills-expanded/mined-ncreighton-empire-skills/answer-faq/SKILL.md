---
name: answer-faq
description: "Use this skill to generate a concise FAQ answer for a given question, optionally grounded in provided context text. Uses an LLM."
compatibility: ">=1.0"
---

# answer-faq

Use this skill to generate a concise FAQ answer for a given question, optionally grounded in provided context text. Uses an LLM.

- **Kind**: tool  |  **Niche**: ai  |  **Cost tier**: near_free  |  **Version**: 0.1.0

## Empire Integration
```python
import sys
sys.path.insert(0, r'C:\D\Claude Code Projects\_SHARED')
import empire_bootstrap  # wires all shared paths
```

## Usage

**As a CLI:**
```bash
python run.py --question <string>
```

**From a Python agent (ATEN runtime):**
```python
from skill_library import executor
result = executor.execute("answer-faq", {question=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `question` | string | yes | The question |
| `context` | string | no | Optional grounding context |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
