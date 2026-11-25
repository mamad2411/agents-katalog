---
name: generate-cta
description: "Use this skill to generate N compelling call-to-action lines for a given product or offer description. Uses an LLM. Returns a list of CTA options."
compatibility: ">=1.0"
---

# generate-cta

Use this skill to generate N compelling call-to-action lines for a given product or offer description. Uses an LLM. Returns a list of CTA options.

- **Kind**: tool  |  **Niche**: reviews  |  **Cost tier**: near_free  |  **Version**: 0.1.0

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
result = executor.execute("generate-cta", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Input text |
| `count` | number | no | How many CTAs (default 5) |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
