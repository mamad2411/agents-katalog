---

name: openclaw-platform-management
description: OpenClaw platform operations — access/troubleshooting, subagent creation, and Docker migration on Charles's Hostinger server. Covers gateway ports, config management, Docker exec patterns, and agent registration.
category: openclaw

---
**Manage, access, and troubleshoot the OpenClaw platform on Charles's Hostinger server.**

## What This Skill Does

This skill OpenClaw platform operations — access/troubleshooting, subagent creation, and Docker migration on Charles's Hostinger server. Covers gateway ports, config management, Docker exec patterns, and agent registration.

## Umbrella Sections

- **[§1 Access & Troubleshooting](#section-1-access--troubleshooting)** — Gateway ports, config paths, Docker exec, TUI access, model fallback, duplicate Telegram replies
- **[§2 Agent Creation](#section-2-agent-creation)** — Create new named subagents with full file structure and openclaw.json registration
- **[§3 Docker Migration](#section-3-docker-migration)** — Migrate OpenClaw from one Docker setup to another

**New — Error Pattern Reference:**
- `references/version-mismatch-err-module.md` — Full diagnosis and fix for ERR_MODULE_NOT_FOUND caused by `lastTouchedVersion` / installed package version mismatch (May 14 2026)

---

## §1 Access & Troubleshooting

**Gateway ports, config paths, Docker exec patterns, TUI access, model fallback configuration, and common issues.**

> **Non-Fatal Telegram Errors (Known False Positives):** The following errors appear in logs but messages still go through. Do NOT restart the container or declare bots down when you see these:
> - `ERR_MODULE_NOT_FOUND: cleanup-kBh9Q3mQ.js` — Non-fatal; Telegram sendMessage still succeeds.
> - `heartbeat failed` with same module error — Non-fatal; heartbeat fails on schedule but system keeps running.
> - **Verification:** Check `ls -la /root/.openclaw/.openclaw/telegram/update-offset-*.json` for recent timestamps, or `docker exec openclaw-mm3f-openclaw-1 ps aux | grep node` to confirm two node processes (server.mjs + openclaw) are running.

### Trigger
Use whenever `openclaw` commands fail with "command not found" or when you need to interact with a running OpenClaw instance.

### 1. Determine If OpenClaw Is Running Inside Docker

**CRITICAL — Gateway ONLY runs in Docker:**
There is NO host-level `openclaw` binary on this VPS. All commands require `docker exec openclaw-mm3f-openclaw-1`. When container stops, gateway is DOWN.

Restart:
```bash
cd /docker/openclaw-mm3f && docker compose up -d && sleep 10
ss -tlnp | grep 18789
```

```bash
docker ps --format '{{.Names}}\t{{.Image}}\t{{.Status}}' | grep -i openclaw
```

If you see a running container (e.g., `openclaw-mm3f-openclaw-1` using `ghcr.io/hostinger/hvps-openclaw:latest`), **ALL subsequent commands must use `docker exec`**.

**Docker setup layout (Hostinger HVPS pattern):**
- Compose file: `/docker/openclaw-mm3f/docker-compose.yml`
- Volumes: `./data:/data`, `./data/linuxbrew:/home/linuxbrew`
- Container working directory: `/data`
- OpenClaw binary inside container: `/data/.npm-global/bin/openclaw`

**Inside the container (use `docker exec <container> <command>`):**
```bash
docker exec openclaw-mm3f-openclaw-1 /data/.npm-global/bin/openclaw --version
# Expected: OpenClaw 2026.5.12 (f066dd2)

# TUI inside container:
docker exec -it openclaw-mm3f-openclaw-1 /data/.npm-global/bin/openclaw tui

# Gateway logs inside container:
docker exec openclaw-mm3f-openclaw-1 cat /tmp/gateway.log

# Processes inside container:
docker exec openclaw-mm3f-openclaw-1 ps aux | grep openclaw
```

**If NOT in Docker** (bare metal or VM install), the CLI may be installed but not in `$PATH`. Common locations:

```bash
which openclaw 2>/dev/null                    # Check PATH first
find / -name 'openclaw' -type f -executable 2>/dev/null | head -5
ls /data/linuxbrew/.linuxbrew/bin/openclaw 2>/dev/null  # linuxbrew install
npm list -g openclaw 2>/dev/null                           # npm global install
```

If found, add to PATH:
```bash
export PATH="/data/linuxbrew/.linuxbrew/bin:$PATH"
```

**Node version requirement:** OpenClaw 2026.4.x requires Node.js v22.12+. If system Node is older (v20), you MUST use the Docker container or linuxbrew Node — system Node will fail with "Node.js v22+ is required".

### 2. Verify OpenClaw Is Running

```bash
ps aux | grep openclaw | grep -v grep
```

Typical processes:
- `openclaw` - main process
- `openclaw-tui` - terminal UI
- `openclaw-gateway` - HTTP gateway service
- `node ... vite.js dev` - web UI dev server

### 3. Find the Config File

**Docker:** inside the container, config is at `/data/.openclaw/openclaw.json`
**Host:** two possible locations:
```bash
ls -la ~/.openclaw/openclaw.json               # Primary config
ls -la ~/.openclaw/.openclaw/openclaw.json     # Internal config (backup/symlink)
readlink -f ~/.openclaw/openclaw.json          # Resolve symlinks
```

**IMPORTANT:** The config may reference `/data/.openclaw/` but the actual path is `/root/.openclaw/`. Always verify with `ls`.

### 4. Gateway Ports

The gateway exposes multiple ports. Check which are active:

```bash
ss -tlnp | grep -E '18789|18791|34343|3000|3001'
```

| Port | Purpose | Auth Required |
|------|---------|---------------|
| 18789 | Web UI + health endpoint | No (health: `/health` returns `{"ok": true, "status": "live"}`) |
| 18791 | Authenticated API (v1/chat/completions) | Yes (Bearer token) |
| 34343 | WebSocket/internal | Varies |
| 3000 | OpenClaw Studio (Next.js) | No |
| 3001 | Hot reload / dev | No |

### 5. Get the Hooks Auth Token

```bash
python3 -c "import json; c=json.load(open('/root/.openclaw/openclaw.json')); print(c.get('hooks',{}).get('token','not found'))"
```

Use it for authenticated API calls:
```bash
curl -s http://localhost:18791/v1/chat/completions \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"model":"model-id","messages":[{"role":"user","content":"test"}]}'
```

### 6. Test Gateway Health

```bash
curl -s http://localhost:18789/health
# Expected: {"ok": true, "status": "live"}
```

### 7. Send Messages via Gateway (fallback method)

When CLI is unavailable, try these API endpoints:

```bash
curl -s http://localhost:18789/api/agent/send \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"agentId":"main","channel":"telegram","accountId":"default","text":"ping","from":"test"}'
```

Common endpoints:
- `/api/agent/send` - send message
- `/hooks/telegram` - webhook for Telegram updates
- `/health` - health check

### 8. Check Logs

**Docker:**
```bash
docker exec <container> cat /tmp/gateway.log | grep -i -E "fallback|model|error|fail|qwen|opus|rate" | tail -30
```

**Host:**
```bash
cat /tmp/gateway.log 2>/dev/null              # Gateway output
ls ~/.openclaw/.openclaw/logs/ 2>/dev/null    # Log directory
cat ~/.openclaw/.openclaw/logs/gateway-startup.log 2>/dev/null
```

### 9. Verify Config JSON Is Valid

```bash
python3 -c "import json; json.load(open('/root/.openclaw/openclaw.json')); print('Config OK')"
```

### 10. Agent-Level Model Overrides Shadow Defaults

**CRITICAL:** When you change `agents.defaults.model.fallbacks`, each agent that has its own `"model"` key will NOT see the new fallbacks. The per-agent `model` field overrides the defaults entirely — including fallbacks.

**Check which agents have overrides:**
```bash
docker exec <container> python3 -c "
import json
with open('/data/.openclaw/openclaw.json') as f:
    c = json.load(f)
for a in c['agents']['list']:
    mid = a.get('model', '<defaults>')
    print(f\"{a['id']}: {mid}\")"
```

**Remove agent-level overrides so agents use defaults:**
```python
import json
with open('/data/.openclaw/openclaw.json', 'r') as f:
    config = json.load(f)
for a in config['agents']['list']:
    if 'model' in a and a['id'] not in ('main', 'rei-reporter'):
        del a['model']
with open('/data/.openclaw/openclaw.json', 'w') as f:
    json.dump(config, f, indent=2)
```

**The gateway will hot-reload automatically** — check the logs within 3 seconds:
```bash
docker exec <container> grep 'reload' /tmp/gateway.log | tail -5
```

Expected log entries:
```
[reload] config change detected; evaluating reload (agents.list)
[reload] config hot reload applied (agents.list)
```

**Current recommended model chain (set in defaults):**
```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "kilocode/qwen/qwen3.6-plus:free",
        "fallbacks": [
          "openrouter/anthropic/claude-sonnet-4-6",
          "openrouter/qwen/qwen3.6-plus:free"
        ]
      }
    }
  }
}
```

This gives a 3-tier chain:
1. Primary: free Qwen (kilocode provider)
2. Fallback 1: Claude Sonnet 4.6 via OpenRouter (smart, cheaper than Opus)
3. Fallback 2: Same Qwen model but via OpenRouter (bypasses kilocode rate limits)

### 11. Fix Duplicate Telegram Replies

**Symptom:** Every message gets two replies from the same Telegram bot.

**Cause 1 — dmPolicy: pairing (most common):**
The `pairing` policy creates duplicate session handling. Fix:
```python
import json
with open('/data/.openclaw/openclaw.json', 'r') as f:
    c = json.load(f)
c['channels']['telegram']['dmPolicy'] = 'allowlist'
with open('/data/.openclaw/openclaw.json', 'w') as f:
    json.dump(c, f, indent=2)
```
The gateway hot-reloads automatically.

**Cause 2 — zombie gateway processes:**
When gateway restarts fail, duplicate processes can run. Check:
```bash
docker exec <container> pgrep -f openclaw-gateway
# If multiple PIDs returned, kill extras:
docker exec <container> kill <extra_pid>
```
Log evidence: `"gateway already running (pid XXXX); lock timeout"` and `"Port 18789 is already in use"`

**Cause 3 — duplicate Telegram account entries:**
Check if the same bot token appears in multiple account configs. Each active account creates a separate listener.

### 12. Fix TUI Showing Stale Model/ModelOverride

**Symptom:** TUI shows the wrong model (e.g., `gemma-4-31b-it`) even after changing config and confirming gateway hot-reload.

**Cause:** OpenClaw stores `model` and `modelOverride` at the **session level** in `sessions.json`. The TUI reads the session's active model, not the config defaults. When a fallback kicks in, it overwrites the session's model field.

**Fix:**
```python
import json
path = '/data/.openclaw/agents/main/sessions/sessions.json'
with open(path) as f:
    d = json.load(f)
for key, val in d.items():
    if isinstance(val, dict):
        for k in ('model', 'modelOverride', 'fallbackNoticeActiveModel'):
            val.pop(k, None)
with open(path, 'w') as f:
    json.dump(d, f, indent=2)
```
Then reconnect the TUI — it will pick up config defaults on fresh WebSocket connection.

### 13. Execute Python Scripts in Docker Without Quoting Hell

Writing inline Python via `docker exec sh -c 'python3 -c "..."'` causes shell quoting nightmares. Use this pattern instead:

```bash
# Step 1: Write the script on the host
cat > /tmp/fix_something.py << 'EOF'
import json
# your code here
EOF

# Step 2: Copy into container and run
docker cp /tmp/fix_something.py <container>:/tmp/fix_something.py
docker exec <container> python3 /tmp/fix_something.py

# Step 3: Clean up (optional)
rm /tmp/fix_something.py
docker exec <container> rm /tmp/fix_something.py
```

### 14. ERR_MODULE_NOT_FOUND — Version Mismatch Root Cause

**Symptom:** Logs show continuous `Cannot find module '/data/.npm-global/lib/node_modules/openclaw/dist/cleanup-*.js'` and `task-registry.maintenance-*.js` errors. Health endpoint returns `200 {"ok":true,"status":"live"}` but WebSocket requests fail with `UNAVAILABLE`. External port (e.g., 49248) returns `000`.

**Root Cause:** The running OpenClaw gateway was on an **older config version** (e.g., 2026.5.5) while the **installed npm package** is newer (2026.5.7). OpenClaw's bundled JS chunks use content-hashed filenames that change between versions. When the config's `lastTouchedVersion` doesn't match the installed package version, the gateway tries to load chunks with old hash suffixes that no longer exist.

**Diagnosis steps:**
```bash
# Check installed npm package version
docker exec openclaw-mm3f-openclaw-1 npm list -g openclaw

# Check what version the config thinks is running
docker exec openclaw-mm3f-openclaw-1 cat /data/.openclaw/openclaw.json | python3 -c "
import json,sys; d=json.load(sys.stdin); print(d.get('meta',{}))"

# List actual dist files — note the hash suffixes present
docker exec openclaw-mm3f-openclaw-1 ls /data/.npm-global/lib/node_modules/openclaw/dist/ | grep -E "cleanup|task-registry|managed-image"

# Compare: error log shows hash like DuW0FRWY but actual file is DxA2A4eM
# If they don't match → version mismatch
```

**Fix (two-step):**
1. Restart the container to force a re-sync between the running process and installed package:
   ```bash
   cd /docker/openclaw-mm3f && docker compose restart openclaw
   ```
2. Update `lastTouchedVersion` in openclaw.json to match the installed package version:
   ```bash
   docker exec openclaw-mm3f-openclaw-1 sed -i 's/"lastTouchedVersion": "OLDVERSION"/"lastTouchedVersion": "NEWVERSION"/' /data/.openclaw/openclaw.json
   ```

**Verification:**
```bash
# External port should now return 200
curl -s -o /dev/null -w "%{http_code}" "http://$CHARLES_HOST_IP:49248/"

# Health endpoint should still be 200
curl -s http://127.0.0.1:18789/health

# Logs should show clean startup with new version
docker logs openclaw-mm3f-openclaw-1 --tail 20
```

> **Note:** `lastTouchedVersion` in openclaw.json tracks the **config schema version**, not the OpenClaw application version. It must match the installed `openclaw` npm package version for the gateway to load the correct JS chunk hashes. This is an internal OpenClaw state tracking mechanism — updating it aligns the config with reality.

### Common Issues

1. **Gateway log says "nohup: failed to run command"** — gateway started before PATH was set. If process is running (check `ps`), it's fine.
2. **404 on API endpoints** — endpoint paths change between versions. Try different paths or check the web UI at port 18789.
3. **401 Unauthorized on port 18791** — need Bearer token from hooks.token in config.
4. **Can't attach TUI** — another session already has it. Check `ps aux | grep openclaw-tui`.
5. **Config references /data/ but that doesn't exist** — use `/root/.openclaw/` instead.
6. **OpenClaw 2026.4.x requires Node.js v22.12+** — system Node v20 will fail. Use Docker container's Node or linuxbrew Node.
7. **Hot-reload does not propagate to already-connected TUI sessions** — reconnect the TUI after config changes.
8. **ERR_MODULE_NOT_FOUND on cleanup-*.js / task-registry.maintenance-*.js** — version mismatch; see §1.14 above.

---

## §2 Agent Creation

**Create a new OpenClaw subagent workspace with full file structure and openclaw.json registration.**

### Trigger
Use when Charles wants to add a new named AI agent to his team.

### Step 1: Check Existing State

**Check if the agent is already registered in openclaw.json:**
```bash
python3 -c "
import json
with open('/root/.openclaw/.openclaw/openclaw.json') as f:
    config = json.load(f)
agents = config.get('agents', {}).get('list', [])
matches = [a for a in agents if a['id'] == '<agent-id>']
print(json.dumps(matches, indent=2))
"
```

**Check if workspace directory exists:**
```bash
ls -la /root/.openclaw/workspace/agents/<agent-id>/ 2>/dev/null || echo "Directory does not exist"
```

**Check existing agents for reference:**
```bash
ls /root/.openclaw/workspace/agents/
```

### Step 2: Create Workspace Directory Structure

```bash
mkdir -p /root/.openclaw/workspace/agents/<agent-id>/{memory,scripts,data/.learnings,logs}
touch /root/.openclaw/workspace/agents/<agent-id>/.openclaw/config.json
```

### Step 3: Create Required Files

Every agent needs these files (model after existing agents like Bob or Mark):

| File | Purpose |
|------|---------|
| `IDENTITY.md` | Name, role, specialty, emoji |
| `AGENTS.md` | System rules, capabilities, workflows, tools, guardrails, delivery protocol |
| `SOUL.md` | Personality, voice, workflow philosophy, signature move |
| `TOOLS.md` | Toolkit description, command patterns, evaluation frameworks |
| `USER.md` | What the agent knows about Charles, his businesses, expectations |
| `QUICK_START.md` | First-run guide for the agent |
| `HEARTBEAT.md` | Status tracker |
| `README.md` | Full overview for humans |

### Step 4: Register in openclaw.json (if not already there)

The agent entry goes in `agents.list`:

```json
{
  "id": "<agent-id>",
  "name": "<Agent Name>",
  "workspace": "/root/.openclaw/workspace/agents/<agent-id>",
  "model": "openrouter/anthropic/claude-sonnet-4-5"
}
```

**CRITICAL PATH NOTE:** Existing configs may show `/data/.openclaw/workspace/agents/<agent-id>` as the workspace path, but the actual filesystem uses `/root/.openclaw/workspace/agents/<agent-id>`. `/data` does not exist on this machine. If the config references `/data/`, update it or create a symlink:

```bash
ln -sf /root/.openclaw /data/.openclaw 2>/dev/null
```

### Step 5: Add Telegram Account (if needed)

In `channels.telegram.accounts`:

```json
"<agent-id>": {
  "enabled": true,
  "dmPolicy": "allowlist",
  "botToken": "<bot-token>",
  "allowFrom": ["<user-telegram-id>"],
  "groupPolicy": "disabled",
  "streaming": "partial"
}
```

### Step 6: Add Binding

In `bindings`:

```json
{
  "agentId": "<agent-id>",
  "match": {
    "channel": "telegram",
    "accountId": "<agent-id>"
  }
}
```

### Step 7: Add Spawn Allowlist (optional)

If the main agent should be able to spawn this new agent, add it to the main agent's `subagents.allowAgents`:

```json
"subagents": {
  "allowAgents": ["main", "mark", "eric", "michael", "bob", "<agent-id>"]
}
```

### Step 8: Verify

```bash
# Verify directory exists
ls -la /root/.openclaw/workspace/agents/<agent-id>/

# Verify config is valid JSON
python3 -c "import json; json.load(open('/root/.openclaw/.openclaw/openclaw.json')); print('Config OK')"

# Verify all required files exist
for f in IDENTITY.md AGENTS.md SOUL.md TOOLS.md USER.md QUICK_START.md HEARTBEAT.md README.md; do
  [ -f "/root/.openclaw/workspace/agents/<agent-id>/$f" ] || echo "MISSING: $f"
done
```

### Existing Agents Reference
- **bob** 🏘️ — Property Intelligence & Outreach
- **eric** 🎬 — Video Creation & Social Media
- **mark** 🎨 — Design & Graphics
- **michael** 🎨 — REI Content & Community Events
- **tammie** 👩‍💼 — HR & Hiring Automation

### Pitfalls
- **Path mismatch:** Config may reference `/data/.openclaw/` but the real path is `/root/.openclaw/`. Always verify with `ls`.
- **OpenClaw CLI not in PATH:** Even when OpenClaw processes are running, the `openclaw` CLI binary may NOT be in `$PATH`. Test with `which openclaw` first.
- **TUI already running:** If another session has `openclaw tui` attached, you can't launch a second instance. Use the gateway HTTP API on port 18789 instead.
- **Agent already registered but no workspace:** Create the directory without modifying config.
- **Don't copy API keys between agents:** Each agent may need its own credentials.
- **Gateway API auth:** Get the hooks token from `openclaw.json` (`hooks.token`).

---

## §3 Docker Migration

**Migrate OpenClaw from one Docker setup to another — preserve data, agents, and configuration.**

### Trigger
Use when moving OpenClaw between Docker environments, or when rebuilding the OpenClaw container.

### Migration Workflow

1. **Backup existing data:**
   ```bash
   # Backup the data volume
   docker run --rm -v openclaw-mm3f_data:/data -v $(pwd):/backup alpine tar czf /backup/openclaw-backup.tar.gz -C /data .
   ```

2. **Stop the source container:**
   ```bash
   docker compose -f /docker/openclaw-mm3f/docker-compose.yml down
   ```

3. **Transfer to new environment:**
   ```bash
   # Copy backup to new server
   scp openclaw-backup.tar.gz new-server:/path/to/backup/
   ```

4. **Restore on new server:**
   ```bash
   # Create new data volume
   docker volume create new_openclaw_data
   
   # Restore data
   docker run --rm -v new_openclaw_data:/data -v $(pwd):/backup alpine tar xzf /backup/openclaw-backup.tar.gz -C /data
   
   # Update docker-compose.yml with new volume name
   # volumes: ./data:/data → volumes: new_openclaw_data:/data
   ```

5. **Start on new server:**
   ```bash
   docker compose -f /docker/openclaw-mm3f/docker-compose.yml up -d
   ```

### Key Files to Preserve
- `/data/.openclaw/openclaw.json` — main config
- `/data/.openclaw/agents/` — agent workspaces
- `/data/linuxbrew/` — Node.js installation (if using linuxbrew Node)
- `/data/.openclaw/sessions/` — session data

### Common Migration Issues
- **Path references:** After migration, verify `/data/.openclaw/` paths match the new environment
- **Node version:** Ensure new environment has Node.js v22.12+ or uses the linuxbrew Node
- **Volume permissions:** If container runs as non-root UID, `chown` the restored data volume
