---
name: observability-mimir-monolithic
category: observability
description: "Mimir 싱글바이너리 (Monolithic) 모드 가이드 — 분산 모드 대비 경량, 중소 규모 배포를 위한 Mimir 모놀리식 설정 Use when working with observability 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Mimir 싱글바이너리 (Monolithic) 모드 가이드

분산 모드 대비 경량, 중소 규모 배포를 위한 Mimir 모놀리식 설정

## Quick Reference (모드 선택)

```
Mimir 배포 모드?
    │
    ├─ 활성 시리즈 < 1M ─────────> 싱글바이너리 (monolithic)
    │   리소스: 2-4 CPU, 8-16GB
    │   Pod: 1개
    │
    ├─ 활성 시리즈 1M-10M ────────> SimpleScalable
    │   컴포넌트: read/write/backend 3그룹
    │
    └─ 활성 시리즈 > 10M ─────────> Microservices (분산)
        컴포넌트: 7+ 개별 스케일링
```

---

## 싱글바이너리 아키텍처

```
OTel Collector
    │
    │  OTLP HTTP (/otlp/v1/metrics)
    │  또는 Remote Write (/api/v1/push)
    ▼
┌──────────────────────────────────────┐
│  Mimir (싱글바이너리)                  │
│                                        │
│  ┌─────────┐  ┌──────────┐  ┌───────┐│
│  │Distributor│→│Ingester  │→│Compactor││
│  └─────────┘  └──────────┘  └───────┘│
│  ┌─────────┐  ┌──────────┐  ┌───────┐│
│  │Querier  │  │Query     │  │Ruler  ││
│  │         │  │Frontend  │  │       ││
│  └─────────┘  └──────────┘  └───────┘│
│        ↕            ↕           ↕      │
│  ┌─────────────────────────────────┐  │
│  │        Store Gateway            │  │
│  └─────────────────────────────────┘  │
│                  ↕                     │
│         S3 / Filesystem               │
└──────────────────────────────────────┘
```

모든 컴포넌트가 **단일 프로세스**에서 실행. 외부 Kafka 불필요 (자체 WAL로 버퍼링).

---

## Helm Values (dev, Kind 환경)

```yaml
# mimir-monolithic-dev-values.yaml
deploymentMode: SingleBinary  # monolithic 모드 활성화

mimir:
  structuredConfig:
    common:
      storage:
        backend: filesystem   # dev: 로컬 디스크, prod: s3

    # OTLP 네이티브 수집 활성화
    distributor:
      otlp_config:
        convert_all_attributes: true

    # 수집 제한
    limits:
      ingestion_rate: 50000              # samples/sec
      ingestion_burst_size: 100000
      max_global_series_per_user: 500000
      max_label_names_per_series: 30

    # 블록 스토리지
    blocks_storage:
      storage_prefix: blocks
      tsdb:
        dir: /data/tsdb
        retention_period: 24h     # TSDB 보존 (S3 이전 전)

    # Ruler (recording/alerting rules)
    ruler:
      enable_api: true
      rule_path: /data/ruler

    # Alertmanager
    alertmanager:
      enable_api: true
      data_dir: /data/alertmanager

singleBinary:
  replicas: 1
  resources:
    requests:
      cpu: "1"
      memory: "4Gi"
    limits:
      cpu: "2"
      memory: "8Gi"
  persistentVolume:
    enabled: true
    size: 30Gi

# Mimir 전용 Kafka/Minio 비활성화 (불필요)
minio:
  enabled: false
kafka:
  enabled: false

# Nginx gateway
nginx:
  enabled: true     # 단일 진입점 제공
  replicas: 1

# 메트릭 수집 (self-monitoring)
metaMonitoring:
  serviceMonitor:
    enabled: true
    labels:
      release: kube-prometheus-stack
```

---

## Helm Values (prod, EKS 환경)

