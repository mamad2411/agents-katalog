---

name: openclaw-access-troubleshooting
description: How to find, access, and interact with OpenClaw when the CLI binary isn't in PATH. Covers gateway API, config paths, ports, and alternative interaction methods.

---
Use this when `openclaw` commands fail with "command not found" or when you need to interact with a running OpenClaw instance without the CLI.

## What This Skill Does

This skill How to find, access, and interact with OpenClaw when the CLI binary isn't in PATH. Covers gateway API, config paths, ports, and alternative interaction methods.

## 1. Determine If OpenClaw Is Running Inside Docker

**CRITICAL FIRST CHECK** — The gateway ONLY runs inside the Docker container on this VPS. There is NO host-level `openclaw` binary. `which openclaw` always fails.

When container is stopped: gateway DOWN, no fallback. Restart with:
```bash
cd /docker/openclaw-mm3f && docker compose up -d && sleep 10
```

```bash
docker ps --format '{{.Names}}\t{{.Image}}\t{{.Status}}' | grep -i openclaw
```

If you see a running container (e.g., `openclaw-mm3f-openclaw-1` using `ghcr.io/hostinger/hvps-openclaw:latest`), **ALL subsequent commands must use `docker exec`**.

**Docker setup layout** (Hostinger HVPS pattern):
- Compose file: `/docker/openclaw-mm3f/docker-compose.yml`
- Volumes: `./data:/data`, `./data/linuxbrew:/home/linuxbrew`
- Container working directory: `/data`
- OpenClaw binary inside container: `/data/.npm-global/bin/openclaw`

**IMPORTANT: DUAL INSTALL PATTERN — Host-level AND Docker can both run simultaneously.** When the host-level OpenClaw starts its own gateway on the same port (18789), the Docker container's gateway crashes with `EADDRINUSE`. This is **expected and benign** — the host-level installation is the primary; the Docker container is redundant when a host-level gateway exists.

**How to tell which is primary:**
```bash
lsof -i :18789
# If openclaw (PID on host) owns port 18789 → host-level is primary
# If container's openclaw-gateway crashed → host-level won the port
```

**Inside the container (use `docker exec <container> <command>`):**
```bash
# Version check
docker exec openclaw-mm3f-openclaw-1 /data/.npm-global/bin/openclaw --version
# Expected: OpenClaw 2026.5.12 (f066dd2)

# TUI — gateway must be running in the SAME container:
docker exec -it openclaw-mm3f-openclaw-1 /data/.npm-global/bin/openclaw tui

# Gateway health (from host):
curl -s http://127.0.0.1:18789/health
# Expected: {"ok":true,"status":"live"}
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

## 1b. Test the OpenClaw TUI and Fallback (Docker)

To test the TUI and verify model fallback is working:

```bash
docker exec -it openclaw-mm3f-openclaw-1 /data/.npm-global/bin/openclaw tui
```

**To check fallback status WITHOUT using TUI** (read gateway logs):

```bash
docker exec <container> grep -i 'model-fallback\|failover' /tmp/gateway.log | tail -30
```

**Fallback log entry format:**
```
[agent] embedded run failover decision: runId=xxx decision=fallback_model reason=rate_limit provider=kilocode/qwen/qwen3.6-plus:free
[model-fallback] model fallback decision: decision=candidate_succeeded requested=kilocode/qwen/qwen3.6-plus:free candidate=openrouter/google/gemma-4-31b-it
```

Key patterns to look for:
- `decision=candidate_succeeded` — fallback worked
- `decision=candidate_failed` — failed over but next candidate exists
- `decision=none_fallback_model` — all candidates exhausted (system failure)
- `reason=rate_limit` — API rate limiting
- `reason=auth` — missing API key
- `reason=timeout` — request timed out

## 2. Verify OpenClaw Is Running

```bash
ps aux | grep openclaw | grep -v grep
```

Typical processes:
- `openclaw` - main process
- `openclaw-tui` - terminal UI
- `openclaw-gateway` - HTTP gateway service
- `node ... vite.js dev` - web UI dev server

## 3. Find the Config File

**Docker:** inside the container, config is at `/data/.openclaw/openclaw.json`
**Host:** two possible locations:
```bash
ls -la ~/.openclaw/openclaw.json               # Primary config
ls -la ~/.openclaw/.openclaw/openclaw.json     # Internal config (backup/symlink)
readlink -f ~/.openclaw/openclaw.json          # Resolve symlinks
```

**IMPORTANT:** The config may reference `/data/.openclaw/` but the actual path is `/root/.openclaw/`. Always verify with `ls`.

## 4. Gateway Ports

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

## 5. Get the Hooks Auth Token

```bash
python3 -c "import json; c=json.load(open('/root/.openclaw/openclaw.json')); print(c.get('hooks',{}).get('token','not found'))"
```

Use it for authenticated API calls:
```bash
curl -s http://localhost:18791/v1/chat/completions \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_HOOKS_TOKEN" \
  -d '{"model":"model-id","messages":[{"role":"user","content":"test"}]}'
