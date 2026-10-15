---
name: k8s-dns-troubleshooting
description: Use when pods cannot resolve service names, CoreDNS is unhealthy, DNS lookups are slow or timing out, service discovery is broken, or when performing a DNS health check on a Kubernetes cluster
---

# Kubernetes DNS Troubleshooting

Investigate and diagnose internal Kubernetes DNS (CoreDNS). Perform a quick health assessment to determine whether cluster DNS is functioning correctly, then deep-dive into root causes when issues are found.

## Keywords

coredns, kube-dns, dns, resolve, nslookup, dig, service discovery, NXDOMAIN, dns timeout, dns lookup, ndots, search domain, cluster.local, Corefile, dns policy, dns resolution, dns health, dns check, name resolution, dns-default, cluster-first

## When to Use This Skill

- Pods cannot resolve service names (NXDOMAIN or timeouts)
- CoreDNS pods are crashing, restarting, or not running
- DNS lookups are slow (high latency on service calls)
- Service discovery is broken after a cluster upgrade or config change
- A general DNS health check is needed to confirm the cluster is healthy
- Applications log connection errors that trace back to DNS failures
- Cross-namespace service resolution is failing
- Headless service DNS records are not returning pod IPs

### When NOT to Use

- DNS records for external providers are not syncing → use [external-dns-troubleshooting](../external-dns-troubleshooting)
- TLS certificate issuance failures → use [cert-manager-troubleshooting](../cert-manager-troubleshooting)
- Service exists but has no endpoints → use [k8s-namespace-troubleshooting](../k8s-namespace-troubleshooting)

**Note:** Pods failing to resolve external domains (e.g., `api.example.com`) are in scope — this is an upstream forwarding issue diagnosed in Section 3 (Corefile) and Section 5 (network connectivity). ExternalDNS is a separate concern about *publishing* records to providers.

## Related Skills

- [external-dns-troubleshooting](../external-dns-troubleshooting) - External DNS record management
- [k8s-namespace-troubleshooting](../k8s-namespace-troubleshooting) - General namespace diagnosis
- [k8s-platform-operations](../k8s-platform-operations) - Cluster-wide health checks
- [k8s-network-troubleshooting](../k8s-network-troubleshooting) - Network connectivity and service mesh issues
- [k8s-security-hardening](../k8s-security-hardening) - Network policies that may block DNS
- [Shared: Network Policies](../_shared/references/network-policies.md)

## Quick Reference

| Task | Command |
|------|---------|
| CoreDNS pod status | `kubectl get pods -n kube-system -l k8s-app=kube-dns` |
| CoreDNS logs | `kubectl logs -n kube-system -l k8s-app=kube-dns --tail=100` |
| DNS service ClusterIP | `kubectl get svc kube-dns -n kube-system` |
| DNS endpoints | `kubectl get endpoints kube-dns -n kube-system` |
| Test DNS from existing pod | `kubectl exec -n ${NS} ${POD} -- nslookup kubernetes.default` |
| Find a running pod to exec into | `kubectl get pods -A --field-selector=status.phase=Running -o jsonpath='{.items[0].metadata.namespace} {.items[0].metadata.name}'` |
| View Corefile | `kubectl get configmap coredns -n kube-system -o yaml` |
| Pod DNS config | `kubectl exec ${POD} -n ${NS} -- cat /etc/resolv.conf` |

---

## Quick DNS Health Check

Run this checklist first for a fast pass/fail indicator of cluster DNS health. Complete all checks before drawing conclusions.

### Step 1: CoreDNS Pods

```bash
# Are CoreDNS pods running?
kubectl get pods -n kube-system -l k8s-app=kube-dns -o wide

# Check for restarts (indicates instability)
kubectl get pods -n kube-system -l k8s-app=kube-dns -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{range .status.containerStatuses[*]}{.restartCount}{end}{"\n"}{end}'
```

### Step 2: DNS Service and Endpoints

```bash
# kube-dns Service must exist with a ClusterIP
kubectl get svc kube-dns -n kube-system

# Endpoints must point to CoreDNS pod IPs
kubectl get endpoints kube-dns -n kube-system
```

### Step 3: Resolution Test

Test DNS from an existing running pod. No new workloads are deployed.

