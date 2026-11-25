---
name: browser-debug
description: |
  Playwright + Chrome 2-Layer 아키텍처로 웹 프로젝트를 점검합니다.
  Layer 1: Playwright 스크립트 자동 생성 → headless 실행 (빠른 1차 검증, 컨텍스트 최소)
  Layer 2: FAIL한 시나리오만 Chrome MCP로 정밀 디버깅 (콘솔/네트워크/DOM 검사)
  서버가 기동되지 않은 상태에서도 자동 탐지하여 서버를 기동한 뒤 점검을 수행합니다.

  다음 키워드/문맥에서 트리거됩니다:
  - "브라우저 디버깅", "Chrome 디버깅", "크롬 디버깅"
  - "브라우저 QA", "웹 QA", "QA 점검", "QA 테스트"
  - "웹 디버그", "웹 디버깅", "프론트 디버깅"
  - "페이지 점검", "UI 테스트", "기능 검증", "화면 확인"
  - "Claude in Chrome으로 확인", "브라우저에서 확인"
  - "프로젝트 QA", "전체 점검", "사이트 점검"
  - "Playwright QA", "Playwright로 QA"
  - `/browser-debug` 슬래시 커맨드로도 호출 가능

  프로젝트 코드를 브라우저에서 직접 확인하고 싶거나, UI 버그를 체계적으로 찾고 싶을 때 사용하세요.
  서버가 꺼져 있어도 자동으로 기동합니다.
paths:
  - "**/*.html"
  - "**/*.tsx"
  - "**/*.jsx"
  - "**/*.vue"
---

# Browser Debug & QA - 2-Layer 아키텍처 웹 점검

## 개요

QA 시나리오를 기반으로 **2-Layer** 구조로 웹 프로젝트를 점검한다.

```
Layer 1 (Playwright): QA-SCENARIOS.html → 테스트 코드 생성 → headless 실행
                      → 모든 PASS → 완료 (Chrome 호출 없음)
                      → FAIL 존재 → Layer 2로 에스컬레이션

Layer 2 (Chrome MCP): FAIL건만 Chrome으로 재실행
                      → console/network/DOM 정밀 검사
                      → 원인 분석 → 코드 수정 → Playwright 재검증
```

반드시 아래 Phase를 순서대로 수행한다. Phase를 건너뛰지 않는다.

---

## Phase 0: QA 시나리오 확인

**다음 순서로 `QA-SCENARIOS.html` 파일을 탐색한다:**

1. `.claude/tracks/`에서 status가 `in_progress`인 활성 Track의 `.claude/tracks/{track_id}/QA-SCENARIOS.html`
2. `.claude/docs/QA-SCENARIOS.html`
3. 프로젝트 루트 `QA-SCENARIOS.html` (하위 호환)

### 기존 시나리오가 있는 경우

1. `QA-SCENARIOS.html`를 읽어 내용을 확인한다
2. 시나리오 유효성 검증:
   - 테스트 URL이 현재 프로젝트와 일치하는가
   - 변경 파일과 현재 git 변경사항이 대체로 일치하는가
   - P0 시나리오가 1개 이상 있는가
3. 유효하면 → Phase 1로 직행
4. 유효하지 않으면 → 시나리오 재생성

### 기존 시나리오가 없는 경우

1. `Skill("qa-scenario")`로 QA 시나리오 생성
2. 생성 완료 후 Phase 1로 진행

---

## Phase 1: 서버 기동 + Playwright 환경 준비

### 서버 확인 및 기동

1. `curl -s -o /dev/null -w "%{http_code}" http://localhost:{port}`로 서버 상태 확인
2. 서버 미기동 시 → 자동 빌드 및 기동 (`references/server-detection.md` 참조)
3. 포트 충돌 시 → 대체 포트로 자동 전환 (설정 파일 수정 없이 `--server.port` 인자 사용)
4. Health check로 서버 ready 확인 (최대 60초 대기)
5. 대체 포트 사용 시 QA 시나리오의 테스트 URL도 해당 포트로 자동 조정

