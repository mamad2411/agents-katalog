---
name: run
description: Run a privileged (sudo) or remote-over-SSH command through sudo-proxy, which shows the user a single-keypress TUI approval prompt before anything executes. Use when a task needs to install packages, edit system files, manage services, or run any command on a remote host — NOT for ordinary unprivileged work in the current directory.
---

# sudo-proxy: run

sudo-proxy runs a command through a human-approval gate: every `execute`
pops a single-keypress Y/N prompt in the user's terminal (and, when
privileged, a live `sudo` password prompt) before the command runs. No
credential is stored; there is no auto-approve mode. It works for local
commands and for commands on a remote host reached over an SSH tunnel.

The `sudo-proxy-mcp` binary must already be on the user's `PATH`
(`cargo install sudo-proxy` or `cargo binstall sudo-proxy`). This plugin
launches the server; it does not install the binary.

## When to use it — and when not to

Use sudo-proxy only when the command genuinely needs it:

- **Privilege escalation** — installing packages, editing system files,
  managing services, anything that needs `sudo`.
- **A remote host** — running a command on another machine over SSH.

For everything else — reading files, building, running tests, git, any
unprivileged command in the working tree — keep using the ordinary Bash
tool. sudo-proxy adds a human-approval round-trip on *every* call, so
routing routine work through it just slows the user down.

## How to call it

1. **Start the server first.** Call `start_server` before the first
   `execute`. With no arguments it opens a local terminal with the
   approval TUI; pass `host` to open an SSH-tunnelled session to a remote
   machine. If a server is already running it returns immediately, so
   calling it again is cheap and safe.

2. **Execute with a clear description.** Every `execute` takes an `argv`
   array and should carry a `description`. That description is what the
   user reads in the approval prompt, so make it specific and honest —
   "Install nginx" or "Restart the ci-runner service", not "run command".
   A good description is the difference between an easy `y` and a puzzled
   deny.

3. **Match the host.** Pass the same `host` to `execute` that you passed
   to `start_server`; omit it for localhost. Set `privileged: false` for
   commands that should run as the current user but still behind the Y/N
   gate.

```jsonc
start_server()
execute({ "argv": ["apt", "install", "nginx"], "description": "Install nginx" })

// remote host
start_server({ "host": "ci-runner" })
execute({ "argv": ["systemctl", "restart", "buildkite"],
          "host": "ci-runner",
          "description": "Restart the Buildkite agent on ci-runner" })
```

Expect denials: the user may press `N`. Treat a denied command as a
deliberate choice, report it plainly, and do not try to route around the
gate.

## Reference

- Tools (`start_server`, `execute`, `status`, `stop_server`,
  `update_host`): https://github.com/tarides/sudo-proxy/blob/main/docs/mcp.md
- Security model and threat model:
  https://github.com/tarides/sudo-proxy/blob/main/docs/security.md
