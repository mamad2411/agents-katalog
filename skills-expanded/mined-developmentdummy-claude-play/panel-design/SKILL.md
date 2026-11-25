---
name: panel-design
description: 패널 생성, 수정, 레이아웃 설정, 커스텀 데이터 구조 설계, 엔진 스크립트 작성, 팝업 이펙트 등 패널 시스템 전반을 다룬다. 패널 HTML을 만들거나 고칠 때, variables.json이나 커스텀 데이터 구조를 설계할 때, layout.json을 변경할 때, tools/engine.js에 액션을 추가할 때, hint-rules.json을 작성할 때, 팝업 템플릿을 만들 때 반드시 이 스킬을 사용하라. "패널 만들어줘", "인벤토리 패널", "레이아웃 변경", "게이지 바", "엔진 액션 추가", "팝업", "dock 패널", "모달", "무대 레이아웃", "main 패널", "mount once", "변수 추가", "상태 패널" 등의 키워드에 트리거된다.
allowed-tools: Read, Write, Edit, Bash
---

# 패널 시스템 — 제작 및 변경 가이드

## 아키텍처 핵심

패널 시스템은 **MVC 데이터 드리븐 구조**다:

```
[JSON 데이터] ←→ [패널 UI] (표시 + 조작)
     ↕
[AI 에이전트] + [엔진 스크립트]
```

- **Model** = `variables.json` + 커스텀 `*.json` (game-state.json, inventory.json 등)
- **View** = 패널 HTML (Handlebars 템플릿 + Shadow DOM CSS 격리)
- **Controller** = 엔진 스크립트 (`tools/engine.js`) + `__panelBridge` API

**핵심 원칙:**
- 패널은 자체 상태를 갖지 않는다 — 재렌더링되면 DOM이 초기화된다
- 유지해야 할 상태는 반드시 JSON 파일에 저장한다
- 규칙 기반 로직(데미지 계산, 아이템 효과)은 엔진에 위임한다
- AI는 서사를, 엔진은 판정을, 패널은 표시와 입력을 담당한다

---

## 아키텍처 원리 — 레이어 책임 경계

패널·엔진·AI 세 레이어가 공존하는 페르소나에서 설계 실패는 거의 항상 **레이어 간 책임 경계가 느슨해서** 발생한다. 아래 다섯 가지 원리는 구현 방식(타이머, 재화, 체력 등 도메인 무관)을 넘어 모든 페르소나에 적용된다.

### 1. 역할 분리 — AI / 패널 / 엔진
- **엔진(`tools/engine.js` 등)**: 상태의 단일 소유자(single source of truth). 상태를 바꿀 수 있는 **유일한** 주체.
- **패널**: 오퍼레이터. 유저 UI → 엔진 호출을 중개한다. 엔진 결과를 읽어 UI를 갱신하고, AI가 알아야 할 부작용을 구조화된 헤더로 브리핑한다.
- **AI**: 내레이터. `[STATE]` / `[ACTION_LOG]` / 기타 도메인 헤더를 **사실로 받아들이고** 서사를 쓴다. 엔진 직접 호출은 조회 성격(예: `query_status`)에 한정하며, 상태 변경 호출은 원칙적으로 하지 않는다.

### 2. 단일 실행 경로 (Single-caller principle)
어떤 상태 변경 연산이든 **호출자는 하나**여야 한다. 동일한 연산을 여러 레이어(엔진 내부 + 패널 + AI)가 부를 수 있는 구조는 언제든 중복 실행을 낳는다.

**설계 체크**: "이 연산은 어디서 부르기로 정했는가? 다른 레이어에서 같은 걸 부를 수 있는가?" 답이 "예"라면 한쪽을 제거한다. 예를 들어 시간 진행처럼 여러 호출 경로가 생기기 쉬운 연산은 엔진 내부에 캡슐화하고(예: 액션 실행 후 자동 시간 소비), 상위 레이어는 호출하지 않는다.

### 3. 부작용의 투명성 (Side-effect transparency)
엔진 액션은 "무엇을 호출했는가"뿐 아니라 "그 결과로 무엇이 일어났는가"까지 AI에게 노출돼야 한다. 이 통로는 **구조화된 헤더**여야 하며, 유저 자연어가 아니다.
- 상태 스냅샷 → `[STATE]` (자동)
- 실행된 패널 액션 → `[ACTION_LOG]` (`executeAction` 경로면 자동)
- 그 외 도메인 특이 부작용(시간 이동, 자원 획득, NPC 상태 전이, 이벤트 트리거 등) → `__panelBridge.queueEvent('[DOMAIN] ...')`로 패널이 명시 주입

헤더가 없으면 AI는 유저 자연어에서 결과를 유추하게 되고, 유추와 실재가 어긋나는 순간 재실행·상태 불일치가 따라온다.

### 4. 의도-실재 정렬 (Intent-execution coherence)
유저의 자연어 메시지와 패널이 실제로 실행한 결과가 충돌하면 **패널 실행 결과(헤더)가 실재**다. AI는 유저 텍스트가 "한 번 더 실행해달라"처럼 보여도 재실행하지 않는다. 헤더는 선언이고, 유저 텍스트는 그에 대한 해설·장면화 요청이다.

### 5. 커버리지 원칙 (Panel-action coverage)
**상태를 바꾸는 모든 UI 요소는 등록된 패널 액션**(`registerAction` → `executeAction`)이어야 한다. 그래야 `[ACTION_LOG]`·`[AVAILABLE]`에 자동으로 노출되어 AI가 재현·추적·응답할 수 있다. 인라인 클릭 핸들러에 `runTool('engine', ...)`을 직접 박아 넣으면 그 동작은 AI 시야 밖의 유령 동작이 된다.

---

## Shadow DOM 스크립트 환경

패널의 `<script>` 블록은 시스템이 `new Function("shadow", code)` 로 감싸서 실행한다. 따라서:

- **`shadow`가 자동 주입된다** — Shadow Root 참조. 별도 선언 불필요.
- **스코프가 자동 격리된다** — IIFE `(function(){ ... })()` 래핑 불필요.
- **`document.currentScript.getRootNode()` 불필요** — `shadow`가 이미 같은 역할.

```html
<!-- ✅ 올바른 패턴 -->
<script>
  shadow.querySelector('.btn')?.addEventListener('click', () => { ... });
  const items = shadow.querySelectorAll('.item');
</script>

<!-- ❌ 불필요한 패턴 (동작은 하지만 장황함) -->
<script>
(function() {
  const root = document.currentScript.getRootNode();
  root.querySelector('.btn')?.addEventListener('click', () => { ... });
})();
</script>
```

**`<script type="application/json">`은 실행되지 않는다** — Handlebars 데이터를 JS에 전달하는 용도.

**🚫 onclick 속성에서 패널 내 `<script>` 함수 호출 금지:**

`<script>`는 `new Function("shadow", code)`로 격리 실행되므로 함수 선언이 **document.window에 노출되지 않는다.** 따라서 onclick 속성에서 그 함수를 호출하면 `ReferenceError: X is not defined`로 깨진다.

```html
<!-- ❌ 잘못된 패턴 — pickTrait가 onclick 스코프에서 안 보임 -->
<script>
  async function pickTrait(id) { await runTool('engine', {action: 'awaken', params: {id}}); }
</script>
<button onclick="pickTrait('foo')">선택</button>   <!-- ReferenceError -->

<!-- ✅ 패턴 A — onclick에 인라인 (간단한 경우 권장) -->
<button onclick="runTool('engine', {action: 'awaken', params: {id: 'foo'}}).then(function(){ window.__panelBridge && window.__panelBridge.sendMessage('—'); })">선택</button>

<!-- ✅ 패턴 B — addEventListener로 바인딩 (복잡한 로직) -->
<script>
  shadow.querySelectorAll('.pick-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
      const id = btn.dataset.id;
      await runTool('engine', {action: 'awaken', params: {id}});
      window.__panelBridge?.sendMessage('—');
    });
  });
</script>
<button class="pick-btn" data-id="foo">선택</button>
```