### Playwright 환경 확인 (`references/playwright-setup.md` 참조)

1. `npx playwright --version`으로 설치 여부 확인
2. 미설치 시 자동 설치:
   ```bash
   npm install -D @playwright/test
   npx playwright install chromium
   ```
3. `.claude/playwright-tests/playwright.config.ts` 인라인 생성 (서버 포트 반영)
4. `.claude/playwright-results/` 디렉토리 준비

---

## Phase 2: Playwright 테스트 자동 생성

`QA-SCENARIOS.html`를 파싱하여 Playwright 테스트 코드를 생성한다. (`references/playwright-template.md` 참조)

### 생성 절차

1. QA-SCENARIOS.html에서 시나리오 목록 추출 (ID, URL, Given/When/Then, 검증 방법, 검증 코드)
2. 각 시나리오를 Playwright 테스트 코드로 변환:
   - `network` 검증 → `page.waitForResponse()` + status 체크
   - `javascript` 검증 → `page.locator()` + `expect` 또는 `page.evaluate()`
   - `console` 검증 → `page.on('console')` 에러 수집
   - `screenshot` 검증 → `expect(page).toHaveScreenshot()` 또는 `expect(locator).toHaveScreenshot()` (Visual Regression)
   - 검증 코드 블록 → `page.evaluate()` 래핑
3. 로그인 처리: `beforeAll`에서 form submit → `storageState` 저장
4. BLOCKED 시나리오 → `test.skip` 처리
5. 생성된 파일: `.claude/playwright-tests/qa-scenarios.spec.ts`

### 주의사항

- `console.assert()` → Playwright `expect()`로 변환
- `document.querySelector()` → `page.locator()`로 변환
- 상대 URL은 `baseURL`과 자동 결합

---

## Phase 3: Layer 1 실행 - Playwright headless 검증

### 실행

```bash
cd .claude/playwright-tests && npx playwright test --reporter=json,list 2>&1
```

### Screenshot Baseline 처리

`screenshot` 검증이 포함된 시나리오의 첫 실행 시:
1. baseline 스크린샷이 없으면 FAIL이 발생한다 (Playwright 기본 동작)
2. `--update-snapshots` 플래그로 재실행하여 기준 스크린샷을 자동 생성한다:
   ```bash
   cd .claude/playwright-tests && npx playwright test --update-snapshots --reporter=json,list 2>&1
   ```
3. 생성된 baseline은 `.claude/playwright-tests/__screenshots__/`에 저장된다
4. 이후 실행에서는 baseline 대비 pixel diff로 비교한다

### 결과 처리

1. `.claude/playwright-results/results.json` 파싱
2. 각 시나리오별 pass/fail 분류
3. screenshot FAIL 시: diff 이미지 경로(`*-diff.png`)를 QA-SCENARIOS.html에 기록
4. QA-SCENARIOS.html 업데이트:
   - PASS → ✅ PASS
   - FAIL → ❌ (Layer 2 대기)
   - SKIP → ⏭️ SKIP

### 분기

- **모든 PASS** → Phase 5(결과 보고)로 직행. Chrome 호출 없음.
- **FAIL 존재** → Phase 4(Layer 2)로 진행

---

## Phase 4: Layer 2 실행 - Chrome 정밀 디버깅 (FAIL건만)

FAIL한 시나리오만 Chrome MCP로 정밀 디버깅한다. (`references/layer-escalation.md` 참조)

### Chrome 도구 준비

1. ToolSearch로 Chrome 도구 사전 로드:
   → `"select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__tabs_create_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__javascript_tool,mcp__claude-in-chrome__read_console_messages,mcp__claude-in-chrome__read_network_requests,mcp__claude-in-chrome__form_input,mcp__claude-in-chrome__find"`
2. `tabs_context_mcp`로 탭 준비
3. `read_console_messages` + `read_network_requests` 트래킹 활성화
4. 로그인 처리 (필요 시)

### FAIL 시나리오별 디버깅

각 FAIL 시나리오에 대해:

