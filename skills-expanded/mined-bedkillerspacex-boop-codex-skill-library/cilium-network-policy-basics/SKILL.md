---
name: cilium-network-policy-basics
description: >
  Author and validate Cilium NetworkPolicy / CiliumClusterwideNetworkPolicy for L3/L4,
  L7 HTTP, and DNS: endpoint selectors, ingress/egress, toFQDNs, and Hubble evidence.
  Use on owned Cilium clusters (EKS/GKE/self-managed) when default-deny, microsegmentation,
  or identity-aware policies are required — not generic Kubernetes NetworkPolicy alone
  when Cilium CRDs and Hubble are the control plane.
---

# Cilium Network Policy Basics

## Scope And Authorization

- **In scope:** clusters you own or operate under written authorization; lab/CTF clusters.
- **Out of scope:** applying deny-all or probing policies on third-party clusters; disabling cluster security for convenience.
- Prefer staging / canary namespaces before clusterwide default-deny.
- Redact pod IPs, service accounts, and internal DNS from tickets when not needed.
- Pair YAML/Helm changes with `code-quality-standards`.

## When To Use

- Writing or reviewing **CiliumNetworkPolicy** / **CiliumClusterwideNetworkPolicy**.
- Moving from Kubernetes `NetworkPolicy` to Cilium L7 (HTTP methods/paths) or **toFQDNs** DNS policy.
- Debugging “policy dropped” with Hubble / `cilium policy get`.
- Tokens: cilium, CNP, CCNP, identity, L3/L4/L7, DNS, Hubble, endpoint selector.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Generic K8s NetworkPolicy only (no Cilium) | cluster CNI docs / platform skill |
| TLS plaintext / mTLS app design | `tls-plaintext-acquisition` / service-mesh skill |
| QUIC/HTTP3 path analysis | `quic-http3-analysis` |
| Implementation quality baseline | `code-quality-standards` |
| Secrets rotation | `secrets-management-hygiene` |
| Host firewall outside cluster | OS/network ops skill |

## Domain Concepts

| Concept | Notes |
| --- | --- |
| Endpoint identity | Cilium labels + security identity; prefer labels over raw IPs |
| CNP vs CCNP | Namespace-scoped vs clusterwide; default-deny often CCNP + namespace exceptions |
| L3/L4 | `fromEndpoints` / `toEndpoints` / `toCIDR` / ports/protocols |
| L7 HTTP | `http` rules: method, path, headers (requires L7 proxy) |
| DNS | `toFQDNs` + `toPorts` DNS; pair with egress allow for resolved IPs |
| Host policies | Separate from pod CNP; careful on control-plane nodes |

## Workflow

### 1. Confirm scope and success criteria

1. Cluster name, Cilium version (`cilium version`), Hubble enabled, owner, change window.
2. Success: required flows work; unauthorized cross-namespace/egress denied; drops visible in Hubble.
3. Rollback: previous CNP/CCNP YAML + `kubectl apply`; know how to temporarily widen policy if locked out of DNS.

### 2. Inventory identities and flows

```bash
kubectl get cnp,ccnp -A
cilium status
cilium endpoint list
hubble observe --namespace app --last 50
```

1. Map workloads by **labels** that will appear in `endpointSelector`.
2. List required egress (in-cluster services, FQDNs, CIDRs) and ingress callers.
3. Note existing K8s NetworkPolicy that may stack with Cilium.

### 3. Baseline before tighten

1. Capture allow-all behavior: sample Hubble flows for critical paths (login, payment, DNS).
2. Export current policies: `kubectl get cnp,ccnp -A -o yaml > backup-policies.yaml`.
3. Confirm DNS path works under current policy (`nslookup` from a debug pod).

### 4. Author policies (smallest reversible step)

**L3/L4 example (same-namespace allow from frontend):**

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: backend-ingress
  namespace: app
