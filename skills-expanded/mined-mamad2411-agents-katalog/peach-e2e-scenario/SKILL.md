---
name: peach-e2e-scenario
description: |
  E2E 시나리오 생성, 실행, 자동수정을 통합 처리하는 스킬.
  "시나리오 만들어줘", "시나리오 실행", "e2e 실행", "E2E 돌려", "시나리오 돌려",
  "시나리오 변환", "녹화 변환", "e2e 변환", "codegen 변환",
  "e2e 생성", "시나리오 생성", "시나리오 검증" 키워드로 트리거.
---

# E2E 시나리오 통합 전문가

시나리오 생성 + 실행 + 자동수정을 하나의 루프로 처리한다.
기존 시나리오 코드 패턴을 참조하고, 필요시 DOM을 실시간 조사하여 시나리오를 작성한다.
실행 실패 시 에러를 분석하고 스크립트를 직접 수정하여 재실행한다.

## 모드

| 모드 | 트리거 | 동작 |
|------|--------|------|
| `auto` (기본) | `/peach-e2e-scenario [설명]` | 생성 + 실행 + 자동수정 루프 |
| `create` | `/peach-e2e-scenario create [설명 or codegen]` | 시나리오 생성만 |
| `run` | `/peach-e2e-scenario run [경로 or 번호]` | 실행 + 자동수정 루프 |

## 도구 역할 분담

| 용도 | 도구 |
|------|------|
| **시나리오 실행** | `./e2e.sh run` (playwright-cli 기반) |
| **셀렉터 디버깅/DOM 확인** | `agent-browser eval` (빠름) |
| **iframe 디버깅** | `./e2e/pwc.sh eval` (fallback) |
| **문법 검증** | `node --check` |

## 강제 게이트

- `./e2e.sh status`로 탭 목록을 확인하고 사용자가 실행 탭을 지정하기 전에는 `./e2e.sh run`, `agent-browser eval`, 탭 전환을 시작하지 않는다.
- Google 로그인, OAuth, 관리자 콘솔, 결제, 기존 Chrome Beta 프로필 세션 유지가 핵심인 작업은
  시나리오 생성/분석까지만 진행하고, 실제 실행은 사용자 확인 후 시작한다.
- `agent-browser` 디버깅이 비정상이면 OS 레벨 브라우저 우회(`open -a`, 다른 브라우저 실행, 다른 프로필 경로 사용)를 하지 않는다.
- 로그인/2차 인증이 필요하면 AI가 직접 처리하지 않고, 사용자가 Chrome Beta 고정 프로필에서 먼저 인증을 완료하도록 안내한다.

## 워크플로우

### 공통: 환경 확인 + 탭 확인

```bash
cd e2e && ./e2e.sh setup
```

`setup`이 모든 환경(Chrome Beta, agent-browser, playwright-cli, CDP 연결)을 자동 체크/설치한다.
CDP 미연결이면 아래 순서로 자동 복구를 먼저 시도한다.

1. `cd e2e && ./e2e.sh chrome &` 실행
2. `sleep 4` 대기
3. `cd e2e && ./e2e.sh status` 재확인
4. 여전히 미연결이면 사용자에게 `cd e2e && ./e2e.sh chrome` 수동 실행을 안내한다

```bash
cd e2e && ./e2e.sh status
```

탭 목록을 사용자에게 보여주고 **"몇 번 탭에서 실행할까요?"** 확인.

> 탭 번호는 **0번부터 시작**. `chrome://` 탭은 제외. `[번호]`가 `--tab N`의 N과 동일.
> 사용자가 로그인한 탭을 그대로 사용. 환경(local/test/prod) 구분 없음.
> 탭 번호를 받기 전에는 실행하지 않는다. 민감 세션 작업은 탭 번호를 받아도 사용자 승인 전까지 분석만 수행한다.
> **탭 드리프트 방지**: 사용자가 탭 번호를 응답한 뒤 `agent-browser tab N` 직후
> `agent-browser eval "document.title + ' | ' + location.href"` 로 탭이 맞는지 재검증한다.
> 예상과 다르면 `./e2e.sh status` 재출력 후 재선택. 디버깅/재현 시에는 `E2E_TAB_ID` 고정 권장.
> (상세: `peach-e2e-browse/references/탭-선택-패턴.md`)

> **파일 업로드 시나리오**: 시나리오 코드에서 `page.setInputFiles()` 또는 file input 조작이 필요하면
> OS 네이티브 파일 다이얼로그 차단을 위해 `Page.setInterceptFileChooserDialog` 방식을 사용한다.
> CDP Escape / `agent-browser press Escape`로는 macOS 네이티브 다이얼로그를 닫을 수 없다.
> (상세: `peach-e2e-browse/references/SPA-프레임워크-입력패턴.md §3`)

### auto 모드 (기본)

1. **입력 소스 판별** — 자연어 요청 vs codegen 녹화 코드
2. **기존 시나리오 패턴 참조** — `e2e/시나리오/` 하위 기존 코드를 읽어 패턴 파악
   - `references/시나리오-생성-패턴.md` 참조
