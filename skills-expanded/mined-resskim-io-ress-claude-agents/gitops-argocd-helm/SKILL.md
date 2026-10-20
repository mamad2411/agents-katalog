---
name: gitops-argocd-helm
category: cicd
description: "ArgoCD + Helm 통합 패턴 가이드 — ArgoCD Image Updater, Multi-source Application, Helm hooks 비교, Secrets+Helm 통합 Use when working with cicd 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# ArgoCD + Helm 통합 패턴 가이드

ArgoCD Image Updater, Multi-source Application, Helm hooks 비교, Secrets+Helm 통합

## Quick Reference (결정 트리)

```
Helm + ArgoCD 통합?
    │
    ├─ 이미지 자동 업데이트 ──> ArgoCD Image Updater
    │     │
    │     ├─ Digest 기반 (불변) ──> write-back: git (권장)
    │     └─ Tag 기반 (semver) ───> update-strategy: semver
    │
    ├─ Chart + Values 분리 ────> Multi-source Application
    │     │
    │     └─ spec.sources[] (ArgoCD 2.8+)
    │
    ├─ Hook 선택 ──────────────> ArgoCD hooks (권장)
    │     │
    │     ├─ DB 마이그레이션 ──> PreSync Job
    │     └─ 알림 전송 ────────> PostSync Job
    │
    └─ 시크릿 관리 ────────────> ESO + Helm 통합
          │
          └─ ExternalSecret을 Helm template에 포함
```

---

## ArgoCD Image Updater

컨테이너 이미지 태그가 업데이트되면 자동으로 Git에 반영하는 컴포넌트.

### 설치

```yaml
# ArgoCD Application으로 설치
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: argocd-image-updater
  namespace: argocd
spec:
  source:
    repoURL: https://argoproj.github.io/argo-helm
    chart: argocd-image-updater
    targetRevision: 0.11.0
    helm:
      values: |
        config:
          registries:
            - name: ECR
              api_url: https://<account>.dkr.ecr.ap-northeast-2.amazonaws.com
              prefix: <account>.dkr.ecr.ap-northeast-2.amazonaws.com
              credentials: ext:/scripts/ecr-login.sh
              default: true
            - name: GCR
              api_url: https://gcr.io
              prefix: gcr.io
              credentials: pullsecret:argocd/gcr-credentials
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
```

### Application에 이미지 업데이트 설정

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  annotations:
    # 이미지 업데이트 대상 지정
    argocd-image-updater.argoproj.io/image-list: >
      app=<account>.dkr.ecr.ap-northeast-2.amazonaws.com/myapp
    # 업데이트 전략: semver (태그 기반)
    argocd-image-updater.argoproj.io/app.update-strategy: semver
    # semver 필터: 1.x.x만 허용
    argocd-image-updater.argoproj.io/app.allow-tags: "regexp:^1\\."
    # Git write-back (Git에 변경 커밋)
    argocd-image-updater.argoproj.io/write-back-method: git
    argocd-image-updater.argoproj.io/write-back-target: "helmvalues:values.yaml"
    argocd-image-updater.argoproj.io/git-branch: main
```

### Update Strategy 비교

| 전략 | 설명 | 사용 시점 |
|------|------|----------|
| `semver` | SemVer 태그 중 최신 선택 | 버전 태그 사용 시 (`v1.2.3`) |
| `latest` | 가장 최근 빌드된 이미지 | `latest` 태그 사용 시 |
| `digest` | SHA digest 비교 | 동일 태그의 내용 변경 감지 |
| `name` | 알파벳 순 최신 태그 | 날짜 기반 태그 (`20260307`) |

### Write-back 방식

```
argocd (기본):  ArgoCD 파라미터 override로 적용 (Git 변경 없음)
                → 간단하지만 Git에 기록이 안 남음

git (권장):     values.yaml을 직접 수정하고 커밋
                → GitOps 원칙에 맞음, 변경 이력 추적 가능
                → write-back-target으로 수정 대상 파일 지정
```

---

## Multi-source Application (ArgoCD 2.8+)

Helm chart와 values 파일을 서로 다른 Git repo에서 가져오는 패턴.

### 왜 필요한가

```
기존 문제:
  chart repo (공개 Helm registry)와
  values repo (내부 Git)가 분리되어 있으면
  하나의 Application으로 관리 불가

해결:
  spec.sources[] (복수형)으로 여러 소스 지정