```yaml
# mimir-monolithic-prod-values.yaml
deploymentMode: SingleBinary

mimir:
  structuredConfig:
    common:
      storage:
        backend: s3
        s3:
          endpoint: s3.ap-northeast-2.amazonaws.com
          bucket_name: goti-prod-mimir-blocks
          region: ap-northeast-2

    distributor:
      otlp_config:
        convert_all_attributes: true

    limits:
      ingestion_rate: 200000
      ingestion_burst_size: 400000
      max_global_series_per_user: 1500000
      max_label_names_per_series: 30

    blocks_storage:
      storage_prefix: blocks
      tsdb:
        dir: /data/tsdb
        retention_period: 48h

    ruler:
      enable_api: true
      storage:
        backend: s3
        s3:
          bucket_name: goti-prod-mimir-ruler

    alertmanager:
      enable_api: true
      storage:
        backend: s3
        s3:
          bucket_name: goti-prod-mimir-alertmanager

singleBinary:
  replicas: 1
  resources:
    requests:
      cpu: "2"
      memory: "8Gi"
    limits:
      cpu: "4"
      memory: "16Gi"
  persistentVolume:
    enabled: true
    size: 50Gi
    storageClass: gp3
  # IRSA (AWS IAM Role for Service Account)
  serviceAccount:
    annotations:
      eks.amazonaws.com/role-arn: arn:aws:iam::role/mimir-s3-access

minio:
  enabled: false
kafka:
  enabled: false

nginx:
  enabled: true
  replicas: 2

metaMonitoring:
  serviceMonitor:
    enabled: true
    labels:
      release: kube-prometheus-stack
```

---

## OTel Collector → Mimir 연동

### 방법 1: OTLP Native (권장)

Mimir가 OTLP 엔드포인트를 네이티브로 지원. OTel Collector에서 직접 전송.

```yaml
# OTel Collector config
exporters:
  otlphttp/mimir:
    endpoint: http://mimir-nginx.monitoring.svc:80/otlp
    tls:
      insecure: true

service:
  pipelines:
    metrics:
      receivers: [otlp]
      processors: [memory_limiter, attributes, batch]
      exporters: [otlphttp/mimir]
```

### 방법 2: Prometheus Remote Write

기존 Prometheus 호환 방식. Exemplar 지원.

```yaml
# OTel Collector config
exporters:
  prometheusremotewrite/mimir:
    endpoint: http://mimir-nginx.monitoring.svc:80/api/v1/push
    tls:
      insecure: true
    resource_to_telemetry_conversion:
      enabled: true        # OTel resource attributes → Prometheus labels

service:
  pipelines:
    metrics:
      receivers: [otlp]
      processors: [memory_limiter, attributes, batch]
      exporters: [prometheusremotewrite/mimir]
```

### 비교

| 항목 | OTLP Native | Remote Write |
|------|-------------|--------------|
| 성숙도 | 최신 (Mimir 2.10+) | 검증됨 |
| Exemplar | 지원 | 지원 |
| Native Histogram | 지원 | 지원 |
| OTel metadata 보존 | 높음 | 변환 과정에서 일부 손실 |
| 설정 복잡도 | 낮음 | 보통 |

**권장**: OTLP native. OTel 표준 파이프라인과 일관성 유지.

---

## 분산 → 싱글바이너리 전환 시 주의

### 제거되는 Pod (8→1)

| 분산 모드 Pod | 싱글바이너리 | 상태 |
|---|---|---|
| distributor | 내장 | ✅ |
| ingester | 내장 | ✅ |
| querier | 내장 | ✅ |
| query-frontend | 내장 | ✅ |
| store-gateway | 내장 | ✅ |
| compactor | 내장 | ✅ |
| ruler | 내장 | ✅ |
| kafka (ingest storage) | **제거** | 자체 WAL |
| minio (dev S3) | **제거** (filesystem) | 로컬 PV |

### 데이터 마이그레이션

분산 모드의 S3 블록은 싱글바이너리에서 그대로 읽을 수 있다 (동일 포맷).
filesystem 모드로 전환 시 기존 S3 데이터는 접근 불가 — 보존 기간 만료까지 S3 유지 필요.

---

## 스케일링 한계

### 싱글바이너리 한계 신호

