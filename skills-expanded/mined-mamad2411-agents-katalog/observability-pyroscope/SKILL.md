---
name: observability-pyroscope
category: observability
description: "Continuous Profiling with Pyroscope — Pyroscope 기반 Continuous Profiling: eBPF/SDK/Java Agent 통합, Span Profiles, FlameQL 가이드 Use when working with observability 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Continuous Profiling with Pyroscope

Pyroscope 기반 Continuous Profiling: eBPF/SDK/Java Agent 통합, Span Profiles, FlameQL 가이드

## Quick Reference (언어별 프로파일링 결정 트리)

```
프로파일링 대상 언어?
    |
    +-- Go ──────────> pyroscope.ebpf (코드 변경 없음) 또는 Go SDK (세밀한 제어)
    +-- Java ────────> pyroscope.java (async-profiler, JVMTI) 또는 -javaagent (JFR)
    +-- Python ──────> pyroscope.ebpf (권장) 또는 SDK (py-spy, wall-clock 권장)
    +-- Node.js ─────> pyroscope.ebpf (권장) 또는 SDK (perf_hooks)
    +-- Rust/C++ ────> pyroscope.ebpf (유일한 선택지)
    +-- 멀티 언어 ───> pyroscope.ebpf DaemonSet (전체 노드 커버)
```

---

## CRITICAL: Pyroscope 아키텍처

### 전체 데이터 흐름

```
┌──────────────────────────────────────────────────────┐
│                  Kubernetes Cluster                    │
│                                                       │
│  ┌──────────┐   ┌──────────┐   ┌──────────────────┐ │
│  │ App Pod  │   │ App Pod  │   │ App Pod          │ │
│  │ (Go SDK) │   │ (No SDK) │   │ (-javaagent)     │ │
│  └────┬─────┘   └────┬─────┘   └────┬─────────────┘ │
│       │              │              │                 │
│       ▼              ▼              ▼                 │
│  ┌────────────────────────────────────────────────┐  │
│  │           Grafana Alloy (DaemonSet)             │  │
│  │  pyroscope.ebpf ── 커널 레벨 프로파일링        │  │
│  │  pyroscope.java ── async-profiler JVMTI        │  │
│  │  pyroscope.write ─ Pyroscope 서버로 전송       │  │
│  └───────────────────────┬────────────────────────┘  │
│                          ▼                            │
│  ┌────────────────────────────────────────────────┐  │
│  │       Pyroscope Server (Microservices)          │  │
│  │  Ingester → Store → Compactor → Querier        │  │
│  │             ↕ MinIO / S3 (Block Storage)        │  │
│  └───────────────────────┬────────────────────────┘  │
└──────────────────────────┼───────────────────────────┘
                           ▼
                 ┌──────────────────┐
                 │  Grafana UI      │
                 │  Flame Graph     │
                 │  Tempo 연동      │
                 └──────────────────┘
```

### 핵심 컴포넌트

| 컴포넌트 | 역할 | 비고 |
|----------|------|------|
| **Ingester** | 프로파일 데이터 수집, 인메모리 버퍼링 | 쓰기 경로 |
| **Store** | 블록 스토리지(S3/MinIO)에 영구 저장 | Parquet 포맷 |
| **Compactor** | 블록 병합, 보존 정책 적용 | 백그라운드 |
| **Querier** | FlameQL 쿼리 처리, Grafana에 결과 반환 | 읽기 경로 |
| **Alloy** | 프로파일 수집 에이전트 (eBPF/JVMTI) | DaemonSet |

---

## Helm Installation (v1.18+)

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install pyroscope grafana/pyroscope \
  -n monitoring --create-namespace -f pyroscope-values.yaml
```

### values.yaml (Microservices 모드)

```yaml
pyroscope:
  structuredConfig:
    storage:
      backend: s3
      s3:
        endpoint: minio.monitoring.svc:9000
        bucket_name: pyroscope-data
        access_key_id: ${MINIO_ACCESS_KEY}
        secret_access_key: ${MINIO_SECRET_KEY}
        insecure: true
    compactor:
      compaction_interval: 30m
      retention_period: 720h  # 30일
    multitenancy_enabled: false

  components:
    ingester:
      replicas: 2
      resources:
        requests: { cpu: 500m, memory: 1Gi }
        limits: { memory: 2Gi }
    querier:
      replicas: 2
      resources:
        requests: { cpu: 250m, memory: 512Mi }
    compactor:
      replicas: 1
      persistence: { enabled: true, size: 20Gi }

