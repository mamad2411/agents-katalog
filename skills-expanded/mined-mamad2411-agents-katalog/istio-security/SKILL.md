---
name: istio-security
category: service-mesh
description: "Istio Security 가이드 — mTLS, PeerAuthentication, AuthorizationPolicy, JWT 인증 Use when working with service-mesh 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Istio Security 가이드

mTLS, PeerAuthentication, AuthorizationPolicy, JWT 인증

## Quick Reference (결정 트리)

```
보안 요구사항?
    │
    ├─ 서비스 간 암호화 ─────> mTLS (PeerAuthentication)
    │       │
    │       ├─ 전환 중 ────> PERMISSIVE 모드
    │       └─ 완료 ───────> STRICT 모드
    │
    ├─ 서비스 간 접근 제어 ──> AuthorizationPolicy
    │       │
    │       ├─ 화이트리스트 ─> ALLOW 규칙
    │       └─ 블랙리스트 ───> DENY 규칙
    │
    └─ 사용자 인증 ──────────> RequestAuthentication (JWT)
```

---

## CRITICAL: Zero Trust Security

```
┌─────────────────────────────────────────────────────────────┐
│                    Istio Security Layers                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Layer 1: Transport (mTLS)                                   │
│  ├─ 모든 서비스 간 통신 암호화                               │
│  ├─ 자동 인증서 발급/갱신                                    │
│  └─ PeerAuthentication으로 제어                              │
│                                                              │
│  Layer 2: Authorization                                      │
│  ├─ 서비스 간 접근 제어                                      │
│  ├─ Source/Operation 기반 규칙                               │
│  └─ AuthorizationPolicy로 제어                               │
│                                                              │
│  Layer 3: End-User Authentication                            │
│  ├─ JWT 토큰 검증                                            │
│  ├─ OIDC 연동 (Google, Auth0 등)                            │
│  └─ RequestAuthentication으로 제어                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 핵심 리소스

| 리소스 | 목적 | 대상 |
|--------|------|------|
| **PeerAuthentication** | mTLS 설정 | 서비스 간 (워크로드) |
| **AuthorizationPolicy** | 접근 제어 | 서비스 간 |
| **RequestAuthentication** | JWT 검증 | 최종 사용자 |

---

## mTLS (PeerAuthentication)

### 모드

| 모드 | 동작 | 사용 시기 |
|------|------|----------|
| **DISABLE** | mTLS 비활성화 | 레거시 호환 |
| **PERMISSIVE** | mTLS + 평문 허용 | 마이그레이션 중 |
| **STRICT** | mTLS만 허용 | 프로덕션 권장 |

### 네임스페이스 전체 STRICT mTLS

```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT
```

### 메시 전체 STRICT mTLS

```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system  # 루트 네임스페이스
spec:
  mtls:
    mode: STRICT
```

### 특정 워크로드 예외

```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: legacy-service-exception
  namespace: production
spec:
  selector:
    matchLabels:
      app: legacy-service
  mtls:
    mode: PERMISSIVE  # 레거시 서비스는 예외
---
# 특정 포트만 예외
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: metrics-port-exception
  namespace: production
spec:
  selector:
    matchLabels:
      app: my-service
  mtls:
    mode: STRICT
  portLevelMtls:
    9090:  # Prometheus 메트릭 포트
      mode: PERMISSIVE
```

### CRITICAL: mTLS 마이그레이션 단계

```
1. PERMISSIVE로 시작 (기존 트래픽 유지)
   ↓
2. 모든 서비스에 sidecar 주입 확인
   ↓
3. mTLS 트래픽 모니터링 (Kiali)
   ↓
4. STRICT로 전환
   ↓
5. 문제 시 PERMISSIVE로 롤백
```

---

## AuthorizationPolicy

### 기본 구조

```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: policy-name
  namespace: target-namespace
spec:
  selector:
    matchLabels:
      app: target-service  # 정책 적용 대상
  action: ALLOW  # ALLOW, DENY, CUSTOM, AUDIT
  rules:
    - from:  # 소스 조건
        - source:
            principals: ["cluster.local/ns/default/sa/frontend"]
      to:    # 대상 조건
        - operation:
            methods: ["GET"]
            paths: ["/api/*"]
      when:  # 추가 조건
        - key: request.headers[x-token]
          values: ["valid"]