| 지표 | 경고 수준 | 조치 |
|------|----------|------|
| 활성 시리즈 | > 800K | SimpleScalable 전환 검토 |
| 수집 속도 | > 100K samples/s 지속 | 리소스 증설 또는 모드 전환 |
| 쿼리 지연 | p99 > 10s | querier 분리 검토 |
| 메모리 사용 | > 12GB 지속 | 모드 전환 |

### 스파이크 트래픽 대응 (Goti 시나리오)

30만 동시 접속 스파이크 시:
- **메트릭은 Kafka 불필요** — Mimir 자체 WAL + ingestion rate limiting으로 버퍼링
- `ingestion_burst_size`를 `ingestion_rate`의 2배로 설정
- 스파이크 이후 안정화되면 ingester가 자체적으로 처리
- 극단적 스파이크 시 `otelcol_exporter_send_failed_metric_points` 모니터링

---

## Recording Rules 관리

### 방법 1: mimirtool (권장)

```bash
# rules 파일 업로드
mimirtool rules load rules.yaml \
  --address=http://mimir-nginx:80 \
  --id=anonymous

# rules 확인
mimirtool rules list --address=http://mimir-nginx:80
```

### 방법 2: PrometheusRule CRD + Mimir Ruler Sync

Alloy의 `mimir.rules.kubernetes` 대신 mimirtool CLI 또는 별도 sidecar로 sync.

```yaml
# CronJob으로 rules sync
apiVersion: batch/v1
kind: CronJob
metadata:
  name: mimir-rules-sync
spec:
  schedule: "*/5 * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: sync
              image: grafana/mimirtool:latest
              command:
                - mimirtool
                - rules
                - sync
                - --address=http://mimir-nginx:80
                - --rule-dirs=/rules
              volumeMounts:
                - name: rules
                  mountPath: /rules
          volumes:
            - name: rules
              configMap:
                name: mimir-recording-rules
```

---

## Anti-Patterns

| 안티패턴 | 결과 | 올바른 접근 |
|---------|------|-----------|
| 소규모에서 분산 모드 사용 | Pod 9개 낭비, 운영 복잡성 | 싱글바이너리로 시작 |
| filesystem 스토리지를 prod에서 사용 | 데이터 유실 위험, HA 불가 | S3 사용 |
| ingestion_rate를 너무 낮게 설정 | 스파이크 시 데이터 드롭 | burst_size를 rate의 2배로 |
| Kafka를 메트릭 버퍼로 사용 | 불필요한 복잡성 | Mimir WAL이 자체 버퍼링 |
| 싱글바이너리에서 replica > 1 | 데이터 중복, 충돌 | replica=1 고정 (HA 필요 시 모드 전환) |

---

## 체크리스트

### 설치
- [ ] Helm chart 설치 (`deploymentMode: SingleBinary`)
- [ ] PersistentVolume 크기 적정 (dev: 30Gi, prod: 50Gi+)
- [ ] 리소스 할당 (dev: 1CPU/4Gi, prod: 2CPU/8Gi)
- [ ] Storage backend 설정 (dev: filesystem, prod: S3+IRSA)

### 연동
- [ ] OTel Collector에서 OTLP 또는 Remote Write로 전송 확인
- [ ] Grafana datasource 연결 (endpoint: mimir-nginx:80)
- [ ] Recording rules 로드 확인
- [ ] ServiceMonitor로 self-monitoring 활성화

### 마이그레이션 (분산→싱글)
- [ ] 기존 분산 모드 Helm release 제거
- [ ] Kafka (Mimir 전용) 제거
- [ ] Minio (dev) 제거
- [ ] 싱글바이너리 Helm release 설치
- [ ] Grafana datasource endpoint 업데이트

---

## 참조 스킬

- `/observability-otel` — OTel Collector 기본 설정
- `/observability-otel-collector-helm` — Helm chart 환경별 패턴
- `/observability-alloy-to-otel` — Alloy → OTel 마이그레이션
- `/monitoring-prometheus-operator` — PrometheusRule CRD
