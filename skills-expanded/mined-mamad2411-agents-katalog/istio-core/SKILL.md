---
name: istio-core
category: service-mesh
description: "Istio Core Patterns — Istio Service Mesh 핵심 개념: Sidecar vs Ambient 모드 비교 및 선택 가이드 Use when working with service-mesh 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Istio Core Patterns

Istio Service Mesh 핵심 개념: Sidecar vs Ambient 모드 비교 및 선택 가이드

## Quick Reference

```
Istio 모드 선택
    │
    ├─ L7 기능 필수 (트레이싱, 세밀한 라우팅) ───> Sidecar Mode
    │
    ├─ 리소스 효율성 우선 ─────────────────────> Ambient Mode
    │   └─ L7 필요 시 ───> waypoint 배포
    │
    ├─ 레거시 앱 (Sidecar 주입 불가) ──────────> Ambient Mode
    │
    ├─ 모니터링 상세도 중요 ───────────────────> Sidecar Mode
    │
    └─ 신규 구축 + 2026 이후 ─────────────────> Ambient Mode 권장
```

---

## Sidecar Mode

### 아키텍처

```
┌─────────────────────────────────────────────────────┐
│  Pod                                                │
│  ┌─────────────────┐    ┌─────────────────┐        │
│  │  Application    │◄──►│  Envoy Proxy    │◄──────►│ 외부
│  │  Container      │    │  (Sidecar)      │        │
│  └─────────────────┘    └─────────────────┘        │
│                                │                    │
│                                ▼                    │
│                         mTLS, L7 정책               │
└─────────────────────────────────────────────────────┘
```

### Sidecar Injection 설정

```yaml
# Namespace 레벨 자동 주입
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    istio-injection: enabled
---
# Pod 레벨 제어
apiVersion: v1
kind: Pod
metadata:
  name: my-app
  annotations:
    # 주입 비활성화
    sidecar.istio.io/inject: "false"

    # 리소스 커스터마이징
    sidecar.istio.io/proxyCPU: "100m"
    sidecar.istio.io/proxyMemory: "128Mi"
    sidecar.istio.io/proxyCPULimit: "500m"
    sidecar.istio.io/proxyMemoryLimit: "512Mi"
```

### Sidecar 리소스 스코핑

```yaml
# 불필요한 설정 수신 제한 (메모리 절약)
apiVersion: networking.istio.io/v1beta1
kind: Sidecar
metadata:
  name: default
  namespace: production
spec:
  workloadSelector:
    labels:
      app: my-app
  egress:
  - hosts:
    - "./*"                    # 같은 namespace만
    - "istio-system/*"         # istio-system
    - "*/payment-service.svc"  # 특정 서비스
  outboundTrafficPolicy:
    mode: REGISTRY_ONLY  # 등록된 서비스만 허용
```

---

## Ambient Mode

### 아키텍처

```
Node Level (ztunnel)                    Namespace Level (waypoint)
┌─────────────────────────────────────────────────────────────────┐
│  Node                                                           │
│  ┌──────────────┐                                               │
│  │   ztunnel    │◄─────── L4 mTLS, 암호화                       │
│  │  (DaemonSet) │                                               │
│  └──────┬───────┘                                               │
│         │                                                       │
│  ┌──────▼───────┐     ┌─────────────────┐                      │
│  │     Pod      │────►│    Waypoint     │◄─── L7 정책 필요 시   │
│  │ (Sidecar 無) │     │   (선택적)      │                      │
│  └──────────────┘     └─────────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
```

### Ambient 활성화

```yaml
# Namespace에 Ambient 적용
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    istio.io/dataplane-mode: ambient
---
# Waypoint 배포 (L7 기능 필요 시)
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: production-waypoint
  namespace: production
  labels:
    istio.io/waypoint-for: service  # 또는 workload
spec:
  gatewayClassName: istio-waypoint
  listeners:
  - name: mesh
    port: 15008
    protocol: HBONE
```

