---
name: authoring-service
description: 바깥 서비스(services[].url = 원격 MCP 문, services[].api = 원격 REST 베이스)를 붙이고 그 자격을 잇는 법. 자격 계약(auth — kind·scheme·required·fields·accounts·inject·help·verify)과 여러 호스트(bases) 선언, OAuth 인가(등록된 앱·콜백 주소·제공자 방언), 동사가 ctx.service(이름).fetch()·connected()·fields()·account() 로 닿는 규율, GET 으로 오는 호출(scripts.get), 키 유무에 따라 화면이 "연결하러 가기" 안내로 물러나는 패턴. 패키지가 Unsplash·OpenAI·Notion·인스타그램처럼 키가 필요한 바깥 API 에 닿아야 하면 선언하기 전에 먼저 읽어라. 채널(사람이 들어오는 문)은 authoring-channel 이 다룬다.
---

# 바깥 서비스 잇기

바깥 서비스는 **나가는 문**이다. 내 동사가 남의 몸(REST·MCP)을 부른다. 채널(들어오는 문 —
남이 나에게 말을 건다)과 성질이 반대라 선언 자리가 다르고(`services[]` vs `surfaces.channels[]`),
자격을 쥐는 쪽도 다르다: 채널 어댑터는 자격 전체를 env 로 받지만, **서비스 자격은 동사의 손을
영영 지나지 않는다** — 기판이 호출 시점에 헤더를 붙인다.

세 규율. 이걸 어기면 키를 넣어도 영영 안 켜진다.

1. **키는 vault 에만.** 매니페스트에는 형태(`auth`)만, 코드에는 아무것도.
2. **동사는 `ctx.service(이름)` 하나로 닿는다.** `ctx.secret`, `process.env.X_KEY`, 키를 손에 쥔
   직접 `fetch` 는 없는 문이다.
3. **키를 넣는 화면은 기판의 연결 화면 하나다.** 패키지 화면은 안내와 딥링크(`/connect`)까지만.

## 선언

```yaml
services:
  - name: unsplash
    api: https://api.unsplash.com        # REST 베이스 — 동사의 요청은 이 접두 밖으로 못 나간다
    auth:
      kind: token
      scheme: Client-ID                  # Authorization 접두 (미선언 = Bearer)
      required: false                    # 없어도 돌고 그 기능만 꺼진다 (미선언 = true: 없으면 주 기능이 안 선다)
      fields:                            # 입력 칸 — 미선언이면 토큰 문자열 한 칸(붙여넣기)
        - { key: access_key, label: Access Key, header: true }   # 정확히 하나가 헤더로 나간다
        - { key: app_id, label: Application ID }                 # 비밀 아닌 칸 — 동사가 fields() 로 읽는다
      help:
        url: https://unsplash.com/oauth/applications
        note: "없어도 무료 저장소(Openverse)로 동작합니다 — 연결하면 Unsplash 사진 검색이 켜집니다."
      verify:
        url: https://api.unsplash.com/photos?per_page=1   # 2xx 면 유효 — "저장됨 ≠ 유효" 를 기판이 판정한다
```

| 축 | 뜻 | 빠지면 |
|---|---|---|
| `kind` | `none` · `token` · `oauth`. oauth 는 인가 흐름이 토큰을 만들고, `fields` 는 로그인이 묻지 않는 부속 값만 받는다 | 자격 없는 문 |
| `scheme` | 헤더 접두. token 형에서만, `inject` 와 함께 쓸 수 없다 | Bearer |
| `inject` | 자격이 실리는 자리 — `{query: <이름>}` · `{form: <이름>}`. 토큰을 파라미터로 받는 API 용. api 형에서만 | Authorization 헤더 |
| `accounts` | **계정 축.** true 면 자격이 계정마다 하나(`<패키지>/<서비스>@<계정>`) | 서비스당 자격 하나 |
| `required` | **필수/선택.** false = 없어도 돌고 그 기능만 꺼진다. 연결 화면이 이 축으로 "필요"(사이드바 배지에 세어진다)와 "선택"을 가른다 | true |
| `fields` | 입력 칸. 칸 어휘는 채널 `credential.fields` 와 같고, `header: true` 만 서비스 전용. key 있는 칸들이면 vault 에 JSON 으로 앉고 header 칸만 헤더로 나간다 | 토큰 문자열 한 칸 |
| `help.note` | **이 키가 있으면 무엇이 켜지는지.** 연결 화면이 그대로 보여 준다 — 사용자가 키를 얻으러 갈 이유다 | 이름만 보인다 |
| `help.url` | 발급처 | 링크 없음 |
| `verify.url` | 저장 뒤 실왕복 한 번 | 저장만 됨(유효 판정 불가) |

`bases:` 는 같은 자격이 나가는 **다른 호스트**다(교환이 다른 도메인에 사는 제공자). 적으면 그 접두도
같은 판정을 지나고 고지서에 함께 선다 — 두 번째 서비스를 만들어 같은 비밀을 두 좌표에 앉히지 마라.

