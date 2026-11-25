---
name: "gateway-patterns"
description: "API gateway patterns with configuration and code: token bucket rate limiting in Redis and Lua, JWT validation at the edge, backend-for-frontend topology, API versioning with Sunset headers, request ID propagation, and the gateway anti-patterns to avoid. Use when building or reviewing a gateway layer."
---

# Gateway Patterns

> Named patterns, configuration examples, and anti-patterns for API gateway design. Covers rate limiting algorithms, JWT validation, BFF topology, API versioning, and circuit breaking at the edge.

## Patterns

### Pattern: Token Bucket Rate Limiting (Redis + Lua)

The token bucket algorithm allows bursts up to the bucket capacity while enforcing an average rate. Each client has a virtual bucket that refills at a fixed rate. Requests consume tokens. When the bucket is empty, requests are rejected.

Redis atomic Lua implementation (single round-trip, avoids race condition):

```lua
-- token_bucket.lua
-- KEYS[1] = bucket key, e.g. "rl:user:42"
-- ARGV[1] = capacity (max tokens)
-- ARGV[2] = refill rate (tokens/second)
-- ARGV[3] = current timestamp (unix seconds, float)
-- ARGV[4] = tokens requested (usually 1)

local key = KEYS[1]
local capacity = tonumber(ARGV[1])
local rate = tonumber(ARGV[2])
local now = tonumber(ARGV[3])
local requested = tonumber(ARGV[4])

local bucket = redis.call('HMGET', key, 'tokens', 'last_refill')
local tokens = tonumber(bucket[1]) or capacity
local last_refill = tonumber(bucket[2]) or now

-- Refill tokens based on elapsed time
local elapsed = now - last_refill
local refilled = math.min(capacity, tokens + elapsed * rate)

if refilled < requested then
  -- Not enough tokens — reject
  redis.call('HMSET', key, 'tokens', refilled, 'last_refill', now)
  redis.call('EXPIRE', key, math.ceil(capacity / rate) + 1)
  return 0  -- rejected
else
  -- Consume tokens — allow
  redis.call('HMSET', key, 'tokens', refilled - requested, 'last_refill', now)
  redis.call('EXPIRE', key, math.ceil(capacity / rate) + 1)
  return 1  -- allowed
end
```

Kong declarative configuration using Rate Limiting Advanced plugin:

```yaml
# kong.yaml (deck format)
plugins:
  - name: rate-limiting-advanced
    config:
      limit: [100]             # 100 requests
      window_size: [60]        # per 60 seconds
      window_type: sliding     # sliding window counter
      identifier: consumer     # rate limit per Kong consumer
      strategy: redis          # distributed counter in Redis
      redis:
        host: redis.internal
        port: 6379
        database: 0
      hide_client_headers: false
      retry_after_jitter_max: 0
```

### Pattern: JWT Validation at the Edge

Gateway validates JWT structure, signature, and standard claims. It then forwards a trusted identity header to the backend. The backend trusts the header only from known gateway addresses — it does not re-validate the JWT.

Nginx/OpenResty JWT validation (via `lua-resty-jwt`):

```nginx
# nginx.conf
location /api/ {
    access_by_lua_block {
        local jwt = require("resty.jwt")
        local cjson = require("cjson")

        local auth_header = ngx.req.get_headers()["Authorization"]
        if not auth_header or not auth_header:find("^Bearer ") then
            ngx.status = 401
            ngx.say('{"error":"missing_token"}')
            return ngx.exit(401)
        end

        local token = auth_header:sub(8)  -- strip "Bearer "

        -- Public key fetched from JWKS and cached
        local jwt_obj = jwt:verify(ngx.shared.jwt_public_keys:get("current"), token, {
            valid_issuers = {"https://auth.example.com"},
            valid_audiences = {"api.example.com"},
        })

        if not jwt_obj.verified then
            ngx.status = 401
            ngx.say('{"error":"invalid_token","detail":"' .. jwt_obj.reason .. '"}')
            return ngx.exit(401)
        end

        -- Forward validated identity to backend
        ngx.req.set_header("X-User-Id", jwt_obj.payload.sub)
        ngx.req.set_header("X-User-Scopes", table.concat(jwt_obj.payload.scope or {}, ","))
        ngx.req.set_header("X-Tenant-Id", jwt_obj.payload.tid or "")
        ngx.req.clear_header("Authorization")  -- backend does not need the token
    }

    proxy_pass http://backend_upstream;
}
```

Envoy JWT authentication filter:

```yaml
# envoy.yaml fragment
http_filters:
  - name: envoy.filters.http.jwt_authn
    typed_config:
      "@type": type.googleapis.com/envoy.extensions.filters.http.jwt_authn.v3.JwtAuthentication
      providers:
        auth0:
          issuer: "https://auth.example.com/"
          audiences:
            - "api.example.com"
          remote_jwks:
            http_uri:
              uri: "https://auth.example.com/.well-known/jwks.json"
              cluster: auth0_jwks_cluster
              timeout: 5s
            cache_duration: 300s
          forward_payload_header: "x-jwt-payload"  # base64-encoded claims forwarded to backend
      rules:
        - match: { prefix: "/api/" }
          requires: { provider_name: "auth0" }
        - match: { prefix: "/health" }
          # No JWT required for health checks
```

### Pattern: Backend for Frontend (BFF) Topology

Three clients, three gateways. Each owned by the team responsible for that client surface.

