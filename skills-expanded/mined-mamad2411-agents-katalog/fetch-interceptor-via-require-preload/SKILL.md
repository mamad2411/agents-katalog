---
name: fetch-interceptor-via-require-preload
description: Patch globalThis.fetch in SDK subprocesses BEFORE the SDK captures it, by shipping a CJS interceptor bundle and loading it with node --require / bun --preload at spawn time.
category: agent-sdk
version: 1.0.0
version_origin: extracted
tags: [interceptor, fetch, node-require, bun-preload, observability]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/lukilabs/craft-agents-oss.git
source_ref: main
source_commit: 61f7d48a5b4fd0a8094f002c9e3aea5f3824dcfb
source_project: craft-agents-oss
source_path: packages/shared/src/unified-network-interceptor.ts
imported_at: 2026-04-18T00:00:00Z
---

# Fetch interceptor via --require/--preload

## When to use
- Need to observe/modify every HTTP request a third-party SDK (Claude Agent SDK, OpenAI SDK) makes, BEFORE the SDK captures the fetch reference.
- Patching at the app level is too late - SDKs often snapshot `globalThis.fetch` on import.
- Want one interceptor bundle that works across Bun, Node, Electron main, and subprocesses.

## How it works
1. Write the interceptor in TypeScript with explicit side-effects on import (mutate `globalThis.fetch`).
2. Bundle to CJS so it loads fast and works under `--require`:
   ```
   bun run esbuild packages/shared/src/unified-network-interceptor.ts \
     --bundle --platform=node --format=cjs --outfile=dist/interceptor.cjs
   ```
3. When spawning the SDK subprocess, pass the preload flag:
   - Node: `['node', '--require', '/abs/path/interceptor.cjs', 'agent.js']`
   - Bun: `['bun', '--preload', '/abs/path/interceptor.cjs', 'agent.ts']`
4. The interceptor runs FIRST, replaces `globalThis.fetch` with a wrapper. When the SDK later does `import { fetch } from ...` or just uses `globalThis.fetch`, it sees the wrapped version.
5. Wrapper reads env-injected config (feature flags, proxy settings) - the parent sets env before `spawn`, so child reads them.
6. On the response path, for SSE streams, you pipe-transform the chunks to rewrite / capture / scrub per API format (Anthropic vs OpenAI have different strictness).

## Example
```ts
// interceptor.ts (bundled to interceptor.cjs)
const origFetch = globalThis.fetch;
globalThis.fetch = async (input, init) => {
  const url = typeof input === 'string' ? input : input.url;
  if (init?.body && url.includes('/v1/messages')) {
    init = { ...init, body: transformRequest(init.body) };
  }
  const res = await origFetch(input, init);
  if (res.headers.get('content-type')?.includes('text/event-stream')) {
    return new Response(transformSse(res.body!), res);
  }
  return res;
};
```

Parent spawn:
```ts
Bun.spawn(['bun', '--preload', '/app/dist/interceptor.cjs', 'agent.ts'], {
  env: { ...parentEnv, CRAFT_FEATURE_FLAGS: JSON.stringify(flags) },
});
```

## Gotchas
- `--require` only works with CJS. If your interceptor imports ESM-only deps, inline them at bundle time.
- In Bun, `--preload` is the right flag. `--require` works for compatibility but `--preload` is recommended.
- The interceptor executes BEFORE `process.env` is parsed by your parent app? NO - env is set at fork, available immediately.
- If the SDK imports fetch from `undici` directly (not `globalThis`), patching global fetch is useless. Check the SDK source; sometimes you have to monkey-patch `undici`'s request too.
- Test the interceptor in isolation first - debugging "my SDK silently stopped working after upgrade" at 3am is unfun.
