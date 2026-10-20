---
name: istio-ambient
category: service-mesh
description: "Istio Ambient Mode 심화 가이드 — Ambient GA (Istio 1.24+), ztunnel, HBONE, Waypoint 고급 설정, targetRefs, Cilium 통합 Use when working with service-mesh 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Istio Ambient Mode 심화 가이드

Ambient GA (Istio 1.24+), ztunnel, HBONE, Waypoint 고급 설정, targetRefs, Cilium 통합

## CRITICAL: Ambient Mode (GA - Istio 1.24)

```
Istio 1.24 (2024-11)에서 Ambient Mode GA 달성
- ztunnel, Waypoint API 모두 Stable
- Sidecar 없이 서비스 메시 기능 제공
- L4/L7 분리 아키텍처
```

### 아키텍처 상세

```
+------------------------------------------------------------------+
|                   Istio Ambient Mode Architecture                  |
+------------------------------------------------------------------+
|                                                                    |
|  +--------------------------------------------------------------+ |
|  |                        Control Plane                          | |
|  |  +---------+  +---------+  +---------+                       | |
|  |  | Istiod  |  | Istiod  |  | Istiod  |  (HA)                 | |
|  |  +----+----+  +----+----+  +----+----+                       | |
|  +-------+------------+------------+----------------------------+ |
|          | xDS        |            |                              |
|          v            v            v                              |
|  +--------------------------------------------------------------+ |
|  |                         Data Plane                            | |
|  |                                                                | |
|  |  Node 1                          Node 2                       | |
|  |  +--------------------+         +--------------------+       | |
|  |  | ztunnel (DaemonSet)|         | ztunnel (DaemonSet)|       | |
|  |  | - Rust 기반         |         | - Rust 기반         |       | |
|  |  | - L4 mTLS + 정책   |         | - L4 mTLS + 정책   |       | |
|  |  | - HBONE 터널링     |         | - HBONE 터널링     |       | |
|  |  +--------+-----------+         +--------+-----------+       | |
|  |           |                              |                    | |
|  |  +--------v-----------+         +--------v-----------+       | |
|  |  |   Pod (Sidecar 無) |         |   Pod (Sidecar 無) |       | |
|  |  +--------------------+         +--------------------+       | |
|  |                                                                | |
|  |  Waypoint Proxy (L7 필요 시에만):                             | |
|  |  +------------------------------------------------------------+ |
|  |  | Envoy 기반 per-namespace/service 배포                     | |
|  |  | - HTTP 라우팅, AuthZ, 트레이싱                            | |
|  |  | - Gateway API로 선언                                      | |
|  |  +------------------------------------------------------------+ |
|  +--------------------------------------------------------------+ |
+------------------------------------------------------------------+
```

---

## HBONE 프로토콜

### 트래픽 흐름

```
L4 Only (Waypoint 없음):
  App Pod → ztunnel(src) ──[HBONE/mTLS]──> ztunnel(dst) → App Pod

L7 필요 (Waypoint 있음):
  App Pod → ztunnel(src) ──[HBONE]──> Waypoint ──> ztunnel(dst) → App Pod
```

### HBONE 상세

```
- HTTP CONNECT 기반 터널링 프로토콜
- 포트 15008 사용 (ztunnel ↔ ztunnel, ztunnel ↔ waypoint)
- mTLS 자동 적용 (SPIFFE ID 기반)
- HTTP/2 멀티플렉싱 지원
- 기존 TCP 연결 위에 투명하게 동작
```

---

## Ambient 활성화

### 네임스페이스 레이블

```bash
# Ambient 모드 활성화
kubectl label namespace production istio.io/dataplane-mode=ambient

# Ambient 비활성화 (Sidecar로 복원)
kubectl label namespace production istio.io/dataplane-mode-

# 특정 Pod 제외 (opt-out)
kubectl label pod <pod-name> istio.io/dataplane-mode=none
```

