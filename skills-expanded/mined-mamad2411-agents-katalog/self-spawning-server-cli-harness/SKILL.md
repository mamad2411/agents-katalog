---
name: self-spawning-server-cli-harness
description: A single 'cli run' command that spawns its own headless server subprocess, reads stdout until it sees a readiness sentinel with the URL, runs the test, and tears the server down — eliminating "start server in one terminal, connect in another" friction.
category: cli
version: 1.0.0
version_origin: extracted
tags: [cli, subprocess, bun, self-contained, testing]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/lukilabs/craft-agents-oss.git
source_ref: main
source_commit: 61f7d48a5b4fd0a8094f002c9e3aea5f3824dcfb
source_project: craft-agents-oss
source_path: apps/cli/src/server-spawner.ts
imported_at: 2026-04-18T00:00:00Z
---

# Self-spawning server CLI harness

## When to use
- CLI is a thin client over a long-running server, but users / CI want "one command, done".
- Server startup is expensive enough that for interactive use you want the daemon pattern, but for scripting / CI the spawn-and-die pattern beats it on UX.
- You need the test runner to KNOW when the server is ready before issuing requests.

## How it works
1. Auto-detect the server entry by walking up from `import.meta.dir` looking for `packages/server/src/index.ts` - no config file, works in monorepo + install.
2. Generate a fresh `CRAFT_SERVER_TOKEN` (`crypto.randomUUID()`) per spawn - each run has its own auth credential.
3. Strip toxic env vars before spawn - e.g. `CLAUDECODE` triggers a nesting guard in the SDK that rejects the child process. Use destructuring rest: `const { CLAUDECODE: _, ...parentEnv } = process.env`.
4. `Bun.spawn(['bun', 'run', serverEntry], { env: { ...parentEnv, CRAFT_SERVER_TOKEN, CRAFT_RPC_PORT: '0', CRAFT_RPC_HOST: '127.0.0.1' }, stdout: 'pipe', stderr: 'pipe' })`. Port `0` = OS picks.
5. Pipe server stderr through to our stderr (unless `--quiet`) so debug logs flow during CI failures.
6. Read stdout line-by-line looking for `CRAFT_SERVER_URL=ws://127.0.0.1:NNNNN`. Once found, resolve `{ url, token, stop }`.
7. Timeout the whole startup with `setTimeout(() => { proc.kill(); reject('did not start') }, 30_000)`.
8. Caller uses `{ url, token }`, then calls `stop()` which `SIGTERM`s and `await proc.exited`.

## Example
```ts
export async function spawnServer(opts): Promise<SpawnedServer> {
  const entry = opts.serverEntry ?? findServerEntry();
  const token = crypto.randomUUID();
  const { CLAUDECODE: _, ...parentEnv } = process.env;
  const proc = Bun.spawn(['bun', 'run', entry], {
    env: { ...parentEnv, CRAFT_SERVER_TOKEN: token, CRAFT_RPC_PORT: '0' },
    stdout: 'pipe', stderr: 'pipe',
  });
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => { proc.kill(); reject(new Error('timeout')); }, 30_000);
    (async () => {
      let buf = ''; const reader = proc.stdout.getReader(); const dec = new TextDecoder();
      while (true) {
        const { done, value } = await reader.read(); if (done) break;
        buf += dec.decode(value, { stream: true });
        const [head, ...tail] = buf.split('\n'); buf = tail.join('\n');
        for (const line of [head, ...tail]) {
          if (line.startsWith('CRAFT_SERVER_URL=')) {
            clearTimeout(timer);
            resolve({ url: line.slice(17).trim(), token,
              stop: async () => { proc.kill('SIGTERM'); await proc.exited; } });
            return;
          }
        }
      }
    })();
  });
}
```

## Gotchas
- If you forget to strip `CLAUDECODE`, the child refuses to start and your CLI hangs until timeout with no useful error.
- The server MUST print the URL line on a single flushed stdout line. If your server framework buffers logs, force a flush.
- `CRAFT_RPC_PORT=0` means OS chooses - DO NOT hardcode a port or parallel tests collide.
- Use stdout for READY signal, stderr for everything else. Mixing them is the #1 reason readiness detection "randomly" fails.
- On Windows, `SIGTERM` is approximated - ensure the server also handles `SIGHUP` / exits on stdin close as a fallback.
