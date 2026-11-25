---
name: mesh-patterns
description: "Service mesh patterns: Istio install and namespace setup, the Istio ingress gateway, Linkerd observability, Kiali, traffic mirroring, and JWT authentication at the mesh level. Use when rolling out or extending Istio or Linkerd."
---

# Service Mesh Patterns

Istio mTLS, traffic routing, circuit breaking, Linkerd ServiceProfiles, and Envoy debugging.

## Istio Install and Namespace Setup

```bash
# Install Istio with production profile
istioctl install --set profile=production -y

# Production profile includes:
# - 2 ingress gateway replicas (HA)
# - Horizontal pod autoscaling for istiod
# - Stricter security defaults

# Enable sidecar injection for namespace
kubectl label namespace production istio-injection=enabled

# Verify injection is working
kubectl rollout restart deployment -n production
kubectl get pods -n production -o json | \
  jq '.items[] | {name: .metadata.name, containers: [.spec.containers[].name]}'
# Each pod should have 2 containers: app + istio-proxy

# Check control plane health
istioctl analyze -n production
kubectl get pods -n istio-system
```

## Istio Ingress Gateway

```yaml
# Replace nginx-ingress with Istio Gateway + VirtualService
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: app-gateway
  namespace: production
spec:
  selector:
    istio: ingressgateway  # Istio's ingress gateway pods
  servers:
    - port:
        number: 443
        name: https
        protocol: HTTPS
      tls:
        mode: SIMPLE
        credentialName: myapp-tls  # Kubernetes Secret with cert
      hosts:
        - api.example.com
    - port:
        number: 80
        name: http
        protocol: HTTP
      tls:
        httpsRedirect: true  # Redirect HTTP -> HTTPS
      hosts:
        - api.example.com

---
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: app-gateway-vs
  namespace: production
spec:
  hosts:
    - api.example.com
  gateways:
    - app-gateway
  http:
    - match:
        - uri: {prefix: /api}
      route:
        - destination:
            host: payment-api
            port: {number: 80}
```

## Linkerd: Full Stack Observability

```bash
# Install Linkerd viz (metrics and dashboard)
linkerd viz install | kubectl apply -f -
linkerd viz check

# Real-time traffic stats per deployment
linkerd viz stat deploy -n production

# Real-time top routes (like htop for HTTP)
linkerd viz top deploy/payment-api -n production

# Tap live traffic (sample requests/responses)
linkerd viz tap deploy/frontend -n production \
  --to svc/payment-api \
  --path /api \
  --method POST

# Route-level success rate
linkerd viz routes deploy/payment-api -n production

# Check mTLS between specific pods
linkerd viz edges deploy -n production
```

## Kiali Dashboard (Istio)

```bash
# Install Kiali (service mesh observability UI)
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/kiali.yaml

# Port-forward to access locally
kubectl port-forward svc/kiali 20001:20001 -n istio-system

# Or expose via VirtualService
cat << 'EOF' | kubectl apply -f -
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: kiali
  namespace: istio-system
spec:
  hosts: [kiali.internal.example.com]
  gateways: [app-gateway]
  http:
    - route:
        - destination:
            host: kiali
            port: {number: 20001}
EOF
```

## Traffic Mirroring (Shadow Traffic)

```yaml
# Mirror 10% of production traffic to staging
# Staging responses are ignored -- pure observation
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: payment-api-mirror
  namespace: production
spec:
  hosts:
    - payment-api
  http:
    - route:
        - destination:
            host: payment-api
            subset: production
          weight: 100
      mirror:
        host: payment-api-staging
        port: {number: 80}
      mirrorPercentage:
        value: 10.0   # Mirror 10% of requests
```

## JWT Authentication at the Mesh Level

```yaml
# Validate JWTs at the sidecar level (before request reaches app)
apiVersion: security.istio.io/v1beta1
kind: RequestAuthentication
metadata:
  name: jwt-auth
  namespace: production
spec:
  selector:
    matchLabels:
      app: payment-api
  jwtRules:
    - issuer: "https://auth.example.com"
      jwksUri: "https://auth.example.com/.well-known/jwks.json"
      audiences: ["payment-api"]
      forwardOriginalToken: true   # Pass JWT to app for further validation

---
# Require valid JWT (reject unauthenticated requests)
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: require-jwt
  namespace: production
spec:
  selector:
    matchLabels:
      app: payment-api
  action: ALLOW
  rules:
    - when:
        - key: request.auth.claims[iss]
          values: ["https://auth.example.com"]
```
