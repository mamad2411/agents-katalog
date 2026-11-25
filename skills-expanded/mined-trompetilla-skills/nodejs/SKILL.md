---
name: NodeJS
description: Avoid common Node.js mistakes — event loop blocking, async error handling, ESM gotchas, and memory leaks.
metadata: {"clawdbot":{"emoji":"💚","requires":{"bins":["node"]},"os":["linux","darwin","win32"]}}
---

## Event Loop
- `fs.readFileSync` blocks entire server — use `fs.promises.readFile` or callback version
- CPU-intensive code blocks — offload to worker threads or child process
- `setImmediate` vs `process.nextTick` — nextTick runs before I/O, setImmediate after
- Long-running loops starve I/O — break into chunks with setImmediate

## Async Error Handling
- Unhandled promise rejection crashes in Node 15+ — always `.catch()` or try/catch with await
- `process.on('unhandledRejection')` for global handler — log and exit gracefully
- Errors in callbacks need explicit handling — won't propagate to outer try/catch
- `Promise.all` fails fast — one rejection rejects all, use `Promise.allSettled` if need all results

## CommonJS vs ESM
- `"type": "module"` in package.json for ESM — otherwise `.mjs` extension
- ESM: `import x from 'y'` — CommonJS: `const x = require('y')`
- No `__dirname` in ESM — use `import.meta.url` with `fileURLToPath`
- Can't `require()` ESM modules — use dynamic `import()` which returns Promise
- `exports` is reference to `module.exports` — reassigning `exports = x` breaks it

## Environment Variables
- `process.env` values are always strings — `PORT=3000` is `"3000"` not `3000`
- Missing env var is `undefined`, not error — check explicitly or use defaults
- `.env` files need `dotenv` — not built-in, call `dotenv.config()` early
- Don't commit `.env` — use `.env.example` with dummy values

## Memory Leaks
- Event listeners accumulate — `removeListener` when done, or use `once`
- Closures capturing large objects — nullify references when done
- Global caches grow unbounded — use LRU cache with size limit
- `--max-old-space-size` to increase heap — but fix leaks first

## Streams
- Backpressure: `write()` returns false when buffer full — wait for `drain` event
- `.pipe()` handles backpressure automatically — prefer over manual read/write
- Error handling on all streams — `stream.on('error', handler)` or pipeline errors silently
- `pipeline()` over `.pipe()` — handles errors and cleanup properly

## Common Mistakes
- `JSON.parse` throws on invalid JSON — wrap in try/catch
- `require()` is cached — same object returned on repeated calls
- Circular dependencies partially work — but export may be incomplete at require time
- `async` function always returns Promise — even if you return plain value
- `Buffer.from(string)` encoding matters — default is UTF-8, specify if different
