---
name: feature
description: 통합 기능 개발 워크플로우. Phase, Sprint, Git, 문서를 한 번에 관리합니다.
---

# /feature - 통합 기능 개발 워크플로우

## Usage

```bash
/feature <subcommand> [options]
```

### Subcommands

| Command | Description |
|---------|-------------|
| `start` | 새 기능 개발 시작 |
| `progress` | 현재 기능 진행상황 확인 |
| `complete` | 기능 개발 완료 및 PR 생성 |

## /feature start

새 기능 개발을 시작합니다.

```bash
/feature start "사용자 인증" --phase 2 --sprint current
```

### 실행 과정

```
┌────────────────────────────────────────────────────────────────────┐
│                    /feature start WORKFLOW                          │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. Git Branch 생성                                                 │
│     └── branch-manager: feature/user-authentication                │
│                                                                     │
│  2. Phase Task 연결                                                 │
│     └── phase-tracker: docs/phases/phase-2/TASKS.md 업데이트       │
│                                                                     │
│  3. Sprint Item 추가 (선택)                                         │
│     └── /sprint add: 현재 Sprint에 연결                            │
│                                                                     │
│  4. 진행상황 문서 초기화                                            │
│     └── progress-tracker: PROGRESS.md 업데이트                     │
│                                                                     │
│  5. Context 로드                                                    │
│     └── context-optimizer: 관련 파일 자동 로드                     │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--phase N` | 연결할 Phase 번호 | current |
| `--sprint` | Sprint 연결 (current/N/none) | current |
| `--from-task` | Phase Task ID로 시작 (예: T2-03) | - |
| `--no-branch` | 브랜치 생성 생략 | false |

### Output

```
🚀 FEATURE START: 사용자 인증

📋 Setup Complete:
   Branch:   feature/user-authentication
   Phase:    Phase 2 - Core Features
   Task:     T2-05 (newly created)
   Sprint:   Sprint 3 (5 pts added)

📁 Documents Updated:
   ✅ docs/phases/phase-2/TASKS.md
   ✅ docs/PROGRESS.md
   ✅ docs/CONTEXT.md

🎯 Next Steps:
   1. Implement the feature
   2. Run `/feature progress` to track
   3. Run `/feature complete` when done
```

## /feature progress

현재 기능 개발 진행상황을 확인합니다.

```bash
/feature progress
```

### Output

```
📊 FEATURE PROGRESS: 사용자 인증

🔀 Branch: feature/user-authentication
   Commits: 5 (ahead of main by 5)
   Changed: 8 files (+342, -45)

📈 Task Progress:
   Phase 2 / T2-05: [████████░░░░░░░░░░░░] 40%
   Sprint 3: 2/5 pts completed

📝 Recent Activity:
   • 2h ago: feat(auth): add login form
   • 4h ago: feat(auth): setup auth service
   • 1d ago: chore: initialize auth module

⚠️ Reminders:
   - Tests not yet written
   - Documentation pending
```

## /feature complete

기능 개발을 완료하고 PR을 생성합니다.

```bash
/feature complete [--no-pr]
```

### 실행 과정

```
┌────────────────────────────────────────────────────────────────────┐
│                   /feature complete WORKFLOW                        │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. Quality Gate 실행                                               │
│     └── quality-gate: lint, test, coverage 검증                    │
│                                                                     │
│  2. Phase Task 완료 표시                                            │
│     └── phase-tracker: T2-05 → ✅                                  │
│                                                                     │
│  3. Sprint Item 완료                                                │
│     └── /sprint complete: 포인트 반영                              │
│                                                                     │
│  4. Commit 정리                                                     │
│     └── commit-helper: 최종 커밋 메시지 생성                       │
│                                                                     │
│  5. PR 생성                                                         │
│     └── pr-creator: GitHub PR 생성                                 │
│                                                                     │
│  6. 문서 업데이트                                                   │
│     └── agile-sync: CHANGELOG, PROGRESS 동기화                     │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

### Output

```
✅ FEATURE COMPLETE: 사용자 인증

📋 Quality Checks:
   ✅ Lint: passed
   ✅ Tests: 12/12 passed
   ✅ Coverage: 85% (threshold: 80%)

📊 Updates:
   ✅ Phase 2 / T2-05: marked complete
   ✅ Sprint 3: +5 pts (now 24/40)
   ✅ PROGRESS.md: updated to 65%
   ✅ CHANGELOG.md: entry added

🔗 Pull Request:
   #42: feat(auth): add user authentication
   https://github.com/user/repo/pull/42

🎉 Feature complete! Awaiting review.
```

## Integration Map

```
/feature
    │
    ├── branch-manager (Git 브랜치)
    ├── phase-tracker (Phase Task)
    ├── /sprint (Sprint Item)
    ├── progress-tracker (진행률)
    ├── quality-gate (품질 검증)
    ├── commit-helper (커밋 메시지)
    ├── pr-creator (PR 생성)
    └── agile-sync (문서 동기화)
```

## Related Commands

| Command | Purpose |
|---------|---------|
| `/bugfix` | 버그 수정 워크플로우 |
| `/release` | 릴리스 워크플로우 |
| `/phase` | Phase 관리 |
| `/sprint` | Sprint 관리 |
