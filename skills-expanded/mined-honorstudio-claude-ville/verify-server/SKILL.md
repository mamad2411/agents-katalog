---
name: verify-server
description: Verify ClaudeVille server starts correctly, REST API responds, and WebSocket connections work. Trigger after changes to server.js or adapters/ files.
---

# Server Verification

Verify the ClaudeVille Node.js server operates correctly with all endpoints and real-time features.

## Prerequisites

- Server must NOT be running before test (port 4000 free)
- Node.js available

## Check Items

### 1. Server Startup

Start the server and verify it binds to port 4000:

```bash
node claudeville/server.js &
sleep 2
lsof -ti :4000
```

- **PASS**: Server starts, port 4000 in use, ASCII logo printed
- **FAIL**: Server crashes, port conflict, or startup error

### 2. Provider Detection

Check server log output for active providers:

- **PASS**: At least Claude Code provider detected (`~/.claude/` exists)
- **WARN**: Only 1 provider detected
- **FAIL**: No providers detected

### 3. REST API - Sessions Endpoint

```bash
curl -s http://localhost:4000/api/sessions
```

- **PASS**: Returns JSON with `{ sessions: [...], count: N, timestamp: N }`
- **FAIL**: Non-200 status, invalid JSON, or missing fields

### 4. REST API - Teams Endpoint

```bash
curl -s http://localhost:4000/api/teams
```

- **PASS**: Returns JSON with `{ teams: [...], count: N }`
- **FAIL**: Non-200 status or invalid JSON

### 5. REST API - Providers Endpoint

```bash
curl -s http://localhost:4000/api/providers
```

- **PASS**: Returns JSON with `{ providers: [...], count: N }`, count >= 1
- **FAIL**: Non-200 status or empty providers

### 6. Static File Serving

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:4000/
curl -s -o /dev/null -w "%{http_code}" http://localhost:4000/widget.html
```

- **PASS**: index.html returns 200, widget.html returns 200
- **WARN**: widget.html returns 404 (widget route not added to server)
- **FAIL**: index.html returns non-200

### 7. CORS Headers

```bash
curl -s -I http://localhost:4000/api/sessions
```

- **PASS**: `Access-Control-Allow-Origin: *` header present
- **FAIL**: Missing CORS headers

## Cleanup

After all checks, kill the server process:

```bash
kill $(lsof -ti :4000) 2>/dev/null
```
