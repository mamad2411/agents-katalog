---
name: stay-awake
description: Use when running long coding-agent sessions on macOS that risk idle sleep, especially when tests, builds, debugging, or CI triage may outlast display or system sleep timers, when starting implementation from a spec or ticket set or similar long-running task, or when the user says "caffeinate yourself".
---

# Stay Awake

## Overview

Keep macOS awake during agent work using `caffeinate` with a bounded lifecycle.
Prefer process-coupled assertions, then timeout-based assertions, and only use unbounded assertions with explicit cleanup.

GitHub Copilot CLI runs through shell-backed sessions and tool execution. In practice, the most reliable wake assertion target is the shell or concrete command process that will own the long-running work, not an abstract "agent" process. If the work is started from a shell, capture that shell's PID with `$$`; if it is started from a wrapper script or a specific child process, use that process ID instead.

## When to Use

Use this skill when:

- The session may run long enough for idle sleep to interrupt work
- You are running long tests, builds, or debugging loops on macOS
- You need predictable wake-lock cleanup at session end

Do not use this skill on non-macOS systems.

## Decision Order

1. **Attach to the agent process when possible** (best)
2. **Use a timeout when process attachment is not possible**
3. **Use bare `caffeinate` only as fallback**, then always cancel at session end

## Quick Reference

| Situation | Command | Cleanup behavior |
| --- | --- | --- |
| Agent process ID is known | `caffeinate -i -w <process_id>` | Stops automatically when process exits |
| Duration is known | `caffeinate -i -t <seconds>` | Stops automatically at timeout |
| No PID and no duration | `caffeinate -i` | Must be manually stopped |
| Long single command | `caffeinate -i <command> [args...]` | Stops when wrapped command exits |

## Workflow

### 1) Prefer a process-coupled wake lock

If the shell or long-running command process ID is available, tie the assertion to that process:

```bash
caffeinate -i -w <process_id>
```

If the work is started from a shell, the current shell's process ID can be read directly with `$$` and used immediately:

```bash
agent_process_id=$$
caffeinate -i -w "$agent_process_id"
```

This is the safest default because wakefulness ends with the process that owns the long-running work. If the agent is not running inside a shell, if the chosen process exits immediately, or if the work is being driven by a wrapper process instead of a shell, prefer a timeout or a fallback `caffeinate -i` with cleanup instead.

### 2) Otherwise use a timeout

If no stable process ID is available, choose a bounded timeout:

```bash
caffeinate -i -t 5400   # 90 minutes
```

Use seconds. Renew only when needed.

### 3) Fallback to bare caffeinate only with explicit cleanup

If neither process-coupling nor timeout is feasible:

```bash
caffeinate -i &
caffeinate_process_id=$!
```

At end of session, stop it:

```bash
kill "$caffeinate_process_id"
```

## Prompting Pattern

When the user has not specified a wake-lock strategy, ask in this order:

1. Can this be attached to the shell or long-running command process that will own the work?
2. If not, what timeout should be used?
3. If neither is known, confirm temporary fallback to bare `caffeinate -i` and commit to end-of-session cleanup.

## Caffeinate Notes (researched)

- `-w <pid>` releases assertion when the target process exits.
- A shell-based agent can discover its current shell process ID with `$$` (Bash/Zsh/sh semantics), and can pass that value to `caffeinate -w` when the shell is the process that should govern the wake lock.
- `-t <seconds>` is ignored when `caffeinate` is wrapping a utility command.
- `-u` defaults to 5 seconds if `-t` is not provided.
- `-s` is valid only on AC power.
- Without utility arguments, assertions persist until `caffeinate` exits.

## Common Mistakes

| Mistake | Why it fails | Correction |
| --- | --- | --- |
| Running `caffeinate` indefinitely by default | Easy to forget cleanup | Prefer `-w` or `-t` first |
| Using `-s` without confirming AC power | Assertion may not behave as expected on battery | Prefer `-i` unless AC-only behavior is intended |
| Using `-u` for long sessions | `-u` is not a durable long-session lock | Use `-i`, optionally with `-w` or `-t` |
| Starting background `caffeinate` without tracking PID | Cleanup is unreliable | Capture `$!` and kill at session end |

## Rationalization Table

| Excuse | Reality |
| --- | --- |
| "I will remember to stop it later." | Unbounded assertions are easy to forget. Use `-w` or `-t` first. |
| "I do not need a cleanup plan for this short task." | Short tasks often expand. Always use bounded or explicitly tracked lifecycle. |
| "Bare `caffeinate` is faster." | It is faster now but riskier later. One extra flag prevents stale wake locks. |

## Red Flags

- Starting with bare `caffeinate` when PID or timeout is available
- Running `caffeinate` in the background without saving its PID
- Ending session without confirming wake-lock cleanup

If any red flag appears, switch to `-w`, switch to `-t`, or clean up the fallback process immediately.

## References

- `man caffeinate` (local Darwin manual)
- https://keith.github.io/xcode-man-pages/caffeinate.8.html
- https://www.manpagez.com/man/8/caffeinate/