### ztunnel 확인

```bash
# ztunnel DaemonSet 상태
kubectl get pods -n istio-system -l app=ztunnel

# ztunnel 로그
kubectl logs -n istio-system -l app=ztunnel -c istio-proxy

# ztunnel 메트릭
# istio_tcp_connections_opened_total
# istio_tcp_connections_closed_total
# istio_tcp_sent_bytes_total
# istio_tcp_received_bytes_total
```

---

## Waypoint Proxy

### 네임스페이스 Waypoint

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: production-waypoint
  namespace: production
  labels:
    istio.io/waypoint-for: service    # service | workload | all
spec:
  gatewayClassName: istio-waypoint
  listeners:
  - name: mesh
    port: 15008
    protocol: HBONE
```

### 서비스별 Waypoint (세밀한 제어)

```yaml
# 특정 서비스 어카운트에만 적용
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: payment-waypoint
  namespace: production
  labels:
    istio.io/waypoint-for: service
  annotations:
    istio.io/for-service-account: payment-service
spec:
  gatewayClassName: istio-waypoint
  listeners:
  - name: mesh
    port: 15008
    protocol: HBONE
```

### Waypoint 리소스 튜닝

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: high-traffic-waypoint
  namespace: production
  labels:
    istio.io/waypoint-for: service
  annotations:
    proxy.istio.io/config: |
      concurrency: 4
      resources:
        requests:
          cpu: 200m
          memory: 256Mi
        limits:
          cpu: 1000m
          memory: 1Gi
spec:
  gatewayClassName: istio-waypoint
  listeners:
  - name: mesh
    port: 15008
    protocol: HBONE
```

### istioctl 관리

```bash
# Waypoint 생성 (CLI)
istioctl waypoint apply -n production --name production-waypoint

# 서비스별 Waypoint
istioctl waypoint apply -n production --name payment-wp \
  --for service --service-account payment-service

# Waypoint 상태 확인
istioctl waypoint status -n production

# Waypoint 목록
istioctl waypoint list -n production
```

---

## CRITICAL: targetRefs 패턴 (Ambient 정책)

### Ambient에서 L7 정책 적용

```
Ambient에서 L7 정책(AuthorizationPolicy, RequestAuthentication)은
targetRefs를 사용하여 Waypoint가 있는 서비스에 적용.

selector (기존 Sidecar용) vs targetRefs (Ambient 권장):
- selector: Pod label 기반 (Sidecar 모드)
- targetRefs: Service/Gateway 참조 (Ambient 모드, 양쪽 모두 동작)
```

### AuthorizationPolicy (targetRefs)

```yaml
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: payment-authz
  namespace: production
spec:
  targetRefs:
  - kind: Service
    group: ""
    name: payment-service
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/production/sa/order-service"]
    to:
    - operation:
        methods: ["POST"]
        paths: ["/api/v1/payments"]
```

### RequestAuthentication (targetRefs)

```yaml
apiVersion: security.istio.io/v1
kind: RequestAuthentication
metadata:
  name: jwt-auth
  namespace: production
spec:
  targetRefs:
  - kind: Service
    group: ""
    name: api-gateway
  jwtRules:
  - issuer: "https://auth.example.com"
    jwksUri: "https://auth.example.com/.well-known/jwks.json"
    forwardOriginalToken: true
```

### L4 정책 (Waypoint 불필요)

```yaml
# PeerAuthentication은 ztunnel에서 처리 (Waypoint 불필요)
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: strict-mtls
  namespace: production
spec:
  mtls:
    mode: STRICT
---
# L4 AuthorizationPolicy (source principal 기반)
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: l4-deny
  namespace: production
spec:
  action: DENY
  rules:
  - from:
    - source:
        namespaces: ["development"]
```

---

## Cilium + Istio Ambient 통합