```

### ALLOW 정책 (화이트리스트)

```yaml
# 특정 서비스만 접근 허용
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: order-service-allow
  namespace: production
spec:
  selector:
    matchLabels:
      app: order-service
  action: ALLOW
  rules:
    # API Gateway에서만 접근 허용
    - from:
        - source:
            principals:
              - "cluster.local/ns/production/sa/api-gateway"
      to:
        - operation:
            methods: ["GET", "POST"]
            paths: ["/api/orders", "/api/orders/*"]

    # 내부 서비스 (inventory)에서 접근 허용
    - from:
        - source:
            principals:
              - "cluster.local/ns/production/sa/inventory-service"
      to:
        - operation:
            methods: ["GET"]
            paths: ["/internal/orders/*"]
```

### DENY 정책 (블랙리스트)

```yaml
# 특정 경로 차단
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: deny-admin-external
  namespace: production
spec:
  selector:
    matchLabels:
      app: my-service
  action: DENY
  rules:
    # 외부에서 admin 경로 차단
    - from:
        - source:
            notNamespaces: ["production"]
      to:
        - operation:
            paths: ["/admin", "/admin/*"]
```

### 기본 차단 (Default Deny)

```yaml
# 네임스페이스 기본 차단
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: deny-all
  namespace: production
spec:
  {}  # 빈 spec = 모든 접근 차단
```

### CRITICAL: 정책 우선순위

```
1. CUSTOM (가장 높음)
2. DENY
3. ALLOW
4. 매칭 규칙 없음 → 기본 허용 (정책 없으면)
                 → 차단 (빈 정책 있으면)
```

### 네임스페이스 간 통신 제어

```yaml
# production 네임스페이스만 접근 허용
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-production-only
  namespace: production
spec:
  action: ALLOW
  rules:
    - from:
        - source:
            namespaces: ["production"]
    # Istio 시스템도 허용 (필수)
    - from:
        - source:
            namespaces: ["istio-system"]
```

---

## RequestAuthentication (JWT)

### JWT 검증 설정

```yaml
apiVersion: security.istio.io/v1beta1
kind: RequestAuthentication
metadata:
  name: jwt-auth
  namespace: production
spec:
  selector:
    matchLabels:
      app: api-gateway
  jwtRules:
    # Auth0
    - issuer: "https://myapp.auth0.com/"
      jwksUri: "https://myapp.auth0.com/.well-known/jwks.json"
      audiences:
        - "https://api.myapp.com"
      forwardOriginalToken: true

    # Google
    - issuer: "https://accounts.google.com"
      jwksUri: "https://www.googleapis.com/oauth2/v3/certs"

    # 자체 인증 서버
    - issuer: "https://auth.myapp.com"
      jwksUri: "https://auth.myapp.com/.well-known/jwks.json"
      outputPayloadToHeader: x-jwt-payload
```

### JWT 필수 요구 (AuthorizationPolicy 연동)

```yaml
# JWT 없는 요청 차단
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: require-jwt
  namespace: production
spec:
  selector:
    matchLabels:
      app: api-gateway
  action: DENY
  rules:
    - from:
        - source:
            notRequestPrincipals: ["*"]  # JWT principal이 없으면 차단
      to:
        - operation:
            paths: ["/api/*"]
---
# 특정 경로는 JWT 없이 허용
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-public
  namespace: production
spec:
  selector:
    matchLabels:
      app: api-gateway
  action: ALLOW
  rules:
    - to:
        - operation:
            paths: ["/health", "/public/*"]
```

### JWT 클레임 기반 접근 제어

```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: admin-only
  namespace: production
spec:
  selector:
    matchLabels:
      app: admin-service
  action: ALLOW
  rules:
    - from:
        - source:
            requestPrincipals: ["*"]  # 유효한 JWT 필수
      when:
        # JWT의 role 클레임이 admin인 경우만
        - key: request.auth.claims[role]
          values: ["admin"]
```

---

## 실전 시나리오

### 1. 마이크로서비스 보안 구성

```yaml
# 1. 네임스페이스 STRICT mTLS
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT
---
# 2. 기본 차단
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: deny-all
  namespace: production
