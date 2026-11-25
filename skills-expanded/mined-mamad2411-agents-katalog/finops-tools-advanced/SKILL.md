---
name: finops-tools-advanced
category: sre
description: "FinOps Tools 고급 최적화 가이드 — Cast AI 자동 최적화, Kubecost 고급 설정, 4Rs Framework, Right-sizing 자동화 Use when working with sre 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# FinOps Tools 고급 최적화 가이드

Cast AI 자동 최적화, Kubecost 고급 설정, 4Rs Framework, Right-sizing 자동화

## Infracost 정책 파일 (OPA)

```rego
# infracost-policy.rego
package infracost

# 월간 비용 증가 제한
deny[msg] {
  input.diffTotalMonthlyCost > 500
  msg := sprintf("PR increases monthly cost by $%.2f (limit: $500)", [input.diffTotalMonthlyCost])
}

# 대형 인스턴스 경고
warn[msg] {
  r := input.projects[_].breakdown.resources[_]
  r.resourceType == "aws_instance"
  contains(r.metadata.values.instance_type, "xlarge")
  msg := sprintf("Large instance detected: %s (%s)", [r.name, r.metadata.values.instance_type])
}

# 태그 없는 리소스
deny[msg] {
  r := input.projects[_].breakdown.resources[_]
  not r.metadata.values.tags
  msg := sprintf("Resource %s has no tags", [r.name])
}
```

---

## Kubernetes 특화 FinOps 도구 (2026)

### Cast AI 자동 최적화

Cast AI는 Kubernetes 비용을 자동으로 최적화하는 플랫폼입니다.

```yaml
# Cast AI 설치
# 1. 클러스터 연결
# Cast AI 콘솔에서 클러스터 등록 후 에이전트 설치

# 2. 에이전트 배포
helm repo add castai-helm https://castai.github.io/helm-charts
helm install castai-agent castai-helm/castai-agent \
  --namespace castai-agent \
  --create-namespace \
  --set apiKey=$CASTAI_API_KEY \
  --set clusterID=$CLUSTER_ID

# 3. 노드 관리 활성화 (선택적)
helm install castai-cluster-controller castai-helm/castai-cluster-controller \
  --namespace castai-agent \
  --set castai.apiKey=$CASTAI_API_KEY \
  --set castai.clusterID=$CLUSTER_ID
```

### Cast AI 주요 기능

```yaml
# Cast AI 기능 매트릭스
자동 최적화:
  - 인스턴스 선택 최적화 (Spot, RI, On-Demand 믹스)
  - Pod Right-sizing 권장
  - 노드 통합 (Consolidation)
  - 유휴 노드 자동 제거

가시성:
  - 실시간 비용 대시보드
  - 네임스페이스/워크로드별 비용 할당
  - 절감 가능 금액 분석

AI 기반:
  - 워크로드 패턴 학습
  - 예측적 스케일링
  - 이상 비용 감지
```

### Kubecost 고급 설정

```yaml
# kubecost-advanced-values.yaml
kubecostModel:
  # 정확한 비용 할당
  etlFileStoreEnabled: true

  # 다중 클러스터 연합 (Enterprise)
  federatedETL:
    enabled: true
    primaryCluster: true

  # 네트워크 비용 (Cloud Integration 필요)
  networkCosts:
    enabled: true
    prometheusPorts:
      - 9003

# 커스텀 가격 설정
customPricing:
  enabled: true
  configmapName: kubecost-pricing

# 알림 설정
notifications:
  alertConfigs:
    enabled: true
    frontendUrl: "https://kubecost.example.com"
    slackWebhookUrl: "https://hooks.slack.com/..."

    # 예산 알림
    alerts:
      - type: budget
        threshold: 1000
        window: 7d
        aggregation: namespace
        filter: 'namespace:"production"'
---
# 커스텀 가격 ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: kubecost-pricing
  namespace: kubecost
data:
  pricing.json: |
    {
      "provider": "aws",
      "description": "Custom AWS pricing",
      "CPU": "0.031",
      "RAM": "0.004",
      "GPU": "0.95",
      "storage": "0.040",
      "spotCPU": "0.010",
      "spotRAM": "0.001"
    }
```

### IBM FinOps Suite (Turbonomic)

