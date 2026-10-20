---
name: developer-self-service
category: platform
description: "개발자 셀프서비스 플랫폼 가이드 — 개발자가 티켓 없이 환경 프로비저닝, 서비스 생성, DB/시크릿/도메인을 셀프서비스하는 플랫폼 구축 Use when working with platform 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# 개발자 셀프서비스 플랫폼 가이드

개발자가 티켓 없이 환경 프로비저닝, 서비스 생성, DB/시크릿/도메인을 셀프서비스하는 플랫폼 구축

## Quick Reference (결정 트리)

```
셀프서비스 유형?
    ├─ 서비스 생성 ──────> "make new-service" (Cookiecutter/Backstage)
    ├─ 인프라 프로비저닝 ─> Crossplane Claim (DB/Redis/S3)
    ├─ 환경 관리 ────────> Namespace-as-a-Service
    ├─ 도메인/DNS ───────> ExternalDNS 자동 할당
    └─ 시크릿 관리 ──────> Vault / External Secrets

팀 규모별 도구 선택:
  < 10명  → Makefile + Scripts (CLI: make new-service)
  10-50명 → Backstage Templates (포탈 UI + CLI)
  50-200명 → Backstage + Crossplane (포탈 + GitOps)
  200명+  → Port/Backstage + AI Agent (자연어 요청)
```

---

## 1. 셀프서비스 성숙도 모델

```
Level 0: 티켓 기반 → Jira 티켓 → Ops 수동 처리 (3-5일)
Level 1: 템플릿 기반 → Cookiecutter CLI scaffolding (1일)
Level 2: 포탈 기반 → Backstage/Port UI 원클릭 (30분)
Level 3: AI 자동화 → "결제 서비스 필요" → AI가 Golden Path 프로비저닝 (5분)
```

| 지표 | L0 | L1 | L2 | L3 |
|------|----|----|----|----|
| Time-to-First-Deploy | 5일 | 1일 | 30분 | 5분 |
| Ops 티켓/주 | 50+ | 20 | 5 | 0 |

---

## 2. "make new-service" 원커맨드 서비스 생성

```makefile
.PHONY: new-service new-env new-db new-cache
new-service: ## make new-service NAME=payment-api TYPE=spring TEAM=commerce
	@./scripts/create-service.sh --name $(NAME) --type $(or $(TYPE),spring) --team $(or $(TEAM),default)
new-env: ## make new-env NAME=feature-x TTL=72h
	@./scripts/create-namespace.sh --name $(NAME) --ttl $(or $(TTL),72h)
new-db: ## make new-db NAME=payment-db ENGINE=postgres SIZE=small
	@./scripts/create-database.sh --name $(NAME) --engine $(or $(ENGINE),postgres) --size $(or $(SIZE),small)
new-cache: ## make new-cache NAME=payment-cache SIZE=small
	@./scripts/create-cache.sh --name $(NAME) --size $(or $(SIZE),small)
```

### create-service.sh 핵심 흐름

