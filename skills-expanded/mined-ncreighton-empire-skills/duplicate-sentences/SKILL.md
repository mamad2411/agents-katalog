---
name: duplicate-sentences
description: "Use this skill to detect repeated sentences in text (case/whitespace-insensitive) with their counts. Deterministic, offline. For catching LLM repetition and thin/padded content."
compatibility: ">=1.0"
---

# duplicate-sentences

Use this skill to detect repeated sentences in text (case/whitespace-insensitive) with their counts. Deterministic, offline. For catching LLM repetition and thin/padded content.

- **Kind**: analyzer  |  **Niche**: publishing  |  **Cost tier**: free  |  **Version**: 0.1.0

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
result = executor.execute("duplicate-sentences", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Input text |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
