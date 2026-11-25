---
name: terraform-k8s-bootstrap
category: infrastructure
description: "Terraform K8s Bootstrap 가이드 — Terraform→EKS/GKE→ArgoCD 부트스트랩 패턴, 책임 경계 정의, 순환 의존성 해결 Use when working with infrastructure 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Terraform K8s Bootstrap 가이드

Terraform→EKS/GKE→ArgoCD 부트스트랩 패턴, 책임 경계 정의, 순환 의존성 해결

## Quick Reference (결정 트리)

```
K8s 클러스터 부트스트랩?
    │
    ├─ AWS EKS ──────────> terraform-aws-eks 모듈
    │     │
    │     └─ IRSA + helm_release (ArgoCD, ESO)
    │
    ├─ GCP GKE ──────────> terraform-google-kubernetes-engine 모듈
    │     │
    │     └─ Workload Identity + helm_release (ArgoCD, ESO)
    │
    └─ Bootstrap Layer?
          │
          ├─ 최소 셋: Cluster + ArgoCD + ESO + ClusterSecretStore
          └─ 나머지 전부: ArgoCD가 GitOps로 관리
```

---

## CRITICAL: 부트스트랩 순환 의존성 문제

### 문제

```
ArgoCD 앱 배포 → Secret 필요 (DB 비밀번호 등)
Secret 가져오기 → ESO (External Secrets Operator) 필요
ESO 설치        → ArgoCD로 하려면... ArgoCD가 먼저 떠야 함
ArgoCD 시작     → Git repo 접속 Secret 필요 → ESO 필요 → 🔄 순환!
```

### 해결: Terraform Bootstrap Layer

```
Terraform 영역 ("ArgoCD가 자립할 수 있는 최소 셋")
──────────────────────────────────────────────
1. VPC / Network
2. EKS Cluster / GKE Cluster
3. IAM (IRSA / Workload Identity)
4. ArgoCD (helm_release)
5. ESO (helm_release)
6. ClusterSecretStore
7. ArgoCD 초기 시크릿 (Git repo 접속 정보)
──────────────────────────────────────────────
이후 ArgoCD가 전부 관리 (Sync Wave 순서 제어)
```

---

## Terraform vs ArgoCD 책임 경계

### 원칙

```
Terraform = "클러스터를 띄운다" (인프라 프로비저닝)
ArgoCD    = "클러스터를 운영한다" (선언적 상태 관리)
중첩 영역 = "IAM/권한은 Terraform, 워크로드는 ArgoCD"
```

### 소유권 매트릭스

| 컴포넌트 | Terraform | ArgoCD | 이유 |
|----------|-----------|--------|------|
| VPC / Subnet / NAT | O | X | 인프라 기반, 거의 안 바뀜 |
| EKS / GKE Cluster | O | X | 클러스터 자체는 인프라 |
| Node Group / Karpenter IRSA | O | X | IAM은 인프라 영역 |
| Karpenter chart | X | O | K8s 워크로드 |
| ArgoCD | O (bootstrap) | O (self-manage) | 초기 설치 후 자기 자신 관리 |
| ESO | O (bootstrap) | O (self-manage) | 초기 설치 후 ArgoCD가 업데이트 |
| ClusterSecretStore | O | X | IRSA/WI 의존, 인프라 영역 |
| EKS Add-ons (CoreDNS, VPC CNI) | O | X | EKS 관리형, Terraform이 자연스러움 |
| GKE Add-ons | X (자동관리) | X | GKE가 자동 관리 |
| ALB Controller / IRSA | O (IRSA) | O (chart) | IAM은 Terraform, 워크로드는 ArgoCD |
| cert-manager | X | O | K8s 워크로드 |
| Istio | X | O | K8s 워크로드 |
| kube-prometheus-stack | X | O | K8s 워크로드 |
| 앱 Deployment | X | O | 배포 빈도 높음, GitOps |
| RDS / Cloud SQL | O | X | 관리형 서비스, 인프라 |
| ElastiCache / Memorystore | O | X | 관리형 서비스, 인프라 |
| MSK / Pub/Sub | O | X | 관리형 서비스, 인프라 |
| S3 / GCS | O | X | 스토리지, 인프라 |
| Route53 / Cloud DNS | O | X | DNS, 인프라 |

### 회사 규모별 패턴

```
1~3명 (스타트업):
  한 사람이 Terraform + ArgoCD 전부 관리
  Terraform으로 ArgoCD까지 bootstrap → App of Apps로 나머지
  같은 repo에 terraform/ + k8s/ 디렉토리

4~10명 (성장기):
  인프라 담당 1명: Terraform (infra repo)
  개발자들: ArgoCD로 배포 (k8s-config repo)
  ArgoCD 관리는 인프라 담당이 겸임

10명+ (엔터프라이즈):
  Cloud Team:    Terraform (infra repo) — VPC, EKS/GKE, IAM
  Platform Team: ArgoCD 관리 (platform repo) — add-ons, 모니터링
  Dev Team:      Git push만 (app repos) — ArgoCD가 자동 배포
```

