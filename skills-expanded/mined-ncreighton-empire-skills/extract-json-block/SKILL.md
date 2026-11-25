---
name: extract-json-block
description: "Use this skill to pull the first valid JSON object or array out of noisy or LLM-generated text: strips ```json code fences, does a balanced-brace scan, and repairs trailing commas. Returns the parsed data. Deterministic, offline. Essential for safely parsing LLM output before using it."
compatibility: ">=1.0"
---

# extract-json-block

Use this skill to pull the first valid JSON object or array out of noisy or LLM-generated text: strips ```json code fences, does a balanced-brace scan, and repairs trailing commas. Returns the parsed data. Deterministic, offline. Essential for safely parsing LLM output before using it.

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
python run.py --text <string>
```

**From a Python agent (ATEN runtime):**
```python
from skill_library import executor
result = executor.execute("extract-json-block", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Text that contains JSON somewhere |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
