---
name: spring-logging
description: "Structured JSON logging setup for Spring Boot applications — zero extra dependencies. Covers custom Logback JsonLayout, MDC injection via OncePerRequestFilter, frontend log ingestion API, log rotation, and Hibernate slow query tracking."
tags: ["spring-boot", "logging", "logback", "json-layout", "mdc", "structured-logging", "observability"]
metadata:
  hermes:
    tags: [spring-boot, logging, logback, json-layout, mdc, structured-logging]
---

# Spring Boot Structured JSON Logging

Configure production-ready structured logging for Spring Boot without adding logstash-logback-encoder or any external dependency. Uses Jackson (already on classpath via spring-boot-starter-web).

## When to Use

- Setting up JSON structured logging for a Spring Boot service
- Need MDC context (traceId, userId, requestPath) in every log line
- Need frontend browser logs ingested via API
- Need log rotation with time-based retention
- Working in offline/no-network environment where adding dependencies is hard

## Architecture

```
Source              Format          Storage         Retention
backend (logback)   JSON line       logs/*.json     7 days (logback)
frontend (JS)       JSON POST       logs/frontend/  7 days (logback)
nginx               JSON escape=json logs/access/   7 days (cron)
hibernate slow q    JSON (via MDC)  logs/*.json     7 days (logback)
```

## Module 1: JsonLayout — Custom Logback JSON Layout

A `LayoutBase<ILoggingEvent>` that serializes each log event as a single-line JSON object.

**File:** `src/main/java/.../logging/JsonLayout.java`

```java
public class JsonLayout extends LayoutBase<ILoggingEvent> {
    private static final ObjectMapper MAPPER = new ObjectMapper();
    private static final DateTimeFormatter ISO_FORMATTER = DateTimeFormatter.ISO_INSTANT;

    @Override
    public String doLayout(ILoggingEvent event) {
        Map<String, Object> map = new LinkedHashMap<>();
        map.put("timestamp", ISO_FORMATTER.format(Instant.ofEpochMilli(event.getTimeStamp())));
        map.put("level", event.getLevel().toString());
        map.put("logger", event.getLoggerName());
        map.put("thread", event.getThreadName());
        map.put("message", event.getFormattedMessage());
        map.put("source", "backend");  // fixed source identifier
        // MDC injected automatically
        if (event.getMDCPropertyMap() != null && !event.getMDCPropertyMap().isEmpty()) {
            map.putAll(event.getMDCPropertyMap());
        }
        // Exception info
        if (event.getThrowableProxy() != null) {
            Map<String, Object> exc = new LinkedHashMap<>();
            exc.put("class", event.getThrowableProxy().getClassName());
            exc.put("message", event.getThrowableProxy().getMessage());
            map.put("exception", exc);
        }
        return MAPPER.writeValueAsString(map) + CoreConstants.LINE_SEPARATOR;
    }
}
```

**Key points:**
- `LinkedHashMap` preserves field order (timestamp first, source last)
- Jackson is already on classpath via `spring-boot-starter-web` — zero additional Maven/Gradle dependencies
- Fallback JSON on serialization failure to prevent log loss
- `CoreConstants.LINE_SEPARATOR` added after each JSON line (important for log aggregation tools)

## Module 2: logback-spring.xml — Rolling File Appender

Three appenders pattern:

