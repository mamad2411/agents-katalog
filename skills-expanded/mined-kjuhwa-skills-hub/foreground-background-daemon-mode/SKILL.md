---
name: foreground-background-daemon-mode
description: CLI-managed daemon with foreground (for debug) and background (default, detached) modes, log-file path convention, and a status-check sub-command.
category: cli
version: 1.0.0
tags: [cli, daemon, background-process, logs, debugging]
source_type: extracted-from-git
source_url: https://github.com/multica-ai/multica.git
source_ref: main
source_commit: 6cd49e132de7632b1f2aaa675c98e8eca9308bb7
source_project: multica
imported_at: 2026-04-18T00:00:00Z
version_origin: extracted
confidence: medium
---

## When to use

- A CLI that spawns a long-lived background process (task runner, sync daemon).
- Users need a way to start it without a terminal, check on it, tail logs, and stop it cleanly.

## Steps

1. `daemon start` defaults to background (double-fork on Unix, `CREATE_NEW_PROCESS_GROUP` on Windows). Add `--foreground` for interactive debug:
   ```go
   startCmd.Flags().Bool("foreground", false, "run daemon in the foreground (for debug)")
   ```
2. Log to a canonical path unless the foreground flag is set:
   ```
   ~/.myapp/daemon.log                            # default
   ~/.myapp/profiles/<name>/daemon.log            # per-profile
   ```
   In foreground mode, log to stdout/stderr directly.
3. `daemon status` reads the PID file, verifies the process exists, reports uptime and detected agents:
   ```go
   pid := readPIDFile(profile)
   if pid == 0 || !processAlive(pid) { fmt.Println("not running"); return }
   // read the daemon's own health endpoint for detailed status
   status := httpGet(fmt.Sprintf("http://127.0.0.1:%d/status", healthPort(profile)))
   ```
4. `daemon logs` tails the log file with `-f`/`-n`:
   ```go
   logsCmd.Flags().BoolP("follow", "f", false, "follow log output")
   logsCmd.Flags().IntP("lines",  "n", 50,    "number of lines to show")
   ```
5. `daemon stop` sends SIGTERM (or `TerminateProcess` on Windows), waits up to N seconds, falls back to SIGKILL. Clean up the PID file on exit.
6. `daemon restart` is stop + start, preserving the profile flag.

## Example

```
$ mycli daemon start
Daemon running in background (pid 12345). Logs at ~/.myapp/daemon.log.

$ mycli daemon status
running (pid 12345, uptime 2h, 3 agents, 5 runtimes)

$ mycli daemon logs -f
[12:30:01] registered runtime ... (workspace=Engineering, provider=claude)
[12:31:15] task 492abc claimed

$ mycli daemon stop
Daemon stopped.
```

## Caveats

- Double-fork detach is Unix-specific; on Windows use `syscall.CreateProcess` with `DETACHED_PROCESS` + `CREATE_NEW_PROCESS_GROUP`.
- PID file is not a lock — combine with early port-bind on the daemon's health port to catch stale PID cases atomically.
- Rotate the log file if it can grow unbounded; users will run the daemon for weeks.
