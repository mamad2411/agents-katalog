---
description: 
globs: 
alwaysApply: false
---
# Commit Message Convention

## 개요
각 commit message는 **header**, **body**, 그리고 **footer**로 이루어져 있습니다. Header는 **type**, **scope**, 그리고 **subject**로 구성됩니다.

```
<type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

## 기본 규칙
- Header는 commit message의 핵심이며, `<scope>` 부분은 선택사항입니다
- 각 줄은 **100 글자**를 넘어서는 안됩니다 (GitHub 등에서의 가독성 향상)
- Header는 **영문 소문자**로 작성합니다
- Subject는 **명령문**으로 작성합니다

## Type 종류

### 🎉 feat
새로운 기능 추가
```
feat(auth): add social login with google oauth
feat: implement user dashboard
```

### 🐛 fix
버그 수정
```
fix(api): resolve memory leak in user service
fix: prevent duplicate form submissions
```

### 📚 docs
문서 변경 (코드 변경 없음)
```
docs(readme): update installation instructions
docs: add api endpoint documentation
```

### 💎 style
코드 formatting, linting, 세미콜론 누락 등 (로직 변경 없음)
```
style: fix eslint warnings in components
style(css): improve button hover animations
```

### 🔨 refactor
코드 리팩토링 (기능 변경 없음)
```
refactor(utils): extract common validation logic
refactor: simplify user authentication flow
```

### ✅ test
테스트 추가 또는 수정
```
test(auth): add unit tests for login service
test: increase coverage for payment module
```

### 🔧 chore
빌드, 패키지 매니저, 설정 파일 등 수정
```
chore: update dependencies to latest versions
chore(webpack): optimize build configuration
```

### ⚡ perf
성능 개선
```
perf(api): optimize database queries
perf: reduce bundle size by lazy loading
```

### 🔒 security
보안 관련 수정
```
security: update vulnerable dependencies
security(auth): strengthen password validation
```

## Scope 가이드라인
프로젝트에 따라 다르지만, 일반적인 scope 예시:
- `fe` / `frontend`: 프론트엔드 관련
- `be` / `backend`: 백엔드 관련
- `api`: API 관련
- `auth`: 인증/인가 관련
- `ui`: UI 컴포넌트 관련
- `db`: 데이터베이스 관련

## Subject 작성 규칙
- 변경사항을 간결하게 요약
- **영문 소문자**로 시작
- **명령문** 사용 (`add`, `fix`, `update` 등)
- 마지막에 마침표(.) 붙이지 않음
- 50자 이내 권장

### ✅ 좋은 예시
```
feat(auth): add two-factor authentication
fix(api): resolve timeout issue in payment service
docs: update contributing guidelines
```

### ❌ 나쁜 예시
```
feat(auth): Added two-factor authentication.  // 대문자 시작, 마침표
fix(api): Fixed timeout issue  // 과거형 사용
docs: Updated the contributing guidelines  // 과거형 사용
```

## Body 작성 가이드
- 한글 또는 영문으로 작성
- **무엇을** 변경했는지보다 **왜** 변경했는지에 집중
- 변경 이유와 구현 방법 설명
- 72자마다 줄바꿈 권장

## Footer 작성 규칙

### Breaking Changes
```
BREAKING CHANGE: user authentication now requires email verification
```

### Issue 연결
```
Closes #123
Fixes #456
Resolves #789
```

### 여러 이슈 연결
```
Closes #123, #456
```

## Revert
이전 commit을 되돌리는 경우:
```
revert: this reverts commit <hash>

Reason for revert: explanation...
```

## 완전한 예시

### 예시 1: 기능 추가
```
feat(auth): implement social login with google oauth

사용자 편의성 향상을 위해 Google OAuth 2.0을 이용한 소셜 로그인 기능을 추가했습니다.
기존 이메일 가입 외에 Google 계정으로도 회원가입 및 로그인이 가능합니다.

- Google OAuth 2.0 API 연동
- 소셜 로그인 버튼 UI 추가
- 사용자 정보 동기화 로직 구현

Closes #127
```

### 예시 2: 버그 수정
```
fix(payment): resolve transaction timeout issue

결제 처리 중 간헐적으로 발생하는 타임아웃 문제를 해결했습니다.
API 호출 시 연결 시간 초과값을 30초로 증가시키고,
재시도 로직을 추가하여 안정성을 개선했습니다.

Fixes #89
```

### 예시 3: 문서 업데이트
```
docs: add development environment setup guide

신규 개발자를 위한 개발 환경 설정 가이드를 추가했습니다.
Node.js, npm, 환경변수 설정 등의 상세한 설명을 포함합니다.
```

## 추가 팁
1. **한 커밋당 하나의 논리적 변경**만 포함
2. **작은 단위**로 자주 커밋
3. **의미 있는 메시지** 작성 (나중에 히스토리 추적 시 도움)
4. **팀 컨벤션**을 우선적으로 따르기