```xml
<!-- 1. Console: text format for docker logs -->
<appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
    <encoder><pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern></encoder>
</appender>

<!-- 2. JSON File: structured logging with custom layout -->
<appender name="JSON_FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
    <file>/app/logs/enterprise.json</file>
    <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
        <fileNamePattern>/app/logs/enterprise.%d{yyyy-MM-dd}.json</fileNamePattern>
        <maxHistory>7</maxHistory>
        <totalSizeCap>1GB</totalSizeCap>
    </rollingPolicy>
    <encoder class="ch.qos.logback.core.encoder.LayoutWrappingEncoder">
        <layout class="com.example.logging.JsonLayout" />
    </encoder>
</appender>

<!-- 3. Frontend File: pass-through (already JSON) -->
<appender name="FRONTEND_FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
    <file>/app/frontend-logs/frontend.json</file>
    <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
        <fileNamePattern>/app/frontend-logs/frontend.%d{yyyy-MM-dd}.json</fileNamePattern>
        <maxHistory>7</maxHistory>
    </rollingPolicy>
    <encoder><pattern>%msg%n</pattern></encoder>
</appender>

<!-- Frontend logger (standalone, no inheritance to avoid duplication) -->
<logger name="FRONTEND_LOGGER" level="INFO" additivity="false">
    <appender-ref ref="FRONTEND_FILE" />
</logger>

<!-- Hibernate slow query -->
<logger name="org.hibernate.SQL_SLOW" level="INFO" />

<root level="INFO">
    <appender-ref ref="CONSOLE" />
    <appender-ref ref="JSON_FILE" />
</root>
```

## Module 3: LoggingFilter — MDC Injection + Request Body Capture

A `OncePerRequestFilter` that sets MDC context for every `/api/**` request and captures request body/params for full audit trail.

**Key design decisions:**
- `traceId`: UUID truncated to 16 chars — compact but unique enough for tracing
- `userId`: extracted from JWT Bearer token if present (parse failure does not block the request)
- `requestPath`: URI path from `HttpServletRequest.getRequestURI()`
- `shouldNotFilter:` only applies to `/api/**` paths (excludes /actuator, static files)
- Request body capture via `ContentCachingRequestWrapper` (included in `spring-boot-starter-web`, no extra dep)
- Query parameters logged for GET/DELETE; body logged for POST/PUT (truncated to 1KB)
- Multipart requests skipped (body is binary/unparsed at filter level)
- Response body summary captured via `ContentCachingResponseWrapper` (first 200 chars)
- `MDC.clear()` in the finally block to prevent context leaking to other requests

```java
@Component
public class LoggingFilter extends OncePerRequestFilter {
    private static final Logger log = LoggerFactory.getLogger(LoggingFilter.class);
    private static final int MAX_BODY_LOG = 1024;
    private final SecretKey jwtKey;

    public LoggingFilter(@Value("${app.jwt.secret}") String jwtSecret) {
        this.jwtKey = Keys.hmacShaKeyFor(jwtSecret.getBytes(StandardCharsets.UTF_8));
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain chain) throws ServletException, IOException {
        MDC.put("traceId", UUID.randomUUID().toString().replace("-", "").substring(0, 16));
        // extract userId from JWT...
        MDC.put("requestPath", request.getRequestURI());

        // Wrap to capture request body
        ContentCachingRequestWrapper req = new ContentCachingRequestWrapper(request);
        ContentCachingResponseWrapper resp = new ContentCachingResponseWrapper(response);

        long start = System.currentTimeMillis();
        try { chain.doFilter(req, resp); }
        finally {
            long duration = System.currentTimeMillis() - start;
            String body = captureBody(req);
            String params = request.getQueryString() != null ? "?" + request.getQueryString() : "";
            String respBody = captureResponseBody(resp, response.getContentType());

            log.info("[REQ] {} {}{} -> {} ({}ms) body={} resp={}",
                request.getMethod(), request.getRequestURI(), params,
                response.getStatus(), duration, body, respBody);
            resp.copyBodyToResponse(); // ensure response body is sent
            MDC.clear();
        }
    }
    ```java
        private String captureBody(ContentCachingRequestWrapper req) {
            String ct = req.getContentType();
            if (ct != null && ct.startsWith("multipart/")) return "[multipart]";
            byte[] buf = req.getContentAsByteArray();
            if (buf == null || buf.length == 0) return "";
            String body = new String(buf, req.getCharacterEncoding() != null
                ? req.getCharacterEncoding() : StandardCharsets.UTF_8);
            return body.length() > MAX_BODY_LOG ? body.substring(0, MAX_BODY_LOG) + "..." : body;
        }

        private String captureResponseBody(ContentCachingResponseWrapper resp, String contentType) {
            // Skip binary content types (image, video, audio, octet-stream, pdf, zip)
            if (contentType != null) {
                String ct = contentType.toLowerCase();
                if (ct.startsWith("image/") || ct.startsWith("video/") || ct.startsWith("audio/")
                    || ct.contains("octet-stream") || ct.contains("pdf")
                    || ct.contains("zip") || ct.contains("gzip"))
                    return "[binary]";
            }
            byte[] buf = resp.getContentAsByteArray();
            if (buf == null || buf.length == 0) return "";
            String body = new String(buf, StandardCharsets.UTF_8);
            return body.length() > 200 ? body.substring(0, 200) + "..." : body;
        }

    @Override
    protected boolean shouldNotFilter(HttpServletRequest request) {
        return !request.getRequestURI().startsWith("/api/");
    }
}
```

## Module 4: LogController — Frontend Log Ingestion

REST endpoint at `POST /api/logs` that accepts a JSON array of log events from browser JS.

**Key design decisions:**
- `source` field is OVERRIDDEN to `"frontend"` (regardless of what the client sends) — prevents spoofing
- Written via `FRONTEND_LOGGER` logger (not the root logger), which writes to a separate file with pass-through encoder
- `additivity="false"` prevents duplicate writes to enterprise.json
- No auth required (add to SecurityConfig permitAll)
- Returns 400 on empty array
- Keepalive: true on fetch ensures delivery during page unload

```java
@RestController
@RequestMapping("/api/logs")
public class LogController {
    private static final Logger frontendLog = LoggerFactory.getLogger("FRONTEND_LOGGER");
    private static final ObjectMapper MAPPER = new ObjectMapper();

