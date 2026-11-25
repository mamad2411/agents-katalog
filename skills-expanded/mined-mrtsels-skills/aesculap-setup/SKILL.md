---
name: aesculap-setup
description: Install, configure, and troubleshoot Aesculap — the self-healing daemon for Hermes Agent. Covers Linux systemd and macOS launchd deployments, scope tier selection, identity file blacklisting, provider config (triage/selffix), and git rollback preconditions.
version: 1.0.0
author: agent
platforms: [linux, macos]
metadata:
  hermes:
    tags: [devops, hermes, self-healing, systemd, launchd, macos]
    related_skills: [hermes-agent]
---

# Aesculap Self-Healing Daemon Setup

Aesculap is a self-healing plugin for Hermes Agent: it monitors log errors and process liveness (Tier 0 probes), triages failures with an LLM (Tier 1), and either self-fixes within safe bounds (Tier 2) or escalates to a coding agent or human.

Source: https://github.com/banxia-O/Aesculap-hermes (installed as editable package from `/Users/minimx/Aesculap-hermes`).

## Quick Install

```bash
# Install (macOS: conda Python)
pip install aesculap-hermes

# Or if editable from source:
cd /path/to/Aesculap-hermes && pip install -e .
```

## Configuration

### Scope Tiers (PRD §9.1)

| Tier | Scope | Risk |
|------|-------|------|
| A | Project tree only (`hermes-agent/`) | ⭐ safest, recommended |
| B | Hermes config dir + project tree | ⭐⭐⭐ |
| C | Whole host / environment | ⭐⭐⭐⭐⭐ ONLY dedicated host |

### Identity Files to Blacklist

The wizard scans `~/.hermes/` for these files and prompts the user to blacklist them (they are persona/memory files that must never be modified):

Common candidates:
- `~/.hermes/SOUL.md`
- `~/.hermes/memories/MEMORY.md`
- `~/.hermes/memories/USER.md`
- `~/.hermes/memories/MEMORY.md.lock`
- `~/.hermes/memories/USER.md.lock`

These go under `scope.identity_files` in the config.

### Provider Config (Triage & Selffix)

Use DeepSeek with OpenAI-compatible protocol if Hermes uses DeepSeek:

```yaml
triage:
  provider: openai_compatible
  model: deepseek-v4-flash
  base_url: https://api.deepseek.com
  api_key_env: DEEPSEEK_API_KEY

selffix:
  provider: openai_compatible
  model: deepseek-v4-flash
  base_url: https://api.deepseek.com
  api_key_env: DEEPSEEK_API_KEY
```

Both triage and self-fix can use the same model (flash is fine for self-healing). Use `deepseek-v4-pro` only if triage needs deeper reasoning.

### Full Config Template

```yaml
enabled: true
mode: fix
aesculap_home: /opt/aesculap
state_dir: /Users/minimx/.hermes/aesculap/state
audit_log_path: /Users/minimx/.hermes/aesculap/audit.jsonl

scope:
  tier: A
  project_root: /Users/minimx/.hermes/hermes-agent
  identity_files:
    - /Users/minimx/.hermes/SOUL.md
    - /Users/minimx/.hermes/memories/MEMORY.md
    - /Users/minimx/.hermes/memories/USER.md
  extra_blacklist: []

detectors:
  log_paths:
    - /Users/minimx/.hermes/logs/hermes.log
  error_patterns:
    - Traceback
    - CRITICAL
    - \bERROR\b
  liveness_interval_seconds: 120
  full_checkup_interval_seconds: 86400

triage:
  provider: openai_compatible
  model: deepseek-v4-flash
  base_url: https://api.deepseek.com
  api_key_env: DEEPSEEK_API_KEY

selffix:
  provider: openai_compatible
  model: deepseek-v4-flash
  base_url: https://api.deepseek.com
  api_key_env: DEEPSEEK_API_KEY
  retry_budget: 3
  observe_window_seconds: 60

coding_agent:
  tool: claude
  command_template: ""

notify:
  command_template: "hermes gateway send --text {message}"
  cooldown_seconds: 3600
```

## Installation by Platform

### Linux (systemd)