```

### 구성 예시

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
spec:
  project: default
  sources:                              # 복수형 sources[]
    # Source 1: Helm chart (공개 레지스트리)
    - repoURL: https://prometheus-community.github.io/helm-charts
      chart: kube-prometheus-stack
      targetRevision: 65.1.0
      helm:
        valueFiles:
          # Source 2의 파일을 참조 ($values/)
          - $values/environments/prod/kube-prometheus-stack.yaml

    # Source 2: values 파일 (내부 Git repo)
    - repoURL: https://github.com/my-org/k8s-config.git
      targetRevision: main
      ref: values                       # $values로 참조 가능
  destination:
    server: https://kubernetes.default.svc
    namespace: monitoring
```

### ApplicationSet + Multi-source

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: monitoring-stack
spec:
  generators:
    - list:
        elements:
          - env: dev
            cluster: in-cluster
            valuesPath: environments/dev
          - env: prod
            cluster: https://prod-eks.example.com
            valuesPath: environments/prod
  template:
    metadata:
      name: "monitoring-{{env}}"
    spec:
      sources:
        - repoURL: https://prometheus-community.github.io/helm-charts
          chart: kube-prometheus-stack
          targetRevision: 65.1.0
          helm:
            valueFiles:
              - "$values/{{valuesPath}}/kube-prometheus-stack.yaml"
        - repoURL: https://github.com/my-org/k8s-config.git
          targetRevision: main
          ref: values
      destination:
        server: "{{cluster}}"
        namespace: monitoring
```

---

## Helm Hooks vs ArgoCD Hooks

### 비교표

| 항목 | Helm Hook | ArgoCD Hook |
|------|-----------|-------------|
| 어노테이션 | `helm.sh/hook` | `argocd.argoproj.io/hook` |
| 실행 시점 | install/upgrade/delete | PreSync/Sync/PostSync/SyncFail |
| 삭제 정책 | `helm.sh/hook-delete-policy` | `argocd.argoproj.io/hook-delete-policy` |
| 순서 제어 | `helm.sh/hook-weight` | `argocd.argoproj.io/sync-wave` |
| ArgoCD 인식 | 무시됨 (ArgoCD가 관리 안 함) | ArgoCD가 직접 관리 |
| 권장 여부 | ArgoCD 환경에서는 비권장 | ArgoCD 환경에서 권장 |

### ArgoCD에서 Helm Hook이 무시되는 이유

```
ArgoCD는 helm template으로 매니페스트를 렌더링한 후 kubectl apply.
helm install/upgrade를 실행하지 않으므로 Helm Hook이 트리거되지 않음.

→ 해결: helm.sh/hook 어노테이션을 argocd.argoproj.io/hook으로 교체
```

### DB 마이그레이션 Hook 예시 (ArgoCD 방식)

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migrate-{{ .Values.image.tag }}
  annotations:
    argocd.argoproj.io/hook: PreSync           # 앱 배포 전 실행
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
    argocd.argoproj.io/sync-wave: "-1"         # ESO 시크릿 이후
spec:
  template:
    spec:
      containers:
        - name: migrate
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          command: ["./migrate", "up"]
          envFrom:
            - secretRef:
                name: db-credentials
      restartPolicy: Never
  backoffLimit: 3
```

### Slack/Discord 알림 Hook

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: notify-deploy
  annotations:
    argocd.argoproj.io/hook: PostSync          # 배포 완료 후
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
spec:
  template:
    spec:
      containers:
        - name: notify
          image: curlimages/curl:8.5.0
          command:
            - curl
            - -X POST
            - $(WEBHOOK_URL)
            - -H
            - "Content-Type: application/json"
            - -d
            - '{"content": "Deploy completed: {{ .Values.image.tag }}"}'
          env:
            - name: WEBHOOK_URL
              valueFrom:
                secretKeyRef:
                  name: webhook-secrets
                  key: discord-url
      restartPolicy: Never
```

---

## Secrets + Helm 통합

### ExternalSecret을 Helm template에 포함

```yaml
# templates/external-secret.yaml
{{- if eq .Values.secrets.backend "external-secrets" }}
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: {{ include "myapp.fullname" . }}-secrets
  annotations:
    argocd.argoproj.io/sync-wave: "-1"        # 앱 Deployment보다 먼저
spec:
  refreshInterval: {{ .Values.secrets.refreshInterval | default "1h" }}
  secretStoreRef:
    name: {{ .Values.secrets.secretStore }}
    kind: ClusterSecretStore
  target:
    name: {{ include "myapp.fullname" . }}-secrets
  data:
    - secretKey: DB_PASSWORD
      remoteRef:
        key: {{ .Values.global.environment }}/myapp/db-password
    - secretKey: API_KEY
      remoteRef:
        key: {{ .Values.global.environment }}/myapp/api-key
{{- end }}
```

### ArgoCD + ESO ignoreDifferences 설정

ESO가 생성한 Secret의 data 필드는 ArgoCD가 관리하지 않도록 설정.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
spec:
  ignoreDifferences:
    - group: ""
      kind: Secret
      jsonPointers:
        - /data
        - /metadata/annotations
        - /metadata/labels
```

