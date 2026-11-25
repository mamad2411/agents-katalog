---
name: cert-manager-tls-automation
description: >
  Guides installing and configuring cert-manager for automated TLS
  certificate issuance and renewal — Issuers vs. ClusterIssuers, ACME/
  Let's Encrypt HTTP-01 and DNS-01 challenges, private-CA issuance, and
  integration with Ingress-nginx and Istio gateways. Use when a user
  asks to "automate TLS certificates on Kubernetes," "set up
  cert-manager with Let's Encrypt," "fix a stuck Certificate that
  won't become Ready," "use DNS-01 for a wildcard cert," "rotate mTLS
  certs automatically," or "issue certs from an internal CA."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: kubernetes-platform
  maturity: stable
---

# cert-manager TLS Automation

## Purpose

cert-manager turns TLS certificate issuance and renewal into a
Kubernetes-native, declarative, continuously-reconciled process: a
`Certificate` resource describes desired state, and cert-manager's
controllers (a canonical example of the Operator/CRD/reconcile-loop
pattern) handle requesting, validating, and renewing the corresponding
Secret automatically. Without it, TLS certs are a manual renewal
process that reliably fails the same way — someone forgets, the cert
expires, and a production outage results from an entirely preventable
cause. This skill covers Issuer/ClusterIssuer setup, ACME challenge
types, private-CA issuance, and wiring automated certs into Ingress and
Istio.

## When to use

- Installing cert-manager on a cluster that currently has no automated
  TLS issuance (manually uploaded/renewed certs, or none at all).
- Choosing between an `Issuer` (namespace-scoped) and a `ClusterIssuer`
  (cluster-wide) for a given trust source.
- Setting up Let's Encrypt (or another ACME CA) issuance via HTTP-01 or
  DNS-01 challenges, including wildcard certificates (DNS-01 only).
- Issuing certificates from an internal/private CA instead of a public
  ACME CA, for internal-only services.
- Debugging a `Certificate` resource stuck `Ready: False` or a renewal
  that silently didn't happen before expiry.
- Wiring automated certificate issuance into an Ingress controller or a
  service mesh's gateway.

## Prerequisites & environment

- cert-manager ≥ 1.14 (CRD API is `cert-manager.io/v1`; older `v1alpha2`/
  `v1alpha3` API versions are long removed — confirm any inherited
  manifests use the current `v1` API group before applying to a current
  cert-manager install).
- Cluster-admin rights to install cert-manager's CRDs and its
  controller/webhook/cainjector components cluster-wide.
- For ACME/Let's Encrypt: a publicly resolvable DNS name and either port
  80 reachable for HTTP-01 (requires the Ingress/Service actually
  routing that path externally) or a supported DNS provider API
  credential for DNS-01 (needed for wildcard certs, since ACME's
  HTTP-01 challenge cannot validate a wildcard name).
- For a private CA: an existing internal CA's signing key/cert, or
  cert-manager's own self-signed/`CA` Issuer type for fully internal,
  non-public-trust use cases (internal mTLS, dev/test).
- An Ingress controller
  ([ingress-nginx-configuration](../ingress-nginx-configuration/SKILL.md))
  or service mesh gateway
  ([service-mesh-istio](../service-mesh-istio/SKILL.md)) already
  installed as the consumer of the issued certs, if the goal is
  end-to-end automated Ingress/gateway TLS rather than certs alone.

## Step-by-step guidance

1. **Install cert-manager** via its official Helm chart, including
   CRDs:
   ```bash
   helm repo add jetstack https://charts.jetstack.io
   helm repo update
   helm install cert-manager jetstack/cert-manager \
     --namespace cert-manager --create-namespace \
     --version v1.15.1 \
     --set crds.enabled=true
   kubectl get pods -n cert-manager   # controller, webhook, cainjector all Running
   ```

