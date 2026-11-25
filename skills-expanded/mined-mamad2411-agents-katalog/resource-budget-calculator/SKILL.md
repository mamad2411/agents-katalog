---
name: resource-budget-calculator
category: platform
description: 메모리/CPU/connection pool/disk budget을 per-instance와 cluster 합계로 계산하는 공식과 체크리스트. HikariCP formula, K8s requests/limits, DB max_connections 산정. Vlad Mihalcea + HikariCP wiki 기반.
---

# Resource Budget Calculator (M9: 메모리/리소스 budget 계산 부재)

라이브러리 default 또는 "넉넉히 잡자" 식 할당이 누적되면 **per-instance 는 풍족** 하지만 **cluster 합계는 한계 초과**. DB / Cache / Mimir 등이 OOM 또는 connection 고갈.

> Claude mental model 오류: "메모리 / connection 은 넉넉히 잡으면 안전" → 30 replica × 100 connection = 3000 connection 이 PG `max_connections=100` 을 초과. 또는 Mimir 512Mi limit 가 OTel 1.7M series 를 못 받음.

---

## 4 영역 budget 공식

### 1. DB Connection Pool

**HikariCP 공식** (Brett Wooldridge):

```
connections = ((core_count * 2) + effective_spindle_count)

core_count: DB instance 의 CPU 코어 수
effective_spindle_count: HDD 수 (SSD = 0 또는 1)
```

예시:
- PG 4 core + SSD: `(4 * 2) + 1 = 9 connection` (per DB instance 전체)
- 100 connection 은 거의 항상 **잘못된** 직관

**Per-instance 할당**:
```
per_pod_pool_size = total_db_connections / pod_replica_count

예: DB max_connections = 100, pod replica = 30
   → per_pod_pool_size = 100 / 30 ≈ 3
   → HikariCP maximumPoolSize: 3
```

**예약 budget**:
- DB 자체 (postgres, superuser): 10
- 모니터링 (postgres_exporter): 1-2
- 다른 application: 합산
- 여유분: 10-20%

```
application_total_quota = (max_connections - 예약 - 여유) × 0.8
```

---

### 2. JVM Heap

```
container_memory_limit = heap_max + non_heap + native + system

heap_max:        -Xmx (Spring Boot 기본 메모리 사용)
non_heap:        Metaspace + CodeCache + DirectByteBuffer (~256-512Mi)
native:          JVM 자체 + thread stack (~256Mi)
system:          OS / sidecar (~128Mi)
```

권장:
- container limit 4Gi → `-Xmx2Gi -Xms2Gi` (절반 정도 heap)
- 또는 JVM container support: `-XX:MaxRAMPercentage=70` (heap 비율)

함정:
- `-Xmx4Gi` + container limit 4Gi → off-heap + thread stack 초과로 **OOMKilled** (heap 안에서 GC 만 일어남, OS 가 죽임)
- thread per request 모델 (Tomcat 200 thread × 1Mi stack) = 200Mi 추가 native

---

### 3. K8s requests / limits

```yaml
resources:
  requests:
    memory: "512Mi"   # scheduler 가 노드 배치 기준
    cpu: "250m"       # scheduler 기준 + 최소 보장
  limits:
    memory: "2Gi"     # 초과 시 OOMKilled
    cpu: "2000m"      # 초과 시 throttling
```

원칙:
- **requests = p50** 실제 사용량
- **limits = p99 + 50% buffer**
- requests:limits 비율이 **너무 크면** 노드 over-commit + eviction 위험
- limits 없으면 **노드 전체 영향** (cgroup 보호 부재)

CPU throttling 진단:
```promql
rate(container_cpu_cfs_throttled_periods_total[5m])
  / rate(container_cpu_cfs_periods_total[5m])
```

> 0.1 이면 throttling 발생 → limit 상향 또는 HPA 조정.

---

### 4. Prometheus / Mimir series cardinality

```
total_series = Σ (metric × label_combination)

per metric:
  http_requests_total{method, status, endpoint, env}
    = 7 method × 3 status × 50 endpoint × 3 env
    = 3150 series

Mimir distributor 메모리:
  ~ active_series × 10KB
  1M series ≈ 10GB
```