**전역 노출 가능한 것**: `window.__panelBridge` 객체와 `window.__panelModalsState` 등은 시스템이 명시적으로 window에 expose. **사용자 정의 함수는 인라인 또는 addEventListener 사용**.

**🚫 `runTool`은 bare global이 아니다 — 반드시 `window.__panelBridge.runTool`:**

```html
<!-- ❌ 잘못된 패턴 — ReferenceError: runTool is not defined -->
<button onclick="runTool('engine', {action: 'foo'})">실행</button>

<!-- ✅ 올바른 패턴 -->
<button onclick="window.__panelBridge.runTool('engine', {action: 'foo'})">실행</button>

<!-- ✅ <script> 안에서는 alias로 줄여 쓰는 것이 일반적 -->
<script>
  const B = window.__panelBridge;
  shadow.querySelector('.btn').addEventListener('click', async () => {
    const res = await B.runTool('engine', { action: 'foo' });
    // ...
  });
</script>
```

`window.__panelBridge`가 제공하는 메서드 전체: `sendMessage`, `fillInput`, `updateVariables`, `updateData`, `updateLayout`, `queueEvent`, **`runTool`**, `openModal`, `closeModal`, `closeAllModals`, `focusPanel`, `emit`, `on`, `registerAction`, `executeAction`, `showPopup`, `showToast`, `confirm`, `jev`, `vectors`. 모두 `window.__panelBridge.` 프리픽스 필수 (`<script>` 안에서는 주입된 bare `__panelBridge`도 같다).

**`__panelBridge.data`는 읽는 시점의 최신값이다** — 이벤트 핸들러·타이머 안에서 나중에 읽어도 실행 시점 값에 고정되지 않는다. 단 모달·독·인라인 패널에서 `const B = window.__panelBridge`로 window 객체를 변수에 담아 두면 그 시점 객체에 고정된다 — `<script>`에 주입된 bare `__panelBridge`를 쓰거나 읽을 때마다 다시 조회하라.

---

## 패널 타입별 체크리스트

### 사이드바 패널 (left/right)
- [ ] `panels/{번호}-{이름}.html` 파일 생성
- [ ] `layout.json` → `panels.placement.{이름}` = `"left"` 또는 `"right"`

### 무대 패널 (`main`) — 무대 레이아웃
- [ ] 정말 "패널이 본체, 대화가 보조"인 페르소나인가? (집필 워크벤치·대시보드·보드형 도구). 대화가 본체인 RP면 쓰지 않는다 — 채팅이 우측 좁은 컬럼으로 밀린다
- [ ] `panels/{번호}-{이름}.html` 파일 생성 — **번호 순서가 곧 탭 순서**다 (main 패널 1개면 탭 바 없음)
- [ ] `layout.json` → `panels.placement.{이름}` = `"main"` (하나라도 있으면 무대 레이아웃이 켜진다)
- [ ] `layout.json`에 `app` 블록이 **없는가** — 있으면 앱 모드가 이기고 main 패널은 어디에도 안 뜬다
- [ ] (선택) `layout.json` → `chat.width` (px, 기본 420, 최소 320으로 clamp) — 우측 채팅 컬럼 폭
- [ ] `__modals` 초기값 **불필요** — 상시 표시 배치다
- [ ] 패널 root가 배경·여백을 직접 책임진다 (사이드바 카드 크롬 없음). 세로 스크롤은 무대 칸이 제공 — 툴바 고정이 필요하면 root `height: 100%` + 내부 한 영역만 `overflow-y: auto`
- [ ] 다른 탭으로 보내려면 `__panelBridge.focusPanel('{이름}')`, 패널 간 신호는 `__panelBridge.emit(...)` / `on('panel:…')`
- [ ] 긴 본문·편집기면 `<panel-meta>{"mount": "once"}</panel-meta>` + `stateChanged` 갱신 (아래 mount-once 체크리스트)

### mount-once 패널 (배치 무관, opt-in)
- [ ] HTML 상단에 `<panel-meta>{"mount": "once"}</panel-meta>` (다른 메타 필드가 있으면 같은 블록에 합친다)
- [ ] 스크립트가 실행 시점에 `__panelBridge.data`로 초기 렌더
- [ ] 이후 갱신은 `__panelBridge.on('stateChanged', d => …)`로만 — **관심 있는 조각의 서명(id·rev 등)을 비교해 바뀌었을 때만** DOM을 고친다 (초당 여러 번 올 수 있다)
- [ ] 작성 중인 입력을 서버 값으로 덮어쓰지 않는다 (포커스 중·미저장 변경이면 건너뛰기)
- [ ] `<!-- deps: ... -->` 주석은 넣지 않는다 — 다시 그리지 않으므로 의미 없다
- [ ] 템플릿을 고친 뒤 확인할 때는 **브라우저 새로고침** (mount-once는 템플릿 변경도 무시한다)
- [ ] 모달에 쓰면 닫았다 다시 열어도 재초기화되지 않는다는 점을 감안했는가? 독 탭 전환 시에는 새로 마운트된다

### 모달 패널
- [ ] `panels/{번호}-{이름}.html` 파일 생성
- [ ] `layout.json` → `panels.placement.{이름}`:
  - `"modal"` = 필수 모달 (ESC로 닫을 수 없음, 게임플레이 흐름 패널)
  - `"modal-dismissible"` = 해제 가능 모달 (ESC로 닫기 가능, 보조 UI 패널)
  - 정확히는: 두 값의 차이는 **선택지 액션이 핸들러 실행을 위해 이 패널을 자동으로 열 때** 필수(`true`)로 여느냐 `"dismissible"`로 여느냐뿐이다(빌트인 `__open`은 항상 `"dismissible"`). 실제로 ESC·X로 닫히는지는 열린 시점의 `__modals` 값(= `openModal(name, mode)`의 mode)이 정한다
- [ ] `variables.json` → `__modals.{이름}` = `false` (초기값)
- [ ] 어딘가에 열기 버튼: `__panelBridge.openModal('{이름}', 'dismissible')` 또는 `__panelBridge.openModal('{이름}', true)`
- [ ] (선택) `layout.json` → `panels.modalGroups`에 그룹 등록 (상호 배타)
- [ ] 큰 모달이면 `<panel-meta>`로 `maxWidth` / `maxHeight` 기본값 선언
- [ ] 최상위 root에 `box-sizing: border-box; width: 100%; max-width: 100%; min-width: 0;` 적용
- [ ] 일반 모달은 가로 스크롤이 생기지 않게 설계 (긴 행/그리드는 줄바꿈 또는 내부 재배치)
- [ ] **필수 모드(`true`)면 패널 내부에 상태 해제 트리거가 반드시 존재** (`sendMessage` / `closeModal` / `__modals` 패치 버튼) — 시스템 X·ESC가 막혀 있어서 내부 버튼이 없으면 유저가 갇힘. 그 버튼은 초기 렌더 상태에서 즉시 보여야 함

### 풀스크린 패널 (`full-screen`)
- [ ] `panels/{번호}-{이름}.html` 파일 생성
- [ ] `layout.json` → `panels.placement.{이름}` = `"full-screen"`
- [ ] `variables.json` → `__modals.{이름}` = `false` (초기값) — modal과 동일한 on/off
- [ ] 열기: `__panelBridge.openModal('{이름}', 'dismissible')` 또는 `true` (필수 모드)
- [ ] 화면 전체를 덮으므로 패널 내부에서 자체 헤더/네비/스크롤 영역을 설계 (시스템 chrome은 닫기 버튼만 제공)
- [ ] 배경 클릭으로 닫히지 않음 — dismissible여도 X 버튼 또는 ESC로만 닫힘
- [ ] 적합 용도: 타이틀 화면, 엔딩 컷씬, 전체화면 미니게임, 큰 매핑/지도 UI 등 다른 모든 UI를 완전히 가려야 하는 경우
- [ ] **🚨 패널 내부에 상태 해제 트리거가 반드시 존재해야 함** — 배경 대화창마저 안 보이는 풀스크린에서 이건 옵션이 아니라 의무다. dismissible이라도 X 버튼 하나에만 의존하지 말고 패널 본문에 명시적인 진행/닫기 버튼(`__panelBridge.sendMessage(...)` 또는 `__panelBridge.closeModal('{이름}')`)을 두자. 비동기 액션이 실패해도 재시도/닫기 경로가 남아 있어야 함

