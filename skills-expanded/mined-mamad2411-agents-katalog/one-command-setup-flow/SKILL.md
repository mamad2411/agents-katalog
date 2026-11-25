---
name: one-command-setup-flow
description: Bundle CLI configure + authenticate + daemon start into one `cli setup` command, with per-environment profiles (cloud vs self-host) and custom-port overrides.
category: cli
version: 1.0.0
tags: [cli, setup, onboarding, profiles, cobra]
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

- A CLI where first-time setup has always required 3-5 manual steps (config set, login, start daemon).
- You want a single command to onboard users, with sensible defaults for cloud and self-host.

## Steps

1. Define a `setup` command with two modes:
   ```go
   setup := &cobra.Command{
     Use:   "setup",
     Short: "Configure, authenticate, and start the daemon",
   }
   setup.AddCommand(selfHostCmd()) // mycli setup self-host
   rootCmd.AddCommand(setup)
   ```
   Default `setup` uses cloud endpoints; `setup self-host` targets localhost with overridable flags.
2. `setup self-host` flags let users override defaults without editing config:
   ```go
   cmd.Flags().StringVar(&serverURL, "server-url", "http://localhost:8080", "")
   cmd.Flags().StringVar(&appURL,    "app-url",    "http://localhost:3000", "")
   cmd.Flags().Int(   "port",          8080, "backend port (sets server-url)")
   cmd.Flags().Int(   "frontend-port", 3000, "frontend port (sets app-url)")
   cmd.Flags().String("profile",       "",   "profile name (default: derived from URL)")
   ```
3. Implementation is a sequence of small, idempotent steps, each recoverable:
   ```
   1. Resolve server/app URL from flags or defaults
   2. Write to profile config (~/.mycli/profiles/<name>/config.json)
   3. Open browser to {appURL}/auth/cli-callback?port=<local listener>
   4. Wait for callback with token on localhost
   5. Save token to profile config
   6. Fetch workspace list with the token
   7. Start daemon in the background with this profile
   8. Poll daemon health endpoint until ready
   9. Print success banner + "what next" hints
   ```
4. Each step can be re-run independently:
   - `mycli login` repeats steps 3-5.
   - `mycli config set server_url ...` repeats step 2.
   - `mycli daemon start` repeats steps 7-8.
5. Prompt before overwriting an existing profile config (don't clobber silently).

## Example

```
$ mycli setup self-host --port 9090 --frontend-port 4000
==> Writing config to ~/.mycli/profiles/localhost-9090/config.json
==> Opening browser for authentication...
    (paste token if browser doesn't open: http://localhost:4000/auth/cli)
✓ Authenticated as alice@example.com
==> Discovered 2 workspaces: "Engineering", "Marketing"
==> Starting daemon (profile: localhost-9090)...
✓ Daemon running (PID 12345)

Next: assign an issue to an agent from http://localhost:4000
```

## Caveats

- Browser-less environments (CI, VM without X): flag `--token` path that reads a PAT from stdin or env; don't force browser auth.
- Daemon start + healthcheck poll with a 60s timeout; if it fails, print the log path and exit non-zero.
- Profile name derivation must be deterministic (by URL or worktree), so re-running `setup` targets the same profile.
