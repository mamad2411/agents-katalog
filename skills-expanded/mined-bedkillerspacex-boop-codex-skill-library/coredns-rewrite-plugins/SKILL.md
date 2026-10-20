---
name: coredns-rewrite-plugins
description: >
  Configure and safely operate CoreDNS rewrite, template, forward, and related
  plugins for owned Kubernetes or internal DNS. Use when implementing name
  rewrites, stub domains, split-horizon DNS, ClusterFirstWithHostNet edge cases,
  or debugging Corefile plugin order on clusters you administer — not public DNS
  hijacking.
---

# CoreDNS Rewrite Plugins

## Scope And Authorization

- **In scope:** CoreDNS `Corefile` / ConfigMap changes on clusters or DNS servers you operate, with change windows for production kube-dns/CoreDNS.
- **Out of scope:** Poisoning or redirecting DNS for systems you do not own; intercepting third-party resolution.
- Prefer dry-run in a non-prod cluster or local `coredns` binary with a test Corefile.
- Redact internal hostnames that reveal sensitive topology if reports leave the org.
- Pair with `code-quality-standards` for any automation that generates Corefiles.

## When To Use

- Adding `rewrite` rules (name, class, type, EDNS0) for service aliases or migration.
- Combining `rewrite` with `forward`, `kubernetes`, `hosts`, `template`, `errors`, `log`, `cache`, `health`, `ready`.
- Migrating from kube-dns stubDomains / upstreamNameservers to CoreDNS.
- Debugging NXDOMAIN loops, CNAME chains, or wrong plugin order.
- Hardening who can edit the CoreDNS ConfigMap (RBAC).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General K8s network policy / service mesh | mesh or network-policy skills |
| External authoritative DNS (Route53, Cloud DNS) | cloud DNS skills |
| TLS cert issuance for apps | cert-manager / PKI skills |
| PCAP-level DNS forensics | `traffic-analysis-pcap` / NetworkProtocolAnalysisSkill |
| Implementation quality baseline | `code-quality-standards` |

## Plugin roles (topic map)

| Plugin | Role | Typical pitfalls |
| --- | --- | --- |
| `kubernetes` | Cluster service/pod DNS | Wrong cluster domain; fallthrough misuse |
| `rewrite` | Mutate question/answer names | Order vs `kubernetes`; infinite CNAME loops |
| `forward` | Upstream resolvers | Open resolver if mis-bound; no TLS to upstream when required |
| `hosts` / `file` | Static zones | Stale entries shadowing real services |
| `template` | Synthetic answers | Over-broad regex answering everything |
| `cache` | Performance | Caching negative answers during misconfig |
| `errors` / `log` | Observability | Logging client IPs without retention policy |
| `health` / `ready` | Probes | Ready before kubernetes loaded |

**Order matters:** CoreDNS runs plugins in Corefile order per server block. Place `rewrite` **before** plugins that should see the rewritten name (often before `kubernetes` or `forward`), unless you intentionally rewrite answers instead of questions.

## Workflow

### 1. Confirm scope and success criteria

1. Record cluster, CoreDNS Deployment/ConfigMap name (`kube-system/coredns` typical), and who can approve DNS changes.
2. Success: specific FQDNs resolve as designed; no regression for `kubernetes.default.svc.cluster.local`; metrics/ready probes healthy; rollback ConfigMap revision known.
3. List names to rewrite, desired targets, and TTL/cache expectations.

### 2. Inventory current CoreDNS

```bash
kubectl -n kube-system get deploy coredns -o wide
kubectl -n kube-system get cm coredns -o yaml
kubectl -n kube-system logs -l k8s-app=kube-dns --tail=100
# Version
kubectl -n kube-system get deploy coredns -o jsonpath='{.spec.template.spec.containers[0].image}{"\n"}'
```

Note:

1. Cluster domain (usually `cluster.local`).
2. Existing `forward . /etc/resolv.conf` or explicit upstreams.
3. NodeLocal DNSCache presence (extra hop; rewrites may need to live consistently).
4. Autopath / pods insecure options if used.

### 3. Baseline resolution

```bash
# From a debug pod on the cluster
kubectl run -n default dnstest --rm -it --restart=Never --image=busybox:1.36 -- nslookup kubernetes.default.svc.cluster.local
kubectl run -n default dnstest2 --rm -it --restart=Never --image=busybox:1.36 -- nslookup example.internal.corp
# CoreDNS metrics (if enabled)
kubectl -n kube-system port-forward deploy/coredns 9153:9153
# curl -s localhost:9153/metrics | head
```

Capture before/after for each rewritten name and a control name that must not change.