3. **DOM 선조사** (필요시) — agent-browser eval로 URL 구조, 셀렉터 사전 확인
4. **시나리오 생성** — `references/코드패턴.md` 참조하여 스크립트 작성
   - codegen 입력인 경우 `references/변환규칙.md` 추가 참조
   - 프레임워크별 차이는 `references/프레임워크-대응.md` 참조
5. **정보 확인** — 시나리오 이름(한글), 저장 위치(하위 폴더), 카테고리
6. **문법 검증** — `node --check` 통과 확인
7. **실행 승인 확인**
   - 일반 화면: 탭 번호와 시나리오 경로를 확인한 뒤 실행
   - Google/OAuth/관리자/결제/기존 Chrome Beta 프로필 세션 유지 작업:
     `./e2e.sh run` 실행 전 반드시 사용자에게 실제 실행 승인을 다시 확인
8. **실행** — `./e2e.sh run --tab N 시나리오/경로`
9. **자동수정 루프** — 실패 시 아래 [자동수정 루프](#자동수정-루프-최대-3회) 진행
10. **결과 보고**

### create 모드

1. **입력 소스 판별**
   - 자연어 요청 → `references/시나리오-생성-패턴.md` + `references/코드패턴.md` 참조
   - codegen 녹화 → `references/변환규칙.md` + `references/코드패턴.md` 참조
2. **정보 확인** — 시나리오 이름(한글), 저장 위치, 카테고리
3. **시나리오 생성**
   - **필수 변환 항목** (codegen 입력 시):
     1. `chromium.launch()` → `connect()` (lib/connect.js 사용)
     2. `page.goto('/path')` → 현재 탭 상태 확인 후 조건부 이동
        - 민감 세션이거나 사용자 승인 없으면 자동 이동 금지
        - 비민감 세션 + 사용자 승인 확보 시에만 `page.goto()`
     3. `browser.close()` / `context.close()` 제거
     4. `page.pause()` 제거
     5. 다이얼로그 핸들러 추가 (`setDialogHandler` 교체 + finally에서 원복 필수)
     6. try-catch-finally + exitCode 패턴 래핑 (`process.exit(0)` 고정 종료 금지)
     7. 이모지 로그 추가
     8. `waitForTimeout` 최소화 → 조건 대기로 변환
     9. 팝업(`waitForEvent('popup')`) → 닫힘 감지는 `waitForEvent('close')` 사용
4. **문법 검증** — `node --check` 통과 확인
5. **저장 보고** — `e2e/시나리오/{저장위치}/{카테고리}/{이름}.js`

### run 모드

1. **시나리오 선택**
   ```bash
   cd e2e && ./e2e.sh list
   ```
2. **실행 승인 확인**
   - 로그인된 실탭/고정 프로필 세션 유지가 핵심인 시나리오는 실행 전 사용자 승인 필수
3. **실행**
   ```bash
   cd e2e && ./e2e.sh run --tab N 시나리오/경로
   ```
4. **자동수정 루프** — 실패 시 아래 [자동수정 루프](#자동수정-루프-최대-3회) 진행
5. **결과 보고**

## 자동수정 루프 (최대 3회)

시나리오 실행 결과가 `❌ 에러:`이면 **스크립트를 직접 수정하여 재실행**한다.
단순 디버깅 안내에 그치지 않고, 원인을 파악하여 시나리오 파일을 고친 뒤 다시 실행하는 것까지가 이 스킬의 책임이다.

상세: `references/자동수정-판단트리.md` 참조

### 판단 기준

| 에러 유형 | 처리 방법 |
|-----------|----------|
| 셀렉터 불일치 (timeout, locator not found) | agent-browser eval로 실제 DOM 확인 → 시나리오 셀렉터 수정 |
| dialog 자동 닫힘 (`기록하지 못했습니다`, dismiss) | daemon 잔류 확인 후 kill → `setDialogHandler` 패턴 미적용이면 수정 |
| popup `waitForEvent('close')` 에러 | `Promise.race` + `.catch(() => {})` 패턴 적용 |
| URL 패턴 불일치 (`waitForURL` timeout) | 실제 이동 URL 확인 → 패턴 수정 |
| 타이밍 문제 (`waitForTimeout` 후 즉시 실패) | 고정 대기 → `waitForEvent` 또는 `waitForFunction` 이벤트 기반으로 교체 |
| `Target page, context or browser has been closed` | 팝업/탭이 예상보다 일찍 닫힘 → `.catch(() => {})` 또는 `closeTarget` 옵션 추가 |
| navigation timeout (AJAX submit) | waitForNavigation 제거 또는 waitForURL로 교체 |
| 서버 에러 (500, 네트워크 에러) | **자동수정 불가** → 사용자에게 보고 후 중단 |

### 루프 절차

```
1. 에러 메시지 파싱 → 유형 판별
2. agent-browser eval로 실제 DOM/URL 확인
3. 시나리오 스크립트 수정
4. 재실행
5. 여전히 실패? → 1로 돌아감 (최대 3회)
6. 3회 실패 → 에러 이력 요약 → 사용자에게 보고 → peach-e2e-browse 안내
```

### 수정 후 재실행

```bash
E2E_TAB_ID=<id> ./e2e.sh run '시나리오/대상.js'
```

> dialog 관련 오류라면 실행 전 반드시 daemon 잔류 확인:
> ```bash
> lsof -iTCP:9222 -sTCP:ESTABLISHED -n -P | awk '/node/{print $2}' | xargs kill -9 2>/dev/null
> ```

### 셀렉터 디버깅 (agent-browser eval 우선)

```bash
# CDP 연결 (1회)
agent-browser connect 9222

# 현재 URL 확인
agent-browser eval "location.href"

# 셀렉터 존재 여부
agent-browser eval "document.querySelector('.target') !== null"

# 버튼 목록
agent-browser eval "JSON.stringify(Array.from(document.querySelectorAll('button')).map(function(b){return b.innerText}))"

# 요소 개수
agent-browser eval "document.querySelectorAll('tr').length"
```

> iframe 내부 디버깅은 agent-browser로 불가 → playwright-cli fallback:
> ```bash
> ./e2e/pwc.sh eval "document.querySelector('iframe[src*=target]').contentDocument.querySelector('#element').innerText"
> ```

## native dialog 시나리오 규칙

- `window.alert/confirm` JS monkey-patch는 **동작하지 않는다** — Playwright CDP 자동 dismiss가 먼저 실행됨. **사용 금지**.
- native dialog 처리는 반드시 **CDP 레이어 handler** (`page.on('dialog', handler)`) 사용.
- `connect.js`의 `setDialogHandler(page, prevHandler, newHandler)` 유틸로 handler를 교체하고, finally에서 반드시 복원.
  다중 `page.on('dialog')` 등록 시 모두 실행되어 충돌("already handled") 발생 — 교체 패턴 필수.
- popup(`waitForEvent('popup')`)은 `connect.js`를 거치지 않으므로 별도 handler 등록 필요.
- `process.exit(0)` 고정 종료 금지 → `try/catch/finally + exitCode` 패턴 사용.
- 페이지 상태 의존 로직은 클릭 전에 명시적 대기.
- dialog 대기는 고정 `waitForTimeout` 대신 `page.waitForEvent('dialog')` 이벤트 기반 사용.

상세: `peach-e2e-browse/references/native-dialog-주의사항.md` 참조

## 외부 서비스 전환

외부 사이트(Google, Gmail 등) 진입은 `load + 2초 지연 + 직접 이동 fallback` 패턴 사용.
상세: `peach-e2e-browse/references/외부서비스-링크전환-패턴.md` 참조

## 탭 선택 규칙

- 일반 실행: `--tab N` (빠른 실행용)
- 디버깅/재현/장애분석: `E2E_TAB_ID` 우선 (인덱스 드리프트 방지)

```bash
# targetId 조회
curl -s http://127.0.0.1:9222/json | jq -r '.[] | select(.type=="page" and (.url|startswith("chrome")|not)) | [.id,.title,.url] | @tsv'

# targetId로 실행
cd e2e && E2E_TAB_ID=<targetId> ./e2e.sh run '시나리오/대상.js'
```

상세: `peach-e2e-browse/references/탭-선택-패턴.md` 참조

## 핵심 원칙

- 항상 `lib/connect.js`의 `connect()` 함수 사용
- **실행은 반드시 `node`** — `bun`은 CDP WebSocket 연결 불가
- 대상 프로젝트의 DOM 구조를 파악하고 적절한 셀렉터 전략 적용
- 모달 처리: 프레임워크별 패턴 참조 (iframe vs Portal/Teleport)
- dialog handler는 전역이 아닌 조건부 설치
- 외부 서비스 링크 전환은 `click()` 한 줄이 아닌 fallback URL 도달 규칙 적용
- 저장 직후 `node --check`로 문법 검증 필수
- 탭 미확인 상태와 민감 세션 작업에서는 분석만 수행하고 실행은 사용자 확인 후 진행

## 참조 문서

| 문서 | 용도 | 로드 조건 |
|------|------|-----------|
| `references/코드패턴.md` | 시나리오 기본 구조 (IIFE, exitCode, 이모지) | create, auto |
| `references/변환규칙.md` | codegen → CDP 변환 규칙 | codegen 입력 시 |
| `references/프레임워크-대응.md` | 레거시/모던 프레임워크 분기 | create, auto |
| `references/시나리오-생성-패턴.md` | 기존 코드 참조 기반 생성 가이드 | create, auto |
| `references/validation-통과-패턴.md` | form validation 우회 패턴 | create, auto |
| `references/자동수정-판단트리.md` | 에러 유형별 자동수정 전략 | run, auto 실패 시 |
| `references/daemon-잔류-대응.md` | CDP daemon 문제 해결 | dialog 에러 시 |
| `references/dialog-handler-패턴.md` | native dialog 처리 메커니즘 | dialog 시나리오 |
