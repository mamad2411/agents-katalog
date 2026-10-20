---
name: istio-observability
category: service-mesh
description: "Istio Observability Patterns — Istio 모니터링 통합 허브: 메트릭, 트레이싱, Kiali 가이드 Use when working with service-mesh 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Istio Observability Patterns

Istio 모니터링 통합 허브: 메트릭, 트레이싱, Kiali 가이드

## Quick Reference

```
모니터링 설정
    │
    ├─ Sidecar Mode ─────────────────> Pod별 상세 메트릭
    │   └─ istio_requests_total (pod 레이블)
    │
    ├─ Ambient Mode ─────────────────> Node/Waypoint 레벨
    │   ├─ ztunnel: L4 메트릭만
    │   └─ waypoint: L7 메트릭 (배포 시)
    │
    ├─ 트레이싱 필수 ────────────────> Sidecar 또는 Waypoint
    │
    └─ 서비스 토폴로지 ──────────────> Kiali + Prometheus
```

---

## CRITICAL: 모드별 메트릭 수집 아키텍처

### Sidecar Mode

```
┌────────────────────────────────────────────────────────────────┐
│  Pod                                                           │
│  ┌─────────────┐    ┌─────────────┐                           │
│  │ Application │◄──►│   Envoy     │──► /stats/prometheus      │
│  └─────────────┘    │  (Sidecar)  │    :15020                 │
│                     └──────┬──────┘                           │
│                            │                                   │
│                            ▼                                   │
│                     Per-Pod 메트릭                             │
│                     - istio_requests_total                     │
│                     - istio_request_duration                   │
│                     - 자동 Span 생성                           │
└────────────────────────────────────────────────────────────────┘
```

### Ambient Mode

```
┌────────────────────────────────────────────────────────────────┐
│  Node                                                          │
│  ┌─────────────┐                                               │
│  │   ztunnel   │──► /stats/prometheus                         │
│  │ (DaemonSet) │    - L4 메트릭만 (TCP 연결, 바이트)           │
│  └──────┬──────┘                                               │
│         │                                                      │
│  ┌──────▼──────┐    ┌─────────────┐                           │
│  │    Pod      │───►│  Waypoint   │──► L7 메트릭 (선택적)      │
│  │ (Sidecar無) │    │  (필요 시)  │    - istio_requests_total  │
│  └─────────────┘    └─────────────┘                           │
└────────────────────────────────────────────────────────────────┘
```

---

## 모드별 메트릭 비교

| 메트릭 | Sidecar | Ambient (ztunnel) | Ambient (waypoint) |
|--------|---------|-------------------|-------------------|
| `istio_requests_total` | Pod별 상세 | 미지원 | Service별 |
| `istio_request_duration_milliseconds` | Pod별 | 미지원 | Service별 |
| `istio_tcp_connections_opened_total` | Pod별 | Node별 | - |
| `istio_tcp_sent_bytes_total` | Pod별 | Node별 | - |
| 트레이싱 Span | 자동 생성 | L4만 | L7 Span |
| Access Log | Pod별 | ztunnel 로그 | waypoint 로그 |

---

## 구성요소별 상세 가이드

| 주제 | Skill | 내용 |
|------|-------|------|
| Prometheus 연동 | `/istio-metrics` | ServiceMonitor, RED 쿼리, Grafana |
| 분산 트레이싱 | `/istio-tracing` | Jaeger/Tempo, Access Logging, OTel |
| 시각화 (Kiali) | 본 skill 내 §Kiali | 설정, 서비스 토폴로지 (흡수 예정) |

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| Ambient에서 Pod별 메트릭 기대 | 불가능 | ztunnel/waypoint 메트릭 사용 |
| 높은 샘플링 비율 (100%) | 스토리지 폭증 | 1-5%로 조정 |
| 모든 레이블 유지 | 카디널리티 폭발 | Telemetry로 레이블 제거 |
| Access Log 전체 활성화 | 성능 저하 | 필터링 적용 |
| Kiali 없이 Ambient | 디버깅 어려움 | Kiali 1.80+ 설치 |

---

## 체크리스트

### Ambient 전환 시
- [ ] 기존 대시보드 호환성 검토
- [ ] ztunnel 메트릭 추가
- [ ] waypoint 메트릭 추가 (L7용)
- [ ] Kiali 버전 확인 (1.80+)

**관련 skill**: `/istio-metrics`, `/istio-tracing`, `/istio-core`, `/istio-gateway`, `/observability-otel`
