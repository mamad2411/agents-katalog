---
name: gitops-argocd-advanced
category: cicd
description: "GitOps ArgoCD 고급 패턴 — ApplicationSet, Sync 전략, 프로젝트/RBAC, 시크릿 관리 Use when working with cicd 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# GitOps ArgoCD 고급 패턴

ApplicationSet, Sync 전략, 프로젝트/RBAC, 시크릿 관리

## Quick Reference

```
고급 기능 선택?
    │
    ├─ 멀티 환경 배포 ───────> ApplicationSet
    │       │
    │       └─ Generator: List, Cluster, Git
    │
    ├─ 배포 순서 제어 ───────> Sync Waves + Hooks
    │
    ├─ 팀별 권한 분리 ───────> AppProject + RBAC
    │
    └─ 시크릿 관리 ─────────> Sealed Secrets / External Secrets
```

---

## ApplicationSet (멀티 클러스터/환경)

### Generator 유형

| Generator | 용도 |
|-----------|------|
| **List** | 명시적 클러스터/환경 목록 |
| **Cluster** | 등록된 클러스터 기반 |
| **Git Directory** | Git 폴더 구조 기반 |
| **Git File** | Git 파일 내용 기반 |
| **Matrix** | Generator 조합 |

### 멀티 환경 ApplicationSet

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: my-app
  namespace: argocd
spec:
  generators:
    - list:
        elements:
          - env: dev
            namespace: my-app-dev
            revision: develop
          - env: staging
            namespace: my-app-staging
            revision: main
          - env: prod
            namespace: my-app-prod
            revision: v1.2.3  # 프로덕션은 태그

  template:
    metadata:
      name: 'my-app-{{env}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/myorg/my-app.git
        targetRevision: '{{revision}}'
        path: k8s/overlays/{{env}}
      destination:
        server: https://kubernetes.default.svc
        namespace: '{{namespace}}'
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

### Git Directory Generator

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: cluster-addons
  namespace: argocd
