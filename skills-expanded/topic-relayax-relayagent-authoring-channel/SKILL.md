---
name: authoring-channel
description: 채널 어댑터(외부 대화 표면 — Slack, Discord, 텔레그램, 메일 등)를 저작할 때 읽는다. 상주 프로세스 계약, 게이트·slot·직렬화 규율, 자격 연결, 적합성 검사. 패키지에 "슬랙 봇", "디스코드 연동", "메신저로 대화" 가 필요하면 어댑터를 쓰기 전에 먼저 읽어라.
---

# 채널 어댑터 저작

채널은 **글루**다. 외부 이벤트를 착신으로, 회신을 외부 발화로 옮길 뿐 판단하지 않는다.
판단이 필요하면 착신하라 — 지능은 세션에 산다.

불변식: **채널의 모든 대화는 RELAY_API 를 통과한다.** 세션 이력·목록·담장·파일 무대가
전부 기판 장부라서, 장부를 우회한 대화는 기판이 이어가지도 복원하지도 못한다.
플랫폼 SDK 가 주는 "봇이 직접 답하기" 축으로 지능을 어댑터 안에 넣고 싶어질 텐데,
그 순간 대화가 장부 밖으로 나간다 — 어댑터는 운반만 한다.

## 시작 방법

1. **정본은 스키마다.** `relay.manifest.yaml` 의 `surfaces.channels` 주석이 프로세스 계약
   전문이다. 이 문서는 요약이라 어긋나면 스키마가 이긴다.
2. `references/slack.ts` 를 읽는다. 계약 전 조항(게이트·slot·직렬화·dedup·봉투·파일·
   발신·실패·검사)을 구현한 참조 구현이다. 복사해서 플랫폼 부분만 갈아끼우는 시작을 권한다.
3. `relay.yaml` 에 선언한다. 채널 이름은 서비스와 같은 자격 이름공간을 쓴다 —
   겹치면 판정이 거부한다.

   ```yaml
   surfaces:
     channels:
       - name: slack
         source: channels/slack
         entry: index.ts
   ```

4. 완료 기준: `relay validate` → 설치(conform 게이트 통과) → `relay harness-check <패키지>`
   → 실자격으로 왕복 한 번. 넷 다 지나기 전에는 완료가 아니다.

## 프로세스 계약 요약

기판 왕복의 정본은 **클라이언트 전송 계약 v1**(`docs/client-protocol.md`)이다.
구 블로킹 `POST …/chat` 은 은퇴했다 — 개설과 관찰이 분리된 아래 두 동사가 그 자리다.

기판이 entry 를 `node --experimental-strip-types` 로 스폰해 상주시킨다.

| 축 | 계약 |
|---|---|
| env | `RELAY_NAME` `RELAY_CHANNEL` `RELAY_API` `RELAY_TOKEN` + `RELAY_CRED_<이름>` (vault) |
| 착신 | ① 개설 `POST {RELAY_API}/pkg/{RELAY_NAME}/turns` body `{message, session, attachments?}` → **202** `{turn, session}` (턴 종결을 붙들지 않는다) ② 관찰 `GET …/turns/<turn>/stream` SSE |
| 관찰 | `data:` 한 줄 = 봉투 이벤트 JSON 하나. 어휘는 하네스 봉투 protocol 3 그대로 — `delta`·`tool`·`usage`·`task`·`ask`·`file`·`reply`·`error`. 종결은 `reply`/`error` 정확히 하나, **스트림의 끝은 수명주기 `{event:"turn",status:"settled",ok}`** 다. settled 없이 끊긴 스트림은 종결이 아니라 절단이므로 빈 답으로 위장하지 말 것 |
| 봉투 | message 는 `<channel source="<이름>" user="<안정 식별자>" ...>원문</channel>` — **user 필수**, 닉네임·시각은 속성으로 매 착신마다 |
| session | `<채널이름>-<대화키>` 를 `[a-zA-Z0-9._-]{1,64}` 로 정규화. 같은 외부 대화 = 같은 세션. 사람용 이름은 `POST …/sessions/<session>/rename` body `{label}` |
| 직렬화 | **기판이 세션의 유일한 직렬화 지점이다** — 같은 세션의 턴은 도착순으로 줄 선다. 어댑터 큐는 계약이 아니라 발신 순서를 지키기 위한 자기 몫이고, 끼어들기는 `POST …/turns/<turn>/interrupt` |
| dedup | at-least-once 플랫폼의 중복 이벤트 제거는 어댑터 소유 |
| 파일 | 회신 파일은 `file` 이벤트(`path` = stage 상대경로)로 도착 → `GET …/file/<경로>` 로 받아 네이티브 첨부로. 인바운드 첨부는 `POST …/upload` 로 stage 에 앉힌 뒤 참조를 `attachments` 로 |
| 발신 | stdin 줄 단위 JSON `{"type":"post","conversation":"…","text":"…","files":[…]?}` 수신 시 그 대화에 게시 — 트리거 선톡이 이 길로 온다 |
| 검사 | `RELAY_CONFORM=1` 스폰 시 자기 서술 JSON 한 줄(`{"name":"…","protocol":1}`) 내고 exit 0 |
| 검증 | `RELAY_VERIFY=1` + `RELAY_CRED_<이름>` 스폰 시 자격 실왕복 한 번(소켓·상주 없이)만 돌려 `{"ok":…,"note":"…"}` 내고 exit 0 — 저장과 유효를 가른다 |

## 규율

