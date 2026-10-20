---
trigger: always_on
---

1. When accessing or modifying the SQLite database within Durable Objects, do not access the database directly. Instead, add your function in `dal.ts`
2. Tests should use DAL functions whenever possible, unless it is absolutely necessary to have direct access (for example, checking for constraint violation enforcement).
