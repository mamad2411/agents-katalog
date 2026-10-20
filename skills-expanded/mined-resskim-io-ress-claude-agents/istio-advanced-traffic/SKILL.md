---
name: istio-advanced-traffic
category: service-mesh
description: "Istio 고급 트래픽 관리 — Fault Injection, Traffic Mirroring, Retry/Timeout 심화, JWT Claim 라우팅, Blue-Green/Canary 패턴 Use when working with service-mesh 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Istio 고급 트래픽 관리

Fault Injection, Traffic Mirroring, Retry/Timeout 심화, JWT Claim 라우팅, Blue-Green/Canary 패턴

## Quick Reference (결정 트리)

```
트래픽 관리 요구사항?
    │
    ├─ 장애 복원력 ──────────> Retry + Timeout + Circuit Breaker
    │       │
    │       ├─ 재시도 조건 ──> retryOn (5xx, connect-failure, retriable-status-codes)
    │       ├─ 타임아웃 ────> timeout + perTryTimeout 조합
    │       └─ Fault Injection → 카오스 테스트 (delay / abort)
    │
    ├─ 배포 전략 ────────────> Canary / Blue-Green / Traffic Mirroring
    │       │
    │       ├─ 점진적 전환 ──> weight 기반 Canary
    │       ├─ 즉시 전환 ────> subset 기반 Blue-Green
    │       └─ 안전 검증 ────> Traffic Mirroring (fire-and-forget)
    │
    └─ 라우팅 분기 ──────────> Header / JWT Claim 기반
            │
            ├─ 헤더 매칭 ────> match.headers (exact, prefix, regex)
            └─ JWT 클레임 ──> @request.auth.claims (Gateway에서만)
```

---

## CRITICAL: DestinationRule TrafficPolicy 심화

### 프로덕션 권장 설정

```yaml
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: payment-service
  namespace: production
spec:
  host: payment-service
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
        connectTimeout: 500ms
        tcpKeepalive:
          time: 7200s
          interval: 75s
      http:
        http2MaxRequests: 1000
        maxRequestsPerConnection: 10
        h2UpgradePolicy: DEFAULT
        maxRetries: 3
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 10s
      baseEjectionTime: 30s
      maxEjectionPercent: 30
      minHealthPercent: 50
    loadBalancer:
      simple: LEAST_REQUEST
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
    trafficPolicy:               # subset별 오버라이드 가능
      connectionPool:
        http:
          http2MaxRequests: 500   # canary는 낮게
```

### 주요 필드 설명

| 필드 | 설명 | 권장값 |
|------|------|--------|
| `tcp.maxConnections` | 최대 TCP 연결 수 | 서비스 특성에 맞게 |
| `tcp.connectTimeout` | TCP 연결 타임아웃 | 500ms ~ 1s |
| `tcp.tcpKeepalive` | TCP Keepalive 설정 | time: 7200s |
| `http.http2MaxRequests` | 최대 동시 HTTP/2 요청 | 1000 |
| `http.maxRequestsPerConnection` | 연결당 최대 요청 | 10 (연결 재활용) |
| `http.h2UpgradePolicy` | HTTP/2 업그레이드 | DEFAULT |
| `outlierDetection.consecutive5xxErrors` | 연속 5xx 에러 임계값 | 5 |
| `outlierDetection.interval` | 분석 주기 | 10s |
| `outlierDetection.baseEjectionTime` | 최소 제거 시간 | 30s |
| `outlierDetection.maxEjectionPercent` | 최대 제거 비율 | 30~50% |
| `outlierDetection.minHealthPercent` | 최소 건강 비율 | 50% |

### 로드밸런서 알고리즘

| 알고리즘 | 설명 | 적합 시나리오 |
|----------|------|---------------|
| `ROUND_ROBIN` | 순차 분배 (기본) | 균일한 처리 시간 |
| `LEAST_REQUEST` | 가장 적은 요청 수 | 불균일한 처리 시간 |
| `RANDOM` | 랜덤 분배 | 대규모 인스턴스 |
| `PASSTHROUGH` | 원본 목적지 유지 | 특수 케이스 |

---

## Retry + Timeout 심화

### 고급 Retry 설정

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: payment-vs
  namespace: production
spec:
  hosts: ["payment-service"]
  http:
  - route:
    - destination:
        host: payment-service
    timeout: 10s                  # 전체 타임아웃
    retries:
      attempts: 3                 # 최대 재시도 횟수
      perTryTimeout: 3s           # 시도당 타임아웃
      retryOn: "connect-failure,refused-stream,503,retriable-status-codes"
      retryRemoteLocalities: true # 다른 로컬리티에서 재시도