---

## EKS Bootstrap (Terraform)

### 디렉토리 구조

```
terraform/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── terraform.tfvars
│   └── prod/
│       ├── main.tf
│       ├── variables.tf
│       └── terraform.tfvars
├── modules/
│   ├── vpc/
│   ├── eks/
│   └── bootstrap/          # ArgoCD + ESO 설치
│       ├── main.tf
│       ├── argocd.tf
│       ├── eso.tf
│       └── variables.tf
└── backend.tf               # S3 remote state
```

### Bootstrap 모듈 (ArgoCD + ESO)

```hcl
# modules/bootstrap/argocd.tf

resource "helm_release" "argocd" {
  name             = "argocd"
  namespace        = "argocd"
  create_namespace = true
  repository       = "https://argoproj.github.io/argo-helm"
  chart            = "argo-cd"
  version          = var.argocd_chart_version   # "7.7.0"

  values = [templatefile("${path.module}/values/argocd.yaml", {
    environment = var.environment
  })]

  depends_on = [module.eks]
}

# ArgoCD가 Git repo에 접근하기 위한 초기 시크릿
resource "kubernetes_secret" "argocd_repo" {
  metadata {
    name      = "repo-credentials"
    namespace = "argocd"
    labels = {
      "argocd.argoproj.io/secret-type" = "repository"
    }
  }
  data = {
    type     = "git"
    url      = var.git_repo_url
    password = var.git_token               # GitHub PAT or deploy key
    username = "x-access-token"
  }

  depends_on = [helm_release.argocd]
}
```

```hcl
# modules/bootstrap/eso.tf

# ESO용 IRSA
module "eso_irsa" {
  source = "terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks"

  role_name = "${var.cluster_name}-eso"
  attach_external_secrets_policy = true

  oidc_providers = {
    main = {
      provider_arn = module.eks.oidc_provider_arn
      namespace_service_accounts = ["external-secrets:external-secrets"]
    }
  }
}

resource "helm_release" "external_secrets" {
  name             = "external-secrets"
  namespace        = "external-secrets"
  create_namespace = true
  repository       = "https://charts.external-secrets.io"
  chart            = "external-secrets"
  version          = var.eso_chart_version   # "0.12.1"

  set {
    name  = "serviceAccount.annotations.eks\\.amazonaws\\.com/role-arn"
    value = module.eso_irsa.iam_role_arn
  }

  depends_on = [helm_release.argocd]
}

# ClusterSecretStore (AWS Secrets Manager)
resource "kubectl_manifest" "cluster_secret_store" {
  yaml_body = yamlencode({
    apiVersion = "external-secrets.io/v1beta1"
    kind       = "ClusterSecretStore"
    metadata = { name = "aws-secretsmanager" }
    spec = {
      provider = {
        aws = {
          service = "SecretsManager"
          region  = var.aws_region
          auth = {
            jwt = {
              serviceAccountRef = {
                name      = "external-secrets"
                namespace = "external-secrets"
              }
            }
          }
        }
      }
    }
  })

  depends_on = [helm_release.external_secrets]
}
```

---

## GKE Bootstrap (Terraform)

### GKE 클러스터 + Bootstrap

```hcl
# modules/gke/main.tf

module "gke" {
  source = "terraform-google-modules/kubernetes-engine/google//modules/private-cluster"
  version = "~> 34.0"

  project_id        = var.project_id
  name              = "${var.cluster_name}-${var.environment}"
  region            = var.region
  zones             = var.zones
  network           = module.vpc.network_name
  subnetwork        = module.vpc.subnets_names[0]
  ip_range_pods     = "pods"
  ip_range_services = "services"

  release_channel    = "REGULAR"                 # 자동 K8s 버전 관리
  enable_autopilot   = var.use_autopilot         # Autopilot vs Standard

  # Workload Identity (GKE 권장)
  identity_namespace = "${var.project_id}.svc.id.goog"

  node_pools = var.use_autopilot ? [] : [
    {
      name         = "default"
      machine_type = var.node_machine_type        # "e2-standard-4"
      min_count    = var.node_min_count
      max_count    = var.node_max_count
      auto_upgrade = true
    }
  ]
}
```

