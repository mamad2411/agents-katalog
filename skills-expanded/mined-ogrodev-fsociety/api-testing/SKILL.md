---
name: api-testing
description: |
  Activate this skill whenever the user mentions API endpoint, REST API, RESTful, GraphQL, GraphQL introspection,
  GraphQL mutation, gRPC, gRPC reflection, WebSocket, WebSocket upgrade, WS endpoint,
  API security, API fuzzing, API enumeration, API versioning, API gateway, API rate limit,
  JWT, JSON Web Token, bearer token, access token, refresh token, API key, OAuth, OAuth2,
  OIDC, OpenID Connect, PKCE, authorization code, client credentials, implicit grant,
  BOLA, broken object level authorization, BFLA, broken function level authorization,
  mass assignment, parameter pollution, parameter tampering, parameter discovery,
  IDOR, insecure direct object reference, horizontal privilege escalation, vertical privilege escalation,
  authorization bypass, auth bypass, authentication bypass, token manipulation,
  content-type confusion, type confusion, deserialization, API injection,
  rate limiting, rate limit bypass, race condition, TOCTOU,
  Swagger, OpenAPI, API documentation, API specification, WSDL, WADL,
  API enumeration, endpoint discovery, hidden endpoints, undocumented API,
  GraphQL batching, query depth, nested query, introspection query,
  API gateway bypass, WAF bypass API, API fingerprinting,
  CORS misconfiguration, CORS bypass, origin header,
  HTTP method override, verb tampering, content negotiation,
  API key leakage, bearer token theft, token replay,
  server-sent events, SSE, long polling, streaming API,
  gRPC-web, protobuf, protocol buffers, service definition,
  arjun, x8, paramspider, postman, insomnia, burp repeater, burp intruder,
  comprehensive API audit, API pentest, API attack surface,
  or discusses testing API security, API hacking, API exploitation, or API reconnaissance.
version: 2.0.0
---

# API Security Testing

API testing is the most target-rich domain in modern application security. REST, GraphQL, gRPC, and WebSocket interfaces expose business logic directly, often with weaker controls than their web UI counterparts. This skill covers the full API attack lifecycle -- from endpoint discovery and authentication analysis through injection, authorization abuse, business logic exploitation, and rate limit bypass.

## Attack Surface Decision Tree

Before diving into testing, classify the API type and prioritize your approach.

```
Is there API documentation (Swagger/OpenAPI/GraphQL introspection)?
├── YES → Start with documented endpoints, then hunt for undocumented ones
│   ├── REST with OpenAPI → Parse spec, test every endpoint/method/parameter
│   ├── GraphQL with introspection → Dump schema, map all queries/mutations/subscriptions
│   └── gRPC with reflection → List services, extract .proto definitions
└── NO → Start with endpoint discovery and fingerprinting
    ├── Known web app → Spider + JS analysis + API path brute-force
    ├── Mobile app → Decompile APK/IPA, extract API calls and endpoints
    └── Unknown target → Port scan + service fingerprint + path fuzzing

What authentication mechanism is used?
├── JWT → jwt-attacks.md (alg:none, key confusion, claim manipulation)
├── OAuth2/OIDC → oauth-attacks.md (PKCE bypass, token theft, redirect manipulation)
├── API Key → Test key scope, rotation, leakage in logs/responses/JS
├── Session cookie → Standard session attacks (fixation, prediction, theft)
├── mTLS → Certificate validation bypass, weak CA trust
└── None / Optional → Test if auth is truly enforced on all endpoints

What is the primary risk?
├── Data exposure → Focus on BOLA/IDOR, mass data retrieval, excessive data exposure
├── Privilege escalation → Focus on auth bypass, BFLA, role manipulation
├── Injection → Focus on SQLi, NoSQLi, command injection, SSTI through API params
├── Business logic → Focus on race conditions, mass assignment, workflow bypass
└── Availability → Focus on rate limiting, GraphQL DoS, resource exhaustion
```

## Methodology

Follow this sequence for systematic API assessment. Each phase feeds the next.

### Phase 1 — Reconnaissance and Endpoint Discovery

Map the entire API attack surface before testing anything.

