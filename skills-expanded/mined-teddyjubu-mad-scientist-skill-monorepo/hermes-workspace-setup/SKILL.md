---
name: hermes-workspace-setup
description: Connect and troubleshoot Hermes Workspace (web UI at port 3001) to its Hermes Agent backend (API server at port 8642). Use when the dashboard shows "Connecting to Hermes Agent..." or when the enhanced /api/* endpoints are missing.
version: 1.0.0
metadata:
  hermes:
    tags: [hermes, workspace, web-ui, api-server, gateway, troubleshooting]
    related_skills: [hermes-agent, hermes-agent-setup]
---

# Hermes Workspace Setup & Troubleshooting

Hermes Workspace is a web UI (Node/Vite) that connects to the Hermes Agent gateway's built-in HTTP API server. When it shows "Connecting to Hermes Agent...", the backend API is either not running or missing the enhanced endpoints.

## What This Skill Does

This skill Connect and troubleshoot Hermes Workspace (web UI at port 3001) to its Hermes Agent backend (API server at port 8642). Use when the dashboard shows "Connecting to Hermes Agent..." or when the enhanced /api/* endpoints are missing.

## Architecture

```
Browser → port 3001 (Hermes Workspace / Vite)
                ↓ HTTP
          port 8642 (Hermes gateway API server)
                ↓
          Hermes Agent (Python)
```

The workspace lives at: /root/.openclaw/workspace/hermes-workspace/
The gateway source lives at: /root/.hermes/hermes-agent/
Config: /root/.hermes/.env

## Two-Tier Capability Model

The workspace probes these endpoints at startup:

- Core:     /health, /v1/models, /v1/chat/completions
- Enhanced: /api/sessions, /api/skills, /api/memory, /api/config, /api/jobs

If only core is available, the workspace falls back to "portable" OpenAI-compat mode.
If enhanced is available, it runs in "enhanced-hermes" mode with full session/memory/skills UI.

## Step 1 — Enable the API Server

The gateway's HTTP API is OFF by default. Enable it by adding to /root/.hermes/.env:

```
API_SERVER_ENABLED=true
API_SERVER_HOST=0.0.0.0
API_SERVER_PORT=8642
```

Then restart the gateway:
```bash
/root/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main gateway restart
```

Verify:
```bash
curl -s http://127.0.0.1:8642/health
# Should return: {"status": "ok", "platform": "hermes-agent"}
```

## Step 2 — Check Which Fork is Installed

CRITICAL PITFALL: The NousResearch/hermes-agent main branch is MISSING the enhanced
/api/sessions, /api/skills, /api/memory, /api/config endpoints. These only exist in
the outsourc-e/hermes-agent fork.

Check which endpoints respond:
```bash
for ep in /health /v1/models /api/sessions /api/skills /api/memory /api/config /api/jobs; do
  echo "$ep -> $(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8642$ep)"
done
```

Expected with outsourc-e fork:
  /health      -> 200
  /v1/models   -> 200
  /api/sessions -> 200
  /api/skills  -> 200
  /api/memory  -> 200
  /api/config  -> 200
  /api/jobs    -> 200 or 500 (exists but may have internal error — not 404)

If /api/sessions returns 404, you have the NousResearch main branch. Fix: replace api_server.py.

## Step 3 — Replace api_server.py with outsourc-e Fork

```bash
cd /root/.hermes/hermes-agent

# Add outsourc-e remote if not already present
git remote add outsourc-e https://github.com/outsourc-e/hermes-agent.git 2>/dev/null || true
git fetch outsourc-e

# Back up and replace
cp gateway/platforms/api_server.py gateway/platforms/api_server.py.bak
git show outsourc-e/main:gateway/platforms/api_server.py > gateway/platforms/api_server.py

# Restart gateway
/root/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main gateway restart
```

Wait ~5 seconds then re-run the endpoint check above.

## Workspace .env

The workspace reads its own .env at:
  /root/.openclaw/workspace/hermes-workspace/.env

It must contain:
```
HERMES_API_URL=http://127.0.0.1:8642
```

If it's pointing at a different port or host, update it and restart the workspace process.

## Restarting the Workspace Frontend

The Vite dev server (port 3001) is run as a background process. Find and restart it:

```bash
# Find the PID
ps aux | grep "vite.*port 3000\|hermes-workspace" | grep -v grep

# Kill and relaunch
pkill -f "vite.*hermes-workspace" 2>/dev/null
cd /root/.openclaw/workspace/hermes-workspace
PORT=3001 pnpm dev > /tmp/hermes-workspace.log 2>&1 &
```

Note: The process may have been started with PORT=3003 internally but mapped to 3001
via network config — check the actual command in ps aux.

## Common Issues

### "Connecting to Hermes Agent..." won't go away
- Check port 8642 is actually listening: `ss -tlnp | grep 8642`
- If nothing listening: API_SERVER_ENABLED not set, or gateway not restarted after adding it
- If listening but 404 on /api/sessions: NousResearch main branch, need outsourc-e api_server.py

### venv has no pip binary
The hermes-agent venv doesn't install pip as a script. Use:
```bash
/root/.hermes/hermes-agent/venv/bin/python -m pip install PACKAGE
```

### Cannot merge outsourc-e/main (conflict in api_server.py)
Do NOT attempt git merge — the two branches have diverged significantly.
Just replace the single file directly as shown in Step 3. The rest of the codebase
stays on NousResearch main. This is safe because api_server.py is self-contained.

### /api/jobs returns 500
This is a known internal error in the jobs endpoint — it does NOT mean the endpoint
is missing. The workspace treats any non-404 response as "endpoint exists." Ignore it
unless you're actively using the Jobs UI.

### Dashboard shows old data / Welcome modal keeps appearing
The welcome modal is a first-time onboarding overlay stored in browser localStorage.
It will stop appearing once you click "Skip setup" or "Get Started".
The sidebar loads sessions from /api/sessions in real time — if sessions appear there,
the backend is connected regardless of what the modal says.

## Verification Checklist

1. `curl http://127.0.0.1:8642/health` → 200 with {"status":"ok"}
2. `curl http://127.0.0.1:8642/api/sessions` → 200 (not 404)
3. `curl http://127.0.0.1:8642/api/config` → 200 with model info
4. Browser at http://SERVER:3001/dashboard → sidebar shows sessions from today
5. Dashboard "Model" card shows current model (e.g. anthropic/claude-sonnet-4.6)
