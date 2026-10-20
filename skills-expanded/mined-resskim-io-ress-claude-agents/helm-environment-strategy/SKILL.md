---
name: helm-environment-strategy
category: infrastructure
description: "Helm & Kustomize 환경별 변수화 전략 — 환경별(dev/staging/prod) 설정 분리, Helm values overlay, Kustomize overlay 패턴 Use when working with infrastructure 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Helm & Kustomize 환경별 변수화 전략

환경별(dev/staging/prod) 설정 분리, Helm values overlay, Kustomize overlay 패턴

## Quick Reference (결정 트리)

```
환경별 설정 관리?
    │
    ├─ Helm 사용 ───────────> Values Overlay 패턴
    │     │
    │     ├─ 단순 override ──> values-{env}.yaml
    │     └─ 복잡한 구조 ───> Umbrella Chart + subcharts
    │
    ├─ Kustomize 사용 ──────> Overlay 패턴
    │     │
    │     ├─ base/ + overlays/{env}/
    │     └─ components/ (재사용 가능한 조각)
    │
    └─ ArgoCD 연동 ─────────> ApplicationSet + values override
          │
          ├─ Git Generator ──> 브랜치/디렉토리별 환경
          └─ List Generator ─> 명시적 환경 목록
```

---

## Helm Values Overlay 패턴

### 디렉토리 구조

```
charts/
├── my-app/
│   ├── Chart.yaml
│   ├── values.yaml                 # 기본값 (가장 안전한 설정)
│   ├── values-dev.yaml             # kind/로컬
│   ├── values-staging.yaml         # staging
│   ├── values-prod.yaml            # production
│   └── templates/
│       ├── _helpers.tpl
│       ├── deployment.yaml
│       ├── service.yaml
│       ├── ingress.yaml
│       ├── hpa.yaml
│       ├── pdb.yaml
│       ├── configmap.yaml
│       ├── serviceaccount.yaml
│       └── servicemonitor.yaml
└── infra/                          # 인프라 차트 (모니터링, 로깅 등)
    ├── monitoring/
    │   ├── Chart.yaml
    │   ├── values.yaml
    │   ├── values-dev.yaml
    │   └── values-prod.yaml
    └── logging/
        └── ...
```

### values.yaml 설계 원칙

```yaml
# values.yaml — 모든 환경의 기본값
# 원칙: 가장 제한적이고 안전한 값으로 설정

global:
  environment: dev               # override 대상
  clusterName: my-cluster
  domain: dev.example.com        # override 대상

image:
  repository: myapp
  tag: latest                    # CI에서 override
  pullPolicy: IfNotPresent

replicaCount: 1                  # prod에서 override

resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 256Mi

# --- Feature Flags (기본: 비활성화) ---
hpa:
  enabled: false
  minReplicas: 1
  maxReplicas: 3
  targetCPU: 80

pdb:
  enabled: false
  minAvailable: 1

ingress:
  enabled: true
  className: nginx               # override 대상
  tls:
    enabled: false               # prod에서 true
  annotations: {}                # override 대상

# --- 모니터링 ---
monitoring:
  serviceMonitor:
    enabled: true
    interval: 30s
  metricsPort: 8080

logging:
  level: info                    # dev에서 debug override 가능
  format: json

tracing:
  enabled: false                 # Phase 1부터 true
  sampleRate: 1.0                # prod에서 0.01~0.1

# --- 외부 서비스 (환경별 엔드포인트) ---
database:
  host: localhost
  port: 5432
  name: myapp
  # password는 Secret으로 관리 — values에 절대 넣지 않음

redis:
  host: localhost
  port: 6379

kafka:
  brokers: "localhost:9092"
  # MSK 전환 시 endpoint만 변경

# --- 시크릿 관리 ---
secrets:
  backend: k8s-secret            # k8s-secret | external-secrets | vault
  externalSecrets:
    refreshInterval: 1h
    secretStore: aws-secretsmanager
```

### 환경별 Override

```yaml
# values-dev.yaml (kind 환경 — 최소한의 override만)
global:
  environment: dev

logging:
  level: debug

tracing:
  enabled: true
  sampleRate: 1.0    # dev는 모든 trace 수집

resources:
  requests:
    cpu: 50m
    memory: 64Mi
  limits:
    cpu: 200m
    memory: 128Mi
```

```yaml
# values-staging.yaml
global:
  environment: staging
  domain: staging.example.com

replicaCount: 2

resources:
  requests:
    cpu: 250m
    memory: 256Mi
  limits:
    cpu: 1000m
    memory: 512Mi

hpa:
  enabled: true
  minReplicas: 2
  maxReplicas: 5

ingress:
  className: nginx
  tls:
    enabled: true

database:
  host: staging-db.internal
  name: myapp_staging

tracing:
  enabled: true
  sampleRate: 0.5
```

```yaml
# values-prod.yaml
global:
  environment: prod
  domain: example.com

replicaCount: 3

image:
  pullPolicy: Always

resources:
  requests:
    cpu: 500m
    memory: 512Mi
  limits:
    cpu: 2000m
    memory: 2Gi

hpa:
  enabled: true
  minReplicas: 3
  maxReplicas: 50
  targetCPU: 70

pdb:
  enabled: true
  minAvailable: 2

ingress:
  className: alb
  tls:
    enabled: true
  annotations:
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip

database:
  host: prod-db.cluster-xxx.ap-northeast-2.rds.amazonaws.com
  name: myapp_prod

redis:
  host: prod-redis.xxx.apne2.cache.amazonaws.com

kafka:
  brokers: "b-1.msk-prod.xxx.kafka.ap-northeast-2.amazonaws.com:9092"

tracing:
  sampleRate: 0.01

secrets:
  backend: external-secrets
```

