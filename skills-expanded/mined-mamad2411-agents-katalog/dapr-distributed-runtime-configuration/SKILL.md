---
name: dapr-distributed-runtime-configuration
description: >
  Configures Dapr's sidecar building blocks — state management, pub/sub,
  and service invocation — for polyglot microservices, including
  component YAML, sidecar annotations, and resiliency policies. Use
  when the user asks to "add a Dapr state store component," "set up
  Dapr pub/sub between services," "call another service via Dapr
  service invocation," "configure a Dapr sidecar for a Kubernetes
  deployment," or "add retry/circuit-breaker resiliency to a Dapr
  building block."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: serverless-and-alternative-compute
  maturity: stable
---

# Dapr Distributed Runtime Configuration

## Purpose

Dapr (Distributed Application Runtime) runs as a **sidecar** alongside
each service instance, exposing language-agnostic HTTP/gRPC APIs for
building blocks like state management, publish/subscribe messaging, and
service-to-service invocation — so a polyglot fleet of services (Go,
Python, Java, Node) gets consistent, swappable infrastructure
integrations (Redis today, a different state store tomorrow) without
each service embedding its own client library and retry logic per
backend. The value is in the abstraction and the operational
consistency it buys across languages; getting component scoping,
resiliency policies, and sidecar resource sizing wrong undermines both.
Validating these configurations before deploy is covered separately in
[dapr-configuration-validation](../dapr-configuration-validation/SKILL.md).

## When to use

- Adding a new state store, pub/sub broker, or binding component to a
  Dapr-enabled application.
- Wiring service-to-service calls through Dapr's service invocation
  building block instead of direct HTTP/gRPC client code.
- Configuring retry, timeout, and circuit-breaker resiliency policies
  for a specific component or service.
- Scoping which applications can access which Dapr components in a
  shared Kubernetes namespace or cluster.
- Deciding whether a given integration belongs in application code,
  behind a Dapr building block, or as a native Kubernetes/cloud-provider
  integration instead.

## Prerequisites & environment

