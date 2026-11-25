---
name: agent-cli-detection-path
description: Auto-detect which coding-agent CLIs (claude, codex, opencode, etc.) are installed on PATH and register a runtime per detected agent × watched workspace.
category: agents
version: 1.0.0
tags: [cli, agents, detection, runtime, daemon]
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

- A local daemon needs to tell the server which agents it can actually execute.
- Users install agents one-by-one over time; you want the daemon to pick up newly-installed ones without restart (or at next poll, depending on cost).

## Steps

1. Maintain a static list of supported agent types with their canonical PATH name and env override:
   ```go
   type agentSpec struct {
       Name        string   // "claude"
       Command     string   // "claude"
       EnvPathVar  string   // "MYAPP_CLAUDE_PATH" to override
       EnvModelVar string   // "MYAPP_CLAUDE_MODEL" to override model
   }
   var supportedAgents = []agentSpec{
       {"claude", "claude", "MYAPP_CLAUDE_PATH", "MYAPP_CLAUDE_MODEL"},
       {"codex",  "codex",  "MYAPP_CODEX_PATH",  "MYAPP_CODEX_MODEL"},
       {"opencode", "opencode", "MYAPP_OPENCODE_PATH", "MYAPP_OPENCODE_MODEL"},
       // ...
   }
   ```
2. Detect each agent by looking up its binary and running `--version`:
   ```go
   for _, a := range supportedAgents {
       path := firstNonEmpty(os.Getenv(a.EnvPathVar), a.Command)
       resolved, err := exec.LookPath(path)
       if err != nil { continue }
       version, err := detectVersion(ctx, resolved)
       if err != nil { logger.Warn("version detect failed", "agent", a.Name); continue }
       detected[a.Name] = agentInfo{ Path: resolved, Version: version }
   }
   ```
3. `detectVersion` is just `agent --version` with a 5s timeout; capture stdout, trim.
4. Register one runtime per (agent × watched workspace). The runtime record on the server carries:
   ```json
   {
     "runtime_id": "<uuid>",
     "daemon_id": "<host-or-uuid>",
     "workspace_id": "<uuid>",
     "provider": "claude",
     "cli_version": "0.121.0",
     "device_name": "alice-macbook"
   }
   ```
5. Re-detect on the workspace-sync loop (every ~30s) so a newly-installed agent shows up without daemon restart. Skip detection on the hot path (task poll every 3s) — it's fine to lag by one sync interval.
6. On shutdown, send an explicit deregister for every registered runtime so the server stops routing tasks immediately instead of waiting for heartbeat timeout.

## Example

```
$ mycli daemon status
running (pid 12345, uptime 2h)

Detected agents:
  claude     0.121.0   /usr/local/bin/claude
  codex      0.45.0    /opt/homebrew/bin/codex
  opencode   2.1.3     /Users/alice/.local/bin/opencode

Registered runtimes: 6 (2 workspaces × 3 agents)
```

## Caveats

- Don't cache detection results across daemon restarts — users upgrade agents between restarts and you want the new version detected.
- A failed `--version` call is not fatal; log WARN and skip that agent. Don't let one broken agent block registration of the others.
- Per-agent env overrides (`MYAPP_CLAUDE_PATH`) matter for users with multiple installed versions (pnpm/npx fallbacks) or Windows where `.exe` suffixes differ.
