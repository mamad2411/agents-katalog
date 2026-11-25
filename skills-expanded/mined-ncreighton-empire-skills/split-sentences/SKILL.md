---
name: split-sentences
description: "Use this skill to split text into sentences (on . ! ? followed by a capital/quote). Deterministic, offline. For readability, summarization prep, and per-sentence processing."
compatibility: ">=1.0"
---

# split-sentences

Use this skill to split text into sentences (on . ! ? followed by a capital/quote). Deterministic, offline. For readability, summarization prep, and per-sentence processing.

- **Kind**: tool  |  **Niche**: publishing  |  **Cost tier**: free  |  **Version**: 0.1.0

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
result = executor.execute("split-sentences", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Input text |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
