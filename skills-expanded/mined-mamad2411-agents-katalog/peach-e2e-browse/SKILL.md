---
name: peach-e2e-browse
description: |
  agent-browser CLI로 Chrome Beta CDP에 연결하여 페이지 탐색, 데이터 확인, 요소 조작을 수행하는 스킬.
  "브라우저 확인", "페이지 봐줘", "DOM 확인", "데이터 점검", "클릭해줘", "화면 확인" 키워드로 트리거.
  E2E 시나리오 작성 중 셀렉터 확인이나 실행 실패 디버깅에도 사용한다.
---

# AI 브라우저 탐색

`agent-browser`(기본) + `./e2e/pwc.sh`(fallback)로 Chrome Beta를 제어한다.
사람이 로그인을 완료한 브라우저를 AI가 이어받아 탐색한다.

## 도구 역할 분담

| 용도 | 도구 | 이유 |
|------|------|------|
| **탐색/검증/확인** | **agent-browser** | eval 6.6x 빠름, 토큰 2.3x 절약 |
| **시나리오 실행** | playwright-cli (`./e2e.sh run`) | lib/connect.js 기반 시나리오 인프라 |
| **fallback** | playwright-cli (`./e2e/pwc.sh`) | iframe 등 agent-browser 미지원 기능 |

## 의사결정 트리 (최우선 확인)

```
목표가 무엇인가?
├─ 데이터 읽기 (텍스트, 개수, 값 확인)
│  → eval 한 줄로 해결
│
├─ 요소 조작 (클릭, 입력)
│  ├─ CSS 셀렉터를 알고 있다 → eval로 click/value 설정
│  └─ 셀렉터를 모른다 → snapshot -i -c + grep으로 ref 찾기 → click ref
│
├─ iframe 내부 접근
│  → playwright-cli fallback (references/iframe-모달-패턴.md 참조)
│
└─ 페이지 전체 구조 파악 (부득이할 때만)
   → snapshot -i -c (절대 전체 snapshot 금지)
```

> **핵심: eval부터 시도. snapshot은 최후수단.**

## 워크플로우

```
1. 환경 확인 (setup)
2. CDP 연결 (agent-browser connect 9222)
3. tab list → 사용자에게 탭 목록 보여주고 작업 탭 확인
4. 선택된 탭에서 작업 (eval/click/snapshot)
5. 결과를 사용자에게 보고
```

### 1단계: 환경 확인

```bash
cd e2e && ./e2e.sh setup
```

`setup`이 모든 환경(Chrome Beta, agent-browser, playwright-cli, CDP 연결)을 자동 체크/설치한다.
CDP 미연결이면: `./e2e.sh chrome` 실행 요청.

### 2단계: CDP 연결

```bash
agent-browser connect 9222
```

> 1회 연결하면 세션 유지. 매 명령마다 재연결 불필요.

### 3단계: 탭 확인 → 사용자에게 선택 요청

```bash
agent-browser tab list
```

탭 목록을 사용자에게 보여주고 **"몇 번 탭에서 작업할까요?"** 라고 확인한다.
출력 예:
```
  [0] Daum - https://www.daum.net/
  [1]  - chrome://webui-toolbar.top-chrome/
→ [2] NAVER - https://www.naver.com/
  [3] Google - https://www.google.com/
```

> **`→` 표시는 agent-browser 내부 포커스이지 Chrome UI 포커스가 아니다.**
> CDP는 사용자가 Chrome에서 보고 있는 탭을 알 수 없다.
> 따라서 작업 시작 전 반드시 사용자에게 탭 번호를 확인해야 한다.

사용자가 탭 번호를 지정하면 `agent-browser tab N`으로 전환 후 진행한다.

### 4단계: 조작

선택된 탭에서 eval → 판단 → 추가 eval/click.

### 5단계: 결과 보고

eval 결과, 페이지 상태를 텍스트로 요약하여 사용자에게 보고.

## 탭 규칙

**현재 탭에서 작업. 탭 전환은 사용자 명시적 지시 시에만.**

- 사용자가 URL을 지정하면 → 현재 탭에서 `agent-browser open "URL"`
- "N번 탭으로 가줘" → `agent-browser tab N`
- "새 탭으로 열어줘" → `agent-browser tab new "URL"`
- AI가 임의로 탭 전환/새 탭 열기 금지

> **`open URL --new-tab` 사용 금지!** 기존 탭을 덮어쓴다.
> 새 탭은 반드시 `tab new "URL"` 사용.

## 조작 명령

### 페이지 이동

```bash
agent-browser open "https://대상URL"
```

### JavaScript 실행 (기본 조작 방법)

