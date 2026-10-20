---
name: coredns-golang-dns
description: CoreDNS configuration and Go DNS programming. Use when writing Corefiles, patching CoreDNS in Kubernetes (kube-system ConfigMap, NodeHosts, rewrites, conditional forwarders), serving static A/AAAA/CNAME/SRV records, building Go DNS servers/interceptors with miekg/dns (split-horizon, conditional forward, response rewriting, transparent proxy), enabling DNS-over-TLS / DNS-over-HTTPS with cert-manager Certificates and trust-manager Bundles, or distributing CA trust for DoT/DoH clients.
license: MIT
version: 1.0.0
---

# CoreDNS & Go DNS

CoreDNS Corefile authoring, Kubernetes CoreDNS patching, static record serving,
DoT/DoH with cert-manager + trust-manager, and Go DNS server/interceptor
development with `github.com/miekg/dns`.

## When to Use

- Editing the cluster CoreDNS ConfigMap (kube-system) to add forward zones,
  static hosts, rewrites, or stubdomains.
- Deploying a *second* CoreDNS instance as a custom resolver / interceptor in
  front of upstream DNS.
- Writing a Go service that answers DNS queries — split-horizon resolvers,
  conditional forwarders, response rewriters, captive-portal style
  interceptors, or test fixtures.
- Adding TLS to DNS endpoints (DoT 853, DoH 443/8443) and trusting the issuing
  CA cluster-wide.

## Decision Tree

```
Static A/AAAA/CNAME inside cluster?
  └─ Patch kube-system/coredns Corefile via `hosts` or `file` plugin
     → references/coredns-static-records.md

Override an external domain inside the cluster?
  └─ `rewrite` or `template` plugin in CoreDNS
     → references/coredns-static-records.md

Intercept and conditionally rewrite responses?
  └─ Build a Go forwarder in front of CoreDNS using miekg/dns
     → references/go-dns-interceptor.md  +  scripts/go-dns-interceptor/

DoT/DoH with valid certs?
  └─ cert-manager Certificate → CoreDNS `tls`/`https` plugin
     → references/coredns-tls-cert-manager.md
  └─ Distribute the CA via trust-manager Bundle for clients
     → references/coredns-tls-cert-manager.md
  └─ CoreDNS forwarding to upstream DoT (tls:// + trust-manager bundle)
     → references/coredns-tls-cert-manager.md (Forwarding Upstream over DoT)

Something not working?
  └─ Diagnostic recipes (rcodes, dig flags, metrics, DoT handshake)
     → references/troubleshooting.md
```

## Quick Reference

| Topic | File |
|-------|------|
| Corefile syntax, server blocks, plugin chain | `references/coredns-corefile.md` |
| `hosts`, `file`, `template`, `rewrite` plugins | `references/coredns-static-records.md` |
| Patching kube-system CoreDNS ConfigMap | `references/coredns-kubernetes.md` |
| DoT/DoH via cert-manager + trust-manager | `references/coredns-tls-cert-manager.md` |
| `miekg/dns` quick start (server, client, RR) | `references/go-dns-miekg.md` |
| Go DNS server with static records + forward | `references/go-dns-server.md` |
| DNS interception patterns (proxy, splice) | `references/go-dns-interceptor.md` |
| Working Go example | `scripts/go-dns-interceptor/main.go` |
| Debugging (NXDOMAIN/SERVFAIL, dig flags, DoT handshake, metrics) | `references/troubleshooting.md` |

## Workflows

### Add static records to in-cluster CoreDNS
1. Inspect: `kubectl -n kube-system get cm coredns -o yaml`.
2. Choose plugin — `hosts` for inline A/AAAA, `file` for full zone, `rewrite`
   for response rewriting, `template` for synthesized RRs. See
   `references/coredns-static-records.md`.
3. Patch via Kustomize/Helm overlay — see `references/coredns-kubernetes.md`
   for recipes that survive cluster upgrades.
4. Roll: `kubectl -n kube-system rollout restart deploy/coredns`.
5. Verify: `dig +short @<kube-dns-svc-ip> <name>` from a debug pod.

### Build a Go DNS interceptor
1. Scaffold from `scripts/go-dns-interceptor/main.go`.
2. Define static record map (A/AAAA/CNAME/TXT/SRV).
3. For names not in the static map, forward upstream via `dns.Client`.
4. Optionally rewrite responses (e.g. NXDOMAIN → synthesized A record).
5. See `references/go-dns-interceptor.md` for split-horizon, response
   rewriting, and transparent-proxy patterns.

### Add TLS (DoT / DoH)
1. Issue cert via cert-manager `Certificate` (DNS SANs for the resolver name).
2. Mount Secret into CoreDNS pod, reference in `tls`/`https` directives.
3. Distribute the issuing CA via trust-manager `Bundle` so clients trust DoT.
4. See `references/coredns-tls-cert-manager.md` for full manifests.

## Important Notes

- CoreDNS plugin order is **fixed at compile time**, not by Corefile order.
  The Corefile only enables/configures plugins. See
  `references/coredns-corefile.md`.
- `hosts` plugin reloads its file every 5s by default — good for GitOps.
- `kubectl edit` on the kube-system ConfigMap may be reverted by some
  installers (kubeadm phase, EKS addon, kops). Use the installer's overlay
  mechanism — see `references/coredns-kubernetes.md`.
- For DoT, CoreDNS needs the cert + key, not just the cert. trust-manager
  distributes the **CA** to clients, not the leaf.
- `miekg/dns` requires explicit `m.SetReply(r)` and `m.Authoritative = true`
  for static answers, or downstream resolvers treat them as referrals.
- Static record TTLs default to 3600s in CoreDNS `hosts` plugin and 60s in
  `file` plugin's SOA — set explicitly for fast iteration.
