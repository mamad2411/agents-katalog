---
name: k8s-gpu-scheduling
category: platform
description: "Kubernetes GPU 스케줄링 & 모니터링 — Kueue 큐 관리, Volcano Gang 스케줄링, GPU 모니터링 Use when working with platform 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Kubernetes GPU 스케줄링 & 모니터링

Kueue 큐 관리, Volcano Gang 스케줄링, GPU 모니터링

## Quick Reference

```
스케줄링 도구 선택?
    │
    ├─ 큐/쿼터 관리 ──────> Kueue
    │       │
    │       └─ 팀별 GPU 할당, 우선순위
    │
    ├─ Gang 스케줄링 ─────> Volcano
    │       │
    │       └─ 분산 학습 (모든 Pod 동시 시작)
    │
    └─ 모니터링 ──────────> DCGM Exporter
            │
            └─ GPU 사용률, 온도, 메모리
```

---

## Kueue (큐 관리)

### 설치

```bash
kubectl apply --server-side -f \
  https://github.com/kubernetes-sigs/kueue/releases/download/v0.6.0/manifests.yaml
```

### ClusterQueue 설정

```yaml
# GPU 리소스 풀 정의
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: a100-40gb
spec:
  nodeLabels:
    nvidia.com/gpu.product: "NVIDIA-A100-SXM4-40GB"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: t4
spec:
  nodeLabels:
    nvidia.com/gpu.product: "Tesla-T4"
---
# ClusterQueue
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: ml-cluster-queue
spec:
  namespaceSelector: {}
  queueingStrategy: StrictFIFO
  resourceGroups:
    - coveredResources: ["cpu", "memory", "nvidia.com/gpu"]
      flavors:
        - name: a100-40gb
          resources:
            - name: "nvidia.com/gpu"
              nominalQuota: 16
              borrowingLimit: 4
            - name: "cpu"
              nominalQuota: 128
            - name: "memory"
              nominalQuota: 512Gi
        - name: t4
          resources:
            - name: "nvidia.com/gpu"
              nominalQuota: 32
  preemption:
    reclaimWithinCohort: Any
    withinClusterQueue: LowerPriority
---
# LocalQueue (팀별)
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  name: ml-team-queue
  namespace: ml-training
spec:
  clusterQueue: ml-cluster-queue
```

### Kueue Job 제출

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: training-job
  namespace: ml-training
  labels:
    kueue.x-k8s.io/queue-name: ml-team-queue
spec:
  parallelism: 4
  completions: 4
  suspend: true  # Kueue가 관리
  template:
    spec:
      containers:
        - name: trainer
          image: pytorch-training:latest
          resources:
            requests:
              nvidia.com/gpu: 1
              cpu: 8
              memory: 32Gi
            limits:
              nvidia.com/gpu: 1
      restartPolicy: Never
```

---

## Volcano (Gang Scheduling)

### 설치

```bash
helm repo add volcano-sh https://volcano-sh.github.io/helm-charts
helm install volcano volcano-sh/volcano \
  --namespace volcano-system \
  --create-namespace
```

### 분산 학습 Job (PyTorch DDP)

```yaml
apiVersion: batch.volcano.sh/v1alpha1
kind: Job
metadata:
  name: pytorch-ddp-training
spec:
  minAvailable: 4      # Gang: 4개 모두 시작해야 함
  schedulerName: volcano
  plugins:
    svc: ["--publish-not-ready-addresses"]
    ssh: []
    env: []
  policies:
    - event: PodEvicted
      action: RestartJob
  queue: default
  tasks:
    - replicas: 4
      name: worker
      template:
        spec:
          containers:
            - name: pytorch
              image: pytorch-ddp:latest
              command:
                - torchrun
                - --nnodes=4
                - --nproc_per_node=1
                - --rdzv_backend=c10d
                - --rdzv_endpoint=$(VC_WORKER_0_SVC):29500
                - train.py
              ports:
                - containerPort: 29500
                  name: rdzv
              resources:
                limits:
                  nvidia.com/gpu: 1
              env:
                - name: NCCL_DEBUG
                  value: INFO
          restartPolicy: OnFailure
