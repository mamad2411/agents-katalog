---
name: 3a-review
description: >
  Use when a developer is about to transition between project phases and
  needs a readiness check. Validates that prerequisites are met before
  moving from planning to implementation, implementation to deploy, or
  deploy to production. Triggers on: "am I ready to deploy", "review",
  "readiness check", "pre-deploy", "pre-production", "gate check",
  "3a review", "can I move on", "is my agent ready", "checklist",
  "before I deploy", "go to production".
  Not for creating a plan — use 3a-plan.
  Not for tracking progress — use 3a-track.
allowed-tools: Read Write Grep Glob Bash
metadata:
  type: skill
  version: "0.1.0"
---

# review

Verify readiness before transitioning between project phases.

## When to use

- Developer is about to start implementing (plan -> implement)
- Developer is about to deploy (implement -> deploy)
- Developer is about to go to production (deploy -> production)
- Developer wants to validate their work before a milestone

Do NOT use for:

- Creating a plan -> use `3a-plan`
- Checking general progress -> use `3a-track`
- Running `agentcore` commands -> delegate to `aws-agents`

## Input

`$ARGUMENTS` can be:

- "pre-implement" — validate before starting implementation
- "pre-deploy" — validate before deploying to AWS
- "pre-production" — validate before going to production
- Empty — auto-detect the appropriate review based on current phase

## Process

### Step 0: Check prerequisites and determine review type

**Check that `aws-agents` plugin is installed.** Review results reference `aws-agents` skills for fixing blockers. If `aws-agents` is not available, stop and tell the developer:

> 3A Plugin은 `aws-agents` 플러그인과 함께 사용해야 합니다.
> 설치 방법: `claude plugin add --from https://github.com/aws/agent-toolkit-for-aws/tree/main/plugins/aws-agents`
> 설치 후 다시 실행해 주세요.

**Determine review type.** If `$ARGUMENTS` specifies a review type, use it. Otherwise, detect the current phase (same logic as `3a-track` Step 1) and select the appropriate review:

| Current phase | Review to run |
|---|---|
| Phase 1: Scaffold | pre-implement |
| Phase 2: Implement | pre-deploy |
| Phase 3: Deploy | pre-production |

Load the corresponding checklist from references:
- [`references/pre-implement.md`](references/pre-implement.md)
- [`references/pre-deploy.md`](references/pre-deploy.md)
- [`references/pre-production.md`](references/pre-production.md)

### Step 1: Run the checklist

For each item in the checklist, check the actual project state. Don't ask the developer — verify directly by reading files and running non-destructive commands.

Mark each item:
- **PASS**: requirement met, with evidence
- **FAIL**: requirement not met, with what's missing
- **WARN**: partially met or best practice not followed
- **SKIP**: not applicable to this project

### Step 2: Produce review report

```markdown
## 리뷰: [리뷰 유형]
**날짜**: [date]
**결과**: [통과 / 실패 — N건의 차단 요소]

### 체크리스트

| # | 항목 | 결과 | 비고 |
|---|---|---|---|
| 1 | [점검 항목] | 통과 | [근거] |
| 2 | [점검 항목] | 실패 | [누락 사항] |
| 3 | [점검 항목] | 주의 | [권장 사항] |

### 차단 요소 (진행 전 반드시 해결)

1. [차단 요소] — **해결 방법**: [구체적 조치]

### 주의 사항 (권장하지만 차단하지 않음)

1. [주의 사항] — **제안**: [개선 방안]

### 다음 단계

차단 요소가 모두 해결된 경우:
> [다음 단계]로 진행할 준비가 되었습니다. `[aws-agents 스킬]`을 사용하세요.

차단 요소가 남아 있는 경우:
> 위 [N]건의 차단 요소를 해결한 후 `/3a-review [유형]`을 다시 실행하세요.
```

### Step 3: Save the review

Write the review to `.3a/reviews/[review-type].md`. If a previous review exists, archive it with a timestamp suffix.

### Step 4: Guide resolution

For each FAIL item, provide:
1. What specifically is missing
2. Which `aws-agents` skill or command fixes it
3. A concrete example of what "done" looks like

Do not fix the issues directly — explain what to do and let the developer (with `aws-agents`) handle implementation.

## Output

- Review report saved to `.3a/reviews/[review-type].md`
- Clear PASS/FAIL verdict with specific blockers
- Actionable fix instructions for each blocker
- Explicit go/no-go for the phase transition

## Quality criteria

- Every checklist item is verified against actual project state, not self-reported
- Blockers are specific and actionable, not vague warnings
- Fix instructions reference the correct `aws-agents` skill
- The developer knows exactly what to fix and how to verify the fix