    @PostMapping
    public ResponseEntity<String> collect(@RequestBody List<Map<String, Object>> events) {
        if (events == null || events.isEmpty())
            return ResponseEntity.badRequest().body("events must be a non-empty array");
        for (Map<String, Object> event : events) {
            event.put("source", "frontend");  // override client source
            frontendLog.info(MAPPER.writeValueAsString(event));
        }
        return ResponseEntity.ok("ok");
    }
}
```

## Module 5: Frontend LogCollector (Vanilla JS)

Browser-side logger that buffers events and batch-sends to `/api/logs`.

```javascript
var __log = new (function(){
 var b=[], MAX=20, I=10000, t=null;
 var send=function(){
  var e=b.splice(0); if(!e.length) return;
  fetch('/api/logs',{method:'POST',
   body:JSON.stringify(e),headers:{'Content-Type':'application/json'},keepalive:true
  }).catch(function(){b=e.concat(b)})
 };
 var push=function(l,m,d){
  b.push({timestamp:new Date().toISOString(),level:l,message:m,data:d||null,
   url:location.href,userAgent:navigator.userAgent,source:'frontend'});
  if(!t)t=setInterval(function(){send()},I);
  if(b.length>=MAX)send()
 };
 // Override console.warn/error
 var cw=console.warn,ce=console.error;
 console.warn=function(){cw.apply(console,arguments);push('WARN',arguments[0])};
 console.error=function(){ce.apply(console,arguments);push('ERROR',arguments[0])};
 // Global error handlers
 window.onerror=function(m,s,l,c,e){push('ERROR',m,{source:s,line:l,col:c})};
 window.onunhandledrejection=function(e){
  push('ERROR','Unhandled Rejection',{reason:(e.reason&&e.reason.message)||String(e.reason)})};
 this.debug=function(m,d){push('DEBUG',m,d)};
 this.info=function(m,d){push('INFO',m,d)};
 this.warn=function(m,d){push('WARN',m,d)};
 this.error=function(m,d){push('ERROR',m,d)};
})();
```

**Key design decisions:**
- Buffer size 20 + 10s interval: balances freshness vs batching efficiency
- `keepalive: true`: ensures delivery during page navigation/close
- On send failure: events are prepended back to buffer (retry at next interval)
- Console.warn/error overridden but original is preserved (`cw.apply`) — no loss of console behavior
- `window.onerror` and `onunhandledrejection` catch everything not explicitly logged

## Module 6: Hibernate Slow Query

In `application.yml`:

```yaml
spring:
  jpa:
    properties:
      hibernate:
        session:
          events:
            LOG_QUERIES_SLOWER_THAN_MS: 2000
