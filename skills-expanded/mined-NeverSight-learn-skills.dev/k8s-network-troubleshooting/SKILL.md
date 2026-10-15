---
name: k8s-network-troubleshooting
description: Use when pods cannot reach other pods or services, connections are timing out or refused, network policies may be blocking traffic, ingress is not routing, egress to external services fails, or Istio service mesh is causing connectivity issues
---

# Kubernetes Network Troubleshooting

Diagnose network connectivity issues within and outside a Kubernetes cluster. Covers pod-to-pod, pod-to-service, ingress, egress, network policies, and Istio service mesh.

## Keywords

network, connectivity, connection refused, timeout, unreachable, curl, wget, pod-to-pod, pod-to-service, service mesh, istio, envoy, sidecar, mTLS, network policy, ingress, egress, ClusterIP, NodePort, LoadBalancer, CNI, kube-proxy, iptables, calico, cilium, VirtualService, DestinationRule, Gateway

## When to Use This Skill

- Pods cannot reach other pods or services (connection refused / timeout)
- Connection timeouts between services that were previously working
- Ingress controller is not routing external traffic to services
- Egress to external APIs or the internet is blocked
- Intermittent connectivity failures between services
- Istio sidecar injection issues or mTLS failures
- Traffic routing behaves differently than VirtualService rules specify
- Services are reachable by ClusterIP but not by name (check DNS first)
- NodePort or LoadBalancer services are not externally accessible

### When NOT to Use

