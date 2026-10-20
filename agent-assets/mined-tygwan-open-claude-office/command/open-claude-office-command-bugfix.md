---
name: bugfix
description: 통합 버그 수정 워크플로우. 이슈 분석부터 PR까지 한 번에 관리합니다.
---

# /bugfix - 통합 버그 수정 워크플로우

## Usage

```bash
/bugfix <subcommand> [options]
```

### Subcommands

| Command | Description |
|---------|-------------|
| `start` | 버그 수정 시작 |
| `analyze` | 버그 원인 분석 |
| `complete` | 버그 수정 완료 및 PR 생성 |

## /bugfix start

버그 수정을 시작합니다.

```bash
/bugfix start "로그인 실패 오류" --issue 123 --priority high
```

### 실행 과정

```
┌────────────────────────────────────────────────────────────────────┐
│                     /bugfix start WORKFLOW                          │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. Git Branch 생성                                                 │
│     └── branch-manager: fix/login-failure-123                      │
│                                                                     │
│  2. 이슈 정보 가져오기 (GitHub 연동 시)                              │
│     └── gh issue view 123                                          │
│                                                                     │
│  3. Sprint에 긴급 항목 추가                                         │
│     └── /sprint add: [HOTFIX] 로그인 실패 오류                     │
│                                                                     │
│  4. Root Cause 분석 시작                                            │
│     └── analyzer agent 활성화                                       │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--issue N` | GitHub Issue 번호 | - |
| `--priority` | 우선순위 (critical/high/medium/low) | medium |
| `--hotfix` | 메인 브랜치에서 직접 분기 | false |
| `--no-sprint` | Sprint 연결 생략 | false |

### Output

```
🐛 BUGFIX START: 로그인 실패 오류

📋 Setup:
   Branch:   fix/login-failure-123
   Issue:    #123 - Login fails with special characters
   Priority: HIGH
   Sprint:   Sprint 3 (hotfix item added)

🔍 Initial Analysis:
   Related files detected:
   - src/auth/login.ts
   - src/utils/validation.ts

🎯 Next Steps:
   1. Run `/bugfix analyze` for root cause
   2. Implement the fix
   3. Run `/bugfix complete` when done
```

## /bugfix analyze

버그 원인을 분석합니다.

```bash
/bugfix analyze [--deep]
```

### 실행 과정

```
┌────────────────────────────────────────────────────────────────────┐
│                    /bugfix analyze WORKFLOW                         │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. 관련 코드 검색                                                  │
│     └── Grep: 에러 메시지, 관련 함수 검색                          │
│                                                                     │
│  2. Git History 분석                                                │
│     └── 최근 변경사항에서 원인 추적                                │
│                                                                     │
│  3. 의존성 분석                                                     │
│     └── analyzer agent: 호출 체인 분석                             │
│                                                                     │
│  4. Root Cause 도출                                                 │
│     └── 원인 및 수정 방향 제시                                     │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

### Output

```
🔍 BUGFIX ANALYSIS: 로그인 실패 오류

📍 Root Cause Identified:
   File: src/utils/validation.ts:45
   Issue: Special characters not escaped in regex

📝 Analysis Details:
   The validateEmail() function uses a regex pattern
   that doesn't handle special characters properly.
   When username contains '+' or '.', validation fails.

🔄 Recent Changes (potential cause):
   • 3 days ago: refactor(auth): simplify validation
     Changed regex pattern, removed escape handling

💡 Recommended Fix:
   1. Update regex pattern in validation.ts:45
   2. Add test cases for special characters
   3. Consider using email-validator library

📁 Files to Modify:
   - src/utils/validation.ts (fix)
   - tests/validation.test.ts (add tests)
```

## /bugfix complete

버그 수정을 완료하고 PR을 생성합니다.

```bash
/bugfix complete [--no-pr]
```

### 실행 과정

```
┌────────────────────────────────────────────────────────────────────┐
│                   /bugfix complete WORKFLOW                         │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. Regression Test 실행                                            │
│     └── 기존 테스트 + 새 테스트 실행                               │
│                                                                     │
│  2. Quality Gate 검증                                               │
│     └── quality-gate: lint, test, coverage                         │
│                                                                     │
│  3. Commit 생성                                                     │
│     └── commit-helper: fix(scope): description                     │
│                                                                     │
│  4. Issue 연결 PR 생성                                              │
│     └── pr-creator: Fixes #123                                     │
│                                                                     │
│  5. Sprint 업데이트                                                 │
│     └── /sprint complete: hotfix 항목 완료                         │
│                                                                     │
│  6. 문서 업데이트                                                   │
│     └── CHANGELOG에 버그 수정 기록                                 │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

### Output

```
✅ BUGFIX COMPLETE: 로그인 실패 오류

📋 Quality Checks:
   ✅ Lint: passed
   ✅ Tests: 15/15 passed (3 new tests)
   ✅ Regression: no failures

📊 Updates:
   ✅ Sprint 3: hotfix completed
   ✅ CHANGELOG.md: bug fix recorded

🔗 Pull Request:
   #44: fix(auth): handle special chars in validation
   https://github.com/user/repo/pull/44
   Fixes #123

🎉 Bug fix complete! PR ready for review.
```

## Priority Handling

| Priority | Branch | Review |
|----------|--------|--------|
| `critical` | hotfix/ from main | Expedited |
| `high` | fix/ from develop | Priority |
| `medium` | fix/ from develop | Normal |
| `low` | fix/ from develop | Queued |

## Related Commands

| Command | Purpose |
|---------|---------|
| `/feature` | 기능 개발 워크플로우 |
| `/release` | 릴리스 워크플로우 |
| `/troubleshoot` | 문제 분석 |
