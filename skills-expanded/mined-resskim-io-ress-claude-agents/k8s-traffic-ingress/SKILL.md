---
name: k8s-traffic-ingress
category: kubernetes
description: "Ingress Rate Limiting — NGINX Ingress, Kong 기반 Rate Limiting Use when working with kubernetes 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Ingress Rate Limiting

NGINX Ingress, Kong 기반 Rate Limiting

## Quick Reference

```
Ingress Rate Limiting
    │
    ├─ NGINX Ingress ───> Annotation 기반 설정
    │   └─ limit-rps, limit-connections
    │
    └─ Kong ────────────> Plugin 기반 설정
        └─ Redis 연동 지원
```

---

## NGINX Ingress Rate Limiting

### Annotation 기반

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ticket-api
  annotations:
    # 초당 요청 수 제한
    nginx.ingress.kubernetes.io/limit-rps: "100"

    # 분당 요청 수 제한
    nginx.ingress.kubernetes.io/limit-rpm: "1000"

    # 동시 연결 수 제한
    nginx.ingress.kubernetes.io/limit-connections: "50"

    # Burst 허용
    nginx.ingress.kubernetes.io/limit-burst-multiplier: "5"

    # Whitelist (rate limit 제외 IP)
    nginx.ingress.kubernetes.io/limit-whitelist: "10.0.0.0/8,192.168.0.0/16"
spec:
  rules:
  - host: ticket.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: ticket-api
            port:
              number: 80
```

### ConfigMap 기반 (전역)

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-configuration
  namespace: ingress-nginx
data:
  # 전역 rate limiting
  limit-req-status-code: "429"
  limit-conn-status-code: "429"

  # 클라이언트 식별 (IP 기반)
  use-forwarded-headers: "true"
  compute-full-forwarded-for: "true"
```

---

## Kong Rate Limiting

### Plugin 설정

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: rate-limiting-ticket
spec:
  plugin: rate-limiting
  config:
    second: 10
    minute: 100
    hour: 1000
    policy: redis
    redis_host: redis
    redis_port: 6379
    redis_database: 0
    fault_tolerant: true
    hide_client_headers: false
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ticket-api
  annotations:
    konghq.com/plugins: rate-limiting-ticket
spec:
  ingressClassName: kong
  rules:
  - host: ticket.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: ticket-api
            port:
              number: 80
```

### Consumer별 Rate Limiting

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongConsumer
metadata:
  name: vip-user
  annotations:
    kubernetes.io/ingress.class: kong
username: vip-user
---
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: rate-limiting-vip
spec:
  plugin: rate-limiting
  config:
    second: 100  # VIP는 10배 허용
    minute: 1000
    policy: redis
```

---

## 체크리스트

- [ ] Ingress annotation 설정
- [ ] 전역 ConfigMap 구성
- [ ] Whitelist IP 설정
- [ ] Kong Redis 연동 (분산 환경)

**관련 skill**: `/k8s-traffic`, `/k8s-helm`, `/k8s-security`