```bash
#!/bin/bash
set -euo pipefail
# 1) Scaffolding
cookiecutter gh:company/service-templates/$TYPE --no-input service_name=$NAME team_name=$TEAM
# 2) Git repo 생성 + push
gh repo create "company/$NAME" --private --source=./$NAME --push
# 3) CI/CD 파이프라인 복사
cp platform/ci-templates/$TYPE.github-actions.yml ./$NAME/.github/workflows/ci.yml
# 4) Namespace + ResourceQuota
kubectl apply -f - <<EOF
apiVersion: v1
kind: Namespace
metadata:
  name: $NAME
  labels: { team: $TEAM, managed-by: platform, cost-center: $TEAM }
---
apiVersion: v1
kind: ResourceQuota
metadata: { name: default-quota, namespace: $NAME }
spec:
  hard: { requests.cpu: "4", requests.memory: 8Gi, limits.cpu: "8", limits.memory: 16Gi }
EOF
# 5) ArgoCD Application 등록
kubectl apply -f - <<EOF
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata: { name: $NAME, namespace: argocd, labels: { team: $TEAM } }
spec:
  project: $TEAM
  source: { repoURL: "https://github.com/company/$NAME", targetRevision: main, path: k8s/overlays/dev }
  destination: { server: "https://kubernetes.default.svc", namespace: $NAME }
  syncPolicy: { automated: { prune: true, selfHeal: true }, syncOptions: [CreateNamespace=true] }
EOF
# 6) ServiceMonitor 등록
kubectl apply -f - <<EOF
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata: { name: $NAME, namespace: $NAME }
spec:
  selector: { matchLabels: { app: $NAME } }
  endpoints: [{ port: metrics, interval: 15s }]
EOF
# 7) Backstage catalog-info.yaml 생성 (repo 안에 포함)
echo "Done: https://backstage.internal/catalog/default/component/$NAME"
```

---

## 3. 환경 프로비저닝 셀프서비스 (Crossplane)

### CompositeResourceDefinition (Database)

```yaml
apiVersion: apiextensions.crossplane.io/v1
kind: CompositeResourceDefinition
metadata:
  name: xdatabases.platform.company.io
spec:
  group: platform.company.io
  names: { kind: XDatabase, plural: xdatabases }
  claimNames: { kind: DatabaseClaim, plural: databaseclaims }
  versions:
    - name: v1alpha1
      served: true
      referenceable: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                engine: { type: string, enum: [postgres, mysql], default: postgres }
                size: { type: string, enum: [small, medium, large], default: small }
                team: { type: string }
              required: [engine, size, team]
```

### Composition (size -> instanceClass 매핑)

```yaml
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata: { name: database-postgres, labels: { engine: postgres } }
spec:
  compositeTypeRef: { apiVersion: platform.company.io/v1alpha1, kind: XDatabase }
  resources:
    - name: rds-instance
      base:
        apiVersion: rds.aws.upbound.io/v1beta1
        kind: Instance
        spec:
          forProvider:
            engine: postgres
            engineVersion: "16"
            instanceClass: db.t3.micro
            allocatedStorage: 20
            skipFinalSnapshot: true
            publiclyAccessible: false
      patches:
        - type: FromCompositeFieldPath
          fromFieldPath: spec.size
          toFieldPath: spec.forProvider.instanceClass
          transforms:
            - type: map
              map: { small: db.t3.micro, medium: db.r6g.large, large: db.r6g.xlarge }
```

### 개발자가 작성하는 전부 (Claim)

```yaml
# DB 요청
apiVersion: platform.company.io/v1alpha1
kind: DatabaseClaim
metadata: { name: payment-db, namespace: payment-team }
spec: { engine: postgres, size: small, team: payment }
---
# Redis 요청
apiVersion: platform.company.io/v1alpha1
kind: CacheClaim
metadata: { name: payment-cache, namespace: payment-team }
spec: { engine: redis, size: small, team: payment }
---
# S3 요청
apiVersion: platform.company.io/v1alpha1
kind: BucketClaim
metadata: { name: payment-uploads, namespace: payment-team }
spec: { region: ap-northeast-2, versioning: true, encryption: true, team: payment }
```

---

## 4. Backstage Software Templates 실전 예제

```yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: new-spring-service
  title: Spring Boot 서비스 생성
  description: Golden Path 기반 Spring Boot 서비스 (Git + CI/CD + NS + 모니터링 자동 설정)
  tags: [spring, java, recommended]
spec:
  owner: platform-team
  type: service
  parameters:
    - title: 서비스 기본 정보
      required: [name, team]
      properties:
        name: { title: 서비스 이름, type: string, pattern: '^[a-z][a-z0-9-]*$' }
        team: { title: 소유 팀, type: string, ui:field: OwnerPicker }
    - title: 기술 옵션
      properties:
        database: { type: string, enum: [none, postgres, mysql], default: postgres }
        cache: { type: string, enum: [none, redis], default: none }
  steps:
    - id: fetch-template
      name: 코드 생성
      action: fetch:template
      input: { url: ./skeleton, values: { name: "${{ parameters.name }}", team: "${{ parameters.team }}" } }
    - id: publish
      name: GitHub Repo 생성
      action: publish:github
      input:
        repoUrl: "github.com?owner=company&repo=${{ parameters.name }}"
        defaultBranch: main
        repoVisibility: internal
    - id: create-namespace
      name: Namespace 생성
      action: kubernetes:apply
      input:
        manifest:
          apiVersion: v1
          kind: Namespace
          metadata: { name: "${{ parameters.name }}", labels: { team: "${{ parameters.team }}" } }
    - id: create-database
      name: DB 프로비저닝
      if: "${{ parameters.database !== 'none' }}"
      action: kubernetes:apply
      input:
        manifest:
          apiVersion: platform.company.io/v1alpha1
          kind: DatabaseClaim
          metadata: { name: "${{ parameters.name }}-db", namespace: "${{ parameters.name }}" }
          spec: { engine: "${{ parameters.database }}", size: small, team: "${{ parameters.team }}" }
    - id: create-argocd-app
      name: ArgoCD 등록
      action: argocd:create-resources
      input: { appName: "${{ parameters.name }}", repoUrl: "${{ steps.publish.output.remoteUrl }}", path: k8s/overlays/dev }
    - id: register
      name: 카탈로그 등록
      action: catalog:register
      input: { repoContentsUrl: "${{ steps.publish.output.repoContentsUrl }}", catalogInfoPath: /catalog-info.yaml }
  output:
    links:
      - { title: Repository, url: "${{ steps.publish.output.remoteUrl }}" }
      - { title: Backstage, icon: catalog, entityRef: "${{ steps.register.output.entityRef }}" }
```

---

## 5. Port Self-Service Actions 비교

| 항목 | Backstage | Port |
|------|-----------|------|
| 설치 방식 | 셀프호스팅 (React+Node) | SaaS 관리형 |
| 셀프서비스 | Scaffolder Templates | Self-Service Actions |
| 백엔드 연동 | Custom Actions 플러그인 | GitHub Actions/Webhook |
| 데이터 모델 | 고정 (Component, API 등) | Blueprint 커스텀 |
| 비용 | 무료 (운영비 별도) | 유료 (무료 티어 있음) |
| 적합 | 대규모 + 커스터마이징 | 빠른 도입 + 유연 모델링 |

Port Self-Service Action은 JSON으로 `trigger.userInputs`에 서비스명/언어 등 입력 정의, `invocationMethod`로 GitHub Actions workflow 연동. Backstage Scaffolder 대비 설정이 단순하나 SaaS 종속.

---

## 6. DNS/도메인 자동 할당

```yaml
# Ingress 생성 시 ExternalDNS가 자동으로 DNS 레코드 생성
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: payment-api
  namespace: payment-team
  annotations:
    external-dns.alpha.kubernetes.io/hostname: payment-api.dev.company.io
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
  tls:
    - hosts: [payment-api.dev.company.io]
      secretName: payment-api-tls
  rules:
    - host: payment-api.dev.company.io
      http:
        paths:
          - { path: /, pathType: Prefix, backend: { service: { name: payment-api, port: { number: 8080 } } } }
```

**도메인 네이밍 컨벤션**: `{service}.{env}.company.io` / PR 환경: `{service}.pr-{num}.dev.company.io`

---

## 7. 셀프서비스 워크플로우 (GitHub Actions + ArgoCD)

