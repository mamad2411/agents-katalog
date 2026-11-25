---
name: fetch-schema-safely
description: Refresh the generated schema.
allowed-tools: Bash(node:*)
---

```sh
export NODE_TLS_REJECT_UNAUTHORIZED=1
node scripts/refresh-schema.js
```
