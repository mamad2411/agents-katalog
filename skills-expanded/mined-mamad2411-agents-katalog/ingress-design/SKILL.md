# Skill: Ingress and Gateway API Design

## Purpose

Guide the selection, configuration, and architecture of ingress controllers and the Kubernetes Gateway API for routing external traffic into Kubernetes clusters. Covers all major ingress controllers across AKS, EKS, and GKE, plus the evolving Gateway API standard.

## Core Knowledge

### Ingress vs Gateway API

**Ingress (networking.k8s.io/v1):**
- Original Kubernetes API for HTTP/HTTPS routing
- Limited spec — vendor extensions via annotations
- Single resource type (Ingress) for all routing
- Widely supported but fragmented (each controller has different annotations)
- Status: Stable but no longer actively enhanced

**Gateway API (gateway.networking.k8s.io):**
- Next-generation routing API (CNCF, Standard channel resources are GA)
- Role-oriented: infrastructure provider → cluster operator → application developer
- Typed routes: HTTPRoute and GRPCRoute are Standard; TLSRoute/TCPRoute/UDPRoute remain Experimental unless your implementation documents otherwise
- Portable — same Standard-channel manifest works across conformant implementations
- Extensible via policy attachment; BackendTLSPolicy is Standard in `gateway.networking.k8s.io/v1`, while some policies remain Experimental
- Status: Use `gateway.networking.k8s.io/v1` for Standard resources; install Experimental CRDs only when needed and supported by the controller

### Ingress Controllers

#### NGINX Ingress Controller

The most widely deployed ingress controller (kubernetes/ingress-nginx community project).

**Key Features:**
- L7 HTTP/HTTPS routing with path and host matching
- TLS termination with cert-manager integration
- Rate limiting, IP whitelisting, basic auth
- Custom NGINX configuration via annotations and ConfigMaps
- TCP/UDP load balancing via ConfigMap
- WebSocket and gRPC support
- ModSecurity WAF integration

**Basic Ingress Resource:**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  namespace: production
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
    nginx.ingress.kubernetes.io/rate-limit: "10"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - app.example.com
      secretName: app-tls-secret
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /api(/|$)(.*)
            pathType: ImplementationSpecific
            backend:
              service:
                name: api-service
                port:
                  number: 8080
          - path: /
            pathType: Prefix
            backend:
              service:
                name: frontend-service
                port:
                  number: 80
```

**Internal Ingress (Private):**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: internal-ingress
  annotations:
    # AKS - Internal Load Balancer
    service.beta.kubernetes.io/azure-load-balancer-internal: "true"
    # EKS - Internal NLB
    # service.beta.kubernetes.io/aws-load-balancer-scheme: internal
spec:
  ingressClassName: nginx
  rules:
    - host: internal-api.corp.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: internal-api
                port:
                  number: 8080
```

#### Traefik

Cloud-native ingress controller with automatic service discovery and Let's Encrypt integration.

**Key Features:**
- Automatic Let's Encrypt certificate management
- IngressRoute CRD for advanced routing
- Middleware chain (rate limit, circuit breaker, retry, compress)
- Dashboard with real-time traffic metrics
- TCP/UDP routing
- Canary deployments via weighted round-robin

**IngressRoute (Traefik CRD):**
```yaml
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata:
  name: app-route
  namespace: production
spec:
  entryPoints:
    - websecure
  routes:
    - match: Host(`app.example.com`) && PathPrefix(`/api`)
      kind: Rule
      services:
        - name: api-service
          port: 8080
          weight: 90
        - name: api-canary
          port: 8080
          weight: 10
      middlewares:
        - name: rate-limit
        - name: retry
    - match: Host(`app.example.com`)
      kind: Rule
      services:
        - name: frontend
          port: 80
  tls:
    certResolver: letsencrypt
---
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: rate-limit
  namespace: production
spec:
  rateLimit:
    average: 100
    burst: 50
    period: 1m
---
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: retry
  namespace: production
spec:
  retry:
    attempts: 3
    initialInterval: 100ms
```

#### Azure Application Gateway Ingress Controller (AGIC)

Uses Azure Application Gateway as the ingress controller for AKS.

