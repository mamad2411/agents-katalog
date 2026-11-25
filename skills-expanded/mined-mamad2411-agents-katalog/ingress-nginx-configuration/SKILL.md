---
name: ingress-nginx-configuration
description: >
  Guides installing and configuring the NGINX Ingress Controller —
  install methods, per-Ingress annotations, TLS termination, rate
  limiting, path-based/host-based routing, and troubleshooting. Use
  when a user asks to "install nginx ingress controller," "route
  traffic to a Kubernetes service by path or host," "terminate TLS at
  the ingress," "rate limit an endpoint," "fix a 502/504 from
  ingress-nginx," or "configure a canary/header-based ingress split."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: kubernetes-platform
  maturity: stable
---

# NGINX Ingress Controller Configuration

## Purpose

`ingress-nginx` is the most widely deployed way to get HTTP(S) traffic
from outside a cluster to Services inside it, translating the
Kubernetes `Ingress` resource into a running NGINX configuration. Most
production incidents with it are configuration-shaped, not NGINX bugs:
missing TLS secrets, annotation typos that silently no-op, rate limits
set too aggressively for real traffic, or body-size limits that reject
legitimate uploads. This skill covers installing it correctly and
configuring routing, TLS, and traffic controls in a way that fails
loudly instead of silently.

## When to use

- Installing `ingress-nginx` on a cluster that doesn't yet have an
  Ingress controller (many managed clusters ship none by default).
- Writing or reviewing an `Ingress` resource for path-based or
  host-based routing to one or more backend Services.
- Terminating TLS at the ingress (single cert, SNI-based multi-host, or
  wildcard) and wiring it to cert-manager for automated issuance.
- Adding rate limiting, connection limiting, or request body size limits
  per Ingress/path.
- Debugging `502`/`504`/`413`/`495` errors surfaced by the controller.
- Setting up canary routing (header-, weight-, or cookie-based) via
  `ingress-nginx`'s canary annotations, as an alternative to a full
  service mesh for simple north-south splits.

## Prerequisites & environment

- `ingress-nginx` ≥ 1.10 (tracks Kubernetes ≥ 1.29; check the project's
  support matrix — the controller drops support for older Kubernetes
  minor versions on a rolling basis, and running a controller version
  outside its supported Kubernetes range risks undocumented webhook/API
  incompatibilities).
- A way to get external traffic to the controller: a cloud
  `LoadBalancer` Service (managed clusters), `NodePort` + external LB,
  or `hostNetwork`/`hostPort` for bare-metal without a cloud LB — decide
  this before install since it changes the Helm values used.
- `helm` ≥ 3.14 (installed via the official `ingress-nginx` chart) or
  the static manifest install method — prefer Helm for upgrade
  tracking. See [helm-chart-authoring](../helm-chart-authoring/SKILL.md)
  for general chart-management practices that apply to operating this
  chart long-term.
- cert-manager installed if TLS certificates are to be issued/renewed
  automatically rather than manually maintained — see
  [cert-manager-tls-automation](../cert-manager-tls-automation/SKILL.md).
- Cluster admin rights to install the `IngressClass` resource and the
  controller's RBAC/webhook configuration cluster-wide.

## Step-by-step guidance

1. **Install via Helm**, choosing the exposure method for your
   environment:
   ```bash
   helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
   helm repo update
   helm install ingress-nginx ingress-nginx/ingress-nginx \
     --namespace ingress-nginx --create-namespace \
     --set controller.service.type=LoadBalancer \
     --set controller.ingressClassResource.name=nginx \
     --set controller.ingressClassResource.default=true
   ```
   On bare-metal without a cloud load balancer, use
   `--set controller.hostNetwork=true --set controller.kind=DaemonSet`
   (or pair with MetalLB) instead of `LoadBalancer`, which will otherwise
   stay `<pending>` forever.

2. **Confirm the controller is healthy and has an external address**:
   ```bash
   kubectl get pods -n ingress-nginx
   kubectl get svc -n ingress-nginx ingress-nginx-controller
   ```