```bash
# Find a running pod to use as a test subject
kubectl get pods -A --field-selector=status.phase=Running -o jsonpath='{range .items[0]}{.metadata.namespace}{" "}{.metadata.name}{"\n"}{end}'

# Verify the pod's resolv.conf points to the kube-dns ClusterIP
kubectl exec -n ${NS} ${POD} -- cat /etc/resolv.conf

# Test resolution (nslookup available in most images)
kubectl exec -n ${NS} ${POD} -- nslookup kubernetes.default.svc.cluster.local

# If nslookup is not available, try wget or getent as fallbacks
kubectl exec -n ${NS} ${POD} -- getent hosts kubernetes.default.svc.cluster.local
kubectl exec -n ${NS} ${POD} -- wget -qO- --timeout=5 http://kubernetes.default.svc:443 2>&1 | head -1
```

If `nslookup`/`getent` are not available in the pod image, rely on indirect indicators: Steps 1-2 passing (CoreDNS pods running, service and endpoints healthy) plus no DNS errors in CoreDNS logs (Section 6) is strong evidence DNS is functional.

If resolution fails, see Section 2 for comprehensive testing. If it passes, see Section 2 for deeper checks (cross-namespace, headless, external resolution).

### Health Summary Template

Present results using this format:

```markdown
## DNS Health Summary

| Check | Status | Detail |
|-------|--------|--------|
| CoreDNS pods running | PASS/FAIL | X/Y pods ready, Z restarts |
| kube-dns Service exists | PASS/FAIL | ClusterIP: X.X.X.X |
| kube-dns Endpoints populated | PASS/FAIL | X endpoints |
| Resolve kubernetes.default (exec) | PASS/FAIL/SKIP | Resolved to X.X.X.X / Timeout / NXDOMAIN / No tools available |
| CoreDNS health endpoint | PASS/FAIL | localhost:8080/health returns OK |
| CoreDNS restart count | PASS/WARN | Total restarts across pods |

**Overall: HEALTHY / DEGRADED / UNHEALTHY**
```

- **HEALTHY** — All checks pass, zero restarts
- **DEGRADED** — Resolution works but CoreDNS has restarts or reduced replicas
- **UNHEALTHY** — Resolution fails or CoreDNS pods are down

---

## Diagnostic Workflow

When the health check reports DEGRADED or UNHEALTHY, use this decision tree to identify root causes.

```
DNS resolution failing?
├─ CoreDNS pods not running?
│   ├─ Pods Pending → Scheduling issue (Section 1)
│   ├─ Pods CrashLoopBackOff → Bad Corefile or OOM (Section 1, Section 3)
│   └─ Deployment missing → CoreDNS not installed or deleted (Section 1)
├─ CoreDNS pods running but resolution fails?
│   ├─ kube-dns Service missing ClusterIP → Service deleted (Section 1)
│   ├─ kube-dns Endpoints empty → Label mismatch or pods not ready (Section 1)
│   ├─ Pod /etc/resolv.conf wrong → dnsPolicy misconfigured (Section 4)
│   ├─ Internal names fail, external works → Corefile zone config (Section 3)
│   ├─ External names fail, internal works → Upstream forwarder issue (Section 3)
│   ├─ All lookups timeout → Network path blocked (Section 5)
│   └─ Intermittent failures → Overloaded CoreDNS or conntrack (Section 1, Section 5)
├─ DNS slow but eventually resolves?
│   ├─ High ndots causing extra queries → ndots config (Section 4)
│   ├─ CoreDNS CPU/memory saturated → Resource limits (Section 1)
│   └─ Upstream DNS slow → Forwarder latency (Section 3)
└─ Only some pods affected?
    ├─ Check pod dnsPolicy → Per-pod DNS config (Section 4)
    ├─ Network policy blocking egress → UDP/TCP 53 blocked (Section 5)
    └─ Node-specific issue → kube-proxy or iptables (Section 5)
```

---

## Section 1: CoreDNS Component Health