minio:
  enabled: true    # 개발/테스트용 내장 MinIO
  persistence: { size: 50Gi }
```

### 규모별 리소스 가이드

| 규모 | 일일 프로파일 | Ingester | Querier | 스토리지 |
|------|-------------|----------|---------|---------|
| **Small** (5-10 서비스) | ~5GB | 1 x 1Gi | 1 x 512Mi | 50Gi |
| **Medium** (20-50 서비스) | ~20GB | 2 x 2Gi | 2 x 1Gi | 200Gi |
| **Large** (100+ 서비스) | ~100GB | 3 x 4Gi | 3 x 2Gi | S3 무제한 |

---

## Alloy Integration (권장)

eBPF + Java + Write를 하나의 Alloy 설정으로 통합 배포한다.

```alloy
// === 1. 서비스 디스커버리 ===
discovery.kubernetes "pods" {
  role = "pod"
}

discovery.relabel "profiling_targets" {
  targets = discovery.kubernetes.pods.targets

  rule {
    source_labels = ["__meta_kubernetes_namespace"]
    regex         = "default|production|staging"
    action        = "keep"
  }
  // CRITICAL: tag에 점(.) 사용 불가 → 언더스코어(_)로 변환
  rule {
    source_labels = ["__meta_kubernetes_namespace"]
    target_label  = "namespace"
  }
  rule {
    source_labels = ["__meta_kubernetes_pod_name"]
    target_label  = "pod"
  }
  // service_name 매핑 (service.name이 아님!)
  rule {
    source_labels = ["__meta_kubernetes_pod_label_app"]
    target_label  = "service_name"
  }
}

// === 2. pyroscope.ebpf — 커널 레벨 CPU 프로파일링 (모든 언어) ===
// DaemonSet 배포, 코드 변경 없음
pyroscope.ebpf "cluster" {
  forward_to          = [pyroscope.write.backend.receiver]
  targets             = discovery.relabel.profiling_targets.output
  targets_only        = true          // K8s Pod만 대상
  default_sample_rate = 97            // Hz, 소수로 aliasing 방지
  demangle            = "none"        // Go 바이너리는 "none" 권장
}

// === 3. pyroscope.java — async-profiler 기반 (JVMTI) ===
pyroscope.java "jvm" {
  forward_to = [pyroscope.write.backend.receiver]
  targets    = discovery.relabel.profiling_targets.output
  profiling_config {
    interval = "15s"
    cpu      = true
    alloc    = "512k"     // 할당 프로파일링 임계값
    lock     = "10ms"     // lock 경합 프로파일링 임계값
  }
}

// === 4. pyroscope.write — Pyroscope 서버 전송 ===
pyroscope.write "backend" {
  endpoint {
    url = "http://pyroscope.monitoring.svc:4040"
    // 멀티테넌시: headers = { "X-Scope-OrgID" = "team-backend" }
  }
  external_labels = {
    cluster = "production",
    env     = "prod",
  }
}
```

### pyroscope.ebpf 핵심 포인트

- DaemonSet으로 배포하여 노드의 모든 컨테이너 자동 프로파일링
- 커널 레벨 동작, 언어 무관, 코드 변경 불필요
- `targets_only = true`로 K8s Pod만 대상 (호스트 프로세스 제외)

### pyroscope.java 핵심 포인트

- async-profiler를 JVMTI로 JVM에 attach
- CPU, 메모리 할당(alloc), lock 경합(lock) 프로파일링 지원
- Pod annotation 기반 선택적 활성화 가능

---

## SDK Integration

### Go SDK

```go
import (
    "github.com/grafana/pyroscope-go"
    otelpyroscope "github.com/grafana/otel-profiling-go"
)