```
                    ┌─────────────────┐
  Web Browser ─────►│   Web BFF       │──► User Service
                    │  (Node/Express) │──► Order Service (full payload)
                    └─────────────────┘──► Product Service

                    ┌─────────────────┐
  iOS/Android ─────►│   Mobile BFF    │──► User Service
                    │  (Go/Gin)       │──► Order Service (compact payload)
                    └─────────────────┘──► Product Service (image URLs only)

                    ┌─────────────────┐
  Third Parties ───►│   Public API GW │──► User Service (scoped)
                    │  (Kong)         │──► Order Service (versioned, rate limited)
                    └─────────────────┘
```

Mobile BFF response shaping — reducing a 4KB web response to 800 bytes for mobile:

```typescript
// mobile-bff/src/routes/orders.ts
app.get('/orders/:id', async (req, res) => {
  const [order, user] = await Promise.all([
    orderService.getOrder(req.params.id),
    userService.getUser(req.headers['x-user-id']),
  ]);

  // Mobile needs summary only — no line item details, no audit history
  res.json({
    id: order.id,
    status: order.status,
    total: order.total,
    currency: order.currency,
    item_count: order.line_items.length,
    placed_at: order.created_at,
    // Omit: line_items[], shipping_address, billing_address, audit_log[], metadata
  });
});
```

### Pattern: API Versioning with Sunset Headers

Route by URI prefix. Deprecated versions return `Sunset` and `Link` headers (RFC 8594) warning clients.

Kong route configuration:

```yaml
routes:
  - name: orders-v1
    paths: ["/v1/orders"]
    service: order-service-v1
    plugins:
      - name: response-transformer
        config:
          add:
            headers:
              - "Sunset: Sat, 01 Jan 2026 00:00:00 GMT"
              - 'Link: <https://api.example.com/v2/orders>; rel="successor-version"'
              - "Deprecation: true"

  - name: orders-v2
    paths: ["/v2/orders"]
    service: order-service-v2
```

### Pattern: Request ID Propagation

Inject a correlation ID at the gateway for distributed tracing. If the client sends `X-Request-Id`, validate it (UUID format); otherwise generate one. Never trust client-provided trace IDs for security context.

```nginx
# Nginx: generate or validate X-Request-Id
map $http_x_request_id $request_id_final {
    "~^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$" $http_x_request_id;
    default $request_id;  # nginx built-in UUID generation
}

server {
    location /api/ {
        proxy_set_header X-Request-Id $request_id_final;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        add_header X-Request-Id $request_id_final always;
    }
}
```

## Anti-Patterns

### Anti-Pattern: Business Logic in the Gateway

**Incident type**: The gateway queries a product catalog service to determine if a route should be allowed based on product availability. When the catalog service has elevated latency, all gateway requests slow down — including routes unrelated to products.

**Rule**: The gateway makes routing decisions based on request metadata (path, headers, JWT claims). It never calls business services to decide whether to route.

Bad (Kong Lua plugin):
```lua
-- DON'T: gateway calling a business service to make routing decision
local res = http:request_uri("http://product-service/availability/" .. product_id)
if res.status ~= 200 then ngx.exit(503) end
```

Good: Product availability is a service concern. The service returns 404/409. The gateway passes the request through.

### Anti-Pattern: Overly Fat Gateway (The Gateway Monolith)

A gateway that does: authentication + authorization + transformation + aggregation + caching + rate limiting + validation + business rules is a distributed monolith with worse operational characteristics than the monolith it replaced. Each concern added to the gateway reduces team autonomy.

Checklist — if your gateway does more than 4 of these, decompose:
- [ ] Authentication (verifying identity) — OK at gateway
- [ ] Authorization (what the user can do to which resource) — belongs at service
- [ ] Rate limiting — OK at gateway
- [ ] Request routing — core gateway function
- [ ] SSL termination — OK at gateway
- [ ] Response transformation (changing payload structure) — belongs at BFF, not shared gateway
- [ ] Request aggregation (fan-out) — belongs at BFF
- [ ] Caching — belongs at CDN or service
- [ ] Business validation (is this a valid order?) — belongs at service

### Anti-Pattern: Synchronous Gateway Team Bottleneck

Every new route requires a PR to the gateway team's repository, reviewed, merged, and deployed by them. With 20 microservice teams this becomes a bottleneck within weeks.

Solution: GitOps self-service routing. Each service team owns their own route definitions in their service repository. A CI job runs `deck sync` (Kong) or applies the IngressRoute CRD (Traefik) automatically.

```yaml
# order-service/infra/kong-route.yaml (owned by order team, not gateway team)
_format_version: "3.0"
routes:
  - name: order-service-routes
    service: order-service
    paths: ["/v2/orders", "/v2/orders/.*"]
    methods: [GET, POST, PATCH, DELETE]
    strip_path: false
```

### Anti-Pattern: Missing Retry Budget Amplification

Service A calls gateway → gateway calls Service B. Service B is degraded. Service A retries 3 times with exponential backoff. Gateway also retries 3 times. Effective retry amplification: 9x. Under load this creates a retry storm.

Rule: Retry at one layer only. Either the gateway retries (and services do not), or services retry (and the gateway does not). Prefer service-level retries with gateway-level circuit breaking (fast fail when error rate exceeds threshold).

## References

- Kong Rate Limiting Advanced Plugin: docs.konghq.com/hub/kong-inc/rate-limiting-advanced/
- Envoy JWT Authentication: envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/jwt_authn_filter
- RFC 8594: The Sunset HTTP Header Field
- Newman, Sam. "Pattern: Backends For Frontends." samnewman.io, 2015.
- Richardson, Chris. _Microservices Patterns_, Chapter 8. Manning, 2018.
- Nginx `auth_request` module documentation.
- Cloudflare: "An in-depth analysis of sliding window rate limiting." 2023.