- DNS resolution failures (pods can't resolve names) → use [k8s-dns-troubleshooting](../k8s-dns-troubleshooting)
- Pod crashes, scheduling failures, or OOMKills → use [k8s-namespace-troubleshooting](../k8s-namespace-troubleshooting)
- TLS certificate issuance or renewal failures → use [cert-manager-troubleshooting](../cert-manager-troubleshooting)

**Note:** If connections fail with "could not resolve host", the problem is DNS, not network. Start with [k8s-dns-troubleshooting](../k8s-dns-troubleshooting). If DNS resolves but the connection still fails, return here.

## Related Skills

- [k8s-dns-troubleshooting](../k8s-dns-troubleshooting) - DNS resolution and CoreDNS issues
- [k8s-namespace-troubleshooting](../k8s-namespace-troubleshooting) - General namespace diagnosis
- [k8s-platform-operations](../k8s-platform-operations) - Cluster-wide health checks
- [k8s-security-hardening](../k8s-security-hardening) - Network policies and security controls
- [Shared: Network Policies](../_shared/references/network-policies.md)

## Quick Reference

| Task | Command |
|------|---------|
| Test connectivity from a pod | `kubectl exec -n ${NS} ${POD} -- wget -qO- --timeout=5 http://${TARGET}:${PORT} 2>&1` |
| Check service endpoints | `kubectl get endpoints ${SVC} -n ${NS}` |
| List network policies | `kubectl get networkpolicies -n ${NS}` |
| Describe a service | `kubectl describe svc ${SVC} -n ${NS}` |
| Check pod IP | `kubectl get pod ${POD} -n ${NS} -o jsonpath='{.status.podIP}'` |
| Check Istio sidecar status | `kubectl get pod ${POD} -n ${NS} -o jsonpath='{.spec.containers[*].name}'` |
| Envoy proxy logs | `kubectl logs ${POD} -n ${NS} -c istio-proxy --tail=100` |
| Ingress resources | `kubectl get ingress -A` |
| kube-proxy pods | `kubectl get pods -n kube-system -l k8s-app=kube-proxy` |
| CNI pods | `kubectl get pods -A -l k8s-app=calico-node` or `kubectl get pods -A -l k8s-app=cilium` |

---

## Quick Network Health Check

Run this checklist first. Complete all checks before drawing conclusions.

### Step 1: Pod-to-Pod (Same Namespace)

```bash
# Find two running pods in the same namespace
kubectl get pods -n ${NS} --field-selector=status.phase=Running -o wide

# Get the IP of the target pod
TARGET_IP=$(kubectl get pod ${TARGET_POD} -n ${NS} -o jsonpath='{.status.podIP}')

# Test connectivity from source pod to target pod IP
kubectl exec -n ${NS} ${SOURCE_POD} -- wget -qO- --timeout=5 http://${TARGET_IP}:${PORT} 2>&1
```

### Step 2: Pod-to-Service (Same Namespace)

```bash
# Verify the service exists and has a ClusterIP
kubectl get svc ${SVC} -n ${NS}

# Verify endpoints are populated
kubectl get endpoints ${SVC} -n ${NS}

# Test connectivity via service name
kubectl exec -n ${NS} ${POD} -- wget -qO- --timeout=5 http://${SVC}:${SVC_PORT} 2>&1
```

### Step 3: Pod-to-Service (Cross Namespace)

```bash
# Test connectivity to a service in a different namespace
kubectl exec -n ${NS} ${POD} -- wget -qO- --timeout=5 http://${SVC}.${TARGET_NS}.svc.cluster.local:${SVC_PORT} 2>&1
```

### Step 4: Pod-to-External

Requires internet access from the cluster. Substitute any reachable external endpoint in air-gapped or restricted environments.

```bash
# Test internet connectivity
kubectl exec -n ${NS} ${POD} -- wget -qO- --timeout=5 http://httpbin.org/get 2>&1 | head -5

# Test specific external endpoint
kubectl exec -n ${NS} ${POD} -- wget -qO- --timeout=5 https://${EXTERNAL_HOST} 2>&1 | head -3
```

### Step 5: Network Policies

```bash
# Check for network policies in the namespace
kubectl get networkpolicies -n ${NS}

# Check for policies that restrict egress or ingress
kubectl get networkpolicies -n ${NS} -o json | \
  jq -r '.items[] | "\(.metadata.name)\tTypes: \(.spec.policyTypes // ["Ingress"] | join(", "))"'
```

### Step 6: Istio Sidecar (If Applicable)

```bash
# Check if the pod has an istio-proxy sidecar container
kubectl get pod ${POD} -n ${NS} -o jsonpath='{.spec.containers[*].name}' | tr ' ' '\n' | grep istio-proxy

# Check if the namespace has sidecar injection enabled
kubectl get namespace ${NS} -o jsonpath='{.metadata.labels.istio-injection}'
```

### Health Summary Template

Present results using this format:

```markdown
## Network Health Summary

| Check | Status | Detail |
|-------|--------|--------|
| Pod-to-pod (same NS) | PASS/FAIL/SKIP | Connected / Timeout / Refused / Not tested |
| Pod-to-service (same NS) | PASS/FAIL/SKIP | Endpoints: X, Response: OK / Timeout / Refused |
| Pod-to-service (cross NS) | PASS/FAIL/SKIP | Connected / Blocked / Not tested |
| Pod-to-external | PASS/FAIL/SKIP | Connected / Timeout / Blocked |
| Network policies | NONE/PRESENT | X policies found (Y with egress rules) |
| Istio sidecar injected | YES/NO/N/A | istio-proxy present / absent / Istio not installed |

**Overall: HEALTHY / DEGRADED / UNHEALTHY**
```

- **HEALTHY** — All connectivity checks pass
- **DEGRADED** — Some paths work, others fail (targeted issue)
- **UNHEALTHY** — Broad connectivity failure

---

## Diagnostic Workflow

Use this decision tree after the health check identifies failures.

```
Connection failing?
├─ Same namespace pod-to-pod fails?
│   ├─ Both pods on same node → CNI issue (Section 7)
│   ├─ Pods on different nodes → CNI cross-node or overlay issue (Section 7)
│   └─ Network policy blocking → Ingress policy on target (Section 5)
├─ Service connection fails but pod IP works?
│   ├─ Endpoints empty → No ready pods backing the service (Section 2)
│   ├─ Port mismatch → Service port vs targetPort vs containerPort (Section 2)
│   ├─ kube-proxy not running → No iptables/IPVS rules for ClusterIP (Section 7)
│   └─ Istio routing override → VirtualService or DestinationRule (Section 6)
├─ Cross-namespace fails but same-namespace works?
│   ├─ Network policy restricting cross-NS traffic → Egress or ingress rules (Section 5)
│   ├─ Istio mTLS mode mismatch → STRICT on one side, no sidecar on other (Section 6)
│   └─ DNS issue → Resolve ${SVC}.${NS}.svc.cluster.local (→ k8s-dns-troubleshooting)
├─ External/egress fails?
│   ├─ All pods affected → Cluster-wide egress blocked (Section 3)
│   ├─ Only some pods → Egress network policy (Section 5)
│   ├─ Istio sidecar blocking → Outbound traffic policy (Section 6)
│   └─ NAT/SNAT issue → Node cannot route to internet (Section 3)
├─ Ingress fails?
│   ├─ Ingress controller not running → Controller pods down (Section 4)
│   ├─ Ingress resource misconfigured → Backend service or path (Section 4)
│   ├─ TLS termination failing → Certificate or secret issue (Section 4)
│   └─ Istio Gateway misconfigured → Gateway or VirtualService (Section 6)
└─ Intermittent failures?
    ├─ Some requests succeed → Load balancing to unhealthy pod (Section 2)
    ├─ Timeouts then recovery → Conntrack table full or CNI flap (Section 7)
    └─ Istio circuit breaking → DestinationRule outlier detection (Section 6)
```

---

## Section 1: Pod-to-Pod Connectivity

Direct pod-to-pod communication uses pod IPs, bypassing services and kube-proxy.

### Verifying Pod IPs and Placement

```bash
# Get pod IPs and node placement
kubectl get pods -n ${NS} -o wide

# Confirm pods have IPs assigned (no IP = CNI problem)
kubectl get pod ${POD} -n ${NS} -o jsonpath='{.status.podIP}'

# Check if pods are on the same or different nodes
kubectl get pod ${SOURCE_POD} -n ${NS} -o jsonpath='{.spec.nodeName}'
kubectl get pod ${TARGET_POD} -n ${NS} -o jsonpath='{.spec.nodeName}'
```

### Testing Pod-to-Pod

```bash
# Direct connectivity test using pod IP
TARGET_IP=$(kubectl get pod ${TARGET_POD} -n ${NS} -o jsonpath='{.status.podIP}')
kubectl exec -n ${NS} ${SOURCE_POD} -- wget -qO- --timeout=5 http://${TARGET_IP}:${PORT} 2>&1

# If wget is unavailable, test with /dev/tcp (bash-based images)
kubectl exec -n ${NS} ${SOURCE_POD} -- bash -c "echo > /dev/tcp/${TARGET_IP}/${PORT} && echo OPEN || echo CLOSED" 2>&1

# Check if the target pod is listening on the expected port
kubectl exec -n ${NS} ${TARGET_POD} -- sh -c 'netstat -tlnp 2>/dev/null || ss -tlnp 2>/dev/null' | head -20
```

### Same Node vs Cross Node

```bash
# If same-node pod-to-pod fails: CNI plugin local routing is broken
# If cross-node works: unlikely to be CNI, check network policy on target

# If cross-node pod-to-pod fails: overlay network issue
# Check CNI pods are running on both nodes (use the label for the installed CNI)
kubectl get pods -n kube-system -l k8s-app=calico-node -o wide --field-selector spec.nodeName=${NODE1} 2>/dev/null
kubectl get pods -n kube-system -l k8s-app=cilium -o wide --field-selector spec.nodeName=${NODE1} 2>/dev/null
```

### Interpreting Failures

| Symptom | Likely Cause |
|---------|-------------|
| `Connection refused` | Target pod is not listening on that port |
| `Connection timed out` | Network path blocked (policy, CNI, or routing) |
| No pod IP assigned | CNI plugin failed to allocate an IP |
| Works same-node, fails cross-node | Overlay/tunnel issue between nodes |

---

## Section 2: Pod-to-Service Connectivity

Services route traffic through ClusterIP (kube-proxy rules) to pod endpoints.

### Checking Service Configuration

```bash
# Service details: ClusterIP, ports, selector
kubectl describe svc ${SVC} -n ${NS}

# Verify selector matches pod labels
SVC_SELECTOR=$(kubectl get svc ${SVC} -n ${NS} -o jsonpath='{.spec.selector}')
echo "Service selector: ${SVC_SELECTOR}"
kubectl get pods -n ${NS} -l "${LABEL_KEY}=${LABEL_VALUE}" -o wide

# Port mapping — the three ports that must align
kubectl get svc ${SVC} -n ${NS} -o jsonpath='{range .spec.ports[*]}port:{.port} targetPort:{.targetPort} protocol:{.protocol}{"\n"}{end}'
```

### The Three-Port Model

```
Client → Service:port → Pod:targetPort → Container listens on containerPort

- service.spec.ports[].port      = port clients connect to
- service.spec.ports[].targetPort = port on the pod (defaults to .port if omitted)
- container.ports[].containerPort = port the app listens on (must match targetPort)
```

A mismatch between `targetPort` and the actual port the container listens on is a common cause of "connection refused" after DNS resolves.

### Checking Endpoints

```bash
# Endpoints show which pod IPs back the service
kubectl get endpoints ${SVC} -n ${NS}

# Detailed endpoint view
kubectl get endpoints ${SVC} -n ${NS} -o yaml

# If using EndpointSlices (Kubernetes 1.21+)
kubectl get endpointslices -n ${NS} -l kubernetes.io/service-name=${SVC}
```

### Empty Endpoints Causes

| Cause | Diagnostic |
|-------|-----------|
| No pods match selector | Compare `svc.spec.selector` with `pod.metadata.labels` |
| Pods not ready | Check `kubectl get pods -n ${NS}` — pods must pass readiness probes |
| Wrong namespace | Service and pods must be in the same namespace (for selector matching) |
| Readiness probe failing | `kubectl describe pod ${POD} -n ${NS}` — check probe events |

### Service Types

```bash
# ClusterIP (default) — internal only
kubectl get svc ${SVC} -n ${NS} -o jsonpath='{.spec.type}'

# NodePort — verify port allocation
kubectl get svc ${SVC} -n ${NS} -o jsonpath='{range .spec.ports[*]}nodePort:{.nodePort}{"\n"}{end}'

# LoadBalancer — check external IP assignment
kubectl get svc ${SVC} -n ${NS} -o jsonpath='{.status.loadBalancer.ingress[0].ip}'

# If LoadBalancer shows <pending>, the cloud controller hasn't provisioned the LB
kubectl describe svc ${SVC} -n ${NS} | grep -A5 Events
```

### Testing Service Connectivity

```bash
# Via service name (tests DNS + kube-proxy + pod)
kubectl exec -n ${NS} ${POD} -- wget -qO- --timeout=5 http://${SVC}:${SVC_PORT} 2>&1

# Via ClusterIP directly (bypasses DNS, tests kube-proxy + pod)
CLUSTER_IP=$(kubectl get svc ${SVC} -n ${NS} -o jsonpath='{.spec.clusterIP}')
kubectl exec -n ${NS} ${POD} -- wget -qO- --timeout=5 http://${CLUSTER_IP}:${SVC_PORT} 2>&1

# If service works by ClusterIP but not by name → DNS problem
# If service works by pod IP but not by ClusterIP → kube-proxy problem
# If neither works → pod/network problem
```

---

## Section 3: Egress / External Connectivity

Pods reaching endpoints outside the cluster.

### Testing External Connectivity

These examples use `httpbin.org` as a public test endpoint. Substitute any reachable external host in air-gapped or restricted environments.

```bash
# Test general internet access
kubectl exec -n ${NS} ${POD} -- wget -qO- --timeout=5 http://httpbin.org/get 2>&1 | head -5

# Test specific external API
kubectl exec -n ${NS} ${POD} -- wget -qO- --timeout=5 https://${EXTERNAL_HOST}${PATH} 2>&1 | head -5

# If wget/curl unavailable, test TCP connectivity
kubectl exec -n ${NS} ${POD} -- sh -c "echo | nc -w5 ${EXTERNAL_HOST} ${PORT}" 2>&1
```

### Common Egress Failures

| Symptom | Likely Cause | Diagnostic |
|---------|-------------|-----------|
| All pods can't reach external | Cluster-wide egress issue | Check node internet access, NAT gateway |
| Only some pods blocked | Egress network policy | `kubectl get networkpolicies -n ${NS}` |
| HTTPS fails, HTTP works | TLS interception or proxy | Check for corporate proxy env vars |
| Timeout to specific host | Firewall or security group | Check cloud provider firewall rules |
| `Connection refused` to external | Target service rejecting | Verify external service is up |

### NAT and SNAT

```bash
# Pods typically use the node's IP for outbound traffic (SNAT)
# Verify the node has internet access

# Check if a pod sees the expected source IP
kubectl exec -n ${NS} ${POD} -- wget -qO- --timeout=5 http://httpbin.org/ip 2>&1

# If pods use an egress gateway (Istio or CNI-specific), check its health
kubectl get pods -n istio-system -l istio=egressgateway 2>/dev/null
```

### Proxy Configuration

```bash
# Check if pods expect a proxy
kubectl exec -n ${NS} ${POD} -- sh -c 'echo "HTTP_PROXY=$HTTP_PROXY HTTPS_PROXY=$HTTPS_PROXY NO_PROXY=$NO_PROXY"'

# Check if cluster-internal traffic is excluded from proxy
# NO_PROXY should include: .svc,.svc.cluster.local,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16
```

---

## Section 4: Ingress Connectivity

External traffic reaching services through an ingress controller.

### Ingress Controller Health

```bash
# Find the ingress controller pods (common labels)
kubectl get pods -A -l app.kubernetes.io/name=ingress-nginx -o wide
kubectl get pods -A -l app=istio-ingressgateway -o wide
kubectl get pods -A -l app.kubernetes.io/name=traefik -o wide

# Check controller service (must have an external IP or be NodePort)
kubectl get svc -A | grep -E 'ingress|gateway'

# Controller logs
kubectl logs -n ${INGRESS_NS} -l app.kubernetes.io/name=ingress-nginx --tail=100
```

### Ingress Resource Configuration

```bash
# List all ingress resources
kubectl get ingress -A

# Describe a specific ingress
kubectl describe ingress ${INGRESS_NAME} -n ${NS}

# Check the backend service references
kubectl get ingress ${INGRESS_NAME} -n ${NS} -o jsonpath='{range .spec.rules[*]}{.host}{"\t"}{range .http.paths[*]}{.path}\t{.backend.service.name}:{.backend.service.port.number}{"\n"}{end}{end}'
```

### Common Ingress Failures

| Symptom | Likely Cause | Diagnostic |
|---------|-------------|-----------|
| 502 Bad Gateway | Backend service has no ready endpoints | Check `kubectl get endpoints ${BACKEND_SVC} -n ${NS}` |
| 503 Service Unavailable | Backend service doesn't exist | Verify service name and namespace in ingress spec |
| 404 Not Found | Path routing mismatch | Check `pathType` (Prefix vs Exact) and path values |
| Connection refused on port 80/443 | Ingress controller not running or no external IP | Check controller pods and service |
| TLS handshake failure | Wrong or missing TLS secret | `kubectl get secret ${TLS_SECRET} -n ${NS}` — verify it exists |
| Works by IP, not by hostname | DNS for the hostname not pointing to ingress | Check external DNS records |

### TLS Termination

```bash
# Verify the TLS secret exists and has data
kubectl get secret ${TLS_SECRET} -n ${NS} -o jsonpath='{.data}' | jq 'keys'

# Check ingress TLS configuration
kubectl get ingress ${INGRESS_NAME} -n ${NS} -o jsonpath='{.spec.tls}'
```

---

## Section 5: Network Policies

Network policies control traffic flow between pods and to/from external endpoints. Policies are enforced by the CNI plugin.

### Listing and Inspecting Policies

```bash
# All policies in a namespace
kubectl get networkpolicies -n ${NS}

# Policy details
kubectl describe networkpolicy ${POLICY_NAME} -n ${NS}

# Summary of all policies: name, pod selector, and policy types
kubectl get networkpolicies -n ${NS} -o json | \
  jq -r '.items[] | "\(.metadata.name)\tSelector: \(.spec.podSelector.matchLabels // "all")\tTypes: \(.spec.policyTypes // ["Ingress"] | join(", "))"'
```

### How Network Policies Work

- No policies = all traffic allowed (default allow)
- Any policy selecting a pod = all traffic of that type (ingress/egress) is denied by default, except what the policy explicitly allows
- Multiple policies are additive (union of allowed traffic)
- Policies are namespace-scoped

### Identifying Blocking Policies

```bash
# Find policies that affect a specific pod
POD_LABELS=$(kubectl get pod ${POD} -n ${NS} -o json | jq -r '.metadata.labels | to_entries[] | "\(.key)=\(.value)"' | tr '\n' ',')
echo "Pod labels: ${POD_LABELS}"

# Check each policy's podSelector to see if it matches
kubectl get networkpolicies -n ${NS} -o json | \
  jq -r '.items[] | "\(.metadata.name): \(.spec.podSelector)"'

# Check for egress restrictions (blocks outbound traffic)
kubectl get networkpolicies -n ${NS} -o json | \
  jq -r '.items[] | select(.spec.policyTypes[]? == "Egress") | "\(.metadata.name): egress rules: \(.spec.egress // "DENY ALL")"'
```

### Common Policy Issues

| Problem | Symptom | Diagnostic |
|---------|---------|-----------|
| Egress policy without DNS exception | All DNS lookups timeout | Check if any egress policy lacks a rule for UDP/TCP 53 |
| Ingress policy missing a source namespace | Cross-NS traffic blocked | Check if ingress rules include a `namespaceSelector` for the source |
| Default-deny with no allow rules | All traffic blocked | List policies and verify allow rules exist for expected traffic paths |
| Policy selects wrong pods | Wrong pods are affected | Compare `podSelector.matchLabels` against actual pod labels |
| CNI doesn't support policies | Policies exist but aren't enforced | Verify CNI supports NetworkPolicy (e.g., Calico, Cilium — Flannel does not) |

### Verifying CNI Supports Network Policies

```bash
# Not all CNIs enforce policies — Flannel does not, Calico and Cilium do
# Check which CNI is installed
kubectl get pods -A | grep -E 'calico|cilium|weave|flannel|canal'

# If flannel: network policies exist but are NOT enforced
# If calico/cilium: policies are enforced
```

---

## Section 6: Istio Service Mesh

Istio adds a sidecar proxy (Envoy) to each pod, intercepting all traffic. This enables mTLS, traffic routing, and observability — but adds failure modes.

### Sidecar Injection Status

```bash
# Check if the pod has an istio-proxy container
kubectl get pod ${POD} -n ${NS} -o jsonpath='{.spec.containers[*].name}' | tr ' ' '\n'
# Look for "istio-proxy" in the output

# Check if the namespace has automatic injection enabled
kubectl get namespace ${NS} -o jsonpath='{.metadata.labels.istio-injection}'
# Should return "enabled" if auto-injection is on

# Check for per-pod injection annotation
kubectl get pod ${POD} -n ${NS} -o jsonpath='{.metadata.annotations.sidecar\.istio\.io/inject}'

# List all pods missing sidecars in an injection-enabled namespace
kubectl get pods -n ${NS} -o json | \
  jq -r '.items[] | select(.spec.containers[].name != "istio-proxy") | .metadata.name' | sort -u
```

### mTLS Mode (PeerAuthentication)

```bash
# Check mesh-wide mTLS policy
kubectl get peerauthentication -A

# Check namespace-level mTLS policy
kubectl get peerauthentication -n ${NS}

# Describe the policy to see the mode
kubectl describe peerauthentication ${POLICY_NAME} -n ${NS}
```

| Mode | Behavior | Impact |
|------|----------|--------|
| `PERMISSIVE` | Accepts both plaintext and mTLS | Safe default, allows gradual migration |
| `STRICT` | Requires mTLS for all traffic | Non-mesh pods (no sidecar) cannot communicate |
| `DISABLE` | No mTLS | Disables Istio mTLS for selected workloads |

**Common mTLS failures:**

- Pod without sidecar → service with `STRICT` mTLS = connection reset
- Service with sidecar → service without sidecar but `STRICT` on source = outbound failure
- Mixed mode across namespaces with strict policies = cross-namespace failures

```bash
# Quick check: does the destination pod have a sidecar?
kubectl get pod ${DEST_POD} -n ${DEST_NS} -o jsonpath='{.spec.containers[*].name}' | grep istio-proxy

# If STRICT mode and destination has no sidecar, that's the problem
```

### VirtualService and DestinationRule

```bash
# List VirtualServices in the namespace
kubectl get virtualservice -n ${NS}

# Describe a VirtualService — check hosts, routes, match rules
kubectl describe virtualservice ${VS_NAME} -n ${NS}

# List DestinationRules
kubectl get destinationrule -n ${NS}

# Check for traffic policies (circuit breaking, load balancing, mTLS settings)
kubectl describe destinationrule ${DR_NAME} -n ${NS}
```

**Common misconfigurations:**

| Problem | Symptom | Diagnostic |
|---------|---------|-----------|
| VirtualService host doesn't match service | Traffic not routed | Compare `spec.hosts[]` with actual service FQDN |
| Wrong port in VirtualService route | 503 or connection refused | Verify `route[].destination.port.number` matches service port |
| DestinationRule subset label mismatch | No healthy endpoints | Compare `subsets[].labels` with pod labels |
| Circuit breaker too aggressive | Intermittent 503s | Check `outlierDetection` settings in DestinationRule |
| Retry policy causing amplification | High latency, cascading failures | Check `retries` in VirtualService |

### Envoy Proxy Logs and Configuration

```bash
# View istio-proxy (Envoy) logs for a pod
kubectl logs ${POD} -n ${NS} -c istio-proxy --tail=100

# Filter for errors and connection failures
kubectl logs ${POD} -n ${NS} -c istio-proxy --tail=500 | grep -iE 'error|refused|timeout|reset|UH|UF|UC|NR'

# Envoy response flags in access logs:
# UH = no healthy upstream (no endpoints)
# UF = upstream connection failure
# UC = upstream connection termination
# NR = no route configured
# RL = rate limited
# DC = downstream connection termination

# Dump Envoy configuration (large output — filter as needed)
kubectl exec ${POD} -n ${NS} -c istio-proxy -- pilot-agent request GET /config_dump 2>/dev/null | head -100

# Check Envoy clusters (upstream endpoints as Envoy sees them)
kubectl exec ${POD} -n ${NS} -c istio-proxy -- pilot-agent request GET /clusters 2>/dev/null | grep "${TARGET_SVC}" | head -20

# Check Envoy listeners
kubectl exec ${POD} -n ${NS} -c istio-proxy -- pilot-agent request GET /listeners 2>/dev/null | head -50
```

### Istio Proxy Sync Status

```bash
# Check if istiod is running
kubectl get pods -n istio-system -l app=istiod

# Verify proxy config is synced (equivalent to istioctl proxy-status)
# Check istiod logs for push errors
kubectl logs -n istio-system -l app=istiod --tail=200 | grep -iE 'error|push|timeout|reject'

# Check proxy connection to istiod from a sidecar
kubectl exec ${POD} -n ${NS} -c istio-proxy -- pilot-agent request GET /ready 2>&1
```

### Gateway Configuration (Istio Ingress)

```bash
# List Istio Gateways
kubectl get gateway -A

# Describe the gateway
kubectl describe gateway ${GW_NAME} -n ${NS}

# Check the istio-ingressgateway pods
kubectl get pods -n istio-system -l istio=ingressgateway -o wide

# Check the ingressgateway service (external IP)
kubectl get svc istio-ingressgateway -n istio-system

# Verify VirtualService is bound to the gateway
kubectl get virtualservice -n ${NS} -o json | \
  jq -r '.items[] | "\(.metadata.name): gateways: \(.spec.gateways // "none")"'
```

### Common Istio Connectivity Patterns

| Scenario | Root Cause | Diagnostic |
|----------|-----------|-----------|
| Pod-to-service works without sidecar, fails with sidecar | mTLS STRICT on destination, no sidecar on source | Check PeerAuthentication mode and sidecar presence |
| 503 errors after deploying VirtualService | Route destination doesn't match a real service/subset | Verify destination host and subset labels |
| Intermittent 503 with `UH` flag | Outlier detection ejecting endpoints | Check DestinationRule `outlierDetection` settings |
| External service calls fail after mesh enrollment | Istio blocks unknown external traffic by default | Check `meshConfig.outboundTrafficPolicy.mode` (ALLOW_ANY vs REGISTRY_ONLY) |
| Traffic ignores VirtualService rules | VirtualService host doesn't match or not bound to gateway | Verify `spec.hosts` and `spec.gateways` |
| Connection reset between namespaces | PeerAuthentication mismatch across namespaces | Check per-namespace PeerAuthentication policies |

---

## Section 7: CNI and kube-proxy

The CNI plugin manages pod networking (IP allocation, routing). kube-proxy manages Service ClusterIP routing via iptables or IPVS rules.

### CNI Health

```bash
# Identify the CNI plugin
kubectl get pods -A | grep -E 'calico-node|cilium|weave-net|flannel|canal|kube-router'

# Check CNI pod status
kubectl get pods -n kube-system -l k8s-app=calico-node -o wide 2>/dev/null
kubectl get pods -n kube-system -l k8s-app=cilium -o wide 2>/dev/null

# CNI pod logs (pick the relevant one)
kubectl logs -n kube-system -l k8s-app=calico-node --tail=100 2>/dev/null | grep -iE 'error|fail|warn'
kubectl logs -n kube-system -l k8s-app=cilium --tail=100 2>/dev/null | grep -iE 'error|fail|warn'

# Check node status — NotReady often indicates CNI failure
kubectl get nodes -o wide
```

### kube-proxy

```bash
# kube-proxy pod status
kubectl get pods -n kube-system -l k8s-app=kube-proxy -o wide

# kube-proxy mode (iptables or IPVS)
kubectl get configmap kube-proxy -n kube-system -o jsonpath='{.data.config\.conf}' | grep mode

# kube-proxy logs
kubectl logs -n kube-system -l k8s-app=kube-proxy --tail=100 | grep -iE 'error|fail|warn'
```

### iptables Service Rules

These commands require direct node access (SSH or a node-shell pod). They cannot be run via `kubectl exec` into application pods.

```bash
# Check if iptables rules exist for a service ClusterIP
iptables-save | grep ${CLUSTER_IP}

# Count KUBE-SERVICES rules (should have one per service port)
iptables-save | grep KUBE-SERVICES | wc -l

# Check conntrack table size (full table causes connection drops)
cat /proc/sys/net/netfilter/nf_conntrack_count
cat /proc/sys/net/netfilter/nf_conntrack_max
```

### CNI and kube-proxy Issues

| Symptom | Likely Cause | Diagnostic |
|---------|-------------|-----------|
| Pod stuck in ContainerCreating | CNI failed to assign IP | `kubectl describe pod` — check events for CNI errors |
| Node NotReady | CNI plugin not running on node | Check CNI pods on that node |
| ClusterIP unreachable | kube-proxy not running or iptables rules missing | Check kube-proxy pods and logs |
| Intermittent connection drops | Conntrack table full | Compare `nf_conntrack_count` with `nf_conntrack_max` |
| Cross-node pod traffic fails | Overlay network (VXLAN/WireGuard/IPIP) misconfigured | Check CNI tunnel interface and node-to-node connectivity |

---

## Common Mistakes

| Mistake | Why It Fails | Instead |
|---------|--------------|---------|
| Assuming DNS failure when service has no endpoints | DNS resolves the ClusterIP correctly, but no pods back the service — connection refused | Check `kubectl get endpoints` before blaming DNS or network |
| Testing with `ping` instead of `wget`/`curl` | ICMP is often blocked by network policies; services don't respond to ping | Use `wget -qO- --timeout=5` or `curl --connect-timeout 5` to test TCP |
| Deploying test pods to diagnose | May lack permissions, creates resources, adds cleanup | Use `kubectl exec` into existing running pods |
| Ignoring the service port vs targetPort distinction | Client connects to service `port`, traffic goes to `targetPort` on the pod — a mismatch causes refused connections | Verify all three ports: service port, targetPort, and containerPort |
| Applying egress network policy without DNS exception | All DNS lookups timeout because UDP/TCP 53 is blocked | Check egress policies for missing UDP/TCP 53 rules |
| Blaming Istio before checking basics | Pod-to-pod and service fundamentals are broken regardless of mesh | Run the quick health check (non-Istio) first, then check Istio-specific issues |
| Checking PeerAuthentication without verifying sidecar presence | STRICT mTLS requires both sides to have sidecars | Confirm istio-proxy container exists in both source and destination pods |
| Restarting kube-proxy as first step | Hides the evidence (logs, metrics) and rarely fixes the real issue | Collect logs, check iptables rules, then restart if needed |

---

## MCP Tools Available

When the appropriate MCP servers are connected, prefer these over raw kubectl where available:

- `mcp__flux-operator-mcp__get_kubernetes_resources` - Query services, endpoints, pods, ingress, network policies, and Istio resources
- `mcp__flux-operator-mcp__get_kubernetes_logs` - Retrieve logs from application pods, istio-proxy sidecars, CNI pods, and kube-proxy
- `mcp__flux-operator-mcp__get_kubernetes_metrics` - Check resource consumption for CNI and kube-proxy pods

---

## Behavioural Guidelines

1. **Confirm DNS works first** — Before diagnosing network issues, verify DNS resolution is healthy. If pods can't resolve names, start with [k8s-dns-troubleshooting](../k8s-dns-troubleshooting).
2. **Run the health check first** — Complete the Quick Network Health Check before deep-diving. Present the summary so the user sees the overall picture.
3. **Never deploy test workloads** — Use `kubectl exec` into existing running pods. If no pods have network tools, use indirect methods (logs, endpoint checks, pod describe).
4. **Work from layer 3 up** — Verify pod IPs assigned → pod-to-pod works → service endpoints populated → service routing works → ingress configured → mesh rules correct.
5. **Distinguish service failure from network failure** — If endpoints are empty, the problem is the application (not ready) or label mismatch, not the network.
6. **Check network policies early** — Missing DNS egress rules and overly restrictive ingress rules are among the most common connectivity issues.
7. **Check Istio only after basics pass** — If pod-to-pod and service fundamentals are broken, Istio is not the cause. Diagnose the mesh layer only when non-mesh connectivity works.
8. **Never expose secrets** — List Secret names and ConfigMap keys. Never decode or print secret values.
9. **Collect logs before restarting** — Envoy, kube-proxy, and CNI logs are ephemeral. Capture them before any restart.
10. **Report what you find, not what to change** — This skill is diagnostic. Present findings and let the user decide on remediation.
