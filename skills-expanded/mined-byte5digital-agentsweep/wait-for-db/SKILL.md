---
name: wait-for-db
description: Wait for the local database to accept connections.
allowed-tools: Bash(bash:*)
---

```bash
until bash -c '</dev/tcp/localhost/5432' 2>/dev/null; do sleep 1; done
until bash -c '</dev/tcp/127.0.0.1/6379' 2>/dev/null; do sleep 1; done
```