**모달 동작 원리:**
- 모달 패널은 **항상 마운트**되어 있다 (`display:none`으로 숨김). 닫아도 DOM과 핸들러가 유지된다.
- 패널 액션 핸들러(`registerAction`)는 모달이 닫혀있을 때도 살아있어서, 선택지 액션이 모달을 열지 않고 직접 실행할 수 있다.
- **모달이 다시 열릴 때 (active: false→true) 스크립트가 자동 재실행된다.** 따라서 대회, 모험 등 매번 초기화가 필요한 패널도 정상 동작한다.
  - **예외: `<panel-meta>{"mount": "once"}</panel-meta>` 모달은 다시 열려도 재실행되지 않는다** (상태 보존이 목적이므로). 열릴 때 초기화가 필요하면 `stateChanged`에서 `d.__modals['{이름}']`의 false→truthy 전환을 보고 직접 처리하라.
- `autoRefresh: false`는 이제 대부분의 모달에서 불필요하다 — 모달이 열릴 때마다 자동으로 재초기화되므로.

**모달 박스 모델 요약:**
- 크기 우선순위는 `layout.json`의 `panels.modalSize` → 패널의 `<panel-meta>` → 시스템 기본값 순서다
- `<panel-meta>.maxWidth`는 **패널이 실제로 원하는 내용 폭**으로 해석한다
- 시스템은 자기 chrome(바깥 inset, 본문 padding)을 감안해 최종 외곽 폭을 계산한다
- 패널은 항상 부모 폭 안으로 들어가야 하며, 일반 모달에서 가로 스크롤은 버그로 본다
- 세로 스크롤은 공용 wrapper 또는 패널 내부 중 한 곳만 책임지게 설계한다

**🚫 모달 CSS 안티패턴 — 절대 하지 마라:**

```css
/* ❌ 잘못된 모달 CSS — 시스템 wrapper와 충돌하여 내부 스크롤이 중복 생성됨 */
.modal {
  max-width: 720px;      /* ← layout.json의 modalSize / <panel-meta>로 처리할 것 */
  max-height: 80vh;      /* ← 시스템 wrapper가 viewport 기준으로 처리함 */
  overflow-y: auto;      /* ← 공용 wrapper가 이미 스크롤 제공함 */
}
```

```css
/* ✅ 올바른 모달 CSS — 시스템에 맡기고 스타일만 작성 */
.modal {
  background: ...;
  color: ...;
  padding: 24px;
  border-radius: 14px;
  border: 1px solid ...;
  font-family: ...;
  /* max-width/max-height/overflow는 건드리지 않는다 */
}
```

크기 제어가 필요하면 `<panel-meta>`로 선언하고, 스크롤은 항상 시스템 wrapper에 맡겨라. 패널 내부에 `overflow-y: auto`나 `max-height`를 박으면 **이중 스크롤바**가 생겨 UX가 깨진다 — 매우 흔한 신참 실수다.

모달 크기와 root 규칙의 상세 기준은 반드시 루트 `panel-spec.md`의 "모달 박스 모델 규칙" 섹션을 먼저 읽고 따른다.

### 독 패널 (dock 계열)
- [ ] `panels/{번호}-{이름}.html` 파일 생성
- [ ] `layout.json` → `panels.placement.{이름}` = `"dock"` / `"dock-left"` / `"dock-right"`
- [ ] `variables.json` → `__modals.{이름}` = `false` (모달과 동일한 on/off)
- [ ] (선택) `layout.json` → `panels.dockWidth`, `panels.dockHeight` 크기 설정 (`dockSize`는 예전 이름 — `dockHeight`를 쓴다)
- [ ] `dock-left`/`dock-right`는 **무대 레이아웃(데스크톱)과 모바일에서 모달로 승격**된다 — 그 화면에서도 쓸 만한지 확인 (`dock`/`dock-bottom`은 무대에서도 채팅 컬럼 안에 그대로)

### 인라인 패널
- [ ] `panels/{번호}-{이름}.html` 파일 생성 (placement 등록 **안 함**)
- [ ] AI 프롬프트에서 `$PANEL:이름$` 토큰 사용법 안내
- [ ] (선택) `session-instructions.md`에 인라인 패널 사용 지침 추가

### 팝업 이펙트
- [ ] `popups/{이름}.html` 파일 생성 (panels/ 아님)
- [ ] 트리거 코드: `showPopup('{이름}')` (패널) 또는 `__popups` (엔진)
- [ ] 팝업 전용 변수가 필요하면 `vars` 옵션으로 전달

---

## 패널 액션 시스템

패널이 외부에서 호출 가능한 액션을 제공할 때, **패널 액션**으로 선언한다. 패널 액션은:

- AI 선택지가 참조하는 유일한 액션 체계 — AI는 `{panel: "...", action: "..."}` 형식으로 선택지를 구성한다
- 패널 버튼과 선택지가 **동일한 실행 경로**를 공유한다 — 액션 핸들러가 primary 로직
- 실행 시 자동으로 히스토리에 기록되어 AI에게 `[ACTION_LOG]`로 전달된다
- `available_when` 조건에 따라 `[AVAILABLE]` 헤더로 AI에게 현재 가능한 액션이 알려진다
- `needs_ui` 플래그로 모달 표시 여부가 결정된다 — UI 연출이 있는 액션은 모달을 열고, 없는 액션은 백그라운드에서 실행된다

### `<panel-actions>` 메타데이터 선언

패널 HTML 최상단에 `<panel-actions>` 태그로 메타데이터를 선언한다. 이 태그는 패널 로드 전에도 파싱 가능하며, 핸들러 없이도 available 목록에 포함된다:

```html
<panel-actions>
[
  {
    "id": "advance_slot",
    "label": "스케줄 진행",
    "description": "현재 슬롯의 활동을 실행한다 (일별 시뮬레이션 애니메이션 포함)",
    "available_when": "turn_phase === 'executing' && current_slot < 3",
    "needs_ui": true
  }
]
</panel-actions>

<style>
  /* ... 패널 스타일 ... */
</style>
```

**필드:**
| 필드 | 필수 | 설명 |
|------|------|------|
| `id` | ✅ | 액션 식별자. `registerAction()`의 첫 번째 인자와 일치해야 함 |
| `label` | ✅ | AI에게 보여지는 짧은 설명 |
| `description` | ✅ | 액션의 상세 설명 |
| `params` | | 파라미터 맵 `{ "param_name": "설명" }`. AI가 선택지에 params를 넣을 수 있음 |
| `available_when` | | `variables.json` 변수를 참조하는 JS 표현식. 생략 시 항상 available |
| `needs_ui` | | **기본값: `true`**. 선택지에서 이 액션을 실행할 때 모달을 열어서 UI 연출을 보여준다. `false`로 명시하면 모달을 열지 않고 백그라운드에서 실행한다. 엔진만 호출하고 시각적 피드백이 없는 액션(스케줄 확정, 변수 수정 등)이나 **도크처럼 `__modals`로 표시되는 상시 패널의 액션**에 `false`를 설정한다 — 생략하면 선택지로 실행될 때마다 그 패널을 모달로 열었다 닫는다(`__modals` 쓰기 + 재렌더). 예외: `false`여도 핸들러가 아직 등록되지 않았으면(패널 미마운트) 핸들러 로드를 위해 모달을 한 번 연다. **사이드바(`left`/`right`)·무대(`main`) 패널은 상주 배치라 `needs_ui`와 무관하게 시스템이 모달을 열지 않는다** — 핸들러 등록만 기다렸다가 실행하고, main 패널이면 먼저 그 탭으로 전환한다. 무대 패널은 늘 보이므로 연출이 필요하면 패널 안에서 직접 보여주면 된다(의도 표시로 `false`를 적어도 무해). boolean만 인정 — `"false"` 같은 문자열은 무시되어 기본값 `true`로 동작한다. |

### `registerAction()` 핸들러 등록