```yaml
# .github/workflows/create-service.yml
name: Create New Service
on:
  workflow_dispatch:
    inputs:
      service_name: { description: '서비스 이름', required: true }
      type: { description: '서비스 타입', required: true, type: choice, options: [spring, go, react] }
      team: { description: '소유 팀', required: true }
jobs:
  create:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Scaffold + Repo + Deploy
        env: { GH_TOKEN: "${{ secrets.ORG_TOKEN }}" }
        run: |
          cookiecutter templates/${{ inputs.type }} --no-input service_name=${{ inputs.service_name }} team=${{ inputs.team }}
          gh repo create company/${{ inputs.service_name }} --private --source=./${{ inputs.service_name }} --push
      - name: Apply K8s resources
        uses: azure/k8s-deploy@v5
        with: { manifests: "k8s/namespace.yaml\nk8s/argocd-app.yaml\nk8s/resource-quota.yaml" }
      - name: Notify
        uses: slackapi/slack-github-action@v2.0.0
        with:
          payload: '{"text":"새 서비스: ${{ inputs.service_name }} (팀: ${{ inputs.team }})"}'
```

### ArgoCD ApplicationSet (자동 감지)

`teams/*/services/*` 디렉토리 구조에서 자동으로 Application 생성. Git generator로 `path[1]`=팀, `path[3]`=서비스명 매핑. `syncPolicy.automated`로 prune + selfHeal 활성화.

---

## 8. RBAC & 가드레일

```yaml
# Kyverno: namespace에 team/cost-center label 필수 + ResourceQuota 자동 주입
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata: { name: require-team-label }
spec:
  validationFailureAction: Enforce
  rules:
    - name: check-team-label
      match: { any: [{ resources: { kinds: [Namespace] } }] }
      validate:
        message: "team, cost-center label 필수"
        pattern: { metadata: { labels: { team: "?*", cost-center: "?*" } } }
---
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata: { name: inject-resource-quota }
spec:
  rules:
    - name: add-default-quota
      match: { any: [{ resources: { kinds: [Namespace], selector: { matchLabels: { managed-by: platform } } } }] }
      generate:
        kind: ResourceQuota
        apiVersion: v1
        name: default-quota
        namespace: "{{request.object.metadata.name}}"
        data: { spec: { hard: { requests.cpu: "4", requests.memory: 8Gi, limits.cpu: "8", limits.memory: 16Gi } } }
```

**권한 매트릭스**:

| 역할 | namespace | DB | Cache | Bucket | 제약 |
|------|-----------|-----|-------|--------|------|
| developer | 생성 (최대 5개) | small/medium | small | 최대 3개 | 팀 접두사 필수 |
| tech-lead | 생성/삭제 (최대 10개) | large까지 | medium | 제한 없음 | 팀 범위 내 |
| platform-admin | 모든 권한 | 모든 권한 | 모든 권한 | 모든 권한 | 없음 |

---

## 9. 비용 제어

**리소스 쿼터 티어**: small(2CPU/4Gi ~$50/월) | medium(4CPU/8Gi ~$150/월) | large(8CPU/16Gi ~$400/월)

```yaml
# TTL CronJob: 매일 새벽 2시, 만료된 개발 namespace 자동 삭제
apiVersion: batch/v1
kind: CronJob
metadata: { name: cleanup-expired-ns, namespace: platform-system }
spec:
  schedule: "0 2 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: cleanup
              image: bitnami/kubectl:latest
              command: ["/bin/sh", "-c"]
              args: ["kubectl get ns -l managed-by=platform -o json | jq -r '.items[] | select(.metadata.annotations[\"platform.company.io/ttl-expires\"] // \"\" | if . != \"\" then (. | fromdateiso8601) < now else false end) | .metadata.name' | xargs -I{} kubectl delete ns {}"]
          restartPolicy: OnFailure
```

**비용 태깅**: Kyverno mutate로 모든 Deployment/StatefulSet에 `cost-center: {{request.namespace}}` 자동 주입

---

## 10. 측정 지표 (Platform KPI)

