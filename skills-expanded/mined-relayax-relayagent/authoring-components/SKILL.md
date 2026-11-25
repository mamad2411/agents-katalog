---
name: authoring-components
description: 패키지가 다른 패키지의 화면에 컴포넌트를 내주거나, 남의 컴포넌트를 자기 화면에 마운트할 때 읽는다. 자립 번들 저작, mount 계약, import map 소비, 무빌드 화면과 번들형 view 의 차이까지. 화면 조각을 패키지 경계 너머로 재사용해야 하면 만들기 전에 이 문서를 먼저 읽어라.
---

# 컴포넌트 수출과 소비

패키지 화면의 한 조각을 다른 패키지가 쓰게 하는 축이다. 결론부터 말하면 **수출물은 자립
ESM 번들 하나이고, 소비자는 프레임워크도 빌드도 필요 없다.**

## 계약

수출은 파일 하나로 좁혀진다. 산출 디렉토리의 `index.js` 가 진입점이고, 수출은 하나다:

```js
export function mount(el, props) {
  // el 안에 그린다
  return { unmount() { /* 정리 */ } };
}
```

**스타일도 이 파일 안에 탄다.** 옆에 CSS 를 따로 내지 마라 — 소비자가 그 주소를 알아야 하는데
주소에는 제공자의 설치 이름이 들어간다(`/pkg/<설치이름>/components/index.css`). 같은 패키지가
다른 이름으로 서면 바로 깨진다. 소비자가 아는 것은 이름 하나, 부르는 것은 `mount` 하나다.

## 선언

```yaml
surfaces:
  components:
    source: surfaces/components   # 저작 트리
    out: dist                     # 빌드 산출. 미선언이면 source/index.js 를 그대로 서빙
```

`out` 을 선언하면 설치와 발행이 그 자리에서 `npm install` + `npm run build` 를 돈다.
빌드가 실패하면 설치가 실패한다. 손으로 쓴 ESM 한 장이면 `out` 을 빼라 — 그러면 빌드가
아예 없고, 대신 `source/index.js` 가 지금 실재해야 한다(판정이 잡는다).

### 사이드바에서의 자리 — 제공자는 소비자 밑으로 접힌다

부품을 내주는 패키지는 소비자가 그 부품을 결재하는 순간 사이드바에서 **그 소비자(허브) 밑으로
접힌다.** 판정은 선언이 아니라 장부의 결재다 — 허브 없이 이 패키지만 깐 사람에게는 이 줄이
유일한 문이라, 제공자 혼자서 "나는 접혀야 한다" 고 선언하지 않는다. 그래서 **기본은 손댈 것이
없다.** 어긋나는 두 경우만 최상위 `shell.nav` 로 말한다:

```yaml
shell:
  nav: always   # 부품도 내주지만 독립 앱으로도 서야 한다 — 결재가 있어도 늘 최상위
  # nav: never  # 목록에서 아예 뺀다(상세·직접 주소로는 닿는다) — 점검용·내부용 화면에
```

여러 패키지가 한 벌로 설치되는 구성(허브 하나 + 부품 여럿)이면 사용자에게 **묶음**을 권하라 —
`relay suite set <이름> --members <허브> --hub <허브>` 로 사이드바 폴더가 서고, `relay suite pack`
이 허브와 결재된 부품들을 봉투 하나(`.relaypackages`)로 굽는다(제공자가 먼저 앉도록 순서까지
적힌다). 받는 쪽은 사이드바 [+] → 파일 불러오기.

## React 로 저작하기

써도 된다. **React 는 번들 안에 들어가고 소비자에게는 보이지 않는다.** 채팅 위젯이 이미
그 모양이다. react 를 devDependencies 에 두고 번들러가 안으로 말아 넣게 하라:

```js
// build.mjs
import * as esbuild from "esbuild";
await esbuild.build({
  entryPoints: ["src/index.tsx"],
  bundle: true, format: "esm", outfile: "dist/index.js",
  jsx: "automatic", minify: true,
  loader: { ".css": "text" },   // CSS 를 문자열로 받아 번들 안에 태운다
});
```