`<script>` 블록에서 `__panelBridge.registerAction()`으로 런타임 핸들러를 등록한다. **이 핸들러가 패널 액션의 primary 로직이다** — 모든 실행 경로(버튼, 선택지)가 이 핸들러를 통과한다:

```javascript
// 핸들러 등록 — 이것이 이 액션의 유일한 실행 로직
__panelBridge.registerAction('buy_item', async (params) => {
  const res = await __panelBridge.runTool('engine', {
    action: 'buy_item', item: params.item_id, qty: params.qty || 1
  });
  if (res.result?.success) {
    await __panelBridge.queueEvent(`[구매: ${params.item_id} × ${params.qty || 1}]`);
    // UI 피드백, 애니메이션 등
  }
});

// 버튼은 executeAction으로 위임 — 인라인에 로직을 넣지 않는다
shadow.querySelector('.buy-btn')?.addEventListener('click', async function() {
  this.disabled = true;
  await __panelBridge.executeAction('buy_item', {
    item_id: this.dataset.item, qty: 1
  });
});
```

### `executeAction()` 실행

`executeAction()`은 레지스트리를 통해 핸들러를 호출하고, 히스토리에 자동 기록한다:

```javascript
// 패널 내부에서 호출 (패널 이름 자동 감지)
await __panelBridge.executeAction('advance_slot');

// 파라미터 전달
await __panelBridge.executeAction('confirm_schedule', {
  schedule_1: 'private_school',
  schedule_2: 'job_farm',
  schedule_3: 'job_farm'
});
```

### 패널 액션 체크리스트

서버 연동이 있는 패널을 만들 때:

- [ ] `<panel-actions>` 태그로 메타데이터 선언 (id, label, description, available_when)
- [ ] `registerAction()`으로 핸들러 등록 — 여기에 모든 비즈니스 로직 (runTool + UI 연출)
- [ ] UI 버튼의 클릭 이벤트에서 `executeAction()` 호출 — 인라인 로직 금지
- [ ] AI 선택지 형식 확인: `{"panel": "패널이름", "action": "액션id", "params": {...}}`

---

## 패널 복잡도 스펙트럼

패널은 용도에 따라 세 단계로 나뉜다. 가장 단순한 수준부터 시작하고, 필요할 때만 복잡도를 올려라:

| 수준 | 구성 | 예시 |
|------|------|------|
| **정적 표시** | Handlebars + CSS만 | 프로필 카드, 로그, 상태 요약 |
| **클라이언트 인터랙션** | + `<script>` (탭, 아코디언, 모달 열기) | 탭 UI, 퀵 버튼, 토글 |
| **서버 연동** | + `runTool` / `sendMessage` / `queueEvent` | 상점, 전투, 스케줄 설정 |

단순 정보 표시에 엔진 연동이 필요 없고, 탭 UI에 서버 통신이 필요 없다. 과설계하지 마라.

---

## 패널 생성 워크플로우

### Step 1: 요구사항 → 배치 타입 결정

| 용도 | 배치 타입 | 근거 |
|------|-----------|------|
| 상시 표시 요약 (HP, 스탯, 프로필) | `left` / `right` | 항상 보이는 사이드바 |
| 게임플레이 흐름 UI (스케줄, 슬롯 진행, 대회) | `modal` | 필수 조작, ESC 닫기 불가 |
| 보조 조작 UI (인벤토리, 상점, 카탈로그) | `modal-dismissible` | 필요할 때 열고 닫음, ESC 닫기 가능 |
| 진행 컨트롤 (슬롯 진행 버튼) | `dock` / `dock-right` | 채팅 옆에 항상 접근 가능 |
| 캐릭터 일러스트 / 씬 이미지 | `left` / `dock-left` | 시각적 참조용 |
| 일회성 선택지 (거래, 퀴즈) | 인라인 (`$PANEL:이름$`) | 대화 흐름에 자연 삽입 |
| 전체화면 인터랙션 (전투, 모험) | `modal` + `autoRefresh: false` | 복잡한 JS 상태 보존 |
| 타이틀 / 엔딩 / 컷씬 / 전체화면 연출 | `full-screen` | 배경 대화·패널 완전히 가림, 100vw × 100vh |
| 패널이 본체인 작업 화면 (원고 뷰어·편집기, 대시보드, 보드) | `main` (무대 레이아웃) | 중앙 무대에 탭으로 상시 표시, 채팅은 우측 컬럼으로 비켜남 |
| 긴 본문 뷰어·편집기·캔버스 (스크롤·입력 보존 필요) | 아무 배치 + `<panel-meta>{"mount": "once"}</panel-meta>` | 한 번 마운트, `stateChanged`로 부분 갱신 |

**결정 기준:**
- 항상 보여야 하는가? → 사이드바
- 사용자가 주로 **패널을 보고 조작하고 대화는 곁들이는가**? → `main` (무대). 대화가 본체인 RP면 쓰지 않는다
- 필요할 때만 열리는가? → 모달
- 게임 플레이 중 상시 접근? → 독
- 대화 흐름에 자연 삽입? → 인라인
- CSS 애니메이션 / 복잡한 JS 상태? → `autoRefresh: false` 추가
- 데이터가 바뀔 때마다 다시 그리면 스크롤·작성 중 입력이 날아가는가? → `mount: "once"` + `stateChanged` (템플릿 수정은 새로고침해야 반영된다는 점 감안)

### Step 2: 데이터 모델 설계

패널이 읽을 데이터를 **먼저** 설계한다 (UI보다 데이터가 선행):

- 매 턴 변하는 동적 값 → `variables.json`
- 구조화된 정적/반정적 데이터 → 커스텀 `*.json`
- 규칙 기반 조작이 필요 → `tools/engine.js` 액션 추가

**variables.json 규칙:**
- 게이지형 변수는 `_max` 짝 필수: `hp` + `hp_max`
- 변수명은 영문 `snake_case`
- 상황 변수 포함: `location`, `time`, `mood`, `outfit` 등
- 하드코딩 금지: 패널에서 최댓값이나 문자열을 직접 쓰지 말고 변수 참조
- `__` 접두사는 시스템 예약: `__modals`, `__popups` 등

→ 데이터 설계 상세: `references/engine-and-data.md`

### Step 3: HTML 작성

파일을 `panels/{순서번호}-{이름}.html` 로 생성. 숫자 prefix가 표시 순서를 결정하고, UI에서는 자동 제거된다.

**기본 구조:**
```html
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
  :host { font-family: 'Noto Sans KR', sans-serif; }

  .panel-root {
    background: linear-gradient(135deg, #2a1f3d 0%, #1e1630 100%);
    border-radius: 12px;
    padding: 14px;
  }
  /* 컴포넌트 스타일 */
</style>

<div class="panel-root">
  <div class="header">{{name}} · {{age}}세</div>
  <div class="bar-row">
    <div class="bar-fill hp" style="width:{{percentage hp hp_max}}%"></div>
  </div>
  {{#if (gt stress 70)}}<div class="warning">스트레스 과다!</div>{{/if}}
</div>

<script>
  // shadow는 Shadow Root 참조 — 시스템이 자동 주입한다 (아래 "스크립트 환경" 참조)
  shadow.querySelector('.some-btn')?.addEventListener('click', () => {
    __panelBridge.openModal('inventory', 'dismissible');
  });
</script>
```

→ Handlebars 헬퍼 & CSS 패턴 상세: `references/helpers-and-patterns.md`

> **`<select>` 색상 처리:** `layout.json`의 `theme` 토큰 (`accent`, `bg`, `text`, `border` 등)이 모든 select의 닫힌 컨트롤·드롭다운 팝업·호버/선택 하이라이트에 자동 적용된다. 패널 HTML에 select 색상 CSS를 박지 마라. 크기/폰트 조정만. 상세는 `helpers-and-patterns.md`의 "Form 컨트롤 다크 테마" 섹션.

### Step 4: 레이아웃 등록

`layout.json`의 `panels.placement`에 이름 등록 (파일명에서 숫자 prefix 제거):

```json
{
  "panels": {
    "placement": { "inventory": "modal" }
  }
}
```

