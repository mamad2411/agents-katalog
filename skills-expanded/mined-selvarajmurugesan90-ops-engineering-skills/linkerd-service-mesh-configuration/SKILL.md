---
name: linkerd-service-mesh-configuration
description: >
  Guides installing and operating Linkerd as a simpler, mTLS-first
  alternative to Istio — choosing extensions deliberately, enabling
  automatic mutual TLS with zero-config identity, injecting the proxy
  per namespace/workload, and splitting traffic between service
  versions. Use when a user asks to "install Linkerd," "why choose
  Linkerd over Istio," "enable mTLS in Linkerd" (it's on by default —
  explain when it isn't), "set up a canary/traffic split in Linkerd,"
  "inject the Linkerd proxy," or "reduce service mesh overhead versus
  Istio."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: service-mesh-and-api-gateway
  maturity: stable
---

# Linkerd Service Mesh Configuration

## Purpose

Linkerd's design goal is the opposite of "configure everything explicitly":
mutual TLS between meshed workloads is on by default with zero
configuration, the proxy (`linkerd2-proxy`, written in Rust) is
deliberately minimal compared to Envoy, and the control plane ships as a
small set of independently-installable **extensions** (`viz`, `multicluster`,
`jaeger`) rather than one monolithic install. That simplicity is the
point — teams that don't need Istio's full traffic-management surface
(request-level routing rules, WASM plugins, complex L7 policy) but do
need mesh-wide mTLS and basic traffic splitting often get there faster
and with less to operate on Linkerd. This skill covers installing
Linkerd deliberately, understanding what mTLS "automatic" actually means
and when it isn't in effect, and configuring traffic splits for canary
rollouts. Validating the result before it reaches production is a
separate, deeper topic — see
[linkerd-configuration-validation](../linkerd-configuration-validation/SKILL.md).

## When to use

- Deciding whether Linkerd's smaller feature surface and lower resource
  footprint fit better than Istio for a mesh whose only real
  requirements are mTLS and basic canary routing.
- Installing Linkerd's control plane and choosing which extensions
  (`viz` for metrics/dashboard, `multicluster` for cross-cluster mesh,
  `jaeger` for tracing) are actually needed versus installed by default.
