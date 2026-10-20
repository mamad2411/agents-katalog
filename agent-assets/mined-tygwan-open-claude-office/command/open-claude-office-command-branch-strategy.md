# GitHub Flow 브랜치 전략

## 브랜치 구조

```
main (production-ready)
 │
 ├── feature/user-authentication
 ├── feature/payment-integration
 ├── fix/login-bug
 └── hotfix/security-patch
```

## 핵심 원칙

1. **main은 항상 배포 가능** - 테스트 통과, 안정적인 상태
2. **기능별 브랜치** - main에서 분기, 작업 완료 후 PR
3. **PR을 통한 머지** - 리뷰 필수, 직접 push 금지
4. **머지 후 삭제** - 브랜치 정리

## 브랜치 네이밍 규칙

### 형식
```
<type>/<feature-name>
```

### 타입별 예시

| 타입 | 용도 | 예시 |
|------|------|------|
| `feature/` | 새 기능 | `feature/user-authentication` |
| `fix/` | 버그 수정 | `fix/login-redirect` |
| `hotfix/` | 긴급 수정 | `hotfix/security-vulnerability` |
| `refactor/` | 리팩토링 | `refactor/database-layer` |
| `docs/` | 문서 작업 | `docs/api-documentation` |
| `test/` | 테스트 추가 | `test/payment-integration` |

### 네이밍 규칙

1. **소문자 사용**
2. **kebab-case** (하이픈으로 연결)
3. **명확하고 간결하게**
4. **이슈 번호 포함 가능**: `feature/123-user-auth`

### 좋은 예시
```
feature/user-authentication
fix/null-pointer-exception
hotfix/sql-injection
refactor/extract-service-layer
```

### 나쁜 예시
```
new-feature          # 타입 없음
Feature/UserAuth     # 대문자, camelCase
fix_bug              # 언더스코어
my-branch            # 모호함
```

## 워크플로우

### 1. 새 기능 개발

```bash
# 1. main에서 최신 코드 가져오기
git checkout main
git pull origin main

# 2. 기능 브랜치 생성
git checkout -b feature/user-authentication

# 3. 작업 및 커밋
git add .
git commit -m "feat(auth): add login endpoint"

# 4. 원격에 푸시
git push -u origin feature/user-authentication

# 5. PR 생성 (GitHub에서 또는 gh CLI)
gh pr create --base main

# 6. 리뷰 후 머지
# 7. 브랜치 삭제
git branch -d feature/user-authentication
git push origin --delete feature/user-authentication
```

### 2. 버그 수정

```bash
git checkout -b fix/login-redirect
# 수정 작업
git commit -m "fix(auth): correct redirect URL after login"
git push -u origin fix/login-redirect
gh pr create --base main
```

### 3. 긴급 수정 (Hotfix)

```bash
# main에서 직접 분기
git checkout main
git pull origin main
git checkout -b hotfix/security-patch

# 빠른 수정
git commit -m "fix!: patch SQL injection vulnerability"
git push -u origin hotfix/security-patch

# 긴급 PR (빠른 리뷰)
gh pr create --base main --label "urgent"
```

## 머지 전략

### Squash and Merge (권장)
- 여러 커밋을 하나로 합침
- 깔끔한 main 히스토리
- PR 단위로 변경 추적

```bash
# GitHub에서 "Squash and merge" 선택
# 또는
git merge --squash feature/user-authentication
```

### Merge Commit
- 모든 커밋 히스토리 유지
- 상세한 변경 이력 필요 시

## 보호 규칙 (Branch Protection)

### main 브랜치 설정
- [ ] Require pull request reviews
- [ ] Require status checks to pass
- [ ] Require branches to be up to date
- [ ] Do not allow force pushes
- [ ] Do not allow deletions

## 진행상황 문서 연동

브랜치명에서 자동으로 기능명 추출:
```
feature/user-authentication
    ↓ 파싱
user-authentication
    ↓ 매핑
docs/progress/user-authentication-progress.md
```