```

## 6. Test Gateway Health

```bash
curl -s http://localhost:18789/health
# Expected: {"ok": true, "status": "live"}
```

## 7. Send Messages via Gateway (fallback method)

When CLI is unavailable, try these API endpoints:

```bash
curl -s http://localhost:18789/api/agent/send \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_HOOKS_TOKEN" \
  -d '{"agentId":"main","channel":"telegram","accountId":"default","text":"ping","from":"test"}'
```

Note: API endpoint paths may vary by OpenClaw version. Common endpoints:
- `/api/agent/send` - send message
- `/hooks/telegram` - webhook for Telegram updates
- `/health` - health check

## 8. Check Logs

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

## 9. Verify Config JSON Is Valid

```bash
python3 -c "import json; json.load(open('/root/.openclaw/openclaw.json')); print('Config OK')"
```

## 10. Agent-Level Model Overrides Shadow Defaults

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

Expected log entry:
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

## 11. Fix Duplicate Telegram Replies

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

## 12. Fix TUI Showing Stale Model/ModelOverride

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

## 13. Non-Fatal Telegram Dispatch Errors (Known False Positives)

These errors appear in logs but messages still go through. Do NOT treat them as bot-down indicators.

**Error 1 — ERR_MODULE_NOT_FOUND: cleanup-*.js**
```
[telegram] dispatch failed: Error [ERR_MODULE_NOT_FOUND]: Cannot find module '/data/.openclaw/plugin-runtime-deps/openclaw-2026.4.29-c27ae31043c7/dist/cleanup-kBh9Q3mQ.js' imported from /data/.openclaw/plugin-runtime-deps/openclaw-2026.4.29-c27ae31043c7/dist/store-CX_a-msa.js
```
**Verdict:** Non-fatal. Messages still sent/received (`[telegram] sendMessage ok`). The plugin runtime dependency path is stale but the Telegram dispatch recovers.

**Error 2 — heartbeat failed (same module error)**
```
[heartbeat] failed: Cannot find module '/data/.npm-global/lib/node_modules/openclaw/dist/cleanup-kBh9Q3mQ.js' imported from /data/.npm-global/lib/node_modules/openclaw/dist/store-CX_a-msa.js
```
**Verdict:** Non-fatal. Caused by the same stale plugin-runtime-deps path. Heartbeat continues to fail on schedule but the system keeps running.

**How to verify the bots are actually up:**
```bash
# Check update-offset files — active bots will have recent timestamps
ls -la /root/.openclaw/.openclaw/telegram/update-offset-*.json

# Or check the process list inside the container
docker exec openclaw-mm3f-openclaw-1 ps aux | grep node | grep -v grep
# You should see: node server.mjs + openclaw (two separate node processes)
```

**Do NOT restart the container for these errors.** The Telegram bots are polling normally.

---

## 14. Execute Python Scripts in Docker Without Quoting Hell

Writing inline Python via `docker exec sh -c 'python3 -c "..."` causes shell quoting nightmares. Use this pattern instead:

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

> **Support files:** `references/openclaw-may15-2026-session.md` — May 15 2026 session (CORRECTED architecture: container-only, no host binary; "protocol mismatch" root cause = gateway offline, not dual-install conflict). `references/openclaw-nonfatal-errors.md` — full error transcripts and health check template.
> 
> ⚠️ `references/openclaw-dual-install-pattern.md` is OUTDATED — it describes a false dual-install theory that was disproved May 15. The gateway runs ONLY in Docker; there is no host-level openclaw binary.

## Common Issues

1. **Gateway log says "nohup: failed to run command"** — gateway started before PATH was set. If process is running (check `ps`), it's fine.
2. **404 on API endpoints** — endpoint paths change between versions. Try different paths or check the web UI at port 18789.
3. **401 Unauthorized on port 18791** — need Bearer token from hooks.token in config.
4. **Can't attach TUI** — another session already has it. Check `ps aux | grep openclaw-tui`.
5. **Config references /data/ but that doesn't exist** — use `/root/.openclaw/` instead.
6. **OpenClaw 2026.4.x requires Node.js v22.12+** — system Node v20 will fail. Use Docker container's Node or linuxbrew Node.
7. **Hot-reload does not propagate to already-connected TUI sessions** — reconnect the TUI after config changes.