```bash
# Deployment status
kubectl get deploy coredns -n kube-system
kubectl describe deploy coredns -n kube-system

# Pod details — check status, restarts, node placement
kubectl get pods -n kube-system -l k8s-app=kube-dns -o wide

# Resource consumption (requires metrics-server)
kubectl top pods -n kube-system -l k8s-app=kube-dns

# Check for OOMKills
kubectl get pods -n kube-system -l k8s-app=kube-dns -o json | \
  jq -r '.items[] | .metadata.name as $pod | .status.containerStatuses[]? | select(.lastState.terminated.reason == "OOMKilled") | "\($pod)\tOOMKilled"'

# Resource requests and limits
kubectl get deploy coredns -n kube-system -o jsonpath='{.spec.template.spec.containers[0].resources}' | jq .

# Events related to CoreDNS
kubectl get events -n kube-system --field-selector involvedObject.name=coredns --sort-by='.lastTimestamp'

# Service and endpoints
kubectl get svc kube-dns -n kube-system -o yaml
kubectl get endpoints kube-dns -n kube-system -o yaml
```

### What to Look For

| Symptom | Likely Cause | Diagnostic |
|---------|-------------|-----------|
| 0/2 pods ready | CoreDNS crashed or not scheduled | Check events and logs |
| High restart count | OOMKill or Corefile error | Check terminated reason and resource limits |
| Endpoints empty | Pods not ready or label mismatch | Verify pod labels match `k8s-app=kube-dns` |
| CPU near limits | High query volume | Check if CPU is near limits; recommend increasing CPU limits or adding replicas |
| Memory near limits | Large cache or zone data | Check if memory is near limits; recommend increasing memory limits |

---

## Section 2: DNS Resolution Testing

Test DNS using existing running pods — no new workloads are deployed. Pick a pod that is already running in the cluster.

### Finding a Test Pod

```bash
# List running pods (pick one with a shell — alpine, debian, ubuntu images work well)
kubectl get pods -A --field-selector=status.phase=Running -o wide

# Check what tools are available in a pod
kubectl exec -n ${NS} ${POD} -- sh -c 'which nslookup dig getent wget curl 2>/dev/null'
```

Not all container images include DNS tools. Try commands in this order of preference: `nslookup`, `getent hosts`, `wget`/`curl` (connection attempt reveals DNS). If no tools are available, use indirect methods (resolv.conf inspection + CoreDNS log analysis).

### Basic Resolution Tests

```bash
# Resolve the Kubernetes API service (must always work)
kubectl exec -n ${NS} ${POD} -- nslookup kubernetes.default.svc.cluster.local

# Resolve with fully qualified name vs short name
kubectl exec -n ${NS} ${POD} -- sh -c \
  'echo "--- FQDN ---" && nslookup kubernetes.default.svc.cluster.local && echo "--- Short ---" && nslookup kubernetes.default'

# Resolve a service in a specific namespace
kubectl exec -n ${NS} ${POD} -- nslookup ${SERVICE}.${TARGET_NS}.svc.cluster.local

# Test external resolution (upstream forwarding)
kubectl exec -n ${NS} ${POD} -- nslookup www.google.com
```

### Fallback: getent or wget

```bash
# If nslookup is not available, use getent
kubectl exec -n ${NS} ${POD} -- getent hosts kubernetes.default.svc.cluster.local
kubectl exec -n ${NS} ${POD} -- getent hosts ${SERVICE}.${TARGET_NS}.svc.cluster.local

# If neither is available, a wget/curl connection attempt tests DNS indirectly
# (DNS failure shows as "bad address" or "could not resolve host")
kubectl exec -n ${NS} ${POD} -- wget -qO- --timeout=3 http://${SERVICE}.${TARGET_NS}.svc.cluster.local 2>&1 | head -3
```

### Targeted Queries Against CoreDNS Directly

```bash
# Get kube-dns ClusterIP
DNS_IP=$(kubectl get svc kube-dns -n kube-system -o jsonpath='{.spec.clusterIP}')

# Query CoreDNS directly by specifying the nameserver (bypasses pod resolv.conf)
kubectl exec -n ${NS} ${POD} -- nslookup kubernetes.default.svc.cluster.local ${DNS_IP}
```

### Indirect DNS Verification (No Exec Required)

When `kubectl exec` is unavailable or pod images lack tools, verify DNS through infrastructure checks:

