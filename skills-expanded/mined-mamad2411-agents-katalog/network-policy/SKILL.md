# Skill: Kubernetes Network Policies

## Purpose

Provide expert guidance on designing, implementing, and troubleshooting network policies in Kubernetes clusters. Covers native Kubernetes NetworkPolicy, Calico extended policies, and Cilium L7 policies with practical examples and common patterns for microsegmentation.

## Core Knowledge

### Kubernetes NetworkPolicy Fundamentals

Network policies are namespace-scoped resources that control traffic flow to and from pods. Without any NetworkPolicy, all pods accept traffic from any source (default allow-all).

**Key Concepts:**
- Policies are **additive** — multiple policies combine with OR logic (union of allowed traffic)
- A pod is **isolated** for a direction (ingress/egress) once any policy selects it for that direction
- Once isolated, only traffic explicitly allowed by a policy is permitted
- Policies select pods using `podSelector` (label matching)
- Empty `podSelector: {}` selects all pods in the namespace
- Policies are enforced by the CNI plugin — not by Kubernetes itself

**API Structure:**
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: policy-name
  namespace: target-namespace
spec:
  podSelector:          # Which pods this policy applies to
    matchLabels:
      app: web
  policyTypes:          # Which directions to enforce
    - Ingress
    - Egress
  ingress:              # Allowed inbound traffic rules
    - from:
        - podSelector: {}
        - namespaceSelector: {}
        - ipBlock: {}
      ports:
        - protocol: TCP
          port: 8080
  egress:               # Allowed outbound traffic rules
    - to:
        - podSelector: {}
      ports:
        - protocol: TCP
          port: 443
```

### Selector Mechanics

**podSelector** — Selects pods within the same namespace:
```yaml
from:
  - podSelector:
      matchLabels:
        role: frontend
```

**namespaceSelector** — Selects all pods in matching namespaces:
```yaml
from:
  - namespaceSelector:
      matchLabels:
        environment: production
```

**Combined selector (AND logic)** — Both conditions must be true:
```yaml
from:
  - podSelector:
      matchLabels:
        role: api
    namespaceSelector:
      matchLabels:
        team: backend
```

**Separate selectors (OR logic)** — Either condition allows traffic:
```yaml
from:
  - podSelector:
      matchLabels:
        role: api
  - namespaceSelector:
      matchLabels:
        team: backend
```

**ipBlock** — Allow from external CIDR ranges:
```yaml
from:
  - ipBlock:
      cidr: 10.0.0.0/8
      except:
        - 10.0.1.0/24
```

### Common Patterns

#### Pattern 1: Default Deny All Ingress

Isolate all pods in a namespace — deny all inbound traffic by default:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Ingress
```

#### Pattern 2: Default Deny All Egress

Deny all outbound traffic by default (careful — breaks DNS unless allowed):

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-egress
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Egress
```

#### Pattern 3: Allow DNS Egress (Required with deny-all egress)

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Egress
  egress:
    - to:
        - namespaceSelector: {}
          podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - protocol: UDP
          port: 53
        - protocol: TCP
          port: 53
```

#### Pattern 4: Namespace Isolation (Allow within namespace only)

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-same-namespace
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector: {}
```

#### Pattern 5: Allow Specific Pods to Communicate

Frontend → Backend on port 8080:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - protocol: TCP
          port: 8080
```

#### Pattern 6: Allow Ingress Controller Traffic

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-ingress-controller
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: web
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: ingress-nginx
          podSelector:
            matchLabels:
              app.kubernetes.io/name: ingress-nginx
      ports:
        - protocol: TCP
          port: 8080
```

#### Pattern 7: Allow Monitoring (Prometheus Scraping)

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-prometheus-scrape
  namespace: production
spec:
  podSelector:
    matchLabels:
      prometheus.io/scrape: "true"
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: monitoring
          podSelector:
            matchLabels:
              app: prometheus
      ports:
        - protocol: TCP
          port: 9090
        - protocol: TCP
          port: 8080
```

### Calico Network Policies

Calico extends the native Kubernetes NetworkPolicy with additional capabilities through its own CRDs.

#### Calico NetworkPolicy (Namespaced)

```yaml
apiVersion: projectcalico.org/v3
kind: NetworkPolicy
metadata:
  name: allow-api-ingress
  namespace: production
spec:
  selector: app == 'api-server'
  types:
    - Ingress
    - Egress
  ingress:
    - action: Allow
      protocol: TCP
      source:
        selector: role == 'frontend'
        namespaceSelector: environment == 'production'
      destination:
        ports:
          - 8443
  egress:
    - action: Allow
      protocol: TCP
      destination:
        selector: app == 'database'
        ports:
          - 5432
    - action: Allow
      protocol: UDP
      destination:
        selector: k8s-app == 'kube-dns'
        namespaceSelector: kubernetes.io/metadata.name == 'kube-system'
        ports:
          - 53
```

#### Calico GlobalNetworkPolicy (Cluster-wide)

