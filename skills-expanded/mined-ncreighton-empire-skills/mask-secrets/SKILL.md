---
name: mask-secrets
description: "Use this skill to redact secrets from text before logging or sharing: masks OpenAI keys (sk-), GitHub PATs, AWS access keys, Slack tokens, Bearer tokens, and email addresses. Deterministic, offline. Returns the masked text and a redaction count."
compatibility: ">=1.0"
---

# mask-secrets

Use this skill to redact secrets from text before logging or sharing: masks OpenAI keys (sk-), GitHub PATs, AWS access keys, Slack tokens, Bearer tokens, and email addresses. Deterministic, offline. Returns the masked text and a redaction count.

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
result = executor.execute("mask-secrets", {text=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | yes | Text possibly containing secrets |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