```

This activates Hibernate 6's built-in slow query tracker. Queries exceeding 2 seconds are logged at INFO level via logger `org.hibernate.SQL_SLOW`, automatically carrying the current MDC context.

## Module 7: Nginx JSON Access Log

```nginx
log_format json_escape escape=json '{'
 '"timestamp":"$time_iso8601",'
 '"remote_addr":"$remote_addr",'
 '"request":"$request",'
 '"status":$status,'
 '"request_time":$request_time,'
 '"source":"nginx"}';
```

**Server block pattern (suppress inherited default format):**

The `nginx:alpine` base image includes `access_log /var/log/nginx/access.log main;` in its default nginx.conf http block. If your config in `conf.d/` only adds a new `access_log`, each request produces TWO lines — one in Apache combined format (inherited) + one in JSON. Fix by explicitly disabling inherited logs before adding your JSON format:

```nginx
server {
    listen 80;
    access_log off;                                           # suppress inherited combined format
    access_log /var/log/nginx/access.log json_escape buffer=32k flush=5s;
    # ... location blocks ...
}
```

Without `access_log off;`, the default http-level combined format still fires alongside the server-level JSON format — doubling file size and making log aggregation tools parse both.

**Note:** `escape=json` (Nginx 1.11.8+) automatically escapes special characters. Without it, variables containing `"` or `\` break JSON structure.

## Module 8: Log Cleanup

Two complementary approaches:

**1. logback built-in** (covers backend + frontend JSON logs):
- `maxHistory=7` on each RollingFileAppender — logback deletes expired files during rollover
- Zero maintenance

**2. External cleanup script** (covers nginx logs):

```bash
#!/bin/bash
LOG_DIR="${1:-./logs/access}"
find "$LOG_DIR" -name "*.log" -type f -mtime +7 -delete
```

## Module 9: CLI Log Aggregation

When backend writes JSON and nginx writes JSON to separate files, viewing them together requires a unified CLI tool.

### Single-source viewer

For a single log source (e.g. backend only):

```bash
tail -n 50 "$LOG_DIR/backend/enterprise.json"
tail -f "$LOG_DIR/backend/enterprise.json"
```

### Multi-source aggregated tail (chronological order)

When backend and nginx logs are in separate files, merge by timestamp field using `jq`:

```bash
#!/bin/bash
LOG_DIR="${1:-./logs}"
tail_q() { tail -n 50 "$1" | grep '^{' | while IFS= read -r line; do
  echo "$line" | jq -c '{ts: .timestamp, msg: (.message // .request), src: .source}'
done; }
{
  tail_q "$LOG_DIR/backend/enterprise.json"
  tail_q "$LOG_DIR/access/access.log"
} | sort -t'"' -k4
```

### Live multi-stream follow

**Bash + grep (simpler):**

```bash
enterprise_logs_f() {
  local D="${1:-./logs}"
  tail -f "$D/backend/enterprise.json" "$D/access/access.log" 2>/dev/null | grep '^{'
}
```

**Python + subprocess (with source labels, for richer output):**