```bash
# 1. Confirm pod resolv.conf nameserver matches kube-dns ClusterIP
DNS_IP=$(kubectl get svc kube-dns -n kube-system -o jsonpath='{.spec.clusterIP}')
echo "kube-dns ClusterIP: ${DNS_IP}"

# 2. Verify CoreDNS is serving queries (check logs for recent activity)
kubectl logs -n kube-system -l k8s-app=kube-dns --tail=50 --since=5m

# 3. Check CoreDNS health endpoint from within a CoreDNS pod
COREDNS_POD=$(kubectl get pods -n kube-system -l k8s-app=kube-dns -o jsonpath='{.items[0].metadata.name}')
kubectl exec -n kube-system ${COREDNS_POD} -- wget -qO- http://localhost:8080/health 2>&1
kubectl exec -n kube-system ${COREDNS_POD} -- wget -qO- http://localhost:8181/ready 2>&1

# 4. Check for DNS-related errors in application pod logs
kubectl logs -n ${NS} ${POD} --tail=200 | grep -iE 'dns|resolve|NXDOMAIN|lookup|name.resolution|no.such.host|could.not.resolve'
```

### Headless Service Verification

Headless services (ClusterIP: None) return individual pod IPs instead of a single VIP.

```bash
# Verify headless service has endpoints (indirect check — no exec needed)
kubectl get endpoints ${HEADLESS_SVC} -n ${NAMESPACE} -o jsonpath='{.subsets[*].addresses[*].ip}'

# If exec is available, resolve and confirm multiple A records
kubectl exec -n ${NS} ${POD} -- nslookup ${HEADLESS_SVC}.${NAMESPACE}.svc.cluster.local

# Individual pod DNS for StatefulSets
# Format: ${POD_NAME}.${HEADLESS_SVC}.${NAMESPACE}.svc.cluster.local
kubectl exec -n ${NS} ${POD} -- nslookup ${STATEFULSET_POD}-0.${HEADLESS_SVC}.${NAMESPACE}.svc.cluster.local
```

### Interpreting Results

| Result | Meaning |
|--------|---------|
| Returns IP address | Resolution working |
| `** server can't find ... NXDOMAIN` | Name does not exist — wrong service name, namespace, or missing service |
| `bad address` / `could not resolve host` | DNS lookup failed — CoreDNS unreachable or misconfigured |
| `connection timed out; no servers could be reached` | Cannot reach CoreDNS — network or service issue |
| `SERVFAIL` | CoreDNS received the query but failed to resolve — check Corefile and upstream |

---

## Section 3: CoreDNS Configuration (Corefile)

The Corefile is stored as a ConfigMap and defines how CoreDNS handles queries.

```bash
# View the Corefile
kubectl get configmap coredns -n kube-system -o jsonpath='{.data.Corefile}'

# View with line numbers for reference
kubectl get configmap coredns -n kube-system -o jsonpath='{.data.Corefile}' | cat -n

# Check if a custom ConfigMap exists
kubectl get configmap coredns-custom -n kube-system 2>/dev/null
```

### Default Corefile Structure

A healthy default Corefile looks like:

```
.:53 {
    errors
    health {
       lameduck 5s
    }
    ready
    kubernetes cluster.local in-addr.arpa ip6.arpa {
       pods insecure
       fallthrough in-addr.arpa ip6.arpa
       ttl 30
    }
    prometheus :9153
    forward . /etc/resolv.conf
    cache 30
    loop
    reload
    loadbalance
}
```

### Key Plugins and What Can Go Wrong

| Plugin | Purpose | Common Issue |
|--------|---------|-------------|
| `kubernetes` | Resolves cluster.local names | Wrong cluster domain, `pods` setting, or missing `fallthrough` |
| `forward` | Sends non-cluster queries upstream | Wrong upstream address, unreachable forwarder |
| `cache` | Caches responses | TTL too high causes stale answers; too low overloads upstream |
| `loop` | Detects forwarding loops | CoreDNS restarts if loop detected — check `/etc/resolv.conf` on nodes |
| `errors` | Logs errors | Missing plugin hides failures |
| `health` | Liveness endpoint on :8080 | If missing, kubelet cannot health-check CoreDNS |
| `ready` | Readiness endpoint on :8181 | If missing, endpoints not populated until pod is actually ready |
| `reload` | Hot-reload on Corefile change | Without this, ConfigMap changes require pod restart |

### Common Corefile Misconfigurations

