---
name: peach-e2e-convert
description: |
  Playwright codegen 녹화 스크립트를 CDP 시나리오로 변환하는 스킬.
  "시나리오 변환", "녹화 변환", "e2e 변환", "codegen 변환" 키워드로 트리거.
---

# E2E 시나리오 변환 전문가

Playwright codegen으로 녹화한 스크립트를 CDP 시나리오 파일로 변환하고 직접 실행하여 검증한다.

## 워크플로우

### 1단계: 입력 수신

사용자가 Playwright codegen 녹화 코드를 전달한다.

### 2단계: 정보 확인

다음을 사용자에게 물어본다:
- **시나리오 이름**: 한글 (예: `3-배송정보`)
- **저장 위치**: 시나리오 하위 폴더명 (예: `시나리오-사용자`, `시나리오-백오피스`)
- **카테고리**: 하위 폴더명 (예: `조제등록`, `주문관리`)
- 기존 카테고리에 없으면 새 폴더 생성

### 3단계: 변환 실행

`references/변환규칙.md`와 `references/코드패턴.md`를 참조하여 변환한다.

**필수 변환 항목:**
1. `chromium.launch()` → `connect()` (lib/connect.js 사용)
2. `page.goto('/path')` → 페이지 체크 후 자동 이동
3. `browser.close()` / `context.close()` 제거
4. `page.pause()` 제거
5. 다이얼로그 핸들러 추가 (참조 보관 + finally에서 removeListener 해제 필수)
6. try-catch-finally + `process.exit(0)` 래핑
7. 이모지 로그 추가
8. `waitForTimeout` 최소화 → 조건 대기로 변환
9. 팝업(`waitForEvent('popup')`) → 닫힘 감지는 `waitForEvent('close')` 사용

### 4단계: 저장 및 실행 검증

- 파일 저장: `e2e/시나리오/{저장위치}/{카테고리}/{이름}.js`
- 저장 후 **즉시 직접 실행하여 검증**:
  1. CDP 연결 확인:
     ```bash
     cd e2e && ./e2e.sh status
     ```
     CDP 미연결이면 사용자에게 안내: `cd e2e && ./e2e.sh chrome` 실행 요청.
  2. 시나리오 실행 (playwright-cli 기반):
     ```bash
     cd e2e && ./e2e.sh run 시나리오/{저장위치}/{카테고리}/{이름}.js
     # 탭 지정 시:
     cd e2e && ./e2e.sh run --tab 0 시나리오/{저장위치}/{카테고리}/{이름}.js
     ```
  3. 실행 로그 분석:
     - `✨ 완료!` 로그 확인 → 성공
     - `❌ 에러:` 로그 발생 → 원인 분석 후 코드 수정 → 재실행
     - 에러가 해결될 때까지 수정-재실행 반복

### 셀렉터 디버깅 (agent-browser eval 우선)

시나리오 실행 중 셀렉터 에러가 발생하면 **agent-browser eval**로 현재 DOM을 확인한다.

```bash
# CDP 연결 (1회)
agent-browser connect 9222

# 셀렉터 존재 여부 확인
agent-browser eval "document.querySelector('[role=dialog]') !== null"

# 버튼 텍스트 목록 확인
agent-browser eval "JSON.stringify(Array.from(document.querySelectorAll('button')).map(function(b){return b.innerText}))"

# 현재 URL 확인
agent-browser eval "location.pathname"

# 요소 개수 확인
agent-browser eval "document.querySelectorAll('.target').length"
```

> iframe 내부 요소 디버깅은 agent-browser로 불가 → playwright-cli fallback:
> ```bash
> ./e2e/pwc.sh eval "document.querySelector('iframe[src*=target]').contentDocument.querySelector('#element').innerText"
> ```

### 프레임워크별 대응

대상 프로젝트의 프레임워크에 따라 셀렉터와 대기 전략이 달라진다.
`references/프레임워크-대응.md`를 참조하여 적절한 패턴을 적용한다.

## 핵심 원칙

- 대상 프로젝트의 DOM 구조를 파악하고 적절한 셀렉터 전략 적용
- 모달 처리: 프레임워크별 패턴 참조 (iframe vs Portal/Teleport)
- 항상 `lib/connect.js`의 `connect()` 함수 사용
- **실행은 반드시 `node`** — `bun`은 CDP WebSocket 연결 불가

## 참조 문서

| 문서 | 용도 |
|------|------|
| `references/변환규칙.md` | 범용 CDP 변환 규칙 + 트러블슈팅 |
| `references/코드패턴.md` | 시나리오 파일 기본 구조 및 이모지 로그 규칙 |
| `references/프레임워크-대응.md` | React/Vue/Next.js 등 프레임워크별 차이점 |
