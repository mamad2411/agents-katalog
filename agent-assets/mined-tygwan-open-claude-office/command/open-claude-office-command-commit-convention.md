# Conventional Commits 규칙

## 커밋 메시지 형식

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## 타입 정의

### 버전에 영향을 주는 타입

| 타입 | 설명 | 버전 영향 | 예시 |
|------|------|----------|------|
| `feat` | 새로운 기능 추가 | MINOR | `feat: add user login` |
| `fix` | 버그 수정 | PATCH | `fix: resolve null pointer` |

### 버전에 영향 없는 타입

| 타입 | 설명 | 예시 |
|------|------|------|
| `docs` | 문서 변경 | `docs: update README` |
| `style` | 코드 포맷팅 (기능 변경 없음) | `style: fix indentation` |
| `refactor` | 리팩토링 (기능 변경 없음) | `refactor: extract method` |
| `test` | 테스트 추가/수정 | `test: add unit tests` |
| `chore` | 빌드, 설정 변경 | `chore: update deps` |
| `perf` | 성능 개선 | `perf: optimize query` |
| `ci` | CI 설정 변경 | `ci: add GitHub Actions` |

## Breaking Change (MAJOR 버전)

### 방법 1: `!` 사용
```
feat!: remove deprecated API

기존 v1 API가 완전히 제거됩니다.
```

### 방법 2: footer 사용
```
feat: new authentication system

BREAKING CHANGE: 기존 토큰 형식과 호환되지 않습니다.
마이그레이션 가이드: docs/migration.md
```

## Scope (선택)

영향 범위를 명시:
```
feat(auth): add OAuth2 support
fix(api): handle timeout errors
docs(readme): add installation guide
```

### 권장 Scope
- `auth`: 인증/인가
- `api`: API 관련
- `ui`: UI/프론트엔드
- `db`: 데이터베이스
- `config`: 설정

## Description 작성 규칙

1. **현재형 동사로 시작**: add, fix, update, remove, refactor
2. **소문자로 시작**
3. **마침표 없음**
4. **50자 이내**

### 좋은 예시
```
feat(auth): add password reset functionality
fix(api): handle empty response gracefully
refactor(user): extract validation logic
```

### 나쁜 예시
```
feat: Added new feature.     # 과거형, 마침표
Fix bug                      # 대문자, 모호함
update                       # 설명 부족
```

## Body 작성 (선택)

- 변경 이유 설명
- 이전 동작과 비교
- 72자 줄바꿈 권장

```
fix(auth): prevent session fixation attack

기존에는 로그인 후에도 세션 ID가 유지되어
세션 고정 공격에 취약했습니다.

이제 로그인 성공 시 새 세션 ID를 발급합니다.
```

## Footer (선택)

### 이슈 참조
```
feat(payment): add stripe integration

Closes #123
Refs #456, #789
```

### Breaking Change
```
feat!: new API structure

BREAKING CHANGE: /api/v1/* 엔드포인트가 /api/v2/*로 변경됩니다.
```

### Co-author
```
feat: collaborative feature

Co-authored-by: Name <email@example.com>
```

## 커밋 메시지 체크리스트

- [ ] 적절한 타입 선택 (feat, fix, docs 등)
- [ ] 명확한 scope (선택)
- [ ] 현재형 동사로 시작하는 description
- [ ] 50자 이내 description
- [ ] Breaking change 시 `!` 또는 `BREAKING CHANGE:` 사용
- [ ] 관련 이슈 번호 참조 (해당 시)