**게이트는 기본 닫힘, 판정 대상은 발화자다.** 착신은 전부 기판 주인의 권한으로 돌므로
게이트가 곧 보안 경계다. 방 ID 에 게이트하면 그 방의 전원이 통과해 버린다 — 그룹에서는
멘션·스레드 참여 같은 플랫폼 관례로 응답 범위를 더 좁혀라. allow 목록이 비었으면 전부
차단이 맞다. "일단 열어두고 나중에 잠그자"는 남의 발화가 내 권한으로 도는 기간을 만든다.

**ack 는 즉시, 처리는 뒤에.** 소켓·웹훅 플랫폼은 ack 가 늦으면 재전송한다. 턴이 끝나기를
기다렸다 ack 하면 긴 턴마다 중복 이벤트가 쌓인다 — 받자마자 ack 하고 dedup 으로 거른다.

**취소·오류 응답을 외부에 답인 양 내보내지 마라.** 끼어들기(cancel)로 끝난 호출의 오류는
새 턴이 흡수한다. 착신 실패는 외부에도 실패로 알리되, 내부 사정(토큰·경로·스택)은 싣지
않는다. `RELAY_TOKEN` 과 자격은 외부 대화에 절대 노출 금지 — 상세는 stderr 로 보내면
기판 로그(`~/.relay/logs/channels.jsonl`)에 남는다.

**프로세스 종료 = 실패다.** 네트워크 단절에 크래시로 답하지 마라 — 백오프 재접속은 어댑터
소유고, 기판은 죽은 어댑터를 되살리지 않는다(로그에 남길 뿐). 반대로 자격 불완전처럼
사람이 고쳐야 하는 상태는 fail-loud 로 즉시 죽어라 — 조용히 떠 있는 반쪽 어댑터는
로그도 없이 침묵한다.

**`RELAY_CONFORM=1` 문은 자격·네트워크 없이 즉시 답해야 한다.** 설치가 이 문으로 계약
준수를 판정한다. 자격 검사를 이 문 앞에 두면 자격 없는 기계에서 설치 자체가 막힌다 —
entry 최상단에서 분기하라. cwd 에 파일을 남기지도 마라 — conform 의 오염 검사가 잡는다.
임시 파일이 필요하면 `os.tmpdir()`.

**저장과 유효를 가르는 `RELAY_VERIFY=1` 문을 구현하라.** 자격이 vault 에 앉았다고 실제로
먹히는 건 아니다. 이 문은 주입된 자격으로 최소 왕복 한 번(Slack 이면 `auth.test`)만 돌려
`{"ok":true/false,"note":"…"}` 를 내고 종료한다 — **소켓을 열거나 상주로 흐르지 마라**
(GUI 의 "연결" 이 살아 있는 채널을 안 끊고 새 자격을 검증하는 근거). 이 문이 async 라면
하단의 상주 진입(`main()`)을 `if (process.env.RELAY_VERIFY !== "1")` 로 가드해야 한다 —
안 그러면 검증과 상주가 동시에 돈다. 미구현이면 화면은 "저장만" 으로 정직히 강등된다.

**의존성은 0 이 기본값이다.** Node 22+ 전역 `fetch`/`WebSocket` 로 대부분의 플랫폼이
붙는다. import 없는 단일 파일이면 CJS/ESM 판별과 무관하게 strip-types 로 그대로 돈다.
SDK 를 들이는 순간 그 패키지를 설치하는 모든 사용자가 그 의존성 트리를 신뢰해야 한다.

**여러 토큰이 필요하면 자격 하나에 JSON 한 줄.** vault 자리는 채널당 하나
(`relay connect <패키지> <채널이름>`)다. slack 참조 구현의 형:
`{"app_token":"xapp-…","bot_token":"xoxb-…","allow":["U…"]}` — 게이트 목록처럼
자격과 함께 움직이는 설정도 이 안에 싣는다.

## 선톡 — 트리거에서 채널로 먼저 말 걸기

트리거의 `then.delivery` 에 `<채널이름>:<대화키>` 를 적으면, 그 턴은 해당 대화의 slot
에서 돌고 reply 가 어댑터 stdin 으로 온다(`{"type":"post",…}`). 사용자의 후속 발화가
같은 slot 에 착신되어 대화가 이어진다.

```yaml
triggers:
  - id: morning-brief
    when: { cron: "0 9 * * 1-5", tz: Asia/Seoul }
    then:
      agent: my-agent
      prompt: 오늘의 브리핑을 정리해줘
      delivery: "slack:D0ABCDEF"   # <채널이름>:<플랫폼 대화키>
```

## 검증 순서

```sh
RELAY_CONFORM=1 node --experimental-strip-types channels/<이름>/<entry>   # 자기 서술 + exit 0
RELAY_VERIFY=1 RELAY_CRED_<이름>='<자격 JSON>' node --experimental-strip-types channels/<이름>/<entry>  # {"ok":…} + exit 0
relay validate <패키지 디렉토리>       # 선언·실체 판정
relay install <패키지 디렉토리>        # conform 게이트 포함
relay harness-check <패키지>          # 하네스 + 채널 적합성 일괄
relay connect <패키지> <채널이름>      # 자격을 vault 에
relay daemon                          # 스폰 확인 — 로그는 ~/.relay/logs/channels.jsonl
```

자격 없이 데몬을 먼저 띄워 fail-loud(기동 → 자격 없음 → exit 1 이 로그에 남는 것)를
확인하고, connect 후 재기동해 실왕복을 보는 순서가 빠르다.
