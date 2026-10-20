---
name: istio-gateway-api
category: service-mesh
description: "Gateway API (K8s Native) — Kubernetes Gateway API + HTTPRoute 기반 트래픽 라우팅 Use when working with service-mesh 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Gateway API (K8s Native)

Kubernetes Gateway API + HTTPRoute 기반 트래픽 라우팅

## Quick Reference

```
Gateway API 구조
    │
    ├─ GatewayClass ────────> 구현체 정의 (istio)
    │
    ├─ Gateway ─────────────> 리스너 정의
    │
    ├─ HTTPRoute / GRPCRoute > 라우팅 규칙
    │
    └─ ReferenceGrant ──────> Cross-namespace 허용
```

---

## 아키텍처

```
┌──────────────────────────────────────────────────────────────┐
│  Kubernetes Gateway API                                      │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  GatewayClass (구현체 정의)                             │ │
│  │    ↓                                                    │ │
│  │  Gateway (리스너 정의)                                  │ │
│  │    ↓                                                    │ │
│  │  HTTPRoute / GRPCRoute / TCPRoute                       │ │
│  │    ↓                                                    │ │
│  │  ReferenceGrant (Cross-namespace 허용)                  │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

---

## Gateway + HTTPRoute 구성

```yaml
# GatewayClass (보통 Istio가 자동 생성)
apiVersion: gateway.networking.k8s.io/v1
kind: GatewayClass
metadata:
  name: istio
spec:
  controllerName: istio.io/gateway-controller
---
# Gateway
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: api-gateway
  namespace: istio-system
spec:
  gatewayClassName: istio
  listeners:
  - name: http
    port: 80
    protocol: HTTP
    hostname: "api.example.com"
    allowedRoutes:
      namespaces:
        from: All
  - name: https
    port: 443
    protocol: HTTPS
    hostname: "api.example.com"
    tls:
      mode: Terminate
      certificateRefs:
      - name: api-tls-secret
        kind: Secret
    allowedRoutes:
      namespaces:
        from: Selector
        selector:
          matchLabels:
            gateway-access: "true"
---
# HTTPRoute
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: api-routes
  namespace: production
spec:
  parentRefs:
  - name: api-gateway
    namespace: istio-system
  hostnames:
  - "api.example.com"
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /api/v1/users
    backendRefs:
    - name: user-service
      port: 8080
  - matches:
    - path:
        type: PathPrefix
        value: /api/v1/orders
    backendRefs:
    - name: order-service
      port: 8080
```

---

## ReferenceGrant (Cross-namespace)

```yaml
# production namespace의 리소스를 Gateway가 참조 허용
apiVersion: gateway.networking.k8s.io/v1beta1
kind: ReferenceGrant
metadata:
  name: allow-gateway-access
  namespace: production
spec:
  from:
  - group: gateway.networking.k8s.io
    kind: HTTPRoute
    namespace: istio-system
  to:
  - group: ""
    kind: Service
---
# Secret 참조 허용 (TLS 인증서)
apiVersion: gateway.networking.k8s.io/v1beta1
kind: ReferenceGrant
metadata:
  name: allow-tls-secret
  namespace: cert-manager
spec:
  from:
  - group: gateway.networking.k8s.io
    kind: Gateway
    namespace: istio-system
  to:
  - group: ""
    kind: Secret
```

---

## 트래픽 관리 패턴

### Canary 배포

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: canary-route
spec:
  parentRefs:
  - name: api-gateway
  rules:
  - backendRefs:
    - name: my-service-v1
      port: 8080
      weight: 90
    - name: my-service-v2
      port: 8080
      weight: 10
```

### A/B Testing (헤더 기반)

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: ab-testing
spec:
  parentRefs:
  - name: api-gateway
  rules:
  - matches:
    - headers:
      - name: x-feature-flag
        value: "new-checkout"
    backendRefs:
    - name: my-service-feature
      port: 8080
  - backendRefs:
    - name: my-service-stable
      port: 8080
```

### Traffic Mirroring

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: mirror-traffic
spec:
  parentRefs:
  - name: api-gateway
  rules:
  - filters:
    - type: RequestMirror
      requestMirror:
        backendRef:
          name: my-service-shadow
          port: 8080
    backendRefs:
    - name: my-service-stable
      port: 8080
```

### Timeout (with Istio extension)

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: timeout-retry
  annotations:
    retry.istio.io/attempts: "3"
    retry.istio.io/per-try-timeout: "3s"
spec:
  parentRefs:
  - name: api-gateway
  rules:
  - backendRefs:
    - name: my-service
      port: 8080
    timeouts:
      request: 10s
```

---

## 체크리스트

- [ ] GatewayClass 존재 확인
- [ ] allowedRoutes 설정
- [ ] ReferenceGrant (cross-namespace)
- [ ] parentRefs 정확히 지정
- [ ] TLS 인증서 갱신 자동화

**관련 skill**: `/istio-gateway`, `/istio-gateway-classic`, `/istio-core`