1. **에러 유형 분석** (Playwright 에러 메시지 기반):
   - `Timeout` → `read_network_requests` 우선 (서버 응답 지연?)
   - `Assertion Failed` → `javascript_tool` 우선 (DOM 상태 불일치?)
   - `Console Error` → `read_console_messages` 우선 (JS 에러?)
   - `Navigation Error` → `read_network_requests` 우선 (404/500?)

2. **Chrome 정밀 검사**:
   - `navigate` → 해당 페이지 이동
   - `read_console_messages` → JS 에러/경고 확인
   - `read_network_requests` → API 상태코드/응답 확인
   - `javascript_tool` → DOM 상태 정밀 검사
   - `computer(action="screenshot")` → 현재 화면 시각 확인 (필요 시)

3. **원인 분석 → 코드 수정**:
   - JS/CSS 수정 → 서버 재기동 불필요
   - Java/설정 수정 → 서버 재기동 필요

4. **Playwright 재검증** (수정 후 반드시 실행):
   ```bash
   cd .claude/playwright-tests && npx playwright test --grep "S{번호}" --reporter=json 2>&1
   ```
   - PASS → 🔧 FIX→PASS 기록
   - FAIL → 추가 디버깅 또는 사용자 보고

### P0 FAIL 우선 처리

- FAIL이 5개 이상이면 P0 FAIL만 먼저 Chrome 디버깅
- P0 수정 후 Playwright 전체 재실행 → 연쇄 FAIL 해소 여부 확인
- P1/P2 FAIL은 P0 해결 후 순차 처리

### 서버 재기동 필요 시

서버 재기동이 필요하면 사용자에게 묻지 않고 Bash로 자체 재기동:
1. 기존 프로세스 종료 (PID 기반)
2. 코드 변경 시 재빌드
3. 동일 포트로 재기동
4. Health check 통과 후 재검증 재개

---

## Phase 5: Track 연동 및 결과 보고

### Track 연동

`.claude/tracks/`에서 활성 Track 탐색 후:
1. Track의 `plan.md`에서 "브라우저 QA" Phase 찾기
2. QA Task를 `[x]`로 마킹
3. Checkpoint에 결과 요약 기록:
   ```
   [x] **Checkpoint**: QA 검증 완료
     - Layer 1 (Playwright): {N}건 PASS
     - Layer 2 (Chrome): {N}건 에스컬레이션 → {N}건 FIX
     - 전체: {N}건, PASS: {N}, FIX→PASS: {N}, FAIL: {N}, BLOCKED: {N}
   ```

### 결과 보고

1. QA-SCENARIOS.html 최종 업데이트 확인
2. QA 과정에서 수정한 파일을 `git add` (commit은 하지 않음)
3. 사용자에게 최종 요약:
   - Layer 1 (Playwright) 결과: PASS/FAIL 카운트, 소요 시간
   - Layer 2 (Chrome) 결과: 에스컬레이션 건수, FIX 건수
   - 발견 및 수정한 버그 요약
   - 수정된 파일 목록

### 정리

- `.claude/playwright-tests/`, `.claude/playwright-results/`는 git add 대상 제외
- 다음 QA 실행 시 덮어쓰기됨

---

## 주의사항

- **Layer 1 우선**: 항상 Playwright 먼저 실행. Chrome은 FAIL건만.
- **Console/Network은 Chrome 전용**: Playwright에서 커버 불가한 영역은 Layer 2에서 처리
- **Playwright 재검증 필수**: Layer 2 수정 후 반드시 Playwright로 재검증
- **서버 재기동 자체 처리**: 사용자에게 묻지 않고 Bash로 직접 처리
- **QA-SCENARIOS.html 실시간 업데이트**: 각 시나리오 결과 즉시 반영
- JavaScript `alert()`, `confirm()`, `prompt()` 등 모달 다이얼로그 트리거 금지
- 실제 데이터에 영향 주는 동작은 사용자 확인 후 진행

## 관련 스킬

- `browser-debug-chrome`: Chrome-only 레거시 버전 (백업)
- `qa-scenario`: QA 시나리오 문서 생성 (Phase 0에서 자동 호출)