spec:
  {}
---
# 3. API Gateway → Backend 허용
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-from-gateway
  namespace: production
spec:
  selector:
    matchLabels:
      app: backend-service
  action: ALLOW
  rules:
    - from:
        - source:
            principals:
              - "cluster.local/ns/production/sa/api-gateway"
---
# 4. Prometheus 메트릭 수집 허용
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-prometheus
  namespace: production
spec:
  action: ALLOW
  rules:
    - from:
        - source:
            namespaces: ["monitoring"]
      to:
        - operation:
            ports: ["9090"]
            methods: ["GET"]
```

### 2. mTLS 검증 (Defense in Depth)

```yaml
# mTLS가 실제로 적용되었는지 추가 검증
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: require-mtls
  namespace: production
spec:
  action: DENY
  rules:
    - from:
        - source:
            notPrincipals: ["*"]  # principal이 없으면 = 평문 통신
```

### 3. Rate Limiting (EnvoyFilter)

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: EnvoyFilter
metadata:
  name: rate-limit
  namespace: production
spec:
  workloadSelector:
    labels:
      app: api-gateway
  configPatches:
    - applyTo: HTTP_FILTER
      match:
        context: SIDECAR_INBOUND
        listener:
          filterChain:
            filter:
              name: "envoy.filters.network.http_connection_manager"
      patch:
        operation: INSERT_BEFORE
        value:
          name: envoy.filters.http.local_ratelimit
          typed_config:
            "@type": type.googleapis.com/udpa.type.v1.TypedStruct
            type_url: type.googleapis.com/envoy.extensions.filters.http.local_ratelimit.v3.LocalRateLimit
            value:
              stat_prefix: http_local_rate_limiter
              token_bucket:
                max_tokens: 100
                tokens_per_fill: 100
                fill_interval: 1s
              filter_enabled:
                runtime_key: local_rate_limit_enabled
                default_value:
                  numerator: 100
                  denominator: HUNDRED
              filter_enforced:
                runtime_key: local_rate_limit_enforced
                default_value:
                  numerator: 100
                  denominator: HUNDRED
```

---

## 디버깅

### 정책 확인

```bash
# PeerAuthentication 확인
kubectl get peerauthentication -A

# AuthorizationPolicy 확인
kubectl get authorizationpolicy -A

# RequestAuthentication 확인
kubectl get requestauthentication -A
```

### mTLS 상태 확인

```bash
# istioctl로 mTLS 상태 확인
istioctl x authz check <pod-name> -n <namespace>

# Envoy 설정 확인
istioctl proxy-config cluster <pod-name> -n <namespace>

# 실제 연결 확인
istioctl x describe pod <pod-name> -n <namespace>
```

### Kiali 시각화

Kiali 대시보드에서 mTLS 상태 확인:
- 🔒 아이콘: mTLS 활성화
- ⚠️ 아이콘: PERMISSIVE 모드
- 🔓 아이콘: mTLS 없음

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 바로 STRICT | 서비스 장애 | PERMISSIVE로 시작 |
| 빈 allow 규칙 | 모든 접근 차단 | 명시적 규칙 추가 |
| istio-system 차단 | 시스템 오류 | istio-system 허용 |
| 모니터링 차단 | 메트릭 수집 불가 | monitoring NS 허용 |
| JWT 없이 DENY | 인증 없는 요청 차단 | RequestAuthentication 먼저 |

---

## 체크리스트

### mTLS
- [ ] PERMISSIVE로 시작
- [ ] 모든 서비스 sidecar 확인
- [ ] Kiali에서 mTLS 상태 확인
- [ ] STRICT로 전환

### AuthorizationPolicy
- [ ] 기본 차단 정책 설정
- [ ] 필요한 통신만 ALLOW
- [ ] istio-system 접근 허용
- [ ] 모니터링 접근 허용

### JWT
- [ ] RequestAuthentication 설정
- [ ] AuthorizationPolicy로 필수 요구
- [ ] 공개 경로 예외 처리

**관련 skill**: `/istio-core`, `/istio-traffic`, `/k8s-security`