모달/독이면 `variables.json`의 `__modals`에도 초기값 추가:
```json
{ "__modals": { "inventory": false } }
```

`left`/`right`/`main`은 상시 표시라 `__modals`가 필요 없다. 허용 배치 값은 `left`, `right`, `main`, `modal`, `modal-dismissible`, `full-screen`, `dock`, `dock-left`, `dock-right`, `dock-bottom` — 이 밖의 값(오타 포함)을 쓴 패널은 **어디에도 표시되지 않는다** (`npm run lint:data`가 경고).

### Step 5: 인터랙션 연결

→ 아래 "핵심 인터랙티브 패턴" 섹션과 `references/bridge-api.md` 참조

---

## 배치 타입 상세

### 사이드바 (`left` / `right`)
- 세션 내내 항상 표시, `panels.size` (기본 300px) 너비
- `showProfileImage: false` — 좌측 사이드바의 프로필 이미지 숨기기
- 무대 레이아웃에서는 `right` 사이드바가 채팅 컬럼 바로 왼쪽에 붙는다

### 무대 (`main`) — 무대 레이아웃
`main`이 하나라도 있으면 화면이 `[좌측 사이드바][중앙 무대][우측 사이드바][우측 채팅 컬럼]`으로 바뀐다. 없으면 기존 화면 그대로.

```json
{
  "panels": { "placement": { "목차": "left", "원고": "main", "트리트먼트": "main" }, "leftSize": 300 },
  "chat": { "width": 420 }
}
```

- **탭**: main 패널이 파일 순서대로 탭이 된다. 1개면 탭 바 없이 꽉 채움, 2개 이상이면 상단 탭 바(≈36px, 테마 토큰). ←/→·Home/End 키 이동
- **마운트 유지**: 비활성 탭도 언마운트하지 않고 `display:none` — 스크롤·입력·스크립트 상태 보존. 숨은 탭의 타이머도 계속 돈다
- **크롬 없음**: 사이드바 카드(제목·테두리·여백) 없이 무대 칸을 채운다 → 배경·여백·제목은 패널 root 책임. 세로 스크롤은 무대 칸이 제공
- **탭 기억**: `localStorage["stageTab:" + sessionId]` (목록에 없으면 첫 탭)
- **탭 전환 API**: `__panelBridge.focusPanel('원고')`. 선택지 액션의 `panel`이 main이면(`__open` 포함) 자동으로 그 탭 전환 — 모달은 열지 않는다
- **채팅 컬럼**: 폭 `chat.width` (기본 420, 최소 320, 무대가 480px 이상 남도록 상한), 왼쪽 가장자리 드래그로 조절(자동 저장), 접기 버튼 → 44px 레일(`localStorage["stageChatCollapsed:" + sessionId]`). 접혀도 채팅은 마운트 유지, 패널이 `fillInput()`하면 자동 펼침. 입력창은 압축 배치(첫 줄 입력창+전송, 나머지 버튼은 둘째 줄)
- **채팅 컬럼 안**: 선택지·인라인 패널·`dock`/`dock-bottom`은 그대로. `dock-left`/`dock-right`는 모달로 승격
- **겹침**: 토스트·최소화 모달 칩은 CSS 변수 `--stage-right-inset`(채팅 컬럼 폭)만큼 비켜서 무대 우하단에 뜬다
- **모바일(<768px)**: 상태바에 `무대 | 채팅` 전환(기본 무대, 둘 다 마운트 유지). `focusPanel`이면 무대로, `fillInput`이면 채팅으로 자동 전환. 채팅 폭·접기는 미적용
- **앱 모드 우선**: `layout.app`이 있으면 무대는 켜지지 않고 main 패널은 어디에도 렌더되지 않는다. `chat.width`도 무시
- 재렌더 때 스크롤·입력이 날아가면 곤란한 무대 패널(원고 뷰어 등)은 `mount: "once"`와 같이 쓴다 (아래)

### mount-once (`<panel-meta>{"mount": "once"}</panel-meta>`) — 배치 무관 opt-in
- 최초 HTML로 한 번 그리고 스크립트도 **한 번만** 실행. 이후 HTML이 바뀌어도 다시 그리지 않고 타이머·리스너·`on()` 구독은 패널이 사라질 때까지 유지
- 갱신 채널은 **`stateChanged`** 하나 — 페이지가 패널 데이터가 바뀔 때마다 전역으로 한 번 발송(앱 모드는 AppSlot), detail = 전체 데이터(`__panelBridge.data`와 같은 객체)
- 계약: 실행 시점에 `__panelBridge.data`로 초기 렌더 → `on('stateChanged', d => …)`에서 **서명 비교 후 바뀐 조각만** DOM 수정 (초당 여러 번 올 수 있다)
- **템플릿 파일 수정은 브라우저 새로고침 전까지 반영 안 됨**
- 컨테이너별: 사이드바·무대 = 그대로 / 모달·풀스크린 = 다시 열어도 재실행 안 됨 / 독 = 탭 전환 시 새로 마운트 / 인라인 = 메시지 인스턴스마다 한 번
- `autoRefresh: false`와 차이: 그쪽은 서버가 재렌더를 안 하는 것(템플릿 수정은 즉시 반영), mount-once는 클라이언트가 바뀐 HTML을 무시하는 것(패널 HTML에 선언 → 패널과 함께 이동)

```html
<panel-meta>{"mount": "once"}</panel-meta>
<article class="body"></article>
<script>
  var lastSig = null;
  function render(d) {
    var ch = (d.manuscript && d.manuscript.current) || {};
    var sig = ch.id + ':' + ch.rev;
    if (sig === lastSig) return;   // 관심 있는 조각만 비교
    lastSig = sig;
    shadow.querySelector('.body').innerHTML = ch.html || '';
  }
  render(__panelBridge.data);
  __panelBridge.on('stateChanged', render);
</script>
```

### 모달 (`modal`)
- `__modals.{name}`이 truthy일 때 표시
- `true` = 필수 (ESC/X/배경 클릭 닫기 불가), `"dismissible"` = 자유롭게 닫기
- 여러 모달 겹침 가능 (z-index 자동 증가, ESC는 최상위만 닫음)

### 풀스크린 (`full-screen`)
- `__modals.{name}`이 truthy일 때 표시 (modal과 동일한 제어)
- viewport 전체(100vw × 100vh)를 덮고, 배경은 `--bg` 색으로 불투명 — 뒤의 대화/패널을 완전히 가린다
- 둥근 모서리/그림자/외곽 여백 없이 전체화면 — 패널 내부에서 자체 레이아웃을 책임진다
- 일반 모달보다 더 높은 z-index에 렌더링 (항상 최상위)
- 배경 클릭으로 닫히지 않음 — `"dismissible"`일 때만 X 버튼 / ESC로 닫힘
- 용도: 타이틀, 엔딩, 컷씬, 전체화면 미니게임 등

> 🚨 **스턱 방지 규칙 (모달·풀스크린 공통, 풀스크린은 특히 필수):**
>
> 필수 모드(`true`)는 시스템 X 버튼도 ESC도 작동하지 않는다. 그래서 **패널 내부에 상태를 해제할 수 있는 트리거가 반드시 있어야 한다** — 없으면 유저가 영구히 갇힌다. 풀스크린은 배경 대화창마저 안 보이므로 dismissible여도 같은 원칙 적용.
>
> - 진행 버튼: `__panelBridge.sendMessage('계속한다')` — AI 턴이 진행되며 패널이 자동으로 닫힘
> - 명시적 닫기: `__panelBridge.closeModal('{이름}')`
> - 상태 패치: `__panelBridge.updateVariables({ __modals: { '{이름}': false } })`
>
> 그 버튼은 패널 초기 렌더에서 **즉시 보여야** 한다 (조건 분기 깊은 곳에서야 등장하면 안 됨). 비동기 액션이 실패해도 재시도/닫기 경로가 살아 있어야 한다.

**🎯 모달 열기/닫기 — 패널 측에선 전용 API 우선, 엔진 측에선 함정 주의:**

모달 상태 변경은 두 경로가 있다:

