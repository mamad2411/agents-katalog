---
name: validate-server-21-step-harness
description: A 21-step sequential integration test that walks the whole RPC surface (connect, health, CRUD, send+stream, tool use, source create, skill create, cleanup) and keeps going past failures to print a single summary at the end.
category: cli
version: 1.0.0
version_origin: extracted
tags: [integration-test, cli, smoke-test, rpc]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/lukilabs/craft-agents-oss.git
source_ref: main
source_commit: 61f7d48a5b4fd0a8094f002c9e3aea5f3824dcfb
source_project: craft-agents-oss
source_path: docs/cli.md
imported_at: 2026-04-18T00:00:00Z
---

# --validate-server integration harness

## When to use
- CI has to verify a newly-built server binary passes every public RPC call before shipping.
- You want ONE command that creates + cleans up test resources (sessions, sources, skills) without polluting user state.
- Failures should be surveyed end-to-end, not halted at the first issue - faster iteration than re-running 20 times.

## How it works
1. CLI flag `--validate-server` spawns (or connects to) a server, runs a fixed ordered list of RPC calls.
2. Representative sequence (21 steps):
   1. Connect + handshake
   2. `credentials:healthCheck`
   3. `system:versions`
   4. `system:homeDir`
   5. `workspaces:get`
   6. `sessions:get`
   7. `LLM_Connection:list`
   8. `sources:get`
   9. `sessions:create` - **prefix with `__cli-validate-`** so cleanup is grep-safe
   10. `sessions:getMessages`
   11. Send message + stream (text)
   12. Send message + tool use (Bash)
   13. `sources:create` (ephemeral Cat Facts API)
   14. Send + source mention
   15. Send + skill create (agent writes a SKILL.md)
   16. `skills:get` (verify appears)
   17. Send + skill mention
   18. `skills:delete`
   19. `sources:delete`
   20. `sessions:delete`
   21. Disconnect
3. Each step wrapped: `try { ...; results.push({ step, ok: true }) } catch (e) { results.push({ step, ok: false, err: e.message }) }`. NEVER rethrow from inside the loop.
4. After loop, print a summary; exit 0 if `results.every(ok)`, else exit 1.
5. `--json` mode emits the results array as a machine-readable summary for CI parsing.
6. Auto-cleanup inside `finally` for every created resource - even if step 10 fails, session-delete still runs.

## Example
```ts
const steps: Array<[name: string, fn: () => Promise<void>]> = [
  ['connect', async () => { await client.connect(); }],
  ['health', async () => { await client.invoke('credentials:healthCheck'); }],
  /* ...20 more */
];
const results = [];
for (const [name, fn] of steps) {
  const start = Date.now();
  try { await fn(); results.push({ name, ok: true, ms: Date.now() - start }); }
  catch (e) { results.push({ name, ok: false, err: String(e), ms: Date.now() - start }); }
}
console.log(JSON.stringify(results, null, 2));
process.exit(results.every(r => r.ok) ? 0 : 1);
```

## Gotchas
- Prefix test resources with something grep-safe (`__cli-validate-<uuid>`) so developers can `grep | xargs delete` leftovers.
- ALWAYS clean up in the reverse order of creation (skill -> source -> session).
- Keep the list ordered from "cheap + foundational" to "expensive + integration" - cheap failures short-circuit the useful signal.
- Print timings - regressions often show up as "was 200ms, now 15s" before they become outright failures.
- Mention in docs that --validate-server MUTATES state. Surprises burn trust.