Limits (Mimir runtime overrides):
```yaml
overrides:
  user-1:
    ingestion_rate: 100000          # samples/s
    ingestion_burst_size: 1000000
    max_global_series_per_user: 1500000
    max_global_series_per_metric: 100000
```

함정:
- request 1 record 가 15MB 초과 → distributor reject (Alloy WAL flush 시 발생)
- → Alloy 측 `max_samples_per_send` 조정 (작게)

---

## 사례: Goti 1.7M series / 512Mi Mimir

```
시작 상태: Mimir distributor memory limit 512Mi
누적 series: 1.7M (label cardinality 폭발)
결과: distributor OOMKilled cycle
```

분석:
```
1.7M series × ~10KB = 17GB metadata
→ 512Mi 로 절대 불가능
→ memory limit 4Gi 로 올리거나, cardinality 줄이거나
```

**근본 해결**: cardinality 축소 (user_id 라벨 제거, env 그루핑 등)

---

## ❌ Budget 미계산 안티패턴 6종

### 1. HikariCP default (10) 그대로

→ replica 증가 시 DB connection 폭증.

### 2. PG max_connections default (100) 그대로

→ 30 replica × 10 = 300 → connection refused.

### 3. `-Xmx` 미설정

→ JVM 이 container memory 일부만 인식 (구버전) 또는 100% 잡음 (overcommit).

### 4. K8s limits 미설정

→ 단일 pod 가 노드 전체 메모리 점유 → kubelet eviction → cascade.

### 5. HPA target metric 없음

→ replica 가 부하 못 따라가거나 over-scale.

### 6. Prometheus 보존 기간 미산정

```
storage = sample_rate × series × retention × byte_per_sample
       = 1/15s × 1.7M × 30d × ~2 byte
       ≈ 587GB
```

→ PVC 100GB 잡았다가 retention 7일로 강제 단축.

---

## 자가 검증 체크리스트

신규 서비스 / replica 변경 / DB instance 변경 시:

- [ ] **HikariCP per-pod pool size** = (DB max / replica) 보다 작거나 같은가?
- [ ] **DB max_connections** + 예약(monitoring/superuser) + 20% 여유?
- [ ] **JVM `-Xmx`** 이 container limit 의 **50-70%** 인가?
- [ ] K8s **requests = p50** 실측, **limits = p99 × 1.5**?
- [ ] CPU **throttling rate < 10%** ?
- [ ] HPA target metric / threshold 명시?
- [ ] Prometheus / Mimir **series budget** 산정 (cardinality 폭발 차단)?
- [ ] PVC retention 산정 (sample_rate × series × retention)?

---

## 외부 근거

- [About Pool Sizing — HikariCP Wiki](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing) — 공식 산출 식
- [The best way to determine the optimal connection pool size — Vlad Mihalcea](https://vladmihalcea.com/optimal-connection-pool-size/)
- [Recommended connection pool size and Kubernetes — Prisma](https://github.com/prisma/prisma/discussions/17026) — per_instance = total / replicas
- [PostgreSQL Tuning — max_connections](https://www.postgresql.org/docs/current/runtime-config-connection.html)
- [JVM memory in containers — Eclipse Adoptium](https://adoptium.net/news/2021/01/jvm-container-awareness/)
- [Kubernetes resource management](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)

---

## 의외의 발견

- **"1 connection per CPU core"** 가 통념 (100+ connection) 을 깬다 — `(cores × 2) + spindles` 가 실증 최적
- **per-pod 가 아닌 cluster 합계** 가 항상 bottleneck (DB 측에서 본 connection 수)
- JVM container support 가 켜져 있어도 **off-heap + native + thread stack** 합산이 limit 의 30% 이상

---

## 연계 skill

- [`platform/dev-prod-parity-checklist.md`](../dev-prod-parity-checklist/SKILL.md) — replica scaling 환경 차이
- [`testing/negative-path-coverage.md`](../negative-path-coverage/SKILL.md) — pool 고갈 / OOM 시나리오 테스트
- [`observability/observability-from-day-zero.md`](../observability-from-day-zero/SKILL.md) — cardinality 폭발 방지