### Helm 설치 명령

```bash
# dev (kind)
helm upgrade --install myapp ./charts/my-app \
  -f charts/my-app/values.yaml \
  -f charts/my-app/values-dev.yaml \
  -n myapp --create-namespace

# prod
helm upgrade --install myapp ./charts/my-app \
  -f charts/my-app/values.yaml \
  -f charts/my-app/values-prod.yaml \
  --set image.tag=${GIT_SHA} \
  -n myapp --create-namespace
```

---

## Kustomize Overlay 패턴

### 디렉토리 구조

```
k8s/
├── base/
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   └── configmap.yaml
├── components/                    # 재사용 가능한 조각
│   ├── monitoring/
│   │   ├── kustomization.yaml
│   │   └── servicemonitor.yaml
│   ├── hpa/
│   │   ├── kustomization.yaml
│   │   └── hpa.yaml
│   └── pdb/
│       ├── kustomization.yaml
│       └── pdb.yaml
└── overlays/
    ├── dev/
    │   ├── kustomization.yaml
    │   └── patches/
    │       └── deployment-resources.yaml
    ├── staging/
    │   ├── kustomization.yaml
    │   └── patches/
    │       ├── deployment-resources.yaml
    │       └── ingress-tls.yaml
    └── prod/
        ├── kustomization.yaml
        └── patches/
            ├── deployment-resources.yaml
            ├── deployment-replicas.yaml
            └── ingress-alb.yaml
```

### Overlay 예시

```yaml
# overlays/prod/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: myapp-prod

resources:
  - ../../base

components:
  - ../../components/monitoring
  - ../../components/hpa
  - ../../components/pdb

patches:
  - path: patches/deployment-resources.yaml
  - path: patches/deployment-replicas.yaml
  - path: patches/ingress-alb.yaml

configMapGenerator:
  - name: app-config
    behavior: merge
    literals:
      - ENVIRONMENT=prod
      - LOG_LEVEL=info
      - TRACING_SAMPLE_RATE=0.01

images:
  - name: myapp
    newTag: v1.2.3
```

---

## ArgoCD 연동 패턴

### ApplicationSet으로 환경별 자동 배포

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: myapp-environments
  namespace: argocd
spec:
  generators:
    - list:
        elements:
          - env: dev
            cluster: in-cluster
            namespace: myapp-dev
            valuesFile: values-dev.yaml
          - env: staging
            cluster: in-cluster
            namespace: myapp-staging
            valuesFile: values-staging.yaml
          - env: prod
            cluster: prod-cluster
            namespace: myapp-prod
            valuesFile: values-prod.yaml
  template:
    metadata:
      name: "myapp-{{env}}"
    spec:
      project: default
      source:
        repoURL: https://github.com/org/repo.git
        targetRevision: main
        path: charts/my-app
        helm:
          valueFiles:
            - values.yaml
            - "{{valuesFile}}"
      destination:
        server: "{{cluster}}"
        namespace: "{{namespace}}"
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

---

## 변수화 체크리스트

Phase 0 (docker-compose) 시작 시 확인:

```
[ ] 환경변수가 .env 파일로 분리되어 있는가?
[ ] 하드코딩된 호스트명/포트가 없는가?
[ ] 리소스 제한이 설정되어 있는가?
[ ] Health check가 정의되어 있는가?
[ ] 로그가 stdout/stderr로 출력되는가?
[ ] 시크릿이 코드에 포함되어 있지 않은가?
```

Phase 1 (kind) 전환 시 확인:

```
[ ] Helm values.yaml에 모든 변수가 정의되어 있는가?
[ ] values-dev.yaml에 kind 전용 설정이 분리되어 있는가?
[ ] StorageClass가 변수화되어 있는가?
[ ] IngressClass가 변수화되어 있는가?
[ ] ConfigMap/Secret이 분리되어 있는가?
[ ] ServiceMonitor가 조건부 생성되는가?
```

Phase 3 (EKS/GKE) 전환 시 확인:

```
[ ] values-prod.yaml에 managed service 엔드포인트가 설정되어 있는가?
[ ] IAM/IRSA 설정이 반영되어 있는가?
[ ] ALB/GCLB Ingress annotation이 설정되어 있는가?
[ ] HPA/PDB가 활성화되어 있는가?
[ ] External Secrets Operator가 설정되어 있는가?
[ ] Node selector/affinity가 필요한 경우 설정되어 있는가?
```

---

## Anti-Patterns (하지 말 것)

```
# 1. 환경별 templates 디렉토리 분리 — 금지
templates-dev/     ← 유지보수 지옥
templates-prod/    ← 구조 동기화 불가능

# 2. if/else로 환경 분기 — 최소화
{{ if eq .Values.global.environment "prod" }}
  # prod 전용 50줄...
{{ else }}
  # dev 전용 50줄...
{{ end }}
# → 대신 feature flag (hpa.enabled, pdb.enabled) 사용

# 3. values.yaml에 시크릿 — 절대 금지
database:
  password: "my-secret-password"  ← 금지

# 4. 환경별 Chart.yaml — 금지 (Chart는 하나, values만 분리)
```
