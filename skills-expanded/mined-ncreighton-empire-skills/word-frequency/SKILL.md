---
name: word-frequency
description: "Use this skill to get the most frequent words in a text: tokenizes, lowercases, drops common stopwords (optional), and returns the top-N words with counts plus total/unique word counts. Deterministic, offline. For content analysis, keyword discovery, and tag suggestions."
compatibility: ">=1.0"
---

# word-frequency

Use this skill to get the most frequent words in a text: tokenizes, lowercases, drops common stopwords (optional), and returns the top-N words with counts plus total/unique word counts. Deterministic, offline. For content analysis, keyword discovery, and tag suggestions.

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
result = executor.execute("word-frequency", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Text to analyze |
| `top` | number | no | How many top words (default 10) |
| `include_stopwords` | boolean | no | Include common stopwords (default false) |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
