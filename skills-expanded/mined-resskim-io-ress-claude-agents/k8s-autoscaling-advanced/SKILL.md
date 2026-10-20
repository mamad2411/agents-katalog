---
name: k8s-autoscaling-advanced
category: kubernetes
description: "Kubernetes Autoscaling 고급 가이드 — Karpenter, 조합 전략, 모니터링 Use when working with kubernetes 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Kubernetes Autoscaling 고급 가이드

Karpenter, 조합 전략, 모니터링

## Karpenter (Node Autoscaler)

### 설치 (EKS)

```bash
helm repo add karpenter https://charts.karpenter.sh
helm install karpenter karpenter/karpenter \
  --namespace karpenter --create-namespace \
  --set serviceAccount.annotations."eks\.amazonaws\.com/role-arn"=$KARPENTER_ROLE_ARN \
  --set settings.clusterName=$CLUSTER_NAME \
  --set settings.interruptionQueue=$KARPENTER_QUEUE
```

### NodePool 설정

```yaml
apiVersion: karpenter.sh/v1
kind: NodePool
metadata:
  name: default
spec:
  template:
    spec:
      requirements:
        # 인스턴스 유형
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["spot", "on-demand"]
        - key: kubernetes.io/arch
          operator: In
          values: ["amd64"]
        - key: karpenter.k8s.aws/instance-category
          operator: In
          values: ["c", "m", "r"]
        - key: karpenter.k8s.aws/instance-size
          operator: In
          values: ["medium", "large", "xlarge"]
      nodeClassRef:
        group: karpenter.k8s.aws
        kind: EC2NodeClass
        name: default
  limits:
    cpu: 1000
    memory: 1000Gi
  disruption:
    consolidationPolicy: WhenEmptyOrUnderutilized
    consolidateAfter: 1m
---
apiVersion: karpenter.k8s.aws/v1
kind: EC2NodeClass
metadata:
  name: default
spec:
  amiFamily: AL2
  subnetSelectorTerms:
    - tags:
        karpenter.sh/discovery: "my-cluster"
  securityGroupSelectorTerms:
    - tags:
        karpenter.sh/discovery: "my-cluster"
  role: KarpenterNodeRole-my-cluster
```

### Karpenter vs Cluster Autoscaler

| 항목 | Karpenter | Cluster Autoscaler |
|------|-----------|-------------------|
| 프로비저닝 속도 | 30-60초 | 수 분 |
| 인스턴스 선택 | 자동 최적화 | 노드 그룹 기반 |
| Spot 통합 | 네이티브 | 별도 설정 |
| 비용 최적화 | 자동 consolidation | 수동 |
| 지원 클라우드 | AWS | AWS, GCP, Azure |

---

## 조합 전략

### 권장 조합

```
┌─────────────────────────────────────────────────────────┐
│             Production Autoscaling Stack                 │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Stateless API ──> HPA (CPU 70%)                        │
│       +                                                  │
│  Event Consumer ──> KEDA (Kafka lag)                    │
│       +                                                  │
│  Right-sizing ──> VPA (Off mode, 추천만)                │
│       +                                                  │
│  Node 관리 ──> Karpenter (Spot 70% + On-Demand 30%)     │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 워크로드별 권장

| 워크로드 | 권장 조합 |
|----------|----------|
| API 서버 | HPA (CPU) + Karpenter |
| Kafka Consumer | KEDA (lag) + Karpenter |
| Batch Job | KEDA ScaledJob + Spot |
| ML 추론 | HPA (custom metric) + GPU Node |
| 크론 작업 | KEDA (cron trigger) |

---

## 모니터링

### Prometheus 메트릭

```promql
# HPA 현재 레플리카
kube_horizontalpodautoscaler_status_current_replicas

# HPA 목표 레플리카
kube_horizontalpodautoscaler_status_desired_replicas

# KEDA 스케일링 이벤트
keda_scaler_metrics_value

# Karpenter 노드 프로비저닝
karpenter_nodes_created_total
karpenter_nodes_terminated_total
```

### Grafana 대시보드

```json
{
  "panels": [
    {
      "title": "HPA Status",
      "targets": [{
        "expr": "kube_horizontalpodautoscaler_status_current_replicas{namespace=\"$namespace\"}",
        "legendFormat": "{{horizontalpodautoscaler}}"
      }]
    },
    {
      "title": "KEDA Scaler Value",
      "targets": [{
        "expr": "keda_scaler_metrics_value{namespace=\"$namespace\"}",
        "legendFormat": "{{scaledObject}}"
      }]
    }
  ]
}
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 메모리로 HPA | 느린 반응, OOM | CPU 또는 Custom Metric |
| requests 미설정 | HPA 계산 불가 | 항상 requests 설정 |
| HPA + VPA Auto | 충돌 | VPA Off 모드 사용 |
| maxReplicas > 파티션 | 유휴 Pod | 파티션 수 이하로 |
| 짧은 cooldown | 플래핑 | 적절한 대기 시간 |
| Spot만 사용 | 중단 위험 | On-Demand 혼합 |
| Karpenter limits 미설정 | 비용 폭증 | CPU/메모리 제한 |

---

## 체크리스트

### Karpenter
- [ ] Spot + On-Demand 혼합
- [ ] consolidation 정책 설정
- [ ] NodePool limits 설정
- [ ] EC2NodeClass 설정
- [ ] Disruption budgets 설정

### 조합 전략
- [ ] 워크로드 유형별 Autoscaler 선택
- [ ] HPA + VPA 충돌 방지 (VPA Off 모드)
- [ ] KEDA + Karpenter 연동 확인
- [ ] Scale-to-Zero 대상 식별

### 모니터링
- [ ] Prometheus 메트릭 수집 설정
- [ ] Grafana 대시보드 구성
- [ ] 알림 규칙 설정
- [ ] 스케일링 이벤트 로깅

---

## Sources

- [Karpenter Documentation](https://karpenter.sh/docs/)
- [KEDA Documentation](https://keda.sh/docs/)
- [Kubernetes Autoscaling Best Practices](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)

---

## 참조 스킬

- `/k8s-autoscaling` - Autoscaling 기본 가이드 (HPA, VPA, KEDA)
- `/aws-eks` - EKS 클러스터 설정
- `/kafka` - Kafka 기반 스케일링
- `/finops` - 비용 최적화
- `/monitoring-metrics` - 모니터링 메트릭