**Key Features:**
- Azure-managed WAF (OWASP rules)
- Autoscaling (Application Gateway v2)
- SSL offloading with Azure Key Vault integration
- URL-based routing, multi-site hosting
- Backend health probes
- Session affinity (cookie-based)
- Private IP frontend for internal ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: agic-ingress
  namespace: production
  annotations:
    kubernetes.io/ingress.class: azure/application-gateway
    appgw.ingress.kubernetes.io/ssl-redirect: "true"
    appgw.ingress.kubernetes.io/waf-policy-for-path: "/subscriptions/.../wafPolicies/myPolicy"
    appgw.ingress.kubernetes.io/backend-protocol: "https"
    appgw.ingress.kubernetes.io/backend-hostname: "api.internal"
    appgw.ingress.kubernetes.io/health-probe-path: "/healthz"
    appgw.ingress.kubernetes.io/health-probe-interval: "30"
    appgw.ingress.kubernetes.io/connection-draining: "true"
    appgw.ingress.kubernetes.io/connection-draining-timeout: "60"
spec:
  tls:
    - hosts:
        - app.example.com
      secretName: app-tls
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /api/*
            pathType: ImplementationSpecific
            backend:
              service:
                name: api-service
                port:
                  number: 443
          - path: /*
            pathType: ImplementationSpecific
            backend:
              service:
                name: frontend
                port:
                  number: 80
```

#### AWS Load Balancer Controller

Provisions AWS ALB (L7) or NLB (L4) for Kubernetes Ingress and Service resources.

**ALB Ingress:**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: alb-ingress
  namespace: production
  annotations:
    kubernetes.io/ingress.class: alb
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:us-east-1:123456789:certificate/abc123
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTPS":443}]'
    alb.ingress.kubernetes.io/ssl-redirect: "443"
    alb.ingress.kubernetes.io/group.name: shared-alb
    alb.ingress.kubernetes.io/healthcheck-path: /healthz
    alb.ingress.kubernetes.io/wafv2-acl-arn: arn:aws:wafv2:us-east-1:123456789:regional/webacl/my-acl/id
    alb.ingress.kubernetes.io/actions.weighted-routing: |
      {"type":"forward","forwardConfig":{"targetGroups":[
        {"serviceName":"api-stable","servicePort":"8080","weight":90},
        {"serviceName":"api-canary","servicePort":"8080","weight":10}
      ]}}
spec:
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 8080
          - path: /
            pathType: Prefix
            backend:
              service:
                name: frontend
                port:
                  number: 80
```

#### GKE Ingress (GCE Ingress Controller)

Google-managed ingress using Google Cloud Load Balancer.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: gke-ingress
  namespace: production
  annotations:
    kubernetes.io/ingress.class: gce
    kubernetes.io/ingress.global-static-ip-name: my-static-ip
    networking.gke.io/managed-certificates: my-managed-cert
    networking.gke.io/v1beta1.FrontendConfig: my-frontend-config
spec:
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /api/*
            pathType: ImplementationSpecific
            backend:
              service:
                name: api-service
                port:
                  number: 8080
---
# GKE Managed Certificate
apiVersion: networking.gke.io/v1
kind: ManagedCertificate
metadata:
  name: my-managed-cert
spec:
  domains:
    - app.example.com
---
# Frontend config for SSL policy and redirects
apiVersion: networking.gke.io/v1beta1
kind: FrontendConfig
metadata:
  name: my-frontend-config
spec:
  sslPolicy: modern-ssl-policy
  redirectToHttps:
    enabled: true
    responseCodeName: MOVED_PERMANENTLY_DEFAULT
```

### Kubernetes Gateway API

#### Architecture and Role Separation

```
┌─────────────────────────────────────────────────────────────┐
│ Infrastructure Provider                                       │
│   → GatewayClass (defines the controller implementation)     │
├─────────────────────────────────────────────────────────────┤
│ Cluster Operator                                             │
│   → Gateway (deploys listeners, TLS certs, IP allocation)   │
├─────────────────────────────────────────────────────────────┤
│ Application Developer                                        │
│   → HTTPRoute / GRPCRoute / TLSRoute (routing rules)        │
└─────────────────────────────────────────────────────────────┘
```

#### GatewayClass

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: GatewayClass
metadata:
  name: nginx
spec:
  controllerName: gateway.nginx.org/nginx-gateway-controller
---
apiVersion: gateway.networking.k8s.io/v1
kind: GatewayClass
metadata:
  name: istio
spec:
  controllerName: istio.io/gateway-controller
---
apiVersion: gateway.networking.k8s.io/v1
kind: GatewayClass
metadata:
  name: cilium
spec:
  controllerName: io.cilium/gateway-controller
```

#### Gateway

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: production-gateway
  namespace: gateway-system
  annotations:
    # Cloud-specific annotations for LB type
    service.beta.kubernetes.io/azure-load-balancer-internal: "false"
spec:
  gatewayClassName: nginx
  listeners:
    - name: https
      protocol: HTTPS
      port: 443
      tls:
        mode: Terminate
        certificateRefs:
          - kind: Secret
            name: wildcard-tls
            namespace: gateway-system
      allowedRoutes:
        namespaces:
          from: Selector
          selector:
            matchLabels:
              gateway-access: "true"
    - name: http
      protocol: HTTP
      port: 80
      allowedRoutes:
        namespaces:
          from: Same
    - name: internal
      protocol: HTTPS
      port: 8443
      hostname: "*.internal.corp.com"
      tls:
        mode: Terminate
        certificateRefs:
          - kind: Secret
            name: internal-tls
      allowedRoutes:
        namespaces:
          from: All
```

#### HTTPRoute

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: api-routes
  namespace: production
spec:
  parentRefs:
    - name: production-gateway
      namespace: gateway-system
      sectionName: https
  hostnames:
    - "api.example.com"
  rules:
    # Canary with header match
    - matches:
        - headers:
            - name: x-canary
              value: "true"
      backendRefs:
        - name: api-canary
          port: 8080
    # Weighted traffic split
    - matches:
        - path:
            type: PathPrefix
            value: /api/v2
      backendRefs:
        - name: api-v2-stable
          port: 8080
          weight: 90
        - name: api-v2-canary
          port: 8080
          weight: 10
    # Default route
    - matches:
        - path:
            type: PathPrefix
            value: /api/v1
      backendRefs:
        - name: api-v1
          port: 8080
      filters:
        - type: RequestHeaderModifier
          requestHeaderModifier:
            add:
              - name: X-Api-Version
                value: "v1"
        - type: ResponseHeaderModifier
          responseHeaderModifier:
            set:
              - name: X-Frame-Options
                value: DENY
```

#### GRPCRoute

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: GRPCRoute
metadata:
  name: grpc-routes
  namespace: production
spec:
  parentRefs:
    - name: production-gateway
      namespace: gateway-system
  hostnames:
    - "grpc.example.com"
  rules:
    - matches:
        - method:
            service: mypackage.UserService
            method: GetUser
      backendRefs:
        - name: user-service
          port: 50051
    - matches:
        - method:
            service: mypackage.OrderService
      backendRefs:
        - name: order-service
          port: 50051
```

#### TLSRoute (Passthrough — Experimental channel)

TLSRoute is not part of the Standard channel in all Gateway API releases/controllers. Install the Experimental CRDs and verify controller support before using it.

```yaml
apiVersion: gateway.networking.k8s.io/v1alpha2
kind: TLSRoute
metadata:
  name: tls-passthrough
  namespace: production
spec:
  parentRefs:
    - name: production-gateway
      namespace: gateway-system
      sectionName: tls-passthrough
  hostnames:
    - "secure.example.com"
  rules:
    - backendRefs:
        - name: tls-backend
          port: 443
```

#### HTTP-to-HTTPS Redirect

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: redirect-to-https
  namespace: gateway-system
spec:
  parentRefs:
    - name: production-gateway
      sectionName: http
  rules:
    - filters:
        - type: RequestRedirect
          requestRedirect:
            scheme: https
            statusCode: 301
```

### TLS Termination Patterns

#### Pattern 1: Edge Termination (Most Common)
TLS terminates at the ingress/gateway; backend traffic is plain HTTP.

```
Client --[HTTPS]--> Ingress --[HTTP]--> Pod
```

#### Pattern 2: Re-encryption (End-to-End TLS)
TLS terminates at ingress; new TLS connection to backend.

```yaml
# NGINX annotation for backend HTTPS
nginx.ingress.kubernetes.io/backend-protocol: "HTTPS"

# Gateway API - BackendTLSPolicy (Standard channel)
apiVersion: gateway.networking.k8s.io/v1
kind: BackendTLSPolicy
metadata:
  name: api-backend-tls
  namespace: production
spec:
  targetRefs:
    - group: ""
      kind: Service
      name: api-service
  validation:
    caCertificateRefs:
      - name: backend-ca
        group: ""
        kind: ConfigMap
    hostname: api.internal
```

#### Pattern 3: TLS Passthrough
Ingress passes encrypted traffic directly to backend (no termination).

```yaml
# NGINX annotation
nginx.ingress.kubernetes.io/ssl-passthrough: "true"
```

#### Pattern 4: cert-manager Integration

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@example.com
    privateKeySecretRef:
      name: letsencrypt-prod-key
    solvers:
      - http01:
          ingress:
            ingressClassName: nginx
---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: app-cert
  namespace: production
spec:
  secretName: app-tls-secret
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  dnsNames:
    - app.example.com
    - api.example.com
  duration: 2160h    # 90 days
  renewBefore: 720h  # 30 days before expiry
```

### Internal vs External Ingress

#### Dual-Ingress Pattern

```yaml
# External ingress - public-facing
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: external-gateway
  annotations:
    # AKS: public IP
    service.beta.kubernetes.io/azure-load-balancer-internal: "false"
spec:
  gatewayClassName: nginx
  listeners:
    - name: public-https
      port: 443
      protocol: HTTPS
      tls:
        certificateRefs:
          - name: public-tls
---
# Internal ingress - private (VNet/VPC only)
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: internal-gateway
  annotations:
    # AKS: internal LB with specific subnet
    service.beta.kubernetes.io/azure-load-balancer-internal: "true"
    service.beta.kubernetes.io/azure-load-balancer-internal-subnet: "ingress-subnet"
spec:
  gatewayClassName: nginx
  listeners:
    - name: private-https
      port: 443
      protocol: HTTPS
      hostname: "*.internal.corp.com"
      tls:
        certificateRefs:
          - name: internal-tls
```

## Cloud-Specific Examples

### AKS Ingress Options
1. **NGINX Ingress Controller** — Deploy via Helm (app routing add-on available)
2. **AGIC** — Azure Application Gateway as ingress (managed WAF)
3. **Traefik** — Default with AKS app routing add-on
4. **Istio Gateway** — If using Istio service mesh

```bash
# AKS App Routing add-on (managed NGINX)
az aks approuting enable --resource-group myRG --name myCluster

# Enable with Azure DNS integration
az aks approuting zone add \
  --resource-group myRG --name myCluster \
  --ids /subscriptions/.../dnszones/example.com \
  --attach-zones
```

### EKS Ingress Options
1. **AWS Load Balancer Controller** — ALB (L7) or NLB (L4)
2. **NGINX Ingress Controller** — Deploy via Helm
3. **Istio Gateway** — If using Istio

```bash
# Install AWS LB Controller via Helm
helm install aws-load-balancer-controller \
  eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=my-cluster \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller
```

### GKE Ingress Options
1. **GKE Ingress (GCE)** — Google Cloud Load Balancer (default)
2. **GKE Gateway Controller** — Gateway API implementation
3. **NGINX/Traefik** — Self-managed via Helm

```yaml
# GKE Gateway API (multi-cluster)
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: gke-gateway
spec:
  gatewayClassName: gke-l7-global-external-managed
  listeners:
    - name: https
      protocol: HTTPS
      port: 443
      tls:
        certificateRefs:
          - kind: ManagedCertificate
            name: my-cert
```

## Decision Matrix: Ingress Controllers

| Criteria | NGINX | Traefik | AGIC | AWS LB Controller | GKE Ingress |
|----------|-------|---------|------|-------------------|-------------|
| **Cloud** | Any | Any | AKS | EKS | GKE |
| **L7 Features** | Rich | Rich | Rich | Moderate | Moderate |
| **WAF** | ModSecurity | Plugin | Azure WAF | AWS WAF | Cloud Armor |
| **Auto TLS** | cert-manager | Built-in | Key Vault | ACM | Managed Certs |
| **Gateway API** | Yes (v1.1+) | Yes | Planned | Yes | Yes (native) |
| **TCP/UDP** | ConfigMap | Native | No | NLB mode | No |
| **Canary** | Annotations | Weighted | Limited | Target groups | No |
| **Managed** | Self/AKS addon | Self/AKS addon | Azure | AWS | Google |

## Troubleshooting Tips

- **502/503 from ingress:** Check backend pod health, readiness probes, and service selectors
- **TLS errors:** Verify Secret exists in correct namespace, cert covers the hostname, cert not expired
- **Path routing not working:** Check `pathType` (Prefix vs Exact vs ImplementationSpecific)
- **Ingress not getting IP:** Check controller logs, cloud LB quota, service type LoadBalancer events
- **Gateway API routes not attaching:** Verify `parentRefs` match Gateway name/namespace/sectionName, check `allowedRoutes` on listener

```bash
# Debug ingress controller
kubectl logs -n ingress-nginx deploy/ingress-nginx-controller --tail=100
kubectl get events -n production --field-selector reason=Sync

# Check Gateway status
kubectl get gateway -A -o wide
kubectl describe httproute my-route -n production
```

---

**Analysis only — verify against vendor documentation before applying.**