```jsx
// src/index.tsx
import { createRoot } from "react-dom/client";
import css from "./panel.css";
import Panel from "./Panel";

let styled = false;
function ensureStyle() {
  if (styled || typeof document === "undefined") return;
  styled = true;
  const tag = document.createElement("style");
  tag.textContent = css;
  document.head.appendChild(tag);
}

export function mount(el, props = {}) {
  ensureStyle();
  const root = createRoot(el);
  root.render(<Panel {...props} />);
  return { unmount: () => root.unmount() };
}
```

**react 를 external 로 빼지 마라.** 번들이 작아지는 대신 소비자에게 "React 를 제공하라" 는
전제가 생기고, 그 순간 무빌드 화면이 이 컴포넌트를 못 쓴다. 크기가 걱정이면 번들을 잘게
쪼개지 말고 패키지당 하나로 굵게 유지하라.

## 소비

먼저 선언한다. 설치가 이 선언을 해석해 결재를 앉히고, 그 결재대로 기판이 소비자 문서에
import map 을 심는다:

```yaml
edges:
  - provider: "@local/ui@^1"
    components: true
```

**무빌드 화면(단일 HTML)** — 정적 import 로 끝난다. 주소를 조립하지 마라, 이름만 쓴다:

```html
<div id="panel"></div>
<script type="module">
  import { mount } from "@local/ui";
  mount(document.getElementById("panel"), { title: "재고" });
</script>
```

**번들형 view(`surfaces.view.out` 선언분)** — 여기는 다르다. 번들러가 bare 이름을 빌드
시점에 해석하려 들기 때문에 정적 import 가 통하지 않는다. webpack 이 건드리지 않는 동적
import 를 쓴다:

```jsx
useEffect(() => {
  let handle;
  import(/* webpackIgnore: true */ "@local/ui").then(({ mount }) => {
    handle = mount(ref.current, { title: "재고" });
  });
  return () => handle?.unmount();
}, []);
```

주석이 있어야 import 문이 산출에 그대로 남고 브라우저가 import map 으로 푼다.

**그리고 타입 선언이 필요하다.** 해석이 런타임이라 tsc 는 이 이름을 모른다 — 없으면 빌드가
`Cannot find module` 로 죽는다(next build 가 타입검사를 같이 돈다). view 소스에 한 장 둔다:

```ts
// surfaces/view/relay-components.d.ts
declare module "@local/ui" {
  export function mount(el: HTMLElement, props?: { title?: string }): { unmount(): void };
}
```

무빌드 화면은 타입검사가 없으니 이 파일도 필요 없다.

## 규율 셋

- **자립.** 번들은 자기 런타임을 안고 나온다. 소비자에게 프레임워크를 요구하지 마라.
- **스타일.** 번들이 자기 스타일을 안고 나온다(위 `ensureStyle`). 내부 클래스는 계약이
  아니다 — 테마는 CSS 변수로 열어라, 채팅 위젯의 `--rc-*` 가 선례다.
- **입자.** 이 축은 **기능 조각**의 형태다(패널, 목록, 지도 — 자기 사각형을 스스로 관리
  하는 것). 디자인 원자(Button, Card)를 이렇게 내보내지 마라: children 과 context 와
  ref 가 명령형 마운트 경계를 넘지 못하고, 런타임 사본이 번들마다 실린다.

## 흔한 실수

- **주소를 손으로 조립한다.** `/pkg/<이름>/components/index.js` 를 코드에 박지 마라.
  설치 이름은 설치 시점에 정해지고 같은 패키지가 다른 이름으로 두 벌 설 수 있다.
  이름으로 import 하면 기판이 푼다.
- **소스를 고치고 다시 굽지 않는다.** 데몬은 구운 번들을 서빙한다. `npm run relay -- build
  <패키지>` 로만 재빌드하라. `npm run validate` 가 낡은 산출물을 판정한다.
- **원자를 내보낸다.** 위 입자 규율을 보라.
- **제공자를 안 세우고 소비를 선언한다.** 설치가 fail-loud 로 잡는다 — 제공 패키지를
  먼저 설치하고 굽는다.
- **CSS 를 옆 파일로 내고 소비자에게 링크시킨다.** 그 주소에 설치 이름이 박힌다. 번들 안에
  태워라.

## 완성 확인

발행 후 소비자 화면을 열어 컴포넌트가 그려지는지 본다. 안 뜨면 콘솔부터 본다: import 가
404 면 제공자가 안 구워진 것이고, "Failed to resolve module specifier" 면 결재가 없는
것이다(edges 선언과 설치 해석을 확인하라).
