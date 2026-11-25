---
name: agent-chat
description: 에이전트 패키지에 대화 표면(채팅)을 붙일 때 읽는다. 채팅 화면 선언, 기판 위젯 마운트, 화면 안 컴포넌트형 채팅, React 바인딩, 화면 맥락 주입까지. 패키지에 채팅·대화창·말풍선·도우미가 필요하거나 view에서 에이전트와 대화해야 하면 채팅 UI를 만들기 전에 이 문서를 먼저 읽어라.
---

# 에이전트 채팅 붙이기

에이전트 패키지의 화면(view)에 대화 기능을 넣는 방법을 다룬다. 결론부터 말하면
**채팅 UI 를 처음부터 만들 일은 거의 없다.** 기판(relay 데몬)이 완성된 채팅 클라이언트를
모든 패키지에 제공하고, 이 문서는 그것을 상황에 맞게 꽂는 방법이다.

## 기판이 주는 것

기판은 위젯 번들 한 벌을 정적 자산으로 서빙한다. 어느 패키지 화면에서든 URL 로 바로 불러 쓴다.

| 자산 | 무엇인가 |
|---|---|
| `/assets/chat-app.js` | 완성된 채팅 UI (ESM). 세션 탭, 첨부(선택·드래그·붙여넣기), 진행 표시, 이력 복원, 모델 설정 포함. `mount`·`mountTabs` 를 수출한다 |
| `/assets/chat-app.css` | 그 위젯의 스타일. **같이 링크해야 한다** — 빠뜨리면 마크업만 뜨고 레이아웃이 무너진다 |

번들은 하네스(에이전트 CLI)와의 연결지점이라 기판과 함께 갱신된다(no-store 서빙).
기판의 대화 API 가 바뀌면 번들도 같이 바뀌므로 화면이 깨지지 않는다. 직접 만든 채팅 UI 나
복사해 둔 사본에는 그 보장이 없다 — 조용히 어긋난다.

> 예전에는 `chat-widget.js`(UI)와 `chat-core.js`(headless) 두 자산이었다. 클라이언트 전송
> 계약 v1 컷에서 **한 번들로 합쳐졌고 구 이름은 서빙되지 않는다**. headless 소비는 아래
> 시나리오 4 를 보라.

## 좌표는 기판이 주입한다 — URL 을 파싱하지 마라

위젯은 자기가 어느 기판의 어느 인스턴스에 붙는지를 **주입으로만** 받는다. 패키지 view 를
서빙할 때 기판이 문서 머리에 심는다:

```html
<script>window.__RELAY_CONTEXT={base:"/pkg/<설치이름>",root:"",instanceId:"<설치이름>"};</script>
```

그래서 화면 코드는 설치 이름을 알 필요가 없다. **`location.pathname` 에서 `/pkg/<이름>/view`
를 파싱하던 구 관용구는 은퇴했다** — 마운트 문법(`/pkg/`·`/i/`)을 클라이언트가 조립하는 것은
계약 위반이고, 같은 패키지가 다른 마운트(조직 기판의 `/i/<id>`)에 서는 순간 깨진다.
좌표가 없으면 위젯은 조립을 시도하지 않고 콘솔에 판정을 남기며 마운트를 포기한다(fail-loud).

## 네 가지 시나리오

필요한 만큼만 내려가라. 위 시나리오로 충분하면 아래를 만들지 마라.

### 1. 대화만 있으면 된다 — 화면 없이

패키지가 대화형 도우미라 전용 화면이 필요 없는 경우. **아무것도 선언하지 않아도 된다** —
에이전트가 있고 `surfaces.view` 가 없으면 기판이 `/pkg/<이름>/view/` 에 전체 화면 대화를
세운다. 대화 표면은 선언이 아니라 `agents[]` 에서 도출된다.

첫 인사말만 얹고 싶으면 그 말을 하는 에이전트에 붙인다:

```yaml
agents:
  - name: 일기
    persona: agents/일기/AGENT.md
    greeting: 무엇을 도와드릴까요?
```

greeting 은 빈 대화의 시작 인사말로 그려지고, 세션 번들 meta.json 에도 그 에이전트 몫이
실린다. 에이전트가 여럿이면 인사말도 각자 갖는다 — 화면이 그리는 것은 착지 에이전트의 것이다.

### 2. 화면이 있고, 대화는 보조 — 자동 마운트

대시보드나 목록 같은 화면이 주인공이고 대화는 곁에 떠 있으면 되는 경우. view 문서에 두 줄:

```html
<link rel="stylesheet" href="/assets/chat-app.css">
<script type="module" src="/assets/chat-app.js"></script>
```

우측 하단에 부유 위젯이 자동으로 마운트된다. 대상 인스턴스는 기판이 주입한 좌표에서 온다.

### 3. 대화가 화면 안의 영역 — inline 수동 마운트

레이아웃의 한 영역(사이드 패널, 하단 반쪽)이 대화여야 하는 경우. 자동 마운트를 끄고
원하는 자리에 직접 심는다:

```html
<link rel="stylesheet" href="/assets/chat-app.css">
<script>window.RELAY_CHAT_MANUAL = true</script>
<div id="chat" style="height:520px"></div>
<script type="module">
  import { mount } from "/assets/chat-app.js";
  mount(document.getElementById("chat"), { title: "도우미" });
</script>
```

`mount(el, opts)` 의 첫 인자가 대상 엘리먼트다(구 판의 `mount({ target })` 은 은퇴).
`opts` 는 전부 선택이다 — `instanceId`(생략 시 주입 좌표) · `conversation`(이어 열 대화
스레드) · `title` · `onClose`(있으면 헤더에 접기 버튼이 생긴다). 반환값의 `unmount()` 로 건다.

