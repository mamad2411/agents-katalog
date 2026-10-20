---
name: platform-backstage
category: platform
description: "Backstage Platform Engineering 가이드 — Golden Paths, Software Templates, 셀프서비스 인프라 프로비저닝 Use when working with platform 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Backstage Platform Engineering 가이드

Golden Paths, Software Templates, 셀프서비스 인프라 프로비저닝

## Quick Reference (결정 트리)

```
Platform Engineering 기능?
    │
    ├─ 서비스 생성 표준화 ────> Software Templates (Golden Paths)
    │       │
    │       └─ template.yaml + skeleton/
    │
    ├─ 인프라 셀프서비스 ────> Terraform 통합 템플릿
    │       │
    │       └─ GitOps PR 생성
    │
    └─ 조직 구조 설계 ──────> System/Domain 계층화
```

---

## CRITICAL: Platform Engineering 원칙

```
┌─────────────────────────────────────────────────────────────────┐
│               Internal Developer Platform (IDP)                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Backstage Portal                       │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐ │   │
│  │  │  Catalog    │ │  Templates  │ │     TechDocs        │ │   │
│  │  │  (검색/탐색) │ │  (생성)     │ │     (문서)          │ │   │
│  │  └─────────────┘ └─────────────┘ └─────────────────────┘ │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐ │   │
│  │  │  K8s Plugin │ │ ArgoCD      │ │   Prometheus        │ │   │
│  │  │  (운영)     │ │ (배포)      │ │   (모니터링)         │ │   │
│  │  └─────────────┘ └─────────────┘ └─────────────────────┘ │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                    ┌─────────▼─────────┐                        │
│                    │   Golden Paths    │                        │
│                    │  (표준화된 방식)   │                        │
│                    └───────────────────┘                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**핵심 가치**:
| 가치 | 설명 |
|------|------|
| **Self-Service** | 개발자가 직접 인프라 프로비저닝 |
| **Golden Paths** | 표준화된 best practice 경로 |
| **Discoverability** | 서비스/API/문서 통합 검색 |
| **Automation** | 반복 작업 자동화 |

---

## Software Templates (Golden Paths)

### 템플릿 구조

```
templates/
├── spring-boot-service/
│   ├── template.yaml        # 템플릿 정의
│   └── skeleton/            # 생성될 파일들
│       ├── catalog-info.yaml
│       ├── src/
│       ├── Dockerfile
│       ├── helm/
│       └── .github/
│           └── workflows/
└── react-app/
    ├── template.yaml
    └── skeleton/
```

### 템플릿 정의 (template.yaml)

```yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: spring-boot-service
  title: Spring Boot Service
  description: 표준 Spring Boot 마이크로서비스 생성
  tags:
    - java
    - spring-boot
    - recommended
spec:
  owner: group:team-platform
  type: service

  parameters:
    - title: 서비스 정보
      required:
        - serviceName
        - owner
      properties:
        serviceName:
          title: 서비스 이름
          type: string
          pattern: '^[a-z][a-z0-9-]*$'
        owner:
          title: 담당 팀
          type: string
          ui:field: OwnerPicker
          ui:options:
            catalogFilter:
              kind: Group

    - title: 기술 옵션
      properties:
        javaVersion:
          title: Java 버전
          type: string
          enum: ['17', '21']
          default: '21'
        database:
          title: 데이터베이스
          type: string
          enum: ['postgresql', 'mysql', 'none']
          default: 'postgresql'

    - title: 저장소 설정
      required:
        - repoUrl
      properties:
        repoUrl:
          title: 저장소 위치
          type: string
          ui:field: RepoUrlPicker
          ui:options:
            allowedHosts:
              - github.com

  steps:
    # 1. 템플릿 파일 생성
    - id: fetch-base
      name: Fetch Base Template
      action: fetch:template
      input:
        url: ./skeleton
        values:
          serviceName: ${{ parameters.serviceName }}
          owner: ${{ parameters.owner }}
          javaVersion: ${{ parameters.javaVersion }}

    # 2. GitHub 저장소 생성
    - id: publish
      name: Publish to GitHub
      action: publish:github
      input:
        allowedHosts: ['github.com']
        repoUrl: ${{ parameters.repoUrl }}
        defaultBranch: main

    # 3. 카탈로그 등록
    - id: register
      name: Register in Catalog
      action: catalog:register
      input:
        repoContentsUrl: ${{ steps['publish'].output.repoContentsUrl }}
        catalogInfoPath: '/catalog-info.yaml'

    # 4. ArgoCD 앱 생성
    - id: argocd
      name: Create ArgoCD Application
      action: argocd:create-resources
      input:
        appName: ${{ parameters.serviceName }}
        argoInstance: main
        namespace: ${{ parameters.serviceName }}
        repoUrl: ${{ steps['publish'].output.remoteUrl }}
        path: helm

  output:
    links:
      - title: Repository
        url: ${{ steps['publish'].output.remoteUrl }}
      - title: Open in Catalog
        icon: catalog
        entityRef: ${{ steps['register'].output.entityRef }}
```

### Skeleton 템플릿 파일

```yaml
# skeleton/catalog-info.yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: ${{ values.serviceName }}
  annotations:
    github.com/project-slug: my-org/${{ values.serviceName }}
    backstage.io/techdocs-ref: dir:.
spec:
  type: service
  lifecycle: experimental
  owner: ${{ values.owner }}
```

---

## 셀프서비스 인프라 프로비저닝

### Terraform 통합 템플릿

```yaml
# templates/terraform-rds/template.yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: provision-rds
  title: Provision RDS Database
  description: 셀프서비스 RDS 데이터베이스 프로비저닝