```bash
# Validate config
aesculap config /path/to/aesculap.yaml

# Install systemd unit (user scope, no root)
aesculap install-systemd /path/to/aesculap.yaml --scope user --write

# Enable and start
systemctl --user daemon-reload
systemctl --user enable --now aesculap.service

# For boot-start without active login session:
loginctl enable-linger $USER
```

### macOS (launchd)

Since macOS has no systemd, use LaunchAgent instead. Aesculap's `install-systemd` writes a .service file but the `--write` flag works on macOS to produce the file; however `systemctl` will fail. Replace with launchd:

**Step 1: Create wrapper script** (needed to source `.env` — launchd doesn't inherit shell env vars):

```bash
cat > ~/.hermes/bin/aesculap-launcher.sh << 'SCRIPT'
#!/bin/bash
set -e
if [ -f ~/.hermes/.env ]; then
    set -a
    source ~/.hermes/.env
    set +a
fi
exec /path/to/python3 -m aesculap start /Users/minimx/.hermes/aesculap.yaml
SCRIPT
chmod +x ~/.hermes/bin/aesculap-launcher.sh
```

**Step 2: Create LaunchAgent plist:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.aesculap.daemon</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/minimx/.hermes/bin/aesculap-launcher.sh</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/minimx</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>ThrottleInterval</key>
    <integer>5</integer>
    <key>StandardOutPath</key>
    <string>/Users/minimx/.hermes/logs/aesculap-stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/minimx/.hermes/logs/aesculap-stderr.log</string>
</dict>
</plist>
```

Write to `~/Library/LaunchAgents/com.aesculap.daemon.plist`.

**Step 3: Load and verify:**

```bash
launchctl load ~/Library/LaunchAgents/com.aesculap.daemon.plist
sleep 2
launchctl list | grep aesculap
# Expected: PID\t0\tcom.aesculap.daemon

# Verify status
aesculap status ~/.hermes/aesculap.yaml
```

**Control commands:**

```bash
launchctl stop com.aesculap.daemon      # pause
launchctl start com.aesculap.daemon     # resume
launchctl unload ~/Library/LaunchAgents/com.aesculap.daemon.plist  # uninstall
launchctl load ~/Library/LaunchAgents/com.aesculap.daemon.plist    # reinstall
```

## State Directory on macOS

**Pitfall:** The default `state_dir: /var/lib/aesculap` requires root. As a user-scope daemon, this causes `PermissionError: [Errno 13] Permission denied: '/var/lib/aesculap'`.

**Fix:** Use a path under the user's home:

```yaml
state_dir: /Users/minimx/.hermes/aesculap/state
audit_log_path: /Users/minimx/.hermes/aesculap/audit.jsonl
```

## Git Precondition

Aesculap needs git for rollback (PRD §7.1). Initialize `~/.hermes` as a git repo:

```bash
cd ~/.hermes
git init
```

Add a `.gitignore` that excludes runtime artifacts (not just secrets):

```
# Aesculap runtime state (auto-generated)
aesculap/state/
aesculap/audit.jsonl

# Ephemeral Hermes dirs
logs/
sessions/
cron/output/
image_cache/
```

## Verification

```bash
# Validate config
aesculap config ~/.hermes/aesculap.yaml
# Expected: config OK: tier=A mode=fix probes=0 enabled=True

# Run probes once
aesculap probe ~/.hermes/aesculap.yaml

# Check status
aesculap status ~/.hermes/aesculap.yaml
# Shows: mode, enabled, tier, audit log records, open issues

# Toggle master switch
aesculap enable ~/.hermes/aesculap.yaml
aesculap disable ~/.hermes/aesculap.yaml

# Switch mode
aesculap mode observe ~/.hermes/aesculap.yaml   # watch-only
aesculap mode fix ~/.hermes/aesculap.yaml        # auto-fix (default)
```

## CLi Reference

```
aesculap config PATH         Validate config
aesculap probe PATH          Run Tier 0 probe suite once
aesculap start PATH          Run daemon foreground
aesculap enable/disable PATH Master switch
aesculap mode fix|observe    Switch mode
aesculap status PATH         Show daemon + open issue status
aesculap stop                Print stop commands
aesculap install PATH        Interactive wizard (not macOS-friendly)
aesculap install-systemd PATH --scope user [--write]  systemd unit
```