여러 대화를 탭으로 열어야 하면 `mountTabs(el, opts)` 를 쓴다 — 반환값의 `openTab({ instanceId,
conversationId, title })` 로 탭을 연다.

### 4. 대화 UI 가 앱 디자인의 일부 — 계약 위에 직접 그리기

말풍선 하나, 한 줄 입력처럼 UI 자체가 앱 디자인에 녹아야 하는 경우에만. 길이 둘이다:

**(a) SDK 를 의존성으로** — `@relay/chat` 의 `createChat` 이 전송 큐·이력·업로드·세션
관리를 준다. 기판 레포 안에서는 `file:` 의존성으로 잡는다:

```js
import { createChat } from "@relay/chat";
const ctx = window.__RELAY_CONTEXT;
const chat = createChat({ base: ctx.base, root: ctx.root, instance: ctx.instanceId });
chat.on("message", (m) => render(m));   // { role: "user"|"bot"|"sys", text }
chat.on("busy", (b) => spinner(b));
await chat.send("질문");                 // { reply } 또는 { error: { code, message } }
```

**(b) 계약을 직접 말한다** — 전송 계약 v1 은 공개 문서(`docs/client-protocol.md`)라
fetch 두 번이면 된다: `POST {base}/turns` 로 열고(202 `{turn}`), `GET {base}/turns/<turn>/stream`
을 SSE 로 읽는다. 스트림의 마지막은 `{event:"turn",status:"settled"}` 다.

메서드·이벤트 표면은 [references/client-api.md](references/client-api.md) 에 있다.

## React 로 만든다면

시나리오 3·4 를 손으로 배선하지 말고 템플릿 [assets/relay-chat.tsx](assets/relay-chat.tsx) 를
view 소스에 복사하라. 세 가지가 들어 있다:

- `<RelayChat />` — 시나리오 3. 위젯을 inline 으로 심는 컴포넌트
- `useRelayCoords()` — 주입 좌표를 읽는 훅 (미주입이면 `null`)
- `sendTurn()` — 시나리오 4(b). 계약을 직접 말하는 최소 왕복 (개설 → 스트림 → 종결)

템플릿은 기판이 서빙하는 번들·계약을 런타임에 소비할 뿐이라 복사해도 썩지 않는다
(아래 "사본" 이야기는 번들 자체에 대한 것이다). 단, `<RelayChat />` 을 쓰는 화면에
시나리오 2 의 자동 마운트 script 를 같이 넣으면 부유 위젯이 중복으로 뜬다 — 하나만 쓴다.

## 화면 맥락 주입 — "지금 보는 것"을 알고 답하게

사용자가 보고 있는 탭이나 선택된 항목을 에이전트가 알고 답해야 한다면, `send` 의 `scene`
옵션에 화면 스냅샷을 실어라:

```js
await chat.send(질문, { scene: `화면: ${현재탭}\n선택: ${선택항목.id}` });
```

합성은 기판 몫이다 — 세션 프롬프트에는 서문으로 붙고, 말풍선과 대화 이력에는 질문 원문만
남는다(첨부와 같은 계약). 스냅샷은 "지금 보이는 것"의 요약이면 충분하다. 앱 상태 전체를
직렬화하지 마라.

맥락 주입 때문에 채팅 UI 를 재작성하는 것은 틀린 결론이다(2026-08 실측 — 빌더가 이 옵션을
몰라 위젯 전체를 다시 만들었다). 프롬프트를 손으로 합성해야 하는 특수한 경우에만 `display`
를 쓴다: `chat.send(맥락 + "\n" + 질문, { display: 질문 })`. 이력에 맥락이 섞여 남는 것이 차이다.

## 흔한 실수

- **구 자산 이름을 쓴다.** `/assets/chat-widget.js`·`/assets/chat-core.js` 는 서빙되지 않는다(404).
  번들은 `/assets/chat-app.js` 한 벌이고 CSS 를 같이 링크해야 한다.
- **CSS 를 빠뜨린다.** 스타일 링크 없이 번들만 로드하면 위젯이 뜨긴 뜨는데 레이아웃이 무너진다.
- **URL 에서 설치 이름을 파싱한다.** 좌표는 기판이 주입한다 — `window.__RELAY_CONTEXT` 를 읽어라.
- **사본을 뜬다.** 번들을 `public/` 에 복사하거나 빌드 산출물에 인라인하면 기판이 갱신될 때
  낡은 사본이 새 기판 API 와 어긋나 조용히 깨진다. 반드시 `/assets` URL 로 불러라.
- **위젯 내부 클래스로 스타일링한다.** 테마는 `--rc-accent`, `--rc-bg`, `--rc-ink`, `--rc-line`
  같은 `--rc-*` CSS 변수 재정의로 맞춘다. 내부 클래스는 계약이 아니라 언제든 바뀐다.
- **에이전트가 여럿인데 착지를 안 정한다.** 대화는 기본으로 패키지 짧은 이름과 같은 에이전트에
  착지한다. 특정 서브에이전트와의 대화창이면 `createChat({ agent })` 로 명시한다.

## 완성 확인

발행 후 `/pkg/<이름>/view/` 를 열어 위젯이 뜨고 한 턴이 오가는지 확인한다. 세션 이력, 첨부,
진행 표시, 모델 설정은 위젯이 공짜로 준다 — 이 중 하나라도 직접 구현하고 있다면 잘못된 길로
들어선 신호다. 위젯이 안 뜨면 콘솔부터 본다: 좌표 미주입이면 그 판정이 찍혀 있다.