| Problem | Symptom | Diagnostic |
|---------|---------|-----------|
| Wrong cluster domain | All internal lookups return NXDOMAIN | Check if `kubernetes` zone matches `--cluster-domain` kubelet flag |
| `forward . 8.8.8.8` when nodes use private DNS | External resolution of private zones fails | Check if `forward` directive should use `/etc/resolv.conf` or a private upstream |
| Missing `loop` plugin | CoreDNS forwards to itself via node resolv.conf, infinite loop | Check if `loop` plugin is present in Corefile |
| `pods verified` instead of `pods insecure` | Pod A/AAAA records fail verification checks | Check if `pods` setting is `verified` — recommend `pods insecure` unless strict verification is needed |
| Custom forward zone typo | Queries for that zone fail | Verify zone block spelling and upstream IP |
| Missing `fallthrough` in kubernetes block | Reverse lookups for pod IPs fail | Check if `fallthrough in-addr.arpa ip6.arpa` is present |

---

## Section 4: Pod DNS Configuration

Each pod gets its DNS config from the kubelet, controlled by the pod's `dnsPolicy` field.

### dnsPolicy Options

| Policy | Behaviour | When Used |
|--------|-----------|-----------|
| `ClusterFirst` (default) | Use CoreDNS for all lookups. Falls back to upstream for non-cluster names | Standard workloads |
| `Default` | Use the node's `/etc/resolv.conf` directly — bypasses CoreDNS | Pods that must use node DNS (rare) |
| `None` | No auto-config — requires `dnsConfig` to specify nameservers | Custom DNS setups |
| `ClusterFirstWithHostNet` | Like ClusterFirst but for `hostNetwork: true` pods | Pods using host networking that still need cluster DNS |

### Checking Pod DNS Config

```bash
# View the resolv.conf inside a running pod
kubectl exec ${POD} -n ${NS} -- cat /etc/resolv.conf

# Check the dnsPolicy on a pod spec
kubectl get pod ${POD} -n ${NS} -o jsonpath='{.spec.dnsPolicy}'

# Check dnsConfig overrides
kubectl get pod ${POD} -n ${NS} -o jsonpath='{.spec.dnsConfig}' | jq .
```

### Expected resolv.conf for ClusterFirst

```
nameserver 10.96.0.10    # kube-dns ClusterIP
search ${NS}.svc.cluster.local svc.cluster.local cluster.local
options ndots:5
```

### The ndots Problem

With `ndots:5` (the default), any name with fewer than 5 dots triggers search domain expansion. A lookup for `api.example.com` (2 dots, fewer than 5) generates these queries in order:

1. `api.example.com.${NS}.svc.cluster.local` — NXDOMAIN
2. `api.example.com.svc.cluster.local` — NXDOMAIN
3. `api.example.com.cluster.local` — NXDOMAIN
4. `api.example.com.` — success (finally resolves)

This means **4 DNS queries instead of 1** for every external name, adding latency and load.

**If ndots is the cause, recommend to the user:**
- Use trailing dots in application config (FQDN): `api.example.com.` bypasses search domains entirely
- Reduce ndots per pod via `spec.dnsConfig.options` (e.g., `ndots: "2"`)

### Common Pod DNS Issues

| Problem | Symptom | Diagnostic |
|---------|---------|-----------|
| `dnsPolicy: Default` on a non-hostNetwork pod | Pod uses node DNS, cannot resolve cluster services | Check `dnsPolicy` — recommend changing to `ClusterFirst` |
| `hostNetwork: true` without `ClusterFirstWithHostNet` | Pod uses node DNS, skips CoreDNS | Check `dnsPolicy` — recommend `ClusterFirstWithHostNet` |
| `dnsPolicy: None` without `dnsConfig` | Pod has no nameservers, all lookups fail | Check if `dnsConfig.nameservers` is defined |
| High ndots with many external calls | Slow DNS, high query volume to CoreDNS | Check ndots value — recommend reducing ndots or using FQDNs with trailing dot |

---

## Section 5: Network Connectivity to DNS

If CoreDNS is running and configured correctly but pods still cannot resolve, the network path may be blocked.

