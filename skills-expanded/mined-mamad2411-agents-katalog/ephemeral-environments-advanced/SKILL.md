---
name: ephemeral-environments-advanced
category: cicd
description: "Ephemeral Environments 고급 가이드 — Qovery 설정, 데이터베이스 전략, Spot 인스턴스 비용 최적화 Use when working with cicd 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Ephemeral Environments 고급 가이드

Qovery 설정, 데이터베이스 전략, Spot 인스턴스 비용 최적화

---

## Qovery 설정

### 프로젝트 설정

```yaml
# .qovery.yml
application:
  name: myapp
  project: my-project
  publicly_accessible: true

  # Preview 환경 설정
  preview_environments:
    enabled: true
    auto_deploy: true
    auto_delete: true  # PR 종료 시 자동 삭제

    # 리소스 제한
    resources:
      cpu: 500m
      memory: 512Mi

    # 도메인
    custom_domains:
      - domain: "pr-{{ branch_name }}.preview.example.com"

  # 데이터베이스 복제
  databases:
    - name: postgres
      type: postgresql
      mode: CONTAINER  # Preview는 컨테이너 DB
      clone_from: production  # 프로덕션에서 스키마 복제

  # 환경 변수
  environment_variables:
    - key: ENVIRONMENT
      value: preview
    - key: DATABASE_URL
      value: "{{ database.postgres.internal_url }}"
```

### CLI 사용

```bash
# Qovery CLI 설치
brew install qovery

# 프로젝트 초기화
qovery init

# Preview 환경 목록
qovery preview list

# 특정 PR 환경 확인
qovery preview status --pr 123

# 수동 삭제
qovery preview delete --pr 123
```

---

## 데이터베이스 전략

### 옵션 비교

| 옵션 | 장점 | 단점 | 적합 |
|------|------|------|------|
| **빈 DB** | 빠름, 독립적 | 테스트 데이터 없음 | 단위 테스트 |
| **스키마 복제** | 구조 동일 | 데이터 없음 | 통합 테스트 |
| **시드 데이터** | 일관된 테스트 | 관리 필요 | E2E 테스트 |
| **스냅샷 복제** | 실제와 유사 | 느림, 비용 | QA 테스트 |

### 시드 데이터 자동화

```yaml
# k8s/overlays/preview/seed-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: db-seed
  annotations:
    argocd.argoproj.io/hook: PostSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
spec:
  template:
    spec:
      containers:
        - name: seed
          image: myapp:latest
          command: ["./seed.sh"]
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: db-credentials
                  key: url
      restartPolicy: Never
  backoffLimit: 3
```

---

## 비용 최적화

### Spot/Preemptible 인스턴스

```yaml
# Karpenter NodePool for Preview
apiVersion: karpenter.sh/v1
kind: NodePool
metadata:
  name: preview-spot
spec:
  template:
    spec:
      requirements:
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["spot"]
        - key: kubernetes.io/arch
          operator: In
          values: ["amd64", "arm64"]
      nodeClassRef:
        name: preview
      taints:
        - key: preview
          value: "true"
          effect: NoSchedule
  limits:
    cpu: 100
    memory: 200Gi
  disruption:
    consolidationPolicy: WhenEmpty
    consolidateAfter: 30s  # 빠른 정리
---
# Preview Pod에 toleration 추가
spec:
  tolerations:
    - key: preview
      operator: Equal
      value: "true"
      effect: NoSchedule
  nodeSelector:
    karpenter.sh/capacity-type: spot
```

### 자동 스케일 다운

```yaml
# KEDA ScaledObject (사용량 기반)
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: preview-scaler
  namespace: preview-pr-123
spec:
  scaleTargetRef:
    name: myapp
  minReplicaCount: 0  # 제로 스케일!
  maxReplicaCount: 2
  cooldownPeriod: 300  # 5분
  triggers:
    - type: prometheus
      metadata:
        serverAddress: http://prometheus:9090
        metricName: http_requests_total
        threshold: "1"
        query: |
          sum(rate(http_requests_total{namespace="preview-pr-123"}[5m]))
```

---

## Sources

- [Ephemeral Environments](https://ephemeralenvironments.io/)
- [Argo CD ApplicationSet PR Generator](https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Generators-Pull-Request/)
- [Qovery Preview Environments](https://www.qovery.com/blog/preview-environments)
- [Northflank Preview Environments](https://northflank.com/blog/preview-environment-platforms)
- [Cost Savings with Ephemeral](https://www.bunnyshell.com/blog/ephemeral-environments-cost-savings/)

## 참조 스킬

- `/ephemeral-environments` - Ephemeral 환경 핵심 (ArgoCD ApplicationSet, Namespace 격리, Kyverno 정리)
- `/gitops-argocd` - ArgoCD GitOps
- `/finops` - FinOps 기초
- `/k8s-scheduling` - 스케줄링 최적화
