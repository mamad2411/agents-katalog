---
name: extract-hashtags
description: "Use this skill to extract hashtags from social text: pulls #tags, de-duplicates case-insensitively, drops numeric-only tags, and returns them both with and without the # prefix. Deterministic, offline. Useful for auditing or reusing the tag set of a post."
compatibility: ">=1.0"
---

# extract-hashtags

Use this skill to extract hashtags from social text: pulls #tags, de-duplicates case-insensitively, drops numeric-only tags, and returns them both with and without the # prefix. Deterministic, offline. Useful for auditing or reusing the tag set of a post.

- **Kind**: analyzer  |  **Niche**: reviews  |  **Cost tier**: free  |  **Version**: 0.1.0

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
result = executor.execute("extract-hashtags", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Social post text |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