```

### retryOn 조건 상세

| 조건 | 설명 |
|------|------|
| `5xx` | 모든 5xx 응답 |
| `connect-failure` | 연결 실패 |
| `refused-stream` | REFUSED_STREAM 에러 |
| `gateway-error` | 502, 503, 504 |
| `retriable-status-codes` | x-envoy-retriable-status-codes 헤더 참조 |
| `reset` | 연결 리셋 |
| `retriable-4xx` | 409 Conflict |
| `retriable-headers` | 헤더 기반 재시도 조건 |

### CRITICAL: Timeout 설계 원칙

```
전체 timeout > attempts × perTryTimeout

예: timeout=10s, attempts=3, perTryTimeout=3s
    → 최대 9s 소요 (3회 × 3s), 10s 내 완료
    → perTryTimeout이 timeout보다 크면 timeout이 우선

주의: Istio 기본 timeout은 disabled (무제한)
     → 반드시 명시적으로 설정할 것
```

---

## Fault Injection (카오스 테스트)

### Delay Injection (지연 주입)

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: payment-fault-delay
  namespace: production
spec:
  hosts: ["payment-service"]
  http:
  - fault:
      delay:
        percentage:
          value: 10.0              # 10% 요청에 지연
        fixedDelay: 5s             # 5초 지연
    route:
    - destination:
        host: payment-service
```

### Abort Injection (에러 주입)

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: payment-fault-abort
  namespace: staging
spec:
  hosts: ["payment-service"]
  http:
  - fault:
      abort:
        percentage:
          value: 5.0               # 5% 요청에 에러
        httpStatus: 503            # 503 반환
    route:
    - destination:
        host: payment-service
```

### Delay + Abort 조합

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: chaos-test
  namespace: staging
spec:
  hosts: ["order-service"]
  http:
  # 특정 테스터만 Fault Injection (안전)
  - match:
    - headers:
        x-chaos-test:
          exact: "true"
    fault:
      delay:
        percentage:
          value: 50.0
        fixedDelay: 3s
      abort:
        percentage:
          value: 10.0
        httpStatus: 500
    route:
    - destination:
        host: order-service
  # 일반 트래픽은 정상
  - route:
    - destination:
        host: order-service
```

### CRITICAL: Fault Injection 주의사항

```
1. Fault Injection은 retry/timeout과 같은 route에서 주의
   - delay가 timeout보다 크면 timeout이 먼저 발생
   - retry + abort 조합 시 재시도 후에도 abort 발생 가능

2. 프로덕션에서는 반드시 헤더 매칭으로 범위 제한
   - match.headers로 테스트 트래픽만 적용

3. 권장 순서:
   staging에서 검증 → 프로덕션 일부(헤더 제한) → 점진적 확대
```

---

## Canary 배포 패턴

### Weight 기반 점진적 전환

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: product-canary
  namespace: production
spec:
  hosts: ["product-service"]
  http:
  - route:
    - destination:
        host: product-service
        subset: stable
      weight: 90
    - destination:
        host: product-service
        subset: canary
      weight: 10
---
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: product-dr
  namespace: production
spec:
  host: product-service
  subsets:
  - name: stable
    labels:
      version: v1
  - name: canary
    labels:
      version: v2
```

### Header + Weight 조합 (내부 테스터 우선)

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: product-canary-header
  namespace: production
spec:
  hosts: ["product-service"]
  http:
  # 내부 테스터 → 항상 canary
  - match:
    - headers:
        x-canary:
          exact: "true"
    route:
    - destination:
        host: product-service
        subset: canary
  # 일반 트래픽 → 가중치 분배
  - route:
    - destination:
        host: product-service
        subset: stable
      weight: 95
    - destination:
        host: product-service
        subset: canary
      weight: 5
```

---

## Blue-Green 배포 패턴

### Subset Switch (즉시 전환)

```yaml
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: product-dr
  namespace: production
spec:
  host: product-service
  subsets:
  - name: blue
    labels:
      version: v1
  - name: green
    labels:
      version: v2
---
# Blue → Green 전환 (weight 100% 변경)
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: product-bg
  namespace: production
spec:
  hosts: ["product-service"]
  http:
  - route:
    - destination:
        host: product-service
        subset: green     # blue → green으로 변경
      weight: 100
```

### 롤백: `subset: green` → `subset: blue` 변경만으로 즉시 롤백

---

## Traffic Mirroring (Shadow Testing)

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: product-mirror
  namespace: production
