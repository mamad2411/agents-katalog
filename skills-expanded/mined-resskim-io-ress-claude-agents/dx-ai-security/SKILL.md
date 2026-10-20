---
name: dx-ai-security
category: dx
description: "AI 코드 보안 & 품질 보증 가이드 — AI 생성 코드 보안 검증, 품질 게이트, 비용 관리 Use when working with dx 도메인의 패턴 / 구현 선택."
effort: low
deprecated: false
---

# AI 코드 보안 & 품질 보증 가이드

AI 생성 코드 보안 검증, 품질 게이트, 비용 관리

## Quick Reference

```
AI 코드 검증 영역?
    │
    ├─ 보안 ─────────> 시크릿 스캔, 취약점 패턴
    │
    ├─ 품질 ─────────> 커버리지, 복잡도, 환각 감지
    │
    └─ 비용 ─────────> 토큰 예산, 사용량 추적
```

---

## AI 비용 관리 (FinOps)

### 토큰 예산 관리

```yaml
# ai-budget-policy.yaml
apiVersion: finops.company.io/v1
kind: AIBudget
metadata:
  name: team-backend-ai-budget
spec:
  team: backend
  period: monthly

  limits:
    totalBudget: 1000              # USD

    services:
      github-copilot:
        budget: 400
        perUserLimit: 50
      claude-api:
        budget: 400
        tokenLimit: 10000000       # 10M tokens
      openai-api:
        budget: 200

  alerts:
    - threshold: 50                # 50% 사용 시
      action: notify
      channels: ["slack:#finops"]
    - threshold: 80                # 80% 사용 시
      action: notify
      channels: ["slack:#finops", "email:team-lead"]
    - threshold: 100               # 100% 도달 시
      action: throttle
      fallbackModel: "gpt-3.5-turbo"

  tracking:
    granularity: per-request
    attributes:
      - user
      - repository
      - task_type
```

### 비용 모니터링 (PromQL)

```promql
# AI 토큰 사용량 (일간)
sum(increase(ai_tokens_used_total[24h])) by (team, model)

# 팀별 AI 비용
sum(
  increase(ai_tokens_used_total[30d])
  * on(model) group_left(cost_per_token)
  ai_model_pricing
) by (team)

# 작업 유형별 토큰 효율성
sum(ai_tokens_used_total) by (task_type)
/
sum(ai_tasks_completed_total) by (task_type)

# 예산 소진율
sum(ai_cost_total) by (team)
/
sum(ai_budget_limit) by (team)
```

---

## 보안 가이드라인

### AI 생성 코드 보안 체크리스트

```yaml
# ai-security-checklist.yaml
checks:
  # 1. 시크릿 노출
  - name: secret-detection
    tools: [trufflehog, gitleaks]
    severity: critical
    block_merge: true

  # 2. 취약점 패턴
  - name: vulnerability-patterns
    patterns:
      - "eval("                   # 코드 실행
      - "exec("
      - "innerHTML"               # XSS
      - "dangerouslySetInnerHTML"
      - "SELECT.*FROM.*WHERE"     # SQL Injection 가능성
    severity: high
    block_merge: true

  # 3. 의존성 검증
  - name: dependency-check
    description: "새 의존성 추가 시 승인 필요"
    files: ["package.json", "go.mod", "requirements.txt", "pom.xml"]
    require_approval: true

  # 4. 권한 상승
  - name: privilege-escalation
    patterns:
      - "sudo"
      - "chmod 777"
      - "privileged: true"
      - "runAsRoot: true"
    severity: critical
    block_merge: true
```

### Kyverno AI 코드 정책

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: ai-generated-code-review
spec:
  validationFailureAction: Audit
  background: true
  rules:
    - name: require-human-review-for-ai-pr
      match:
        any:
          - resources:
              kinds:
                - PullRequest
              annotations:
                ai-generated: "true"
      validate:
        message: "AI 생성 PR은 최소 1명의 인간 리뷰어 승인이 필요합니다"
        deny:
          conditions:
            - key: "{{ request.object.spec.approvals }}"
              operator: LessThan
              value: 1
