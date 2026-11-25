name: openwork-testability
description: |
  Make testing sending a message via the UI a core part of OpenWork testability.
  Use Docker Compose + Chrome MCP as the default testing pairing.

  Triggers when user mentions:
  - "testability toolbox"
  - "dev:web + headless"
  - "send a message via the ui"
---

## Recommended: Docker Compose + Chrome MCP

One command to start, then point Chrome MCP at it. Zero manual wiring.

### 1. Start the stack

```bash
# From the openwork repo root
docker compose -f packaging/docker/docker-compose.dev.yml up -d
```

First run takes ~2 minutes (image pull + dep install + binary build).
Subsequent runs take ~10 seconds (all cached in named volumes).

Wait for both services:
- Headless health: `curl http://localhost:8787/health` (should return `{"ok":true,...}`)
- Web UI: `http://localhost:5173`

### 2. Verify with Chrome MCP

Open the web UI in Chrome MCP:

```
chrome-devtools: new_page url="http://localhost:5173"
```

The UI is already wired to headless — you'll see **"REMOTE WORKSPACE"** in the
input area and **"workspace / Remote"** in the sidebar. No Settings > Remote
configuration needed.

### 3. Send a test message

1. The UI should load on `/session` with a **"New task"** view.
2. Type a message in the chat input (e.g., "hello from testability").
3. Click **Send** (or press Enter).
4. Confirm the message appears in the thread and a response is received.

The feature is not done until this works.

### 4. Tear down

```bash
docker compose -f packaging/docker/docker-compose.dev.yml down
```

### Useful commands

```bash
# Logs
docker compose -f packaging/docker/docker-compose.dev.yml logs headless
docker compose -f packaging/docker/docker-compose.dev.yml logs web

# Health check
curl http://localhost:8787/health

# Restart just headless
docker compose -f packaging/docker/docker-compose.dev.yml restart headless

# Override tokens (optional)
OPENWORK_TOKEN=my-token docker compose -f packaging/docker/docker-compose.dev.yml up -d
```

### What the stack does

- **headless** (port 8787): installs deps, builds Linux binaries to `/tmp`
  (avoids overwriting host macOS binaries), starts OpenCode + OpenWork server,
  auto-generates and shares tokens.
- **web** (port 5173): waits for headless health check, reads the shared token,
  starts Vite with `VITE_OPENWORK_URL` pre-wired to `localhost:8787`.
- No custom Dockerfile — uses `node:22-bookworm-slim` off the shelf.
- Named volumes cache bun, pnpm store, so rebuilds are fast.

---

## Alternative: Manual (non-Docker)

Use this when Docker is unavailable or you need custom control.

### Option A: Single script (auto-wired)

```bash
cd _repos/openwork
pnpm --filter openwork-server build:bin && pnpm --filter owpenwork build:bin
pnpm dev:headless-web
```

This builds binaries, starts headless + web, and pre-wires tokens via env vars.
Open the URL printed to stdout (default `http://localhost:<port>`).

### Option B: Two separate processes

1. Start headless in an empty workspace (always use a non-default port):

```bash
mkdir -p /tmp/openwork-headless-test
nohup pnpm --filter openwrk dev -- start --workspace "/tmp/openwork-headless-test" --port 8788 > /tmp/openwrk-headless.log 2>&1 &
```

2. Start the web UI (always use a non-default port):

```bash
nohup pnpm dev:web -- --port 5175 > /tmp/openwork-dev-web.log 2>&1 &
```

3. Connect the UI to headless (Chrome MCP preferred):

- Open `http://localhost:5175/`.
- Go to Settings -> Remote.
- From `/tmp/openwrk-headless.log` copy:
  - OpenWork server URL (example: `http://127.0.0.1:8787`)
  - Client token
- Click **Test connection** and confirm **Connected**.

4. Send a test message (same as step 3 above).

---

## Capture logs if something fails

- Docker: `docker compose -f packaging/docker/docker-compose.dev.yml logs`
- Manual: `/tmp/openwrk-headless.log`, `/tmp/openwork-dev-web.log`
- Chrome DevTools console (Chrome MCP)

## Full test suite (run all)

```bash
pnpm test:health
pnpm test:sessions
pnpm test:refactor
pnpm test:events
pnpm test:todos
pnpm test:permissions
pnpm test:session-switch
pnpm test:fs-engine
pnpm test:e2e
pnpm test:openwrk
```

## Related skills

- For UI flow verification with Chrome MCP (remote behavior), use `skills/openwork-chrome-mcp-testing/SKILL.md`.

## Notes

- Docker Compose + Chrome MCP is the default testing pairing.
- The feature is not done until a UI message is sent successfully.
- First run is slow (~2min); subsequent runs use cached volumes (~10s).
- Binaries are built inside the container to `/tmp` so they don't conflict with macOS-native binaries on the host mount.