```bash
# Discover API endpoints — load Hexstrike tools
# ToolSearch → select:mcp__hexstrike-ai__comprehensive_api_audit

# Parameter discovery on known endpoints
# ToolSearch → select:mcp__hexstrike-ai__arjun_parameter_discovery
# ToolSearch → select:mcp__hexstrike-ai__x8_parameter_discovery
# ToolSearch → select:mcp__hexstrike-ai__paramspider_mining

# Record discovered endpoints
node ${CLAUDE_PLUGIN_ROOT}/scripts/target-intel.js add <target> endpoint "/api/v1/users" --source "api-enum"
node ${CLAUDE_PLUGIN_ROOT}/scripts/target-intel.js add <target> tech-stack "framework:express" --source "fingerprint"
```

Key actions:
1. Parse OpenAPI/Swagger specs if available (`/swagger.json`, `/api-docs`, `/openapi.yaml`, `/v2/api-docs`, `/v3/api-docs`)
2. Fuzz common API base paths: `/api/`, `/api/v1/`, `/api/v2/`, `/rest/`, `/graphql`, `/gql`, `/grpc`
3. Extract endpoints from JavaScript bundles, mobile apps, documentation
4. Test for API versioning — try `/api/v0/`, `/api/v1/`, `/api/v2/`, `/api/v3/`, `/api/internal/`, `/api/admin/`, `/api/debug/`
5. Check for GraphQL at `/graphql`, `/gql`, `/api/graphql`, `/graphql/console`, `/graphiql`
6. Check for gRPC reflection with `grpcurl`

See `references/api-enumeration.md` for comprehensive endpoint discovery techniques.

### Phase 2 — Authentication Analysis

Test the authentication layer before anything else. A broken auth mechanism gives you access to everything.

```bash
# JWT analysis
# ToolSearch → select:mcp__hexstrike-ai__jwt_analyzer

# OAuth flow analysis
# ToolSearch → select:mcp__hexstrike-ai__bugbounty_authentication_bypass_testing

# Log auth-related findings
node ${CLAUDE_PLUGIN_ROOT}/scripts/findings-tracker.js add "/api/auth/login" auth-bypass "jwt-alg" HIGH "JWT algorithm none accepted"
```

Test sequence:
1. **Token analysis**: Decode JWTs, inspect session tokens, check API key formats
2. **Algorithm attacks**: alg:none, RS256→HS256 key confusion, weak HMAC secrets
3. **Token lifecycle**: Expiry enforcement, refresh token rotation, revocation
4. **OAuth flows**: Redirect URI validation, PKCE enforcement, token leakage
5. **Credential attacks**: Default credentials, brute-force protection, account lockout

See `references/jwt-attacks.md` for JWT-specific attacks.
See `references/oauth-attacks.md` for OAuth2/OIDC exploitation.
See `references/auth-bypass.md` for authorization bypass techniques.

### Phase 3 — Authorization Testing (BOLA/BFLA/IDOR)

Authorization bugs are the #1 API vulnerability. Test every endpoint for horizontal and vertical access control.

```bash
# Replay requests with different user contexts
# ToolSearch → select:mcp__hexstrike-ai__http_repeater
# ToolSearch → select:mcp__hexstrike-ai__http_intruder

# Log authorization findings
node ${CLAUDE_PLUGIN_ROOT}/scripts/findings-tracker.js add "/api/users/123" idor "user_id" CRITICAL "BOLA — access any user's data by changing ID"
```

Test pattern:
1. Authenticate as User A, capture requests for User A's resources
2. Replace User A's token/session with User B's token/session
3. Replace resource IDs (numeric, UUID, email, username) with User B's identifiers
4. Test admin endpoints with non-admin tokens
5. Test object creation/modification/deletion with wrong user context
6. Test function-level access: can a regular user call admin-only API functions?

ID patterns to fuzz:
- Sequential integers: `1, 2, 3, ...` — trivially enumerable
- UUIDs: `550e8400-e29b-41d4-a716-446655440000` — check if predictable (v1 time-based)
- Encoded IDs: Base64, hex — decode and manipulate
- Composite IDs: `org_123_user_456` — change one component at a time

### Phase 4 — Injection Testing

APIs often lack the input validation that web forms have. Test every parameter for injection.

