---
name: ephemeral-environments
category: cicd
description: "Ephemeral Environments 가이드 — PR별 프리뷰 환경: Argo CD ApplicationSet, Qovery, Namespace 격리 패턴 Use when working with cicd 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Ephemeral Environments 가이드

PR별 프리뷰 환경: Argo CD ApplicationSet, Qovery, Namespace 격리 패턴

## Quick Reference (결정 트리)

```
Ephemeral 환경 구현 방식?
    |
    +-- GitOps 기반 ----------------> Argo CD ApplicationSet
    |       |
    |       +-- PR Generator -------> GitHub/GitLab PR 연동
    |       +-- Matrix Generator ---> 멀티 환경 조합
    |
    +-- 플랫폼 서비스 --------------> Qovery / Bunnyshell
    |       |
    |       +-- 완전 관리형 ---------> Qovery (AWS/GCP)
    |       +-- Kubernetes 네이티브 -> Bunnyshell
    |
    +-- 순수 Kubernetes ------------> Namespace 격리
            |
            +-- 단순 격리 -----------> Namespace + NetworkPolicy
            +-- vCluster ------------> 가상 클러스터 격리

환경 수명 주기?
    |
    +-- PR Merge 시 삭제 -----------> 자동 정리 필수
    +-- TTL 기반 삭제 --------------> 시간 제한 (24h, 7d)
    +-- 수동 삭제 ------------------> 개발자 요청 시
```

---

## CRITICAL: Static vs Ephemeral 환경 비교

| 항목 | Static 환경 | Ephemeral 환경 |
|------|------------|---------------|
| **수명** | 영구적 | PR/브랜치 기반 |
| **비용** | 고정 (24/7 운영) | 사용 시간만 |
| **격리** | 환경 간 공유 | 완전 격리 |
| **충돌** | 동시 개발 충돌 | 충돌 없음 |
| **테스트** | 큐 대기 필요 | 병렬 테스트 |
| **피드백** | 느림 | PR에서 즉시 확인 |

### 비용 절감 효과

```
Static 환경 (3개: dev, staging, qa)
    |
    +-- 24/7 운영: 월 $3,000
    +-- 사용률: 평균 30%
    +-- 유휴 비용: 월 $2,100 낭비

Ephemeral 환경
    |
    +-- PR당 평균 8시간 운영
    +-- 월 100 PR 기준: 800시간
    +-- 비용: 월 $400-600 (85-90% 절감!)
```

---

## Argo CD ApplicationSet (PR Generator)

### 아키텍처

```
GitHub PR Open
    |
    v
+------------------+
| ApplicationSet   |
| (PR Generator)   |
+------------------+
    |
    +-- PR #123 --> Application: preview-123
    +-- PR #456 --> Application: preview-456
    +-- PR #789 --> Application: preview-789
    |
    v
+------------------+
| Namespace:       |
| preview-pr-123   |
+------------------+
    |
    +-- Deployment
    +-- Service
    +-- Ingress: pr-123.preview.example.com
```

### ApplicationSet 정의

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: pr-preview
  namespace: argocd
spec:
  goTemplate: true
  goTemplateOptions: ["missingkey=error"]

  generators:
    # Pull Request Generator
    - pullRequest:
        github:
          owner: myorg
          repo: myapp
          tokenRef:
            secretName: github-token
            key: token
          labels:
            - preview  # 'preview' 라벨이 있는 PR만
        requeueAfterSeconds: 60  # 1분마다 동기화

  template:
    metadata:
      name: 'preview-{{.number}}'
      namespace: argocd
      labels:
        app.kubernetes.io/name: 'preview-{{.number}}'
        preview: "true"
      annotations:
        # PR 정보
        github.com/pr-number: '{{.number}}'
        github.com/pr-title: '{{.title}}'
        github.com/pr-author: '{{.author}}'
      finalizers:
        - resources-finalizer.argocd.argoproj.io
    spec:
      project: preview-environments

      source:
        repoURL: https://github.com/myorg/myapp.git
        targetRevision: '{{.head_sha}}'  # PR의 head commit
        path: k8s/overlays/preview
        kustomize:
          namePrefix: 'pr-{{.number}}-'
          commonLabels:
            pr-number: '{{.number}}'
          images:
            - 'myapp=ghcr.io/myorg/myapp:pr-{{.number}}'

      destination:
        server: https://kubernetes.default.svc
        namespace: 'preview-pr-{{.number}}'

      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
          - CreateNamespace=true
          - PruneLast=true
        retry:
          limit: 3
          backoff:
            duration: 5s
            factor: 2
            maxDuration: 1m
```

### AppProject (권한 격리)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: preview-environments
  namespace: argocd
spec:
  description: "Preview environments for PRs"

  # 소스 제한
  sourceRepos:
    - https://github.com/myorg/myapp.git

  # 대상 제한
  destinations:
    - namespace: 'preview-*'
      server: https://kubernetes.default.svc

  # 허용된 리소스
  clusterResourceWhitelist:
    - group: ''
      kind: Namespace

  namespaceResourceWhitelist:
    - group: ''
      kind: '*'
    - group: apps
      kind: '*'
    - group: networking.k8s.io
      kind: '*'

  # 금지된 리소스
  namespaceResourceBlacklist:
    - group: ''
      kind: ResourceQuota
    - group: ''
      kind: LimitRange
```

### Preview URL 설정

```yaml
# k8s/overlays/preview/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: preview
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - "*.preview.example.com"
      secretName: preview-wildcard-tls
  rules:
    - host: "$(PR_NUMBER).preview.example.com"
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: myapp
                port:
                  number: 8080
```

