---
name: git-workflow
description: Git 워크플로우 관리 스킬. GitHub Flow, Conventional Commits, 브랜치 전략, PR 관리 시 사용. "git", "커밋", "브랜치", "PR", "머지" 키워드에 반응.
---

# Git Workflow 스킬

GitHub Flow와 Conventional Commits 기반의 Git 워크플로우를 지원합니다.

## 워크플로우 개요

```
main ─────●─────●─────●─────●─────●───▶
           \         /     \     /
feature/    ●───●───●       ●───●
user-auth              feature/
                       payment
```

## 핵심 규칙

### GitHub Flow
1. `main`은 항상 배포 가능한 상태
2. 새 작업은 `feature/{name}` 브랜치에서
3. PR을 통해서만 `main`에 머지
4. 머지 후 브랜치 삭제

### Conventional Commits
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## 참조 문서

- [커밋 컨벤션](git-workflow/COMMIT-CONVENTION.md)
- [브랜치 전략](git-workflow/BRANCH-STRATEGY.md)
- [PR 템플릿](git-workflow/PR-TEMPLATE.md)

## Semantic Versioning 연동

| 커밋 타입 | 버전 영향 | 예시 |
|----------|----------|------|
| `fix:` | PATCH | 1.0.0 → 1.0.1 |
| `feat:` | MINOR | 1.0.0 → 1.1.0 |
| `feat!:` / `BREAKING CHANGE:` | MAJOR | 1.0.0 → 2.0.0 |
| `docs:`, `chore:`, `test:` | 없음 | - |

## 관련 에이전트

| 에이전트 | 역할 |
|---------|------|
| commit-helper | 커밋 메시지 작성 |
| branch-manager | 브랜치 생성/관리 |
| pr-creator | PR 생성 및 설명 작성 |
| code-reviewer | 코드 리뷰 |
| git-troubleshooter | Git 문제 해결 |

## 진행상황 문서 연동

브랜치명에서 기능명을 추출하여 자동 연동:
```
feature/user-authentication
    ↓
docs/progress/user-authentication-progress.md
```

## 빠른 시작

```bash
# 커밋 메시지 작성 도움
"이 변경사항에 대한 커밋 메시지를 작성해줘"

# 새 기능 브랜치 생성
"user-authentication 기능을 위한 브랜치를 만들어줘"

# PR 생성
"현재 브랜치의 PR을 생성해줘"

# 코드 리뷰
"최근 변경사항을 리뷰해줘"

# 충돌 해결
"머지 충돌을 해결해줘"
```