```yaml
apiVersion: projectcalico.org/v3
kind: GlobalNetworkPolicy
metadata:
  name: deny-external-egress
spec:
  selector: environment == 'restricted'
  types:
    - Egress
  egress:
    # Allow cluster-internal traffic
    - action: Allow
      destination:
        nets:
          - 10.0.0.0/8
          - 172.16.0.0/12
          - 192.168.0.0/16
    # Allow DNS
    - action: Allow
      protocol: UDP
      destination:
        selector: k8s-app == 'kube-dns'
        namespaceSelector: kubernetes.io/metadata.name == 'kube-system'
        ports:
          - 53
    # Deny everything else
    - action: Deny
```

#### Calico — Service Account Based Policy

```yaml
apiVersion: projectcalico.org/v3
kind: NetworkPolicy
metadata:
  name: restrict-by-serviceaccount
  namespace: production
spec:
  selector: all()
  ingress:
    - action: Allow
      source:
        serviceAccounts:
          names:
            - api-service-account
            - worker-service-account
```

#### Calico — HTTP Method Matching (Application Layer)

```yaml
apiVersion: projectcalico.org/v3
kind: NetworkPolicy
metadata:
  name: allow-get-only
  namespace: production
spec:
  selector: app == 'readonly-api'
  types:
    - Ingress
  ingress:
    - action: Allow
      protocol: TCP
      http:
        methods:
          - GET
          - HEAD
      destination:
        ports:
          - 8080
```

#### Calico — DNS Policy (FQDN-based egress)

```yaml
apiVersion: projectcalico.org/v3
kind: GlobalNetworkPolicy
metadata:
  name: allow-external-apis
spec:
  selector: needs-external-api == 'true'
  types:
    - Egress
  egress:
    - action: Allow
      protocol: TCP
      destination:
        domains:
          - "api.github.com"
          - "*.amazonaws.com"
        ports:
          - 443
```

### Cilium CiliumNetworkPolicy

Cilium provides L3-L7 network policy enforcement using eBPF.

#### Basic L3/L4 Policy

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: allow-frontend-to-api
  namespace: production
spec:
  endpointSelector:
    matchLabels:
      app: api
  ingress:
    - fromEndpoints:
        - matchLabels:
            app: frontend
      toPorts:
        - ports:
            - port: "8080"
              protocol: TCP
```

#### L7 HTTP Policy (Path and Method filtering)

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: l7-api-policy
  namespace: production
spec:
  endpointSelector:
    matchLabels:
      app: api
  ingress:
    - fromEndpoints:
        - matchLabels:
            app: frontend
      toPorts:
        - ports:
            - port: "8080"
              protocol: TCP
          rules:
            http:
              - method: GET
                path: "/api/v1/users"
              - method: POST
                path: "/api/v1/users"
              - method: GET
                path: "/api/v1/health"
```

#### L7 gRPC Policy

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: grpc-policy
  namespace: production
spec:
  endpointSelector:
    matchLabels:
      app: grpc-service
  ingress:
    - fromEndpoints:
        - matchLabels:
            app: grpc-client
      toPorts:
        - ports:
            - port: "50051"
              protocol: TCP
          rules:
            http:
              - method: ""
                path: "/mypackage.MyService/GetResource"
```

#### L7 Kafka Policy

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: kafka-produce-only
  namespace: production
spec:
  endpointSelector:
    matchLabels:
      app: kafka-broker
  ingress:
    - fromEndpoints:
        - matchLabels:
            app: producer
      toPorts:
        - ports:
            - port: "9092"
              protocol: TCP
          rules:
            kafka:
              - apiKey: "produce"
                topic: "events"
              - apiKey: "metadata"
              - apiKey: "apiversions"
```

#### DNS-Based Egress Policy (Cilium)

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: allow-external-https
  namespace: production
spec:
  endpointSelector:
    matchLabels:
      app: web
  egress:
    - toEndpoints:
        - matchLabels:
            k8s:io.kubernetes.pod.namespace: kube-system
            k8s-app: kube-dns
      toPorts:
        - ports:
            - port: "53"
              protocol: ANY
          rules:
            dns:
              - matchPattern: "*.github.com"
              - matchName: "api.stripe.com"
    - toFQDNs:
        - matchPattern: "*.github.com"
        - matchName: "api.stripe.com"
      toPorts:
        - ports:
            - port: "443"
              protocol: TCP
```

#### CiliumClusterwideNetworkPolicy

```yaml
apiVersion: cilium.io/v2
kind: CiliumClusterwideNetworkPolicy
metadata:
  name: lock-down-host
spec:
  nodeSelector:
    matchLabels:
      node-role.kubernetes.io/worker: ""
  ingress:
    - fromEntities:
        - cluster
        - health
    - fromCIDR:
        - 10.0.0.0/8
      toPorts:
        - ports:
            - port: "22"
              protocol: TCP