```bash
# API fuzzing with injection payloads
# ToolSearch → select:mcp__hexstrike-ai__api_fuzzer

# Log injection findings
node ${CLAUDE_PLUGIN_ROOT}/scripts/findings-tracker.js add "/api/search" sqli "query" CRITICAL "SQL injection in search parameter"
```

Injection targets:
1. **SQL injection**: All string parameters, especially search/filter/sort — test `'`, `"`, `1 OR 1=1`, `UNION SELECT`
2. **NoSQL injection**: JSON parameters — test `{"$gt":""}`, `{"$ne":null}`, `{"$regex":".*"}`
3. **Command injection**: Parameters used in file operations, exports, integrations — test `;id`, `|whoami`, `` `id` ``
4. **SSTI**: Parameters reflected in responses — test `{{7*7}}`, `${7*7}`, `<%= 7*7 %>`
5. **XXE**: XML-accepting endpoints — test entity expansion, external entity loading
6. **GraphQL injection**: Query variables, directive arguments — see `references/graphql-attacks.md`

Content-type switching can unlock injection vectors:
- Send `application/xml` to a JSON endpoint → enables XXE
- Send `application/x-www-form-urlencoded` → may bypass JSON validation
- Remove `Content-Type` header entirely → default parser may differ

### Phase 5 — Business Logic and Mass Assignment

Business logic flaws cannot be found by scanners. These require understanding the application's workflow.

```bash
# Parameter discovery for hidden fields
# ToolSearch → select:mcp__hexstrike-ai__arjun_parameter_discovery
# ToolSearch → select:mcp__hexstrike-ai__x8_parameter_discovery

# Log business logic findings
node ${CLAUDE_PLUGIN_ROOT}/scripts/findings-tracker.js add "/api/users/register" type-confusion "role" HIGH "Mass assignment — role field accepted in registration"
```

Test areas:
1. **Mass assignment**: Send extra fields in create/update requests (`role`, `isAdmin`, `balance`, `verified`, `plan`)
2. **Race conditions**: Concurrent requests to exploit TOCTOU bugs (double spending, duplicate registrations)
3. **Workflow bypass**: Skip steps in multi-step processes (skip payment, skip verification)
4. **Parameter pollution**: Same parameter multiple times, URL vs body parameter conflicts
5. **Object property injection**: Prototype pollution via `__proto__`, `constructor.prototype`
6. **Numeric manipulation**: Negative amounts, zero-value transactions, integer overflow

See `references/mass-assignment.md` for mass assignment and object property injection.
See `references/parameter-tampering.md` for type confusion and parameter manipulation.

### Phase 6 — Rate Limiting and Abuse

Rate limiting protects against brute-force, enumeration, and DoS. Test if limits are properly enforced.

```bash
# Rate limit testing with intruder
# ToolSearch → select:mcp__hexstrike-ai__http_intruder

# Log rate limit findings
node ${CLAUDE_PLUGIN_ROOT}/scripts/findings-tracker.js add "/api/auth/login" rate-limit "credentials" MEDIUM "No rate limiting on login endpoint"
```

See `references/rate-limit-bypass.md` for comprehensive bypass techniques.

### Phase 7 — GraphQL-Specific Testing

GraphQL introduces unique attack vectors that don't exist in REST APIs.

```bash
# GraphQL-specific scanner
# ToolSearch → select:mcp__hexstrike-ai__graphql_scanner

# Log GraphQL findings
node ${CLAUDE_PLUGIN_ROOT}/scripts/findings-tracker.js add "/graphql" info-leak "introspection" MEDIUM "GraphQL introspection enabled in production"
```

See `references/graphql-attacks.md` for introspection abuse, batching attacks, DoS via nested queries, and field-level injection.

### Phase 8 — Log and Report

Record all findings in the data layer and generate reports.

```bash
# Summary of all findings
node ${CLAUDE_PLUGIN_ROOT}/scripts/findings-tracker.js summary

# Check for exploit chains
node ${CLAUDE_PLUGIN_ROOT}/scripts/chain-detector.js

# Log technique usage
node ${CLAUDE_PLUGIN_ROOT}/scripts/techniques-tracker.js add "api_fuzzer" "<target>" "content-type-confusion" "success" \
  --notes "JSON→XML switch enabled XXE on /api/export endpoint"

# Generate HTML report
node ${CLAUDE_PLUGIN_ROOT}/scripts/findings-tracker.js html
```

