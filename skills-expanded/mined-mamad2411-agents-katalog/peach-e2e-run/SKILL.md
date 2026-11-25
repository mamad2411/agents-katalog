---
name: peach-e2e-run
description: |
  E2E 시나리오를 Claude Code에서 실행하는 스킬.
  "시나리오 실행", "e2e 실행", "E2E 돌려", "시나리오 돌려" 키워드로 트리거.
---

# E2E 시나리오 실행

`./e2e.sh` CLI를 통해 시나리오를 실행한다. (playwright-cli 기반)
디버깅은 agent-browser eval로 빠르게 확인한다.

## 도구 역할 분담

| 용도 | 도구 |
|------|------|
| **시나리오 실행** | `./e2e.sh run` (playwright-cli 기반) |
| **셀렉터 디버깅/DOM 확인** | `agent-browser eval` (빠름) |
| **iframe 디버깅** | `./e2e/pwc.sh eval` (fallback) |

## 워크플로우

```
1. 환경 확인 (setup)
2. 탭 목록 → 사용자에게 탭 번호 확인
3. 시나리오 목록 → 사용자 선택
4. --tab N으로 지정된 탭에서 시나리오 실행
5. 결과 보고 (에러 시 agent-browser eval로 디버깅)
```

### 1단계: 환경 확인

```bash
cd e2e && ./e2e.sh setup
```

`setup`이 모든 환경(Chrome Beta, agent-browser, playwright-cli, CDP 연결)을 자동 체크/설치한다.
CDP 미연결이면: `./e2e.sh chrome` 실행 요청.

### 2단계: 탭 확인

```bash
cd e2e && ./e2e.sh status
```

탭 목록을 사용자에게 보여주고 **"몇 번 탭에서 실행할까요?"** 확인.

> 탭 번호는 **0번부터 시작**한다. status 출력에서 확인.
> `chrome://` 탭은 목록에서 제외된다. 실제 페이지 탭만 표시.
> ```
> [0] 페이지 제목
>         https://example.com/...
> [1] NAVER
>         https://www.naver.com/
> ```
> **`[번호]`가 `--tab N`의 N과 동일하다.**

사용자가 로그인한 탭을 그대로 사용한다. 환경(local/test/prod) 구분 없음.

### 3단계: 시나리오 목록

```bash
cd e2e && ./e2e.sh list
```

### 4단계: 실행

```bash
cd e2e && ./e2e.sh run --tab 0 1                       # 0번 탭, 1번 시나리오
cd e2e && ./e2e.sh run --tab 0 1-3                     # 1~3번 순차
cd e2e && ./e2e.sh run --tab 0 all                     # 전체
cd e2e && ./e2e.sh run 1                               # 탭 미지정 → 자동 탐지
```

> `--tab N`은 CDP 조회 후 URL로 변환되어 `E2E_TAB_URL` 환경변수로 `lib/connect.js`에 전달된다.
> 탭 미지정 시 첫 번째 비-chrome 페이지 탭이 자동 선택된다.

> **빈 브라우저 주의**: Chrome Beta에 `chrome://` 탭만 있고 페이지 탭이 없으면 connect.js가 에러를 발생시킨다.
> 이 경우 먼저 페이지 탭을 열어야 한다:
> ```bash
> agent-browser connect 9222
> agent-browser tab new "https://www.google.com"
> ```
> 또는 시나리오 내에서 직접 탭을 열도록 작성한다.

### 5단계: 결과 보고 + 디버깅

- `✨ 완료!` → 성공 보고
- `❌ 에러:` → **agent-browser eval로 빠르게 디버깅**:

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
