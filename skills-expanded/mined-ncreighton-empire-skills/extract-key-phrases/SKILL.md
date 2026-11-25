---
name: extract-key-phrases
description: "Use this skill to extract the most important key phrases / topics from a text as a short list. Uses an LLM. For tagging and SEO keyword discovery."
compatibility: ">=1.0"
---

# extract-key-phrases

Use this skill to extract the most important key phrases / topics from a text as a short list. Uses an LLM. For tagging and SEO keyword discovery.

- **Kind**: analyzer  |  **Niche**: publishing  |  **Cost tier**: near_free  |  **Version**: 0.1.0

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
result = executor.execute("extract-key-phrases", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Input text |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