### ESO + ArgoCD Sync-Wave 순서

ExternalSecret이 Secret을 생성한 후에야 Deployment가 참조 가능.

```yaml
# Wave -2: ExternalSecret (먼저 Secret 생성)
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-credentials
  annotations:
    argocd.argoproj.io/sync-wave: "-2"
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: ClusterSecretStore
  target:
    name: db-credentials

---
# Wave 0: Deployment (Secret이 존재해야 함)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: example-server
  annotations:
    argocd.argoproj.io/sync-wave: "0"
spec:
  template:
    spec:
      containers:
      - envFrom:
        - secretRef:
            name: db-credentials   # wave -2에서 생성됨
```

**연쇄 장애 패턴**: ESO가 Secret 생성 실패 → Deployment도 실패 → 전체 Sync 실패
- ClusterSecretStore namespace 허용 목록 관리 필수
- ESO controller 로그 확인: `kubectl logs -n external-secrets deploy/external-secrets`

### Sealed Secrets

ESO 대안. `kubeseal`로 암호화 → Git 커밋 가능한 SealedSecret 생성.

```bash
helm install sealed-secrets sealed-secrets/sealed-secrets -n kube-system
kubeseal --format yaml < secret.yaml > sealed-secret.yaml  # Git에 커밋 가능
```

---

## ECR CronJob 패턴

Kind/로컬 환경에서 ECR private registry pull을 위한 자격증명 자동 갱신.

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: ecr-credential-renew
  namespace: kube-system
spec:
  schedule: "0 */6 * * *"          # 6시간마다 (ECR 토큰 12시간 유효)
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: ecr-credential-renewer
          containers:
          - name: ecr-login
            image: amazon/aws-cli:2.22.0
            command:
            - /bin/sh
            - -c
            - |
              TOKEN=$(aws ecr get-login-password --region $AWS_REGION)
              kubectl delete secret ecr-pull-secret -n default --ignore-not-found
              kubectl create secret docker-registry ecr-pull-secret \
                -n default \
                --docker-server=$AWS_ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com \
                --docker-username=AWS \
                --docker-password=$TOKEN
            env:
            - name: AWS_REGION
              valueFrom:
                configMapKeyRef:
                  name: aws-config
                  key: region
            - name: AWS_ACCOUNT
              valueFrom:
                configMapKeyRef:
                  name: aws-config
                  key: account-id
          restartPolicy: OnFailure
```

### IAM 최소 권한

```json
{
  "Effect": "Allow",
  "Action": [
    "ecr:GetAuthorizationToken",
    "ecr:BatchGetImage",
    "ecr:GetDownloadUrlForLayer"
  ],
  "Resource": "*"
}
```

**연쇄 장애**: Secret 미갱신 → `imagePullSecrets` 만료 → ImagePullBackOff → 전체 Pod 실패

---

## AWS 환경 종속값 변수화

### Anti-pattern: 하드코딩

```yaml
# ❌ YAML에 직접 작성
image:
  repository: <account-id>.dkr.ecr.ap-northeast-2.amazonaws.com/example-server

# ❌ Makefile/스크립트에 직접 작성
AWS_ACCOUNT=<account-id>
AWS_REGION=ap-northeast-2
```

### 올바른 패턴: values로 추출

```yaml
# values.yaml (환경별로 override)
aws:
  accountId: ""        # 환경별 values에서 설정
  region: ""
  partition: "aws"     # 기본값: aws (GovCloud: aws-us-gov)

# templates/deployment.yaml
image: "{{ .Values.aws.accountId }}.dkr.ecr.{{ .Values.aws.region }}.amazonaws.com/{{ .Chart.Name }}"

# environments/dev/values.yaml
aws:
  accountId: "<account-id>"
  region: "ap-northeast-2"
```

---

### Helm Chart 버전 관리 전략

```yaml
# ArgoCD Application에서 chart 버전 고정
spec:
  source:
    chart: myapp
    targetRevision: "1.2.3"     # 정확한 버전 (~ 범위 금지)

# Renovate로 자동 업데이트 PR 생성
# renovate.json
{
  "packageRules": [
    {
      "matchDatasources": ["helm"],
      "matchPackageNames": ["kube-prometheus-stack"],
      "groupName": "monitoring",
      "schedule": ["every 2 weeks"]
    }
  ]
}
```