```hcl
# modules/bootstrap/eso-gke.tf

# Workload Identity for ESO
resource "google_service_account" "eso" {
  account_id   = "eso-${var.environment}"
  display_name = "External Secrets Operator"
  project      = var.project_id
}

resource "google_project_iam_member" "eso_secret_accessor" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.eso.email}"
}

# K8s SA ↔ GCP SA 바인딩
resource "google_service_account_iam_member" "eso_workload_identity" {
  service_account_id = google_service_account.eso.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project_id}.svc.id.goog[external-secrets/external-secrets]"
}

resource "helm_release" "external_secrets" {
  name             = "external-secrets"
  namespace        = "external-secrets"
  create_namespace = true
  repository       = "https://charts.external-secrets.io"
  chart            = "external-secrets"
  version          = var.eso_chart_version

  set {
    name  = "serviceAccount.annotations.iam\\.gke\\.io/gcp-service-account"
    value = google_service_account.eso.email
  }

  depends_on = [module.gke]
}

# ClusterSecretStore (GCP Secret Manager)
resource "kubectl_manifest" "cluster_secret_store" {
  yaml_body = yamlencode({
    apiVersion = "external-secrets.io/v1beta1"
    kind       = "ClusterSecretStore"
    metadata = { name = "gcp-secretmanager" }
    spec = {
      provider = {
        gcpsm = {
          projectID = var.project_id
          auth = {
            workloadIdentity = {
              clusterLocation  = var.region
              clusterName      = module.gke.name
              clusterProjectID = var.project_id
              serviceAccountRef = {
                name      = "external-secrets"
                namespace = "external-secrets"
              }
            }
          }
        }
      }
    }
  })

  depends_on = [helm_release.external_secrets]
}
```

---

## ArgoCD App of Apps (Bootstrap 이후)

Terraform bootstrap 완료 후 ArgoCD가 자기 자신과 나머지를 관리.

```yaml
# argocd/apps/root-app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: root
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/my-org/k8s-config.git
    targetRevision: main
    path: argocd/apps
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### Sync Wave 순서 (Bootstrap Layer 이후)

```yaml
# argocd/apps/ 디렉토리 내 Application들

# Wave -3: ArgoCD self-manage (Terraform에서 넘겨받기)
argocd.argoproj.io/sync-wave: "-3"

# Wave -2: 인프라 기반 (ESO self-manage, cert-manager)
argocd.argoproj.io/sync-wave: "-2"

# Wave -1: 모니터링 / 메시 (kube-prometheus-stack, Istio)
argocd.argoproj.io/sync-wave: "-1"

# Wave 0: 플랫폼 도구 (Ingress controller, KEDA)
argocd.argoproj.io/sync-wave: "0"

# Wave 1+: 앱 배포
argocd.argoproj.io/sync-wave: "1"
```

---

## Terraform State 관리

### Remote Backend 설정

```hcl
# backend.tf (EKS)
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "eks/${var.environment}/terraform.tfstate"
    region         = "ap-northeast-2"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}

# backend.tf (GKE)
terraform {
  backend "gcs" {
    bucket = "my-terraform-state"
    prefix = "gke/${var.environment}"
  }
}
```

### 충돌 방지 원칙

```
1. Terraform이 관리하는 리소스를 ArgoCD가 수정하지 않는다.
   → ArgoCD Application에 ignoreDifferences 설정

2. ArgoCD가 관리하는 리소스를 Terraform이 수정하지 않는다.
   → Terraform에서 K8s 리소스 생성 최소화

3. Bootstrap 후 Terraform → ArgoCD 핸드오프:
   → ArgoCD가 self-manage Application으로 자신을 관리
   → ESO도 ArgoCD Application으로 전환 (버전 업데이트 등)
   → Terraform의 helm_release는 lifecycle { ignore_changes = all }
```

```hcl
# 핸드오프 후 Terraform이 더 이상 관리하지 않도록
resource "helm_release" "argocd" {
  # ... 초기 설정 ...

  lifecycle {
    ignore_changes = all    # ArgoCD가 self-manage로 전환 후
  }
}
```

---

## EKS vs GKE 차이점 요약

| 항목 | EKS | GKE |
|------|-----|-----|
| IAM 연동 | IRSA (Pod Identity) | Workload Identity |
| Secret Store | AWS Secrets Manager | GCP Secret Manager |
| Add-on 관리 | Terraform `cluster_addons` | GKE 자동 관리 (대부분) |
| LB Controller | AWS LB Controller (별도 설치) | GKE Ingress (내장) |
| Node 관리 | Karpenter 권장 | Autopilot 또는 NAP |
| K8s 업그레이드 | 수동 or Auto Mode | Release Channel (자동) |
| 비용 | $0.10/hr + 노드 | Standard: 무료 + 노드 |
| CSI Driver | EBS CSI (별도) | PD CSI (내장) |