```bash
# 값 읽기
agent-browser eval "document.title"
agent-browser eval "document.querySelector('#field').value"
agent-browser eval "document.querySelectorAll('tr').length"

# 조건부 읽기
agent-browser eval "document.querySelector('.cls') ? document.querySelector('.cls').innerText.trim() : '없음'"

# 목록 추출 (JSON.stringify 패턴)
agent-browser eval "JSON.stringify(Array.from(document.querySelectorAll('li')).map(function(el){return el.innerText}))"

# 클릭
agent-browser eval "document.querySelector('a.link').click()"

# 값 입력
agent-browser eval "document.querySelector('#keyword').value = '검색어'"
```

> **eval은 단순 표현식만.** IIFE `(function(){...})()` 사용 금지 -- 직렬화 오류 발생.
> 여러 동작은 각각 별도 eval로 나눠서 실행한다.

### 요소 탐색 (snapshot -- 부득이할 때만)

```bash
# 인터랙티브 요소만 + 컴팩트 출력 (필수 옵션)
agent-browser snapshot -i -c

# CSS 범위 제한 (더 절약)
agent-browser snapshot -i -c -s "table"
```

> **전체 snapshot 금지.** 토큰 비교:
> - 전체 snapshot: ~65,700 토큰
> - snapshot -i -c: ~9,800 토큰
> - eval: ~1~460 토큰

snapshot 후 ref로 조작:
```bash
agent-browser click e10
agent-browser fill e37 "검색어"
agent-browser press Enter
```

> ref는 DOM 변경 시 무효. 클릭/이동 후 반드시 다시 snapshot.

### 클릭 / 입력 / 키보드 (ref 기반)

```bash
agent-browser click e10
agent-browser fill e37 "검색어"
agent-browser press Enter
```

### 스크린샷

```bash
agent-browser screenshot          # 터미널 출력
agent-browser screenshot result.png  # 파일 저장 (토큰 미소비)
```

## fallback: playwright-cli (iframe/모달)

agent-browser가 지원하지 못하는 경우 playwright-cli로 전환한다.

### 전환이 필요한 경우

- iframe 내부 요소 접근 (jQuery UI Dialog + iframe 모달)
- agent-browser snapshot에 iframe 태그만 보이고 내부가 비어있을 때

### 전환 방법

```bash
# playwright-cli 세션 오픈 (1회)
./e2e/pwc.sh open

# 탭 전환
./e2e/pwc.sh tab-select N

# iframe 내부 읽기
./e2e/pwc.sh eval "document.querySelector('iframe[src*=대상]').contentDocument.querySelector('#element').innerText"

# iframe 내부 입력 + 클릭 -- 별도 eval로 분리
./e2e/pwc.sh eval "document.querySelector('iframe[src*=대상]').contentDocument.querySelector('#keyword').value = '검색어'"
./e2e/pwc.sh eval "document.querySelector('iframe[src*=대상]').contentDocument.querySelector('input[type=submit]').click()"
```

> 상세 패턴은 `references/iframe-모달-패턴.md` 참조
> playwright-cli 명령어는 `references/playwright-cli-명령어.md` 참조

## 실측 비교 데이터

동일 시나리오 (구글 → Gmail → 메일 15개 추출), Chrome Beta CDP 9222:

| 항목 | agent-browser | playwright-cli | 배율 |
|------|--------------|---------------|------|
| eval 평균 속도 | **189ms** | 1,249ms | 6.6x |
| 총 명령 시간 | **1,521ms** | 6,257ms | 4.1x |
| 총 출력 바이트 | **1,918B** | 4,343B | 2.3x |
| eval 출력 형식 | 결과값만 | 결과+코드+탭목록+페이지정보 | - |

## 핵심 규칙

1. **eval 우선** -- 데이터 읽기, 클릭, 입력 모두 eval로 먼저 시도. snapshot은 셀렉터를 모를 때만.
2. **작업 탭을 사용자에게 확인** -- CDP는 사용자의 포커스 탭을 알 수 없음. `tab list`를 보여주고 탭 번호를 명시적으로 확인한다.
3. **새 탭은 `tab new URL`** -- `open URL --new-tab` 사용 금지 (기존 탭 덮어씀).
4. **snapshot은 `-i -c` 필수** -- 전체 snapshot 금지. 토큰 폭발.
5. **eval은 단순 표현식만** -- IIFE 금지, 여러 동작은 별도 eval로 분리.
6. **ref는 매번 변경됨** -- DOM이 바뀌면 이전 ref 무효, 다시 snapshot.
7. **iframe → playwright-cli fallback** -- agent-browser는 iframe 내부 접근 불가.
8. **connect 9222 필수** -- 모든 작업 전 CDP 연결 확인.

## 참조 문서

| 문서 | 용도 |
|------|------|
| `references/agent-browser-명령어.md` | agent-browser 전체 명령어 레퍼런스 |
| `references/playwright-cli-명령어.md` | fallback 전용 (iframe 등 agent-browser 미지원 시) |
| `references/iframe-모달-패턴.md` | jQuery UI Dialog + iframe 모달 접근 패턴 |