spec:
  owner: team-platform
  type: resource

  parameters:
    - title: 데이터베이스 설정
      required:
        - name
        - owner
        - environment
      properties:
        name:
          title: DB 이름
          type: string
          pattern: '^[a-z0-9-]+$'
        owner:
          title: 담당 팀
          type: string
          ui:field: OwnerPicker
        environment:
          title: 환경
          type: string
          enum:
            - dev
            - staging
            - prod
        engine:
          title: DB 엔진
          type: string
          enum:
            - postgres
            - mysql
          default: postgres
        instanceClass:
          title: 인스턴스 크기
          type: string
          enum:
            - db.t3.micro
            - db.t3.small
            - db.t3.medium
          default: db.t3.small

  steps:
    # 1. Terraform 코드 생성
    - id: fetch-terraform
      name: Generate Terraform
      action: fetch:template
      input:
        url: ./terraform
        values:
          name: ${{ parameters.name }}
          environment: ${{ parameters.environment }}
          engine: ${{ parameters.engine }}
          instanceClass: ${{ parameters.instanceClass }}

    # 2. GitOps 저장소에 PR 생성
    - id: create-pr
      name: Create PR in Infra Repo
      action: publish:github:pull-request
      input:
        repoUrl: github.com?owner=myorg&repo=terraform-infra
        branchName: provision-${{ parameters.name }}-db
        title: 'Provision RDS: ${{ parameters.name }}'
        description: |
          ## New RDS Database Request
          - **Name**: ${{ parameters.name }}
          - **Environment**: ${{ parameters.environment }}
          - **Engine**: ${{ parameters.engine }}
          - **Instance**: ${{ parameters.instanceClass }}

          Requested by: ${{ parameters.owner }}

    # 3. Backstage 리소스 등록
    - id: register
      name: Register Resource
      action: catalog:register
      input:
        catalogInfoPath: /catalog-info.yaml

  output:
    links:
      - title: Pull Request
        url: ${{ steps['create-pr'].output.remoteUrl }}
      - title: Resource in Catalog
        entityRef: ${{ steps.register.output.entityRef }}
```

---

## 고급 Catalog 구성

### 상세 Component 정의

```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: order-service
  title: Order Service
  description: 주문 처리 마이크로서비스
  annotations:
    github.com/project-slug: myorg/order-service
    argocd/app-name: order-service-prod
    backstage.io/kubernetes-id: order-service
    backstage.io/kubernetes-namespace: order
    backstage.io/techdocs-ref: dir:.
    prometheus.io/rule: "sum(rate(http_requests_total{service=\"order-service\"}[5m]))"
  tags:
    - java
    - spring-boot
    - grpc
  links:
    - url: https://grafana.example.com/d/order-service
      title: Grafana Dashboard
    - url: https://argocd.example.com/applications/order-service
      title: ArgoCD
spec:
  type: service
  lifecycle: production
  owner: team-commerce
  system: e-commerce
  dependsOn:
    - component:default/user-service
    - resource:default/order-database
  providesApis:
    - order-api
```

### System/Domain 계층 구조

```yaml
# domain.yaml
apiVersion: backstage.io/v1alpha1
kind: Domain
metadata:
  name: commerce
  title: Commerce Domain
  description: 전자상거래 비즈니스 도메인
spec:
  owner: group:commerce-leadership
---
# system.yaml
apiVersion: backstage.io/v1alpha1
kind: System
metadata:
  name: e-commerce
  title: E-Commerce Platform
  description: 전자상거래 플랫폼 시스템
spec:
  owner: team-platform
  domain: commerce
---
# api.yaml
apiVersion: backstage.io/v1alpha1
kind: API
metadata:
  name: order-api
  title: Order API
  description: 주문 관리 REST API
spec:
  type: openapi
  lifecycle: production
  owner: team-commerce
  system: e-commerce
  definition:
    $text: https://raw.githubusercontent.com/myorg/order-service/main/openapi.yaml
```

---

## TechDocs 빌드 (CI)

```yaml
# .github/workflows/techdocs.yaml
name: Publish TechDocs

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
      - 'mkdocs.yml'

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install mkdocs-techdocs-core

      - name: Build TechDocs
        run: mkdocs build --strict

      - name: Publish to S3
        run: |
          aws s3 sync ./site s3://techdocs-bucket/default/component/order-service/
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| Catalog 미등록 | 서비스 검색 불가 | CI에서 catalog-info.yaml 검증 |
| 템플릿 과복잡 | 사용자 혼란 | 필수 옵션만 최소화 |
| TechDocs 미작성 | 문서 없는 서비스 | 템플릿에 기본 문서 포함 |
| Golden Path 없음 | 일관성 부재 | 표준 템플릿 제공 |
| 수동 인프라 요청 | 프로비저닝 지연 | 셀프서비스 템플릿 |

---

## 체크리스트

### Software Templates
- [ ] Golden Path 템플릿 작성
- [ ] 언어/프레임워크별 템플릿
- [ ] 인프라 프로비저닝 템플릿
- [ ] GitOps 통합 (ArgoCD)

### Catalog 구성
- [ ] catalog-info.yaml 표준 정의
- [ ] System/Domain 계층 구조 설계
- [ ] API 스펙 등록 (OpenAPI)
- [ ] Team/Owner 매핑

### TechDocs
- [ ] mkdocs.yml 표준 설정
- [ ] CI에서 TechDocs 빌드
- [ ] S3/GCS 스토리지 연결

**관련 skill**: `/backstage` (기본 설치), `/golden-paths`, `/gitops-argocd`