### Waypoint 세부 설정

```yaml
# Service Account별 Waypoint
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: payment-waypoint
  namespace: production
  labels:
    istio.io/waypoint-for: service
  annotations:
    # 리소스 설정
    proxy.istio.io/config: |
      resources:
        requests:
          cpu: 100m
          memory: 128Mi
        limits:
          cpu: 500m
          memory: 512Mi
spec:
  gatewayClassName: istio-waypoint
  listeners:
  - name: mesh
    port: 15008
    protocol: HBONE
    allowedRoutes:
      namespaces:
        from: Same
```

---

## CRITICAL: Sidecar vs Ambient 비교표

| 항목 | Sidecar Mode | Ambient Mode |
|------|-------------|--------------|
| **아키텍처** | Pod당 Envoy Sidecar | Node당 ztunnel + waypoint |
| **리소스** | Pod당 ~50-100MB | **70% 절감 가능** |
| **L4 mTLS** | Sidecar에서 처리 | ztunnel에서 처리 |
| **L7 정책** | 직접 적용 | **waypoint 배포 필요** |
| **모니터링 상세도** | Pod별 상세 메트릭 | **Node/waypoint 레벨** |
| **트레이싱** | 자동 Span 생성 | **ztunnel은 L4만** |
| **성숙도** | 5년+ 검증 | 2024 GA, 발전 중 |
| **앱 변경** | 재배포 필요 | 무중단 적용 |
| **디버깅** | Pod별 명확 | 상대적 복잡 |
| **Startup 지연** | Sidecar 초기화 대기 | 없음 |

### 성능 비교 (실측 기반)

```yaml
# Sidecar Mode
리소스:
  평균 Pod: +80MB 메모리, +50m CPU
  1000 Pod 클러스터: ~80GB 추가 메모리
지연시간:
  P50: +1ms
  P99: +3ms

# Ambient Mode
리소스:
  Node당 ztunnel: ~50MB
  waypoint (L7용): ~100MB
  1000 Pod / 10 Node: ~500MB + waypoint
지연시간:
  L4만: +0.5ms
  L7 (waypoint): +2ms
```

---

## CRITICAL: Ambient Mode 제한사항 (2026.01)

### 미지원/제한 기능

| 기능 | 상태 | 대안 |
|------|------|------|
| **EnvoyFilter** | 미지원 | waypoint용 별도 설정 필요 |
| **Lua Filter** | 미지원 | WasmPlugin 사용 |
| **일부 AuthorizationPolicy** | 제한적 | waypoint 배포 시 L7 가능 |
| **RequestAuthentication (L7)** | waypoint 필요 | L7 정책은 waypoint에서 |
| **Traffic Mirroring** | 제한적 | waypoint 필요 |
| **Fault Injection** | waypoint 필요 | L7 기능 |
| **Custom Headers** | waypoint 필요 | L7 기능 |

### 모니터링 관점 제한

```yaml
# Sidecar Mode에서 가능한 것
- Pod별 상세 메트릭 (istio_requests_total per pod)
- 자동 분산 트레이싱 Span
- Pod 레벨 Access Log

# Ambient Mode 제한
- ztunnel: L4 메트릭만 (TCP 연결, 바이트)
- 트레이싱: waypoint 배포 시에만 L7 Span
- Access Log: ztunnel/waypoint 레벨
```

### 워크로드 호환성

```yaml
# Ambient 호환 확인
지원:
  - 일반 Deployment/StatefulSet
  - Kubernetes Service 통한 통신

제한:
  - hostNetwork: true Pod
  - initContainer 네트워킹 의존
  - 일부 CNI 플러그인 (Calico eBPF 등 확인 필요)
```

---

## 마이그레이션 가이드

### Sidecar → Ambient

