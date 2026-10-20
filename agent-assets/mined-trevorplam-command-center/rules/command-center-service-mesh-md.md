---
description: Run Service Mesh and Traffic Management Standards Check
globs: ['**/istio/**/*.yaml', '**/linkerd/**/*.yaml', '**/consul/**/*.yaml', 'helm/**/*.yaml']
---

# Infrastructure: Service Mesh & Traffic Management Standards

<audit_rules>

- You MUST implement proper service mesh configuration for traffic management and security.
- You MUST configure mTLS (mutual TLS) for all inter-service communication.
- You MUST implement traffic splitting and canary deployments for safe rollouts.
- You MUST configure circuit breaking and outlier detection for resilience.
- You MUST implement proper observability with distributed tracing and metrics collection.
- You MUST configure retry policies and timeouts for service communication.
- You MUST implement proper access control with service-to-service authentication.
- You MUST ensure proper ingress/egress gateway configuration for edge traffic.
- You MUST configure health checks and readiness probes for service mesh endpoints.
- You MUST implement proper traffic mirroring for testing and debugging.
  </audit_rules>

<example_good>

```yaml
# Istio Service Mesh Configuration
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: user-service
spec:
  hosts:
    - user-service
  http:
    - match:
        - headers:
          canary:
            exact: 'true'
      route:
        - destination:
            host: user-service
            subset: v2
          weight: 100
    - route:
        - destination:
            host: user-service
            subset: v1
          weight: 90
        - destination:
            host: user-service
            subset: v2
          weight: 10
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: user-service
spec:
  host: user-service
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 50
        maxRequestsPerConnection: 10
    loadBalancer:
      simple: LEAST_CONN
    circuitBreaker:
      consecutiveErrors: 3
      interval: 30s
      baseEjectionTime: 30s
    tls:
      mode: ISTIO_MUTUAL
  subsets:
    - name: v1
      labels:
        version: v1
    - name: v2
      labels:
        version: v2
---
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: user-service-policy
spec:
  selector:
    matchLabels:
      app: user-service
  rules:
    - from:
        - source:
            principals: ['cluster.local/ns/default/sa/order-service']
    - to:
        - operation:
            methods: ['GET', 'POST']
```

</example_good>

<example_bad>

```yaml
# BAD: No service mesh configuration
apiVersion: v1
kind: Service
metadata:
  name: user-service
spec:
  selector:
    app: user-service
  ports:
    - port: 80
      targetPort: 8080
  # BAD: No mTLS configuration
  # BAD: No circuit breaking
  # BAD: No traffic management
  # BAD: No observability
```

</example_bad>