2. **Create a `ClusterIssuer` for Let's Encrypt via HTTP-01** (simplest
   setup, works for any single-hostname cert where the Ingress already
   routes the ACME solver path publicly):
   ```yaml
   apiVersion: cert-manager.io/v1
   kind: ClusterIssuer
   metadata:
     name: letsencrypt-prod
   spec:
     acme:
       server: https://acme-v02.api.letsencrypt.org/directory
       email: platform-team@example.com
       privateKeySecretRef: { name: letsencrypt-prod-account-key }
       solvers:
         - http01:
             ingress:
               ingressClassName: nginx
   ```
   Start against Let's Encrypt's **staging** endpoint
   (`https://acme-staging-v02.api.letsencrypt.org/directory`) while
   validating the setup, then switch to the production endpoint —
   Let's Encrypt's production ACME server enforces per-domain rate
   limits that a misconfigured test loop can exhaust for real.

3. **Use DNS-01 for wildcard certificates** or when port 80 isn't
   publicly reachable:
   ```yaml
   apiVersion: cert-manager.io/v1
   kind: ClusterIssuer
   metadata: { name: letsencrypt-dns }
   spec:
     acme:
       server: https://acme-v02.api.letsencrypt.org/directory
       email: platform-team@example.com
       privateKeySecretRef: { name: letsencrypt-dns-account-key }
       solvers:
         - dns01:
             route53:
               region: us-east-1
               hostedZoneID: <HOSTED_ZONE_ID>
           selector:
             dnsZones: ["example.com"]
   ```
   The credential cert-manager uses to call the DNS provider's API
   (an IAM role via IRSA on EKS, a service account key, etc.) should
   itself follow least-privilege workload-identity practice — see
   [managed-kubernetes-eks-aks-gke](../managed-kubernetes-eks-aks-gke/SKILL.md)
   for the IRSA/workload-identity setup pattern that should back this
   rather than a static DNS-provider API key mounted as a Secret.

4. **Request a certificate via Ingress annotation** (most common path —
   cert-manager watches Ingress resources and creates the `Certificate`
   automatically):
   ```yaml
   metadata:
     annotations:
       cert-manager.io/cluster-issuer: letsencrypt-prod
   spec:
     tls:
       - hosts: ["payments.example.com"]
         secretName: payments-example-com-tls
   ```
   Or create the `Certificate` resource directly for non-Ingress
   consumers (a Deployment mounting the Secret itself, a mesh gateway):
   ```yaml
   apiVersion: cert-manager.io/v1
   kind: Certificate
   metadata: { name: payments-example-com, namespace: payments }
   spec:
     secretName: payments-example-com-tls
     issuerRef: { name: letsencrypt-prod, kind: ClusterIssuer }
     dnsNames: ["payments.example.com"]
     duration: 2160h    # 90d
     renewBefore: 360h  # renew 15d before expiry
   ```

5. **Set up a private CA** for internal-only services that don't need
   public trust:
   ```yaml
   apiVersion: cert-manager.io/v1
   kind: Issuer
   metadata: { name: internal-ca, namespace: payments }
   spec:
     ca:
       secretName: internal-ca-key-pair   # pre-existing CA cert+key Secret
   ```
   For a fully self-managed root, cert-manager can also bootstrap a
   self-signed root and an intermediate `CA` Issuer chained from it —
   appropriate for internal mTLS where distributing a private CA's trust
   bundle to clients is feasible.

6. **Wire automated certs into Istio's ingress gateway** rather than
   Kubernetes Ingress, when the mesh's own gateway is the TLS
   termination point:
   ```yaml
   apiVersion: cert-manager.io/v1
   kind: Certificate
   metadata: { name: gateway-cert, namespace: istio-system }
   spec:
     secretName: gateway-cert-tls
     issuerRef: { name: letsencrypt-prod, kind: ClusterIssuer }
     dnsNames: ["payments.example.com"]
   ```
   ```yaml
   apiVersion: networking.istio.io/v1
   kind: Gateway
   metadata: { name: payments-gateway, namespace: istio-system }
   spec:
     servers:
       - port: { number: 443, name: https, protocol: HTTPS }
         tls: { mode: SIMPLE, credentialName: gateway-cert-tls }
         hosts: ["payments.example.com"]
   ```
   See [service-mesh-istio](../service-mesh-istio/SKILL.md) for the
   rest of the Gateway/VirtualService setup this depends on; note this
   automates the *gateway's* external TLS cert, separate from Istio's
   own internally-managed mTLS between sidecars.