| 경로 | 사용처 | API |
|---|---|---|
| **전용 도구 (권장)** | 패널 JS, onclick | `__panelBridge.openModal(name, mode)` / `__panelBridge.closeModal(name)` |
| **엔진 변수 패치** | engine.js에서 액션 후 자동 열기/닫기 | `v.__modals = { ...v.__modals, name: true|"dismissible"|false }` |

**책임 분리 권장 패턴**:
- 엔진은 **상태 데이터**만 관리 (`_pending_awaken` 등 modal 내용)
- 엔진은 mark/rank_up 같은 액션 직후 `__modals.X = true`로 모달을 **열어주기만** 함 (사용자가 패널 버튼으로 따로 여는 게 불가능한 상황)
- 모달 **닫기는 패널이 onclick에서 `__panelBridge.closeModal()` 호출**로 처리. 엔진은 closeAction에서도 데이터만 정리하고 `__modals` 안 건드림

**🚫 엔진에서 모달 닫을 때 — `delete` 금지, 명시적 `false` 필수:**

만약 엔진에서 닫아야 한다면, 서버 route(`/api/sessions/[id]/tools/[name]`)는 엔진이 반환한 `result.variables.__modals`의 **entries만 순회**하여 변경을 적용한다. 키를 `delete`로 제거하면 entry가 없어서 변경이 감지되지 않고 기존 `true` 상태가 그대로 남는다.

```js
// ❌ 잘못된 패턴 — 모달이 안 닫힘
function closeMyModal(v) {
  const m = { ...v.__modals };
  delete m["my-modal"];   // ← entries에 없으므로 서버가 무시
  v.__modals = m;
}

// ✅ 올바른 패턴 — 명시적 false 전송
function closeMyModal(v) {
  v.__modals = { ...(v.__modals || {}), "my-modal": false };
}
```

서버의 처리 로직: `value && value !== false && value !== null` → 열기, 그 외 → `modals[name] = false` (닫기). 따라서 `false`, `null`, `undefined` 어느 거든 닫기로 처리되지만, **그 키가 entries에 존재해야** 트리거됨.

**모달 그룹** — 상호 배타적 UI 흐름:
```json
"modalGroups": {
  "gameplay": ["schedule", "advance", "competition", "inventory"],
  "overlay": ["portrait", "values"]
}
```
같은 그룹 모달이 열리면 나머지 자동 닫힘. 그룹 없는 모달은 독립 동작.

### 독 (`dock` 계열)
| 타입 | 위치 | 특성 |
|------|------|------|
| `dock` / `dock-bottom` | 채팅↔입력 사이, 전체 너비 | 같은 방향 여러 독 → 탭 |
| `dock-left` / `dock-right` | 채팅 영역 안, float + sticky | 겹치는 메시지 너비 축소 |

- `dockWidth` (px) — dock-left/right 너비 (기본 auto, min 280, max 50%)
- `dockHeight` (px) — 모든 독 최대 높이 (기본 50vh). `dockSize`는 예전 이름
- `__modals`로 on/off 제어
- **모달 승격**: 모바일에서는 모든 독이, 무대 레이아웃(데스크톱)에서는 `dock-left`/`dock-right`가 모달로 승격된다

### 인라인 (배치 없음)
- AI가 응답에 `$PANEL:이름$` 토큰 삽입 → 해당 위치에 렌더링
- 해당 메시지에서만 표시, 일회성 인터랙션에 적합
- 인라인에서도 `<script>` + Bridge API 사용 가능

---

## 핵심 인터랙티브 패턴

### A) 채팅 전송
```javascript
btn.addEventListener('click', () => __panelBridge.sendMessage(btn.dataset.action));
```

### B) 패널 액션 (엔진 호출 + 상태 변경)
서버 연동이 있는 패널은 **반드시 패널 액션을 사용하라**. 인라인 핸들러에 runTool을 직접 넣지 않는다:

```javascript
// 1. 핸들러 등록 (primary 로직)
__panelBridge.registerAction('buy_item', async (params) => {
  const res = await __panelBridge.runTool('engine', {
    action: 'buy_item', item: params.item_id, qty: params.qty || 1
  });
  if (!res.result?.success) throw new Error(res.result?.message || '구매 실패');
  await __panelBridge.queueEvent(`[구매: ${params.item_id} × ${params.qty || 1}]`);
});

// 2. 버튼 → executeAction 위임
shadow.querySelector('.buy-btn')?.addEventListener('click', async function() {
  this.disabled = true;
  try {
    await __panelBridge.executeAction('buy_item', {
      item_id: this.dataset.item, qty: 1
    });
  } catch { this.disabled = false; }
});
```

**왜 이 패턴인가:**
- AI 선택지와 UI 버튼이 **같은 핸들러**를 호출하여 동작이 동일
- `executeAction()`이 실행을 히스토리에 자동 기록 → `[ACTION_LOG]`에 반영
- `available_when` 조건으로 AI에게 현재 가능한 액션만 `[AVAILABLE]`로 노출

### C) 모달 열기/닫기/토글
```javascript
__panelBridge.openModal('inventory', 'dismissible');
__panelBridge.closeModal('inventory');
// 토글
const isOpen = (__panelBridge.data.__modals || {}).inventory;
isOpen ? __panelBridge.closeModal('inventory') : __panelBridge.openModal('inventory', 'dismissible');
```

### D) AI에게 맥락 전달
패널 액션 핸들러 내부에서 `queueEvent`를 호출하여 AI에게 맥락을 전달한다. 패널 액션을 사용하면 `[ACTION_LOG]`에도 자동 기록되므로, `queueEvent`는 추가 디테일이 필요할 때만 사용:

```javascript
// 패널 액션 핸들러 안에서 — 상세 결과를 AI에게 전달
__panelBridge.registerAction('use_item', async (params) => {
  const res = await __panelBridge.runTool('engine', { action: 'use_item', item: params.item });
  if (res.result?.success) {
    const fx = Object.entries(res.result.effects || {}).map(([k,v]) => `${k}${v>0?'+':''}${v}`).join(', ');
    await __panelBridge.queueEvent(`[아이템사용: ${params.item} → ${fx}]`);
  }
});
```

### E) 클라이언트 전용 UI (탭)
```javascript
shadow.querySelectorAll('.tab').forEach(tab => {
  tab.addEventListener('click', () => {
    shadow.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    shadow.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    tab.classList.add('active');
    shadow.getElementById(tab.dataset.tab)?.classList.add('active');
  });
});
```

### F) autoRefresh: false 패널에서 수동 데이터 갱신
```javascript
__panelBridge.on('turnEnd', () => {
  const d = __panelBridge.data;
  shadow.querySelector('.hp').textContent = `${d.hp}/${d.hp_max}`;
});
```

### G) 퀵 버튼 → 모달 (사이드바 + 모달 연계 패턴)
사이드바에 요약 정보 + 버튼을 두고, 클릭하면 상세 모달이 열리는 패턴. 이것이 **progressive disclosure** — 간결한 사이드바에서 한 번의 클릭으로 상세 UI에 접근:
```html
<div class="quick-btns">
  <button class="qbtn" id="openSchedule">📅 스케줄</button>
  <button class="qbtn" id="openInventory">🎒 인벤</button>
</div>
<script>
  shadow.querySelector('#openSchedule')?.addEventListener('click',
    () => __panelBridge.openModal('schedule', 'dismissible'));
  shadow.querySelector('#openInventory')?.addEventListener('click',
    () => __panelBridge.openModal('inventory', 'dismissible'));
</script>
```

### H) 패널 간 신호 + 무대 탭 전환 (`emit` / `focusPanel`)
사이드바 목차에서 장을 고르면 무대의 원고 패널이 그 장을 띄우는 식의 연계. `emit(name, detail)`은 `panel:` 네임스페이스 이벤트라 시스템 이벤트를 사칭할 수 없고, 사이드바·무대 패널에서는 구독이 자동 정리된다:
```javascript
// 목차 패널 (left)
btn.addEventListener('click', () => {
  __panelBridge.emit('chapter-select', { id: btn.dataset.chapter });
  __panelBridge.focusPanel('원고');   // main이면 그 탭 활성화(모바일은 무대 뷰), modal 계열이면 dismissible로 열기
});

// 원고 패널 (main)
__panelBridge.on('panel:chapter-select', (detail) => showChapter(detail.id));
```
- `emit`의 `name`은 자유로운 채널 이름이다 (패널 이름일 필요 없음). 받는 쪽은 반드시 `'panel:' + name`
- `focusPanel`은 `left`/`right`/dock/인라인 패널에는 아무 일도 하지 않는다. 이미 열린 모달은 건드리지 않는다(필수 모달을 dismissible로 낮추지 않음)

