---
name: cilium-ebpf-cni-and-mesh-configuration
description: >
  Configures Cilium as an eBPF-based Kubernetes CNI — kube-proxy
  replacement, CiliumNetworkPolicy for L3/L4/L7 network policy, and
  Cilium's ambient-style service mesh capability built on the same
  eBPF datapath rather than per-pod sidecars. Use when a user asks to
  "install Cilium," "replace kube-proxy with Cilium," "write a
  CiliumNetworkPolicy," "compare Cilium's sidecar-less mesh to Istio
  ambient or Linkerd," "reduce per-pod proxy overhead with eBPF," or
  "troubleshoot Cilium connectivity after install."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: service-mesh-and-api-gateway
  maturity: stable
---

# Cilium eBPF CNI and Mesh Configuration

## Purpose

Cilium sits at a different layer than the other meshes in this domain:
it's first a **CNI plugin** — the thing actually wiring up pod
networking — built on eBPF programs attached to the kernel's networking
hooks instead of iptables rules, which is what lets it also replace
kube-proxy's `Service` load-balancing and implement L3/L4/L7 network
policy without per-pod sidecar proxies for most of that functionality.
Its newer service-mesh capability builds on the same eBPF datapath (plus
Envoy for L7 cases that need it) rather than injecting a sidecar into
every pod, which is the core trade-off to understand versus
sidecar-based meshes: less per-pod overhead and simpler operations for
policy and L4 routing, at the cost of a feature set that's less mature
for complex L7 traffic management than Istio or a sidecar-based mesh.
This skill covers installing Cilium, enabling kube-proxy replacement,
writing `CiliumNetworkPolicy`, and using its mesh capability where
warranted. Validating policy and observability configuration before
production is a separate, deeper topic — see
[cilium-configuration-validation](../cilium-configuration-validation/SKILL.md).

## When to use

- Choosing or installing a CNI and deciding whether Cilium's eBPF
  datapath and kube-proxy replacement are worth adopting over a simpler
  CNI plus a separate mesh.
- Replacing kube-proxy with Cilium's eBPF-based `Service`
  implementation for lower per-packet overhead at scale.
- Writing `CiliumNetworkPolicy` for L3/L4 (IP/port) or L7 (HTTP
  method/path, DNS, Kafka topic) traffic restriction.
- Evaluating Cilium's sidecar-less mesh capability as an alternative to
  a sidecar-based mesh (Istio, Linkerd, Consul Connect) when the primary
  driver is reducing per-pod proxy overhead.
- Setting up Hubble for flow-level network observability.
- Debugging connectivity that broke after installing or upgrading
  Cilium, or after enabling kube-proxy replacement specifically.

## Prerequisites & environment

- A Linux kernel version new enough for the eBPF features you intend to
  use — check Cilium's own compatibility matrix for your target Cilium
  release rather than assuming any kernel works; kube-proxy replacement
  and some L7 features have stricter minimum kernel requirements than
  basic connectivity.
- The `cilium` CLI (separate from `kubectl`) for install, status, and
  connectivity testing: `cilium install`, `cilium status`, `cilium
  connectivity test`.
- A cluster with no CNI already installed (Cilium is typically the CNI,
  not a layer on top of one), or a clear migration plan if replacing an
  existing CNI on a live cluster — CNI migration on a running cluster is
  disruptive and needs a maintenance window, not a live rolling change.
- If enabling kube-proxy replacement: confirm whether kube-proxy is
  already running in the cluster and needs to be removed, since running
  both simultaneously is unsupported and produces confusing, overlapping
  `Service` behavior.
- For the mesh/L7 capability specifically: Envoy is used under the hood
  for L7 policy and mesh features, so budget for that additional
  component even though there's no per-pod sidecar.

## Step-by-step guidance

1. **Install Cilium via the CLI**, which handles CRD installation and
   validates cluster compatibility before applying:
   ```bash
   cilium install --version <cilium-version>
   cilium status --wait
   ```
   Avoid pinning to `latest` implicitly — pick a specific version
   deliberately so upgrades are a reviewed, intentional step.

2. **Enable kube-proxy replacement explicitly**, and confirm it's
   actually active rather than assuming the install flag alone
   guarantees it:
   ```bash
   cilium install --set kubeProxyReplacement=true
   cilium status --verbose | grep -i "KubeProxyReplacement"
   ```
   If kube-proxy is already running in the cluster, plan its removal
   (typically a DaemonSet deletion) as part of the same migration window
   — leaving both active is unsupported.

3. **Run the built-in connectivity test after any install or upgrade**,
   before trusting the cluster is healthy:
   ```bash
   cilium connectivity test
   ```
   This exercises pod-to-pod, pod-to-service, and (if enabled) policy
   enforcement paths across nodes, and is far more thorough than
   eyeballing `cilium status`.