```yaml
# Turbonomic Kubernetes 에이전트 설치
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: kubeturbo
  namespace: turbo
spec:
  selector:
    matchLabels:
      name: kubeturbo
  template:
    metadata:
      labels:
        name: kubeturbo
    spec:
      serviceAccountName: kubeturbo
      containers:
        - name: kubeturbo
          image: turbonomic/kubeturbo:8.10.0
          args:
            - --turboconfig=/etc/kubeturbo/turbo.config
            - --v=2
          volumeMounts:
            - name: turbo-config
              mountPath: /etc/kubeturbo
              readOnly: true
            - name: varlog
              mountPath: /var/log
      volumes:
        - name: turbo-config
          configMap:
            name: turbo-config
        - name: varlog
          emptyDir: {}
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: turbo-config
  namespace: turbo
data:
  turbo.config: |
    {
      "communicationConfig": {
        "serverMeta": {
          "turboServer": "https://turbonomic.example.com"
        },
        "restAPIConfig": {
          "opsManagerUserName": "kubeturbo",
          "opsManagerPassword": "..."
        }
      },
      "targetConfig": {
        "targetName": "production-eks"
      }
    }
```

### 4Rs 프레임워크 적용

```
4Rs FinOps Framework:
    |
    +-- Right-sizing
    |   +-- 리소스 요청/제한 최적화
    |   +-- Kubecost Savings 권장사항 적용
    |   +-- VPA 자동 조정
    |
    +-- Reserved
    |   +-- 예약 인스턴스 / Savings Plans
    |   +-- 안정적 워크로드 식별
    |   +-- RI 커버리지 분석
    |
    +-- Reduce
    |   +-- 유휴 리소스 제거
    |   +-- 개발 환경 야간 축소
    |   +-- 오래된 스냅샷/이미지 정리
    |
    +-- Replatform
        +-- Spot 인스턴스 활용
        +-- ARM 인스턴스 전환
        +-- Serverless 고려 (KEDA)
```

### Right-sizing 자동화

```yaml
# VPA + Kubecost 연동
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: my-app-vpa
  namespace: production
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  updatePolicy:
    updateMode: "Auto"  # 자동 적용
  resourcePolicy:
    containerPolicies:
      - containerName: "*"
        minAllowed:
          cpu: 50m
          memory: 64Mi
        maxAllowed:
          cpu: 2
          memory: 4Gi
        controlledResources: ["cpu", "memory"]
---
# Goldilocks (VPA 권장사항 시각화)
# 설치
helm repo add fairwinds-stable https://charts.fairwinds.com/stable
helm install goldilocks fairwinds-stable/goldilocks \
  --namespace goldilocks \
  --create-namespace

# 네임스페이스 활성화
kubectl label namespace production goldilocks.fairwinds.com/enabled=true
```

### 비용 할당 태깅 표준

```yaml
# 비용 할당을 위한 표준 라벨
metadata:
  labels:
    # 필수 라벨
    cost-center: "engineering"      # 비용 센터
    team: "platform"                # 팀
    environment: "production"       # 환경
    application: "my-app"           # 애플리케이션

    # 선택 라벨
    project: "project-alpha"        # 프로젝트
    owner: "john@example.com"       # 담당자
    budget-code: "ENG-2024-001"     # 예산 코드
---
# OPA/Kyverno로 라벨 강제
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-cost-labels
spec:
  validationFailureAction: Enforce
  rules:
    - name: check-cost-labels
      match:
        any:
          - resources:
              kinds:
                - Deployment
                - StatefulSet
      validate:
        message: "cost-center, team, environment 라벨이 필요합니다"
        pattern:
          metadata:
            labels:
              cost-center: "?*"
              team: "?*"
              environment: "production|staging|development"
```

---

## Kubernetes FinOps 체크리스트

### 가시성
- [ ] Kubecost/OpenCost 설치
- [ ] 클라우드 가격 통합
- [ ] 비용 할당 라벨 표준화
- [ ] 대시보드 구축

### 최적화
- [ ] Right-sizing 분석 (VPA/Goldilocks)
- [ ] Spot 인스턴스 활용 (Karpenter)
- [ ] 유휴 리소스 식별
- [ ] 예약 인스턴스 분석

### 자동화
- [ ] Cast AI 또는 자동 최적화 도구
- [ ] 비용 알림 설정
- [ ] 예산 정책 적용
- [ ] 정기 리뷰 프로세스

## Sources

- [Cast AI](https://cast.ai/)
- [Kubecost Documentation](https://docs.kubecost.com/)
- [FinOps Tools 2026](https://platformengineering.org/blog/10-finops-tools-platform-engineers-should-evaluate-for-2026)
- [IBM Turbonomic](https://www.ibm.com/products/turbonomic)

## 참조 스킬

- `/finops-tools` - FinOps 기본 도구 (OpenCost, Kubecost, Infracost, KEDA+Karpenter)
- `/finops` - FinOps 기초
- `/finops-greenops` - GreenOps & 지속가능성
