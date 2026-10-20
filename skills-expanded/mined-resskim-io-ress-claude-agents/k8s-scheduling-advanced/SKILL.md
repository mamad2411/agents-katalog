---
name: k8s-scheduling-advanced
category: kubernetes
description: "Kubernetes Scheduling 고급 가이드 — 실전 시나리오, Topology Spread, 디버깅 Use when working with kubernetes 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Kubernetes Scheduling 고급 가이드

실전 시나리오, Topology Spread, 디버깅

## 실전 시나리오

### 1. 프로덕션 워크로드 격리

```yaml
# 프로덕션 노드 Taint
# kubectl taint nodes prod-node-* environment=production:NoSchedule

apiVersion: apps/v1
kind: Deployment
metadata:
  name: production-app
spec:
  template:
    spec:
      tolerations:
        - key: "environment"
          operator: "Equal"
          value: "production"
          effect: "NoSchedule"
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: environment
                    operator: In
                    values:
                      - production
      containers:
        - name: app
          image: app:latest
```

### 2. 멀티 AZ 고가용성

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ha-app
spec:
  replicas: 6
  template:
    spec:
      affinity:
        # 다른 노드에 분산
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchLabels:
                  app: ha-app
              topologyKey: kubernetes.io/hostname

        # AZ 균등 분산
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app: ha-app
                topologyKey: topology.kubernetes.io/zone
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: ScheduleAnyway
          labelSelector:
            matchLabels:
              app: ha-app
```

### 3. 데이터 지역성 (캐시 + 앱)

```yaml
# Redis 배포
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
spec:
  template:
    metadata:
      labels:
        app: redis
        tier: cache
    spec:
      containers:
        - name: redis
          image: redis:7
---
# 앱: Redis와 같은 노드 선호
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  template:
    spec:
      affinity:
        podAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    tier: cache
                topologyKey: kubernetes.io/hostname
      containers:
        - name: web
          image: web:latest
```

---

## Topology Spread Constraints

### 균등 분산

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: spread-app
spec:
  replicas: 6
  template:
    spec:
      topologySpreadConstraints:
        # AZ 간 균등 분산
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: DoNotSchedule
          labelSelector:
            matchLabels:
              app: spread-app

        # 노드 간 균등 분산
        - maxSkew: 1
          topologyKey: kubernetes.io/hostname
          whenUnsatisfiable: ScheduleAnyway
          labelSelector:
            matchLabels:
              app: spread-app
      containers:
        - name: app
          image: app:latest
```

| 파라미터 | 설명 |
|----------|------|
| **maxSkew** | 최대 불균형 허용치 (1 = 완벽 균등) |
| **whenUnsatisfiable** | DoNotSchedule / ScheduleAnyway |

---

## 디버깅

### 스케줄링 실패 원인 확인

```bash
# Pod 이벤트 확인
kubectl describe pod <pod-name>

# 일반적인 실패 메시지
# - 0/5 nodes are available: 3 node(s) had taint {key=value:NoSchedule}
# - 0/5 nodes are available: 2 node(s) didn't match Pod's node affinity
# - 0/5 nodes are available: 1 Insufficient cpu, 2 Insufficient memory
```

### 노드 상태 확인

```bash
# 노드 라벨 확인
kubectl get nodes --show-labels

# 노드 Taint 확인
kubectl describe nodes | grep -A3 Taints

# 노드 리소스 확인
kubectl describe node <node-name> | grep -A5 "Allocated resources"
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| required만 사용 | 스케줄링 불가 상황 | preferred 혼용 |
| Anti-Affinity + 적은 노드 | 레플리카 부족 | 노드 수 확보 또는 preferred |
| Toleration만 설정 | 다른 노드에도 배치됨 | Node Affinity 함께 사용 |
| topologyKey 오타 | 무시됨 | 표준 키 사용 |
| 과도한 Taint | 스케줄링 복잡 | 필요한 것만 |
| maxSkew 너무 엄격 | Pending Pod 발생 | ScheduleAnyway 사용 |
| Topology Spread 없이 HA | AZ 편중 | topologySpreadConstraints 추가 |

---

## 체크리스트

### 실전 시나리오
- [ ] 프로덕션/스테이징 워크로드 격리
- [ ] GPU 노드 전용화 (Taint + Affinity)
- [ ] 데이터 지역성 구성 (캐시 + 앱)

### Topology Spread
- [ ] maxSkew 적절히 설정
- [ ] 여러 topology 레벨 고려 (zone + hostname)
- [ ] whenUnsatisfiable 전략 선택

### 디버깅
- [ ] kubectl describe pod으로 이벤트 확인
- [ ] 노드 라벨/Taint 정기 점검
- [ ] 리소스 여유 확인
- [ ] Pending Pod 알림 설정

**관련 skill**: `/k8s-autoscaling`, `/k8s-security`, `/k8s-helm`

---

## 참조 스킬

- `k8s-scheduling.md` - 스케줄링 기초, Node Affinity, Taint/Toleration, Pod Affinity
- `/k8s-autoscaling` - 오토스케일링
- `/k8s-security` - 보안 정책
- `/k8s-helm` - Helm 차트 관리