```

### MPI Job (Horovod)

```yaml
apiVersion: batch.volcano.sh/v1alpha1
kind: Job
metadata:
  name: horovod-training
spec:
  minAvailable: 5  # 1 master + 4 workers
  schedulerName: volcano
  plugins:
    ssh: []
    svc: []
  tasks:
    - replicas: 1
      name: master
      policies:
        - event: TaskCompleted
          action: CompleteJob
      template:
        spec:
          containers:
            - name: horovod
              image: horovod-training:latest
              command:
                - horovodrun
                - -np
                - "4"
                - -H
                - $(VC_WORKER_HOSTS)
                - python
                - train.py
    - replicas: 4
      name: worker
      template:
        spec:
          containers:
            - name: horovod
              image: horovod-training:latest
              resources:
                limits:
                  nvidia.com/gpu: 1
```

---

## GPU 모니터링

### DCGM Exporter 메트릭

```promql
# GPU 사용률 (%)
DCGM_FI_DEV_GPU_UTIL

# GPU 메모리 사용량
DCGM_FI_DEV_FB_USED / DCGM_FI_DEV_FB_TOTAL * 100

# GPU 온도
DCGM_FI_DEV_GPU_TEMP

# 전력 소비
DCGM_FI_DEV_POWER_USAGE

# Tensor Core 활용률
DCGM_FI_PROF_PIPE_TENSOR_ACTIVE

# SM (Streaming Multiprocessor) 활용률
DCGM_FI_PROF_SM_ACTIVE
```

### Grafana 대시보드 패널

```json
{
  "panels": [
    {
      "title": "GPU Utilization by Node",
      "targets": [{
        "expr": "DCGM_FI_DEV_GPU_UTIL{gpu=~\"$gpu\"}",
        "legendFormat": "{{kubernetes_node}} - GPU {{gpu}}"
      }]
    },
    {
      "title": "GPU Memory Usage",
      "targets": [{
        "expr": "DCGM_FI_DEV_FB_USED{gpu=~\"$gpu\"} / DCGM_FI_DEV_FB_TOTAL * 100",
        "legendFormat": "{{kubernetes_node}} - GPU {{gpu}}"
      }]
    },
    {
      "title": "Cluster GPU Allocation",
      "targets": [{
        "expr": "sum(kube_pod_container_resource_limits{resource=\"nvidia_com_gpu\"}) / sum(kube_node_status_allocatable{resource=\"nvidia_com_gpu\"}) * 100"
      }]
    }
  ]
}
```

### 알림 규칙

```yaml
groups:
  - name: gpu-alerts
    rules:
      - alert: GPUHighTemperature
        expr: DCGM_FI_DEV_GPU_TEMP > 85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "GPU temperature > 85°C"

      - alert: GPUMemoryExhausted
        expr: DCGM_FI_DEV_FB_USED / DCGM_FI_DEV_FB_TOTAL > 0.95
        for: 5m
        labels:
          severity: critical

      - alert: GPUUnderutilized
        expr: DCGM_FI_DEV_GPU_UTIL < 20
        for: 30m
        labels:
          severity: info
        annotations:
          summary: "GPU underutilized - consider right-sizing"
```

---

## 체크리스트

### Kueue
- [ ] ClusterQueue 정의
- [ ] LocalQueue (팀별) 생성
- [ ] ResourceFlavor (GPU 유형별)
- [ ] 우선순위 클래스 정의

### Volcano
- [ ] Volcano 설치
- [ ] Queue 정의
- [ ] Gang scheduling Job 작성
- [ ] Plugin 설정 (ssh, svc)

### 모니터링
- [ ] DCGM Exporter 활성화
- [ ] Grafana 대시보드 구성
- [ ] 알림 규칙 설정
- [ ] 사용률 리포트 자동화

**관련 agent**: `mlops-expert`
**관련 skill**: `/k8s-gpu` (기본, GPU Operator, 공유 전략), `/ml-serving`, `/k8s-autoscaling`

---

## Sources

- [NVIDIA GPU Operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/)
- [Kueue Documentation](https://kueue.sigs.k8s.io/)
- [Volcano Documentation](https://volcano.sh/docs/)
- [DCGM Exporter](https://github.com/NVIDIA/dcgm-exporter)