spec:
  endpointSelector:
    matchLabels:
      app: backend
  ingress:
    - fromEndpoints:
        - matchLabels:
            app: frontend
      toPorts:
        - ports:
            - port: "8080"
              protocol: TCP
```

**L7 HTTP (method/path):**

```yaml
# under toPorts entry
rules:
  http:
    - method: "GET"
      path: "/healthz"
    - method: "POST"
      path: "/api/v1/.*"
```

**DNS / FQDN egress:**

```yaml
egress:
  - toEndpoints:
      - matchLabels:
          k8s:io.kubernetes.pod.namespace: kube-system
          k8s:k8s-app: kube-dns
    toPorts:
      - ports:
          - port: "53"
            protocol: UDP
        rules:
          dns:
            - matchPattern: "*"
  - toFQDNs:
      - matchName: "api.partner.example"
    toPorts:
      - ports:
          - port: "443"
            protocol: TCP
```

1. Prefer **default-deny egress** per namespace after DNS + required FQDNs/CIDRs are listed.
2. Avoid `toEntities: all` except documented break-glass with expiry.
3. Do not put secrets in annotations; keep policy pure connectivity.

### 5. Verify with evidence

```bash
kubectl apply -f policy.yaml
cilium policy get
hubble observe --verdict DROPPED --namespace app -f
# From a test pod:
curl -sS -o /dev /null -w "%{http_code}\n" http://backend.app.svc:8080/healthz
# Expect deny from wrong label / wrong path
```

1. Prove **allow** for intended callers and **drop** for others (Hubble verdict).
2. After FQDN rules, confirm DNS proxy and TLS to partner still succeed.
3. Regression: cluster DNS, metrics scrapers, and operators that need cross-namespace access.

### 6. Observe and harden

1. Alert on sustained DROPPED for production namespaces (false-positive policy).
2. Review Hubble UI / metrics for policy map pressure after large L7 rules.
3. Document exceptions (CI runners, bastion) with owner and review date.

### 7. Hand off

1. Store policies in GitOps; link PR to change ticket.
2. Runbook: “locked out of DNS” recovery and who can apply CCNP.
3. Apply `code-quality-standards` to any automation that generates CNP.

## Policy Design Table

| Goal | Prefer | Avoid |
| --- | --- | --- |
| Microseg same cluster | `fromEndpoints` labels | Wide `toCIDR: 0.0.0.0/0` |
| SaaS API egress | `toFQDNs` + DNS rules | Hard-coded CDN IPs only |
| Health checks | Explicit path allow | Open all methods on port |
| Multi-tenant | Per-namespace CNP + minimal CCNP | One clusterwide allow-all |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Selectors | Stable app labels | Temporary pod names |
| Default deny | Staged namespace by namespace | Instant clusterwide lockout |
| L7 | Allowlist methods/paths | Regex that matches everything |
| Evidence | Hubble DROPPED/ALLOWED | “kubectl apply succeeded” |
| Break-glass | Ticket + expiry | Permanent `toEntities: world` |

## Output Checklist

- [ ] Cluster/Cilium/Hubble version and owner recorded
- [ ] Label inventory and required flows documented
- [ ] Policy backup taken before tighten
- [ ] CNP/CCNP applied for intended L3/L4/L7/DNS
- [ ] Allow + deny cases verified with Hubble or equivalent
- [ ] DNS and critical egress still work
- [ ] Exceptions have owner + review date
- [ ] GitOps/runbook updated; secrets not in policy YAML
- [ ] Residual risk noted (e.g. host network pods)

## Rules

- Authorized clusters only; never use policy drops to harass multi-tenant neighbors.
- Evidence (Hubble verdicts, curl codes) over assumptions about CNI behavior.
- Prefer reversible GitOps applies; keep emergency widen path documented.
- Focus this skill on Cilium policy authoring and validation; route mesh mTLS, generic K8s, and host firewall elsewhere.
- Never paste live cluster tokens or private FQDN inventories into public notes.
