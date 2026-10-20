---

name: self-hosted-communication-server
description: Set up, configure, and maintain self-hosted Discord-compatible chat platforms (Spacebar, Revolt, etc.) for AI agent teams — fork-first, patch-friendly, Docker-free when needed.
version: 2.6.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [self-hosted, spacebar, revolt, matrix, chat-platform]
    triggers:
      - self-hosted discord alternative
      - spacebarchat setup
      - revoltchat server
      - matrix synapse dendrite
      - self-hosted communication
    related_skills: [gateway-architecture-analysis, gateway-troubleshooting]

---
# Self-Hosted Communication Server

Workflow for setting up a self-hosted Discord-compatible chat server for AI agent/team communication.

## General Approach

1. **Choose your platform**
   - [Spacebar](https://github.com/spacebarchat/server) — Most Discord-compatible backend (fork of Fosscord). Node.js/TypeScript, PostgreSQL.
   - [Revolt](https://github.com/revoltchat) — Rust backend, MongoDB. Less Discord-API compatible.
   - [Matrix (Synapse/Dendrite)](https://matrix.org) — Most mature self-hosted protocol, but not Discord-API compatible.

2. **Fork first** — always fork to your GitHub account before cloning. This enables:
   - Custom patches that persist across upstream updates
   - Config defaults tailored to your infra
   - CI/CD for your deployment

3. **Dependencies** (varies by platform):
   - Node.js 22+ (for Spacebar)
   - PostgreSQL 16+ (for Spacebar)
   - Python 3.13+ (for Spacebar schema generation)
   - Build tools (gcc/g++ on Linux, VS Build Tools on Windows)

4. **Database setup** — create a dedicated user + database before starting the app

5. **Configuration** — Let the server generate its initial config, then edit it

6. **Registration UX** — Many self-hosted platforms have strict defaults. When setting up for dev/AI agent use, relax:
   - Disable captcha
   - Disable email verification
   - Disable DOB requirement
   - Relax password requirements

7. **Patching** — Expect gaps in Discord API compatibility. Common fixes:
   - Login endpoint may only support email/phone (not username) — patch the ORM query
   - Registration may not set JWT secret properly — generate one in config
   - Missing API routes may need stubs

## Spacebar-Specific Steps

> **🔗 Operational runbooks** — For Docker Desktop recovery (WSL2 wedge, named-pipe failures), Windows cron health checks, hybrid Docker+Native deployment, and the full health check runbook, see the **`spacebar-deployment`** skill. The umbrella skill covers setup/architecture; the deployment skill covers runtime operations.

See `references/spacebar-windows-setup.md` for the full session detail.

Quick start (after fork + clone):
```bash
npm install
npm run build:tsgo
export CONFIG_PATH=config.json
export DATABASE='postgres://user:***@127.0.0.1/spacebar'
npm run start
```

### Config fields that must be set (bundle mode):
```jsonc
{
  "general": { "serverName": "localhost:3001" },
  "api": { "endpointPublic": "http://localhost:3001/api/v9" },
  "cdn": { "endpointPublic": "http://localhost:3001", "endpointPrivate": "http://localhost:3001" },
  "gateway": { "endpointPublic": "ws://localhost:3001/" }
}
```

### ⏱️ Spacebar startup timing (native mode)

Spacebar registers ALL API routes at startup before beginning to listen. This takes **~45-60 seconds**. During this time the process logs hundreds of `[Server] Route ... registered` lines — this is normal, NOT a hang. After ~45s the port opens (`netstat` shows LISTENING); after ~60s the API responds to `curl /api/v9/gateway`. Kill stale Node processes holding the port before restarting.

**🚨 Pitfall: CDN endpoint must NOT have trailing slash.** If `endpointPrivate` ends with `/` and the internal upload path (e.g. `/avatars/user_id`) starts with `/`, concatenation produces `//avatars/user_id` — a double-slash path that Express does NOT route. The internal POST returns 404. Remove trailing slashes from BOTH `endpointPrivate` and `endpointPublic`.

## CDN Route Registration in Bundle Mode

When running Spacebar as a bundle (single `dist/bundle/start.js`), the CDN's `start()` runs inside `Promise.all` alongside API + Gateway. The CDN's `Monitoring.attach()` tries to register prometheus metrics (`spacebar_http_request_total`, `spacebar_http_duration`) that were **already registered** by the API. This throws, rejecting the entire `Promise.all`, which prevents all post-startup code from executing.

### Fix `src/util/monitoring/Monitoring.ts`

Make `attach()` handle already-registered metrics gracefully:

```ts
// Before — throws "metric already registered"
let counter = new client.Counter({ name: "spacebar_http_request_total", ... });
client.register.registerMetric(counter);

// After — uses existing metric if already registered
let counter;
try {
  counter = new client.Counter({ name: "spacebar_http_request_total", ... });
} catch {
  counter = client.register.getSingleMetric("spacebar_http_request_total");
}
```

### Fix `dist/util/monitoring/Monitoring.js` (compiled JS)

The compiled JS is what actually runs at startup. The TypeScript source fix is for rebuilds; for immediate effect on a running system, patch the JS directly:

**Before (throws on second start when metrics already registered):**
```javascript
const http_request_total = new client.Counter({
    name: "spacebar_http_request_total", ...
});
client.register.registerMetric(http_request_total);
const http_response_rate_histogram = new client.Histogram({
    name: "spacebar_http_duration", ...
});
client.register.registerMetric(http_response_rate_histogram);
```

**After — wrap each `registerMetric` with try/catch + fallback:**
```javascript
let http_request_total;
try {
    http_request_total = new client.Counter({
        name: "spacebar_http_request_total",
        help: "The total number of HTTP requests received",
        labelNames: ["path", "method", "status_code"],
    });
    client.register.registerMetric(http_request_total);
} catch (e) {
    const existing = client.register.getSingleMetric("spacebar_http_request_total");
    if (existing) {
        http_request_total = existing;
    } else {
        throw e;
    }
}
let http_response_rate_histogram;
try {
    http_response_rate_histogram = new client.Histogram({
        name: "spacebar_http_duration",
        labelNames: ["path", "method", "status_code"],
        help: "The duration of HTTP requests in seconds",
        buckets: [0.0, 0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 10],
    });
    client.register.registerMetric(http_response_rate_histogram);
} catch (e) {
    const existing = client.register.getSingleMetric("spacebar_http_duration");
    if (existing) {
        http_response_rate_histogram = existing;
    } else {
        throw e;
    }
}
```

Key change: `let` (not `const`) so the variable can be reassigned to the existing metric.

### Fix `dist/bundle/Server.js`

Wrap each `.start()` with `.catch()` so one failure doesn't block the rest:

```ts
await Promise.all([
  api.start().catch(e => console.error("[API] Failed:", e.message)),
  cdn.start().catch(e => console.error("[CDN] Failed:", e.message)),
  gateway.start().catch(e => console.error("[Gateway] Failed:", e.message)),
  webrtc.start().catch(e => console.error("[WebRTC] Failed:", e.message)),
]);
// Then mount avatars manually as fallback
const avatarsMod = require("../cdn/routes/avatars.js");
app.use("/avatars", avatarsMod.default || avatarsMod);
```

### 6. Verify

**⚠️ Always update both `src/webpage/` AND `dist/webpage/`.** HTML changes in `dist/` take effect immediately; `src/` is the rebuild source. After any edit to instances.json or logo files, copy from `src/` to `dist/`:

```bash
cp /opt/fermi/src/webpage/*.png /opt/fermi/src/webpage/*.webp /opt/fermi/dist/webpage/ 2>/dev/null
```

Then verify:
```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3001/avatars/test
# 404 = route registered (user doesn't exist)
# 500 = route registered but handler threw
# 000 = not registered
```

## Fermi Web Client Setup

See `references/fermi-web-client-setup.md` for the full detailed guide.
## Fermi Login Troubleshooting

> **🔗 Login troubleshooting reference** — For the complete checklist covering
> duplicate users, Python vs Node.js bcrypt incompatibility, PostgreSQL password
> desync after restore, gateway state file bleed, and Fermi cache issues, see
> `references/login-troubleshooting.md`.
> 
> See `references/fermi-fixes.md` for Spacebar login schema, READY payload, and Fermi root redirect fixes.
> 
> ### 🚨 Fermi Service Worker Caches Old Assets (Browser Persistence)

The Fermi client registers a **service worker** (`/service.js`) that downloads ALL static files into an offline cache. This cache persists across **hard refreshes** (Ctrl+Shift+R) and even across domain migrations (e.g., `discy` → `gc`). If API calls still hit the old domain after a migration, the fix is **Clear Site Data** in DevTools → Application → Storage, not just a refresh.

See `references/fermi-service-worker-cache.md` for the full service worker architecture, the message-pump API (including `ForceClear` to wipe caches programmatically), and debugging techniques.

### Symptom: "This instance has likely sent the incorrect links"

Fermi shows this warning and **disables the Login button** when the gateway/CDN URLs the Spacebar API returns don't match the public API URL the client is connecting to.

### Root Cause

Spacebar's internal config returns `ws://localhost:3100/` (or whatever internal host:port the server was started on) for the gateway endpoint, rather than the public domain:

```
GET /api/v9/gateway → {"url": "ws://localhost:3100/"}       # ❌
GET /api/v9/gateway → {"url": "wss://discy.your.domain/"}   # ✅
```

Fermi discovers the API URL properly (via `.well-known/spacebar`), calls the gateway endpoint, sees the mismatch, and blocks the login.

### Diagnosis Chain

Verify each layer to pinpoint where the break is:

```bash
# 1. Is the API reachable at the public domain?
curl -s -o /dev/null -w "%{http_code}" https://discy.your.domain/api/v9/auth/login
# → 401 = good (API up, needs auth header)
# → 502 = proxy/broken tunnel

# 2. Does .well-known discovery return the correct API URL?
curl -s https://discy.your.domain/.well-known/spacebar
# → {"api":"https://discy.your.domain/api/v9"}  ✅

curl -s https://discy.your.domain/.well-known/spacebar-v2
# → {"api":"https://discy.your.domain/api/v9"}  ✅

# 3. What does the gateway endpoint return?
curl -s https://discy.your.domain/api/v9/gateway -H "Authorization: $(get-token)"
# → Check if url matches public domain or says localhost/internal

# 4. Check the server config via policies API
curl -s https://discy.your.domain/api/v9/policies/instance -H "Authorization: $(get-token)"
# serverName should be the public domain — if it's already correct,
# the gateway URL is a SEPARATE config value that needs updating
```

### Fixing the Gateway URL

**The gateway URL is NOT stored in `policies/instance`.** The `policies/instance` endpoint is GET-only (no PATCH/PUT/POST) — there is no API endpoint to update it. The fix requires server-side access:

#### Option A: Update Spacebar's config (database or environment)

Spacebar gets its gateway URL from:
- `config.json` → `gateway.endpointPublic` (if `CONFIG_PATH` is set at startup)
- Database `config` table (JSON column, if `CONFIG_PATH` is NOT set)
- See `CONFIG_PATH required for native (non-Docker) Spacebar` in the Pitfalls section below

Update via PostgreSQL:

```sql
-- If config is in DB
UPDATE config SET data = jsonb_set(data, '{gateway,endpointPublic}', '"wss://discy.your.domain/"');
```

#### Option B: Set `CONFIG_PATH` environment variable

```bash
export CONFIG_PATH='config.json'
```

In `config.json`:

```json
{
  "gateway": { "endpointPublic": "wss://discy.your.domain/" },
  "api": { "endpointPublic": "https://discy.your.domain/api/v9" },
  "cdn": { "endpointPublic": "https://discy.your.domain" }
}
```

#### Option C: Caddy rewrite (last resort — response manipulation is fragile)

Add a Caddy directive on the VPS to intercept and rewrite the gateway response:

```caddy
@gateway path /api/v9/gateway
handle @gateway {
  header Content-Type application/json
  header -Content-Length
  header -Etag
  respond {"url":"wss://discy.your.domain/"}
}
```

### Fermi's Client-Side Validation Logic

Fermi checks URLs by:
1. Reading `.well-known/spacebar` (or falling back to the instance map from `instances.json`)
2. Calling the API gateway endpoint on the discovered server
3. Comparing the gateway URL's hostname with the API URL's hostname
4. If they differ → **warning + disable login button**

### Bypassing the Warning (Temporary Workaround)

Set the correct instance info in localStorage **before** the Fermi client loads on the login screen:

```js
localStorage.setItem("instanceinfo", JSON.stringify({
  api: "https://discy.your.domain/api/v9",
  gateway: "wss://discy.your.domain/",
  cdn: "https://discy.your.domain"
}));
localStorage.setItem("fermi_client_instance", "https://discy.your.domain");
```

This is fragile — Fermi may overwrite `instanceinfo` on subsequent loads when it re-fetches the gateway endpoint and detects the mismatch again. It's useful for a one-shot login.

### Fallback: Minimal Chat Client

For quick access without fixing the server config, build a minimal HTML page that uses the Spacebar API directly (bypasses Fermi entirely). The API supports CORS (`Access-Control-Allow-Origin: *`), so any page can call it:

```html
<script>
const API = 'https://discy.your.domain/api/v9';

// Login
const r = await fetch(`${API}/auth/login`, {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({login: username, password: password})
});
const token = r.token;

// List channels
const channels = await fetch(`${API}/guilds/${guildId}/channels`, {
  headers: {'Authorization': token}
});

// Read messages
const msgs = await fetch(`${API}/channels/${channelId}/messages?limit=50`, {
  headers: {'Authorization': token}
});

// Send message
await fetch(`${API}/channels/${channelId}/messages`, {
  method: 'POST',
  headers: {'Authorization': token, 'Content-Type': 'application/json'},
  body: JSON.stringify({content: "Hello!"})
});
</script>
```

### 🚨 Fermi Login Schema Mismatch — `email` vs `login`

The Fermi client sends the login form as `{"email":"...","password":"..."}` but
Spacebar's `LoginSchema` expects `{"login":"...","password":"..."}` and rejects
`email` as an unknown property (`additionalProperties: false` in the AJV schema
validator). This produces a 400 error with `"Invalid Form Body"` — the login
never reaches the password check.

**Symptom:** API login with `curl -d '{"email":"user","password":"pass"}'` returns
`{"code":50035,"message":"Invalid Form Body"}` but `{"login":"user","password":"pass"}`
works fine.

**Fix — Disable schema validation + accept `email` field:**

1. In `/opt/spacebar/dist/api/util/handlers/route.js`, add `"LoginSchema"` to the
`ignoredRequestSchemas` array:

```javascript
const ignoredRequestSchemas = [
    "SettingsProtoUpdateJsonSchema",
    "LoginSchema",  // ← add this
];
```

2. In `/opt/spacebar/dist/api/routes/auth/login.js`, patch the destructuring:

```javascript
// Before:
const { login, password, captcha_key, undelete } = req.body;
// After:
let { login, password, captcha_key, undelete, email } = req.body;
if (!login && email) { login = email; }
```

3. Restart Spacebar: `fuser -k 3100/tcp; sleep 2; cd /opt/spacebar && CONFIG_PATH=... nohup node dist/bundle/start.js &`

Both steps are required. Fix A bypasses `additionalProperties: false`. Fix B maps
`email` → `login` so the downstream user lookup finds the matching account.

### 🚨 Fermi 302 Redirect Lockout (Root → /channels/@me)

The Fermi Node.js server issues a hard 302 redirect from `/` → `/channels/@me`
on **every** request, regardless of whether the user is authenticated:

```javascript
// dist/index.js — minified server code
if(s === "/") {
    r.writeHead(302, {"Location": "/channels/@me"});
    r.end();
    return;
}
```

The app at `/channels/@me` immediately tries to establish a WebSocket connection
with whatever token is in `localStorage`. If no valid token exists (fresh install,
cleared site data, expired session), it sends OP 2 (Identify) with an empty/invalid
token, Spacebar rejects the connection with close code 4004, and the client enters
an infinite retry loop showing:

> **"Unable to connect to the server, retrying in 9 seconds..."**

**The login form is never shown** because `/channels/@me` is the app, not the
login page (`index.html`). The user is stuck with no way to authenticate.

**Symptom:** Root URL returns 302 redirect, and after following the redirect the
page shows the retry spinner instead of the login form. All server-side checks
pass (API 200, WebSocket OP 10 received, login endpoint works).

**Fix — Patch the Fermi server to serve `index.html` at `/`:**

In `dist/index.js` (the compiled server), replace the redirect with a file read:

```javascript
// Before — infinite retry loop for unauthenticated users
if(s === "/") {
    r.writeHead(302, {"Location": "/channels/@me"});
    r.end();
    return;
}

// After — serve login page at root
if(s === "/") {
    const ip = await e.readFile(n.join(p, "webpage", "index.html"));
    r.writeHead(200, {"Content-Type": "text/html"});
    r.write(ip);
    r.end();
    return;
}
```

After patching, restart Fermi:

```bash
kill $(pgrep -f 'node dist/index') 2>/dev/null
sleep 1
cd /opt/fermi && PORT=8081 nohup node dist/index.js >> /opt/fermi/fermi.log 2>&1 &
```

Verify:
```bash
curl -s -o /dev/null -w "%{http_code}\n" https://domain/
# → 200 (not 302)
curl -sL https://domain/ | grep -o '<title>[^<]*</title>'
# → "<title>the operator: AI Chat Platform</title>"
```

The login page now loads at the root URL. The user can authenticate, and after
successful login Fermi redirects to `/channels/@me` client-side with a valid token.

**Why Caddy can't fix this:** Adding a Caddy `@root` handler with `file_server`
that serves `index.html` directly doesn't work because Caddy runs in a Docker
container that doesn't have access to the Fermi `dist/webpage/` directory on the
host. The patch to Fermi's server is the correct fix.

### 🚨 `instances.json` Cached at Startup — Restart Required

Fermi loads `instances.json` **exactly once** during process initialization.
Editing the file on disk without restarting the node process has **zero effect**
on the running server. This differs from HTML/CSS changes, which are read from
disk on every request.

**Symptom of stale cache:** You SSH to the server, edit `/opt/fermi/dist/webpage/instances.json`, verify the file content is correct with `cat`, but the public endpoint (`curl https://domain/instances.json`) still returns the old URLs.

**Fix:**
```bash
kill $(pgrep -f 'node dist/index') 2>/dev/null
sleep 1
cd /opt/fermi && nohup node dist/index.js >> /opt/fermi/fermi.log 2>&1 &
```

Then immediately verify:
```bash
curl -s http://localhost:8081/instances.json | head -5
```

The restart is only needed for `instances.json` changes — simple HTML edits (OG meta, logo src, header text) take effect immediately without restarting.

## Windows Docker Production Resilience

When deploying to **Windows** with Docker, container `restart` policies alone are not enough — Windows apps don't auto-start after reboot the way systemd services do. Use a **multi-layer approach** to ensure the stack survives reboots, crashes, and Docker Desktop restarts:

### Layer 1: Container Restart Policies

Every service in the docker-compose should use `restart: unless-stopped` or `restart: always`:

```yaml
services:
  postgres:
    restart: unless-stopped
  app:
    restart: unless-stopped
    depends_on:
      postgres:
        condition: service_healthy
```

This handles Docker daemon restarts and container crashes.

### Layer 2: Self-Contained Compose

Keep all dependencies inline in one docker-compose.yml. **Do not rely on `depends_on` pointing to a service in another stack** — it will silently fail at startup because the referenced service doesn't exist in the same file.

```yaml
services:
  postgres:     # defined HERE, in the same file
    image: postgres:16-alpine
    restart: unless-stopped
  app:
    depends_on:
      postgres:
        condition: service_healthy
```

Dependencies across stacks require shared Docker networks. The stack owning postgres must create the network; other stacks join it as external:

```yaml
networks:
  app:
    external: true
    name: backend_edge
```

### Layer 3: Docker Desktop Auto-Start

Docker Desktop must be in the Windows user startup programs:

```powershell
# Check if present
Get-ItemProperty 'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run' | Select-Object 'Docker Desktop'

# Add if missing (runs on user login)
# Docker Desktop installer usually sets this automatically
```

Verify the path points to `C:\Program Files\Docker\Docker\Docker Desktop.exe`.

### Layer 4: Windows Startup Folder Batch Script

Create a startup `.bat` script that calls `docker compose up -d` and add a shortcut to the Windows Startup folder:

```batch
@echo off
cd /d "E:\Path\To\Your\Project"
docker info >nul 2>&1
if %ERRORLEVEL% neq 0 (
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    timeout /t 30 /nobreak >nul
)
docker compose -f docker-compose.yml --env-file .env up -d
```

Add to Startup folder:

```powershell
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut([Environment]::GetFolderPath('Startup') + '\YourProject.lnk')
$Shortcut.TargetPath = 'E:\Path\To\Your\Project\docker-start.bat'
$Shortcut.WorkingDirectory = 'E:\Path\To\Your\Project'
$Shortcut.WindowStyle = 7   # minimized
$Shortcut.Description = 'Your project — Docker auto-start on Windows boot'
$Shortcut.Save()
```

### Layer 5: Hermes Cron Heartbeat (Safety Net)

As a final fallback, create a Hermes cron job that checks container health every 5 minutes and restarts on failure:

```
cronjob action=create name="Project heartbeat" schedule="every 5m" toolsets=["terminal"] workdir="E:\Path\To\Your\Project" prompt="Check if the Docker stack is running. If any container is missing or unhealthy, run 'docker compose -f docker-compose.yml --env-file .env up -d'. If Docker isn't running, launch Docker Desktop first and wait 30s. Report status."
```

### The Full Chain

```
Windows boots
  → Docker Desktop (HKCU Run, auto-starts)
    → Project.lnk (Startup folder → docker-start.bat)
      → docker compose up -d (restart: unless-stopped on all containers)
        → Hermes heartbeat cron (every 5min, catches edge cases)
```

### 🚨 Docker Desktop Intermittent Named-Pipe Failure (Windows)

Docker Desktop on Windows communicates with its Linux VM through a named pipe. This pipe can intermittently return **500 Internal Server Error** or **hang indefinitely**, especially after sleep/wake cycles or repeated `docker compose` invocations.

**Three Docker contexts, three different pipes:**
```bash
docker context ls
# default        → npipe:////./pipe/docker_engine
# desktop-linux  → npipe:////./pipe/dockerDesktopLinuxEngine
# desktop-windows → npipe:////./pipe/dockerDesktopWindowsEngine
```
The `desktop-linux` pipe is most prone to failure. The `default` context is sometimes more reliable.

**Diagnosis:** `docker ps` returns a 500 error or hangs indefinitely. The pipe is broken.

**Fix A — Full Docker Desktop restart (most reliable):**
```powershell
Get-Process 'com.docker.backend','Docker Desktop' -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Process 'C:\Program Files\Docker\Docker\Docker Desktop.exe'
```
Wait 45-60 seconds for the Linux VM to fully boot.

**🐛 Gotcha — `docker version` returns engine but `docker ps` still 500:** After relaunch, `docker version` may show the Engine version while `docker ps` still returns `500 Internal Server Error`. The named-pipe proxy connects to the engine before the container management endpoint is ready. Wait another 30-60s after `docker version` succeeds before `docker ps` works.

**Fix B — Context switching:**
```bash
docker context use default    # try this first
docker context use desktop-linux  # alternate
```
One context may work while the other is broken.

**Fix C — Run Spacebar natively (bypass Docker):**
When the pipe keeps failing, run Spacebar directly with Node.js. Connect to the existing Docker PostgreSQL container (it exposes port 5432 by default):
```bash
cd /path/to/spacebar
export NODE_ENV=production
export CONFIG_PATH=config.production.json
export PORT=3100    # avoid port 3001 conflicts (see Pitfalls)
export DATABASE=postgres://postgres@127.0.0.1:5432/spacebar
export APPLY_DB_MIGRATIONS=false
node --enable-source-maps dist/bundle/start.js
```

### 🚨 Fix D — Nuclear Recovery (WSL Distro Term + Crash-Looper Containment)

When `docker ps` hangs indefinitely and Fix A (restart Docker Desktop) doesn't help because crash-looping containers immediately re-wedge the pipe:

**Root cause:** Crash-looping containers (restarting every few seconds) stress the WSL2 `ext4.vhdx` filesystem until the Windows↔WSL named pipe deadlocks. Docker Desktop appears to be running (`com.docker.backend.exe` process alive) but all `docker` CLI commands hang. The `wsl -t docker-desktop` and `wsl --shutdown` may report success while `docker-desktop` still shows as "Running" because Docker's watchdog auto-restarts faster than you can terminate.

#### Diagnostic: check the backend log before acting

### 4. Upload to VPS + Copy to dist/

**🚨 Fermi serves ALL static files from `dist/webpage/`, NOT `src/webpage/`.** Uploading to `src/webpage/` alone has NO effect on the running server.

```bash
# Upload to src/ first (source of truth for rebuilds)
scp -i ~/.ssh/oracle_vps backus-logo.png backus-avatar.webp \
  ubuntu@vps:/opt/fermi/src/webpage/

# Then COPY to dist/ (the runtime serving directory)
ssh -i ~/.ssh/oracle_vps ubuntu@vps "cp /opt/fermi/src/webpage/backus-logo.png /opt/fermi/dist/webpage/ && cp /opt/fermi/src/webpage/backus-avatar.webp /opt/fermi/dist/webpage/"

# Update HTML and instances files in BOTH directories
ssh -i ~/.ssh/oracle_vps ubuntu@vps "sed -i 's|/logo.svg|/backus-logo.png|g' /opt/fermi/dist/webpage/login.html /opt/fermi/dist/webpage/index.html /opt/fermi/dist/webpage/app.html && sed -i 's|src=\"/logo.svg\"|src=\"/backus-logo.png\"|g' /opt/fermi/dist/webpage/index.html"
```

If you only modify HTML (not images), the `dist/webpage/` edits take effect immediately — no restart needed since HTML is read from disk on each request.

### 5. Restart Fermi (only if instances.json changed)

The `instances.json` is **cached in memory at process startup**. After modifying it, restart Fermi:

```bash
ssh -i ~/.ssh/oracle_vps ubuntu@vps "kill \$(pgrep -f 'node dist/index') 2>/dev/null; sleep 1; cd /opt/fermi && nohup node dist/index.js >> /opt/fermi/fermi.log 2>&1 &"
```

**🚨 This is NOT optional.** Unlike HTML or CSS changes (which are read from disk on every request), instances.json is loaded exactly once during process initialization. Editing the file on disk without restarting has ZERO effect on the running server. This is a common source of "I updated instances.json but Fermi still shows the old domain" reports.

Simple HTML edits (OG meta, header src) DON'T require a restart — they're read from disk on each request.

**Two patterns to look for:**

1. **Engine stuck with HTTP 500** — The log shows `still waiting for the engine to respond to _ping after Xs: HTTP 500`. The WSL VM is running but the engine's init control API is unresponsive and the named pipe is stuck. Proceed with full nuclear recovery below.

2. **WSL VM = Stopped** — If `wsl -l -v` shows `docker-desktop` as **Stopped** (not Running) while Docker Desktop processes are alive and `docker ps` hangs, the engine failed during WSL initialization. This is a **faster recovery path**: skip the `wsl -t docker-desktop` step (terminating an already-stopped distro is a no-op). Just kill Docker processes, restart, and wait for WSL to boot fresh.

```bash
# Quick check to distinguish variants
wsl -l -v 2>/dev/null | grep docker-desktop
# → "Running"  → proceed with full nuclear recovery below
# → "Stopped"  → skip Phase 4 (wsl -t), just restart Docker Desktop
```

**➡️ Step-by-step recovery (full variant):**

```bash
# 1. Kill ALL Docker Desktop processes
taskkill //F //IM "Docker Desktop.exe" 2>/dev/null
taskkill //F //IM com.docker.backend.exe 2>/dev/null
taskkill //F //IM com.docker.build.exe 2>/dev/null
taskkill //F //IM docker-sandbox.exe 2>/dev/null
taskkill //F //IM docker.exe 2>/dev/null
sleep 2
# Repeat — Docker Desktop processes respawn from Windows auto-restart
taskkill //F //IM "Docker Desktop.exe" 2>/dev/null
taskkill //F //IM com.docker.backend.exe 2>/dev/null
sleep 1

# 2. Clear stale lock files
rm -f "$LOCALAPPDATA/Docker/backend.lock" "$LOCALAPPDATA/Docker/frontend.lock" "$LOCALAPPDATA/Docker/launcher.lock"

# 3. Terminate the docker-desktop WSL distro (while Docker processes are dead)
wsl -t docker-desktop 2>/dev/null
sleep 3

# 4. Verify clean state
wsl -l -v                    # docker-desktop should be Stopped
tasklist | grep -i docker    # should return nothing (CLEAN)

# 5. Launch Docker Desktop fresh
"/c/Program Files/Docker/Docker/Docker Desktop.exe" &

# 6. Wait for responsiveness (30-60s on first boot after WSL reset)
for i in $(seq 1 20); do
  timeout 5 docker ps >/dev/null 2>&1 && break
  sleep 3
done
```

**➡️ After Docker comes back — IMMEDIATELY contain crash-loopers:**

Once `docker ps` responds, stop crash-looping containers and disable their restart policy BEFORE they can re-wedge the pipe:

```bash
# Find crash-looping containers
docker ps -a --filter "status=restarting" --format '{{.Names}}'
# Or check specific known troublemakers
docker ps -a --filter "name=spacebar" --format '{{.Names}} {{.Status}}'
docker ps -a --filter "name=oauth2-proxy" --format '{{.Names}} {{.Status}}'

# Stop + disable restart on each
for name in spacebar oauth2-proxy-n8n oauth2-proxy-agent; do
  if docker ps -a --filter "name=$name" --format '{{.Names}}' | grep -q .; then
    docker stop "$name" 2>/dev/null || true
    docker update --restart=no "$name" 2>/dev/null || true
    echo "Disabled: $name"
  fi
done
```

**Wedge recovery script:** `$HERMES_HOME/scripts/docker-wedge-recovery.sh` automates the full sequence above. To set up automatic prevention, install it as a cron heartbeat:

```bash
# Hermes cron: checks Docker every 5 minutes, auto-recovers on wedge
cronjob action=create name="Docker heartbeat" \
  schedule="every 5m" \
  toolsets=["terminal"] \
  prompt="Run the docker wedge recovery script at $HERMES_HOME/scripts/docker-wedge-recovery.sh. Report whether Docker is healthy or was recovered."
```

**🚨 Key insight:** The `docker-desktop` WSL distro is extremely persistent. Even after `wsl -t docker-desktop`, Docker Desktop's watchdog (`com.docker.backend.exe`) respawns it. You must kill ALL Docker processes first, THEN terminate the WSL distro before the watchdog restarts. If `docker-desktop` still shows as "Running" after termination, you missed a Docker process — kill and retry.

### Prevention: Stop Crash-Loopers Before They Wedge

The most common trigger for the named-pipe wedge is containers in a crash/restart loop. The Spacebar TypeORM migration crash (`42P07` on `security_keys` table) is the prime example (see Pitfalls section below).

**Prevention checklist:**
1. **Use `restart: unless-stopped` or `restart: no` for containers that may fail on boot** — avoid `restart: always` for containers whose startup depends on DB state that could be out of sync
2. **When Spacebar container keeps crashing due to migration errors**, stop it and set `restart=no` — the native Spacebar (on a different port) won't trigger the crash loop
3. **Check for crash-loopers after any Docker restart:** `docker ps -a --filter "status=restarting"` — if any exist, stop+disable them immediately
4. **Consider running Spacebar natively (Fix C)** when the Docker container is the source of repeated crashes — eliminates the crash-looper trigger entirely

## Public Domain Exposure (VPS Proxy + SSH Tunnels)

When you need to expose your local Spacebar+Fermi stack at a public domain (e.g., `https://discy.your.domain`), the architecture is:

```
Browser → discy.domain → VPS Caddy (Docker)
  ├── /api/* → 172.17.0.1:3001 → SSH tunnel → local:3001 (Spacebar API)
  ├── /.well-known/spacebar* → returns {api: "https://discy.domain/api/v9"}
  └── /*     → 172.17.0.1:8081 → SSH tunnel → local:8080 (Fermi UI)
```

### Prerequisites

- **VPS** with Docker + Caddy (or another reverse proxy) — Oracle free tier works
- **SSH key** between local machine and VPS
- **Domain** pointing to VPS IP (A record)
- **GatewayPorts** enabled on VPS SSH server (so reverse tunnel binds to `0.0.0.0`)

### Step 1: Enable GatewayPorts on VPS

```bash
sudo sed -i 's/^#GatewayPorts no/GatewayPorts yes/' /etc/ssh/sshd_config
sudo sed -i 's/^GatewayPorts no/GatewayPorts yes/' /etc/ssh/sshd_config
sudo systemctl restart sshd
```

### Step 2: Create SSH Reverse Tunnels

Run these from the local machine (where Spacebar+Fermi run):

```bash
# Tunnel 1: Spacebar API (port 3001 → localhost:3001)
ssh -N -R 0.0.0.0:3001:localhost:3001 user@vps

# Tunnel 2: Fermi UI (port 8081 → localhost:8080)
ssh -N -R 0.0.0.0:8081:localhost:8080 user@vps
```

Use `-o ServerAliveInterval=60 -o ExitOnForwardFailure=yes` for reliability.

### Step 3: Configure Caddy on VPS

The Caddy container runs in Docker bridge mode. **🚨 Pitfall:** `127.0.0.1` inside a Docker container loops to the container itself, not the host. Use the Docker gateway IP (`172.17.0.1`) or `host.docker.internal` instead.

```caddy
discy.your.domain {
  encode gzip

  # Well-known auto-discovery for Fermi
  @wellknown path /.well-known/spacebar*
  handle @wellknown {
    header Content-Type application/json
    respond {"api":"https://discy.your.domain/api/v9"}
  }

  # API + WebSocket — use handle @api, NOT handle_path
  # 🚨 handle_path strips the prefix (/api/v9/auth/login → /v9/auth/login)
  @api path /api/*
  handle @api {
    reverse_proxy 172.17.0.1:3001
  }

  # Fermi UI
  handle {
    reverse_proxy 172.17.0.1:8081
  }
}
```

### Step 4: Open iptables for Docker→Host Traffic

Docker containers cannot reach arbitrary host ports by default. Add rules INSERTED before the REJECT rule at the bottom of the INPUT chain:

```bash
sudo iptables -I INPUT 7 -i docker0 -p tcp --dport 3001 -j ACCEPT
sudo iptables -I INPUT 7 -i docker0 -p tcp --dport 8081 -j ACCEPT
# Persist
sudo iptables-save | sudo tee /etc/iptables/rules.v4
```

The rule number must be BEFORE the final REJECT. Check with `sudo iptables -L INPUT -n -v --line-numbers`.

### Step 5: Fix Fermi Client Instance URLs (Mixed-Content Fix)

**The core problem:** Fermi's built-in "Local Spacebar" instance points to `http://localhost:3001/api/v9`. When accessing Fermi via `https://discy.your.domain`, Chrome blocks HTTPS→HTTP API calls with `Local Network Access detected` errors.

**The fix:** Add an instance with HTTPS URLs in `instances.json` (served at `/instances.json` from the Fermi server):

```json
{
  "name": "Your Instance",
  "description": "Description for the picker",
  "urls": {
    "api": "https://discy.your.domain/api/v9",
    "gateway": "wss://discy.your.domain/api/v9",
    "cdn": "https://discy.your.domain",
    "wellknown": "https://discy.your.domain"
  },
  "url": "https://discy.your.domain",
  "display": true
}
```

**🚨 Pitfall: `urls` object MUST include `"wellknown"`.** Fermi's `Specialuser` constructor calls `new URL(json.serverurls.wellknown)`. If `wellknown` is undefined, the constructor throws `TypeError: URL constructor: undefined is not a valid URL`, blocking login after fetch succeeds with a token. Set it to the base server URL.

The instances are in `src/webpage/instances.json` (source) and `dist/webpage/instances.json` (built). After modifying, **restart the Fermi server** — instances are loaded at startup:

```bash
kill <fermi-pid> && cd /path/to/Fermi && node dist/index.js
```

### Step 6: Tunnel Persistence

For persistent tunnels, create a script that auto-reconnects on failure:

```bash
#!/bin/bash
while true; do
  ssh -i "$KEY" -o ServerAliveInterval=30 -o ServerAliveCountMax=3 \
    -o ExitOnForwardFailure=yes \
    -N -R 0.0.0.0:3001:localhost:3001 user@vps &
  ssh -i "$KEY" .. -N -R 0.0.0.0:8081:localhost:8080 user@vps &
  wait -n   # Wait for any tunnel to die
  kill $(jobs -p) 2>/dev/null
  sleep 3
done
```

On Windows, run via git-bash/MSYS. The script keeps running as long as the shell is open.

### 🔍 Debugging Mixed-Content Issues

When login fails from an HTTPS domain, open browser DevTools console and look for:

1. **`Local Network Access detected: ... accessing target "http://localhost:3001/...`** — The client is making HTTP API calls from an HTTPS page. Chrome blocks these. **Fix:** Change the instance API URL to HTTPS.

2. **`TypeError: URL constructor: undefined is not a valid URL`** — After a failed login, the code tries to construct a user avatar URL from undefined data. Triage the root cause (the failed API call), not this secondary error.

3. **Source map errors** about `userPreferences.ts` paths — Harmless local path leaks in the built source map. Ignore.

### Alternate Approach: Cloudflare Tunnel

If you don't have a VPS or want a simpler setup:

```bash
cloudflared tunnel --url http://localhost:8080
```

This creates a `trycloudflare.com` URL instantly. For a custom domain, use a named tunnel:

```bash
cloudflared tunnel create my-tunnel
cloudflared tunnel route dns my-tunnel discy.your.domain
cloudflared tunnel run my-tunnel
```

The quick tunnel approach has no uptime guarantee but is useful for testing.

## Hermes Agent Integration (Discord → Spacebar Routing)

Since Hermes agents use `discord.py` which hardcodes Discord's API (https://discord.com/api/v10) and WebSocket gateway (wss://gateway.discord.gg/), they cannot connect to Spacebar without redirection. Two approaches:

### Method 1: Python Monkey-Patch Wrapper (Tested, Preferred)

Create a gateway wrapper that patches discord.py constants at runtime BEFORE importing the gateway code:

```python
def patch_discord():
    import discord.http, discord.gateway
    from yarl import URL
    discord.http.Route.BASE = "http://localhost:3001/api/v9"
    discord.gateway.DiscordWebSocket.DEFAULT_GATEWAY = URL("ws://localhost:3001/")
```

**Key requirements:**
- Patches MUST execute before any `from hermes_cli.gateway import run_gateway` call
- Set `HERMES_HOME` to the profile directory (e.g., `~/AppData/Local/hermes/profiles/chief-of-staff`) to ensure the gateway runs under that profile
- **Critical: strip `sys.argv[1]` before calling `run_gateway()`** — use `sys.argv.pop(1)` not `sys.argv[1]`. Without this, the leftover profile name leaks into Hermes's argparse where it's treated as an invalid command, producing `hermes: error: argument command: invalid choice: '<profile-name>'`
- Profile's `.env` must contain `DISCORD_BOT_TOKEN=<spacebar-token>` and `HERMES_GATEWAY_BUSY_ACK_ENABLED=false`
- Run via the Hermes venv Python (not system Python): `/path/to/hermes/venv/Scripts/python.exe wrapper.py <profile-name>`

**⚠️ Slow import warning:** The first `import discord` takes ~10-15 seconds (discord.client is the bottleneck). This is NOT a hang — the gateway proceeds after import completes. For background-started processes, wait at least 30 seconds before checking connectivity.

**Verification** — log output should show:
```
[Spacebar] INFO Route.BASE: https://discord.com/api/v10 → http://localhost:3001/api/v9
[Spacebar] INFO DEFAULT_GATEWAY: wss://gateway.discord.gg/ → ws://localhost:3001/
```

**Testing confirmed:** The patching works on Hermes v0.15.1 / discord.py 2.7.1. The gateway successfully initializes and attempts to connect to Spacebar with the correct patched endpoints.

**Additional channel-type patches required:** Beyond the base URL and gateway patches,
VoiceChannel and CategoryChannel also need `_update` method patches to handle
missing Spacebar fields (`bitrate`, `permission_overwrites`). See
`references/gateway-channel-patches.md` for the complete patch code.

### 🚨 `DISCORD_COMMAND_SYNC_POLICY=off` Required to Prevent Gateway Crash

After connecting to Spacebar, the Hermes gateway's `_run_post_connect_initialization` tries to sync Discord slash commands via `GET /applications/{id}/commands`. Spacebar returns **404 Unknown application** because bot users registered through the API don't have associated OAuth2 applications. This raises an unhandled exception that crashes the gateway:

```
RuntimeError: GET /applications/<discord-channel-id>/commands failed: 404 {\"code\":404,\"message\":\"Unknown application\"}
```

The crash happens AFTER the gateway connects successfully (you see `Connected as botname#0001`), so it looks like it's stable for ~15-20 seconds before dying.

**Fix — Set `DISCORD_COMMAND_SYNC_POLICY=off` in every profile's `.env`:**

```
DISCORD_COMMAND_SYNC_POLICY=off
```

This tells the Hermes adapter to skip slash command sync entirely. The env var is checked inside `adapter.py::_get_discord_command_sync_policy()` (valid values: `safe`, `bulk`, `off`). Without it, every gateway on a Spacebar instance will crash on startup.

**Bulk fix for all profiles:**
```bash
for d in ~/AppData/Local/hermes/profiles/*/; do
  echo "DISCORD_COMMAND_SYNC_POLICY=off" >> "$d.env"
done
```

**Note:** This only affects slash command registration — regular message-based commands and the Hermes skill system still work normally through the gateway.

### 🚨 Spacebar Gateway Global `.env` Requirements

> **🔗 Thread responsiveness:** If the gateway connects but doesn't respond in
> thread channels, see `references/gateway-thread-responsiveness.md` for the
> three root causes: free response channels, DISCORD_ALLOWED_USERS mismatch,
> and thread membership.

Two settings in the global `.env` are needed for a clean gateway startup:

```
GATEWAY_ALLOW_ALL_USERS=true
HERMES_REDACT_SECRETS=true
```

- `GATEWAY_ALLOW_ALL_USERS=true` — without this, the gateway logs `No user allowlists configured. All unauthorized users will be denied.` and blocks all DMs/commands.
- `HERMES_REDACT_SECRETS=true` — without this, the gateway logs `Secret redaction: DISABLED` and leaks API keys/tokens verbatim into logs and session JSONs.

Set both **before** starting the gateway. These are global settings, not per-profile.

### 🚨 Persistent Gateway Launcher on Windows (Batch Auto-Restart)

The Hermes background terminal kills gateway processes when the parent session ends (SIGTERM → exit -15). For a persistent gateway that survives terminal sessions and auto-restarts after crashes, use a Windows batch file with an infinite restart loop:

```batch
@echo off
set HERMES_HOME_BASE=%USERPROFILE%\AppData\Local\hermes
cd /d %~dp0..\..\Documents\github\agent-fleet

:restart
echo [%date% %time%] Starting architect gateway...
set DISCORD_BOT_TOKEN=
set SPACEBAR_BOT_TOKEN=
set SPACEBAR_GATEWAY_URL=
set SPACEBAR_API_URL=

REM Source the .env file
for /f "tokens=1,* delims==" %%a in ('type "%HERMES_HOME_BASE%\profiles\<profile>\.env"') do set "%%a=%%b"

REM Clear stale state
del /f /q "%HERMES_HOME_BASE%\profiles\<profile>\gateway.pid" 2>nul
del /f /q "%HERMES_HOME_BASE%\profiles\<profile>\gateway_state.json" 2>nul

REM Start the gateway (WAIT blocks until the process exits)
start /B /WAIT python scripts/spacebar-gateway.py <profile>

echo [%date% %time%] Gateway exited - restarting in 5 seconds...
timeout /t 5 /nobreak >nul
goto restart
```

**Key design decisions:**
- `start /B` creates a truly detached process (survives the parent shell)
- `/WAIT` blocks so the batch loop knows when the gateway dies
- `goto :restart` loops forever — no external supervisor needed
- Stale state files are cleaned every iteration (gateway.pid, gateway_state.json)
- All env vars are unset at the top of each loop iteration to prevent bleed

**To install:** Place the `.bat` file in `~/AppData/Local/hermes/` and add a shortcut to `shell:startup` (Windows Startup folder) or run it from a terminal.

See `references/windows-gateway-launcher.md` for the full template and troubleshooting.

```
RuntimeError: GET /applications/<discord-channel-id>/commands failed: 404 {"code":404,"message":"Unknown application"}
```

The crash happens AFTER the gateway connects successfully (you see `Connected as botname#0001`), so it looks like it's stable for ~15-20 seconds before dying.

**Fix — Set `DISCORD_COMMAND_SYNC_POLICY=off` in every profile's `.env`:**

```
DISCORD_COMMAND_SYNC_POLICY=off
```

This tells the Hermes adapter to skip slash command sync entirely. The env var is checked inside `adapter.py::_get_discord_command_sync_policy()` (valid values: `safe`, `bulk`, `off`). Without it, every gateway on a Spacebar instance will crash on startup.

**Bulk fix for all profiles:**
```bash
for d in ~/AppData/Local/hermes/profiles/*/; do
  echo "DISCORD_COMMAND_SYNC_POLICY=off" >> "$d.env"
done
```

**Note:** This only affects slash command registration — regular message-based commands and the Hermes skill system still work normally through the gateway.

## Discord ↔ Spacebar Bidirectional Bridge

> **📄 Full reference:** See `references/discord-spacebar-bridge.md` for the
> complete bridge architecture, configuration, loop prevention, and troubleshooting.

> **📄 Thread channel organization:** See `references/thread-channel-organization.md`\n> for creating dedicated Spacebar channels per Discord thread and moving\n> messages into them.\n\n> **📄 Bridge control panel:** See `references/bridge-control-panel.md` for\n> the HTTP toggle server (port 9099) with `/enable`, `/disable`, `/toggle`,\n> and `/status` endpoints.\n\n### 🚨 Bridge Echo Loops — Two-Layer Defense

Message relay loops between Discord and Spacebar are the #1 bridge stability risk.
Three layers of defense are required:

#### Layer 1: Message-ID Cache (5-minute TTL)

Every relayed message's ID is cached for 5 minutes. If the same message ID arrives
from the other side's WebSocket, it's dropped. This catches most loop cases, but
**fails when the Spacebar WebSocket delivers a relayed message with a new
Spacebar message ID** (different from the original Discord message ID).

#### Layer 2: Unicode Marker Tags in Content (Reliable)

Each relayed message is prefixed with a Unicode marker character before the
platform label:

```python
from_discord_marker = "\u24D8"  # Ⓓ  marks "from Discord"
from_spacebar_marker = "\u24D0" # Ⓢ  marks "from Spacebar"
```

Format:
- Discord → Spacebar: `**[author]** Ⓓ (from Discord) message text`
- Spacebar → Discord: `**[author]** Ⓢ (from Spacebar) message text`

Both message handlers check for the marker character BEFORE forwarding:

```python
if self.bc.from_discord_marker in content or self.bc.from_spacebar_marker in content:
    return  # Already relayed — drop to prevent loop
```

The marker character is much more reliable than checking the text `(from Discord)`
because:
- It's a single Unicode codepoint — no substring matching issues
- It won't appear naturally in user message content
- It survives content truncation better than word-based checks

#### Layer 3: Self-Author Check (Discord side only)

The Discord `on_message` handler already checks `message.author.id == self.user.id`
to skip messages sent by the bot itself. This prevents loops caused by the Discord
side re-sending its own relayed messages.

#### Discovery: Why Text-Based Tag Checks Failed

The original bridge used `"(from Discord)" in content` as the loop check. This
failed in production because the check was only applied to one of the two
message handlers. Both the Discord `on_message` handler AND the Spacebar
`_handle_message` handler MUST have the marker check — they are independent
code paths and a half-guarded path lets the loop through, causing Discord
rate limits (429) and a bridge crash.

### 🚨 Bridge Port Conflicts (Auto-Fallback)

The bridge control panel binds to `http://127.0.0.1:9099` by default. If port
9099 is still held by a previous bridge instance (Windows SO_REUSEADDR delay),
the bridge crashes on startup. Fix: test port availability before binding and
fall back to the next open port (9100, 9101...).

Log the actual port on startup so clients know where to reach the control panel.

### 🚨 Bridge Channel Mirroring: DISABLED by Default

The bridge's `on_guild_channel_create` and `_handle_channel_create` handlers
MUST be disabled (stubbed to `pass`) to prevent spam. If left active, creating
thread channels on one side triggers creation on the other side — the operator saw
29 spam channels appear in Discord within seconds.

**Root cause:** The bridge listens for `CHANNEL_CREATE` events on both sides
and mirrors them. When you create 29 thread channels in Spacebar to organize
Discord threads, the bridge creates 29 matching channels in Discord — which
already has those conversations as threads, not separate channels.

**Fix:** Stub both handlers:
```python
async def on_guild_channel_create(self, channel):
    pass  # DISABLED — use static channel_map.json instead

async def _handle_channel_create(self, d: dict):
    pass  # DISABLED — prevents mirror loops
```

Channel mapping for the bridge is maintained via the static
`migration_data/channel_map.json` file only. Auto-creation is never safe
across platforms with different channel/thread models.

For real-time two-way sync between a Discord server and Spacebar, run a standalone
bridge daemon (`scripts/discord-spacebar-bridge.py` in the `agent-fleet` repo) that:

1. **Connects to Discord** via `discord.py` WebSocket (listening as a bot)
2. **Connects to Spacebar** via raw WebSocket (v9 gateway protocol)
3. **Forwards messages** between both platforms — `**[author]** Content` format
4. **Prevents echo loops** via 5-minute message-ID cache
5. **Mirrors channel creation** — new channels on either side are mirrored

### Architecture

```
Discord WS ──→ on_message ──→ Spacebar REST API (send_message)
Spacebar WS ──→ MESSAGE_CREATE ──→ Discord py (channel.send)
```

### Quick Start

```bash
# Install deps
pip install discord.py websockets aiohttp

# Run
cd /path/to/agent-fleet
DISCORD_BOT_TOKEN=your_token python scripts/discord-spacebar-bridge.py
```

### Bridge Control Panel (HTTP Toggle)

The bridge runs a control server on `http://127.0.0.1:9099/` for on/off toggling
without restarting the process. See `references/bridge-control-panel.md` for
the full endpoint reference.

Both message handlers check an `enabled` flag before forwarding — disabling the
bridge drops all messages in both directions immediately.

### Windows Persistence

A batch file with infinite restart loop is at `~/AppData/Local/hermes/start-bridge.bat`.
Add a shortcut to `shell:startup` for auto-start on boot.

### Method 2: HTTP Proxy (No Code Change)

Set `DISCORD_PROXY=http://localhost:8080` in the profile's `.env` and run a reverse proxy that rewrites Discord API paths to Spacebar. Requires managing a proxy server with WebSocket support.

**Tradeoff:** Method 1 is zero-infrastructure (no proxy needed). Method 2 avoids Python patching but requires nginx/similar.

### Fleet Deployment for 10+ Agents

Use a deploy script that automates profile creation, token setting, and gateway startup:

1. **Source the token `.env` file** — contains `SPACEBAR_BOT_<NAME>` vars for all bots
2. **Create/update Hermes profiles** — `hermes profile create <name>` or update existing
3. **Set tokens** — write `DISCORD_BOT_TOKEN=<token>` to each profile's `.env`
4. **Disable busy-ack** — add `HERMES_GATEWAY_BUSY_ACK_ENABLED=false` to each `.env`
5. **Start gateways** — for each agent:
   ```bash
   nohup "$VENV_PYTHON" "/path/to/spacebar-gateway.py" "$AGENT" \
     > "$LOG_DIR/spacebar-$AGENT.log" 2>&1 &
   ```

**Profile location pitfall on Windows:** Profiles are at `~/AppData/Local/hermes/profiles/<name>/`, NOT `~/.hermes/profiles/<name>/`. All path resolution in deploy scripts must use the correct location. The `hermes profile list` command shows the correct paths.

**🚨 Batch-file token env-var pitfall (Windows only):** When a `.bat` file uses `start /B` to launch the wrapper, `set TOKEN=%%y` in a `for /f` loop sets a **CMD shell variable**, NOT an environment variable. Child processes (including `start /B`'d Python) only inherit environment variables from the parent CMD session. A CMD variable like `%TOKEN%` is invisible to the Python process. **Fix:** Use `set DISCORD_BOT_TOKEN=%%y` directly — `set VAR=value` in CMD always writes to the environment block, so `DISCORD_BOT_TOKEN` becomes visible to child processes. Then check with `if defined DISCORD_BOT_TOKEN (...`. Also clear the variable at each loop iteration (`set "DISCORD_BOT_TOKEN="`) to prevent token bleeding between agents in the same batch loop.

```batch
rem DON'T: TOKEN is a CMD variable, invisible to child process
for /f "tokens=1,* delims==" %%x in (...) do set "TOKEN=%%y"
if defined TOKEN ( start /B "" python wrapper.py "%%a" )

rem DO: DISCORD_BOT_TOKEN is an env var, inherited by start /B
for /f "tokens=1,* delims==" %%x in (...) do set "DISCORD_BOT_TOKEN=%%y"
if defined DISCORD_BOT_TOKEN ( start /B "" python wrapper.py "%%a" )
```

**🚨 `start /B` vs `nohup` on Windows:** When deploying via Hermes `terminal(background=True)` with a bash script that uses `nohup`, the background shell gets killed (exit 143 = SIGTERM) when the parent process terminates. Unlike Linux where `nohup` + `&` fully detaches the child, on Windows (git-bash/MSYS) `nohup`'d children remain in the parent's process group and receive the termination signal. **Fix:** Use Windows `start /B` from a `.bat` file (which creates a truly detached process), or run the deploy script from a standalone terminal session (not a Hermes background terminal). The batch file at `start-all-spacebar-agents.bat` is the recommended launch method on Windows.

**Complete implementation:** See `agent-fleet/scripts/spacebar-gateway.py` (wrapper), `agent-fleet/scripts/spacebar-fleet-deploy.sh` (automated deploy), `agent-fleet/config/spacebar-fleet.yaml` (35-agent fleet config), and this skill's `scripts/deploy-spacebar-bots.py` (minimal Python-only deploy — register, join, token propagation).

### 🚨 Gateway State File Persistence (Token/Session Bleed)

When gateways are killed uncleanly (`taskkill /F`, process kill, Hermes background
termination), two state files persist in the profile directory and can cause new
gateway instances to use stale tokens or resume broken sessions:

- `gateway_state.json` — Contains PID, gateway state (&quot;running&quot;), and platform state (&quot;connected&quot;).
- `gateway.pid` — Contains the PID that was killed.

**Symptom:** After restarting a gateway with a fresh token, the log shows the OLD
user ID. The new gateway detects the existing PID file and either refuses to start
or attempts to resume the dead session.

**Diagnosis:**
```bash
cat ~/AppData/Local/hermes/profiles/&lt;profile&gt;/gateway_state.json
cat ~/AppData/Local/hermes/profiles/&lt;profile&gt;/gateway.pid
```

**Fix — Clear state files before restarting:**
```bash
rm -f ~/AppData/Local/hermes/profiles/&lt;profile&gt;/gateway.pid
rm -f ~/AppData/Local/hermes/profiles/&lt;profile&gt;/gateway_state.json
rm -f ~/AppData/Local/hermes/profiles/&lt;profile&gt;/gateway.lock.spacebar
rm -f ~/AppData/Local/hermes/profiles/&lt;profile&gt;/.gateway_state*
```

Also clear the gateway log to avoid confusion:
```bash
rm -f scripts/logs/&lt;profile&gt;-gateway.log
```

### 🚨 Gateway Lock File Contention (Windows)

When a gateway process is killed without clean shutdown (`taskkill /F`, Hermes background terminal termination), the `.lock` files persist:

- `~/AppData/Local/hermes/gateway.lock` — global lock
- `~/AppData/Local/hermes/profiles/<name>/gateway.lock` — per-agent

**Problem:** On Windows, these files are held open by orphaned Python.exe processes that didn't release their file handles. Attempting `rm` or `os.remove()` fails with `WinError 32 (The process cannot access the file because it is being used by another process)`.

**Fix:**

```bash
# 1. Find orphaned Python processes holding the lock
/c/Windows/System32/tasklist.exe //FI "IMAGENAME eq python.exe" //FO CSV //NH

# 2. Kill by specific PID (use with care — avoid killing active gateways)
/c/Windows/System32/taskkill.exe //F //PID <pid>

# 3. If that doesn't release it, kill ALL Hermes gateway Python processes
#    and restart cleanly. Use the batch file for reliable startup:
start-all-spacebar-agents.bat
```

**Prevention:** Always stop gateways via `hermes -p <name> gateway stop` (clean drain) rather than killing the process. When deploying via background terminal processes, signal them to exit rather than using `process(action='kill')`.

### 🚨 Gateway State File Persistence (Token/Session Bleed)

When gateways are killed uncleanly (`taskkill /F`, process kill, Hermes background termination), two state files persist in the profile directory and can cause new gateway instances to use stale tokens or resume broken sessions:

- `gateway_state.json` — Contains PID, gateway state ("running"), and platform state ("connected").
- `gateway.pid` — Contains the PID that was killed.

**Symptom:** After restarting a gateway with a fresh token, the log shows the OLD user ID. The new gateway detects the existing PID file and either refuses to start or attempts to resume the dead session.

**Fix — Clear state files before restarting:**
```bash
rm -f ~/AppData/Local/hermes/profiles/<profile>/gateway.pid
rm -f ~/AppData/Local/hermes/profiles/<profile>/gateway_state.json
rm -f ~/AppData/Local/hermes/profiles/<profile>/gateway.lock.spacebar
rm -f ~/AppData/Local/hermes/profiles/<profile>/.gateway_state*
```

Also clear the gateway log to avoid confusion:
```bash
rm -f scripts/logs/<profile>-gateway.log
```

### 🚨 `.env` files need `export` for subprocess inheritance

When a profile's `.env` file contains:

```env
DISCORD_BOT_TOKEN=***           # ❌ shell variable only
export DISCORD_BOT_TOKEN=***    # ✅ environment variable
```

The Hermes `source` command (and the gateway startup script) loads the .env via `source ~/.hermes/profiles/<name>/.env`. Without the `export` keyword, the variable is set as a **bash shell variable** and is NOT inherited by child processes (Python).

**Diagnosis:**

```bash
source ~/.hermes/profiles/dev-lead/.env
echo $DISCORD_BOT_TOKEN             # shows the value
python -c "import os; print(os.environ.get('DISCORD_BOT_TOKEN'))"  # None
```

**Fix A (preferred):** Use `set -a` before sourcing to auto-export all variables:

```bash
set -a
source ~/.hermes/profiles/dev-lead/.env
set +a
python scripts/spacebar-gateway.py dev-lead
```

This is the pattern used by `spacebar-fleet-deploy.sh` and `start-spacebar-agent.sh`.

**Fix B (permanent):** Add `export` to every variable in `.env` files. Run a one-time transform:

```bash
sed -i 's/^\([A-Z_][A-Z_0-9]*\)=/export \1=/' ~/.hermes/profiles/*/.env
```

**Fix C (batch file on Windows):** Use `start /B` with `set DISCORD_BOT_TOKEN=*** in the batch loop — `set VAR=value` in CMD always writes to the environment block, so child processes inherit it. See the Fleet Deployment note above.

## Windows Native Persistence (Non-Docker)

For the full guide on running Spacebar as a bare Node.js process (non-Docker)
with VBS startup scripts, auto-restart loops, and Windows-native process management,
see `references/windows-native-persistence-detailed.md`.

For the simpler startup reference (same topic, lighter detail), see
`references/windows-native-persistence.md`.
---

## Fermi UI Customization

### Theming to Match Discord

Fermi uses CSS variables in `themes.css` for theming. See `references/fermi-theming.md`
for the exact Discord hex codes and variable reference.

**Key colors for a Discord-like dark theme:**
- Background: `#313338`
- Sidebar: `#2b2d31`
- Accent: `#5865F2` (Discord blurple)
- Text: `#dbde1e`

**Deployment:** CSS changes in `dist/webpage/` take effect immediately. Always
update both `dist/webpage/` and `src/webpage/` for rebuild persistence.

```bash
# Edit live CSS
vim /opt/fermi/dist/webpage/themes.css
# Copy to source for rebuilds
cp /opt/fermi/dist/webpage/themes.css /opt/fermi/src/webpage/themes.css
```

### Branding / Logo Customization

See `references/fermi-branding-with-user-avatar.md` and `references/client-server-ui-customization.md`
for full branding guides (logos, meta tags, page titles, instances).

## Avatar Server (Standalone CDN)

Spacebar stores user avatars as files in `/opt/spacebar/files/avatars/<userId>/<hash>` (**no file extension**). The hash is the MD5 hex digest of the raw image data.
The bundled CDN in `dist/bundle/start.js` has a known double-slash path issue (see
CDN Route Registration above), so a standalone avatar server is preferred for production.

A rewritten avatar server is at `scripts/serve-avatars.js` in this skill's directory.
It handles both `/avatars/<userId>/<hash>` (via Caddy proxy) and `/<userId>/<hash>`
(direct) paths, strips the leading `avatars` segment when present, and serves the
file with the correct MIME type and cache headers.

**🚨 Bare filename fallback required:** Spacebar stores avatar files WITHOUT file
extensions (e.g., `/opt/spacebar/files/avatars/userId/hash` not `hash.png`). The
avatar server MUST attempt the bare filename as a fallback after trying each
supported extension. Without this fallback, all avatar requests return 404 even
though the files exist on disk.

### Systemd Service

```ini
[Unit]
Description=Avatar Static File Server for Spacebar
After=network.target

[Service]
Type=simple
User=ubuntu
ExecStart=/usr/bin/node /opt/spacebar/serve-avatars.js
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### Caddy Config

```caddy
@avatars path /avatars/*
handle @avatars {
    rewrite * /avatars{path}
    reverse_proxy 172.17.0.1:3456
}
```

The `rewrite` is a no-op placeholder — the avatar server handles the `/avatars/`
prefix internally by stripping it. Without this handler, the request falls through
to the default Fermi proxy and returns a 404.

### Verifying

```bash
# 404 = routing works, file just doesn't exist
curl -s -o /dev/null -w "%{http_code}" http://localhost:3456/avatars/testuser/testhash

# 400 = routing failed (wrong path format)
curl -s -o /dev/null -w "%{http_code}" http://localhost:3456/
```

## 🚨 Systemd Service Management

When deploying Spacebar on a Linux VPS with systemd, three services are typically
involved:

| Service | Unit File | Port |
|---------|-----------|------|
| Spacebar | `spacebar.service` | 3100 |
| Fermi | `fermi.service` | 8081 |
| Avatar server | `avatar-server.service` | 3456 |

**Pitfall — systemd overrides nohup restarts:** If you start Spacebar manually
via `nohup node dist/bundle/start.js ...` and then the systemd `spacebar.service`
is already `enabled`, the systemd service will ALSO start on boot and may bind to
the same port, or worse — start with a DIFFERENT config (no CONFIG_PATH env var)
and use the database config instead. Always restart via systemd:

```bash
sudo systemctl restart spacebar.service    # preferred
sudo systemctl status spacebar.service      # verify config + PID
```

After patching any compiled JS file (`dist/`), restart the appropriate service:

```bash
# Spacebar patches (Identify.js, login.js, route.js, Server.js, Monitoring.js)
sudo systemctl restart spacebar.service

# Fermi patches (index.js instances patch)
sudo systemctl restart fermi.service

# Avatar patches (serve-avatars.js)
sudo systemctl restart avatar-server.service
```

Wait 20-25 seconds for Spacebar to finish route registration before testing.

**Checking what config Spacebar is actually using:**
```bash
grep -o 'CONFIG_PATH\|Using CONFIG_PATH' /opt/spacebar/spacebar.log | tail -3
# → "[Config] Using CONFIG_PATH rather than database: config.production.json"
# If you don't see this line, it's reading from the DB config table.
```

## Absorbed Content

This class-level skill absorbed content from four narrow sibling skills:

| Absorbed Skill | Content Location |
|---|---|
| `spacebar-deployment` | Reference files merged into `references/` directory |
| `spacebar-bot-deployment` | Reference files merged into `references/` directory |
| `spacebar-hermes-integration` | Reference files merged into `references/` directory |
| `spacebar-bot-orchestration` | Council pattern and fleet management (covered in Fleet Management section above and references/) |
| `discord-to-spacebar-migration` | `references/discord-to-spacebar-migration.md` — Full workflow for migrating from Discord |\n  | `discord-to-spacebar-bridge` | `references/discord-spacebar-bridge.md` — Real-time two-way sync between Discord and Spacebar |