### 4. Design rewrite rules safely

#### Question name rewrite (common migration pattern)

```corefile
.:53 {
    errors
    health {
       lameduck 5s
    }
    ready
    # Rewrite client QNAME before kubernetes/forward see it
    rewrite name exact old-api.example.corp new-api.svc.cluster.local
    rewrite name regex ^old-(.*)\.example\.corp$ {1}.svc.cluster.local
    kubernetes cluster.local in-addr.arpa ip6.arpa {
       pods insecure
       fallthrough in-addr.arpa ip6.arpa
       ttl 30
    }
    prometheus :9153
    forward . /etc/resolv.conf {
       max_concurrent 1000
    }
    cache 30
    loop
    reload
    loadbalance
}
```

Guidance:

1. Prefer `rewrite name exact` over broad `regex` when possible.
2. Understand **stop vs continue** behavior for multiple rewrite rules (see CoreDNS rewrite plugin docs for your version).
3. Answer rewrites (`rewrite name … answer auto`) may be required so responses match client expectations — test with dig.
4. Never rewrite `.` catch-alls that break Cluster DNS or upstream resolution.
5. Pair regex with anchors (`^…$`) to avoid partial matches.

#### Stub domain / forward only

```corefile
example.corp:53 {
    errors
    cache 30
    forward . 10.0.0.10 10.0.0.11
}
.:53 {
    # default cluster block...
}
```

Use separate server blocks for corporate zones instead of rewriting everything into `forward`.

### 5. Apply change with rollback

1. Backup ConfigMap: `kubectl -n kube-system get cm coredns -o yaml > coredns-cm.backup.yaml`
2. Edit via process your org allows (`kubectl edit cm coredns` or GitOps).
3. CoreDNS `reload` plugin picks up changes; watch pods for crash loops.
4. If NodeLocal DNSCache is deployed, confirm whether it caches old answers (flush/restart policy per platform docs).

```bash
kubectl -n kube-system rollout status deploy/coredns
kubectl -n kube-system get pods -l k8s-app=kube-dns
```

### 6. Verify with evidence

```bash
# From debug pod or node
nslookup old-api.example.corp
dig +short old-api.example.corp @<coredns-clusterip>
dig +short kubernetes.default.svc.cluster.local @<coredns-clusterip>
# Look for loops
dig +trace old-api.example.corp  # use carefully; prefer controlled dig to CoreDNS Service IP
```

Pass criteria:

1. Rewritten names resolve to intended A/AAAA/CNAME.
2. Unrelated cluster DNS unchanged.
3. No `loop` plugin errors in logs.
4. Latency and `forward` timeouts within SLO; cache TTLs acceptable for cutover.

### 7. Harden operations

1. RBAC: restrict who can `update` ConfigMap `coredns` and Deployment.
2. GitOps the Corefile; PR review required for `rewrite` / `forward` changes.
3. Alert on CoreDNS crash loops, `forward` timeouts, and elevated NXDOMAIN rates.
4. Document each rewrite with owner, ticket, and removal date (migrations should expire).

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Rewrite scope | Exact names / tight regex | `rewrite name regex .* evil.com` |
| Plugin order | rewrite → kubernetes/forward as designed | forward first so rewrite never runs |
| Upstreams | Private resolvers / resolv.conf intentional | Open recursive to Internet from cluster DNS |
| Change mgmt | Backup + GitOps + probe | Live edit prod without rollback |
| Cache | Short TTL during migration | 3600s caching a wrong rewrite |
| Multi-tenancy | Per-zone server blocks | One global rewrite for all tenants |

## Output Checklist

- [ ] Cluster/CoreDNS version and ConfigMap backup recorded
- [ ] Required rewrites and non-goals listed
- [ ] Plugin order reasoned (rewrite vs kubernetes vs forward)
- [ ] Baseline dig/nslookup captured
- [ ] Config applied via approved channel
- [ ] Post-change resolution evidence for success and control names
- [ ] Logs show no loop/reload errors
- [ ] RBAC/GitOps notes updated
- [ ] Migration rewrites have owners/expiry
- [ ] Residual risk (NodeLocal cache, multi-cluster) noted

## Rules

- Operate only on DNS infrastructure you own or are authorized to change.
- Prefer explicit zone forwards over opaque global rewrites when both work.
- Treat Corefile edits as high-impact: bad DNS takes down the cluster control plane consumers.
- Do not use rewrite plugins to impersonate third-party domains on shared resolvers.
- Keep this skill focused on CoreDNS rewrite/forward/Corefile operations; route app-level service discovery elsewhere.
