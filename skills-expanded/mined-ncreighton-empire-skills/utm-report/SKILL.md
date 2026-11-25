---
name: utm-report
description: "Use this skill to audit a batch of URLs for campaign attribution: parses UTM parameters from every URL, flags untagged links, and aggregates counts by source and by campaign. Deterministic, offline. Feed it your link list and get an attribution-readiness report."
compatibility: ">=1.0"
---

# utm-report

Use this skill to audit a batch of URLs for campaign attribution: parses UTM parameters from every URL, flags untagged links, and aggregates counts by source and by campaign. Deterministic, offline. Feed it your link list and get an attribution-readiness report.

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
python run.py --urls <array>
```

**From a Python agent (ATEN runtime):**
```python
from skill_library import executor
result = executor.execute("utm-report", {urls=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `urls` | array | yes | List of URLs (or a newline-separated string) |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
