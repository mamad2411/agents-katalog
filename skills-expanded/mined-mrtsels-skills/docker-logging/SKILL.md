---
name: docker-logging
description: Set up comprehensive request-level logging for Docker-deployed web apps — Nginx access logs, Spring Boot request/response body capture, Docker volume permissions, CLI log tools.
---

# Docker Logging Architecture

Set up a full-stack logging pipeline so every HTTP request across Nginx + Spring Boot is captured, structured, and viewable via a single CLI command.

## Architecture Overview

```
Browser / curl
    │
    ▼
Nginx (access.log — JSON lines)
    │  proxy_pass /api/ → backend
    ▼
Spring Boot (LoggingFilter — JSON to /app/logs/enterprise.json)
    │
    ▼
CLI: enterprise logs -f       # Merge + tail both sources by timestamp
```

Three log streams:
- **Nginx access** — every HTTP request hitting port 80 (static + API proxy)
- **Backend API** — every `/api/**` request with body/params/response summary
- **Frontend JS** — browser-side error/event reporting (POST to `/api/logs`)

---

## 1. Nginx Access Log Configuration

### Problem: Dual log lines (combined + JSON)

When Docker nginx:alpine has a default `access_log /var/log/nginx/access.log main;` in the http block AND you add `access_log /var/log/nginx/access.log json_escape;` in your server block, both fire — producing 2 lines per request.

### Solution: Server-level override

```nginx
# In /etc/nginx/conf.d/enterprise.conf (server block):
server {
    listen 80;
    # Override inherited combined format — only JSON is written
    access_log /var/log/nginx/access.log json_escape;
    ...
}
```

In nginx, a server-level `access_log` directive **replaces** the inherited http-level one for that server. No `off` needed.

### ⚠️ Pitfall: `access_log off;` at server level

```nginx
server {
    access_log off;                          # ← WRONG: permanently disables for this server
    access_log /var/log/nginx/access.log json_escape;  # ← NEVER FIRES
}
```

Once `off` is set at a level, subsequent `access_log` directives at the same level are ignored. Remove the `off` entirely — just use the format override directly.

### JSON log format

```nginx
log_format json_escape escape=json '{'
    '"timestamp":"$time_iso8601",'
    '"remote_addr":"$remote_addr",'
    '"request":"$request",'
    '"status":$status,'
    '"body_bytes":$body_bytes_sent,'
    '"request_time":$request_time,'
    '"upstream_status":"$upstream_status",'
    '"user_agent":"$http_user_agent",'
    '"source":"nginx"'
    '}';

access_log /var/log/nginx/access.log json_escape;
```

---

## 2. nginx:alpine Volume Mount Permissions

### Problem: Worker can't create access.log

nginx:alpine runs workers as `nginx` user (UID 101). When `/var/log/nginx` is a Docker volume mount from the macOS host (owned by UID 501), the master (root) can create `error.log` during startup, but the worker can't create `access.log` lazily on first request.

### Fix: chown in Dockerfile

```dockerfile
FROM nginx:alpine
# ... copy config, static files ...
RUN mkdir -p /var/log/nginx && chown -R nginx:nginx /var/log/nginx
```

This ensures the nginx worker has write permission to the log directory.

### Verification

```bash
# After deployment, send a request and check
curl -s -o /dev/null http://localhost/
cat /var/log/nginx/access.log        # Should have a JSON line
grep -c '^{' /var/log/nginx/access.log    # Should equal request count
```

---

## 3. Spring Boot Request Logging with Body Capture

### Filter: OncePerRequestFilter + ContentCachingRequestWrapper

```java
@Component
public class LoggingFilter extends OncePerRequestFilter {

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain chain) throws ServletException, IOException {
        // Cache request body for POST/PUT (non-multipart)
        boolean cacheBody = isBodyCacheable(request);
        HttpServletRequest wrappedRequest = cacheBody
            ? new ContentCachingRequestWrapper(request)
            : request;
        ContentCachingResponseWrapper wrappedResponse = new ContentCachingResponseWrapper(response);

        long start = System.currentTimeMillis();
        try {
            chain.doFilter(wrappedRequest, wrappedResponse);
        } finally {
            long duration = System.currentTimeMillis() - start;

            // Read cached bodies
            String body = readBody(wrappedRequest, cacheBody);
            String resBody = readResponseBody(wrappedResponse);

            log.info("[REQ] {}{}{} -> {} ({}ms) body={} res={} uid={}",
                method, uri, queryString, status, duration, body, resBody, userId);

            // CRITICAL: flush response to client
            wrappedResponse.copyBodyToResponse();
            MDC.clear();
        }
    }
}
```