7. **Verify issuance and renewal**:
   ```bash
   kubectl describe certificate payments-example-com -n payments
   kubectl get certificaterequests -n payments
   kubectl get order,challenge -n payments   # ACME-specific intermediate resources
   ```
   A healthy `Certificate` shows `Ready: True` with a `Reason` of
   `Issued`. cert-manager renews automatically starting at
   `renewBefore` prior to expiry — verify this actually happened over
   time (`kubectl get secret <name> -o jsonpath='{.metadata.annotations}'`
   shows the last-renewed timestamp) rather than assuming the
   `renewBefore` config guarantees it silently worked.

## Best practices

- Always validate a new Issuer/ClusterIssuer configuration against
  Let's Encrypt's staging endpoint first — production ACME rate limits
  (per-registered-domain certificates per week) are not generous enough
  to absorb a misconfigured retry loop while debugging.
- Prefer DNS-01 over HTTP-01 whenever the DNS provider is already
  automatable and a wildcard cert would reduce the number of
  certificates managed — one wildcard `*.apps.example.com` certificate
  is simpler to reason about than dozens of per-host certs, at the cost
  of a slightly larger blast radius if that single private key is ever
  compromised.
- Scope `ClusterIssuer` DNS-01 credentials (IAM role, service account)
  to only the specific hosted zone(s) cert-manager needs to write
  `TXT` records to — not broader DNS-zone or account-wide permissions.
- Set `renewBefore` with real margin (the common default renews at 2/3
  of certificate lifetime; for Let's Encrypt's 90-day certs, renewing
  15–30 days before expiry gives room to notice and fix a stuck renewal
  before it becomes a live outage).
- Monitor `Certificate` resources for `Ready: False` as a first-class
  alert, not just certificate-expiry monitoring on the resulting Secret
  — catching a stuck challenge days before expiry is far cheaper than
  reacting to an already-expired cert.
- Use namespace-scoped `Issuer`s (not a cluster-wide `ClusterIssuer`)
  when different teams/namespaces should use different trust sources or
  when a namespace's issuer credentials shouldn't be usable
  cluster-wide.

## Common pitfalls

- **Symptom:** A `Certificate` stays `Ready: False` indefinitely, and
  `kubectl get challenge` shows a challenge stuck in a pending/error
  state.
  **Fix:** For HTTP-01, confirm the Ingress controller is actually
  routing `/.well-known/acme-challenge/...` externally (a restrictive
  NetworkPolicy, WAF rule, or auth-requiring Ingress annotation can
  block the solver path) — cert-manager creates a temporary Ingress/Pod
  for the challenge, but anything blocking traffic to it upstream will
  still cause a failure. For DNS-01, confirm the credential used
  actually has write access to the specific hosted zone referenced.

- **Symptom:** A wildcard certificate request fails immediately, citing
  an unsupported challenge type.
  **Fix:** ACME's HTTP-01 challenge cannot validate a wildcard domain by
  protocol design — wildcard certs require DNS-01. Switch the Issuer's
  solver configuration (or add a second solver selected by
  `dnsZones`/`dnsNames` match) rather than trying to force HTTP-01 for a
  `*.example.com` request.

- **Symptom:** Let's Encrypt issuance suddenly starts failing cluster-
  wide with a rate-limit error.
  **Fix:** Production ACME rate limits (per registered domain, per
  week) were exhausted, usually by a misconfigured retry loop hitting
  production instead of staging during setup/debugging, or by issuing
  many near-duplicate certs (one per subdomain) instead of a single
  wildcard. Switch to the staging endpoint for any further debugging,
  and consolidate to a wildcard cert where the number of hostnames
  makes per-host certs impractical.