### GitHub Actions 연동

```yaml
# .github/workflows/preview.yaml
name: Preview Environment

on:
  pull_request:
    types: [opened, synchronize, labeled]

jobs:
  build:
    if: contains(github.event.pull_request.labels.*.name, 'preview')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build and Push Image
        run: |
          docker build -t ghcr.io/${{ github.repository }}:pr-${{ github.event.pull_request.number }} .
          docker push ghcr.io/${{ github.repository }}:pr-${{ github.event.pull_request.number }}

      - name: Comment Preview URL
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## Preview Environment

              Your preview is being deployed!

              **URL:** https://pr-${{ github.event.pull_request.number }}.preview.example.com

              _Deployment typically takes 2-3 minutes._`
            })
```

---

## Namespace 격리 패턴

### 동적 Namespace 생성

```yaml
# namespace-template.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: preview-pr-${PR_NUMBER}
  labels:
    environment: preview
    pr-number: "${PR_NUMBER}"
    created-at: "${TIMESTAMP}"
  annotations:
    # TTL 기반 자동 삭제 (Kyverno와 연동)
    cleanup.kyverno.io/ttl: "168h"  # 7일
---
# ResourceQuota (리소스 제한)
apiVersion: v1
kind: ResourceQuota
metadata:
  name: preview-quota
  namespace: preview-pr-${PR_NUMBER}
spec:
  hard:
    requests.cpu: "2"
    requests.memory: 4Gi
    limits.cpu: "4"
    limits.memory: 8Gi
    persistentvolumeclaims: "5"
    services.loadbalancers: "0"  # LB 금지
---
# LimitRange (기본 리소스)
apiVersion: v1
kind: LimitRange
metadata:
  name: preview-limits
  namespace: preview-pr-${PR_NUMBER}
spec:
  limits:
    - default:
        cpu: 200m
        memory: 256Mi
      defaultRequest:
        cpu: 100m
        memory: 128Mi
      type: Container
```

### NetworkPolicy 격리

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: preview-isolation
  namespace: preview-pr-${PR_NUMBER}
spec:
  podSelector: {}  # 모든 Pod에 적용
  policyTypes:
    - Ingress
    - Egress

  ingress:
    # Ingress Controller에서만 트래픽 허용
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
      ports:
        - protocol: TCP
          port: 8080
    # 같은 네임스페이스 내 통신 허용
    - from:
        - podSelector: {}

  egress:
    # DNS 허용
    - to:
        - namespaceSelector: {}
          podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - protocol: UDP
          port: 53
    # 같은 네임스페이스 내 통신 허용
    - to:
        - podSelector: {}
    # 외부 API 허용 (선택적)
    - to:
        - ipBlock:
            cidr: 0.0.0.0/0
            except:
              - 10.0.0.0/8
              - 172.16.0.0/12
              - 192.168.0.0/16
      ports:
        - protocol: TCP
          port: 443
```

---

## Kyverno 자동 정리

### TTL 기반 삭제

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: cleanup-preview-namespaces
spec:
  rules:
    - name: add-ttl-label
      match:
        any:
          - resources:
              kinds:
                - Namespace
              selector:
                matchLabels:
                  environment: preview
      mutate:
        patchStrategicMerge:
          metadata:
            labels:
              cleanup.kyverno.io/ttl: "168h"  # 7일 후 삭제
---
# Kyverno Cleanup Controller 설정
apiVersion: kyverno.io/v2alpha1
kind: CleanupPolicy
metadata:
  name: cleanup-old-previews
spec:
  match:
    any:
      - resources:
          kinds:
            - Namespace
          selector:
            matchLabels:
              environment: preview
  conditions:
    any:
      # created-at이 7일 이전인 경우
      - key: "{{ time_since('', '{{request.object.metadata.creationTimestamp}}', '') }}"
        operator: GreaterThan
        value: "168h"
  schedule: "0 */6 * * *"  # 6시간마다 실행
```

### PR Merge 시 삭제

```yaml
# .github/workflows/cleanup-preview.yaml
name: Cleanup Preview Environment

on:
  pull_request:
    types: [closed]

jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - name: Delete Preview Namespace
        run: |
          kubectl delete namespace preview-pr-${{ github.event.pull_request.number }} \
            --ignore-not-found=true

      - name: Delete ArgoCD Application
        run: |
          kubectl delete application preview-${{ github.event.pull_request.number }} \
            -n argocd --ignore-not-found=true
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 자동 삭제 미설정 | 리소스 누수 | TTL 또는 PR 연동 삭제 |
| 프로덕션 DB 연결 | 데이터 오염 | 격리된 DB 사용 |
| 리소스 제한 없음 | 비용 폭증 | ResourceQuota 설정 |
| 네트워크 격리 없음 | 보안 위험 | NetworkPolicy 적용 |
| 모든 PR에 환경 생성 | 불필요한 비용 | 라벨 기반 필터링 |

---

## 체크리스트

### ApplicationSet 설정
- [ ] PR Generator 설정
- [ ] GitHub/GitLab 토큰 설정
- [ ] AppProject 권한 제한
- [ ] Preview URL 패턴 정의

### Namespace 격리
- [ ] ResourceQuota 설정
- [ ] LimitRange 설정
- [ ] NetworkPolicy 적용

### 자동화
- [ ] PR Merge 시 삭제 워크플로우
- [ ] TTL 기반 정리 정책
- [ ] Preview URL PR 코멘트

## 참조 스킬

- `/ephemeral-environments-advanced` - Qovery, 데이터베이스 전략, 비용 최적화
- `/gitops-argocd` - ArgoCD GitOps
- `/finops` - FinOps 기초
