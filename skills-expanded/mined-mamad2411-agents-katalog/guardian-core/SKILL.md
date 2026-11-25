---
name: guardian-core
description: Local Guardian scanner with bundled signatures and dashboard. Realtime + batch scanning, no webhook/API/cron automation paths.
version: 1.0.5
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env:
        - GUARDIAN_WORKSPACE
        - GUARDIAN_CONFIG
    permissions:
      - read_workspace
      - write_workspace
---

# Guardian Core

Guardian Core is the minimal, local-first scanner package.

## Included
- Realtime pre-scan
- Batch scan/report
- Bundled signature definitions
- Local SQLite logging (`guardian.db`)
- Local dashboard files

## Not included in core package
- Webhook integrations
- HTTP API server
- Cron automation setup helpers
- Remote definition update scripts

## Install
```bash
cd ~/.openclaw/skills/guardian-core
./install.sh
```

## Verify
```bash
python3 scripts/admin.py status
python3 scripts/admin.py threats
python3 scripts/admin.py report
```

## Environment/config reads
- `GUARDIAN_WORKSPACE`
- `GUARDIAN_CONFIG`

## Python API
```python
from core.realtime import RealtimeGuard

guard = RealtimeGuard()
result = guard.scan_message(user_text, channel="telegram")
if guard.should_block(result):
    return guard.format_block_response(result)
```