```python
# Multiplexes tail -f across log files, prefixing each line with a source label
import subprocess, os, select, sys

files = [("backend/enterprise.json","backend"),("access/access.log","nginx")]
procs = []
for f, label in files:
    path = os.path.join(os.environ.get('LOG_DIR','./logs'), f)
    if os.path.exists(path) and os.path.getsize(path) > 0:
        p = subprocess.Popen(["tail", "-f", "-n", "0", "--retry", path],
                             stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        procs.append((p, label))

polls = [p.stdout for p, _ in procs]
try:
    while True:
        for i, fd in enumerate(polls):
            r, _, _ = select.select([fd], [], [], 0.5)
            if r:
                line = fd.readline().rstrip('\n\r')
                if line:
                    print(f"[{procs[i][1]}] {line}", flush=True)
except (KeyboardInterrupt, SystemExit):
    for p, _ in procs: p.terminate()
```

### CLI subcommand idiom

```bash
cmd_logs() {
  local TAIL=""
  local keyword=""
  case "${1:-}" in
    -f|--tail) TAIL="-f" ;;
    backend)   local FILE="$LOG_DIR/backend/enterprise.json" ;;
    nginx)     local FILE="$LOG_DIR/access/access.log" ;;
    frontend)  local FILE="$LOG_DIR/frontend/frontend.json" ;;
    search)    keyword="${2:-}"; shift 2
               if [ -z "$keyword" ]; then echo "Usage: logs search <term>" >&2; return 1; fi
               for f in "$LOG_DIR"/{backend/enterprise.json,access/access.log,frontend/frontend.json}; do
                 [ -f "$f" ] && [ -s "$f" ] && grep -i "$keyword" "$f" | head -20
               done
               return 0 ;;
    *)         echo "Usage: logs [-f|backend|nginx|frontend|search <term>]" >&2; return 1 ;;
  esac
  if [ -z "$FILE" ]; then
    # multi-stream merge
    cmd_logs backend
    cmd_logs nginx
  else
    if [ "$TAIL" = "-f" ]; then
      tail -f "$FILE" | grep '^{'
    else
      tail -n 50 "$FILE" | grep '^{'
    fi
  fi
}
```

**Key points:**
- `grep '^{'` filters out nginx combined-format lines when both formats are present in the same file
- `jq -c` compacts each JSON event to one line for cleaner output
- Sorting by timestamp works when both sources use ISO 8601 format
- The `-f` flag uses `tail -f` for live tracking; without it shows last 50 lines

## Pitfalls

- **Logback `additivity`**: Set `additivity="false"` on FRONTEND_LOGGER. Without it, frontend events appear in both frontend.json and enterprise.json — doubling disk usage.
- **MDC leak**: Always `MDC.clear()` in a `finally` block. If an exception escapes the filter chain without clearing, the MDC context leaks to the next request, causing cross-request contamination.
- **JWT parsing in filter**: Must not throw. Parse errors should log a warning and continue — a malformed token should not break the request.
- **Frontend log source spoofing**: Backend must override `source` field, never trust the client-provided value.
- **ai-config.json empty file bug**: If ai-config.json exists but is empty, it overrides env vars with empty values. Either delete the file or fix its contents.
- **Nginx escape=json**: Requires Nginx 1.11.8+. Older versions don't support this and will write unescaped quotes, breaking JSON. For older Nginx, use a Lua script or accept imperfect JSON.
- **ContentCachingResponseWrapper + empty response**: Always call `resp.copyBodyToResponse()` after reading the cached body. Without this, the response body is consumed by the wrapper and never sent to the client — the client receives a 200 with zero content length. This is the #1 mistake when adding response body logging.
- **ContentCachingRequestWrapper body must be read after chain.doFilter**: The content is NOT cached until the wrapped request passes through the filter chain. Calling `getContentAsByteArray()` before `chain.doFilter()` returns empty. Always read in the `finally` block.
- **CLI reads the wrong log path**: When adding a CLI tool to view logs (e.g. `enterprise logs`), verify the actual log file path from the Docker volume mount, not from a stale default. In Docker Compose, `./logs/backend:/app/logs` means the file is at `$LOG_DIR/backend/enterprise.json`, not `$LOG_DIR/app.log`. Test with the real running container before declaring the CLI command complete.
