---
name: istio-pitfalls
category: service-mesh
description: "Istio 실전 Pitfalls — 실전 트러블슈팅 + 보안 검증 기반 Istio 실전 함정. FQDN/AuthZ/PeerAuthentication/Gateway/sidecar injection. Use when working with service-mesh 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Istio 실전 Pitfalls

실전 트러블슈팅 + 보안 검증 기반 Istio 실전 함정. FQDN/AuthZ/PeerAuthentication/Gateway/sidecar injection.
기존 Istio skills는 기능/설정 중심이나, 이 문서는 **실제 장애 + 보안 우회** 중심.

---

## 1. VirtualService FQDN 필수

### 문제
Gateway에서 `user-service.app-ns.svc`로 라우팅 → 503 에러.

### 원인
Gateway pod(istio-ingressgateway)은 `kube-system` 네임스페이스에서 실행됨.
해당 pod의 `/etc/resolv.conf`에는 `search kube-system.svc.cluster.local`만 있으므로
`.svc`는 `user-service.app-ns.svc.kube-system.svc.cluster.local`로 해석 → 존재하지 않음.

### 해결
```yaml
# BAD
destination:
  host: user-service.app-ns.svc

# GOOD
destination:
  host: user-service.app-ns.svc.cluster.local
```

### 교훈
cross-namespace 참조 시 항상 FQDN. VirtualService, DestinationRule, ServiceEntry 모두 동일.

---

## 2. AuthorizationPolicy 경로 매칭

### Glob-style 매칭
- `abc*` = `abc` + `abcd` + `abc/xyz` (zero-or-more characters)
- `/api/*` = `/api` + `/api/v1` + `/api/v1/users/123` (주의: 모든 depth 매칭)

### URI Template (Istio 1.22+, 권장)
```yaml
# 단일 segment만 매칭
paths: ["/api/{*}"]
# /api/users ✓, /api/users/123 ✗

# 다중 segment 매칭
paths: ["/api/{**}"]
# /api/users/123/orders ✓
```

### 보안: Path Normalization 우회 기법

| 공격 | 예시 | 우회 대상 |
|------|------|----------|
| Double slash | `//admin` | `/admin` 정책 |
| Encoded slash | `%2Fadmin` | path 분리 |
| Fragment | `/profile#section` | path 필터 |
| Path parameter | `/admin;param=val` | 경로 인식 |

**필수 설정**:
```yaml
meshConfig:
  pathNormalization:
    normalization: DECODE_AND_MERGE_SLASHES
```

DENY 규칙보다 ALLOW + positive matching을 선호 — DENY는 normalization 차이에 더 취약.

---

## 3. Retry + Idempotency

### 사고 사례 (2026-04-03)
Payment VirtualService에 `retryOn: 5xx` 설정 → POST 요청 실패 시 자동 retry → 결제 2회 처리.

### Istio 1.24 개선
`EXCLUDE_UNSAFE_503_FROM_DEFAULT_RETRY` 기본 활성화 — 기본 retry 정책에서 503 제외.
그러나 **명시적 VirtualService retry 설정은 기본 정책을 덮어씀**.

### 안전한 설정
```yaml
retries:
  attempts: 3
  retryOn: reset,connect-failure  # 서버에 도달하지 않은 경우만
  # NEVER: 5xx, gateway-error (POST에서 중복 발생)
```

### 대안
non-idempotent 엔드포인트에 idempotency key 패턴 구현:
```
Request-Id: uuid → 서버측 중복 체크 → 이미 처리된 요청은 cached response 반환
```

---

## 4. PeerAuthentication Selector

### 사고 사례 (2026-04-08)
Prometheus scrape 허용을 위해 `portLevelMtls` PERMISSIVE 설정 → `spec.selector` 누락 → namespace 전체 pod에 적용 → 503.

### 올바른 패턴
```yaml
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: prometheus-metrics-exception
  namespace: app-ns
spec:
  selector:
    matchLabels:
      app: user-service  # 특정 워크로드만 대상
  mtls:
    mode: STRICT
  portLevelMtls:
    "8080":
      mode: PERMISSIVE  # metrics port만 예외
```

**반드시** AuthorizationPolicy로 해당 port 접근을 모니터링 NS로 제한.

---

## 5. JWKS 자동 로테이션

### 문제
RequestAuthentication의 JWKS를 Secret에 하드코딩 → CDN key rotation 시 401.

### 해결 패턴
```
SSM Parameter Store (JWKS JSON)
  → ExternalSecret (자동 동기화)
  → K8s Secret
  → RequestAuthentication jwtRules[].jwksUri 또는 인라인 참조
```

ExternalSecret `refreshInterval`을 key rotation 주기보다 짧게 설정.

---

## 6. Native Sidecars vs holdApplicationUntilProxyStarts

### holdApplicationUntilProxyStarts (기존 방식)
- Envoy ready 될 때까지 app container 시작 지연
- 단점: Envoy 장애 시 app도 시작 불가, shutdown 순서 미보장

### Native Sidecars (K8s 1.28+, 권장)
```yaml
# istiod 설정
ENABLE_NATIVE_SIDECARS: "true"
```
- K8s가 init container(restartPolicy: Always) 시작 순서 보장
- `holdApplicationUntilProxyStarts`, `terminationDrainDuration` 모두 불필요 (무시됨)
- Shutdown 순서도 자동 보장 (app → sidecar 순서)

---

## 7. forwardOriginalToken 보안

### `forwardOriginalToken: true`
- 원본 JWT를 upstream으로 전달 → upstream에서 claims 사용 가능
- **위험**: token relay 공격, scope 누출, lateral movement

### `outputPayloadToHeader` (권장)
- 검증된 claims만 헤더로 전달 (원본 토큰 미전달)
- upstream은 `X-Jwt-Payload` 등 커스텀 헤더에서 claims 추출

### 결정 기준
- 내부 서비스 간: mTLS identity(SPIFFE) 사용, JWT 미전달
- 외부 서비스 호출: `forwardOriginalToken` 불가피 → 서비스별 scoped token 발급 패턴 고려

---

## 8. STRICT mTLS + Prometheus Scrape

### 패턴
1. Mesh-wide STRICT mTLS (기본)
2. Prometheus가 mesh 내부에 있으면 → mTLS로 scrape (추가 설정 불필요)
3. Prometheus가 mesh 외부에 있으면:
   - PeerAuthentication: 해당 워크로드 + metrics port만 `DISABLE` (PERMISSIVE보다 명확)
   - AuthorizationPolicy: 해당 port에 monitoring namespace만 허용