4. **Write `CiliumNetworkPolicy` starting from default-deny per
   namespace**, then add explicit allows, mirroring standard
   Kubernetes `NetworkPolicy` semantics but with L7-aware matching:
   ```yaml
   apiVersion: cilium.io/v2
   kind: CiliumNetworkPolicy
   metadata:
     name: payments-api-ingress
     namespace: payments
   spec:
     endpointSelector:
       matchLabels: { app: payments-api }
     ingress:
       - fromEndpoints:
           - matchLabels: { app: checkout-service }
         toPorts:
           - ports:
               - port: "8080"
                 protocol: TCP
             rules:
               http:
                 - method: "GET"
                   path: "/charges/.*"
                 - method: "POST"
                   path: "/charges"
   ```
   The `rules.http` block is Cilium enforcing an L7 policy (method +
   path) directly in the eBPF/Envoy datapath — no sidecar required for
   the L3/L4 portion; the L7 portion transparently routes through a
   per-node (not per-pod) Envoy proxy Cilium manages.

5. **Restrict egress, including DNS-aware policy**, since plain IP-based
   egress rules are brittle against services with rotating IPs (most
   cloud APIs):
   ```yaml
   apiVersion: cilium.io/v2
   kind: CiliumNetworkPolicy
   metadata:
     name: payments-api-egress
     namespace: payments
   spec:
     endpointSelector:
       matchLabels: { app: payments-api }
     egress:
       - toFQDNs:
           - matchName: "api.stripe.com"
         toPorts:
           - ports: [{ port: "443", protocol: TCP }]
       - toEndpoints:
           - matchLabels:
               k8s:io.kubernetes.pod.namespace: kube-system
               k8s-app: kube-dns
         toPorts:
           - ports: [{ port: "53", protocol: UDP }]
             rules: { dns: [{ matchPattern: "*" }] }
   ```
   `toFQDNs` resolves and pins allowed egress to a DNS name rather than a
   brittle static IP/CIDR.

6. **Enable Hubble for flow-level observability** before relying on
   network policy in production — you want visibility into what's being
   allowed/dropped before tightening further:
   ```bash
   cilium hubble enable
   cilium hubble port-forward &
   hubble observe --namespace payments
   hubble observe --verdict DROPPED
   ```

7. **Consider Cilium's mesh capability only where the sidecar-less
   trade-off genuinely fits** — L4 policy, kube-proxy replacement, and
   basic L7 HTTP policy are Cilium's strongest ground; if the need is
   deep L7 traffic shaping (complex retries, fault injection, rich
   traffic mirroring) across many protocols, compare against a
   sidecar-based mesh's more mature feature set (see
   [service-mesh-istio](../../../kubernetes-platform/skills/service-mesh-istio/SKILL.md)
   for the ambient-mode comparison point, and
   [linkerd-service-mesh-configuration](../linkerd-service-mesh-configuration/SKILL.md)
   for a lighter sidecar-based alternative) before committing.

8. **Validate before production rollout**, not just at initial install —
   see
   [cilium-configuration-validation](../cilium-configuration-validation/SKILL.md)
   for the specific commands.

## Best practices

- Pin an explicit Cilium version at install and upgrade time, and run
  `cilium connectivity test` after every upgrade, not just the initial
  install — eBPF datapath changes between versions can have subtle
  effects that a quick `cilium status` glance won't catch.
- Default-deny per namespace with `CiliumNetworkPolicy`, then add
  explicit allows scoped by label selector, mirroring the same
  discipline used for standard Kubernetes `NetworkPolicy` — Cilium's L7
  awareness doesn't change the underlying default-deny-first principle.
- Prefer `toFQDNs` over static IP/CIDR egress rules for any external
  dependency whose IPs aren't fixed (which is most SaaS/cloud APIs) —
  CIDR-based egress rules silently stop working when the provider
  rotates IPs.
- Enable Hubble before tightening network policy in production, so
  drops are visible and diagnosable rather than discovered as a support
  ticket.
- Don't run kube-proxy and Cilium's kube-proxy replacement
  simultaneously — pick one deliberately and remove the other as part
  of the same change, not as an afterthought.
- Treat CNI installation/migration on a live cluster as a maintenance
  event requiring a window and rollback plan, not a rolling change —
  networking is foundational enough that a bad CNI change can take down
  every pod's connectivity at once.

## Common pitfalls

