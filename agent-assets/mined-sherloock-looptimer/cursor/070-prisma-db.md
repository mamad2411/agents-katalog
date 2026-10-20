---
description: Prisma database practices: ownership checks, select minimal fields, transactions.
globs: "prisma/**, actions/**/*.ts, app/api/**/*.ts"
alwaysApply: false
---

## Database (Prisma)
- Use Prisma's type-safe queries; avoid raw SQL unless necessary.
- Always validate user ownership before modifying timer data.
- Use `select` to only fetch needed fields for performance.
- Use transactions for operations that must succeed/fail together.
- Handle Prisma errors gracefully with user-friendly messages.