- Dapr control plane installed on the target Kubernetes cluster (or
  Dapr's self-hosted mode for local/non-Kubernetes development), with a
  version whose component API version (`v1alpha1`, `v1`) matches what's
  used in component manifests — component spec fields have changed
  across Dapr major versions, so check the installed `dapr --version`
  against the manifests being authored, and confirm a matching Dapr
  sidecar image is pulled/available in the cluster's container
  registry.
- `dapr` CLI for local development/testing (`dapr run`) and
  `kubectl` for inspecting sidecar injection and component status on
  Kubernetes.
- A backing service for each building block in use (Redis, Kafka,
  a cloud provider's managed queue/state store, etc.) already
  provisioned — Dapr components are configuration pointing at real
  infrastructure, not infrastructure themselves.
- Application code updated to call Dapr's HTTP/gRPC API (via a
  language SDK or raw HTTP) rather than a backend-specific client
  library, for the services being migrated onto Dapr building blocks.

## Step-by-step guidance

1. **Enable sidecar injection per Deployment via annotations**, not
   cluster-wide — Dapr sidecars are opt-in per pod:
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: order-service
     namespace: prod
   spec:
     template:
       metadata:
         annotations:
           dapr.io/enabled: "true"
           dapr.io/app-id: "order-service"
           dapr.io/app-port: "8080"
           dapr.io/config: "tracing-config"
       spec:
         containers:
           - name: order-service
             image: registry.example.com/order-service:2.3.0
   ```
   `dapr.io/app-id` is the stable identifier other services use to call
   this one via service invocation — treat it as a public API surface
   name, not an implementation detail that changes casually.

2. **Define a state store component scoped to specific applications**,
   not accessible cluster-wide by default:
   ```yaml
   apiVersion: dapr.io/v1alpha1
   kind: Component
   metadata:
     name: orders-statestore
     namespace: prod
   spec:
     type: state.redis
     version: v1
     metadata:
       - name: redisHost
         value: "orders-redis.prod.svc.cluster.local:6379"
       - name: redisPassword
         secretKeyRef:
           name: orders-redis-secret
           key: password
   scopes:
     - order-service
     - order-fulfillment-service
   ```
   `spec.metadata[].secretKeyRef` pulls the password from a Kubernetes
   `Secret` rather than embedding it in the component manifest — never
   put a real credential value directly in `spec.metadata`.
   `scopes` restricts which `app-id`s may use this component at all;
   omitting `scopes` makes the component usable by every Dapr-enabled
   app in the namespace, which is rarely the intent for anything
   holding sensitive state.

3. **Define a pub/sub component the same way**, scoped and with secrets
   referenced rather than embedded:
   ```yaml
   apiVersion: dapr.io/v1alpha1
   kind: Component
   metadata:
     name: orders-pubsub
     namespace: prod
   spec:
     type: pubsub.kafka
     version: v1
     metadata:
       - name: brokers
         value: "kafka-broker.prod.svc.cluster.local:9092"
       - name: authType
         value: "password"
       - name: saslUsername
         secretKeyRef:
           name: orders-kafka-secret
           key: username
       - name: saslPassword
         secretKeyRef:
           name: orders-kafka-secret
           key: password
   scopes:
     - order-service
     - order-fulfillment-service
     - analytics-ingest-service
   ```
   Publish/subscribe from application code then targets this component
   by name (`orders-pubsub`), not a broker connection string, so
   swapping the backing broker later means changing this manifest, not
   every service's code.

4. **Use service invocation for direct service-to-service calls**,
   getting mTLS, retries, and (with the control plane's built-in
   tracing) distributed tracing for free, rather than each service
   implementing its own HTTP client resiliency:
   ```bash
   curl -X POST http://localhost:3500/v1.0/invoke/order-fulfillment-service/method/fulfill \
     -H "Content-Type: application/json" \
     -d '{"orderId": "<ORDER_ID>"}'
   ```
   The call goes to the local sidecar (`localhost:3500` in this
   example's Dapr HTTP port), which resolves `order-fulfillment-service`
   via the configured name resolution component (Kubernetes DNS
   resolution is the default on Kubernetes) and forwards the request
   over mTLS to that service's own sidecar.

5. **Attach a resiliency policy scoped to specific components/apps**,
   not a single global policy applied blindly everywhere:
   ```yaml
   apiVersion: dapr.io/v1alpha1
   kind: Resiliency
   metadata:
     name: order-service-resiliency
     namespace: prod
   spec:
     policies:
       retries:
         retryForever:
           policy: exponential
           maxInterval: 15s
           maxRetries: 5
       circuitBreakers:
         cbStateStore:
           maxRequests: 1
           interval: 30s
           timeout: 20s
           trip: consecutiveFailures >= 5
     targets:
       components:
         orders-statestore:
           outbound:
             retry: retryForever
             circuitBreaker: cbStateStore
       apps:
         order-fulfillment-service:
           retry: retryForever
   ```
   Different components/targets warrant different policies — a state
   store call and a call to a flaky third-party-backed binding rarely
   need the same retry/circuit-breaker tuning.

6. **Size the sidecar's own resource requests/limits deliberately** —
   the sidecar container consumes cluster resources on every pod it's
   injected into, and an under-sized sidecar becomes a request-path
   bottleneck invisible in the application's own metrics:
   ```yaml
   annotations:
     dapr.io/sidecar-cpu-request: "100m"
     dapr.io/sidecar-cpu-limit: "500m"
     dapr.io/sidecar-memory-request: "128Mi"
     dapr.io/sidecar-memory-limit: "256Mi"
   ```

## Best practices

- Scope every component (`scopes:`) to the specific `app-id`s that
  actually need it — an unscoped component is reachable by any
  Dapr-enabled app in the namespace, which is rarely the intended
  blast radius for anything holding state or credentials.
- Reference secrets via `secretKeyRef` (backed by Kubernetes Secrets or
  a dedicated Dapr secret store component such as Vault) in every
  component manifest — never inline a credential value directly under
  `spec.metadata`.
- Attach resiliency policies per component/app pairing based on that
  specific dependency's real failure characteristics, not one
  copy-pasted policy applied uniformly to every target.
- Treat `app-id` as a stable public identifier once other services
  depend on it via service invocation — renaming it breaks every
  caller's invocation URL.
- Size and monitor the sidecar container's own resource usage and
  latency contribution, not just the application container's — a
  starved sidecar adds latency to every building-block call the
  application makes.
- Use a dedicated Dapr secret store component (Vault, cloud KMS-backed
  secret managers) rather than Kubernetes Secrets alone when the
  organization already has a centralized secrets management standard
  elsewhere.

## Common pitfalls

- **Symptom:** A newly deployed component (state store, pub/sub) is
  usable by an application that has no legitimate reason to touch it,
  discovered during a security review.
  **Fix:** The component manifest omitted `scopes`, making it available
  to every Dapr-enabled app in the namespace by default; add explicit
  `scopes` listing only the intended `app-id`s and redeploy.

- **Symptom:** A component manifest committed to source control
  contains a plaintext database password or broker credential.
  **Fix:** Replace the inline `value` field with `secretKeyRef` pointing
  at a Kubernetes `Secret` (or a Dapr secret store component), remove
  the plaintext value from git history, and rotate the exposed
  credential.

- **Symptom:** Service invocation calls between two services succeed
  most of the time but occasionally hang for the full request timeout
  during a downstream blip, dragging down the calling service's own
  latency.
  **Fix:** No resiliency policy (retry/timeout/circuit breaker) was
  attached to that target; add a `Resiliency` policy scoped to the
  specific app or component with a bounded timeout and a circuit
  breaker so a downstream blip fails fast instead of holding every
  caller's request open.

- **Symptom:** After renaming a service's Dapr `app-id` as part of a
  refactor, other services suddenly can't reach it via service
  invocation.
  **Fix:** `app-id` is the stable address other services invoke by
  name; treat it the same as a DNS name or public API contract — update
  every caller's invocation target as part of the same change, or keep
  the old `app-id` as an alias if the platform supports it, rather than
  renaming it as an isolated change.

- **Symptom:** Application-level latency metrics look fine, but
  end-to-end request latency (as seen by clients) is noticeably higher
  than the application's own numbers suggest.
  **Fix:** The Dapr sidecar's own resource limits are likely too tight
  (CPU-throttled sidecar adds latency to every building-block call);
  check sidecar CPU throttling metrics specifically and raise
  `dapr.io/sidecar-cpu-limit` if the sidecar is being throttled under
  load.

## Worked example

**Scenario:** An `order-service` needs to persist order state to Redis,
publish an `order.created` event to Kafka for downstream consumers, and
call a separate `order-fulfillment-service` directly — all with
sensible resiliency and least-privilege component scoping.

Deployment annotations enabling the sidecar:
```yaml
metadata:
  annotations:
    dapr.io/enabled: "true"
    dapr.io/app-id: "order-service"
    dapr.io/app-port: "8080"
    dapr.io/sidecar-cpu-request: "100m"
    dapr.io/sidecar-cpu-limit: "500m"
```

State store, scoped to only the two services that need order state:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: orders-statestore
  namespace: prod
spec:
  type: state.redis
  version: v1
  metadata:
    - name: redisHost
      value: "orders-redis.prod.svc.cluster.local:6379"
    - name: redisPassword
      secretKeyRef:
        name: orders-redis-secret
        key: password
scopes: [order-service, order-fulfillment-service]
```

Pub/sub component, scoped to publisher and both consumers:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: orders-pubsub
  namespace: prod
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    - name: brokers
      value: "kafka-broker.prod.svc.cluster.local:9092"
scopes: [order-service, order-fulfillment-service, analytics-ingest-service]
```

Application code (pseudocode, language-agnostic Dapr HTTP calls):
```
PUT  http://localhost:3500/v1.0/state/orders-statestore
POST http://localhost:3500/v1.0/publish/orders-pubsub/order.created
POST http://localhost:3500/v1.0/invoke/order-fulfillment-service/method/fulfill
```

A `Resiliency` policy bounds the fulfillment call so a slow
fulfillment-service instance doesn't stall order-service requests
indefinitely:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Resiliency
metadata:
  name: order-service-resiliency
  namespace: prod
spec:
  policies:
    timeouts:
      fulfillmentCallTimeout: 5s
    circuitBreakers:
      cbFulfillment:
        maxRequests: 1
        interval: 30s
        timeout: 20s
        trip: consecutiveFailures >= 5
  targets:
    apps:
      order-fulfillment-service:
        timeout: fulfillmentCallTimeout
        circuitBreaker: cbFulfillment
```
With this in place, a fulfillment-service outage trips the circuit
breaker after five consecutive failures, and order-service's calls fail
fast (bounded by the 5s timeout) instead of piling up waiting on a
downstream that isn't responding.

## Cross-references

- [dapr-configuration-validation](../dapr-configuration-validation/SKILL.md) — pre-deploy validation for the component scoping, secret references, and resiliency policies shown here.
- [knative-eventing-configuration](../knative-eventing-configuration/SKILL.md) — Knative's Broker/Trigger model as an alternative event-routing approach to Dapr's pub/sub building block.
- [azure-functions-configuration](../azure-functions-configuration/SKILL.md) — Azure Functions' Dapr extension lets triggers/bindings target these same Dapr building blocks from a FaaS platform instead of a long-running sidecar-attached service.
