---
name: claude-cli-subprocess-adapter
description: Embed Claude inference in a zero-dep Node.js tool by spawning `claude -p` as a subprocess with a stdin-piped prompt, `--output-format text`, and a timeout guard.
category: ai
tags:
  - claude-cli
  - subprocess
  - node
  - zero-dep
  - stdin-pipe
  - adapter
triggers:
  - claude -p
  - node spawn claude
  - embed claude cli
  - zero-dep claude
  - child_process claude
source_project: inversion-loop
version: 0.1.0-draft
linked_knowledge:
  - claude-cli-bare-flag-disables-oauth
---

# claude-cli-subprocess-adapter

## When to use

You want to call Claude from a Node.js tool without adding `@anthropic-ai/sdk` as a dependency, and the user already has Claude Code CLI installed and authenticated (OAuth session via keychain). Suitable for batch pipelines, orchestrators, and agent loops where:

- Cold-start latency per call (~3–6s) is acceptable
- Each call needing fresh context is actually desirable (natural separation for adversarial / judge-style prompts)
- Zero dependency install is a hard constraint

Not suitable for interactive streaming UIs, per-token callbacks, or tight loops calling Claude hundreds of times — use the SDK for those.

## The technique

Spawn `claude -p --model <id> --output-format text` and pipe the prompt via stdin, not argv. Collect stdout. Enforce a timeout with `child.kill('SIGKILL')`.

```js
const { spawn } = require('child_process');

function runClaude(prompt, opts = {}) {
  const model = opts.model || 'claude-opus-4-7';
  const timeoutMs = opts.timeoutMs || 180000;
  const args = ['-p', '--model', model, '--output-format', 'text'];

  return new Promise((resolve, reject) => {
    const child = spawn('claude', args, {
      stdio: ['pipe', 'pipe', 'pipe'],
      shell: process.platform === 'win32',
    });
    let stdout = '', stderr = '';
    const timer = setTimeout(() => {
      child.kill('SIGKILL');
      reject(new Error(`claude CLI timeout after ${timeoutMs}ms`));
    }, timeoutMs);

    child.stdout.on('data', d => { stdout += d.toString('utf8'); });
    child.stderr.on('data', d => { stderr += d.toString('utf8'); });
    child.on('error', err => { clearTimeout(timer); reject(err); });
    child.on('close', code => {
      clearTimeout(timer);
      if (code !== 0) return reject(new Error(`claude CLI exit ${code}: ${stderr.trim()}`));
      resolve(stdout.trim());
    });

    child.stdin.write(prompt);
    child.stdin.end();
  });
}
```

## Why stdin, not argv

Prompts can be thousands of tokens and contain shell metacharacters, quotes, newlines. Passing via argv forces you to escape carefully and hits OS argv-length limits (128KB on Windows). Stdin has no length limit and bypasses shell interpretation entirely.

## Integration as injectable adapter

Wrap the raw runner so orchestrators can inject a `callClaude(prompt)` function and swap between real / mock:

```js
function makeCallClaude(opts = {}) {
  return async (prompt, perCallOpts) => runClaude(prompt, { ...opts, ...perCallOpts });
}

// Orchestrator injects either makeCallClaude() or a mock returning fixture strings
await orchestrate({ callClaude: makeCallClaude({ log }) });
```

This keeps every module unit-testable with offline fixtures and only the wiring layer depends on the real CLI.

## Watch out

- **Do not pass `--bare`** if relying on OAuth auth — see linked knowledge `claude-cli-bare-flag-disables-oauth`. It silently exits 1 with no stderr.
- Windows: `spawn` needs `shell: true` so the `.cmd` shim in PATH resolves. Accept the `[DEP0190]` deprecation warning — it's benign here because args come from your own code, not untrusted input.

## Counterexample

Don't use this when you need token-level streaming to a UI — `--output-format text` buffers the whole response. Don't use for >100 calls/minute workloads — cold-start cost dominates. For either case, use `@anthropic-ai/sdk` with `.stream()`.

## See also

- Pitfall: `claude-cli-bare-flag-disables-oauth` — `--bare` silently kills OAuth auth
- Adjacent skill: `claude-cli-from-jvm-via-node-wrapper` — JVM callers go through Node wrapper; this skill is the pure-Node direct adapter.
