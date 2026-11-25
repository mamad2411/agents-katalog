---
name: jaccard-similarity
description: "Use this skill to measure word-set (Jaccard) similarity between two texts (0-1), with shared-word count and a near-duplicate flag (>=0.8). Deterministic, offline. For dedup and content-overlap detection."
compatibility: ">=1.0"
---

# jaccard-similarity

Use this skill to measure word-set (Jaccard) similarity between two texts (0-1), with shared-word count and a near-duplicate flag (>=0.8). Deterministic, offline. For dedup and content-overlap detection.

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
python run.py --text_a <string> --text_b <string>
```

**From a Python agent (ATEN runtime):**
```python
from skill_library import executor
result = executor.execute("jaccard-similarity", {text_a=..., text_b=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text_a` | string | yes | First text |
| `text_b` | string | yes | Second text |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