func main() {
    pyroscope.Start(pyroscope.Config{
        ApplicationName: "order-service",
        ServerAddress:   "http://pyroscope.monitoring.svc:4040",
        ProfileTypes: []pyroscope.ProfileType{
            pyroscope.ProfileCPU,
            pyroscope.ProfileAllocObjects,  pyroscope.ProfileAllocSpace,
            pyroscope.ProfileInuseObjects,  pyroscope.ProfileInuseSpace,
            pyroscope.ProfileGoroutines,
            pyroscope.ProfileMutexCount,    pyroscope.ProfileMutexDuration,
            pyroscope.ProfileBlockCount,    pyroscope.ProfileBlockDuration,
        },
        // CRITICAL: 정적 태그만 사용, 점(.) 금지
        Tags: map[string]string{
            "env": "production", "version": "1.2.0", "region": "ap-northeast-2",
        },
    })

    // OTel TracerProvider에 Pyroscope 래퍼 적용 (Span Profiles)
    tp := otelpyroscope.NewTracerProvider(
        sdktrace.NewTracerProvider(sdktrace.WithBatcher(exporter)),
    )
    otel.SetTracerProvider(tp)
}
```

### Java Agent

```bash
java -javaagent:pyroscope.jar \
  -Dpyroscope.application.name=payment-service \
  -Dpyroscope.server.address=http://pyroscope.monitoring.svc:4040 \
  -Dpyroscope.format=jfr \
  -Dpyroscope.labels="env=production,version=2.0.0" \
  -Dpyroscope.upload.interval=15s \
  -Dpyroscope.alloc.enabled=true -Dpyroscope.lock.enabled=true \
  -jar app.jar
```

```yaml
# K8s Deployment 환경변수 방식
env:
  - name: JAVA_TOOL_OPTIONS
    value: "-javaagent:/pyroscope/pyroscope.jar"
  - name: PYROSCOPE_APPLICATION_NAME
    value: "payment-service"
  - name: PYROSCOPE_SERVER_ADDRESS
    value: "http://pyroscope.monitoring.svc:4040"
  - name: PYROSCOPE_FORMAT
    value: "jfr"
  - name: PYROSCOPE_LABELS
    value: "env=production,version=2.0.0"
```

> OTel Java Agent와 병행 시 `-javaagent` 순서 주의: OTel Agent 먼저, Pyroscope 뒤에 배치.

---

## Span Profiles (Trace - Profile 연동)

Span Profiles는 분산 추적의 각 span에 `profile_id`를 연결하여
Grafana Tempo에서 특정 span의 flame graph로 즉시 drill-down할 수 있게 한다.

```
동작: TracerProvider Pyroscope 래퍼 → span에 profile_id 주입
      → Tempo가 인식 → Grafana UI에서 trace → span → flame graph
```

### Grafana Datasource 설정 (tracesToProfiles)

```yaml
apiVersion: 1
datasources:
  - name: Tempo
    type: tempo
    uid: tempo
    jsonData:
      tracesToProfiles:
        datasourceUid: pyroscope
        tags:
          - key: service.name
            value: service_name    # CRITICAL: Pyroscope는 점(.) 불가
          - key: k8s.pod.name
            value: pod
        profileTypeId: "process_cpu:cpu:nanoseconds:cpu:nanoseconds"
        customQuery: true
        query: '{service_name="$${__span.tags.service_name}"}'
```

---

## OTLP Ingestion (v1.16+)

Pyroscope v1.16부터 OTLP 프로토콜로 직접 프로파일 수신 가능.

```yaml
# pyroscope structuredConfig
otlp:
  enabled: true
  grpc:
    endpoint: "0.0.0.0:4318"
```

```alloy
// Alloy에서 OTLP로 전송
otelcol.exporter.otlp "pyroscope" {
  client {
    endpoint = "pyroscope.monitoring.svc:4318"
    tls { insecure = true }
  }
}
```

---

## Profiles Drilldown UI

```
Grafana → Explore → Pyroscope datasource 선택
    → 서비스 선택 (service_name 드롭다운)
    → 프로파일 타입: process_cpu | memory | goroutines | mutex
    → 시간 범위 지정 → Flame Graph / Table / Both 뷰 전환
```

**Flame Graph 읽기**: 가로 폭 = 전체 대비 비율(넓을수록 병목), 세로 = 호출 스택 깊이,
Self = 함수 자체 비용, Total = 하위 호출 포함 비용.

---

## FlameQL Queries

```
# 기본 문법
{label_name="value"}                   # 레이블 매칭
{label_name=~"regex"}                  # 정규식 매칭

# CPU 핫스팟
process_cpu:cpu:nanoseconds:cpu:nanoseconds{service_name="order-service", env="production"}

# 메모리 할당 — 버전 비교
memory:alloc_space:bytes:alloc_space:bytes{service_name="order-service", version="1.2.0"}
memory:alloc_space:bytes:alloc_space:bytes{service_name="order-service", version="1.3.0"}

# Java lock 경합
mutex:contentions:count:delay:nanoseconds{service_name="payment-service"}

# Go 고루틴 누수 감지
goroutines:goroutine:count:goroutine:count{service_name="gateway", env="production"}
```

---

## Production Operations

### 보존 및 압축

```yaml
compactor:
  compaction_interval: 30m
  retention_period: 720h     # 30일
  block_ranges: [2h, 12h, 24h]
