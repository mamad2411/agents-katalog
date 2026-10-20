---
name: deployment-canary
category: cicd
description: "Canary & A/B Testing 배포 가이드 — Argo Rollouts Canary, AnalysisTemplate, Istio 트래픽 라우팅 Use when working with cicd 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Canary & A/B Testing 배포 가이드

Argo Rollouts Canary, AnalysisTemplate, Istio 트래픽 라우팅

## Quick Reference

```
고급 배포 전략?
    │
    ├─ Canary ─────────> 점진적 트래픽 이동 + 자동 분석
    │       │
    │       └─ Argo Rollouts + AnalysisTemplate
    │
    └─ A/B Testing ────> 사용자 세그먼트별 라우팅
            │
            └─ Istio VirtualService + Header/Cookie
```

---

## Canary 배포

### Argo Rollouts Canary

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: my-app
spec:
  replicas: 10
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: my-app
          image: myapp:v2
  strategy:
    canary:
      steps:
        # 1단계: 10% 트래픽
        - setWeight: 10
        - pause: {duration: 5m}

        # 2단계: 분석 실행
        - analysis:
            templates:
              - templateName: success-rate
            args:
              - name: service-name
                value: my-app

        # 3단계: 30% 트래픽
        - setWeight: 30
        - pause: {duration: 5m}

        # 4단계: 50% 트래픽
        - setWeight: 50
        - pause: {duration: 5m}

        # 5단계: 최종 분석
        - analysis:
            templates:
              - templateName: success-rate

        # 6단계: 100%
        - setWeight: 100

      # Istio 트래픽 관리
      trafficRouting:
        istio:
          virtualService:
            name: my-app-vsvc
            routes:
              - primary
          destinationRule:
            name: my-app-destrule
            canarySubsetName: canary
            stableSubsetName: stable
```

### AnalysisTemplate

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate
spec:
  args:
    - name: service-name
  metrics:
    - name: success-rate
      interval: 1m
      count: 5
      successCondition: result[0] >= 0.95
      failureLimit: 3
      provider:
        prometheus:
          address: http://prometheus:9090
          query: |
            sum(rate(http_requests_total{service="{{args.service-name}}",status!~"5.."}[5m]))
            /
            sum(rate(http_requests_total{service="{{args.service-name}}"}[5m]))

    - name: latency-p99
      interval: 1m
      count: 5
      successCondition: result[0] <= 500
      failureLimit: 3
      provider:
        prometheus:
          address: http://prometheus:9090
          query: |
            histogram_quantile(0.99,
              sum(rate(http_request_duration_seconds_bucket{service="{{args.service-name}}"}[5m])) by (le)
            ) * 1000
```

### Istio VirtualService (수동 Canary)

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: my-app
spec:
  hosts:
    - my-app
  http:
    - route:
        - destination:
            host: my-app
            subset: stable
          weight: 90
        - destination:
            host: my-app
            subset: canary
          weight: 10
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: my-app
spec:
  host: my-app
  subsets:
    - name: stable
      labels:
        version: v1
    - name: canary
      labels:
        version: v2
```

---

## A/B Testing

### Header 기반 라우팅

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: my-app
spec:
  hosts:
    - my-app.example.com
  http:
    # 특정 헤더가 있으면 canary로
    - match:
        - headers:
            x-canary:
              exact: "true"
      route:
        - destination:
            host: my-app
            subset: canary

    # 특정 쿠키가 있으면 canary로
    - match:
        - headers:
            cookie:
              regex: ".*canary=true.*"
      route:
        - destination:
            host: my-app
            subset: canary

    # 기본은 stable
    - route:
        - destination:
            host: my-app
            subset: stable
```

### 사용자 세그먼트 기반

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: my-app
spec:
  hosts:
    - my-app.example.com
  http:
    # 베타 테스터
    - match:
        - headers:
            x-user-group:
              exact: "beta"
      route:
        - destination:
            host: my-app
            subset: canary

    # 내부 직원
    - match:
        - headers:
            x-internal:
              exact: "true"
      route:
        - destination:
            host: my-app
            subset: canary

    # 일반 사용자
    - route:
        - destination:
            host: my-app
            subset: stable