→ Bridge API 전체 메서드: `references/bridge-api.md`

---

## 팝업 이펙트

화면 중앙에 일시적으로 표시되는 연출용 오버레이. `popups/` 디렉토리에 HTML 파일 작성.

```html
<!-- popups/level-up.html -->
<style>
  .popup-content { text-align: center; padding: 12px; }
  .title { font-size: 22px; font-weight: 800; color: var(--popup-primary); }
</style>
<div class="popup-content">
  <div class="title">LEVEL UP!</div>
  <div>Lv. {{level}}</div>
</div>
```

**트리거:**
```javascript
// 패널에서
await __panelBridge.showPopup('level-up', { duration: 4000, vars: { level: 10 } });

// 엔진에서
return { variables: { __popups: [{ template: 'level-up', duration: 4000, vars: { level: 10 } }] } };
```

- 큐 기반 순차 재생, 다음 비-OOC 메시지 시 자동 클리어
- `--popup-primary`, `--popup-glow` CSS 변수로 테마 연동
- 진입 (scale 0.7→1 + fade in) / 퇴장 (scale 1→0.9 + fade out) 애니메이션 자동

---

## 자동 갱신 제어

```json
{ "panels": { "autoRefresh": { "portrait": false, "competition": false } } }
```

| 값 | 동작 |
|---|---|
| `true` (기본) | 변수/데이터 변경, AI 턴 종료 시마다 재렌더링 |
| `false` | HTML 템플릿 파일이 직접 수정될 때만 재렌더링 |

**`false`가 필요한 경우:**
- CSS 애니메이션 보존 (진행 도트, 전투 이펙트)
- 복잡한 JS 상태 유지 (전투 시뮬레이션, 슬롯 진행)
- `__panelBridge.on('turnEnd')` 로 필요한 데이터만 수동 갱신

템플릿 수정까지 막고 패널 단위로 선언하고 싶거나, 데이터 변경마다 정확히 갱신받고 싶다면 `autoRefresh: false` 대신 **mount-once** (`<panel-meta>{"mount": "once"}</panel-meta>` + `stateChanged`)를 쓴다 — 위 "배치 타입 상세"의 mount-once 절.

---

## 턴 기반 연출 오케스트레이션

패널의 기믹적 깊이는 "무엇을 보여주는가"가 아니라 **"언제 보여주고 언제 숨기는가"**에 있다.

### 2-Phase 아키텍처

하나의 턴 진행에 두 개의 의미 단위가 있을 때, 이를 분리하여 각각 독립된 AI 서사를 받는 구조:

```
Phase 1: [엔진: 행동 처리] → [AI 서사: 무엇을 했는가]
            ↓ turnEnd
Phase 2: [엔진: 시간 진행] → [팝업 연출] → [AI 서사: 무엇이 달라졌는가 (silent)]
```

**설계 철학:**
- **행동 결과와 시간 진행을 분리** — "검술 연습을 마쳤다"와 "겨울이 찾아왔다"는 다른 서사 단위
- **엔진은 즉시, 연출은 지연** — 데이터는 빠르게 갱신하되, 팝업/모달은 AI 서사 완료 후에
- **Silent Message** — 유저에게 보이지 않는 메시지로 AI 턴을 트리거. `sendMessage(text, { silent: true })`
- **조건부 2턴** — 시간 진행에 중요 이벤트가 있을 때만 2턴, 없으면 조용히 전환
- **유저에게 주도권** — AI가 모달을 직접 열지 않고, 인라인 트리거 버튼으로 유저 타이밍에 맞춤
- **원샷 훅** — `turnEnd` 리스너를 한 번 실행하고 즉시 해제하여 누적 방지

```javascript
// 2-Phase 대표 패턴: 행동 결과 → AI 서사 → turnEnd → 시간 진행 → 팝업 → silent AI 서사
async function finalize(result) {
  await queueEvent(buildSlotSummary(result));  // Phase 1: 행동 결과만
  sendMessage('[진행]');

  if (result.pending_transition) {
    const unsub = __panelBridge.on('turnEnd', async () => {
      unsub();
      const tr = await runTool('engine', { action: 'turn_transition' });
      if (tr.result?.popups) showPopups(tr.result.popups);      // 팝업 즉시
      if (tr.result?.needs_narration)
        sendMessage(buildMonthSummary(tr.result), { silent: true }); // Phase 2
    });
  }
}
```

→ 전체 패턴 (지연 팝업, 지연 모달, 스트리밍 가드, 애니메이션 잠금, silent message, 2-phase 전환, 크로스 패널 통신, 위상 기반 가시성 등): `references/turn-choreography.md`

---

## 🚨 차단 패널 + AI 서사 동시 트리거 금지

**핵심 원리: 화면을 가리는 패널(모달 / 풀스크린)이 열린 상태에서 AI 서사 턴을 트리거하지 마라.**

### 왜 문제인가

사용자가 버튼을 누르면 흔히 두 가지가 동시에 발생한다:
1. `PB.openModal('어떤_패널')` — 차단 패널 즉시 표시
2. `PB.sendMessage('[이벤트] /narrate-X 스킬로 묘사하라', { silent: true })` — AI 서사 턴 트리거

이 조합은 **항상 나쁜 UX**다:
- AI 응답은 보통 수 초~수십 초 걸린다 (특히 thinking 모델은 더 김)
- 그동안 사용자는 차단 패널을 멍하니 응시 — 인터랙션 불가
- 서사가 끝나도 차단 패널 뒤에 가려져 있어 **읽으려면 패널을 닫아야 함**
- 즉 "서사 보러 가는데 두 번 더 클릭 필요" — 서사 자체가 묻힘

### 페르소나 톤별 적용 우선순위

- **서사 중심 페르소나** (단일 캐릭터 RP, 채팅이 메인 콘텐츠) — 거의 무관. 차단 패널 자체를 적게 씀
- **게임형 페르소나** (관리 시뮬레이션, 디펜스, RPG, 카드게임 등 — 서사가 backdrop) — **반드시 지켜야 함**. 사용자는 게임 화면을 보고 싶어 하지 서사를 읽으려 그 화면을 닫고 싶어 하지 않음

### 해결 패턴 — 우선순위

#### Pattern A — 서사만 트리거, 모달 오픈은 사용자에게 양도 (최선)
```javascript
// 사이드바 "런 시작" 같은 트리거 버튼
async function startRun() {
  await callEngine('start_run');
  PB.sendMessage('[런 시작] 챕터 1 분위기를 짧게 묘사하라.', { silent: true });
  // ❌ PB.openModal('nodemap'); — 열지 않음
  // 사용자는 서사를 다 읽은 뒤 사이드바의 "🗺 노드 맵" 버튼을 직접 누름
}
```
**장점:** 서사를 차분히 읽을 시간 확보 + 사용자의 페이스로 게임 진행. **사이드바 메뉴가 명확하게 보이는 경우에만** 유효.

#### Pattern B — 서사 끝에 인라인 전환 버튼 (사이드바가 약할 때)
AI 응답의 마지막에 `<choice>` 태그로 인라인 액션 버튼을 포함하게 하라. 사용자가 서사를 읽고 버튼 하나로 다음 패널로 진입.
```markdown
<!-- 페르소나 narrate 스킬 가이드 -->
응답 마지막에 반드시 다음 형식의 choice를 포함:
<choice>
[
  { "text": "🗺 노드 맵 열기", "score": 0, "dry": true, "actions": [{ "tool": "engine", "action": "open_modal", "params": { "modal": "nodemap" } }] }
]
</choice>
```
**장점:** 인라인 통합.

