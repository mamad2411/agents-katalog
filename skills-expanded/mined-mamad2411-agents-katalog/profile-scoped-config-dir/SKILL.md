---
name: profile-scoped-config-dir
description: Per-profile CLI config directories (~/.myapp/profiles/<name>/) so users can run multiple environments (prod, staging, worktrees) side-by-side without collisions.
category: cli
version: 1.0.0
tags: [cli, config, profiles, daemon, isolation]
source_type: extracted-from-git
source_url: https://github.com/multica-ai/multica.git
source_ref: main
source_commit: 6cd49e132de7632b1f2aaa675c98e8eca9308bb7
source_project: multica
imported_at: 2026-04-18T00:00:00Z
version_origin: extracted
confidence: high
---

## When to use

- CLI that manages long-lived background state (daemon PID, local token, workspace roots).
- Users want to point at cloud and a self-host at the same time, or run multiple dev environments.

## Steps

1. Define a profile root per-profile, everything in it is scoped:
   ```
   ~/.myapp/
     config.json               # default profile (legacy / implicit)
     daemon.pid                # default daemon PID
     profiles/
       staging/
         config.json
         daemon.pid
         daemon.log
       dev-feat-auth-347/
         config.json
         daemon.pid
         workspaces/           # per-profile work dir
   ```
2. Accept `--profile <name>` on every command that reads/writes profile state. Without it, use the default root:
   ```go
   profile, _ := cmd.Flags().GetString("profile")
   cfgDir := defaultConfigDir()
   if profile != "" { cfgDir = filepath.Join(defaultConfigDir(), "profiles", profile) }
   ```
3. Derive per-profile ports deterministically from the profile name:
   ```go
   func profileHealthPort(profile string) int {
       if profile == "" { return defaultHealthPort }
       h := fnv.New32a(); h.Write([]byte(profile))
       return defaultHealthPort + 1 + int(h.Sum32()%1000)
   }
   ```
4. Include the profile name in log lines and in any daemon-registered runtime display name, so "which daemon is this?" is obvious from UI.
5. Document the isolation table in CONTRIBUTING:
   | Resource        | Default                    | Profile mode                              |
   |-----------------|----------------------------|-------------------------------------------|
   | Config          | `~/.myapp/config.json`     | `~/.myapp/profiles/<name>/config.json`    |
   | Daemon PID      | `~/.myapp/daemon.pid`      | `~/.myapp/profiles/<name>/daemon.pid`     |
   | Health port     | e.g. 19514                 | 19514 + 1 + hash(name)%1000               |
   | Workspaces dir  | `~/myapp_workspaces/`      | `~/myapp_workspaces_<name>/`              |

## Example

Concurrent environments:

```bash
myapp setup                                  # default profile → cloud
myapp setup self-host                        # default profile → now localhost (overwrites!)
myapp setup self-host --profile staging      # staging profile → staging server
myapp daemon start --profile staging         # staging daemon
myapp daemon status --profile staging        # only reports this daemon
myapp daemon logs -f                         # default daemon's logs, unaffected
```

## Caveats

- Commands MUST error loud if a profile name doesn't exist, rather than silently falling back to default — users trust the flag to be strict.
- Before `setup` overwrites an existing profile config, prompt "continue? y/N" unless `--force`.
- When building `PATH` for the daemon's child processes, prepend the daemon's own binary dir so agent-spawned `myapp` calls hit the same binary.
