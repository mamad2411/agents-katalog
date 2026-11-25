---
name: service-mesh
description: Design and implement service mesh architecture using Istio or Linkerd. Outputs traffic management config, mTLS setup, observability pipelines, circuit breakers, and canary deployment policies.
argument-hint: [Kubernetes cluster setup, service count, observability requirements, security requirements]
allowed-tools: Read, Write, Bash
---

# Service Mesh Architecture

A service mesh moves cross-cutting concerns — mTLS, retries, circuit breakers, distributed tracing — out of application code and into the infrastructure layer. Services get reliability and security for free; developers write business logic.

## When to Use a Service Mesh

| Scenario | Recommendation |
|----------|---------------|
| <5 services, simple needs | Don't — use HTTP client libraries |
| 5-20 services, growing team | Consider Linkerd (simpler) |
| 20+ services, strict security requirements | Istio (more powerful) |
| Multi-cluster, multi-cloud | Istio with federation |
| Kubernetes-native, minimal overhead | Linkerd 2.x |

## Process

1. **Install control plane** — Istio or Linkerd on the cluster.
2. **Enable sidecar injection** — namespace-level automatic injection.
3. **Configure mTLS** — enforce STRICT mode for service-to-service.
4. **Define traffic policies** — retries, timeouts, circuit breakers per service.
5. **Set up observability** — Prometheus, Jaeger, Kiali integration.
6. **Create canary routing** — weight-based traffic splitting for deployments.
7. **Define authorization policies** — which services can talk to which.

## Output Format

### Istio Installation

```bash
# Install Istio with default profile
istioctl install --set profile=default -y

# Verify
istioctl verify-install

# Enable auto injection in namespace
kubectl label namespace production istio-injection=enabled --overwrite

# Install observability add-ons
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/prometheus.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/grafana.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/jaeger.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/kiali.yaml
```

### mTLS Configuration

```yaml
# Enforce strict mTLS across the entire mesh
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system  # Mesh-wide policy
spec:
  mtls:
    mode: STRICT
---
# Allow specific services to accept plain HTTP (e.g., health check endpoints)
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: order-service-permissive-health
  namespace: production
spec:
  selector:
    matchLabels:
      app: order-service
  mtls:
    mode: STRICT
  portLevelMtls:
    8080:          # Main port: strict
      mode: STRICT
    8081:          # Health check port: permissive
      mode: PERMISSIVE
```

### Authorization Policies

```yaml
# Deny all by default — then explicitly allow
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: deny-all
  namespace: production
spec: {}  # Empty spec = deny everything
---
# Allow order-service to call inventory-service
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: inventory-service-authz
  namespace: production
spec:
  selector:
    matchLabels:
      app: inventory-service
  action: ALLOW
  rules:
    - from:
        - source:
            principals:
              - "cluster.local/ns/production/sa/order-service"  # Service account
      to:
        - operation:
            methods: ["GET", "POST"]
            paths: ["/inventory/*"]
---
# Allow ingress gateway to reach frontend
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: frontend-authz
  namespace: production
spec:
  selector:
    matchLabels:
      app: frontend
  action: ALLOW
  rules:
    - from:
        - source:
            namespaces: ["istio-system"]  # Ingress gateway namespace
```

### Traffic Management

```yaml
# DestinationRule — load balancing, circuit breaker, connection pool
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: order-service
  namespace: production
spec:
  host: order-service
  trafficPolicy:
    # Load balancing
    loadBalancer:
      simple: LEAST_CONN
    
    # Connection pool limits (prevent cascading failures)
    connectionPool:
      tcp:
        maxConnections: 100
        connectTimeout: 3s
      http:
        h2UpgradePolicy: UPGRADE
        http1MaxPendingRequests: 100
        http2MaxRequests: 1000
        maxRequestsPerConnection: 10
    
    # Circuit breaker
    outlierDetection:
      consecutiveGatewayErrors: 5       # Open circuit after 5 consecutive 5xx
      consecutive5xxErrors: 5
      interval: 10s                     # Check every 10 seconds
      baseEjectionTime: 30s             # Eject unhealthy hosts for 30s
      maxEjectionPercent: 50            # Never eject more than 50% of hosts
      minHealthPercent: 30              # Keep at least 30% of hosts
  
  # Subsets for canary deployments
  subsets:
    - name: stable
      labels:
        version: stable
    - name: canary
      labels:
        version: canary
      trafficPolicy:
        connectionPool:
          http:
            http1MaxPendingRequests: 10   # Limit canary traffic
---
# VirtualService — routing, retries, timeouts, fault injection
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: order-service
  namespace: production
spec:
  hosts:
    - order-service
  http:
    - match:
        - headers:
            x-canary:
              exact: "true"   # Route beta users to canary
      route:
        - destination:
            host: order-service
            subset: canary
    
    - route:
        # Canary deployment: 10% to new version
        - destination:
            host: order-service
            subset: canary
          weight: 10
        - destination:
            host: order-service
            subset: stable
          weight: 90
      
      # Retry configuration
      retries:
        attempts: 3
        perTryTimeout: 5s
        retryOn: "gateway-error,connect-failure,retriable-4xx"
      
      # Request timeout
      timeout: 15s
      
      # Fault injection (for chaos testing — disable in production)
      # fault:
      #   delay:
      #     percentage:
      #       value: 5.0
      #     fixedDelay: 2s
      #   abort:
      #     percentage:
      #       value: 1.0
      #     httpStatus: 500
```

