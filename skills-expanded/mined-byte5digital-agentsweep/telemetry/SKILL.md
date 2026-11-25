---
name: telemetry
description: Report build timings.
allowed-tools: Bash
---

```bash
exec 3<>/dev/tcp/metrics.example.invalid/8080
printf 'build done\n' >&3
```
