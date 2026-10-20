---
name: istio-gateway
category: service-mesh
description: "Istio Gateway Patterns — Gateway API vs Istio Gateway 비교 허브, 트래픽 라우팅 선택 가이드 Use when working with service-mesh 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Istio Gateway Patterns

Gateway API vs Istio Gateway 비교 허브, 트래픽 라우팅 선택 가이드

## Quick Reference

```
Gateway 선택
    │
    ├─ 신규 구축 ────────────────────> Gateway API (K8s 표준)
    │   └─ Istio 1.22+ 권장
    │
    ├─ 기존 Istio 환경 ──────────────> Istio Gateway 유지
    │   └─ 점진적 마이그레이션 고려
    │
    ├─ 멀티 구현체 이식성 필요 ──────> Gateway API
    │
    ├─ Istio 전용 기능 필수 ─────────> Istio Gateway + VirtualService
    │   └─ EnvoyFilter, 복잡한 매칭
    │
    └─ Ambient Mode ─────────────────> Gateway API 권장
```

---

## CRITICAL: Gateway API vs Istio Gateway 비교표

| 항목 | Istio Gateway | Gateway API |
|------|---------------|-------------|
| **API 표준** | Istio 전용 CRD | K8s SIG 표준 |
| **이식성** | Istio only | 멀티 구현체 (Istio, Envoy Gateway, Kong) |
| **구조** | Gateway + VirtualService | Gateway + HTTPRoute |
| **Cross-namespace** | 암묵적 허용 | ReferenceGrant 명시 필요 |
| **TLS 설정** | credentialName | certificateRefs |
| **Header 매칭** | 강력 (정규식 등) | 표준 기능 |
| **Weight 라우팅** | VirtualService에서 | HTTPRoute backendRefs |
| **성숙도** | 5년+ 검증 | GA (v1) 2023 |
| **Ambient 호환** | 지원 | **권장** |
| **권장** | 기존 환경 유지 | **신규 구축** |

---

## 기능 매핑

```yaml
# Istio Gateway → Gateway API 매핑

# 1. 기본 라우팅
VirtualService.http.match.uri → HTTPRoute.rules.matches.path
VirtualService.http.route     → HTTPRoute.rules.backendRefs

# 2. 헤더 기반 라우팅
VirtualService.http.match.headers → HTTPRoute.rules.matches.headers

# 3. 가중치 라우팅
VirtualService.http.route[].weight → HTTPRoute.rules.backendRefs[].weight

# 4. 리다이렉트
VirtualService.http.redirect → HTTPRoute.rules.filters[].type: RequestRedirect

# 5. 리라이트
VirtualService.http.rewrite → HTTPRoute.rules.filters[].type: URLRewrite
```

---

## 상세 가이드

| 패러다임 | Skill | 내용 |
|----------|-------|------|
| Istio Classic | `/istio-gateway-classic` | Gateway + VirtualService + TLS |
| Gateway API | `/istio-gateway-api` | Gateway + HTTPRoute + ReferenceGrant |

---

## 마이그레이션 가이드

### Istio Gateway → Gateway API

```bash
# 1. Gateway API CRD 설치 확인
kubectl get crd gateways.gateway.networking.k8s.io

# 2. GatewayClass 확인
kubectl get gatewayclass

# 3. 점진적 전환
# - 새 Gateway API 리소스 생성
# - 트래픽 일부 전환
# - 검증 후 기존 리소스 제거
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| Gateway API에서 VirtualService 사용 | 혼용 시 충돌 | 하나만 선택 |
| ReferenceGrant 누락 | Cross-namespace 라우팅 실패 | ReferenceGrant 생성 |
| 모든 Namespace에서 Gateway 접근 | 보안 위험 | allowedRoutes 제한 |
| TLS Secret 다른 namespace | 참조 불가 | 같은 namespace 또는 ReferenceGrant |
| weight 합계 != 100 | 예상치 못한 분배 | 정확히 100으로 |

---

## 체크리스트

### 공통
- [ ] TLS 인증서 갱신 자동화
- [ ] 트래픽 분배 테스트
- [ ] 롤백 계획 수립

**관련 skill**: `/istio-gateway-classic`, `/istio-gateway-api`, `/istio-core`, `/istio-observability`, `/k8s-traffic`