- Explaining why two meshed pods are (or aren't) already using mTLS, and
  what causes plaintext traffic to slip through.
- Setting up a canary/traffic-split rollout between two versions of a
  service using weighted routing.
- Injecting the Linkerd proxy into a namespace or individual workload,
  and diagnosing why an existing pod didn't pick up the sidecar.
- A user is comparing Linkerd against Istio for a new mesh deployment,
  or migrating an existing Istio mesh to Linkerd (or vice versa).

## Prerequisites & environment

- The `linkerd` CLI installed locally, matching (or within one minor
  version of) the control plane version you intend to run — check with
  `linkerd version` before installing.
- A Kubernetes cluster meeting Linkerd's minimum supported Kubernetes
  version for your chosen Linkerd release (check the release's install
  docs; Linkerd tracks a rolling window of recent Kubernetes minor
  versions, not every version indefinitely).
- Cluster-admin access to install CRDs (`linkerd install --crds`) before
  the control plane itself — recent Linkerd versions split CRD
  installation from control-plane installation into two explicit steps.
- Trust anchor and issuer certificates for the identity system. For a
  first install, `linkerd install` can generate a self-signed trust
  anchor; for production, generate your own trust anchor and issuer
  certificate/key pair (e.g. with `step` or `cert-manager`) so identity
  material isn't tied to a single `linkerd install` invocation and can be
  rotated independently.
- Decide up front whether you need the `viz` extension (Prometheus +
  Grafana + web dashboard) — it's the primary way to see mTLS status and
  traffic metrics, so most production installs want it, but it adds
  components worth being deliberate about.

## Step-by-step guidance

1. **Install CRDs, then the control plane, as separate steps**, and
   verify each before moving to the next:
   ```bash
   linkerd install --crds | kubectl apply -f -
   linkerd install | kubectl apply -f -
   linkerd check
   ```
   `linkerd check` validates the control plane is healthy, certificates
   are valid and not expiring soon, and the API is reachable — treat a
   failing `linkerd check` as a blocker, not a warning.

2. **Install the `viz` extension** if you need metrics, the dashboard, or
   `linkerd viz stat`/`tap` for day-to-day operation:
   ```bash
   linkerd viz install | kubectl apply -f -
   linkerd viz check
   linkerd viz dashboard &
   ```

3. **Provide your own trust anchor and issuer certs in production**
   rather than the auto-generated self-signed default, so identity
   material can be rotated without reinstalling the control plane:
   ```bash
   linkerd install \
     --identity-trust-anchors-file ca.crt \
     --identity-issuer-certificate-file issuer.crt \
     --identity-issuer-key-file issuer.key \
     | kubectl apply -f -
   ```
   The issuer certificate has a limited validity window (Linkerd rotates
   the leaf identity certs it issues to workloads automatically, but the
   issuer cert itself needs its own rotation plan — `linkerd check` warns
   when it's approaching expiry).

4. **Enable proxy injection per namespace**, not cluster-wide, so rollout
   stays deliberate and reversible per team:
   ```bash
   kubectl annotate namespace payments linkerd.io/inject=enabled
   ```
   As with any mesh, labeling/annotating a namespace only affects *new*
   pod admissions through the injector webhook — existing pods need a
   rollout to actually get the proxy container:
   ```bash
   kubectl rollout restart deployment -n payments
   ```
   To inject a single workload instead of a whole namespace, annotate the
   pod template directly (`spec.template.metadata.annotations`) with the
   same `linkerd.io/inject: enabled` key.

5. **Understand what "automatic mTLS" actually covers.** Once both sides
   of a connection are meshed (have a `linkerd-proxy` container), traffic
   between them is mTLS-encrypted with per-pod identity automatically —
   there is no `PeerAuthentication`-equivalent resource to write for the
   common case. What it does *not* cover: traffic to/from anything not
   proxied — an unmeshed pod, a cron `Job` without injection, an external
   caller hitting a `NodePort`/pod IP directly, or traffic that opts out
   via `config.linkerd.io/skip-outbound-ports` / `skip-inbound-ports`
   annotations (commonly set for non-HTTP protocols the proxy can't
   transparently handle). Check `linkerd viz edges` to see which meshed
   pairs are actually using mTLS and which aren't.

6. **Configure traffic splitting for a canary rollout.** Two mechanisms
   exist depending on your Linkerd version: the original SMI
   `TrafficSplit` CRD, and newer Gateway API `HTTPRoute`-based weighted
   routing that recent Linkerd releases favor going forward — check your
   installed version's docs for which is current, since this has been
   moving. `TrafficSplit` example:
   ```yaml
   apiVersion: split.smi-spec.io/v1alpha2
   kind: TrafficSplit
   metadata:
     name: payments-api-canary
     namespace: payments
   spec:
     service: payments-api
     backends:
       - service: payments-api-v1
         weight: 900
       - service: payments-api-v2
         weight: 100
   ```
   `TrafficSplit` requires a root Service (`payments-api`) and two backend
   Services (`payments-api-v1`, `payments-api-v2`) that already exist and
   select the respective pod versions — Linkerd doesn't create those
   Services for you.

7. **Add per-route retries and timeouts** via `ServiceProfile`, Linkerd's
   equivalent of Istio's `VirtualService` HTTP rules, generated from
   OpenAPI specs or protobuf definitions where available:
   ```yaml
   apiVersion: linkerd.io/v1alpha2
   kind: ServiceProfile
   metadata:
     name: payments-api.payments.svc.cluster.local
     namespace: payments
   spec:
     routes:
       - name: GET /charges/{id}
         condition:
           method: GET
           pathRegex: /charges/[^/]+
         timeout: 3s
         isRetryable: true
   ```
   Retries are opt-in per route (`isRetryable: true`) precisely so a
   non-idempotent write route doesn't get silently retried.

8. **Restrict which callers can reach a workload** with the
   `policy.linkerd.io` `Server` and `AuthorizationPolicy` resources —
   Linkerd's mesh-native authorization layer, separate from mTLS itself
   (mTLS provides *identity*; these resources provide *authorization*
   based on that identity):
   ```yaml
   apiVersion: policy.linkerd.io/v1beta3
   kind: Server
   metadata:
     name: payments-api
     namespace: payments
   spec:
     podSelector:
       matchLabels: { app: payments-api }
     port: 8080
   ---
   apiVersion: policy.linkerd.io/v1beta3
   kind: AuthorizationPolicy
   metadata:
     name: payments-api-callers
     namespace: payments
   spec:
     targetRef:
       group: policy.linkerd.io
       kind: Server
       name: payments-api
     requiredAuthenticationRefs:
       - group: policy.linkerd.io
         kind: MeshTLSAuthentication
         name: checkout-service-identity
   ```

## Best practices

- Provide production trust anchors/issuer certs explicitly rather than
  the auto-generated self-signed default — a self-signed CA that lives
  only inside a single `linkerd install` invocation has no rotation
  story and no external record of what's trusted.
- Install extensions (`viz`, `multicluster`, `jaeger`) only when there's
  a concrete need — each is a separate set of components with its own
  upgrade and resource footprint, and Linkerd's whole value proposition
  is staying smaller than the alternative.
- Use `linkerd viz edges` regularly (not just once at install time) to
  confirm which connections are actually mTLS-secured — a workload added
  later without injection silently falls back to plaintext for its
  connections rather than failing loudly.
- Keep `isRetryable` opt-in and scoped to genuinely idempotent routes in
  `ServiceProfile` — blanket retries on write endpoints can double-charge
  or double-process under transient failures.
- Treat the issuer certificate's expiry like any other production
  certificate — monitor `linkerd check`'s expiry warnings and rotate
  before, not after, expiry causes new identity issuance to fail
  mesh-wide.
- When comparing against Istio for a new deployment, weigh Linkerd's
  narrower feature set explicitly: no built-in WASM extensibility, a
  smaller (though evolving) set of L7 traffic-management primitives, and
  the once-stable `TrafficSplit` CRD's ongoing migration toward Gateway
  API — see
  [service-mesh-istio](../../../kubernetes-platform/skills/service-mesh-istio/SKILL.md)
  for the equivalent Istio concepts if a side-by-side comparison is
  needed.

## Common pitfalls

- **Symptom:** Two pods that both show a `linkerd-proxy` container still
  exchange plaintext traffic per `linkerd viz edges`.
  **Fix:** One side is likely opting a port out via
  `config.linkerd.io/skip-inbound-ports` or `skip-outbound-ports`
  (common for non-HTTP protocols like raw TCP database connections that
  need protocol detection tuning), or one pod predates injection and
  hasn't been restarted. Confirm both pods' proxy identity and check the
  skip-port annotations before assuming a bug.

- **Symptom:** `linkerd check` reports the identity issuer certificate
  is expiring soon, and it's ignored as a low-priority warning.
  **Fix:** Treat it as a hard deadline, not a warning to defer — once the
  issuer cert actually expires, the identity service can't issue new
  leaf certificates, and every pod that gets rescheduled or restarts
  after that point fails to establish mTLS and can't join the mesh.
  Rotate proactively via `linkerd upgrade
  --identity-issuer-certificate-file/--identity-issuer-key-file` well
  before the warning becomes an outage.

- **Symptom:** A namespace was annotated `linkerd.io/inject=enabled` but
  a `kubectl get pods` shows only one container per pod, no
  `linkerd-proxy`.
  **Fix:** The annotation only affects pods created *after* it's applied,
  through the mutating webhook — existing pods must be recreated
  (`kubectl rollout restart deployment -n <ns>`) to actually get injected.

- **Symptom:** A `TrafficSplit` is applied but 100% of traffic keeps
  going to the original backend regardless of the configured weights.
  **Fix:** `TrafficSplit` only affects traffic sent to the *root* Service
  name (`payments-api` in the example above) — callers that hardcode or
  resolve the `v1` backend Service name directly bypass the split
  entirely. Confirm every caller actually targets the root Service, not
  a version-specific one.

- **Symptom:** Debugging a connectivity failure, someone temporarily
  disables mTLS enforcement or removes an `AuthorizationPolicy` to "just
  get it working," and it's never re-added.
  **Fix:** This is a real security regression, not a harmless debugging
  step — removing an `AuthorizationPolicy` or unmeshing a workload to
  bypass identity checks should be done on a scratch/non-production
  namespace, tracked with an explicit follow-up to revert, and never
  landed as a "fix" for a connectivity issue that was actually caused by
  something else (a missing `Server` selector, a stale certificate).

## Worked example

**Scenario:** Canary `payments-api` v2 at 10% traffic behind automatic
mTLS in the `payments` namespace, with only `checkout-service` authorized
to call it.

```bash
linkerd install --crds | kubectl apply -f -
linkerd install \
  --identity-trust-anchors-file ca.crt \
  --identity-issuer-certificate-file issuer.crt \
  --identity-issuer-key-file issuer.key \
  | kubectl apply -f -
linkerd check
linkerd viz install | kubectl apply -f -

kubectl annotate namespace payments linkerd.io/inject=enabled
kubectl rollout restart deployment -n payments
```

```yaml
apiVersion: split.smi-spec.io/v1alpha2
kind: TrafficSplit
metadata:
  name: payments-api-canary
  namespace: payments
spec:
  service: payments-api
  backends:
    - service: payments-api-v1
      weight: 900
    - service: payments-api-v2
      weight: 100
---
apiVersion: policy.linkerd.io/v1beta3
kind: Server
metadata:
  name: payments-api
  namespace: payments
spec:
  podSelector:
    matchLabels: { app: payments-api }
  port: 8080
---
apiVersion: policy.linkerd.io/v1beta3
kind: AuthorizationPolicy
metadata:
  name: payments-api-callers
  namespace: payments
spec:
  targetRef:
    group: policy.linkerd.io
    kind: Server
    name: payments-api
  requiredAuthenticationRefs:
    - group: policy.linkerd.io
      kind: MeshTLSAuthentication
      name: checkout-service-identity
```

```bash
kubectl apply -f canary.yaml
linkerd viz edges deployment -n payments
linkerd viz stat trafficsplit -n payments
```

`linkerd viz edges` confirms `checkout-service` → `payments-api-v1`/`v2`
connections are `tls: true` with the expected client/server identities,
and `linkerd viz stat` shows the ~90/10 traffic split and per-version
success rate before shifting weight further. Before this rollout ships,
run it through
[linkerd-configuration-validation](../linkerd-configuration-validation/SKILL.md)
to check injection and policy correctness ahead of time rather than
discovering a gap live.

## Cross-references

- [linkerd-configuration-validation](../linkerd-configuration-validation/SKILL.md) — validating proxy injection and traffic policy correctness before this configuration reaches production.
- [consul-service-mesh-and-discovery-configuration](../consul-service-mesh-and-discovery-configuration/SKILL.md) — an alternative mesh with a stronger multi-cloud/hybrid service-discovery story, useful when comparing options.
- [grpc-service-troubleshooting](../grpc-service-troubleshooting/SKILL.md) — diagnosing gRPC-specific failures on top of a meshed connection, which look different from the HTTP/1.1 failure modes this skill mostly covers.
- [service-mesh-istio](../../../kubernetes-platform/skills/service-mesh-istio/SKILL.md) — the more feature-rich alternative mesh; consult when a comparison or migration between the two is needed.
