---
name: gitops-argocd-ai
category: cicd
description: "AI-assisted GitOps 가이드 — AI 기반 GitOps 자동화: Spacelift Intent, ArgoCD AI 분석, 예측적 배포, Drift 수정 Use when working with cicd 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# AI-assisted GitOps 가이드

AI 기반 GitOps 자동화: Spacelift Intent, ArgoCD AI 분석, 예측적 배포, Drift 수정

## AI GitOps 도구 개요

```
AI GitOps 성숙도:
    |
    +-- Level 1: 분석
    |   +-- Drift 감지 + 알림
    |   +-- 구성 분석
    |   +-- 이상 탐지
    |
    +-- Level 2: 권장
    |   +-- 수정 제안
    |   +-- 최적화 권장
    |   +-- 보안 권고
    |
    +-- Level 3: 자동화
        +-- 자동 수정 (승인 후)
        +-- 예측적 스케일링
        +-- Self-healing
```

---

## Spacelift Intent

Spacelift Intent는 AI를 활용한 IaC 자동화 플랫폼입니다.

```yaml
# Spacelift Stack 설정
# spacelift.yaml
version: 1
stack:
  name: production-infrastructure
  project_root: terraform/

  # AI Intent 활성화
  ai:
    intent:
      enabled: true
      # 자연어로 인프라 변경 요청
      # "Scale the web tier to handle 2x traffic"
      # "Add monitoring for the new database"

  # 정책
  policies:
    - name: drift-detection
      type: PLAN
      body: |
        package spacelift
        deny["Drift detected, review required"] {
          input.spacelift.drift_detection.drifted
        }

    - name: cost-estimation
      type: PLAN
      body: |
        package spacelift
        warn[sprintf("Cost increase: $%.2f/month", [cost_diff])] {
          cost_diff := input.spacelift.cost_estimation.delta_monthly_cost
          cost_diff > 100
        }

  # 자동 Drift 감지
  drift_detection:
    enabled: true
    schedule: "0 */6 * * *"  # 6시간마다
    reconcile: false  # 자동 수정 비활성화 (권장)
    ignore_changes:
      - "aws_instance.*.tags.LastModified"
```

---

## ArgoCD + AI 통합

```yaml
# ArgoCD AI 분석 플러그인 (커스텀)
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-ai-analyzer
  namespace: argocd
data:
  config.yaml: |
    analyzer:
      enabled: true
      model: claude-sonnet-4-6

      # Drift 분석
      drift:
        enabled: true
        notification:
          slack: "#gitops-alerts"
        analysis:
          - compare_desired_vs_live
          - identify_root_cause
          - suggest_remediation

      # 배포 위험 분석
      deployment:
        preSync:
          enabled: true
          checks:
            - resource_impact
            - breaking_changes
            - security_implications

      # 자동 롤백 판단
      rollback:
        enabled: true
        triggers:
          - error_rate_spike
          - latency_increase
          - health_degradation
        humanApproval: true
```

---

## 예측적 배포 분석

```yaml
# AI 기반 배포 분석 워크플로우
# .github/workflows/ai-deploy-analysis.yaml
name: AI Deployment Analysis

on:
  pull_request:
    paths:
      - 'k8s/**'
      - 'terraform/**'

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Diff Analysis
        id: diff
        run: |
          git diff origin/main...HEAD -- k8s/ terraform/ > changes.diff
          echo "changes<<EOF" >> $GITHUB_OUTPUT
          cat changes.diff >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: AI Risk Analysis
        uses: anthropic/claude-code-action@v1
        with:
          prompt: |
            다음 인프라 변경사항을 분석하고 위험도를 평가해주세요:

            변경사항:
            ${{ steps.diff.outputs.changes }}

            다음 관점에서 분석:
            1. 서비스 영향도 (High/Medium/Low)
            2. 롤백 가능성
            3. 다운타임 예상
            4. 보안 영향
            5. 권장 배포 전략

          model: claude-sonnet-4-6
        id: analysis

      - name: Comment PR
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## AI 배포 분석 결과

              ${{ steps.analysis.outputs.response }}

              ---
              _AI 분석 결과입니다. 최종 결정은 리뷰어가 내려주세요._`
            })
```

---

## 자동 Drift 수정 워크플로우

```yaml
# drift-remediation.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
  annotations:
    # Drift 감지 시 알림
    notifications.argoproj.io/subscribe.on-sync-status-unknown.slack: gitops-alerts
spec:
  syncPolicy:
    automated:
      prune: true
      selfHeal: true  # 자동 Drift 수정
      allowEmpty: false
    syncOptions:
      - Validate=true
      - CreateNamespace=true
      - PrunePropagationPolicy=foreground
      - PruneLast=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
---
# Drift 감지 알림 템플릿
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-notifications-cm
  namespace: argocd
data:
  template.drift-detected: |
    message: |
      :warning: Drift 감지됨: {{.app.metadata.name}}

      **상태:** {{.app.status.sync.status}}
      **클러스터:** {{.app.spec.destination.server}}
      **네임스페이스:** {{.app.spec.destination.namespace}}

      **변경된 리소스:**
      {{range .app.status.resources}}
      - {{.kind}}/{{.name}}: {{.status}}
      {{end}}

      [ArgoCD에서 확인]({{.context.argocdUrl}}/applications/{{.app.metadata.name}})

  trigger.on-drift-detected: |
    - description: Drift detected
      when: app.status.sync.status == 'OutOfSync'
      send: [drift-detected]
```

---

## GitOps AI 도구 비교

| 도구 | AI 기능 | 강점 |
|------|--------|------|
| **Spacelift Intent** | 자연어 IaC | Terraform 특화 |
| **env0** | 비용 예측 | 환경 관리 |
| **Harness** | ML 롤백 | CI/CD 통합 |
| **ArgoCD + AI** | 커스텀 분석 | 유연성 |

---

## AI GitOps 체크리스트

### 분석
- [ ] Drift 감지 자동화
- [ ] 배포 위험 분석
- [ ] 비용 영향 예측

### 알림
- [ ] Drift 알림 설정
- [ ] PR 분석 코멘트
- [ ] 이상 징후 알림

### 자동화
- [ ] Self-heal 활성화
- [ ] 승인 게이트 설정
- [ ] 롤백 조건 정의

---

**참조 스킬**: `/gitops-argocd` (기본 GitOps/ArgoCD), `/gitops-argocd-advanced` (ApplicationSet, Sync 전략, 시크릿), `/cicd-devsecops`, `/deployment-strategies`, `/aiops`