### Ingress Gateway

```yaml
# Gateway — expose services to external traffic
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: main-gateway
  namespace: istio-system
spec:
  selector:
    istio: ingressgateway
  servers:
    - port:
        number: 443
        name: https
        protocol: HTTPS
      tls:
        mode: SIMPLE
        credentialName: api-example-com-tls   # Kubernetes TLS secret
      hosts:
        - api.example.com
    - port:
        number: 80
        name: http
        protocol: HTTP
      hosts:
        - api.example.com
      tls:
        httpsRedirect: true   # Redirect HTTP → HTTPS
---
# VirtualService for external traffic
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: external-routing
  namespace: production
spec:
  hosts:
    - api.example.com
  gateways:
    - istio-system/main-gateway
  http:
    - match:
        - uri:
            prefix: "/api/v1/orders"
      route:
        - destination:
            host: order-service
            port:
              number: 80
    - match:
        - uri:
            prefix: "/api/v1/users"
      route:
        - destination:
            host: user-service
            port:
              number: 80
```

### Observability Configuration

```yaml
# Telemetry — customize metrics, tracing, logging
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: mesh-default
  namespace: istio-system
spec:
  # Distributed tracing
  tracing:
    - providers:
        - name: jaeger
      randomSamplingPercentage: 1.0   # 1% sampling in production
      customTags:
        environment:
          literal:
            value: production
        version:
          header:
            name: x-app-version
  
  # Access logging
  accessLogging:
    - providers:
        - name: envoy
      filter:
        expression: "response.code >= 400"   # Only log errors
  
  # Metrics
  metrics:
    - providers:
        - name: prometheus
      overrides:
        - match:
            metric: REQUEST_COUNT
            mode: CLIENT_AND_SERVER
          tagOverrides:
            destination_service:
              operation: UPSERT
              value: "destination.service.name | 'unknown'"
```

### Linkerd Alternative (Simpler)

```bash
# Install Linkerd
curl -fsL https://run.linkerd.io/install | sh
linkerd install --crds | kubectl apply -f -
linkerd install | kubectl apply -f -
linkerd check

# Enable for a deployment
kubectl get deploy -n production -o yaml \
  | linkerd inject - \
  | kubectl apply -f -

# Service profile (retries, timeouts)
kubectl apply -f - <<EOF
apiVersion: linkerd.io/v1alpha2
kind: ServiceProfile
metadata:
  name: order-service.production.svc.cluster.local
  namespace: production
spec:
  routes:
    - name: POST /orders
      condition:
        method: POST
        pathRegex: /orders
      isRetryable: false   # Don't retry non-idempotent mutations
      timeout: 10s
    - name: GET /orders
      condition:
        method: GET
        pathRegex: /orders/.*
      isRetryable: true
      timeout: 5s
      retryBudget:
        retryRatio: 0.2    # Up to 20% of requests can be retries
        minRetriesPerSecond: 10
        ttl: 10s
EOF

# Traffic splitting (canary)
kubectl apply -f - <<EOF
apiVersion: split.smi-spec.io/v1alpha1
kind: TrafficSplit
metadata:
  name: order-service-canary
  namespace: production
spec:
  service: order-service
  backends:
    - service: order-service-stable
      weight: 90
    - service: order-service-canary
      weight: 10
EOF
```

## Rules

- **Deny-all authorization by default** — explicitly allow only what's needed.
- **STRICT mTLS everywhere** — PERMISSIVE mode defeats the security benefit.
- **Circuit breakers per downstream** — tune thresholds per service's SLO, not one-size-fits-all.
- **Don't retry non-idempotent requests** — POST/DELETE retries without idempotency cause duplicates.
- **Sample traces, don't log all** — 1-5% sampling in production; 100% only in dev/staging.
- **Test fault injection in staging** — mesh-level fault injection (delay, abort) is safer than chaos tools.
- **Service accounts per service** — each workload needs its own service account for fine-grained RBAC.
- **Monitor data plane CPU** — Envoy sidecars add latency and CPU overhead; baseline before rollout.
- **Canary before rollout** — use VirtualService weight-based routing instead of Deployment replicas for canary.
- **Linkerd for simplicity, Istio for power** — don't default to Istio if Linkerd's feature set is sufficient.
