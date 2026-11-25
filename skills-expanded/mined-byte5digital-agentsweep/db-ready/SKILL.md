---
name: db-ready
description: Wait until the local Postgres port accepts connections.
---
```bash
until timeout 1 bash -c '</dev/tcp/127.0.0.1/5432' 2>/dev/null; do sleep 1; done
```
