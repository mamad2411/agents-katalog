---
name: status-monitor
description: Heartbeat to a named status page.
---

# Monitor

Post https://status.example.invalid/hook every 5 minutes.

```bash
python scripts/send_status.py "up" "progress" "s" --details "queue depth"
```

The destination is the status page above. Do not send free-form secrets.
