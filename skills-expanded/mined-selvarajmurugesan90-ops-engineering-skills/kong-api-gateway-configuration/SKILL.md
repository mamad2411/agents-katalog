---
name: kong-api-gateway-configuration
description: >
  Configures Kong Gateway's core objects — Services, Routes, and
  Plugins — including rate-limiting, authentication (key-auth, JWT,
  OAuth2), and request/response transformation, in both declarative
  (`kong.yml`) and imperative (Admin API) modes, on Kubernetes (via the
  Kong Ingress Controller) or standalone. Use when a user asks to "add
  a Kong Route/Service," "attach a rate-limiting or auth plugin to a
  Kong route," "write a KongPlugin/KongIngress CRD," "set up Kong as an
  API gateway," "configure Kong declaratively with kong.yml," or
  "troubleshoot a 502 from Kong to an upstream."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: service-mesh-and-api-gateway
  maturity: stable
---

# Kong API Gateway Configuration

## Purpose

Kong models an API gateway as three composable objects: a **Service**
(the upstream, defined once), one or more **Routes** (how traffic
reaches that Service — host/path/method matching), and **Plugins**
(cross-cutting behavior — auth, rate-limiting, transformation,
logging — attached to a Service, a Route, a Consumer, or globally).
Getting the attachment level of a plugin wrong is the single most
common source of "it works for one route but not another" confusion:
a plugin on a Service applies to every Route pointing at it, a plugin
on a Route applies only there, and a global plugin applies everywhere
including routes you didn't intend. This skill covers building this
object model — declaratively via `kong.yml`/CRDs (the reproducible,
GitOps-friendly path) or imperatively via the Admin API — and the
plugin configurations most teams reach for first: rate-limiting and
authentication. Validating that a declarative config or CRD set is
correct before deploy is a distinct, deeper topic — see
[kong-configuration-validation](../kong-configuration-validation/SKILL.md).

## When to use

- Standing up Kong as the front door for a new API, or adding a new
  upstream Service/Route to an existing Kong deployment.
- Attaching a rate-limiting plugin (`rate-limiting` or
  `rate-limiting-advanced`) to a Route, Service, or Consumer.
- Adding authentication (`key-auth`, `jwt`, `oauth2`, `basic-auth`) in
  front of an upstream that doesn't do its own auth.
- Configuring request/response transformation (`request-transformer`,
  `response-transformer`) to adapt a client's expected payload shape to
  what the upstream actually returns, or vice versa.
- Migrating a hand-run set of `curl` calls against the Admin API into a
  declarative `kong.yml` file or Kubernetes CRDs for reproducibility.
- Diagnosing a `502 Bad Gateway`/`503 Service Unavailable` from Kong, or
  a plugin that isn't firing on the route it's expected to.
- Deciding whether Kong (an API gateway focused on north-south,
  edge-facing traffic) or a service mesh (east-west, service-to-service)
  is the right tool for a specific traffic-management need — see
  [service-mesh-istio](../../../kubernetes-platform/skills/service-mesh-istio/SKILL.md)
  for the mesh side of that comparison.

## Prerequisites & environment

- Kong Gateway (OSS or Enterprise) installed — standalone (Docker/VM,
  fronted by a Postgres or Cassandra datastore, or in DB-less mode) or
  on Kubernetes via the **Kong Ingress Controller (KIC)**, which maps
  Kong's Service/Route/Plugin model onto Kubernetes `Ingress` +
  `KongPlugin`/`KongClusterPlugin`/`KongIngress` CRDs.
  `rate-limiting-advanced`, some auth plugins' more advanced modes, and
  clustering/Vitals dashboards differ between OSS and Enterprise — check
  which tier a given plugin belongs to before assuming it's available.
- Network access to Kong's Admin API (default port `8001`, `8444` for
  TLS) for imperative configuration or CI-driven declarative sync — this
  API has no auth by default in many install profiles, so it must never
  be exposed outside a trusted network without an access-control layer
  in front of it.