```

## Cloud-Specific Considerations

### AKS
- Network policy engine must be chosen at cluster creation (cannot add later for Azure CNI traditional)
- Options: `--network-policy calico` or `--network-dataplane cilium`
- Azure NPM (Azure Network Policy Manager) — legacy option using iptables, being deprecated
- With Cilium dataplane: use CiliumNetworkPolicy CRDs for L7 features

### EKS
- No built-in network policy enforcement
- Install Calico or Cilium separately as DaemonSets
- AWS VPC CNI supports Security Groups for Pods (L3/L4 only, per-pod SGs)
- Calico policy-only mode is recommended alongside VPC CNI

### GKE
- Dataplane V2 includes built-in policy enforcement (Cilium-based)
- Standard Kubernetes NetworkPolicy works out of the box
- Network policy logging available (shows allow/deny verdicts)
- FQDN network policies supported natively

```bash
# GKE - Enable network policy logging
gcloud container clusters update CLUSTER_NAME \
  --enable-network-policy-logging
```

## Policy Design Strategy

### Recommended Approach: Default-Deny with Explicit Allow

1. **Start with default deny** in each namespace:
   ```yaml
   # Apply to every namespace
   default-deny-ingress + default-deny-egress
   ```

2. **Allow DNS** (critical — egress deny breaks name resolution):
   ```yaml
   allow-dns-egress for all pods
   ```

3. **Allow specific communication paths**:
   ```yaml
   frontend → api (port 8080)
   api → database (port 5432)
   api → cache (port 6379)
   ```

4. **Allow infrastructure** (monitoring, logging, ingress):
   ```yaml
   prometheus → all (scrape port)
   ingress-controller → web pods
   ```

### Policy Ordering and Precedence

- Kubernetes NetworkPolicy: purely additive, no ordering, no deny rules
- Calico: supports `order` field, explicit Deny actions, tiered policies
- Cilium: additive for allow, supports deny policies via `CiliumClusterwideNetworkPolicy`

### Calico Tiered Policies (Enterprise)

```yaml
apiVersion: projectcalico.org/v3
kind: Tier
metadata:
  name: security
spec:
  order: 100
---
apiVersion: projectcalico.org/v3
kind: Tier
metadata:
  name: platform
spec:
  order: 200
---
# Security team policies take precedence
apiVersion: projectcalico.org/v3
kind: GlobalNetworkPolicy
metadata:
  name: security.block-known-bad
spec:
  tier: security
  order: 10
  selector: all()
  types:
    - Egress
  egress:
    - action: Deny
      destination:
        nets:
          - 198.51.100.0/24  # Known malicious range
    - action: Pass  # Pass to next tier for everything else
```

## Troubleshooting Policy Enforcement

### Step 1: Verify Policy Engine Is Running

```bash
# Check for CNI pods
kubectl get pods -n kube-system | grep -E "calico|cilium|azure-npm"

# Calico
kubectl get tigerastatus

# Cilium
kubectl -n kube-system exec ds/cilium -- cilium status
```

### Step 2: List Policies Affecting a Pod

```bash
# Kubernetes native policies in namespace
kubectl get networkpolicies -n production

# Calico policies
kubectl get networkpolicies.p -n production   # Calico namespaced
kubectl get globalnetworkpolicies.p           # Calico global

# Cilium policies
kubectl get ciliumnetworkpolicies -n production
kubectl get ciliumclusterwidenetworkpolicies
```

### Step 3: Test Connectivity

```bash
# From a debug pod
kubectl run nettest --rm -it --image=nicolaka/netshoot -- bash
# Inside: curl, nslookup, ping, traceroute

# Specific pod-to-pod test
kubectl exec -it frontend-pod -- curl -v http://backend-svc:8080/health
```

### Step 4: Check Policy Verdicts

```bash
# Cilium - monitor traffic in real-time
kubectl -n kube-system exec ds/cilium -- cilium monitor --type policy-verdict

# Cilium - Hubble flow observation
kubectl -n kube-system exec ds/cilium -- hubble observe \
  --namespace production \
  --verdict DROPPED

# Calico - check Felix logs
kubectl logs -n kube-system -l k8s-app=calico-node | grep -i deny
```

### Step 5: Common Issues

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| All traffic blocked after policy | Missing DNS egress allow | Add allow-dns policy |
| Ingress works but response fails | Egress policy missing return path | K8s policies are stateful — check egress rules |
| Policy not taking effect | CNI doesn't support policies | Verify policy engine DaemonSet is running |
| Inter-namespace traffic blocked | Missing namespaceSelector | Add namespace labels and selectors |
| Health checks failing | LB health probes blocked | Allow source CIDR of cloud LB |

### Step 6: Validate Policies with Dry-Run Tools

```bash
# Cilium policy dry-run
kubectl -n kube-system exec ds/cilium -- \
  cilium policy get -o jsonpath='{.policy.allowed}'

# Network policy visualization
# Use tools like: https://editor.networkpolicy.io/
```

---

**Analysis only — verify against vendor documentation before applying.**
