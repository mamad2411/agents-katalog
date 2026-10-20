---
trigger: always_on
---

1. The project will be deployed on Cloudflare Workers with Cloudflare's edge primitives (KV, Durable Object, R2, Cache API).
2. The project uses SQLite-backed Durable Objects (see `wrangler.jsonc`, `new_sqlite_classes`)
3. References to Cloudflare Workers. If you are uncertain about support or features, always research these first party sources:
   Workers: https://developers.cloudflare.com/workers/llms-full.txt
   KV: https://developers.cloudflare.com/kv/llms-full.txt
   Durable Object: https://developers.cloudflare.com/durable-objects/llms-full.txt
   R2: https://developers.cloudflare.com/r2/llms-full.txt
4. Although in `wrangler.jsonc` we have `nodejs_compat` enabled, prefer Web standard APIs where possible. Cloudflare Workers may provide extensions to the API, such as `crypto.DigestStream()`. Refer to the official documentations.
