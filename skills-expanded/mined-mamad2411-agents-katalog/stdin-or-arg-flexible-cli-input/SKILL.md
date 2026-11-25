---
name: stdin-or-arg-flexible-cli-input
description: Accept the same CLI arg either as a trailing positional or piped from stdin, with a --stdin flag to force-read even when a positional is present — the UNIX pipe-friendly default.
category: cli
version: 1.0.0
version_origin: extracted
tags: [cli, stdin, unix-pipes, ergonomics]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/lukilabs/craft-agents-oss.git
source_ref: main
source_commit: 61f7d48a5b4fd0a8094f002c9e3aea5f3824dcfb
source_project: craft-agents-oss
source_path: apps/cli/src/commands.test.ts
imported_at: 2026-04-18T00:00:00Z
---

# Flexible stdin-or-positional CLI input

## When to use
- CLI that takes a message / prompt / document as input.
- Users and CI alike will want to `echo foo | tool send` and `tool send "foo"` and maybe `cat file | tool send --stdin` (explicit).
- Want to NOT print interactive prompts when stdin is a pipe.

## How it works
1. Detect piped stdin: `!process.stdin.isTTY`.
2. Resolution order per command (`send`, `run`, etc.):
   - If trailing positional arg present AND not `--stdin` flag, use positional.
   - Else if stdin is piped, read stdin to EOF and use it.
   - Else, prompt interactively (only if stdin.isTTY).
3. Provide a `--stdin` flag to opt-in even when positional is non-empty (rare but useful for automation that always pipes).
4. Print streaming output to stdout; diagnostics to stderr. Script writers shouldn't have to parse your debug logs.
5. Exit codes:
   - `0` success, `1` error, `130` user-interrupt (Ctrl+C).

## Example
```ts
async function resolveInput(arg: string | undefined, flags: { stdin: boolean }) {
  if (!flags.stdin && arg) return arg;
  if (!process.stdin.isTTY) {
    const chunks: Buffer[] = [];
    for await (const c of process.stdin) chunks.push(c);
    return Buffer.concat(chunks).toString('utf8').trim();
  }
  throw new Error('provide input as argument or via stdin');
}
```

Supported invocations:
```bash
cli send abc "hello"                      # positional
echo "hello" | cli send abc                # piped
cat file.txt | cli send abc --stdin        # explicit override
```

## Gotchas
- Reading stdin to EOF blocks on a TTY; always guard with `isTTY`.
- When printing streaming responses, flush line-by-line - don't hold output for piped consumers.
- Structured output (`--json`) should go to stdout, human diagnostics to stderr - lets users `cli --json sessions | jq` without noise.
- On Windows, piping from CMD.exe can inject `\r` in stdin - `trim()` at the boundary.
