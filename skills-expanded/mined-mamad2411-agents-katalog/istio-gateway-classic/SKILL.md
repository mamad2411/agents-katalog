---
name: istio-gateway-classic
category: service-mesh
description: "Istio Gateway (Classic) — Istio Gateway + VirtualService 기반 트래픽 라우팅 Use when working with service-mesh 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Istio Gateway (Classic)

Istio Gateway + VirtualService 기반 트래픽 라우팅

## Quick Reference

```
Istio Classic 구조
    │
    ├─ Gateway ─────────────> 리스너 정의 (포트, TLS)
    │
    ├─ VirtualService ──────> 라우팅 규칙
    │
    └─ DestinationRule ─────> 트래픽 정책 (subset, 로드밸런싱)
```

---

## 아키텍처

```
┌──────────────────────────────────────────────────────────────┐
│  Istio Ingress Gateway                                       │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Gateway (리스너 정의)                                  │ │
│  │    ↓                                                    │ │
│  │  VirtualService (라우팅 규칙)                           │ │
│  │    ↓                                                    │ │
│  │  DestinationRule (트래픽 정책)                          │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

---

## Gateway + VirtualService 구성

```yaml
# Gateway: 외부 트래픽 진입점
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: api-gateway
  namespace: istio-system
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "api.example.com"
    - "*.api.example.com"
    tls:
      httpsRedirect: true
  - port:
      number: 443
      name: https
      protocol: HTTPS
    hosts:
    - "api.example.com"
    tls:
      mode: SIMPLE
      credentialName: api-tls-secret
---
# VirtualService: 라우팅 규칙
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: api-routes
  namespace: production
spec:
  hosts:
  - "api.example.com"
  gateways:
  - istio-system/api-gateway
  http:
  - match:
    - uri:
        prefix: /api/v1/users
    route:
    - destination:
        host: user-service
        port:
          number: 8080
  - match:
    - uri:
        prefix: /api/v1/orders
    route:
    - destination:
        host: order-service
        port:
          number: 8080
  - route:
    - destination:
        host: default-service
```

---

## TLS 설정

### Simple TLS

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: api-tls-secret
  namespace: istio-system
type: kubernetes.io/tls
data:
  tls.crt: <base64-encoded-cert>
  tls.key: <base64-encoded-key>
```

### mTLS (Mutual TLS)

```yaml
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: mtls-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 443
      name: https
      protocol: HTTPS
    hosts:
    - "secure.example.com"
    tls:
      mode: MUTUAL
      credentialName: mtls-credential
```

---

## 트래픽 관리 패턴

### Canary 배포

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: canary-route
spec:
  hosts:
  - my-service
  http:
  - route:
    - destination:
        host: my-service
        subset: stable
      weight: 90
    - destination:
        host: my-service
        subset: canary
      weight: 10
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: my-service-versions
spec:
  host: my-service
  subsets:
  - name: stable
    labels:
      version: v1
  - name: canary
    labels:
      version: v2
```

### A/B Testing (헤더 기반)

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: ab-testing
spec:
  hosts:
  - my-service
  http:
  - match:
    - headers:
        x-feature-flag:
          exact: "new-checkout"
    route:
    - destination:
        host: my-service
        subset: feature-checkout
  - route:
    - destination:
        host: my-service
        subset: stable
```

### Traffic Mirroring

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: mirror-traffic
spec:
  hosts:
  - my-service
  http:
  - route:
    - destination:
        host: my-service
        subset: stable
    mirror:
      host: my-service
      subset: shadow
    mirrorPercentage:
      value: 100.0
```

### Timeout & Retry

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: timeout-retry
spec:
  hosts:
  - my-service
  http:
  - route:
    - destination:
        host: my-service
    timeout: 10s
    retries:
      attempts: 3
      perTryTimeout: 3s
      retryOn: 5xx,reset,connect-failure
```

---

## 체크리스트

- [ ] Gateway selector 확인
- [ ] TLS Secret 같은 namespace
- [ ] VirtualService hosts 매칭
- [ ] DestinationRule subset 정의
- [ ] TLS 인증서 갱신 자동화

**관련 skill**: `/istio-gateway`, `/istio-gateway-api`, `/istio-core`
