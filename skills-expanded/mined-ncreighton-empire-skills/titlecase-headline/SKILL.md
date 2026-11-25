---
name: titlecase-headline
description: "Use this skill to convert a string to AP-style headline title case: capitalizes the first and last word and all major words, but lowercases short articles/conjunctions/prepositions (a, an, the, and, of, to, etc.) when they fall mid-headline. Deterministic, offline. For post titles and headings."
compatibility: ">=1.0"
---

# titlecase-headline

Use this skill to convert a string to AP-style headline title case: capitalizes the first and last word and all major words, but lowercases short articles/conjunctions/prepositions (a, an, the, and, of, to, etc.) when they fall mid-headline. Deterministic, offline. For post titles and headings.

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
result = executor.execute("titlecase-headline", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Headline text to title-case |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