3. **Write a basic host+path routed Ingress**:
   ```yaml
   apiVersion: networking.k8s.io/v1
   kind: Ingress
   metadata:
     name: payments-api
     namespace: payments
     annotations:
       nginx.ingress.kubernetes.io/rewrite-target: /
   spec:
     ingressClassName: nginx
     rules:
       - host: payments.example.com
         http:
           paths:
             - path: /api(/|$)(.*)
               pathType: ImplementationSpecific
               backend:
                 service:
                   name: payments-api
                   port: { number: 80 }
   ```
   Always set `ingressClassName` explicitly rather than relying on a
   cluster default — an explicit class survives a future second
   controller being installed without silently re-routing existing
   Ingresses.

4. **Terminate TLS** by referencing a Secret of type
   `kubernetes.io/tls`, ideally issued by cert-manager rather than
   manually maintained:
   ```yaml
   spec:
     tls:
       - hosts: ["payments.example.com"]
         secretName: payments-example-com-tls
   ```
   ```yaml
   # cert-manager annotation to auto-provision the above secret
   metadata:
     annotations:
       cert-manager.io/cluster-issuer: letsencrypt-prod
   ```
   See [cert-manager-tls-automation](../cert-manager-tls-automation/SKILL.md)
   for the Issuer/ClusterIssuer setup this depends on.

5. **Add rate limiting** per Ingress (enforced per NGINX worker process,
   not cluster-wide, so effective limits scale with replica count):
   ```yaml
   metadata:
     annotations:
       nginx.ingress.kubernetes.io/limit-rps: "20"
       nginx.ingress.kubernetes.io/limit-burst-multiplier: "3"
   ```

6. **Adjust body size / timeouts** for endpoints outside the defaults
   (default max body size is 1m; default proxy timeouts are 60s):
   ```yaml
   metadata:
     annotations:
       nginx.ingress.kubernetes.io/proxy-body-size: "25m"
       nginx.ingress.kubernetes.io/proxy-read-timeout: "120"
       nginx.ingress.kubernetes.io/proxy-send-timeout: "120"
   ```

7. **Set up canary routing** for a simple weighted or header-based
   split without a full mesh:
   ```yaml
   metadata:
     name: payments-api-canary
     annotations:
       nginx.ingress.kubernetes.io/canary: "true"
       nginx.ingress.kubernetes.io/canary-weight: "10"
   spec:
     ingressClassName: nginx
     rules:
       - host: payments.example.com
         http:
           paths:
             - path: /
               pathType: Prefix
               backend:
                 service: { name: payments-api-v2, port: { number: 80 } }
   ```
   The canary Ingress must have the same host/path as the primary
   Ingress it's canarying against; `ingress-nginx` merges them at the
   NGINX config level.

8. **Validate and reload safely**: the controller watches Ingress
   objects and reloads NGINX config automatically; verify a specific
   change took effect by inspecting the generated config rather than
   assuming the apply succeeded:
   ```bash
   kubectl exec -n ingress-nginx deploy/ingress-nginx-controller -- \
     cat /etc/nginx/nginx.conf | grep -A5 'server_name payments.example.com'
   ```

9. **Check controller logs and events for merge conflicts** when
   multiple Ingress resources target overlapping host/path
   combinations — `ingress-nginx` picks one deterministically but will
   emit a warning event, not fail the apply:
   ```bash
   kubectl get events -n payments --field-selector reason=Sync
   ```

## Best practices

- Set `ingressClassName` on every Ingress explicitly; never depend on
  "there's only one controller so it must be the default" — clusters
  commonly grow a second controller (an internal-only class) later.
- Terminate TLS via cert-manager-issued secrets rather than manually
  uploaded certs, so renewal isn't a manual, easy-to-forget task — see
  [cert-manager-tls-automation](../cert-manager-tls-automation/SKILL.md).
- Treat annotation typos as a silent-failure risk: `ingress-nginx`
  ignores unrecognized annotation keys rather than rejecting the
  resource, so a misspelled `nginx.ingress.kubernetes.io/` annotation
  simply does nothing instead of erroring — verify effect via the
  generated NGINX config or observed behavior, not just "the apply
  succeeded."
- Set resource requests/limits and run at least 2 controller replicas
  with `PodDisruptionBudget` — the Ingress controller is a single point
  of failure for all external traffic if under-provisioned or singly
  scheduled.
- Prefer `pathType: Exact` or `Prefix` over `ImplementationSpecific`
  regex paths where the routing logic doesn't need it — regex paths are
  harder to reason about and easier to accidentally make overly broad.
