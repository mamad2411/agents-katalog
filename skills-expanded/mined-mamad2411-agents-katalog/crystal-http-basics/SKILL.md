---
name: crystal-http-basics
description: >
  Build and harden basic HTTP servers and clients in Crystal: HTTP::Server,
  handlers/middleware, routing, JSON APIs, TLS, timeouts, and safe header
  handling. Use for owned Crystal services and learning/production stubs —
  not as a substitute for full framework security reviews alone.
---

# Crystal HTTP Basics

## Scope And Authorization

- **In scope:** Crystal applications and HTTP services you develop or maintain.
- **Out of scope:** Pointing experimental servers at production traffic without review; scanning third-party sites with custom clients without authorization.
- Prefer explicit bind addresses and TLS termination plans before internet exposure.
- Pair with `code-quality-standards` and language-adjacent security skills (CORS, CSRF, headers) as needed.

## When To Use

- Standing up `HTTP::Server` for health checks, internal tools, or small APIs.
- Choosing between raw `HTTP::Server` and frameworks (Kemal, Lucky, Amber, Athena).
- Configuring request timeouts, body size limits, and logging.
- Writing `HTTP::Client` with timeouts and TLS verification.
- Reviewing Crystal HTTP code for common footguns (blocking in handlers, header injection).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Full REST API design / OpenAPI | `api-documentation-writing` / API skills |
| CORS deep dive | CORS skills |
| Reverse proxy TLS edge | `nginx-security-headers` |
| General Crystal style | Crystal style docs / code-quality |
| Implementation quality baseline | `code-quality-standards` |

## Core building blocks

| Type | Use |
| --- | --- |
| `HTTP::Server` | Listen, accept, dispatch handlers |
| `HTTP::Handler` | Middleware chain |
| `HTTP::Server::Context` | Request/response per connection |
| `HTTP::Client` | Outbound HTTP |
| `HTTP::Params` / JSON | Parsing bodies and query |

## Workflow

### 1. Confirm scope and success criteria

1. Role of service (public API, internal, CLI companion).
2. Success: binds correctly, health route, structured errors, timeouts, tests, graceful shutdown plan.

### 2. Minimal server

```crystal
require "http/server"

server = HTTP::Server.new do |context|
  context.response.content_type = "text/plain"
  context.response.print "ok"
end

address = server.bind_tcp "127.0.0.1", 8080
puts "Listening on http://#{address}"
server.listen
```

Prefer `127.0.0.1` until reverse proxy/TLS is ready; use `0.0.0.0` only intentionally.

### 3. Handler chain and routing

```crystal
require "http/server"

class HealthHandler
  include HTTP::Handler

  def call(context)
    if context.request.path == "/healthz"
      context.response.content_type = "application/json"
      context.response.print %({"status":"ok"})
    else
      call_next(context)
    end
  end
end

class NotFoundHandler
  include HTTP::Handler

  def call(context)
    context.response.status = :not_found
    context.response.print "not found"
  end
end

server = HTTP::Server.new([
  HTTP::LogHandler.new,
  HTTP::ErrorHandler.new,
  HealthHandler.new,
  NotFoundHandler.new,
])
server.bind_tcp "0.0.0.0", 8080
server.listen
```

For non-trivial routing, adopt a framework rather than growing ad-hoc path switches.

### 4. JSON API sketch

```crystal
require "json"

# Parse with limits — check body size before slurp
body = context.request.body.try(&.gets_to_end) || ""
if body.bytesize > 1_048_576
  context.response.status = :payload_too_large
  next
end

begin
  data = JSON.parse(body)
rescue JSON::ParseException
  context.response.status = :bad_request
  context.response.print %({"error":"invalid_json"})
  next
end
```

### 5. Safety defaults

| Topic | Practice |
| --- | --- |
| Headers | Do not put raw user input into header values (CRLF) |
| Methods | Reject unexpected methods with 405 |
| TLS | Terminate at proxy or configure OpenSSL contexts properly; never disable verify in prod clients |
| Timeouts | Set client timeouts; consider server read limits at proxy |
| Concurrency | Avoid long CPU blocks in handlers; offload heavy work |
| Logging | Structured logs; redact `Authorization` |
| CORS | Explicit allowlist if browser clients |

### 6. HTTP client

```crystal
require "http/client"

HTTP::Client.get("https://api.example.com/v1/health") do |client|
  # Prefer per-request timeouts where API allows
end

# Explicit client
client = HTTP::Client.new(URI.parse("https://api.example.com"))
client.connect_timeout = 2.seconds
client.read_timeout = 5.seconds
response = client.get("/v1/health")
client.close
```

Never ship `client.tls.verify_mode = OpenSSL::SSL::VerifyMode::NONE` in production.

### 7. Verify

```bash
crystal version
crystal build src/server.cr -o bin/server
./bin/server &
curl -sS http://127.0.0.1:8080/healthz
crystal spec
```

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Bind | Localhost or intentional iface | Accidental world bind without auth |
| Body | Size limit + JSON rescue | Unbounded `gets_to_end` |
| Client TLS | Default verify | VerifyMode::NONE |
| Errors | ErrorHandler + safe messages | Stack traces to clients in prod |
| Frameworks | Use one when routes grow | 2k-line path case statement |

## Output Checklist

- [ ] Bind address/port and TLS plan documented
- [ ] Health and readiness routes
- [ ] Handler order and error handling set
- [ ] Body size and JSON error paths tested
- [ ] Client timeouts and TLS verify confirmed
- [ ] Header injection risks reviewed
- [ ] Specs for main routes
- [ ] Logging redaction checked
- [ ] Deploy behind proxy if public
- [ ] Residual limits (no full framework features) noted

## Rules

- Crystal HTTP is capable but minimal — do not invent a framework half-way for production product APIs without review.
- Authorized targets for any client testing.
- Focus on **Crystal HTTP server/client basics** and safe defaults.