```bash
# Verify the kube-dns ClusterIP is reachable from an existing pod
DNS_IP=$(kubectl get svc kube-dns -n kube-system -o jsonpath='{.spec.clusterIP}')
kubectl exec -n ${NS} ${POD} -- nslookup kubernetes.default.svc.cluster.local ${DNS_IP}

# If nslookup unavailable, test connectivity with wget to CoreDNS health endpoint
kubectl exec -n ${NS} ${POD} -- wget -qO- --timeout=3 http://${DNS_IP}:8080/health 2>&1

# Check if network policies in the pod's namespace block DNS egress
kubectl get networkpolicies -n ${NS}

# Look for policies that restrict egress
kubectl get networkpolicies -n ${NS} -o json | \
  jq -r '.items[] | select(.spec.policyTypes[] == "Egress") | .metadata.name'
```

### Network Policy DNS Gotcha

If a namespace has an egress NetworkPolicy, it blocks all egress traffic by default — including DNS to kube-system. Check whether existing egress policies include a rule allowing UDP/TCP port 53. If they don't, recommend the user add a DNS egress rule to their NetworkPolicy.

### Node-Level Issues

```bash
# Check iptables rules for kube-dns Service (on the node)
# The kube-dns ClusterIP should have DNAT rules pointing to CoreDNS pod IPs
iptables-save | grep kube-dns

# Check kube-proxy is running (manages ClusterIP rules)
kubectl get pods -n kube-system -l k8s-app=kube-proxy

# Check conntrack table for DNS (UDP conntrack issues cause intermittent failures)
conntrack -L -p udp --dport 53 2>/dev/null | head -20
```

### Intermittent DNS Failures (Race Condition)

A known Linux kernel issue causes intermittent DNS failures when a pod sends UDP packets to a ClusterIP and both the A and AAAA queries race through conntrack. Symptoms: occasional 5-second timeouts on DNS lookups.

**If this race condition is confirmed, recommend one of these approaches to the user:**

| Approach | Recommendation |
|----------|---------------|
| Use TCP for DNS | Recommend setting `use-vc` option in pod `dnsConfig` |
| NodeLocal DNSCache | Recommend deploying node-level DNS cache (eliminates conntrack for DNS) |
| Single-request-reopen | Recommend setting `single-request-reopen` option in pod `dnsConfig` |

---

## Section 6: CoreDNS Logs and Metrics

### Enabling the Log Plugin

By default, CoreDNS does not log every query. To enable verbose logging for debugging, add the `log` plugin to the Corefile:

```bash
# Check if log plugin is already enabled
kubectl get configmap coredns -n kube-system -o jsonpath='{.data.Corefile}' | grep -c "log"
```

If verbose logging is needed, recommend the user add `log` inside the Corefile server block (CoreDNS reloads automatically if the `reload` plugin is present).

### Reading CoreDNS Logs

```bash
# Recent logs
kubectl logs -n kube-system -l k8s-app=kube-dns --tail=200

# Filter for errors
kubectl logs -n kube-system -l k8s-app=kube-dns --tail=500 | grep -iE 'error|fail|refused|timeout|SERVFAIL|NXDOMAIN'

# Watch live (useful during testing)
kubectl logs -n kube-system -l k8s-app=kube-dns -f --tail=50
```

### Key Log Patterns

| Log Pattern | Meaning | Diagnostic |
|-------------|---------|-----------|
| `plugin/loop: Loop ... detected` | CoreDNS is forwarding to itself | Check node `/etc/resolv.conf` and upstream forwarder config for loops |
| `plugin/forward: no upstreams available` | All upstream DNS servers unreachable | Check upstream IPs in Corefile `forward` directive |
| `SERVFAIL` | CoreDNS could not resolve the query | Check upstream forwarder or zone configuration |
| `NXDOMAIN` | Domain does not exist | Verify the queried name is correct |
| `i/o timeout` | Upstream DNS server not responding | Check network path to upstream; upstream may be overloaded |
| `connection refused` | Upstream DNS server rejecting connections | Check if upstream IP is correct and upstream is running |
| `OOMKilled` (in events, not logs) | CoreDNS ran out of memory | Check memory limits; recommend increasing memory limits |

### CoreDNS Metrics

CoreDNS exposes Prometheus metrics on port 9153 (when the `prometheus` plugin is enabled).

```bash
# Check metrics from within a CoreDNS pod (no new workloads needed)
COREDNS_POD=$(kubectl get pods -n kube-system -l k8s-app=kube-dns -o jsonpath='{.items[0].metadata.name}')
kubectl exec -n kube-system ${COREDNS_POD} -- wget -qO- http://localhost:9153/metrics 2>&1 | head -50
```