```

---

## 자동화된 롤백

### Analysis 기반 자동 롤백

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
spec:
  strategy:
    canary:
      steps:
        - setWeight: 20
        - analysis:
            templates:
              - templateName: error-rate
            args:
              - name: service
                value: my-app
      # 분석 실패 시 자동 롤백
      abortScaleDownDelaySeconds: 30
---
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: error-rate
spec:
  args:
    - name: service
  metrics:
    - name: error-rate
      interval: 30s
      successCondition: result[0] < 0.05  # 에러율 5% 미만
      failureLimit: 3                      # 3번 실패 시 롤백
      provider:
        prometheus:
          address: http://prometheus:9090
          query: |
            sum(rate(http_requests_total{service="{{args.service}}",status=~"5.."}[2m]))
            /
            sum(rate(http_requests_total{service="{{args.service}}"}[2m]))
```

### 분석 유형

| 분석 단계 | 용도 |
|----------|------|
| **prePromotionAnalysis** | Blue-Green 전환 전 |
| **postPromotionAnalysis** | Blue-Green 전환 후 |
| **analysis (step)** | Canary 각 단계 |
| **backgroundAnalysis** | 전체 롤아웃 중 지속 |

---

## 프로그레시브 딜리버리 파이프라인

### ArgoCD + Argo Rollouts 통합

```yaml
# ArgoCD Application
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/my-app.git
    targetRevision: main
    path: k8s
  destination:
    server: https://kubernetes.default.svc
    namespace: my-app
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
---
# Rollout (소스 저장소에 포함)
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: my-app
spec:
  replicas: 5
  strategy:
    canary:
      steps:
        - setWeight: 20
        - pause: {duration: 2m}
        - analysis:
            templates:
              - templateName: success-rate
        - setWeight: 50
        - pause: {duration: 2m}
        - setWeight: 100
```

### 전체 플로우

```
┌─────────────────────────────────────────────────────────────┐
│              Progressive Delivery Pipeline                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Git Push → ArgoCD Sync → Rollout 시작                      │
│       │                        │                             │
│       │                        ▼                             │
│       │              [Canary 20%] ─analysis─> Pass?         │
│       │                        │              │              │
│       │                        │         No: Rollback        │
│       │                        ▼                             │
│       │              [Canary 50%] ─analysis─> Pass?         │
│       │                        │              │              │
│       │                        │         No: Rollback        │
│       │                        ▼                             │
│       │              [100% Promotion]                        │
│       │                        │                             │
│       │                        ▼                             │
│       └──────────────> Complete                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Grafana 대시보드

```json
{
  "panels": [
    {
      "title": "Rollout Status",
      "targets": [{
        "expr": "argo_rollouts_info{namespace=\"$namespace\"}",
        "legendFormat": "{{name}} - {{phase}}"
      }]
    },
    {
      "title": "Canary Weight",
      "targets": [{
        "expr": "argo_rollouts_info{name=\"my-app\"} * on() group_left argo_rollouts_replicas{name=\"my-app\",type=\"canary\"}",
        "legendFormat": "Canary %"
      }]
    }
  ]
}
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 분석 메트릭 없음 | 수동 판단 필요 | AnalysisTemplate 사용 |
| 짧은 pause 시간 | 충분한 검증 불가 | 최소 5분 이상 |
| 단일 메트릭만 분석 | 일부 문제 누락 | 다중 메트릭 (에러율 + 지연시간) |

---

## 체크리스트

### Canary
- [ ] Argo Rollouts 설치
- [ ] 단계별 weight 설정
- [ ] AnalysisTemplate 정의
- [ ] 자동 롤백 조건 설정

### A/B Testing
- [ ] Istio VirtualService 설정
- [ ] Header/Cookie 기반 라우팅
- [ ] 사용자 세그먼트 정의

### 모니터링
- [ ] 분석 메트릭 정의
- [ ] 대시보드 구성
- [ ] 알림 설정

**관련 skill**: `/deployment-strategies` (기본 전략), `/gitops-argocd`, `/istio-traffic`, `/sre-sli-slo`
