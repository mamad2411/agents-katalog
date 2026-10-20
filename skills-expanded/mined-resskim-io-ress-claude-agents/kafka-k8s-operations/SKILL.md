---
name: kafka-k8s-operations
category: messaging
description: "Kafka on Kubernetes 운영 가이드 — Strimzi+ArgoCD 통합, kind→EKS(MSK)/GKE 전환, JMX 모니터링, Schema Registry K8s 배포 Use when working with messaging 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Kafka on Kubernetes 운영 가이드

Strimzi+ArgoCD 통합, kind→EKS(MSK)/GKE 전환, JMX 모니터링, Schema Registry K8s 배포

## Quick Reference (결정 트리)

```
Kafka on K8s?
    │
    ├─ Operator 선택 ────> Strimzi (표준)
    │
    ├─ 배포 방식 ────────> ArgoCD Application
    │     │
    │     └─ Sync Wave: CRD(-2) → Operator(-1) → Cluster(0)
    │
    ├─ 환경 전환 ────────> Phase별 전략
    │     │
    │     ├─ kind ─────────> Strimzi (경량)
    │     ├─ EKS ──────────> Strimzi 또는 MSK
    │     └─ GKE ──────────> Strimzi 또는 Pub/Sub
    │
    └─ 모니터링 ─────────> JMX → Prometheus → Grafana
```

---

## Strimzi + ArgoCD 통합

### Sync Wave 순서

```yaml
# 1. Strimzi Operator CRD 설치 (sync-wave: -2)
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: strimzi-operator
  annotations:
    argocd.argoproj.io/sync-wave: "-2"
spec:
  source:
    repoURL: https://strimzi.io/charts/
    chart: strimzi-kafka-operator
    targetRevision: "0.44.0"
    helm:
      values: |
        watchNamespaces:
          - kafka
        resources:
          requests:
            cpu: 100m
            memory: 256Mi
  destination:
    server: https://kubernetes.default.svc
    namespace: kafka
  syncPolicy:
    syncOptions:
      - CreateNamespace=true
      - ServerSideApply=true

---
# 2. Kafka Cluster (sync-wave: 0)
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: kafka-cluster
  annotations:
    argocd.argoproj.io/sync-wave: "0"
spec:
  source:
    repoURL: https://github.com/my-org/k8s-config.git
    path: kafka/overlays/{{ .Values.environment }}
  destination:
    server: https://kubernetes.default.svc
    namespace: kafka
```

### Kafka Cluster CRD (환경별 overlay)

```yaml
# kafka/base/kafka-cluster.yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: my-cluster
  namespace: kafka
spec:
  kafka:
    version: "3.8.0"
    replicas: 3                              # 환경별 override
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
      - name: tls
        port: 9093
        type: internal
        tls: true
    config:
      offsets.topic.replication.factor: 3     # 환경별 override
      transaction.state.log.replication.factor: 3
      transaction.state.log.min.isr: 2
      default.replication.factor: 3
      min.insync.replicas: 2
      inter.broker.protocol.version: "3.8"
    storage:
      type: jbod
      volumes:
        - id: 0
          type: persistent-claim
          size: 100Gi                         # 환경별 override
          class: gp3                          # 환경별 override
          deleteClaim: false
    # JMX 메트릭 노출
    metricsConfig:
      type: jmxPrometheusExporter
      valueFrom:
        configMapKeyRef:
          name: kafka-jmx-config
          key: kafka-metrics-config.yml
    resources:                                # 환경별 override
      requests:
        cpu: 500m
        memory: 2Gi
      limits:
        cpu: "2"
        memory: 4Gi
  zookeeper:
    replicas: 3
    storage:
      type: persistent-claim
      size: 10Gi
      class: gp3
  entityOperator:
    topicOperator: {}
    userOperator: {}
```

### 환경별 Override (Kustomize)

```yaml
# kafka/overlays/dev/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - ../../base
patches:
  - patch: |
      apiVersion: kafka.strimzi.io/v1beta2
      kind: Kafka
      metadata:
        name: my-cluster
      spec:
        kafka:
          replicas: 1
          config:
            offsets.topic.replication.factor: 1
            transaction.state.log.replication.factor: 1
            min.insync.replicas: 1
          storage:
            volumes:
              - id: 0
                type: persistent-claim
                size: 5Gi
                class: standard
          resources:
            requests:
              cpu: 100m
              memory: 512Mi
            limits:
              cpu: 500m
              memory: 1Gi
        zookeeper:
          replicas: 1
          storage:
            type: persistent-claim
            size: 2Gi
            class: standard
```

---

## kind → EKS(MSK) / GKE 전환 전략

### Phase별 Kafka 전략

```
Phase 1 (kind):
  Strimzi Kafka 1 broker, 1 ZK
  Storage: standard (로컬)
  replication.factor: 1
  목적: 개발/테스트, 패턴 검증

Phase 2 (EKS staging):
  옵션 A: Strimzi Kafka 3 brokers (자체 관리)
  옵션 B: Amazon MSK (관리형)
  Storage: gp3 100Gi
  replication.factor: 3

Phase 3 (EKS/GKE prod):
  옵션 A: Strimzi + dedicated node pool (대규모)
  옵션 B: MSK Serverless (AWS) / Pub/Sub (GCP)
  → 앱 코드 변경 없이 KAFKA_BROKERS 환경변수만 교체
```

### Strimzi → MSK 전환 시 변경 사항

