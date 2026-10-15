---
name: gkm-telescope
description: Use when editing files that import from @geekmidas/telescope or configure the debugging dashboard. Activates for telescope dev server setup, request/response inspection, or trace viewer configuration.
---

# gkm-telescope

Docs: https://geekmidas.github.io/toolbox/packages/telescope.html

## Activation

- Files importing `@geekmidas/telescope`
- Files with `Telescope` or `telescope.config.ts` configuration
- Dev server setup for telescope inspection dashboard
- Request/response tracing, log viewer, or performance profiling

## Key patterns

```typescript
import { defineConfig } from '@geekmidas/telescope';

export default defineConfig({
  port: 3001,
  watch: ['src/endpoints/**/*.ts'],
  inspect: {
    requests: true,
    responses: true,
    headers: true,
  },
});
```

- Local debugging dashboard for API requests/responses
- Watch mode for live endpoint inspection during development
- Configurable inspection depth (body, headers, query params)
- Works alongside `@geekmidas/constructs` dev server

## Integration points

- `@geekmidas/constructs` — telescope watches endpoint files
- `@geekmidas/logger` — telescope displays structured log events
- `@geekmidas/db` — inspect query execution traces