```

### 스토리지 용량 산정

| 서비스 수 | 프로파일 간격 | 일일 데이터 | 30일 보존 |
|-----------|-------------|-----------|----------|
| 10 | 15초 | ~3-5 GB | ~100-150 GB |
| 50 | 15초 | ~15-25 GB | ~500-750 GB |
| 100 | 30초 | ~20-40 GB | ~700-1200 GB |

### 성능 영향

| 방식 | CPU 오버헤드 | 메모리 | 비고 |
|------|------------|--------|------|
| **pyroscope.ebpf** | **<1%** | ~50MB/Node | 프로덕션 안전, 권장 |
| **pyroscope.java** | **2-5%** | ~100MB/Pod | alloc 시 증가 |
| **Go SDK** | **1-3%** | ~30MB/Pod | runtime/pprof |
| **Python SDK** | **3-7%** | ~50MB/Pod | wall-clock 권장 |

### 운영 모니터링

```promql
rate(pyroscope_ingester_ingested_profiles_total[5m])        # Ingester 수집률
pyroscope_bucket_store_block_loads_total                     # 블록 로드 수
histogram_quantile(0.99,
  rate(pyroscope_querier_query_duration_seconds_bucket[5m])) # 쿼리 p99
```

---

## CRITICAL: Anti-Patterns

### 1. Tag에 점(.) 사용 금지

Pyroscope는 tag key/value에 점(`.`)을 허용하지 않는다.
OTel `service.name` → Pyroscope `service_name`으로 변환 필수.

```
# 금지                              # 올바른 사용
service.name = "order-service"      service_name = "order-service"
k8s.namespace.name = "production"   namespace = "production"
```

> Alloy `discovery.relabel`의 `target_label`을 언더스코어로 지정하면 자동 변환.

### 2. Unbounded Label 금지

카디널리티가 높은 label은 성능을 급격히 저하시킨다.

```
# 금지 — 카디널리티 폭발           # 허용 — 제한된 카디널리티
user_id = "12345"                   env = "production"
request_id = "abc-def-ghi"          version = "1.2.0"
trace_id = "0af7651916cd43dd"       region = "ap-northeast-2"
```

### 3. OTel Java Agent + Spring Boot Starter 동시 사용 금지

이중 계측 발생. **하나만 선택**: OTel Java Agent 또는 Spring Boot OTel Starter.

### 4. eBPF와 SDK 동시 사용 시 중복 주의

같은 프로세스를 이중 프로파일링하면 데이터 중복.
eBPF를 기본, 세밀한 제어 필요 시에만 SDK로 전환.

### 5. 프로파일링 간격 과소 설정 금지

```
# 금지: interval = "1s"
# 권장: interval = "15s" (일반) 또는 "30s" (대규모)
```

---

## Checklist

### 초기 설정
- [ ] Pyroscope Helm chart v1.18+ 설치 (microservices 모드)
- [ ] MinIO 또는 S3 스토리지 구성 완료
- [ ] Grafana datasource에 Pyroscope 추가 (UID: `pyroscope` 고정)
- [ ] Alloy DaemonSet에 pyroscope.ebpf 설정 추가

### 프로파일링 설정
- [ ] 모든 tag key에 점(`.`) 대신 언더스코어(`_`) 사용
- [ ] unbounded label(user_id, request_id) 태깅 안 함
- [ ] Java 서비스에 pyroscope.java 또는 -javaagent 설정
- [ ] 프로파일링 간격 15초 이상으로 설정

### Trace 연동
- [ ] OTel TracerProvider에 Pyroscope 래퍼 적용 (Span Profiles)
- [ ] Tempo datasource에 tracesToProfiles 설정 완료
- [ ] tag 매핑에서 `service.name` → `service_name` 변환 확인

### 운영
- [ ] 보존 정책 설정 (기본 30일 권장)
- [ ] 프로파일링 오버헤드 확인 (eBPF <1%, Java 2-5%)
- [ ] Ingester/Querier 메트릭 모니터링 대시보드 구성
- [ ] 스토리지 용량 알림 설정

### 검증
- [ ] Grafana Explore에서 flame graph 조회 가능
- [ ] Tempo trace에서 Pyroscope drill-down 동작 확인
- [ ] FlameQL 쿼리로 특정 서비스 프로파일 검색 가능
- [ ] 배포 전후 프로파일 비교(diff) 가능
