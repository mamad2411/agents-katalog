---
name: gateway-api-migration
category: kubernetes
description: "Gateway API 마이그레이션 가이드 — Ingress NGINX -> Gateway API 전환, Istio Gateway API 통합, Annotation 매핑 Use when working with kubernetes 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Gateway API 마이그레이션 가이드

Ingress NGINX -> Gateway API 전환, Istio Gateway API 통합, Annotation 매핑

## TCPRoute / UDPRoute

```yaml
apiVersion: gateway.networking.k8s.io/v1alpha2
kind: TCPRoute
metadata:
  name: postgres-route
  namespace: database
spec:
  parentRefs:
    - name: tcp-gateway
      namespace: gateway-system
      sectionName: postgres
  rules:
    - backendRefs:
        - name: postgres-primary
          port: 5432
---
apiVersion: gateway.networking.k8s.io/v1alpha2
kind: UDPRoute
metadata:
  name: dns-route
  namespace: dns-system
spec:
  parentRefs:
    - name: udp-gateway
  rules:
    - backendRefs:
        - name: coredns
          port: 53
```

---

## Istio Gateway API 모드

### 활성화

```bash
# Istio 설치 시 Gateway API 지원
istioctl install --set profile=minimal \
  --set values.pilot.env.PILOT_ENABLE_GATEWAY_API=true \
  --set values.pilot.env.PILOT_ENABLE_GATEWAY_API_STATUS=true
```

### Istio Gateway API 예시

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: istio-gateway
  namespace: istio-system
spec:
  gatewayClassName: istio
  listeners:
    - name: http
      port: 80
      protocol: HTTP
      allowedRoutes:
        namespaces:
          from: All
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: app-route
  namespace: production
spec:
  parentRefs:
    - name: istio-gateway
      namespace: istio-system
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /
      backendRefs:
        - name: my-app
          port: 8080
```

---

## CRITICAL: Ingress -> Gateway API 마이그레이션

### 변환 예시

```yaml
# Before: Ingress
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-app
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - app.example.com
      secretName: app-tls
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
---
# After: Gateway API
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: app-gateway
  namespace: gateway-system
spec:
  gatewayClassName: envoy-gateway
  listeners:
    - name: https
      port: 443
      protocol: HTTPS
      hostname: app.example.com
      tls:
        mode: Terminate
        certificateRefs:
          - name: app-tls
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: my-app
  namespace: production
spec:
  parentRefs:
    - name: app-gateway
      namespace: gateway-system
  hostnames:
    - app.example.com
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /api
      filters:
        - type: URLRewrite
          urlRewrite:
            path:
              type: ReplacePrefixMatch
              replacePrefixMatch: /
      backendRefs:
        - name: api-service
          port: 8080
```

### 마이그레이션 체크리스트

```
Phase 1: 준비
    [ ] 현재 Ingress 리소스 목록화
    [ ] Annotation 사용 현황 분석
    [ ] Gateway API 구현체 선택

Phase 2: 병행 운영
    [ ] Gateway API CRDs 설치
    [ ] 새 Gateway/HTTPRoute 생성
    [ ] 트래픽 일부 전환 (10%)
    [ ] 모니터링 및 검증

Phase 3: 완전 전환
    [ ] 트래픽 100% 전환
    [ ] Ingress 리소스 제거
    [ ] Ingress Controller 제거
```

### Annotation -> Policy 매핑

| Ingress Annotation | Gateway API |
|-------------------|-------------|
| `nginx.ingress.kubernetes.io/rewrite-target` | HTTPRoute filters.URLRewrite |
| `nginx.ingress.kubernetes.io/ssl-redirect` | HTTPRoute filters.RequestRedirect |
| `nginx.ingress.kubernetes.io/rate-limit` | BackendTrafficPolicy.rateLimit |
| `nginx.ingress.kubernetes.io/auth-tls-secret` | ClientTrafficPolicy.tls |
| `nginx.ingress.kubernetes.io/cors-*` | SecurityPolicy.cors |
| `nginx.ingress.kubernetes.io/proxy-body-size` | EnvoyProxy.config |

---

## Sources

- [Gateway API Official](https://gateway-api.sigs.k8s.io/)
- [Envoy Gateway](https://gateway.envoyproxy.io/)
- [Kong Gateway API](https://docs.konghq.com/kubernetes-ingress-controller/latest/concepts/gateway-api/)
- [Istio Gateway API](https://istio.io/latest/docs/tasks/traffic-management/ingress/gateway-api/)
- [NGINX Ingress EOL](https://medium.com/@h.stoychev87/nginx-ingress-end-of-life-2026-f30e53e14a2e)
- [Gateway API 2026 Guide](https://dev.to/mechcloud_academy/kubernetes-gateway-api-in-2026-the-definitive-guide-to-envoy-gateway-istio-cilium-and-kong-2bkl)

## 참조 스킬

- `/gateway-api` - Gateway API 핵심 개념 (Envoy Gateway, Kong, 리소스 구조)
- `/istio-gateway` - Istio Gateway 설정
