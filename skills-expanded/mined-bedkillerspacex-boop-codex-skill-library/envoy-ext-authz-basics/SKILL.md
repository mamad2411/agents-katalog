---
name: envoy-ext-authz-basics
description: >
  Design, review, and troubleshoot Envoy external authorization (ext_authz):
  HTTP/network filter placement, gRPC vs HTTP auth services, CheckRequest/
  CheckResponse, failure_mode_allow, header mutation, and route overrides. Use
  for owned Envoy/Istio edges—not unauthorized proxy attacks or pure app JWT
  without the Envoy hop.
---

# Envoy ext_authz Basics

## Scope And Authorization

- **In scope:** Envoy/Istio/API gateway configs and auth services you operate.
- **Out of scope:** Pointing ext_authz experiments at third-party edges without permission.
- Prefer fail-closed (`failure_mode_allow: false`) for authenticated APIs.
- Redact tokens from admin config dumps and logs.
- Pair with app auth skills and `code-quality-standards` for the authz service code.

## When To Use

- Centralizing authn/z at the proxy with an external policy service.
- Debugging 403 / `denied by ext_authz` / timeouts to the auth cluster.
- Reviewing whether auth failures fail open.
- Header injection from auth service (`Authorization`, `x-user-id`) with trust rules.
- Istio AuthorizationPolicy vs EnvoyFilter ext_authz choices.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Upstream host ejection | `envoy-outlier-detection` |
| JWT validation only in app | `api-auth-and-jwt-abuse` patterns |
| OPA/Cedar policy modeling depth | policy engine skills |
| Admin interface lockdown only | Envoy security hardening notes herein + catalog |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Placement | ext_authz in http_filters before router |
| Protocol | gRPC V3 Check preferred; HTTP service supported |
| Fail mode | `failure_mode_allow: false` for secured routes |
| Timeouts | Tight timeout + retries policy intentional |
| Headers | Auth service may set identity headers; strip client spoofing |
| Per-route | Skip ext_authz for health checks only |

## Workflow

### 1. Confirm scope and success criteria

1. Listeners/routes requiring auth; public paths exceptions.
2. Success: unauthenticated denied; authz down does not silently allow; latency budget met.

### 2. Inventory Envoy config

```bash
# From admin interface on localhost only
curl -s http://127.0.0.1:9901/config_dump | head
curl -s http://127.0.0.1:9901/clusters | grep -i auth
rg -n "ext_authz|envoy.filters.http.ext_authz" -S .
```

1. Find filter order relative to jwt_authn, cors, router.
2. Note `transport_api_version`, cluster name, `failure_mode_allow`.

### 3. Baseline behavior

1. Request without credentials → expect deny.
2. Auth service kill → expect deny if fail-closed.
3. Measure p95 latency added by authz.

### 4. Configure ext_authz (illustrative)

```yaml
http_filters:
  - name: envoy.filters.http.ext_authz
    typed_config:
      "@type": type.googleapis.com/envoy.extensions.filters.http.ext_authz.v3.ExtAuthz
      transport_api_version: V3
      grpc_service:
        envoy_grpc:
          cluster_name: ext_authz
        timeout: 0.2s
      failure_mode_allow: false
      with_request_body:
        max_request_bytes: 8192
        allow_partial_message: true
      clear_route_cache: true
  - name: envoy.filters.http.router
    typed_config:
      "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router
```

1. Cluster `ext_authz` points to your auth service with TLS and outliers as needed.
2. Health/ready routes: `typed_per_filter_config` to disable ext_authz.
3. Strip hop-by-hop identity headers from downstream before auth (`x-user-*` spoofing).

### 5. Auth service contract

1. gRPC `Authorization/Check` → OK with optional header mutations, or Denied with body/status.
2. Propagate request id; log decision with reason code (no raw passwords).
3. Idempotent checks; careful with body buffering size.
4. Unit-test allow/deny matrix for roles and paths.

### 6. Verify with evidence

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://api.example.internal/v1/secret
curl -s -o /dev/null -w "%{http_code}\n" -H "Authorization: Bearer $TOKEN" https://api.example.internal/v1/secret
# Chaos: scale authz to 0 → still 403/503 not 200
```

1. Config dump shows filter present on intended listeners.
2. Metrics: `ext_authz.ok`, `ext_authz.denied`, `ext_authz.error`, latency histograms.
3. Confirm admin port not public.

### 7. Hand off

1. Runbook: authz errors, certificate expiry, timeout tuning.
2. Dashboards and alerts on error rate and fail-open config drift.
3. Code owners for auth service policy changes.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Failure mode | fail closed | `failure_mode_allow: true` on bank API |
| Headers | Server-set identity after check | Trust client `x-user-id` |
| Timeouts | 100–300ms with budget | 10s timeout stalls all traffic |
| Exceptions | Only `/healthz` | Entire API skipped |
| Admin | localhost / mTLS | 9901 on 0.0.0.0 public |

## Output Checklist

- [ ] Routes requiring auth listed
- [ ] ext_authz filter order and cluster correct
- [ ] failure_mode_allow false (or exception ticketed)
- [ ] Spoofable identity headers stripped
- [ ] Allow/deny and authz-down tests pass
- [ ] Metrics/alerts configured
- [ ] Admin interface exposure reviewed
- [ ] Residual risk noted

## Rules

- Owned gateways only.
- Default deny when authz unavailable for protected routes.
- Never log bearer tokens in clear text.
- Health checks must not require end-user auth in a way that kills the mesh.
- Outlier ejection for upstreams → `envoy-outlier-detection`.
