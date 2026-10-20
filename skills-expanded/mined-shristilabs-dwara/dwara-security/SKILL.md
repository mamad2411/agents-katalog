---
name: dwara-security
description: Configure Dwara API gateway security - consumers and credentials (API keys, JWT via JWKS, OIDC introspection, HMAC request signing, mTLS client certs, Basic), the authorization chain (consumer > route > service > listener > global with deny-anywhere-wins), IP ACL and GeoIP rules, WAF-lite and CRS-style rules, security headers, TLS termination/passthrough/multi-SNI/ACME, post-quantum TLS, and secret references. Use for any dwara.yaml authentication or authorization work, 401/403 triage, consumer onboarding, or credential rotation.
license: Apache-2.0
compatibility: Works in any agent harness supporting the Agent Skills spec. Needs dwara-cli on PATH for validation.
metadata:
  author: shristilabs
  repo: https://github.com/shristilabs/dwara
  docs: https://shristilabs.github.io/dwara/
  version: "0.1.1"
---

# Dwara security

Two separate gates, in order: **authentication** (who is calling - resolves
a `consumer`) then **authorization** (may they do this). A route opts into
authn with `auth_required: true`; authz rules then apply from the
attachment chain.

```
request -> authn (credential -> consumer) -> authz chain -> filters -> proxy
            miss = 401                       deny = 403
```

## Consumers are the identity model

```yaml
consumers:
  - name: mobile-app
    type: user            # user | agent
    groups: [internal]    # feeds allowed_groups authz + masking groups
    credentials: [...]    # one or more credential families
    quotas: { daily_requests: 100000, monthly_requests: 1000000 }
    priority: 8           # load-shed priority
    token_budget: {...}   # AI budgets (dwara-ai-gateway skill)
```

Credential families and how they're presented - details in
[references/authentication.md](references/authentication.md):

| Family | Presented as | Verified by |
| --- | --- | --- |
| `api_key` | `X-API-Key` header (or query param) | Peppered-hash match (`DWARA_CREDENTIAL_PEPPER`) |
| JWT | `Authorization: Bearer` | `jwt_providers[]` JWKS (RS256/ES256..., leeway, refresh) |
| OIDC | `Authorization: Bearer` | `oidc_providers[]` RFC 7662 introspection (cached) |
| HMAC | 5 `X-Dwara-*` signed headers | HMAC-SHA256 over a canonical string, nonce + skew window |
| mTLS | TLS client certificate | `client_ca_file` + subject/fingerprint mapping |
| Basic | `Authorization: Basic` | State-store entries (admin-managed, not config) |

Bearer resolution order: JWT verification -> OIDC introspection (first
`active: true` wins) -> pass through if neither is configured.

## Authorization chain - the two laws

Levels: **consumer > route > service > listener > global**.

1. **Deny anywhere wins.** A `denied_consumers`/`denied_countries`/IP-deny
   at *any* level blocks, regardless of allows elsewhere.
2. **Most specific governs.** Otherwise only the most specific level that
   has rules is evaluated (less-specific levels are not consulted); an
   empty block at that level is transparent.

Within one block: IP gate first (deny -> allow -> default), then
consumer/group rules with `denied_*` checked before `allowed_*`. Available
rules: `allowed_consumers`/`denied_consumers`, `allowed_groups`/
`denied_groups`, `required_scopes` (JWT only), `required_claims` (exact
stringified values), `ip_acl`, `geoip` (needs `geoip.path` .mmdb).
`dry_run: true` logs what would happen (`dwara_policy_dry_run_total`,
`dwara::policy` warns) without blocking - and never *grants* anything.

Denials are `403` with a generic body (on purpose - no oracle); authn
failures are `401` with the authenticator's `WWW-Authenticate` challenge.

Full rule semantics: [references/authorization.md](references/authorization.md).

## TLS, secrets, WAF

- Listener TLS: `terminate` (multi-SNI `certificates[]`, optional
  `client_ca_file`), SNI `passthrough` (ClientHello peek, byte splice).
  ACME (`acme` block: domains, `tls-alpn01|http-01` challenge, state_dir)
  automates certs. `pq: true` opts into post-quantum X25519MLKEM768 hybrid
  (experimental; **validation-rejected in FIPS mode** - FIPS is enterprise).
- Secrets: `${ENV_VAR}` and `${file:/path}` only in OSS; resolved at config
  build; malformed refs are validation errors, never literals. Vault/KMS
  resolvers are enterprise. `GET /config` redacts; never round-trip redacted
  output.
- WAF: route-level heuristic filters (`sqli`, `xss`, `path_traversal` +
  `custom_patterns`, match -> `403 waf_blocked`) and the global CRS-style
  `waf` block (severity/phase/targets/transformations, `paranoia_level`,
  `anomaly_threshold`). Body inspection is capped by
  `max_body_inspect_bytes` - beyond the cap is uninspected.
- Security headers: per-route `security_headers` or
  `default_security_headers` (HSTS, nosniff, frame options, CSP). Note:
  unrouted 404/400 responses escape security headers.

Details: [references/tls-secrets-waf.md](references/tls-secrets-waf.md).
Runnable baseline: [assets/security-baseline.yaml](assets/security-baseline.yaml).

## Edition and wiring status (verify before promising)

- **Enterprise (`--features ent` + license)**: Vault/KMS secret sources,
  FIPS mode, admin RBAC/workspaces/audit log, SPIFFE/SPIRE mesh.
- **No config surface in the schema yet** (check `dwara-cli schema`): Cedar
  policies, OPA sidecar authorization, CEL expression conditions. The wired
  authorization path today is the built-in chain above.
- OSS-complete: every credential family, the full authz chain, WAF, TLS,
  ACME, post-quantum hybrid, peppered API-key hashing.

## Credential rotation (safe pattern)

1. Issue a new credential: `POST /consumers/{name}/credentials` - old and
   new are simultaneously valid (dual-validity window).
2. Distribute the new credential to the client.
3. Retire the old: `POST /credentials/{id}/retire` (empty body = now, or
   `{"at_ms": ...}` future - only earlier than the current retirement).
   Enforcement is lazy - already-issued in-flight requests finish.

JWKS rotation needs no ceremony: keys refresh on `refresh_secs` and
`retired_key_grace_secs` (default 24h) keeps demoted keys verifiable.
Pepper rotation: set `DWARA_CREDENTIAL_PEPPER_PREVIOUS` to the old value
while `DWARA_CREDENTIAL_PEPPER` carries the new one; restart twice.