spec:
  hosts: ["product-service"]
  http:
  - route:
    - destination:
        host: product-service
        subset: v1
    mirror:
      host: product-service
      subset: v2
    mirrorPercentage:
      value: 50.0             # 50% 미러링
```

### CRITICAL: Mirror 특성

```
- Fire-and-forget: 미러 응답은 클라이언트에 반환되지 않음
- Host 헤더에 "-shadow" 접미사 자동 추가
- 미러 대상의 에러가 원본에 영향 없음
- 용도: 새 버전 성능 테스트, 데이터 검증, 로드 테스트
- 주의: 부작용 있는 요청(POST) 미러링 시 중복 처리 위험
```

---

## JWT Claim 기반 라우팅

### Gateway에서 JWT 라우팅

```yaml
# 1. RequestAuthentication 먼저 설정
apiVersion: security.istio.io/v1
kind: RequestAuthentication
metadata:
  name: jwt-auth
  namespace: istio-system
spec:
  selector:
    matchLabels:
      istio: ingressgateway
  jwtRules:
  - issuer: "https://auth.example.com"
    jwksUri: "https://auth.example.com/.well-known/jwks.json"
    forwardOriginalToken: true
---
# 2. VirtualService에서 JWT 클레임 기반 라우팅
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: api-routing
  namespace: production
spec:
  hosts: ["api.example.com"]
  gateways: ["istio-system/api-gateway"]
  http:
  # admin 클레임 → admin 서비스
  - match:
    - headers:
        "@request.auth.claims.role":
          exact: "admin"
    route:
    - destination:
        host: admin-api
        port:
          number: 8080
  # premium 클레임 → premium 서비스
  - match:
    - headers:
        "@request.auth.claims.tier":
          exact: "premium"
    route:
    - destination:
        host: premium-api
        port:
          number: 8080
  # 기본 → public 서비스
  - route:
    - destination:
        host: public-api
        port:
          number: 8080
```

### Nested Claim 접근

```yaml
# JWT payload: {"realm_access": {"roles": ["admin"]}}
# AuthorizationPolicy에서 nested claim 접근
when:
- key: request.auth.claims[realm_access][roles]
  values: ["admin"]

# 참고: VirtualService 라우팅은 최상위 클레임만 지원
# nested claim 라우팅은 AuthorizationPolicy + 서비스 라우팅으로 대체
```

### CRITICAL: JWT 라우팅 제한사항

```
1. Ingress Gateway에서만 동작 (mesh 내부 서비스 간은 불가)
2. 최상위 클레임만 VirtualService에서 접근 가능
3. nested claim은 AuthorizationPolicy의 when 조건으로 처리
4. RequestAuthentication이 반드시 먼저 설정되어야 함
```

---

## 디버깅

```bash
# VirtualService 적용 상태 확인
istioctl analyze -n production

# Envoy 라우팅 설정 확인
istioctl proxy-config routes <pod-name> -n production -o json

# DestinationRule 적용 확인
istioctl proxy-config cluster <pod-name> -n production

# 트래픽 분배 확인 (Prometheus)
# rate(istio_requests_total{destination_service="product-service"}[5m])
# group by destination_version
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| timeout 미설정 | 무한 대기 | 명시적 timeout 설정 |
| perTryTimeout > timeout | 재시도 무의미 | perTryTimeout < timeout/attempts |
| POST 미러링 | 중복 처리 | 읽기 전용 요청만 미러링 |
| Canary weight 급격 변경 | 장애 확산 | 5% → 10% → 25% → 50% → 100% |
| Fault Injection 전체 적용 | 서비스 장애 | 헤더 매칭으로 범위 제한 |
| JWT 라우팅 mesh 내부 시도 | 동작 안 함 | Gateway에서만 사용 |

---

## 체크리스트

### Retry/Timeout
- [ ] 전체 timeout 명시적 설정
- [ ] perTryTimeout × attempts < timeout 확인
- [ ] retryOn 조건 서비스에 맞게 설정
- [ ] 멱등성 없는 요청 재시도 비활성화 검토

### 배포 전략
- [ ] DestinationRule subset 정의
- [ ] Canary weight 점진적 변경 계획
- [ ] 롤백 절차 문서화
- [ ] 미러링 대상 부작용 검토

### Fault Injection
- [ ] staging에서 먼저 검증
- [ ] 헤더 매칭으로 범위 제한
- [ ] 모니터링 대시보드 준비
- [ ] 자동 롤백 조건 정의

**관련 skill**: `/istio-gateway-classic`, `/k8s-traffic-istio`, `/istio-security`, `/deployment-canary`