MCP 문이면 `api:` 대신 `url:` 로 선언하고 `auth` 는 같다. 동사는 `ctx.service(이름).call(도구, 인자)` 로
부른다 — **내 에이전트는 그 서버의 도구를 직접 보지 않는다.** 서비스는 언제나 동사가 감싸서 소비된다.
`tools:` 는 이 서버의 도구 중 **다른 앱에 raw 로 빌려줄 수 있는 것**의 목록(제공자 쪽 캡)이다. 빌리는 앱이
`edges[].agent_access: full` 을 선언해야 그쪽 세션에 raw 로 서고, 없으면 허락(결재) 자체가 거부된다.
raw 로 열 이유가 없으면 `tools:` 를 적지 마라. 칸에는 `note` 가 없다 —
칸의 설명은 `label`, 서비스의 안내는 `help.note` 다(판정이 거부한다).

## 계정이 여럿이면 — `accounts: true`

같은 서비스를 계정 여럿으로 쓰는 앱(계정 셋을 관리하는 인스타 데스크 같은)은 **자기 비밀 보관소를
짓지 마라.** 축이 문법에 있다:

```yaml
  - name: instagram
    api: https://graph.instagram.com
    auth:
      kind: oauth
      accounts: true                     # 자격이 계정마다 하나 — 좌표는 <패키지>/instagram@<계정>
      inject: { query: access_token }    # 이 API 는 토큰을 헤더가 아니라 질의로 받는다
      fields:                            # 로그인이 주지 않는 값 — 인가 번들 안에 함께 앉는다
        - { key: user_id, label: 계정 번호 }
```

```ts
const ig = ctx.service("instagram");
for (const handle of await ig.accounts()) {          // 앉아 있는 계정들
  const one = ig.account(handle);                    // 그 계정의 자격으로 나가는 손잡이
  const { user_id } = await one.fields();
  await one.fetch(`/v23.0/${user_id}/media`, { method: "POST", body: new URLSearchParams({ caption }) });
}
```

고르지 않은 손잡이는 `accounts()` 와 `connected()`(하나라도 있는가)만 답하고 나머지 문은 사유와
함께 선다 — 자격이 여럿인데 아무거나 나가면 그건 캡이 아니라 우연이다.

## OAuth — 등록된 앱과 콜백 주소

`kind: oauth` 는 로그인이 자격을 만든다. 표준(디스커버리·DCR·PKCE·refresh)은 선언 없이 돌고,
`oauth_client` 에는 **표준이 답하지 못하는 것만** 적는다.

```yaml
    auth:
      kind: oauth
      client: registered                 # 자동 등록(DCR)이 안 되는 제공자 — 앱을 사람이 만든다
      oauth_client:
        client_id: "1234567890"          # 공개 식별자라 트리에 살아도 된다 (비밀은 연결 화면에서 vault 로)
        https: true                      # 콜백에 HTTPS 를 요구하는 제공자
        scopes: [business_basic, business_content_publish]
        auth_meta:
          authorization_endpoint: "https://www.instagram.com/oauth/authorize"
          token_endpoint: "https://api.instagram.com/oauth/access_token"
          exchange_endpoint: "https://graph.instagram.com/access_token"        # 단기 → 장기 (제공자 방언)
          exchange_params: { grant_type: ig_exchange_token }
          refresh_endpoint: "https://graph.instagram.com/refresh_access_token" # refresh_token 없이 회전
          refresh_params: { grant_type: ig_refresh_token }
```

- 콜백 주소는 **기판이 정한다**: `http://localhost:<포트>/oauth/cb` (TLS 문이 켜져 있으면 `https://…`).
  연결 화면이 그 주소를 복사할 수 있게 보여 주니, 제공자 앱 설정의 redirect_uri 에 그대로 붙여 넣게 안내하라.
  화면이나 동사가 자기 콜백 주소를 지어내면 안 된다.
- `https: true` 인데 기판의 TLS 문이 없으면 인가는 **시작 전에** 사유와 함께 막힌다(제공자의
  "redirect_uri 불일치" 는 원인을 말해 주지 않는다). 사용자에게 `RELAY_TLS_PORT` 를 켜라고 안내하라.
- 방언(`exchange_*`·`refresh_*`)은 반쪽만 적을 수 없다 — 파라미터만 적고 주소를 빠뜨리면 판정이 거부한다.

## GET 으로 오는 호출 — `scripts.get`

인가 리다이렉트·웹훅 검증은 `GET` 으로 온다. 동사 문은 원래 POST 하나이므로, 그 호출을 받으려면
동사를 지명한다:

```yaml
scripts:
  source: scripts
  get: [webhook-verify]
```

질의 문자열이 그대로 입력이고(같은 키가 여럿이면 배열), **문자열을 돌려주면 그것이 본문 전부**다
(검증 챌린지를 되돌려 주는 상대). 이 문에는 Origin 판정이 없다 — 아무 웹페이지나 두드릴 수 있으니
들어온 값을 세션의 인자가 아니라 **남의 질의 문자열**로 다뤄라. 인가 콜백은 이 문으로 받을 필요가
없다 — 기판의 `/oauth/cb` 가 이미 그 자리다.

