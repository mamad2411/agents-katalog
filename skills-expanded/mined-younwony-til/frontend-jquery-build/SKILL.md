---
name: frontend-jquery-build
description: JavaScript + jQuery 기반 프론트엔드 구현 가이드 스킬. web-frontend 에이전트가 사용한다. 모듈 패턴(IIFE + namespace), 선택자 안정성(id/data-* 우선), 이벤트 위임, AJAX 컨벤션, XSS 안전 처리, 폼 검증 패턴을 표준화한다. 6_SPEC.html의 화면 명세를 입력으로 받아 실제 HTML/CSS/JS 파일을 생성하고 API 계약을 확정 상태로 갱신한다. "jQuery 구현", "JS 화면 만들기", "프론트 코딩", "회원가입 폼 구현" 같은 작업에 사용된다.
---

# Frontend jQuery Build

JavaScript + jQuery 기반 화면 구현 표준 워크플로우. 레거시 호환성을 유지하면서 안전한 코드를 생산한다.

## 입력

- `track_dir`: Track 경로 (6_SPEC.html를 SSOT로 사용)
- `target_pages`: 구현할 화면 ID 목록
- `mode`: `"initial"` | `"partial-rerun"`

## 워크플로우

### Step 1: 프로젝트 컨벤션 감지

구현 시작 전 기존 프로젝트 코드를 1~2개 파일 샘플링하여 감지:
- 파일 배치 (정적 자산 경로, 페이지/모듈 분리 규칙)
- 네임스페이스 패턴 (전역 객체명, 모듈 등록 방식)
- AJAX 헬퍼 존재 여부 (기존 wrapper 함수가 있는지)
- 폼 검증 라이브러리 (jQuery Validate 등)
- 빌드 도구 (있다면 ES6+ 가능, 없다면 ES5 안전)

→ 감지된 컨벤션을 따르고, 새 컨벤션을 도입하지 않는다 (CLAUDE.md "외과적 변경" 원칙).

### Step 2: 화면별 구현

각 target_page에 대해:

#### 2-1. HTML 마크업

- 6_SPEC.html의 컴포넌트 카탈로그 + 필드 목록을 그대로 매핑
- 폼 요소에는 `name` + `id` 모두 부여, label은 `for` 연결
- 인터랙션 타깃에는 `data-action="..."` 속성 추가 (jQuery 선택자 기반점)
- 데이터 표시 영역에는 `data-bind="..."` 사용

#### 2-2. jQuery 모듈

표준 패턴:

```javascript
var App = App || {};

App.Signup = (function($) {
  'use strict';

  var $form, $emailField, $passwordField;

  function cacheDom() {
    $form = $('#signupForm');
    $emailField = $form.find('[name="email"]');
    $passwordField = $form.find('[name="password"]');
  }

  function bindEvents() {
    $form.on('submit', handleSubmit);
    $emailField.on('blur', checkEmailDuplicate);
  }

  function validate() {
    // 6_SPEC의 검증 규칙 그대로 구현
    // 반환: { valid: boolean, errors: { field: message } }
  }

  function handleSubmit(e) {
    e.preventDefault();
    var result = validate();
    if (!result.valid) {
      renderErrors(result.errors);
      return;
    }
    submitSignup();
  }

  function submitSignup() {
    $.ajax({
      url: '/api/users',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({
        email: $emailField.val(),
        password: $passwordField.val()
      })
    })
      .done(function(res) {
        window.location.href = '/login';
      })
      .fail(function(xhr) {
        var err = parseError(xhr);
        renderErrors(err.fieldErrors || {});
      });
  }

  function checkEmailDuplicate() {
    var email = $emailField.val();
    if (!email) return;
    $.ajax({ url: '/api/users/email-check', data: { email: email } })
      .done(function(res) {
        if (res.exists) renderErrors({ email: '이미 사용 중' });
      });
  }

  function renderErrors(errors) {
    // 필드별 에러 표시. .text()로 XSS 안전 처리
    $.each(errors, function(field, message) {
      $form.find('[data-error-for="' + field + '"]').text(message);
    });
  }

  function parseError(xhr) {
    try { return JSON.parse(xhr.responseText); } catch (e) { return {}; }
  }

  function init() {
    cacheDom();
    bindEvents();
  }

  return { init: init };
})(jQuery);

$(function() {
  if ($('#signupForm').length) App.Signup.init();
});
```

#### 2-3. CSS

- 컴포넌트 스코프 클래스(BEM 등 프로젝트 컨벤션) 사용
- 인라인 스타일 금지
- 미디어 쿼리는 6_SPEC.html에 반응형 명시된 경우만

### Step 3: API 계약 확정 (Phase 2 핵심 책임)

구현하면서 실제 호출 코드 기준으로 6_SPEC.html의 "API 계약 초안"을 "확정"으로 승격:

- URL, HTTP 메서드 고정
- 요청 body 필드명/타입 고정
- 응답에서 **실제로 사용하는** 필드만 명시 (사용 안 하는 필드는 옵션 표시)
- 에러 응답 shape 고정

6_SPEC.html의 변경 예시:
```diff
- > **상태:** [초안] — Phase 2(web-frontend)에서 확정함
+ > **상태:** [확정 by web-frontend at 2026-05-11]
+ > **백엔드는 이 shape을 정확히 따라 응답해야 한다.**
```

### Step 4: 9_FRONTEND-MANIFEST.html (선택)

생성/수정 파일이 10개 이상이면 별도 매니페스트 작성:

```markdown
# 프론트엔드 구현 매니페스트

## 신규
- src/main/webapp/signup.html — 회원가입 페이지
- src/main/webapp/js/signup.js — App.Signup 모듈

## 수정
- src/main/webapp/js/common.js — 공통 AJAX 에러 핸들러 추가
```

### Step 5: 4_PLAN.html 진행률 갱신

Phase 2 status = "done", 완료 시각 기록.

## XSS / 보안 체크리스트

각 구현 직후 자체 점검:
- [ ] 사용자 입력을 `.html()`로 삽입하는 곳 없음 (`.text()` 사용)
- [ ] URL에 사용자 입력 직접 연결하지 않음 (encodeURIComponent 또는 서버 검증)
- [ ] localStorage/sessionStorage에 민감 정보 저장 없음
- [ ] AJAX 응답을 신뢰하지 않고 추가 검증

## ES5/ES6 결정 트리

```
프로젝트에 babel/webpack/vite 빌드 설정 존재?
  Yes → ES6+ 사용 (let/const, arrow, template literal, etc.)
  No → ES5 안전 문법만:
       - var 사용 (let/const 금지)
       - function() {} (arrow 금지)
       - 문자열 연결 (template literal 금지)
       - $.each, $.extend 등 jQuery 유틸 적극 활용
```

## partial-rerun 모드

1. 변경 영향 파일 식별 (git status / 변경된 6_SPEC.html 섹션 기준)
2. 영향 모듈만 재구현
3. API 계약이 바뀐 경우 6_SPEC.html 해당 섹션만 갱신 + web-backend에 SendMessage

## 완료 체크리스트

- [ ] target_pages의 모든 화면에 HTML + JS 파일 존재
- [ ] 각 모듈이 IIFE + namespace 패턴 사용
- [ ] AJAX 호출에 통일된 에러 핸들러
- [ ] 6_SPEC.html의 "API 계약" 섹션이 [확정] 상태
- [ ] XSS 체크리스트 통과
- [ ] 4_PLAN.html의 Phase 2 status = "done"