Key metrics to monitor:

| Metric | What It Tells You |
|--------|-------------------|
| `coredns_dns_requests_total` | Total query volume — watch for spikes |
| `coredns_dns_responses_total{rcode="SERVFAIL"}` | Server failures — should be near zero |
| `coredns_dns_responses_total{rcode="NXDOMAIN"}` | Non-existent domains — high count suggests misconfigured clients |
| `coredns_forward_requests_total` | Upstream forwarding volume |
| `coredns_forward_responses_total{rcode="SERVFAIL"}` | Upstream failures |
| `coredns_dns_request_duration_seconds` | Query latency — p99 should be under 100ms |
| `coredns_cache_hits_total` / `coredns_cache_misses_total` | Cache effectiveness |
| `coredns_panics_total` | CoreDNS panics — should be zero |

---

---

## Common Mistakes

| Mistake | Why It Fails | Instead |
|---------|--------------|---------|
| Testing DNS with `ping` instead of `nslookup` | `ping` failure may be ICMP blocked, not DNS | Use `nslookup`, `getent hosts`, or `dig` via `kubectl exec` to test DNS specifically |
| Deploying test pods to diagnose DNS | May lack permissions, creates resources, adds cleanup burden | Use `kubectl exec` into existing pods or rely on indirect checks (CoreDNS logs, health endpoints) |
| Assuming DNS is broken when the Service has no endpoints | DNS resolves the ClusterIP correctly, but no pods back the Service | Check `kubectl get endpoints` before blaming DNS |
| Editing the CoreDNS ConfigMap without the `reload` plugin | Changes take effect only after pod restart | Verify `reload` is in the Corefile, or restart CoreDNS pods after edits |
| Using `dnsPolicy: Default` and expecting cluster DNS to work | `Default` uses the node's DNS, not CoreDNS | Check `dnsPolicy` — recommend `ClusterFirst` for pods that need service discovery |
| Ignoring ndots when debugging slow external lookups | Each external name generates up to 5 queries with ndots:5 | Check ndots value; recommend reducing ndots or using FQDNs with trailing dot |
| Adding a NetworkPolicy without a DNS egress rule | All DNS blocked — every lookup times out | Check egress policies for missing UDP/TCP 53 rules |
| Restarting CoreDNS as the first troubleshooting step | Hides the evidence (logs, metrics) needed for diagnosis | Collect logs and check configuration before restarting |

---

## MCP Tools Available

When the appropriate MCP servers are connected, prefer these over raw kubectl where available:

- `mcp__flux-operator-mcp__get_kubernetes_resources` - Query CoreDNS deployment, pods, services, endpoints, configmaps
- `mcp__flux-operator-mcp__get_kubernetes_logs` - Retrieve CoreDNS pod logs
- `mcp__flux-operator-mcp__get_kubernetes_metrics` - Check CoreDNS resource consumption

---

## Behavioural Guidelines

1. **Run the health check first** — Always complete the Quick DNS Health Check before deep-diving. Present the summary to the user so they see the overall picture.
2. **Never deploy test workloads** — Use `kubectl exec` into existing running pods for DNS testing. If no pods have DNS tools, use indirect methods (resolv.conf inspection, CoreDNS logs, health endpoints).
3. **Distinguish DNS failure from service failure** — If DNS resolves but the service is unreachable, the problem is not DNS. Check endpoints and connectivity.
4. **Check the Corefile before recommending changes** — Read and understand the current configuration before recommending modifications to the user.
5. **Never expose secrets** — List ConfigMap and Secret names. Never decode or print secret values.
6. **Fall back to indirect checks** — When `kubectl exec` is unavailable or pod images lack tools, CoreDNS health endpoints, logs, and infrastructure state (endpoints, service, pod status) provide strong evidence of DNS health.
7. **Consider ndots for performance issues** — Slow DNS is often not a CoreDNS problem but an ndots/search-domain expansion issue.
8. **Collect logs before restarting** — CoreDNS logs are ephemeral. Capture them before any restart.
9. **Check network policies early** — A missing DNS egress rule is one of the most common causes of DNS failure in policy-enforced namespaces.
10. **Recommend scaling before tuning** — If CoreDNS is overloaded, recommend adding replicas before adjusting cache sizes or Corefile plugins.