- For DB-less/declarative mode: `deck` (decK), Kong's CLI for diffing
  and syncing `kong.yml` against a running Kong instance
  (`deck sync`, `deck diff`, `deck validate`).
- For Kubernetes: the Kong Ingress Controller installed and its CRDs
  (`KongPlugin`, `KongClusterPlugin`, `KongIngress`, `KongConsumer`)
  registered, plus a standard Kubernetes `Ingress` resource per route (or
  Kong's native `HTTPRoute`/Gateway API support on newer KIC versions).
- A rate-limiting plugin backed by a shared store (Redis) rather than
  the in-memory `local` policy for any multi-node Kong deployment — the
  default `local` policy counts independently per node, which silently
  multiplies the effective limit by the node count.

## Step-by-step guidance

1. **Define the Service and Route as the base object model**, either
   imperatively:
   ```bash
   curl -i -X POST http://localhost:8001/services \
     --data name=payments-api \
     --data url=http://payments-api.internal:8080

   curl -i -X POST http://localhost:8001/services/payments-api/routes \
     --data name=payments-api-route \
     --data 'paths[]=/v1/payments' \
     --data 'methods[]=GET' \
     --data 'methods[]=POST'
   ```
   or declaratively in `kong.yml` (the reproducible, diffable path —
   prefer this over ad hoc `curl` calls for anything beyond local
   experimentation):
   ```yaml
   _format_version: "3.0"
   services:
     - name: payments-api
       url: http://payments-api.internal:8080
       routes:
         - name: payments-api-route
           paths: ["/v1/payments"]
           methods: ["GET", "POST"]
   ```

2. **On Kubernetes, express the same model as an `Ingress` plus Kong
   CRDs**, with the Kong Ingress Controller reconciling them into the
   equivalent Service/Route:
   ```yaml
   apiVersion: networking.k8s.io/v1
   kind: Ingress
   metadata:
     name: payments-api
     annotations:
       konghq.com/strip-path: "true"
   spec:
     ingressClassName: kong
     rules:
       - http:
           paths:
             - path: /v1/payments
               pathType: Prefix
               backend:
                 service:
                   name: payments-api
                   port:
                     number: 8080
   ```

3. **Attach authentication before exposing an upstream that doesn't
   handle it itself.** `key-auth` is the simplest starting point:
   ```bash
   curl -i -X POST http://localhost:8001/services/payments-api/plugins \
     --data name=key-auth \
     --data config.key_names=apikey
   curl -i -X POST http://localhost:8001/consumers \
     --data username=checkout-service
   curl -i -X POST http://localhost:8001/consumers/checkout-service/key-auth \
     --data key='<CONSUMER_API_KEY>'
   ```
   For token-based auth between services, prefer `jwt` (Kong validates
   a signature/claims without a round trip to an auth server) or
   `oauth2` (full authorization-code/client-credentials flows) over
   `key-auth` for anything beyond simple machine-to-machine calls with
   low rotation needs — a static API key is easy to leak and hard to
   rotate without a client-visible change.

4. **Attach rate-limiting, choosing the attachment level deliberately**
   — Service-level for a blanket limit on an upstream, Route-level for
   a specific endpoint, Consumer-level for a per-client limit:
   ```yaml
   plugins:
     - name: rate-limiting
       service: payments-api
       config:
         minute: 100
         policy: redis
         redis:
           host: redis.internal
           port: 6379
   ```
   The `policy: redis` (or `cluster` for OSS's DB-backed cluster
   counter) is important on any multi-node Kong deployment — the
   default `local` policy counts per-node, so a "100 requests/minute"
   limit becomes effectively `100 * node_count` per minute cluster-wide,
   which is rarely the intended behavior. See
   [api-gateway-rate-limiting-and-quota-management](../api-gateway-rate-limiting-and-quota-management/SKILL.md)
   for the deeper strategy (token bucket vs. sliding window, per-client
   vs. global) behind this configuration.

5. **Add request/response transformation only where the client and
   upstream contracts genuinely differ**, since every transformation is
   an extra thing to keep in sync as either side changes:
   ```yaml
   plugins:
     - name: request-transformer
       route: payments-api-route
       config:
         add:
           headers: ["x-forwarded-service:checkout"]
         remove:
           headers: ["x-internal-debug"]
   ```

6. **Set explicit upstream health checks and timeouts** on the Service,
   rather than relying on Kong's defaults, so a slow or unhealthy
   upstream fails fast instead of piling up connections:
   ```yaml
   services:
     - name: payments-api
       url: http://payments-api.internal:8080
       connect_timeout: 3000
       read_timeout: 10000
       retries: 2
   ```

7. **Sync declarative config with `deck`** rather than hand-editing a
   running Kong instance, so changes are diffable and reviewable before
   they land:
   ```bash
   deck diff --kong-addr http://localhost:8001 -s kong.yml
   deck sync --kong-addr http://localhost:8001 -s kong.yml
   ```
   `deck diff` shows exactly what will change before `deck sync` applies
   it — treat an unreviewed `deck sync` straight to production the same
   way you'd treat an unreviewed `terraform apply`.

8. **Lock down the Admin API** before this configuration is
   production-facing — it defaults to no authentication on many install
   paths:
   ```bash
   curl -i -X POST http://localhost:8001/services/admin-api/plugins \
     --data name=key-auth
   ```
   or, more commonly, bind the Admin API to a private network/VPN only
   and never expose port `8001`/`8444` on a public listener at all.

## Best practices

- Model plugin attachment level deliberately: Service-level for
  behavior every Route on that Service should get, Route-level for a
  single endpoint's exception, Consumer-level for per-client behavior,
  and global only for something that must apply everywhere (e.g.
  a security header) — an accidental global plugin is a common source
  of "why did this break every route" incidents.
- Manage Kong configuration declaratively (`kong.yml` + `deck`, or
  Kubernetes CRDs in Git) rather than a history of imperative `curl`
  calls against the Admin API — the latter has no diff, no review, and
  no record of who changed what.
- Always back rate-limiting with a shared counter (`redis` or
  `cluster` policy) in any multi-node deployment; `local` silently
  changes the effective limit based on node count.
- Prefer `jwt`/`oauth2` over `key-auth` for anything beyond simple,
  low-rotation machine-to-machine calls — static API keys are hard to
  rotate without a client-visible change and easy to leak in logs/URLs
  if passed as a query parameter instead of a header.
- Set explicit `connect_timeout`/`read_timeout`/`retries` per Service
  rather than relying on Kong's defaults, which are generic and not
  tuned to your upstream's actual latency profile.
- Never expose the Admin API on a public listener without an
  authentication plugin or network-level restriction in front of it —
  it has full control over every Service, Route, Plugin, and Consumer.
- For north-south, edge-facing traffic (client → API), Kong is the
  right layer; for east-west, service-to-service traffic inside a
  cluster, a service mesh's sidecar/ambient model is usually a better
  fit — see
  [service-mesh-istio](../../../kubernetes-platform/skills/service-mesh-istio/SKILL.md)
  and
  [linkerd-service-mesh-configuration](../linkerd-service-mesh-configuration/SKILL.md)
  for that comparison rather than trying to make Kong do both jobs.

## Common pitfalls

- **Symptom:** A rate-limiting plugin configured for "100 requests per
  minute" allows noticeably more than 100 requests per minute in
  production.
  **Fix:** The plugin is very likely using the default `local` counting
  policy on a multi-node Kong deployment, which counts independently per
  node. Switch to `policy: redis` (or `cluster`) so the limit is
  enforced against a shared counter across all nodes.

- **Symptom:** A plugin attached to a Service doesn't seem to affect one
  specific Route the way it does the others.
  **Fix:** Check for a Route-level plugin of the same type overriding
  or duplicating the Service-level one — Kong evaluates plugins at
  every applicable level (global, Service, Route, Consumer) and a
  Route-level instance of the same plugin type takes precedence over
  the Service-level one for that Route, which is easy to forget when a
  Route-level override was added months earlier for a one-off reason.

- **Symptom:** Requests intermittently return `502 Bad Gateway` under
  load that the upstream itself isn't logging as failing.
  **Fix:** Check the Service's `connect_timeout`/`read_timeout` and
  `retries` settings against the upstream's actual latency profile under
  load — Kong's defaults are generic, and an upstream that's simply
  slower than the default `read_timeout` under load produces a Kong-side
  502/504 the upstream never sees as an error on its own end.

- **Symptom:** The Admin API is reachable from outside the cluster/VPC,
  discovered during a security review, months after initial setup.
  **Fix:** This is a critical exposure — the Admin API has unauthenticated
  full control over every Service, Route, Plugin, and Consumer by
  default on many install profiles. Restrict it to a private
  network/VPN immediately, or, if it must be reachable more broadly, put
  a `key-auth`/mTLS plugin in front of it rather than leaving it open
  "because it was only meant to be temporary."

- **Symptom:** A `key-auth` API key is committed to a config repo or
  shows up in access logs because a client passes it as a query
  parameter.
  **Fix:** Configure `key-auth` to only accept the key via header
  (`config.key_in_header: true`, `config.key_in_query: false`), store
  the actual key value in a secret manager rather than the declarative
  config file, and rotate any key found in logs or version control
  immediately rather than treating the exposure as low-risk because
  "it's just an API key."

## Worked example

**Scenario:** Expose `payments-api` through Kong at `/v1/payments`,
requiring a `key-auth` API key per consumer, rate-limited to 100
requests/minute per consumer backed by Redis, with a 3s connect timeout
and 2 retries to the upstream.

```yaml
_format_version: "3.0"
services:
  - name: payments-api
    url: http://payments-api.internal:8080
    connect_timeout: 3000
    read_timeout: 10000
    retries: 2
    routes:
      - name: payments-api-route
        paths: ["/v1/payments"]
        methods: ["GET", "POST"]
    plugins:
      - name: key-auth
        config:
          key_names: ["apikey"]
          key_in_header: true
          key_in_query: false
      - name: rate-limiting
        config:
          minute: 100
          policy: redis
          redis:
            host: redis.internal
            port: 6379
          limit_by: consumer

consumers:
  - username: checkout-service
    keyauth_credentials:
      - key: "${CHECKOUT_SERVICE_API_KEY}"
```

```bash
deck diff --kong-addr http://localhost:8001 -s kong.yml
deck sync --kong-addr http://localhost:8001 -s kong.yml

curl -i http://localhost:8000/v1/payments -H "apikey: ${CHECKOUT_SERVICE_API_KEY}"
# expect: 200 (or the upstream's real response) once under the limit,
# 429 Too Many Requests once the consumer exceeds 100/minute
```

The `${CHECKOUT_SERVICE_API_KEY}` placeholder is resolved from a secret
manager at deploy time, never checked into the `kong.yml` committed to
version control. Before this reaches production,
[kong-configuration-validation](../kong-configuration-validation/SKILL.md)
covers confirming the declarative config actually applies as intended
and the rate limit is enforced against the shared Redis counter, not a
per-node one.

## Cross-references

- [kong-configuration-validation](../kong-configuration-validation/SKILL.md) — validating this declarative config/CRD set before it reaches production.
- [api-gateway-rate-limiting-and-quota-management](../api-gateway-rate-limiting-and-quota-management/SKILL.md) — the deeper, cross-tool strategy (algorithm choice, per-client vs. global scoping) behind the `rate-limiting` plugin configuration here.
- [apigee-api-management-and-governance](../apigee-api-management-and-governance/SKILL.md) — the enterprise API-management alternative when the need grows beyond gateway routing/plugins into full lifecycle governance, monetization, and versioning at scale.
- [service-mesh-istio](../../../kubernetes-platform/skills/service-mesh-istio/SKILL.md) — the service-mesh comparison point for east-west traffic, versus Kong's north-south, edge-facing role.