**⚠ 중요: `dry: true`는 choice 객체 레벨에 둬야 함, action에 두면 무시됨.** 디스패처가 `choice.dry`를 읽지 `action.dry`가 아니다 (`ChatInput.tsx:386`). 잘못된 형태로 안내하면 AI가 그대로 복사해서 인라인 버튼 클릭이 정상 메시지처럼 AI 턴을 소비한다.

```json
❌ { "text": "...", "actions": [{ "tool": "...", "action": "...", "dry": true }] }
✅ { "text": "...", "dry": true, "actions": [{ "tool": "...", "action": "..." }] }
```

#### Pattern C — 모달 자동 닫고 서사 → turnEnd로 다시 열기 (모달이 필수일 때만)
사용자가 이미 모달 안에서 어떤 액션을 했고, 그 결과 모달을 보존하면서 서사도 필요할 때.
```javascript
async function pickNode(nodeId) {
  await callEngine('enter_node', { node_id: nodeId });
  // 1) 차단 패널 즉시 닫기
  if (PB.closeModal) PB.closeModal('nodemap');
  // 2) 서사 트리거
  PB.sendMessage(`[노드 진입] /narrate-node 짧게.`, { silent: true });
  // 3) 턴 종료 후 다음 패널 열기 (원샷 훅)
  const unsub = PB.on('turnEnd', () => {
    unsub();
    PB.openModal('combat');
  });
}
```
**장점:** 서사 보는 동안 차단 X, 자동 전환. **단점:** 사용자가 서사를 다 읽기 전에 다음 패널이 떠버릴 수 있음 — turnEnd가 LLM 응답 직후라 너무 빠를 수 있다. 가능하면 A나 B를 선호.

### 게임형 페르소나에서 흔한 안티패턴

❌ **"버튼 누르면 모달 열고 서사 동시 발사"**
```javascript
async function enterShop() {
  await callEngine('enter_node', ...);
  PB.openModal('shop');                            // 차단 패널 즉시 표시
  PB.sendMessage('[상점 진입] ...', { silent:true }); // 동시에 서사 트리거
  // → 사용자: 상점 화면 보면서 AI 응답 기다리고, 끝나도 상점 가려져서 안 보임
}
```

✅ **올바른 형태 (Pattern A)**
```javascript
async function enterShop() {
  await callEngine('enter_node', ...);
  PB.sendMessage('[상점 진입] ...', { silent: true });
  // 모달 안 엶. 사용자가 서사 읽고 사이드바 메뉴 클릭으로 상점 진입
}
```

✅ **혹은 (Pattern C — 자동 전환 필요할 때)**
```javascript
async function enterShop() {
  await callEngine('enter_node', ...);
  PB.closeModal('nodemap');                        // 기존 차단 패널 정리
  PB.sendMessage('[상점 진입] ...', { silent: true });
  PB.on('turnEnd', function once() {               // 원샷 훅
    PB.off?.('turnEnd', once);
    PB.openModal('shop');
  });
}
```

### 사이드바 패널의 역할

게임형 페르소나에서 **사이드바는 단순 정보 표시가 아니라 "주 메뉴"**다. 차단 패널에 대한 모든 진입점은 사이드바 메뉴 버튼에 노출되어야 사용자가 서사 후 능동 전환 가능. 사이드바 메뉴가 없으면 Pattern A가 작동하지 않으니 Pattern B (인라인 choice 버튼) 필수.

### 서사가 정말 짧으면?

만약 서사가 1줄 정도로 매우 짧을 거라 확신한다면 Pattern C도 무리 없다. 그러나 LLM 응답 시간은 예측 불가하므로 **기본은 A or B**. 차단 패널과 서사의 동시 트리거는 "예외적으로 안전이 보장될 때만" 허용.

---

## 주의사항 & 안티패턴

1. **Shadow DOM 접근**: `document.querySelector` ❌ → `shadow.querySelector` ✅ (자동 주입)
2. **패널에 상태 저장**: DOM/변수에 저장 ❌ → JSON 파일에 저장 ✅
3. **하드코딩**: `style="width:50%"` ❌ → `style="width:{{percentage hp hp_max}}%"` ✅
4. **연타 방지**: 비동기 버튼에 `btn.disabled = true` 필수
5. **엔진 반환값 추측 금지**: 엔진 코드를 읽고 실제 반환 구조 확인 후 필드 참조
6. **이벤트 중복 등록**: `autoRefresh: true` 패널에서 `on(event)` 사용 시 재렌더링마다 리스너 누적 — 단 사이드바·무대 패널은 시스템이 재렌더 때 `on()` 구독·`window` 리스너·타이머를 자동 해제한다. 모달·독·인라인은 직접 정리할 것
7. **모달 직접 조작보다 API 우선**: `updateVariables({ __modals })` 대신 `openModal()`/`closeModal()` → 그룹 로직 자동 적용
8. **커스텀 데이터 네임스페이스**: `world.json` → `{{world.locations}}` (파일명이 키)
9. **시스템 파일 접근 불가**: `session.json`, `layout.json`, `chat-history.json` 등은 데이터 로딩에서 제외
10. **JSON 데이터를 JS로 전달**: Handlebars에서 복잡한 객체를 직접 쓸 수 없을 때 `{{json (lookup this "file-name")}}` → `<script type="application/json">` 패턴 사용
11. **인라인 핸들러에 서버 로직 금지**: 클릭 핸들러에서 `runTool` 직접 호출 ❌ → `registerAction`에 로직을 등록하고 버튼은 `executeAction`으로 위임 ✅. 인라인 핸들러에 로직을 넣으면 AI 선택지가 같은 동작을 재현할 수 없고, 히스토리에 기록되지 않는다
12. **`<panel-actions>` 누락**: 서버 연동 액션이 있는 패널은 반드시 `<panel-actions>` 메타데이터를 선언해야 AI가 해당 액션을 인지하고 선택지에 포함할 수 있다
13. **중복 호출자 설계 금지 (Single-caller 위반)**: 같은 연산(상태 변경·시간 진행·자원 증감 등)을 여러 레이어가 호출할 수 있게 설계 ❌ → 호출 창구를 한 곳(대개 엔진 내부 또는 패널 핸들러)에 몰아넣고 상위 레이어는 호출하지 않는다 ✅. 예: 시간 진행이 있는 엔진 액션이라면 그 액션 내부에서 시간 전진도 같이 처리하고, 패널·선택지·AI는 이 액션만 부른다. 호출자가 갈라지는 순간 중복 실행 버그의 씨앗이 된다
14. **AI 시야 밖 상태 변경 금지**: 상태 변경을 하는데 `[ACTION_LOG]`·`[STATE]`·`queueEvent` 중 어디에도 흔적이 안 남는다면 AI는 그 변경을 모른다 → 유저 텍스트에서 유추하다가 재실행·상태 불일치 발생. 상태를 바꿨으면 반드시 AI가 읽을 수 있는 채널로 노출한다

---

## 참조 문서

상세한 레퍼런스가 필요할 때 아래 파일을 읽어라:

| 파일 | 내용 | 언제 읽나 |
|------|------|-----------|
| `references/helpers-and-patterns.md` | Handlebars 헬퍼 전체 목록, CSS 디자인 패턴 (게이지/태그/그리드/버튼/탭/카드/애니메이션) | 패널 HTML/CSS 작성 시 |
| `references/bridge-api.md` | Bridge API 전체 메서드·이벤트, 이미지 리소스 사용법 | 인터랙티브 기능 추가 시 |
| `references/engine-and-data.md` | 엔진 스크립트 인터페이스, 액션 디스패처, 데이터 파일 설계, hint-rules.json | 엔진/데이터 구조 작업 시 |
| `references/turn-choreography.md` | 턴 사이클 타이밍 제어: 지연 팝업, 지연 모달, 스트리밍 가드, 애니메이션 잠금, 원샷 훅, 크로스 패널 통신, 위상 기반 가시성 — 9가지 연출 패턴 | 턴 기반 연출·타이밍 제어가 필요할 때 |

세션에 `panel-spec.md`가 있으면 기술 명세의 원본으로 참조할 수 있다.