| 항목 | Strimzi (kind/EKS) | MSK | 변경 필요 |
|------|-------------------|-----|----------|
| Broker 주소 | `my-cluster-kafka-bootstrap:9092` | `b-1.msk.xxx:9092` | 환경변수만 |
| 인증 | PLAIN / mTLS | IAM / SASL | 클라이언트 설정 |
| Schema Registry | K8s 배포 | Glue Schema Registry | 엔드포인트 변경 |
| 토픽 관리 | KafkaTopic CRD | MSK 콘솔 or CLI | 관리 방식 |
| 모니터링 | JMX → Prometheus | CloudWatch / Open Monitoring | 대시보드 |
| 비용 | EC2 노드 비용 | MSK 브로커 시간당 | 보통 MSK가 비쌈 |

### Strimzi → Pub/Sub 전환 (GKE)

```
GCP에서는 Pub/Sub이 관리형 메시징.
Kafka와 API가 다르므로 앱 코드 수정 필요.
→ 대안: Confluent Cloud (Kafka 호환 관리형)
→ 또는 Strimzi on GKE (직접 관리, 코드 변경 없음)
```

---

## JMX → Prometheus 모니터링

### JMX Exporter ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: kafka-jmx-config
  namespace: kafka
data:
  kafka-metrics-config.yml: |
    lowercaseOutputName: true
    lowercaseOutputLabelNames: true
    rules:
      # Broker 메트릭
      - pattern: kafka.server<type=(.+), name=(.+), clientId=(.+), topic=(.+), partition=(.*)><>Value
        name: kafka_server_$1_$2
        type: GAUGE
        labels:
          clientId: "$3"
          topic: "$4"
          partition: "$5"
      # Request 메트릭
      - pattern: kafka.server<type=(.+), name=(.+)><>(\w+)
        name: kafka_server_$1_$2_$3
        type: GAUGE
      # Controller 메트릭
      - pattern: kafka.controller<type=(.+), name=(.+)><>Value
        name: kafka_controller_$1_$2
        type: GAUGE
      # Log 메트릭
      - pattern: kafka.log<type=(.+), name=(.+), topic=(.+), partition=(.+)><>Value
        name: kafka_log_$1_$2
        type: GAUGE
        labels:
          topic: "$3"
          partition: "$4"
```

### ServiceMonitor (Kafka 전용)

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: kafka-metrics
  namespace: kafka
  labels:
    monitoring: "true"
spec:
  selector:
    matchLabels:
      strimzi.io/kind: Kafka
  namespaceSelector:
    matchNames: [kafka]
  endpoints:
    - port: tcp-prometheus
      interval: 30s
      path: /metrics
```

### 핵심 Grafana 대시보드 패널

```
Broker Health:
  - kafka_server_replicamanager_underreplicatedpartitions (0이어야 정상)
  - kafka_controller_kafkacontroller_activecontrollercount (1이어야 정상)
  - kafka_server_replicamanager_offlinereplicacount (0이어야 정상)

Throughput:
  - rate(kafka_server_brokertopicmetrics_messagesin_total[5m])
  - rate(kafka_server_brokertopicmetrics_bytesin_total[5m])

Consumer Lag:
  - kafka_consumergroup_lag (kafka-exporter에서 수집)

Disk Usage:
  - kafka_log_log_size (파티션별 로그 크기)
```

---

## Schema Registry K8s 배포

### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: schema-registry
  namespace: kafka
spec:
  replicas: 2
  selector:
    matchLabels:
      app: schema-registry
  template:
    metadata:
      labels:
        app: schema-registry
    spec:
      containers:
        - name: schema-registry
          image: confluentinc/cp-schema-registry:7.7.1
          ports:
            - containerPort: 8081
          env:
            - name: SCHEMA_REGISTRY_HOST_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS
              value: "my-cluster-kafka-bootstrap:9092"
            - name: SCHEMA_REGISTRY_LISTENERS
              value: "http://0.0.0.0:8081"
            - name: SCHEMA_REGISTRY_SCHEMA_COMPATIBILITY_LEVEL
              value: "BACKWARD"
          resources:
            requests:
              cpu: 100m
              memory: 256Mi
            limits:
              cpu: 500m
              memory: 512Mi
          readinessProbe:
            httpGet:
              path: /subjects
              port: 8081
            initialDelaySeconds: 10
          livenessProbe:
            httpGet:
              path: /subjects
              port: 8081
            initialDelaySeconds: 30
---
apiVersion: v1
kind: Service
metadata:
  name: schema-registry
  namespace: kafka
spec:
  selector:
    app: schema-registry
  ports:
    - port: 8081
      targetPort: 8081
```

### KRaft 모드 (ZooKeeper 제거)

```yaml
# Strimzi 0.40+ 에서 KRaft 지원
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaNodePool
metadata:
  name: controller
  labels:
    strimzi.io/cluster: my-cluster
spec:
  replicas: 3
  roles:
    - controller
  storage:
    type: jbod
    volumes:
      - id: 0
        type: persistent-claim
        size: 10Gi
---
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaNodePool
metadata:
  name: broker
  labels:
    strimzi.io/cluster: my-cluster
spec:
  replicas: 3
  roles:
    - broker
  storage:
    type: jbod
    volumes:
      - id: 0
        type: persistent-claim
        size: 100Gi
---
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: my-cluster
  annotations:
    strimzi.io/kraft: enabled
    strimzi.io/node-pools: enabled
spec:
  kafka:
    version: "3.8.0"
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
  # zookeeper 섹션 제거!
  entityOperator:
    topicOperator: {}
```