## 동사 — 묻고, 부른다

```ts
export default async function (input: { q: string }, ctx: Ctx) {
  const photos = ctx.service("unsplash");
  // 선택 자격: 없으면 그 기능만 끄고 대체 경로로. 401 을 받아 보고 아는 것은 판단이 아니라 사고다
  if (!(await photos.connected())) return await searchOpenverse(input.q);
  const { app_id } = await photos.fields();        // 비밀 아닌 칸만 온다 — header·secret 칸은 절대 안 온다
  const res = await photos.fetch(`/search/photos?query=${encodeURIComponent(input.q)}`);   // Authorization 은 기판이 붙인다
  if (!res.ok) throw new Error(`Unsplash ${res.status}`);
  return { app_id, ...(await res.json()) };
}
```

필수 자격(`required` 미선언)의 동사는 `connected()` 를 묻지 않아도 된다 — 없으면 연결 화면이
이미 "필요" 로 세워 두고 배지를 켠다. 그래도 사람에게 돌아갈 메시지를 다듬고 싶으면 먼저 묻고
"사이드바의 연결에서 X 를 연결하세요" 를 돌려줘라. 전체 예: `references/optional-service.ts`.

## 화면 — 키 유무에 따라 물러난다

화면은 기판에 상태를 묻고(`GET {base}/services` — 값은 없고 `hasCred`·`required`·`help` 만 온다),
자격이 없으면 그 기능의 자리에 **입력칸 대신 안내와 딥링크**를 그린다. 딥링크는 `/connect?p=<설치
이름>&s=<서비스>` 하나다 — 콘솔 페이지 주소를 화면이 조립하지 않는다(설치 이름은 `__RELAY_CONTEXT
.instanceId`). 전체 조각: `references/connect-banner.html`.

```js
const ctx = window.__RELAY_CONTEXT;
const { services } = await (await fetch(`${ctx.base}/services`, { cache: "no-store" })).json();
const s = services.find((x) => x.name === "unsplash");
if (s && s.kind !== "none" && !s.hasCred) {
  banner.hidden = false;
  banner.querySelector("p").textContent = s.help?.note ?? `${s.name} 을 연결하면 이 기능이 켜집니다`;
  banner.querySelector("a").href = `/connect?p=${encodeURIComponent(ctx.instanceId)}&s=${encodeURIComponent(s.name)}`;
  stockButton.disabled = true;
}
```

연결 화면에서 잇고 돌아오면 다시 물어라 — `visibilitychange` 에 재조회. **화면에 키 입력칸을
두지 마라.** 사용자가 아무 화면에나 비밀값을 넣는 습관이 생기고, 그 화면에는 값을 vault 로 보낼
문도 없다. 미디어 뱅크의 "뱅크에서 고르기" 가 하듯, 없는 것은 안내하고 있는 것은 쓴다.

## 흔한 실수

- **`ctx.secret?.(…)`.** 없는 접근자다. 늘 undefined 라 키를 넣어도 영영 안 켜진다(실사고 2026-08-28:
  세 패키지가 이걸 쓰고 있었고 판정은 통과했다). 답은 `ctx.service(이름).connected()·fields()` 다.
- **`fields` 를 선언하고 `header: true` 를 빠뜨린다.** 판정이 거부한다 — 기판이 무엇을 헤더에
  넣을지 모른다.
- **칸에 `note` 를 적는다.** 칸의 설명은 `label`, 서비스 안내는 `help.note`.
- **선택 자격인데 `required` 를 안 적는다.** 연결 화면이 "필요" 로 세우고 배지를 켠다. 없어도
  돌면 `required: false` 다.
- **화면이 자기 키 입력칸을 만든다.** 위 절.
- **계정마다 다른 토큰을 패키지 폴더에 쓴다.** 축이 문법에 있다 — `auth.accounts: true` 를 선언하고
  `.account(<계정>)` 으로 골라라. 비밀 파일을 직접 쓰는 순간 "자격은 트리에 살지 않는다" 가 그
  패키지에서만 거짓이 된다.
- **토큰을 파라미터로 받는 API 에 자격을 손에 쥐고 직접 `fetch` 한다.** `auth.inject` 가 그 자리다.
- **교환이 다른 호스트에 사는 제공자 때문에 서비스를 둘로 쪼갠다.** `bases` 로 한 서비스에 담아라.

## 검증 순서

1. `relay validate` — 칸·header·required·inject·accounts 판정.
2. 발행 뒤 사이드바 [연결] — 그 줄이 필수/선택으로 맞게 서는가, `help.note` 가 뜻이 통하는가.
3. 키를 넣고 [검증] — 2xx.
4. 동사 실행 — 자격이 선언한 자리(헤더·질의·폼)로 붙어 나가는가(401 이면 `scheme`·`inject` 를 의심).
   계정 축이면 `.accounts()` 가 넣은 계정을 세는가.
5. 앱 화면 — 안내 배너가 기능으로 바뀌는가.
