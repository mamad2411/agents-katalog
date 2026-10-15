---
name: api-security-checklist
category: api
description: Use when you add or change an endpoint, an auth check, a query by id, an outbound call to a user-supplied URL, file handling, or anything touching credentials — the OWASP API Top 10 (2023) as concrete Go and Java checks
tech_stack: Go
source: samber/cc-skills-golang (MIT), github/awesome-copilot (MIT), adapted; category facts from OWASP API Security Top 10 2023 (cited, not reproduced)
---
# API Security Checklist

## Overview

The OWASP API Security Top 10 (2023 edition, still current) orders API risk by how often it actually bites in production. This skill maps each category to a concrete Go/Java check instead of a paragraph of theory — see https://owasp.org/API-Security/editions/2023/en/0x11-t10/ for the source list.

**Core principle:** the most common API vulnerability is a lookup by id with no ownership check. Assume every id in a URL or body is adversarial.

## API1: Broken Object-Level Authorization (BOLA)

The #1 API risk. A lookup that trusts the id alone instead of scoping it to the caller.

```go
// ❌ anyone who guesses/enumerates an id can read or modify it
task, err := repo.Get(ctx, taskID)

// ✅ scoped to the caller/tenant exactly like its neighbours
task, err := repo.GetForOwner(ctx, taskID, ownerIDFromAuth(ctx))
```

Answer "not yours" the same way the endpoint's neighbours do — usually 404 (don't reveal existence to a non-owner) unless the repo already standardizes on 403. **Test it**: a second, different authenticated user requesting the first user's object must get the not-yours response, not the object.

## API2: Broken Authentication

- New routes go in the SAME middleware group as their neighbours (Fiber: `api := app.Group("/api", authMW)`, never a bare `app.Post` outside it; Spring: match the route in the existing `SecurityFilterChain`; Quarkus: `@RolesAllowed`/`@Authenticated`).
- Compare secrets/tokens with `crypto/subtle.ConstantTimeCompare`, never `==` (timing attack on string comparison).
- Generate tokens with `crypto/rand`, never `math/rand`.

## API3: Broken Object Property-Level Authorization (BOPLA — mass assignment / excessive data exposure)

- The **request DTO** lists only the fields a client may set — never bind a request body directly onto a domain/entity struct that also has `role`, `owner_id`, `is_admin`, etc. If the DTO doesn't have the field, the client can't set it.
- The **response DTO** lists only the fields a client may read — no `password_hash`, no internal ids, no other users' data riding along in a list response. Go: unexported fields or explicit response structs, never `json:"-"` as the only defense on a type that's also bound from requests. Java: a dedicated response record, never the JPA entity.

## API4: Unrestricted Resource Consumption

- Body size limit: `fiber.Config{BodyLimit: ...}` (default 4 MB) or `http.MaxBytesReader` — don't rely on the framework default alone for upload endpoints.
- List endpoints have a maximum page size, not just a default (api-design-conventions).
- Server read/write timeouts and outbound client timeouts are set explicitly (resilient-io-and-jobs) — an unbounded request or unbounded upstream call is a resource-consumption hole.
- File uploads stream with a size cap rather than buffering the whole body in memory.

## API5: Broken Function-Level Authorization

Admin/privileged routes are behind an explicit role check, not just "authenticated" — verify the route's authorization matches its actual privilege level, not just that *some* auth middleware ran.

## API6: Unrestricted Access to Sensitive Business Flows

Rate-limit a sensitive flow (password reset, bulk export, payment) the same way its neighbours already do; don't ship a new sensitive endpoint with no rate limit when similar ones have one.

## API7: Server-Side Request Forgery (SSRF)

Any endpoint that fetches a user-supplied URL (webhooks, image-by-URL, link previews):
- Allowlist the scheme (`https` only, usually) and, where feasible, the host.
- Resolve the host and reject private/loopback/link-local ranges (`127.0.0.0/8`, `10.0.0.0/8`, `169.254.0.0/16`, `::1`, etc.) before connecting.
- Disable automatic redirect following, or re-validate the target after each redirect: Go `http.Client{CheckRedirect: func(...) error { return http.ErrUseLastResponse }}`.

## API8: Security Misconfiguration

- No `Access-Control-Allow-Origin: *` combined with `Access-Control-Allow-Credentials: true`.
- No stack traces, SQL errors, or internal paths in an error response (api-design-conventions — the error mapper owns this).
- Debug/profiling endpoints (pprof, actuator internals) are not exposed the same way in a deployed environment as in dev.

## API9: Improper Inventory Management

Keep the OpenAPI document in sync (api-contract-openapi) — an undocumented or "quietly removed" endpoint is still reachable until it's actually gone.

## API10: Unsafe Consumption of APIs

Validate and size-limit third-party API responses before trusting them; apply the same timeout/retry discipline to outbound calls as to your own endpoints (resilient-io-and-jobs).

## Beyond the Top 10

- **SQL/command injection:** parameterized queries always; `exec.Command(name, arg1, arg2)` with separate arguments, never a shell string built from user input.
- **Path traversal:** `os.Root` (Go ≥1.24) when serving files from a directory by user-supplied name.
- **Secrets:** only from env or a secret manager, never hardcoded, never on argv, never in logs (also a monorepo-wide rule).
- **Passwords:** bcrypt or argon2id, never a fast general-purpose hash.

## Commands

- `go vet ./...`
- `go run golang.org/x/vuln/cmd/govulncheck@latest ./...` — does not modify `go.mod`, safe to run anytime.
- `go test -race ./...`
- Java: run whatever dependency-vulnerability check the repo already wires into its build; don't add a new one.

## Common Mistakes

- A lookup-by-id endpoint with no ownership/tenant filter.
- Binding a request body straight onto an entity with privileged fields.
- A new sensitive endpoint shipped with no rate limit when its neighbours have one.
- An image/webhook-by-URL feature with no private-IP block.
- A stack trace or SQL error string reaching the client.

## Red Flags

- `WHERE id = $1` with no second predicate on an endpoint scoped to a caller.
- A DTO that's reused for both request binding and response serialization on a type with sensitive fields.
- `http.Get(userSuppliedURL)` with no scheme/host check beforehand.
- A new route registered outside the app's auth middleware group.
