---
name: ebpf-observability-advanced
category: observability
description: "eBPF Observability 고급 가이드 — Cilium Hubble, DeepFlow, 프로덕션 요구사항, OpenTelemetry 연동 Use when working with observability 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# eBPF Observability 고급 가이드

Cilium Hubble, DeepFlow, 프로덕션 요구사항, OpenTelemetry 연동

## Cilium Hubble

### 개요

Hubble은 Cilium의 네트워크 가시성 레이어로, eBPF 기반 패킷 레벨 모니터링을 제공합니다.

### Hubble 활성화

```bash
# Cilium에서 Hubble 활성화
cilium hubble enable --ui

# 또는 Helm values
helm upgrade cilium cilium/cilium \
  --namespace kube-system \
  --set hubble.enabled=true \
  --set hubble.relay.enabled=true \
  --set hubble.ui.enabled=true \
  --set hubble.metrics.enabled="{dns,drop,tcp,flow,icmp,http}"
```

### Hubble Helm 설정

```yaml
# cilium-values.yaml
hubble:
  enabled: true

  relay:
    enabled: true
    replicas: 1

  ui:
    enabled: true
    replicas: 1
    ingress:
      enabled: true
      hosts:
        - hubble.example.com

  metrics:
    enabled:
      - dns:query
      - drop
      - tcp
      - flow
      - icmp
      - http
    serviceMonitor:
      enabled: true

  # L7 가시성 (HTTP, gRPC, Kafka)
  export:
    static:
      enabled: true
      filePath: /var/run/cilium/hubble/events.log

# L7 프록시 활성화 (필요 시)
envoy:
  enabled: true
```

### Hubble CLI 사용

```bash
# Flow 관찰
hubble observe --namespace production

# 특정 서비스 트래픽
hubble observe --to-service payment-service

# 드롭된 패킷 확인
hubble observe --verdict DROPPED

# HTTP 요청 필터
hubble observe --protocol http --http-status 500

# JSON 출력
hubble observe -o json | jq '.flow.source.labels'

# 실시간 Service Map
hubble observe --output=compact --follow
```

### Network Policy 디버깅

```bash
# 정책으로 드롭된 트래픽 확인
hubble observe --verdict DROPPED --type policy-verdict

# 특정 Pod 트래픽 추적
hubble observe --from-pod production/my-app-xyz

# DNS 쿼리 모니터링
hubble observe --protocol dns

# 출력 예시
TIMESTAMP             SOURCE                DESTINATION           TYPE    VERDICT   SUMMARY
Jan 15 10:30:15.123   production/app-a      production/app-b      L7/HTTP FORWARDED GET /api/users HTTP/1.1
Jan 15 10:30:15.456   production/app-b      external/0.0.0.0      L3/L4   DROPPED   Policy denied
```

---

## DeepFlow

### 개요

DeepFlow는 eBPF 기반 종합 Observability 플랫폼으로, 자동 분산 추적과 네트워크 성능 모니터링을 제공합니다.

### 설치

```bash
# Helm 설치
helm repo add deepflow https://deepflowio.github.io/deepflow
helm install deepflow deepflow/deepflow \
  --namespace deepflow \
  --create-namespace \
  --set global.image.repository=deepflowce
```

### 주요 기능

```yaml
# DeepFlow 기능 매트릭스
AutoTracing:
  - eBPF 기반 자동 Span 생성
  - 분산 트레이싱 (코드 변경 없음)
  - Cross-process 상관관계 자동 연결

AutoMetrics:
  - 서비스별 RED 메트릭 (Rate, Error, Duration)
  - 네트워크 레이턴시
  - TCP 재전송, RTT

AutoTagging:
  - Kubernetes 메타데이터 자동 태깅
  - Cloud 리소스 매핑 (AWS, GCP, Azure)

NetworkProfiling:
  - 패킷 레벨 분석
  - 네트워크 경로 추적
```

---

## CRITICAL: eBPF 요구사항

### 커널 버전

```bash
# 최소 커널 버전 확인
uname -r
# 권장: 5.8 이상 (BTF 지원)
# 최소: 4.15 (기본 eBPF)

# BTF 지원 확인
ls /sys/kernel/btf/vmlinux
```

### 노드 요구사항

| 요구사항 | 설명 |
|---------|------|
| **커널** | 5.8+ 권장 (BTF, CO-RE) |
| **CAP_BPF** | eBPF 프로그램 로드 |
| **CAP_SYS_PTRACE** | uprobe 활성화 |
| **CAP_NET_ADMIN** | XDP, TC 프로그램 |
| **/sys/kernel/debug** | tracing 접근 |

### SecurityContext 설정

```yaml
securityContext:
  # 옵션 1: privileged (개발/테스트)
  privileged: true

  # 옵션 2: capabilities (프로덕션 권장)
  capabilities:
    add:
      - BPF
      - SYS_PTRACE
      - NET_ADMIN
      - PERFMON
  runAsUser: 0
```

---

## OpenTelemetry 연동

### OTel Collector 설정

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 1s
    send_batch_size: 1024

  k8sattributes:
    extract:
      metadata:
        - k8s.namespace.name
        - k8s.pod.name
        - k8s.deployment.name
        - k8s.node.name

exporters:
  otlp/jaeger:
    endpoint: jaeger-collector:4317
    tls:
      insecure: true

  prometheus:
    endpoint: 0.0.0.0:8889
    namespace: ebpf

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch, k8sattributes]
      exporters: [otlp/jaeger]
    metrics:
      receivers: [otlp]
      processors: [batch, k8sattributes]
      exporters: [prometheus]
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 구버전 커널에서 실행 | 기능 제한/실패 | 커널 5.8+ 업그레이드 |
| privileged 없이 배포 | eBPF 로드 실패 | 적절한 capabilities |
| 모든 네임스페이스 활성화 | 오버헤드 증가 | 필요한 네임스페이스만 |
| 샘플링 미설정 | 과도한 데이터 | 10% 샘플링 시작 |
| Hubble L7 무분별 활성화 | CPU 사용량 급증 | 필요한 서비스만 |

---

## 체크리스트

### Hubble 설정
- [ ] Cilium 기반 확인
- [ ] 필요한 메트릭 활성화
- [ ] UI/Relay 배포

### OpenTelemetry
- [ ] OTel Collector 설정
- [ ] 트레이싱 백엔드 연동
- [ ] 샘플링 비율 설정

---

## 참조 스킬

- `ebpf-observability.md` - eBPF 기초, Grafana Beyla, Odigos 가이드
- `/observability-otel` - OpenTelemetry 통합 가이드
- `/monitoring-metrics` - 메트릭 수집/시각화
- `/cilium-networking` - Cilium 네트워킹

---

## Sources

- [Cilium Hubble](https://docs.cilium.io/en/stable/observability/hubble/)
- [DeepFlow](https://deepflow.io/docs/)
- [eBPF Introduction](https://ebpf.io/what-is-ebpf/)