```

---

## 품질 보증

### AI 코드 품질 게이트

```yaml
# .github/workflows/ai-quality-gate.yaml
name: AI Code Quality Gate

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  quality-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      # 1. 테스트 커버리지 (AI PR은 더 높은 기준)
      - name: Test Coverage Check
        run: |
          COVERAGE=$(go test -coverprofile=coverage.out ./... | grep total | awk '{print $3}' | sed 's/%//')
          if [[ "${{ github.event.pull_request.labels.*.name }}" == *"ai-generated"* ]]; then
            THRESHOLD=80  # AI PR: 80% 이상
          else
            THRESHOLD=70  # 일반 PR: 70% 이상
          fi
          if (( $(echo "$COVERAGE < $THRESHOLD" | bc -l) )); then
            echo "Coverage $COVERAGE% is below threshold $THRESHOLD%"
            exit 1
          fi

      # 2. 코드 복잡도 체크
      - name: Complexity Check
        run: gocyclo -over 15 . && echo "Complexity OK" || exit 1

      # 3. AI 환각 감지 (존재하지 않는 API 호출 등)
      - name: Hallucination Detection
        run: |
          go build ./... 2>&1 | tee build.log
          if grep -q "undefined:" build.log; then
            echo "Potential AI hallucination detected: undefined references"
            exit 1
          fi
```

### AI 코드 리뷰 자동화

```yaml
# .github/workflows/ai-code-review.yaml
name: AI-Assisted Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  ai-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: AI Code Review
        uses: coderabbitai/ai-pr-reviewer@latest
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          review_type: "comprehensive"
          focus_areas:
            - security
            - performance
            - best-practices
          language: "ko"

      - name: Summarize Review
        uses: actions/github-script@v7
        with:
          script: |
            const reviews = await github.rest.pulls.listReviews({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: context.payload.pull_request.number
            });

            const aiReviews = reviews.data.filter(r =>
              r.user.login.includes('[bot]')
            );

            if (aiReviews.length > 0) {
              await github.rest.issues.createComment({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: context.payload.pull_request.number,
                body: `## AI 리뷰 요약\n\nAI 리뷰어가 ${aiReviews.length}개의 리뷰를 작성했습니다. 인간 리뷰어의 최종 확인이 필요합니다.`
              });
            }
```

---

## 메트릭 & 모니터링

### AI 생산성 메트릭

```promql
# AI 어시스턴스 수용률
sum(ai_suggestions_accepted_total) by (team)
/
sum(ai_suggestions_total) by (team)

# AI 생성 코드 품질 (버그 발생률)
sum(bugs_from_ai_code_total) by (repository)
/
sum(ai_code_merged_total) by (repository)

# 개발자 시간 절약 추정
sum(ai_task_duration_saved_seconds) by (team, task_type) / 3600

# AI vs 인간 코드 비율
sum(lines_of_code_ai_generated) by (repository)
/
sum(lines_of_code_total) by (repository)
```

### 알림 규칙

```yaml
# ai-alerts.yaml
groups:
  - name: ai-agent-alerts
    rules:
      - alert: AIBudgetExceeded
        expr: |
          sum(ai_cost_total) by (team)
          /
          sum(ai_budget_limit) by (team)
          > 0.9
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "팀 {{ $labels.team }} AI 예산 90% 초과"

      - alert: AICodeQualityDrop
        expr: |
          sum(rate(bugs_from_ai_code_total[7d])) by (repository)
          /
          sum(rate(ai_code_merged_total[7d])) by (repository)
          > 0.1
        for: 24h
        labels:
          severity: warning
        annotations:
          summary: "{{ $labels.repository }} AI 생성 코드 버그율 10% 초과"

      - alert: AISuggestionAcceptanceDropped
        expr: |
          sum(rate(ai_suggestions_accepted_total[7d])) by (team)
          /
          sum(rate(ai_suggestions_total[7d])) by (team)
          < 0.3
        for: 7d
        labels:
          severity: info
        annotations:
          summary: "팀 {{ $labels.team }} AI 제안 수용률 30% 미만"
```

---

## 체크리스트

### 보안
- [ ] 시크릿 스캔 자동화
- [ ] AI PR 추가 검증 워크플로우
- [ ] 취약점 패턴 차단
- [ ] 인간 리뷰 필수화

### FinOps
- [ ] 팀별 토큰 예산 설정
- [ ] 비용 알림 설정
- [ ] 사용량 대시보드 구축

### 품질
- [ ] AI 코드 품질 게이트
- [ ] 커버리지 기준 강화
- [ ] AI 코드 리뷰 자동화
- [ ] 생산성 메트릭 수집

**관련 skill**: `/dx-ai-agents` (거버넌스/통합), `/dx-metrics`, `/finops-advanced`
