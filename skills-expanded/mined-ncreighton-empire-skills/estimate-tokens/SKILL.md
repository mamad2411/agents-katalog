---
name: estimate-tokens
description: "Use this skill to approximate the LLM token count of a text before an API call, for cost/budget guarding. Averages two estimators (~4 chars/token and ~0.75 tokens/word). Deterministic, offline, no tokenizer dependency. Not exact, but reliable for gating oversized prompts."
compatibility: ">=1.0"
---

# estimate-tokens

Use this skill to approximate the LLM token count of a text before an API call, for cost/budget guarding. Averages two estimators (~4 chars/token and ~0.75 tokens/word). Deterministic, offline, no tokenizer dependency. Not exact, but reliable for gating oversized prompts.

- **Kind**: analyzer  |  **Niche**: ai  |  **Cost tier**: free  |  **Version**: 0.1.0

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
result = executor.execute("estimate-tokens", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Text to estimate |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