- For high-traffic rate limiting that needs to be accurate across
  replicas (not per-worker-process), consider whether ingress-nginx's
  per-replica limiting is precise enough, or whether the limit belongs
  at an upstream layer (API gateway, CDN, WAF) instead.

## Common pitfalls

- **Symptom:** Ingress applies successfully but traffic still 404s or
  hits the wrong backend.
  **Fix:** Check for another Ingress claiming the same host with a
  conflicting/overlapping path — `ingress-nginx` merges all Ingresses
  for a host into one NGINX server block and resolves conflicts by an
  internal precedence rule (exact path match, then longest prefix),
  which often isn't the rule the author assumed. List all Ingresses for
  the host (`kubectl get ingress -A | grep <host>`) before debugging
  further.

- **Symptom:** Uploads or large POST bodies fail with `413 Request
  Entity Too Large`.
  **Fix:** Default `proxy-body-size` is 1m. Set
  `nginx.ingress.kubernetes.io/proxy-body-size` explicitly on the
  Ingress for endpoints that need larger payloads, rather than raising
  the controller-wide default for every route.

- **Symptom:** Long-running requests intermittently fail with `504
  Gateway Timeout` under load, but work fine in isolation.
  **Fix:** Default proxy read/send timeouts are 60s. Either the backend
  is genuinely too slow for the client's needs (fix the backend), or a
  legitimately long operation needs
  `proxy-read-timeout`/`proxy-send-timeout` raised per-Ingress —
  distinguish the two before just raising timeouts everywhere, since a
  raised timeout also delays failure detection for a genuinely hung
  backend.

- **Symptom:** TLS termination fails with a certificate/hostname
  mismatch error even though the Ingress's `tls.secretName` looks
  correct.
  **Fix:** Confirm the Secret actually exists in the *same namespace* as
  the Ingress (TLS secrets are not shared across namespaces without an
  explicit sync mechanism) and that cert-manager's `Certificate`
  resource, if used, has reached `Ready: True` — a still-pending
  challenge silently leaves the old/self-signed default certificate in
  place, which the controller serves without erroring.

- **Symptom:** After changing an annotation (e.g. `limit-rps`),
  behavior doesn't change at all.
  **Fix:** Confirm the annotation key/namespace prefix is exactly
  correct (`nginx.ingress.kubernetes.io/...`) — a typo or wrong prefix
  is silently ignored rather than rejected, since Kubernetes annotations
  are free-form strings with no schema validation. Grep the rendered
  NGINX config for the expected directive to confirm it actually applied.

## Worked example

**Scenario:** Route `payments.example.com/api` to `payments-api`,
terminate TLS via cert-manager, rate-limit to 20 req/s, and allow 10MB
uploads.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: payments-api
  namespace: payments
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/limit-rps: "20"
    nginx.ingress.kubernetes.io/limit-burst-multiplier: "3"
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
    nginx.ingress.kubernetes.io/rewrite-target: /$2
spec:
  ingressClassName: nginx
  tls:
    - hosts: ["payments.example.com"]
      secretName: payments-example-com-tls
  rules:
    - host: payments.example.com
      http:
        paths:
          - path: /api(/|$)(.*)
            pathType: ImplementationSpecific
            backend:
              service:
                name: payments-api
                port: { number: 80 }
```

```bash
kubectl apply -f payments-api-ingress.yaml
kubectl get certificate -n payments payments-example-com-tls -w   # wait for Ready: True
curl -I https://payments.example.com/api/health
```

A successful `curl` returns `HTTP/2 200` with a certificate issued by
Let's Encrypt (verify with `openssl s_client -connect
payments.example.com:443 -servername payments.example.com | openssl
x509 -noout -issuer`), confirming both routing and automated TLS are
working end to end.

## Cross-references

- [cert-manager-tls-automation](../cert-manager-tls-automation/SKILL.md) — the Issuer/ClusterIssuer setup that automatically provisions the TLS secrets referenced above.
- [service-mesh-istio](../service-mesh-istio/SKILL.md) — when north-south routing needs mTLS, richer traffic-shaping, or east-west policy beyond what ingress-nginx alone provides.
- [kustomize-overlay-management](../kustomize-overlay-management/SKILL.md) — patching per-environment Ingress hosts/annotations without duplicating the whole resource.
