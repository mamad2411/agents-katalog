---
name: crossplane-advanced
category: infrastructure
description: "Crossplane 고급 패턴 가이드 — 멀티클라우드 패턴, GitOps 통합, Drift Detection, Crossplane v2 Use when working with infrastructure 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Crossplane 고급 패턴 가이드

멀티클라우드 패턴, GitOps 통합, Drift Detection, Crossplane v2

## GCP / Azure ProviderConfig

### GCP ProviderConfig

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: gcp-creds
  namespace: crossplane-system
type: Opaque
stringData:
  credentials: |
    {
      "type": "service_account",
      "project_id": "my-project",
      ...
    }
---
apiVersion: gcp.upbound.io/v1beta1
kind: ProviderConfig
metadata:
  name: default
spec:
  projectID: my-project
  credentials:
    source: Secret
    secretRef:
      namespace: crossplane-system
      name: gcp-creds
      key: credentials
```

### Azure ProviderConfig

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: azure-creds
  namespace: crossplane-system
type: Opaque
stringData:
  credentials: |
    {
      "clientId": "...",
      "clientSecret": "...",
      "subscriptionId": "...",
      "tenantId": "..."
    }
---
apiVersion: azure.upbound.io/v1beta1
kind: ProviderConfig
metadata:
  name: default
spec:
  credentials:
    source: Secret
    secretRef:
      namespace: crossplane-system
      name: azure-creds
      key: credentials
```

---

## 멀티클라우드 패턴

### 환경별 Provider 분리

```yaml
# Production: AWS
apiVersion: platform.example.com/v1alpha1
kind: DatabaseClaim
metadata:
  name: prod-db
  namespace: production
spec:
  parameters:
    size: large
    engine: postgres
    highAvailability: true
  compositionSelector:
    matchLabels:
      provider: aws
      environment: production
---
# Development: GCP (비용 절감)
apiVersion: platform.example.com/v1alpha1
kind: DatabaseClaim
metadata:
  name: dev-db
  namespace: development
spec:
  parameters:
    size: small
    engine: postgres
  compositionSelector:
    matchLabels:
      provider: gcp
      environment: development
```

### Composition Functions

```yaml
# Crossplane Functions으로 복잡한 로직 처리
apiVersion: pkg.crossplane.io/v1beta1
kind: Function
metadata:
  name: function-patch-and-transform
spec:
  package: xpkg.upbound.io/crossplane-contrib/function-patch-and-transform:v0.7.0
---
apiVersion: pkg.crossplane.io/v1beta1
kind: Function
metadata:
  name: function-auto-ready
spec:
  package: xpkg.upbound.io/crossplane-contrib/function-auto-ready:v0.2.1
```

---

## GitOps 통합 (ArgoCD)

### ArgoCD Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: crossplane-infrastructure
  namespace: argocd
spec:
  project: infrastructure
  source:
    repoURL: https://github.com/myorg/infrastructure.git
    targetRevision: main
    path: crossplane/claims
  destination:
    server: https://kubernetes.default.svc
    namespace: crossplane-system
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### 디렉토리 구조

```
infrastructure/
├── crossplane/
│   ├── providers/
│   │   ├── aws.yaml
│   │   ├── gcp.yaml
│   │   └── azure.yaml
│   ├── xrds/
│   │   ├── database.yaml
│   │   ├── network.yaml
│   │   └── storage.yaml
│   ├── compositions/
│   │   ├── database-aws.yaml
│   │   ├── database-gcp.yaml
│   │   └── network-aws.yaml
│   └── claims/
│       ├── production/
│       │   ├── database.yaml
│       │   └── network.yaml
│       └── staging/
│           └── database.yaml
```

---

## CRITICAL: Drift 감지 및 수정

### 자동 Reconciliation

```yaml
# Crossplane은 기본적으로 자동 Drift 수정
# 아래 설정으로 동작 제어 가능

apiVersion: s3.aws.upbound.io/v1beta2
kind: Bucket
metadata:
  name: my-bucket
  annotations:
    # Reconciliation 주기 (기본: 1시간)
    crossplane.io/external-create-pending: ""
spec:
  managementPolicies:
    - "*"  # 전체 관리 (Create, Update, Delete)
    # - "Observe"  # 읽기만 (Drift 감지만, 수정 안함)

  forProvider:
    region: ap-northeast-2
```

### Drift 모니터링

```bash
# 모든 Managed Resources 상태 확인
kubectl get managed

# 특정 리소스 상태 상세 확인
kubectl describe bucket.s3.aws my-bucket

# Synced 조건 확인
kubectl get bucket.s3.aws my-bucket -o jsonpath='{.status.conditions[?(@.type=="Synced")]}'
```

---

## Crossplane v2 (프리뷰)

### 주요 변화

```yaml
# v2에서의 개선점
변경사항:
  - Application Control Plane 개념 도입
  - 더 나은 상태 관리
  - 향상된 Composition Functions
  - 네이티브 Terraform Provider 지원 개선

# Terraform Provider 연동
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: provider-terraform
spec:
  package: xpkg.upbound.io/upbound/provider-terraform:v0.18.0
```

---

## Sources

- [Crossplane Documentation](https://docs.crossplane.io/)
- [Upbound Marketplace](https://marketplace.upbound.io/)
- [Crossplane vs Terraform](https://www.crossplane.io/blog/crossplane-vs-terraform)
- [Multi-cloud Kubernetes 2026](https://www.spectrocloud.com/blog/managing-multi-cloud-kubernetes-in-2025)
- [Crossplane Compositions Guide](https://docs.crossplane.io/latest/concepts/compositions/)

## 참조 스킬

- `/crossplane` - Crossplane 핵심 개념 (설치, Provider, Compositions, XRD)
- `/terraform-modules` - Terraform 모듈
- `/gitops-argocd` - ArgoCD GitOps