```yaml
# Step 1: 준비
# Ambient 지원 Istio 버전 확인 (1.22+)
istioctl version

# Step 2: Namespace 단위 전환
# 기존 Sidecar 레이블 제거
kubectl label namespace production istio-injection-

# Ambient 활성화
kubectl label namespace production istio.io/dataplane-mode=ambient

# Step 3: Pod 재시작 (Sidecar 제거)
kubectl rollout restart deployment -n production

# Step 4: L7 기능 필요 시 waypoint 배포
istioctl waypoint apply -n production --enroll-namespace

# Step 5: 검증
istioctl analyze -n production
```

### Gradual Migration

```yaml
# Namespace 단위 점진적 전환
Phase 1: staging → Ambient
Phase 2: 모니터링 확인 (1주)
Phase 3: production non-critical → Ambient
Phase 4: production critical (신중히)

# 롤백 옵션
kubectl label namespace production istio.io/dataplane-mode-
kubectl label namespace production istio-injection=enabled
kubectl rollout restart deployment -n production
```

---

## 하이브리드 구성

```yaml
# 동일 클러스터에서 혼용
Namespace A: Sidecar Mode (레거시, 상세 모니터링 필요)
Namespace B: Ambient Mode (신규, 리소스 효율)

# 통신 가능
- Sidecar ↔ Ambient: mTLS 자동 협상
- 제한: Cross-namespace L7 정책 시 주의
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| Ambient에서 L7 정책 기대 | 적용 안됨 | waypoint 배포 |
| 모든 앱에 waypoint | 리소스 낭비 | L7 필요한 서비스만 |
| EnvoyFilter 마이그레이션 누락 | 설정 유실 | WasmPlugin 전환 |
| 모니터링 변경 미고려 | 메트릭 손실 | 대시보드 조정 |
| hostNetwork Pod 포함 | 동작 안함 | 해당 Pod 제외 |

---

## 체크리스트

### Sidecar Mode
- [ ] Namespace 레이블 설정
- [ ] 리소스 limit 설정
- [ ] Sidecar 스코핑 (필요 시)
- [ ] Startup probe 조정

### Ambient Mode
- [ ] Istio 버전 확인 (1.22+)
- [ ] CNI 호환성 확인
- [ ] Namespace 레이블 변경
- [ ] L7 필요 서비스에 waypoint 배포
- [ ] 모니터링 대시보드 조정

### 마이그레이션
- [ ] 기능 매핑 검토 (EnvoyFilter 등)
- [ ] 단계별 전환 계획
- [ ] 롤백 계획 수립
- [ ] 모니터링 알림 조정

---

## CRITICAL: mTLS 강제 설정

### Namespace STRICT mTLS

```yaml
# 네임스페이스 전체에 mTLS 강제
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT  # 모든 트래픽 mTLS 필수
```

### 메시 전체 STRICT mTLS

```yaml
# 전체 메시에 mTLS 강제 (istio-system에 적용)
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: STRICT
```

### 특정 포트 예외 (메트릭 수집)

```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: metrics-exception
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

### mTLS 마이그레이션 단계

```
1. PERMISSIVE 모드로 시작 (기존 트래픽 유지)
   │
2. Kiali에서 mTLS 적용 현황 확인
   │
3. 모든 서비스에 Sidecar 주입 완료 확인
   │
4. STRICT 모드로 전환
   │
5. 문제 발생 시 PERMISSIVE로 롤백
```

### mTLS 상태 확인

```bash
# istioctl로 mTLS 상태 확인
istioctl authn tls-check <pod-name> -n <namespace>

# PeerAuthentication 목록
kubectl get peerauthentication -A

# 특정 Pod의 mTLS 설정 확인
istioctl x describe pod <pod-name> -n <namespace>
```

상세한 Istio 보안 설정은 `/istio-security` 스킬 참조

---

**참조 스킬**: `/istio-ambient` (Ambient 심화: 아키텍처 상세, ztunnel, Waypoint 고급, Cilium 통합, 모니터링/트러블슈팅), `/istio-gateway`, `/istio-observability`, `/istio-security`, `/k8s-security`, `/ebpf-observability`
