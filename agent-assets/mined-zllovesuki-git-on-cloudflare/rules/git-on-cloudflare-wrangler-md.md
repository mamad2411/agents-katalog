---
trigger: always_on
---

1. To add new variables/binding, first make changes in wrangler.jsonc, then run `npm run cf-typegen` to update `worker-configuration.d.ts`. The new bindings will be available via `Env`
2. Do not attempt to read `worker-configuration.d.ts` in full as it is auto-generated, and the line limit exceeds what your tool allows.
