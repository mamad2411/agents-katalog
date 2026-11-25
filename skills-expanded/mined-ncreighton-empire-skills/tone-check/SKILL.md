---
name: tone-check
description: "Use this skill to assess the tone of a text (e.g. professional, casual, aggressive, warm) and flag any tone that clashes with a stated target tone. Uses an LLM. For brand-voice QA."
compatibility: ">=1.0"
---

# tone-check

Use this skill to assess the tone of a text (e.g. professional, casual, aggressive, warm) and flag any tone that clashes with a stated target tone. Uses an LLM. For brand-voice QA.

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
result = executor.execute("tone-check", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Input text |
| `target_tone` | string | no | Desired tone to check against |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
