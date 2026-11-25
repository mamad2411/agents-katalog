---
name: normalize-phone
description: "Use this skill to normalize a phone number to E.164 format (+<country><number>): strips formatting, applies a default country code for bare 10-digit US numbers, preserves an explicit +prefix, and flags whether the result is a plausible length. Deterministic, offline. For cleaning contact/lead data."
compatibility: ">=1.0"
---

# normalize-phone

Use this skill to normalize a phone number to E.164 format (+<country><number>): strips formatting, applies a default country code for bare 10-digit US numbers, preserves an explicit +prefix, and flags whether the result is a plausible length. Deterministic, offline. For cleaning contact/lead data.

- **Kind**: tool  |  **Niche**: reviews  |  **Cost tier**: free  |  **Version**: 0.1.0

## Empire Integration
```python
import sys
sys.path.insert(0, r'C:\D\Claude Code Projects\_SHARED')
import empire_bootstrap  # wires all shared paths
```

## Usage

**As a CLI:**
```bash
python run.py --phone <string>
```

**From a Python agent (ATEN runtime):**
```python
from skill_library import executor
result = executor.execute("normalize-phone", {phone=...})
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `phone` | string | yes | Phone number in any format |
| `default_country_code` | string | no | Country code for bare local numbers (default '1') |

## Returns

`object` — `{"status": "ok"|"error", "result": ...}`