```
핵심 메트릭:
  platform_service_creation_duration_seconds  - 서비스 생성 소요 시간 (Target: < 30분)
  platform_provisioning_lead_time_seconds     - 프로비저닝 리드 타임 (Target: < 5분)
  platform_selfservice_adoption_ratio         - 셀프서비스 채택률 (Target: > 80%)
  platform_ops_ticket_count_total             - Ops 티켓 수 (Target: 주 5건 이하)
  platform_developer_nps                      - 개발자 만족도 NPS (Target: > 40)
  platform_resource_cost_dollars              - 팀별 리소스 비용
```

---

## 11. Anti-Patterns

| Anti-Pattern | 문제 | 해결책 |
|-------------|------|--------|
| Shadow IT | 플랫폼 우회하여 직접 인프라 생성 | Golden Path를 매력적으로 (강제 X, 유인 O) |
| 무제한 셀프서비스 | 비용 폭증, 좀비 인프라 | 쿼터 + TTL + 자동 정리 |
| 문서 없는 셀프서비스 | 사용법 모름, 티켓 재발생 | Backstage TechDocs, 인라인 도움말 |
| One-Size-Fits-All | 모든 팀에 동일 템플릿 강제 | 기본 템플릿 + 팀별 커스터마이징 |
| 메트릭 없는 플랫폼 | 개선/가치 증명 불가 | DORA + Platform KPI 필수 |

**출시 전 체크리스트**: RBAC 적용, 리소스 쿼터 설정, TTL 정책, 비용 태깅, 모니터링 자동설정, 문서 통합, Rollback 절차, 에스컬레이션 경로

---

## 12. Go + Spring 개발자 관점 예제

### Spring Boot 개발자

```bash
make new-service NAME=order-api TYPE=spring TEAM=commerce  # 서비스 생성
make new-db NAME=order-db ENGINE=postgres                   # DB 추가
cd order-api && ./gradlew bootRun                           # 로컬 개발
git push origin main                                        # 배포 (ArgoCD 자동 감지)
# 결과: https://order-api.dev.company.io 자동 생성
```

### Go 개발자

```bash
make new-service NAME=notification-worker TYPE=go TEAM=platform
make new-cache NAME=notification-cache                      # Redis 추가
# 생성된 구조:
# cmd/server/main.go, internal/{handler,service}/, Dockerfile,
# k8s/{base,overlays/dev}/, .github/workflows/ci.yml, catalog-info.yaml
```

### Backstage UI 워크플로우

```
backstage.internal → Create → "Spring Boot 서비스 생성" 선택
→ 폼: 이름(order-api), 팀(commerce), DB(postgres), 캐시(redis)
→ Create 클릭 → 실시간 진행:
  ✅ 코드 생성 → ✅ GitHub repo → ✅ Namespace → ✅ DB(2분) → ✅ ArgoCD → ✅ 카탈로그
→ 링크 클릭 → 바로 개발 시작
```

---

## 13. 구현 로드맵

| Phase | 기간 | 내용 |
|-------|------|------|
| 1 | 1-2주 | Makefile + create-service.sh + Cookiecutter 템플릿 |
| 2 | 3-4주 | Crossplane Compositions (DB/Cache/Bucket Claims) |
| 3 | 5-6주 | Backstage Templates + Kyverno 정책 + RBAC |
| 4 | 7-8주 | Platform KPI 대시보드 + 비용 태깅 + 피드백 루프 |

---

## 관련 Skills

- `/backstage` - Developer Portal 구축 상세
- `/golden-paths` - Golden Path 템플릿 설계
- `/crossplane` - Crossplane Composition 상세
- `/ephemeral-environments` - PR별 임시 환경
- `/dx-onboarding` - 개발자 온보딩 자동화
- `/finops` - 비용 최적화 전략
- `/gitops-argocd` - ArgoCD GitOps 배포
