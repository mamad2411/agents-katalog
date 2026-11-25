---
name: web-qa-integration
description: 웹사이트 FE↔BE 경계면 정합성 검증 스킬. web-qa 에이전트가 사용한다. 단순 "동작 확인"이 아니라 프론트의 AJAX 호출 코드와 백엔드의 Controller/DTO 응답 shape을 동시에 읽어 (URL, HTTP 메서드, 요청/응답 필드명, 타입) 4축으로 교차 비교한다. 불일치 발견 시 9_QA-REPORT.html에 [Boundary-Mismatch] 마커로 양쪽 코드를 인용해 기록한다. "경계면 검증", "FE BE 일치 확인", "API 통합 QA", "계약 검증" 같은 작업에 사용된다.
---

# Web QA Integration — 경계면 정합성 검증

프론트엔드와 백엔드 사이의 통합 버그(boundary bug)를 발견하는 워크플로우. 코드 레벨 + 실행 검증을 결합한다.

## 왜 필요한가

웹 통합 버그의 80%는 "각각은 정상인데 합치면 깨지는" 경계면 버그다. 대표적 패턴:

| 패턴 | 예시 |
|------|------|
| 필드명 불일치 | FE: `res.userId` / BE 응답: `id` → `undefined` |
| 타입 불일치 | FE: `parseInt(res.amount)` / BE 응답: `amount: "1,000"` (문자열, 콤마) |
| HTTP 메서드 | FE: `type: 'PUT'` / BE: `@PostMapping` |
| URL 변형 | FE: `/api/user/123` / BE: `@GetMapping("/users/{id}")` (단수/복수) |
| 에러 shape | FE: `xhr.responseJSON.fieldErrors` / BE: `errors: [...]` |
| 인증 헤더 | FE: `X-Auth-Token` / BE: `Authorization: Bearer ...` |
| null/optional | FE: `res.profile.image` (체이닝) / BE: `profile: null` |

## 입력

- `track_dir`: Track 경로 (6_SPEC.html의 "API 계약" 섹션이 기준점)
- `scope`: `"full"` | `"boundary-only"`
- 변경 파일 목록 (해당 시)

## 워크플로우

### Step 1: 검증 대상 endpoint 목록 추출

`{track_dir}/6_SPEC.html`의 "API 계약" 섹션에서 endpoint를 모두 추출.

각 endpoint마다 (URL, HTTP 메서드, 요청 shape, 응답 shape, 에러 shape)을 명세 기준으로 정리.

### Step 2: FE 호출 코드 수집

프로젝트에서 다음을 grep:
- `$.ajax`, `$.get`, `$.post`, `fetch(`
- 6_SPEC.html의 URL 패턴 (`/api/users` 등)

각 호출 위치에서 추출:
- 실제 URL (변수 보간 후)
- HTTP 메서드 (`type`, `method`)
- 요청 body 필드 (실제 전송 객체)
- 응답 처리 코드에서 사용하는 필드 (`res.userId`, `data.email` 등)
- 에러 처리에서 사용하는 필드

### Step 3: BE 응답 shape 수집

각 endpoint에 대응하는 BE 클래스 식별:
- `@RestController` + `@RequestMapping`/`@GetMapping`/`@PostMapping` 어노테이션 grep
- 매칭된 메서드의 반환 타입 → DTO 클래스
- DTO 클래스의 필드 + getter

### Step 4: 교차 비교 매트릭스

각 endpoint마다 다음 표를 작성:

| 축 | FE 코드 | BE 코드 | 일치 |
|----|---------|---------|------|
| URL | `/api/users` | `@PostMapping("/api/users")` | ✓ |
| Method | `type: 'POST'` | `@PostMapping` | ✓ |
| 요청 필드 `email` | `email: $email.val()` | `SignupRequest.email` | ✓ |
| 요청 필드 `password` | `password: $pw.val()` | `SignupRequest.password` | ✓ |
| 응답 필드 `userId` | `res.userId` 사용 | `SignupResponse.userId` | ✓ |
| 응답 필드 `email` | `res.email` 사용 | `SignupResponse.email` | ✓ |
| 응답 타입 `createdAt` | 표시만 (text) | `String createdAt` | ✓ |
| 에러 필드 `fieldErrors` | `err.fieldErrors` 사용 | `ErrorResponse.fieldErrors` | ✓ |

### Step 5: 불일치 보고

발견된 모든 불일치는 9_QA-REPORT.html에 다음 형식으로 기록:

```markdown
### [Boundary-Mismatch #1] 응답 필드명 불일치 — POST /api/users

**FE 코드:** `src/main/webapp/js/signup.js:42`
```javascript
window.location.href = '/user/' + res.userId;
```

**BE 코드:** `src/main/java/com/example/user/SignupResponse.java:8`
```java
private Long id;  // ← 'userId'가 아님
```

**영향:** FE가 `res.userId`를 사용하지만 BE 응답은 `id`. 가입 후 리다이렉트가 `/user/undefined`로 깨짐.

**권장 수정:** BE의 SignupResponse 필드명을 `userId`로 변경 (6_SPEC.html의 약속과 일치). 또는 6_SPEC.html를 변경하고 FE를 `res.id`로 수정.

**심각도:** Critical (사용자 흐름 차단)

**할당:** web-backend (또는 web-frontend, FE/BE 합의 후)
```

### Step 6: 실행 검증 (browser-debug 위임)

코드 레벨 검증 완료 후 `browser-debug` 스킬을 호출하여 실제 브라우저에서 동작 확인. 코드 검증에서 놓친 런타임 이슈(렌더링, 비동기 타이밍, CORS 등) 발견.

### Step 7: 결과 통합

9_QA-REPORT.html 최종 구조:

```markdown
# QA 보고서 — {Track ID}

**검증 일시:** {ISO}
**검증 범위:** {scope}

## 요약

| 카테고리 | Pass | Fail | Critical |
|---------|------|------|----------|
| 경계면 일치 | 12 | 1 | 1 |
| 브라우저 동작 | 5 | 0 | 0 |
| 기능 체크리스트 | 8 | 0 | 0 |

## 발견 이슈

### [Boundary-Mismatch #1] ...
### [Browser-Error #1] ...
### [Feature-Missing #1] ...

## 영향 분석

수정 필요 항목 → 담당 에이전트로 SendMessage 발송 완료
```

## 환경 폴백

- Playwright/Chrome 미설치: 코드 레벨 검증만 수행, 9_QA-REPORT.html에 "Browser execution skipped: 환경 미충족" 명시
- 6_SPEC.html 누락: web-designer 재호출 요청 (오케스트레이터로 에스컬레이션)

## boundary-only 모드

`scope == "boundary-only"`:
- Step 6 (browser-debug) 생략
- 직전 9_QA-REPORT.html에서 미해결 이슈 ID만 재검증
- 해결된 이슈는 status "resolved"로 갱신 (이력 보존)

## 완료 체크리스트

- [ ] 6_SPEC.html의 모든 endpoint에 대해 교차 비교 매트릭스 작성
- [ ] [Boundary-Mismatch] 발견 항목 모두 9_QA-REPORT.html에 코드 인용 포함
- [ ] [Critical] 항목은 담당 에이전트(web-frontend/web-backend)에 SendMessage 전달 완료
- [ ] browser-debug 호출 결과 통합 (또는 폴백 사유 명시)