- **Symptom:** A `Certificate` shows `Ready: True` but the actual
  Ingress/Gateway serving traffic still presents an old or self-signed
  certificate.
  **Fix:** Confirm the Ingress/Gateway resource references the exact
  `secretName` the `Certificate` writes to, and that it lives in the
  same namespace (Secrets are not automatically synced across
  namespaces) — a mismatched or stale `secretName` reference silently
  leaves the consumer serving whatever cert it already had.

- **Symptom:** Deleting a `Certificate` resource (or its namespace)
  unexpectedly also removes the TLS Secret in use by a live Ingress.
  **Fix:** By default cert-manager's Certificate controls the
  lifecycle of its target Secret's *content* (rotating it on renewal)
  but does not delete the Secret on `Certificate` deletion unless
  garbage-collection/owner-reference cleanup is configured to do so in
  your version/settings — regardless, > **Warning:** deleting a
  `Certificate` or its namespace on a resource actively serving
  production traffic is a availability-impacting action; confirm no
  live Ingress/Gateway still references that Secret first, and prefer
  updating/replacing the `Certificate` over deleting it.

## Worked example

**Scenario:** Issue a Let's Encrypt certificate for
`payments.example.com` via DNS-01 (Route 53), validate against staging
first, then cut over to production and wire it into the existing
`payments-api` Ingress.

```yaml
# staging ClusterIssuer for validation
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata: { name: letsencrypt-staging }
spec:
  acme:
    server: https://acme-staging-v02.api.letsencrypt.org/directory
    email: platform-team@example.com
    privateKeySecretRef: { name: letsencrypt-staging-account-key }
    solvers:
      - dns01:
          route53: { region: us-east-1, hostedZoneID: <HOSTED_ZONE_ID> }
        selector: { dnsZones: ["example.com"] }
```

```bash
kubectl apply -f staging-issuer.yaml
kubectl patch ingress payments-api -n payments --type merge \
  -p '{"metadata":{"annotations":{"cert-manager.io/cluster-issuer":"letsencrypt-staging"}}}'
kubectl describe certificate payments-example-com-tls -n payments
```

Once `Ready: True` is confirmed against staging (the browser will show
an untrusted staging-CA cert — this is expected), cut over to
production:

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata: { name: letsencrypt-prod }
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: platform-team@example.com
    privateKeySecretRef: { name: letsencrypt-prod-account-key }
    solvers:
      - dns01:
          route53: { region: us-east-1, hostedZoneID: <HOSTED_ZONE_ID> }
        selector: { dnsZones: ["example.com"] }
```

```bash
kubectl apply -f prod-issuer.yaml
kubectl patch ingress payments-api -n payments --type merge \
  -p '{"metadata":{"annotations":{"cert-manager.io/cluster-issuer":"letsencrypt-prod"}}}'
kubectl delete certificate payments-example-com-tls -n payments   # forces re-issuance against prod issuer
kubectl describe certificate payments-example-com-tls -n payments
curl -vI https://payments.example.com 2>&1 | grep -i "issuer"
```

The final `curl` shows a certificate issued by `Let's Encrypt` (not the
staging CA), and `kubectl get certificate payments-example-com-tls -n
payments -o jsonpath='{.status.renewalTime}'` confirms cert-manager has
scheduled automatic renewal well ahead of the 90-day expiry — no manual
renewal step required going forward.

## Cross-references

- [ingress-nginx-configuration](../ingress-nginx-configuration/SKILL.md) — the Ingress annotation-driven certificate request flow shown above.
- [service-mesh-istio](../service-mesh-istio/SKILL.md) — wiring an automated certificate into an Istio Gateway for mesh-ingress TLS termination.
- [kubernetes-operator-development](../kubernetes-operator-development/SKILL.md) — cert-manager itself as a real-world reference implementation of the CRD + controller + finalizer reconciliation pattern.
