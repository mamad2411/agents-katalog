---
name: bash-exec
description: "Shell command execution via `bash.exec`. Use when a task requires running terminal commands and inspecting bounded stdout or stderr under policy controls."
aliases:
  - shell
  - terminal
triggers:
  - through bash
  - use bash
  - shell command
  - terminal command
  - through terminal
  - через bash
  - через терминал
  - вызови баш
tool_names:
  - bash.exec
preferred_tool_order:
  - bash.exec
execution_mode: executable
---

# bash-exec

Use this skill for shell command execution through `bash.exec`.
Prefer it for diagnostics, package installs, service management, and deterministic CLI workflows inside the allowed workspace/policy scope.

## Tool family

- `bash.exec`

## Required flow

1. Check trusted runtime notes first when the task depends on OS, shell, package manager, or service manager.
2. If the environment is still unclear, run a small inspection command before any mutating command.
3. Explain intended command and expected output.
4. Call `bash.exec`.
5. If the command may prompt or keep running, set `yield_time_ms` on the first call.
6. If `bash.exec` returns `session_id`, keep calling `bash.exec` with that same `session_id`.
7. Send prompt answers through `chars` such as `y\n`; use empty `chars` to poll for more output.
8. Parse `exit_code`, `stdout`, and `stderr` before final answer.
9. If command fails, return concise error and next safe step.

Supported params to consider:
- `cwd`
- `env`
- `shell`
- `login`
- `yield_time_ms`
- `session_id`
- `chars`

Examples:
- inspect environment: `cat /etc/os-release 2>/dev/null || uname -a`
- update packages: `sudo apt update`
- install nginx: `sudo apt install -y nginx`
- check service: `systemctl status nginx --no-pager`
- interactive install prompt: first call `npx vibe-kanban` with `yield_time_ms=500`, then continue with the returned `session_id` and `chars="y\n"` if the tool output asks for confirmation

## Safety rules

- Respect policy restrictions for commands and working directory.
- Never execute destructive commands without explicit user approval.
- Keep command output bounded and relevant to the request.
- Runtime routes the correct skill automatically; do not send `skill_name`.
