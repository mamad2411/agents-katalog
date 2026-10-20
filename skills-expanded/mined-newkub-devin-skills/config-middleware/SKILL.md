---
name: follow-lib-nitro-config-middleware
description: Configure Nitro middleware/plugins/hooks — request pipeline, auth guards, event hooks
argument-hint: "[middleware|plugin|hook]"
related:
  - follow-lib-nitro
  - run-test
  - resolve-errors
---

## Goal

Configure the Nitro request pipeline — middleware, plugins, nitroApp hooks for auth/logging/CORS/request lifecycle

## Scope

cross-cutting concerns on the server side — middleware (`middleware/`), plugins (`plugins/`), runtime hooks (`nitroApp.hooks()`)

## Execute

### 1. Middleware

> Goal: run before every request — auth, logging, headers

```ts
// middleware/auth.ts — global middleware (auto-registered)
import { defineEventHandler, createError, getRequestHeader } from 'nitro/h3'

export default defineEventHandler((event) => {
  const token = getRequestHeader(event, 'authorization')
  if (!token && event.path.startsWith('/api/private')) {
    throw createError({ statusCode: 401 })
  }
  event.context.user = decodeToken(token)   // attach context for handlers
})
```

- Order = filename/`middleware/` registration — check execution order when there are several
- Scoped middleware: `middleware/` in subdirs or check `event.path` in the handler

### 2. Plugins

> Goal: startup logic + app-level 
