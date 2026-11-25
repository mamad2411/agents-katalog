---
name: windows-bash-backslash-halving
description: >-
  Fix for backslash-containing values (Windows named-pipe paths like \\.\pipe\x, UNC paths, regexes)
  getting corrupted when an agent writes them in a Bash-tool command on Windows (Claude Code's Bash tool
  running Git Bash). Use when: (1) a value you wrote with `\\` arrives downstream with `\`, (2)
  connecting to \\.\pipe\... fails with ENOENT although the pipe server is listening, (3) an env var
  exported in Bash differs from what a spawned node or python process reports, (4) a client silently
  falls back to a local or default path, so remote wiring looks "ignored". Not MSYS path conversion:
  MSYS2_ENV_CONV_EXCL and MSYS_NO_PATHCONV do not help.
---

# Windows Bash-tool backslash halving

## Problem

On Windows, command text sent through Claude Code's **Bash tool** (Git Bash) has `\\` collapsed to `\`
before the shell runs it, even inside single quotes, where POSIX forbids any escape processing. Values
that need exact doubled backslashes (named-pipe paths `\\.\pipe\x`, UNC paths `\\server\share`, regex
escapes) arrive corrupted, with no error.

## Trigger conditions

- The definitive probe: `printf '%s\n' 'a\\b'` in the Bash tool prints `a\b`. A real POSIX shell
  prints `a\\b`.
- `net.createConnection({ path: "\.\pipe\x" })` (mangled from `\\.\pipe\x`) fails with ENOENT.
- The symptom can be indirect. Software with a local fallback quietly runs locally when its `pipe:`
  endpoint env var is mangled, which masks the failure. Check the receiving process's environment, not
  the command you wrote.

## Solution

1. **Use a PowerShell tool** for setting or testing exact-backslash values, if your harness has one.
   `'pipe:\\.\pipe\x'` in a PowerShell-tool command arrives intact.
2. Or write the value to a **file** with the file-write or edit tool; no shell layer touches it. JSON
   files still need normal JSON escaping (`"pipe:\\\\.\\pipe\\x"` decodes to `pipe:\\.\pipe\x`).
3. Or **double every backslash** in Bash-tool text: write `\\\\` to deliver `\\`.
4. Verify at the consumer, not the producer:
   `node -e "console.log(JSON.stringify(process.env.MYVAR))"`.

## Verification

The `JSON.stringify` probe shows the exact characters the child process received. For pipe endpoints,
also check the pipe server's log for a connection attempt: zero attempts means the client never had a
valid path.

## Why it happens, and where it doesn't

- The halving happens in the **tool layer** that delivers command text to `bash.exe`, not in bash and
  not in MSYS environment conversion. That is why `MSYS2_ENV_CONV_EXCL` and `MSYS_NO_PATHCONV` have no
  effect.
- **Environment inheritance is faithful.** Bash passes values to child processes unchanged. Only the
  literal command text you write is affected, so a value set once through PowerShell, the registry or a
  settings file flows through correctly afterwards.
- It does not apply to a PowerShell tool, to file contents written with the file tools, or to values a
  Windows process injects itself (for example the harness's own `env` settings).

## Example

A plugin client reads its server endpoint from an env var. Exported in a Bash-tool smoke test as
`MY_ENDPOINT=pipe:\\.\pipe\my-app-server`, it arrived as `pipe:\.\pipe\my-app-server`. The client got
ENOENT and fell back to spawning a local server, so the remote bridge looked dead. The identical test
run through the PowerShell tool connected to the remote server.

## Notes

- Seen on Windows 11 with Claude Code's Bash tool (Git Bash). Re-run the `printf` probe after a harness
  upgrade: if it prints `a\\b`, the bug is fixed in your version.