spec:
  generators:
    - git:
        repoURL: https://github.com/myorg/gitops-config.git
        revision: main
        directories:
          - path: addons/*

  template:
    metadata:
      name: '{{path.basename}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/myorg/gitops-config.git
        targetRevision: main
        path: '{{path}}'
      destination:
        server: https://kubernetes.default.svc
        namespace: '{{path.basename}}'
```

### Cluster Generator (멀티 클러스터)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: monitoring
  namespace: argocd
spec:
  generators:
    - clusters:
        selector:
          matchLabels:
            env: production

  template:
    metadata:
      name: 'monitoring-{{name}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/myorg/gitops-config.git
        targetRevision: main
        path: monitoring
      destination:
        server: '{{server}}'
        namespace: monitoring
```

---

## Sync 전략

### Sync Options

```yaml
syncPolicy:
  automated:
    prune: true           # Git에서 삭제된 리소스 정리
    selfHeal: true        # 수동 변경 되돌리기
    allowEmpty: false     # 빈 앱 허용 안함
  syncOptions:
    - CreateNamespace=true
    - PrunePropagationPolicy=foreground
    - PruneLast=true      # 마지막에 정리
    - Validate=true       # 매니페스트 검증
    - ApplyOutOfSyncOnly=true  # 변경된 것만 적용
    - ServerSideApply=true     # 서버 사이드 적용
```

### Sync Waves (순서 제어)

```yaml
# 1단계: Namespace
apiVersion: v1
kind: Namespace
metadata:
  name: my-app
  annotations:
    argocd.argoproj.io/sync-wave: "-1"

---
# 2단계: ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-config
  annotations:
    argocd.argoproj.io/sync-wave: "0"

---
# 3단계: Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  annotations:
    argocd.argoproj.io/sync-wave: "1"
```

### Sync Hooks

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migration
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
spec:
  template:
    spec:
      containers:
        - name: migration
          image: myapp-migration:latest
          command: ["./migrate.sh"]
      restartPolicy: Never
```

| Hook | 실행 시점 |
|------|----------|
| **PreSync** | Sync 전 |
| **Sync** | Sync 중 |
| **PostSync** | Sync 후 |
| **SyncFail** | Sync 실패 시 |

---

## Repository 구조 Best Practices

### CRITICAL: Config 분리

```
# 권장: 설정 저장소 분리
app-source/          # 애플리케이션 소스 코드
gitops-config/       # K8s 매니페스트 (ArgoCD가 바라봄)

# 비권장: 같은 저장소
my-app/
├── src/
└── k8s/             # CI가 이미지 태그 변경 → 무한 루프 위험
```

### 환경별 구조 (Kustomize)

```
gitops-config/
├── base/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── kustomization.yaml
└── overlays/
    ├── dev/
    │   ├── kustomization.yaml
    │   └── patch-replicas.yaml
    ├── staging/
    │   └── kustomization.yaml
    └── prod/
        ├── kustomization.yaml
        ├── patch-replicas.yaml
        └── patch-resources.yaml
```

```yaml
# overlays/prod/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - ../../base

namePrefix: prod-
namespace: my-app-prod

images:
  - name: myapp
    newName: ghcr.io/myorg/myapp
    newTag: v1.2.3

patchesStrategicMerge:
  - patch-replicas.yaml
```

---

## 프로젝트 & RBAC

### AppProject 정의

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: my-team
  namespace: argocd
spec:
  description: My Team Project

  # 허용되는 소스 저장소
  sourceRepos:
    - 'https://github.com/myorg/*'
    - 'https://charts.helm.sh/*'

  # 배포 대상 제한
  destinations:
    - namespace: 'my-team-*'
      server: https://kubernetes.default.svc
    - namespace: 'my-team-*'
      server: https://prod-cluster.example.com

  # 허용되는 리소스 종류
  clusterResourceWhitelist:
    - group: ''
      kind: Namespace
  namespaceResourceWhitelist:
    - group: '*'
      kind: '*'

  # 금지되는 리소스
  namespaceResourceBlacklist:
    - group: ''
      kind: ResourceQuota
    - group: ''
      kind: LimitRange

  roles:
    - name: developer
      description: Developer role
      policies:
        - p, proj:my-team:developer, applications, get, my-team/*, allow
        - p, proj:my-team:developer, applications, sync, my-team/*, allow
      groups:
        - my-team-developers
```

### AppProject 와일드카드 검증 가이드

**`namespaceResourceWhitelist`**: `kind: "*"` 사용 카운트 → 2개+ API 그룹이면 최소 권한 위반 경고

```yaml
# ❌ 모든 리소스 허용 (사실상 무제한)
namespaceResourceWhitelist:
  - group: '*'
    kind: '*'

# ✅ 단계적 제한: 필요한 리소스만 명시
namespaceResourceWhitelist:
  - group: ''
    kind: ConfigMap
  - group: ''
    kind: Secret
  - group: ''
    kind: Service
  - group: apps
    kind: Deployment
```

**`sourceRepos`**: 최소한 org prefix 제한

```yaml
# ❌ sourceRepos: ['*']
# ✅ sourceRepos: ['https://github.com/my-org/*']
```

**`destinations`**: namespace 패턴 제한

```yaml
# ❌ namespace: '*'
# ✅ namespace: '{team}-*'
```

상세 예제: `/k8s-security` 스킬의 AppProject 섹션 참조

---

## ApplicationSet 하이브리드 패턴

### 부트스트랩 = Application, 앱 배포 = ApplicationSet

```
Bootstrap (순서 중요 → 개별 Application + sync-wave):
  istio-base     (wave -3)
  istiod         (wave -2)
  gateway        (wave -1)
  cert-manager   (wave -2)
  external-secrets (wave -2)

App Deployment (반복 패턴 → ApplicationSet):
  example-server    (dev, staging, prod)
  example-front     (dev, staging, prod)
  example-payment   (dev, staging, prod)
```

### 혼합 금지 원칙

같은 리소스를 Application과 ApplicationSet 양쪽에서 관리하면 충돌 발생.

```yaml
# ❌ istio-base를 Application으로도, ApplicationSet으로도 생성
# → 두 컨트롤러가 동시에 sync하면서 충돌

# ✅ 역할 분리
# infrastructure/bootstrap/ → 개별 Application (sync-wave)
# applications/ → ApplicationSet (Generator 기반)
```

---

**시크릿 관리**: `/gitops-argocd-helm` 스킬의 Secrets + Helm 통합 섹션 참조

---

## 모니터링 & 알림

### Notifications 설정

```yaml
# argocd-notifications-cm ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-notifications-cm
  namespace: argocd
data:
  service.slack: |
    token: $slack-token
  template.app-sync-succeeded: |
    message: |
      {{.app.metadata.name}} 동기화 성공!
      Revision: {{.app.status.sync.revision}}
  trigger.on-sync-succeeded: |
    - when: app.status.sync.status == 'Synced'
      send: [app-sync-succeeded]
```

### Application 알림 설정

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  annotations:
    notifications.argoproj.io/subscribe.on-sync-succeeded.slack: my-channel
    notifications.argoproj.io/subscribe.on-sync-failed.slack: alerts-channel
```

### Prometheus 메트릭

```promql
# Sync 상태
argocd_app_info{sync_status="Synced"}

# Health 상태
argocd_app_info{health_status="Healthy"}

# Sync 실패 카운트
sum(argocd_app_sync_total{phase="Failed"}) by (name)
```

---

## 체크리스트

### ApplicationSet
- [ ] Generator 유형 선택 (List, Git, Cluster)
- [ ] 템플릿 변수 정의
- [ ] 환경별 분기 설정

### Sync 전략
- [ ] Sync Waves 설정 (순서 필요 시)
- [ ] PreSync Hook (마이그레이션 등)
- [ ] 적절한 syncOptions

### 보안
- [ ] Sealed Secrets 또는 External Secrets
- [ ] AppProject로 권한 제한
- [ ] RBAC 설정

### 모니터링
- [ ] Notifications 설정
- [ ] Health 체크 확인
- [ ] Sync 상태 대시보드

**참조 스킬**: `/gitops-argocd` (기본 GitOps/ArgoCD), `/gitops-argocd-ai` (AI-assisted GitOps), `/cicd-devsecops`, `/deployment-strategies`, `/k8s-helm`