## Hexstrike MCP Tool Reference

Load tools via `ToolSearch` → `select:mcp__hexstrike-ai__<tool_name>`.

| Tool | Purpose | Best For |
|------|---------|----------|
| `comprehensive_api_audit` | Full API security assessment | Initial engagement, broad coverage |
| `jwt_analyzer` | JWT decode, attack, brute-force | Token-based auth testing |
| `api_fuzzer` | Method/parameter/content-type fuzzing | Finding unexpected behaviors |
| `graphql_scanner` | GraphQL introspection, injection, DoS | GraphQL-specific targets |
| `http_repeater` | Replay and modify individual requests | Manual testing, auth manipulation |
| `http_intruder` | Parameter fuzzing with wordlists | Brute-force, enumeration, race conditions |
| `http_set_rules` | Match/replace rules for requests | Auto-refresh tokens, header injection |
| `arjun_parameter_discovery` | Common parameter name testing | Finding hidden parameters |
| `x8_parameter_discovery` | Smart heuristic parameter detection | Finding hidden parameters |
| `paramspider_mining` | Web archive parameter mining | Passive parameter discovery |
| `bugbounty_authentication_bypass_testing` | Automated auth bypass workflow | Auth mechanism testing |

## OPSEC Considerations

- **Rate your requests**: Rapid-fire API fuzzing triggers WAFs and rate limiters. Use scan profile timing
- **Rotate tokens**: Don't use the same session/token for all tests. Rotate to avoid correlation
- **Watch for logging**: API endpoints often log full request bodies. Be aware of what you send
- **Error-based enumeration**: Different error messages for valid vs invalid resources reveal object existence
- **Response time analysis**: Timing differences reveal valid vs invalid inputs even with uniform error messages
- **Header fingerprinting**: `X-Request-ID`, `X-Correlation-ID` in responses help servers trace your activity

## Vuln Types for findings-tracker

Use these types when logging API findings:

| Type | Description | Typical Severity |
|------|-------------|-----------------|
| `idor` | Broken object-level authorization (BOLA) | CRITICAL / HIGH |
| `auth-bypass` | Authentication or authorization bypass | CRITICAL / HIGH |
| `sqli` | SQL injection via API parameters | CRITICAL |
| `nosqli` | NoSQL injection (MongoDB, etc.) | CRITICAL / HIGH |
| `cmdi` | Command injection via API parameters | CRITICAL |
| `xss` | XSS via API response reflection | MEDIUM / HIGH |
| `ssti` | Server-side template injection | HIGH / CRITICAL |
| `xxe` | XML external entity via content-type switch | HIGH / CRITICAL |
| `ssrf` | SSRF via API parameters (URLs, webhooks) | HIGH / CRITICAL |
| `info-leak` | Excessive data exposure, debug info, stack traces | MEDIUM / LOW |
| `user-enum` | User enumeration via API responses/timing | LOW / MEDIUM |
| `type-confusion` | Mass assignment, type confusion, parameter pollution | MEDIUM / HIGH |
| `rate-limit` | Missing or bypassable rate limiting | MEDIUM / LOW |
| `config` | CORS misconfiguration, insecure headers, verbose errors | MEDIUM / LOW |

## References

| Reference | Coverage |
|-----------|----------|
| `references/api-enumeration.md` | Endpoint discovery, version fuzzing, spec parsing, JS extraction, path brute-force |
| `references/auth-bypass.md` | Header manipulation, method override, path traversal, token manipulation, race conditions, CORS abuse |
| `references/jwt-attacks.md` | Algorithm none, key confusion, claim manipulation, JWKS abuse, key brute-force, nested JWT |
| `references/oauth-attacks.md` | PKCE bypass, redirect URI manipulation, token theft, scope escalation, client confusion |
| `references/parameter-tampering.md` | Type confusion, HTTP parameter pollution, prototype pollution, content-type switching, deserialization |
| `references/mass-assignment.md` | Hidden field discovery, object property injection, framework-specific patterns, detection and chaining |
| `references/graphql-attacks.md` | Introspection abuse, batching attacks, nested query DoS, field injection, authorization bypass |
| `references/rate-limit-bypass.md` | Header manipulation, distributed requests, race conditions, GraphQL batching, parameter mutation |