```yaml
# Cilium이 CNI인 환경에서 Ambient 설치

# 1. Cilium 설정 확인
# Cilium은 L3/L4 네트워크 정책
# Istio Ambient는 mTLS + L4/L7 정책 (보완적)

# 2. 설치
istioctl install --set profile=ambient \
  --set values.cni.provider=cilium

# 주의사항:
# - Cilium eBPF 모드와 ztunnel 트래픽 인터셉트 충돌 가능
# - 커널 5.10+ 권장
# - 네트워크 정책 중복 확인 필요
# - Cilium의 kube-proxy 대체 모드 호환성 확인
```

---

## 모니터링

### reporter 라벨로 구분

```yaml
# Prometheus 쿼리

# ztunnel 연결 수 (L4)
sum(istio_tcp_connections_opened_total{reporter="ztunnel"}) by (destination_workload)

# L4 트래픽 볼륨
sum(rate(istio_tcp_sent_bytes_total{reporter="ztunnel"}[5m]))
  by (source_workload, destination_workload)

# Waypoint 메트릭 (L7)
sum(rate(istio_requests_total{reporter="waypoint"}[5m]))
  by (destination_service, response_code)

# 비교 대시보드:
# reporter="source"   → Sidecar 모드
# reporter="ztunnel"  → Ambient L4
# reporter="waypoint" → Ambient L7
```

### 텔레메트리 차이

| 기능 | ztunnel (L4) | waypoint (L7) |
|------|-------------|---------------|
| TCP 메트릭 | O | O |
| HTTP 메트릭 | X | O |
| 트레이싱 Span | X | O |
| Access Log | L4 | L7 |
| 권장 보완 | 앱 OTel SDK | 헤더 전파만 |

---

## 트러블슈팅

```bash
# 1. Ambient 적용 상태 확인
kubectl get namespace production -o yaml | grep dataplane-mode

# 2. ztunnel 연결 상태
kubectl exec -n istio-system \
  $(kubectl get pod -n istio-system -l app=ztunnel \
    -o jsonpath='{.items[0].metadata.name}') \
  -- curl localhost:15020/healthz

# 3. Waypoint 상태 확인
kubectl get gateway -n production -l istio.io/waypoint-for

# 4. Waypoint 상세 상태
istioctl waypoint status -n production

# 5. HBONE 연결 테스트
istioctl x waypoint status -n production

# 6. 트래픽 흐름 확인
kubectl logs -n istio-system -l app=ztunnel --tail=100 | grep "connection"

# 7. Envoy 설정 확인 (Waypoint)
istioctl proxy-config routes \
  $(kubectl get pod -n production -l gateway.istio.io/managed -o name | head -1) \
  -n production
```

---

## 마이그레이션 체크리스트

### Sidecar → Ambient 전환

### 사전 확인
- [ ] Istio 1.24+ 확인 (Ambient GA)
- [ ] 커널 5.10+ 확인
- [ ] CNI 호환성 확인 (Cilium 주의)
- [ ] EnvoyFilter 사용 현황 분석 (Ambient 미지원)
- [ ] WasmPlugin 사용 현황 확인

### 전환 단계
- [ ] Namespace 레이블 전환 (`istio.io/dataplane-mode=ambient`)
- [ ] Pod 재시작 (Sidecar 제거 확인)
- [ ] L7 필요 서비스에 Waypoint 배포
- [ ] mTLS 연결 검증
- [ ] AuthorizationPolicy `selector` → `targetRefs` 전환

### 전환 후
- [ ] 모니터링 대시보드 reporter 라벨 조정
- [ ] 알림 규칙 업데이트 (ztunnel/waypoint 메트릭)
- [ ] 성능/리소스 사용량 비교
- [ ] 앱 OTel SDK 계측 추가 (L7 없는 서비스)

---

**참조 스킬**: `/istio-core`, `/istio-gateway`, `/istio-otel`, `/istio-security`, `/k8s-security`, `/istio-ext-authz`