- **Symptom:** After enabling `kubeProxyReplacement=true`, some Services
  become unreachable while others still work.
  **Fix:** kube-proxy is likely still running alongside Cilium's
  replacement, producing inconsistent/overlapping `Service` handling.
  Confirm kube-proxy's DaemonSet is fully removed and `cilium status
  --verbose` reports `KubeProxyReplacement: True/Strict` before treating
  the migration as complete.

- **Symptom:** A `CiliumNetworkPolicy` egress rule using a static CIDR
  for an external API stops working weeks after deployment, with no
  policy change made.
  **Fix:** The external provider rotated its IP range, which a
  CIDR-based rule doesn't track. Switch to `toFQDNs` for any external
  dependency identified by DNS name rather than a small set of fixed
  IPs, and confirm the cluster's DNS egress is itself allowed (Cilium's
  FQDN policy needs to observe the DNS lookup to learn the resolved IP).

- **Symptom:** An L7 HTTP policy (`rules.http` with method/path
  matching) is applied but traffic that should be blocked still gets
  through.
  **Fix:** L7 policy enforcement requires Cilium's per-node Envoy proxy
  to actually be engaged for that traffic — confirm the policy's
  `toPorts.ports` protocol/port matches the real traffic and check
  `cilium status` for the L7 proxy's health; an L7 rule attached to a
  port that doesn't match real traffic silently falls through to
  whatever the L3/L4 rule alone would allow.

- **Symptom:** Connectivity looks broken cluster-wide immediately after
  a Cilium version upgrade.
  **Fix:** Run `cilium connectivity test` immediately post-upgrade as
  standard practice, and keep a rollback plan (previous Helm values/CLI
  install command) ready — eBPF program changes between minor versions
  have occasionally shifted default behavior; don't assume an upgrade is
  purely additive.

- **Symptom:** To resolve a connectivity failure during an incident,
  someone applies a permissive `CiliumNetworkPolicy` allowing all
  ingress/egress for the affected workload "to rule out policy as the
  cause," and it's left in place after the incident closes.
  **Fix:** This silently removes network policy protection for that
  workload going forward. Treat a broad allow-all policy change as a
  time-boxed diagnostic step only, confirm the actual root cause via
  `hubble observe --verdict DROPPED` instead of guessing, and restore
  the original scoped policy (or a corrected version of it) once the
  real cause is found.

## Worked example

**Scenario:** Install Cilium with kube-proxy replacement, default-deny
`payments` namespace ingress/egress, allow only `checkout-service` to
call `payments-api` on specific routes, and allow egress to a specific
external payment processor by hostname.

```bash
cilium install --version <cilium-version> --set kubeProxyReplacement=true
cilium status --wait
cilium connectivity test
cilium hubble enable
```

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: payments-api-default-deny
  namespace: payments
spec:
  endpointSelector: {}
  ingress: []
  egress: []
---
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: payments-api-ingress
  namespace: payments
spec:
  endpointSelector:
    matchLabels: { app: payments-api }
  ingress:
    - fromEndpoints:
        - matchLabels: { app: checkout-service }
      toPorts:
        - ports: [{ port: "8080", protocol: TCP }]
          rules:
            http:
              - method: "POST"
                path: "/charges"
---
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: payments-api-egress
  namespace: payments
spec:
  endpointSelector:
    matchLabels: { app: payments-api }
  egress:
    - toFQDNs:
        - matchName: "api.stripe.com"
      toPorts: [{ ports: [{ port: "443", protocol: TCP }] }]
    - toEndpoints:
        - matchLabels:
            k8s:io.kubernetes.pod.namespace: kube-system
            k8s-app: kube-dns
      toPorts:
        - ports: [{ port: "53", protocol: UDP }]
          rules: { dns: [{ matchPattern: "*" }] }
```

```bash
kubectl apply -f payments-policies.yaml
hubble observe --namespace payments --verdict DROPPED
```

`hubble observe` confirms only `checkout-service → payments-api:8080
POST /charges` and `payments-api → api.stripe.com:443` flows are
forwarded, with everything else in the namespace showing a `DROPPED`
verdict — giving concrete evidence the default-deny policy is enforcing
as intended before it's considered production-ready.
[cilium-configuration-validation](../cilium-configuration-validation/SKILL.md)
covers the fuller pre-production validation pass.

## Cross-references

- [cilium-configuration-validation](../cilium-configuration-validation/SKILL.md) — validating network policy and Hubble observability configuration before this reaches production.
- [consul-service-mesh-and-discovery-configuration](../consul-service-mesh-and-discovery-configuration/SKILL.md) — an alternative for estates that need mesh reach beyond Kubernetes (VMs, multi-cloud), which Cilium's CNI-layer approach doesn't address.
- [linkerd-service-mesh-configuration](../linkerd-service-mesh-configuration/SKILL.md) — a sidecar-based mesh alternative with a more mature L7 traffic-management feature set, worth comparing when Cilium's mesh capability doesn't cover a specific need.
- [service-mesh-istio](../../../kubernetes-platform/skills/service-mesh-istio/SKILL.md) — the comparison point for sidecar-based mesh traffic management and Istio's own ambient (sidecar-less) mode, relevant when weighing Cilium's mesh capability against Istio's.