### Key implementation details

- **`ContentCachingRequestWrapper`** — caches request body in `getContentAsByteArray()`. Must be used BEFORE `chain.doFilter()`.
- **`ContentCachingResponseWrapper`** — caches response body. **Must call `copyBodyToResponse()`** in the `finally` block, or the client gets an empty response.
- **Skip binary content types** — image/*, video/*, audio/*, octet-stream
- **Skip multipart** — file uploads should not be cached (memory cost)
- **Truncation** — limit request body to 1KB, response body to 200 chars in log output
- **No AOP dependency** — `ContentCachingRequestWrapper` is in `spring-boot-starter-web` (Spring Web 6.x)

### Body caching rules

```java
private boolean isBodyCacheable(HttpServletRequest request) {
    String method = request.getMethod();
    if (!"POST".equalsIgnoreCase(method) && !"PUT".equalsIgnoreCase(method)
        && !"PATCH".equalsIgnoreCase(method)) {
        return false;
    }
    String ct = request.getContentType();
    return ct == null || !ct.toLowerCase().startsWith("multipart/");
}
```

---

## 4. CLI Log Tool Pattern

### Multi-subcommand design for `enterprise logs`

```
enterprise logs               # Show last 50 lines from all sources, merged by timestamp
enterprise logs -f            # Real-time follow of all log sources with [backend]/[nginx] labels
enterprise logs backend       # Raw JSON lines from backend
enterprise logs nginx         # Raw JSON lines from nginx (filtered from access.log)
enterprise logs frontend      # Frontend JS event log
enterprise logs search <word> # Cross-file grep
```

### Argument passthrough (bash pitfall)

```bash
# WRONG — only passes first arg, $2 in function is unbound
logs) cmd_logs "${2:-}" ;;

# CORRECT — passes all remaining args
logs) shift; cmd_logs "$@" ;;
```

### Multi-file `tail -f` with labels (python3)

```python
import subprocess, select, os

files = [
    ("/path/to/backend/enterprise.json", "backend"),
    ("/path/to/nginx/access.log", "nginx"),
]

procs = []
for path, label in files:
    p = subprocess.Popen(["tail", "-f", "-n", "0", "--retry", path],
                         stdout=subprocess.PIPE, text=True)
    procs.append((p, label))

while True:
    for i, fd in enumerate([p.stdout for p, _ in procs]):
        r, _, _ = select.select([fd], [], [], 0.5)
        if r:
            line = fd.readline().rstrip()
            if line.startswith('{'):
                print(f"[{procs[i][1]}] {line}", flush=True)
```

### JSON merge by timestamp (python3)

```python
import json, os

entries = []
for path, label in sources:
    with open(path) as f:
        for line in f:
            line = line.rstrip()
            if not line.startswith('{'):
                continue
            try:
                obj = json.loads(line)
                entries.append((obj.get('timestamp', ''), label, obj))
            except json.JSONDecodeError:
                pass

entries.sort(key=lambda x: x[0])
for ts, label, obj in entries[-50:]:
    print(f"{ts} [{label.upper()}] {obj.get('message', '')}")
```

### Filtering JSON lines from mixed-format logs

When access.log still has old combined-format entries, filter with:

```bash
grep '^{' /path/to/access.log | tail -n 50
```

---

## 5. Project Layout Convention

```
logs/
├── backend/enterprise.json    # Spring Boot JSON log (via logback JsonLayout)
├── access/access.log          # Nginx access log (JSON lines only)
├── access/error.log           # Nginx error log
└── frontend/frontend.json     # Frontend JS log (POST to /api/logs)
```

Docker Compose volume mapping:

```yaml
services:
  backend:
    volumes:
      - ${LOG_DIR:-./logs}/backend:/app/logs

  frontend:
    volumes:
      - ${LOG_DIR:-./logs}/access:/var/log/nginx
```

**Important:** When docker-compose.yml is in a subdirectory, relative paths in volume mounts resolve relative to the compose file's directory, not the project root. Use absolute paths with `LOG_DIR="$(pwd)/logs"` from a wrapper script.

---

## 6. When to Use

- Setting up request logging for a Docker-deployed web app
- Adding request/response body capture to Spring Boot
- Configuring Nginx JSON access logs in Docker
- Building CLI tools for aggregating multi-source logs
- Debugging why logs aren't appearing in Docker volumes
