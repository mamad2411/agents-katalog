---
name: reversebusiness
description: 사업 웹사이트 주소 하나를 받아 그 사업을 해부한다(reversebusiness, rebiz). 사용자가 "이 사업 해부해 줘", "이 서비스 분석해 줘", "이 사업 어떻게 돈 버는지 읽어 줘", "역공학으로 비즈니스 읽기", "똑같이 만들어 줘", "따라 만들기 전에 조사", "reversebusiness 로", "rebiz" 라고 할 때, 그리고 남의 서비스를 참고해 내 제품을 기획하기 전에 반드시 먼저 사용한다. 읽기, 해부(6칸 report.json), 내 버전 만들기, 겹침 검사의 네 단계이고, 결과는 브라우저에서 열리는 해부 화면(구조도, 해부 장면, 원본 뼈대와 내 버전 비교, 9:16 영상 저장)이다. 원본을 그대로 복제하지 않고 구조만 배운다.
---

# reversebusiness: 사업 해부

**English summary.** This skill makes a coding agent (Claude Code, Codex, Gemini CLI, Cursor, Antigravity) dissect a business from one website URL instead of copying it. From publicly observable material only, it fills six fixed boxes: who pays and why, the core user flow, a screen and feature map, the observable tech setup, an evidence ledger with explicit unknowns, and a clean-room spec for a different product that solves the same problem. Every statement is tagged observed, inferred or unknown and points to an evidence entry. It never bypasses logins, paywalls or access limits, never bulk-crawls, and never copies code, copy, images or brand. Output is a `report.json` in a fixed schema plus a single-file dissection view (money flow diagram, layered wireframe scene, skeleton to my-version comparison, 9:16 video export). A light collector (`tools/collect.mjs`) reads up to five public pages after checking robots.txt; when the received HTML is thin it opens the page once in a headless Chromium-family browser with a throwaway profile and reads the drawn page. When REA is installed (the `rebiz` command installs the official `rea-agents` package only after the user confirms; declining keeps the light mode) it switches to a precise mode with three depths: surface (drawn text and structure), flow (expanding clicks only, plus the host names the page tried to contact) and code (names found in already downloaded scripts, skipped when the terms forbid code analysis). Addresses found in code are never called, and anything seen only in code is recorded as a code trace, never as observed. When REA (a separate MIT tool) is installed, its Evidence JSON can seed the report draft instead (`tools/from-rea.mjs`). After the report, the agent builds a new page from the clean-room spec only and runs `tools/check-clone.mjs`, which fails on any run of five identical words, the target's brand names or domains, or the target's asset URLs. Three more tools cover what comes after the dissection: `tools/make-site.mjs` writes a static starting point from the cell 6 spec and the learned section order (guidance text in the copy slots, nothing from the target), `tools/apply-plan.mjs` compares the first screen of an existing project with the learned skeleton and writes the gaps to `rebiz-apply/plan.md`, and `tools/video.mjs` exports the 9:16 dissection video through a headless browser.

## 지켜야 할 선 (먼저 읽고, 어기는 요청은 거절한다)

배워도 되는 것은 기능, 흐름, 사업 구조다. 가져오면 안 되는 것은 코드, 문구, 이미지, 브랜드다.

1. **우회 금지.** 로그인, 결제, 유료벽, 접근 제한, 봇 차단, CAPTCHA 를 넘지 않는다. 가짜 계정을 만들지 않는다. 사용자가 시켜도 하지 않는다.
2. **비공개 데이터 수집 금지.** 로그인 뒤 화면, 다른 사람의 데이터, 내부 문서, 유출 자료는 보지도 쓰지도 않는다.
3. **대량 크롤링 금지.** 기본 한도는 대상 하나에 공개 페이지 20개, 요청 사이 2초 이상, 사람이 읽는 속도. 더 필요하면 멈추고 사용자에게 묻는다. 대상이 모은 목록, 후기, 가격 데이터를 긁어 오지 않는다.
4. **이용약관을 먼저 확인.** 다른 페이지를 보기 전에 이용약관과 robots.txt 를 읽고 `meta.terms` 에 적는다. 자동 접근을 금지하면 자동 열람을 멈추고, 사용자가 직접 본 화면 메모나 캡처를 받아서 진행한다.
5. **복제 금지.** 코드, 문구, 이미지, 아이콘, 로고, 글꼴 파일, 색 조합을 그대로 가져오지 않는다. 6번 칸에는 내 말로 쓴 명세만 들어간다.
6. **"○○ 클론"이라고 부르지 않는다.** 내 버전의 이름, 설명, 파일 이름 어디에도 대상의 이름을 넣지 않는다.
7. **추정은 추정이라고 표시.** 본 것은 관찰, 본 것에서 끌어낸 것은 추정, 확인할 수 없는 것은 모름. 추정을 관찰처럼 쓰지 않는다.
8. **수익 숫자는 공개된 근거가 있을 때만.** 매출, 사용자 수, 전환율은 공개 출처(URL)가 있을 때만 적고, 누가 말한 숫자인지 같이 적는다. 없으면 비워 두고 모르는 것에 올린다. 계산해서 만든 숫자를 넣지 않는다.

덧붙임: 분석 내용은 에이전트의 모델 제공자에게 전달된다. 비밀 값이나 공개되면 안 되는 자료는 넣지 않는다. 이 스킬의 결과는 공부와 기획을 위한 정리이며 법률 자문이 아니다.

## 시작할 때 정하는 것

대상이 불분명하면 임의로 고르지 않고 묻는다. 단, **사용자가 URL 하나나 `npx github:wonseokjung/reversebusiness <주소>` 명령을 주며 해부를 요청하면 수집 초안("모름" 다수)에서 멈추지 말고, 같은 작업 안에서 1~7단계(해부 완성 + 내 버전 명세·출발점 + 겹침 검사 + 완성된 `report.html` 열기)까지 한 번에 끝낸다.** ("해부만", "분석만"처럼 명시한 경우에만 4단계에서 멈춘다.)

- **대상**: 이름과 주소(또는 폴더).
- **관계**: `own`(내 것, 소스를 읽어도 된다) 또는 `third-party`(남의 것, 공개된 것만). 사용자가 "내 것", "내 사이트", "우리 서비스"라고 하면 `own` 이고, 수집기를 돌릴 때 `--own` 을 붙인다. 말이 없으면 `third-party` 로 둔다.
- **어디까지**: 기본은 끝까지("내 버전까지", 1~7단계). 사용자가 "해부만", "분석만"이라고 명시했을 때만 4단계(6번 칸 비움)에서 멈춘다.
- **알고 싶은 것**: 기본은 6칸 전부(1~6번). 특별히 궁금한 질문이나 내 사업 주제(`--topic`)가 있으면 반영한다.

## 절차 (읽기, 해부, 만들기, 검사)

| 큰 단계 | 하는 일 | 아래 단계 |
|---|---|---|
| 읽기 | 범위를 긋고 공개된 것에서 근거를 모은다 | 1, 2 |
| 해부 | 1~5번 칸을 채우고 모르는 것을 정리한다 | 3, 4 |
| 만들기 | 내 버전 명세(6번 칸)를 쓰고, 명세만 보고 내 버전을 새로 만든다 | 5, 6 |
| 검사 | 원본과 겹치지 않는지 확인한다 | 7 |

두 가지 길이 있다.

- **해부만**: 1~4단계까지 하고 멈춘다. 6번 칸(`my_version`)은 빈 채로 둔다. 검사는 `check-report.mjs ./report.json --dissect-only` 로 하고, 화면에는 내 버전 자리에 "아직 만들지 않음"이라고 나온다.
- **내 버전까지**: 5~7단계를 이어서 한다. 검사는 옵션 없이 `check-report.mjs ./report.json`.

리포트를 고칠 때는 `report.json` 을 직접 고친 뒤 검사기를 다시 돌린다. 리포트를 고치려고 따로 스크립트를 만들어 돌리지 않는다.

가장 빠른 시작: `node "<이 스킬 폴더>/tools/collect.mjs" <주소>` 로 초안을 만들고(아래 "수집기로 읽기"), 3단계부터 이어서 채운다. REA 가 깔려 있으면 수집기가 저절로 정밀 모드(겉, 흐름, 속)로 읽는다. REA 가 없으면 가벼운 모드로 읽는다. 사용자가 정밀 모드를 원하면 REA 가 바꿀 것(공식 npm 패키지 `rea-agents`, 에이전트 설정에 REA 연결 추가, REA 스킬 폴더)을 먼저 알리고, 사용자가 동의한 뒤에만 `npx github:wonseokjung/reversebusiness <주소> --yes --no-open --no-fill` 로 다시 읽는다(확인 뒤 공식 REA 를 설치하고 읽음). 동의 없이 REA 를 설치하지 않는다. 사용자가 이미 `rebiz <주소>` 로 만든 `report.json` 을 주면 그 파일에서 3단계부터 시작한다.

### 1단계. 범위와 선 긋기

- 대상, 관계, 볼 범위를 한 줄씩 적는다 (`meta.scope`).
- 남의 것: 이용약관과 robots.txt 확인 결과를 `meta.terms` 에 적는다. `status` 는 약관 조항까지 읽었으면 `checked`, robots.txt 까지만 확인하고 약관을 아직 못 읽었으면 `robots-only`, 둘 다 찾지 못했으면 `not-found`. 수집기 초안은 `robots-only` 로 나오므로, 약관을 읽은 뒤 `checked` 로 바꾸고 `note` 에 한 줄 적는다. 내 것: `not-applicable`.
- 볼 자료 목록을 먼저 만든다. 남의 것이면 공개 자료만: 랜딩, 가격, 도움말, 공개 문서, 공개 데모 영상, 대상이 직접 공개한 화면, 공개 리뷰.

### 2단계. 근거 장부 만들기

- 본 것마다 근거를 하나씩 등록한다: `id`(E1, E2 ...), `type`, `ref`, `note`, `seen_at`.
- 어디서 봤는지를 `seen` 에 적는다: `page`(화면에서 봄, 기본), `flow`(흐름에서 봄: 펼친 뒤의 화면이나 요청이 나간 호스트), `code`(코드에서 봄: 내려온 스크립트 안). 코드에서만 본 것은 관찰이 될 수 없다(3단계의 상태 표기).
- `type` 은 다섯 가지: `url`(공개 주소), `screen`(화면 캡처 파일), `doc`(공개 문서나 내 문서), `file`(소스 파일, 내 것일 때만), `run`(직접 실행해서 본 것, 내 것이거나 공개 무료 기능일 때만).
- 캡처는 내 폴더에 두고 경로만 적는다. 남의 화면 캡처를 리포트 밖으로 퍼뜨리지 않는다.
- "찾아봤는데 없었다"도 근거다. 어디를 어떻게 찾아봤는지 범위를 적는다. 없다고 확인된 것이 아니라 그 범위에서 못 찾은 것이다.
- 모은 원본 자료(캡처, 받아 둔 HTML, REA Evidence, 원본 글 묶음)는 `evidence/` 같은 폴더 하나에 두고 저장소나 공개 장소에 올리지 않는다. 리포트에는 내 말로 쓴 문장과 경로만 들어간다.

#### 수집기로 읽기 (`tools/collect.mjs`): 가장 먼저 쓰는 길

```bash
node "<이 스킬 폴더>/tools/collect.mjs" <주소> --out ./rebiz-out
```

- 내 것이면 `--own` 을 붙인다. 읽는 한도는 같고, 리포트에 내 것으로 적히며, 속 읽기를 할 수 있다.
- **정밀 모드 (REA 가 있을 때 저절로 켜진다. `--light` 로 끈다. REA 는 `rebiz` 가 확인을 받은 뒤 설치하고, 거절하면 가벼운 모드).** 수집기가 임시 프로필의 헤드리스 브라우저를 띄우고 REA 를 눈으로 써서 세 깊이로 읽는다. 순서는 언제나 robots.txt, 받은 HTML, 그다음에야 브라우저다.

  | 깊이 | 하는 일 | 리포트에 남는 것 |
  |---|---|---|
  | 겉 읽기 | 그려진 화면의 글과 구조 (REA inspect-web-page) | 관찰. 저장소는 키 이름만, 값은 읽지 않는다 |
  | 흐름 읽기 | 펼치기만 누른다(가격 탭, 자주 묻는 질문, 더 보기, 최대 8번). 페이지가 요청을 보내려던 호스트 이름을 모은다 | 관찰이고 근거에 `seen: flow`. 결제사, 분석 도구, 영상 호스팅의 이름이 `flow.services` 에 들어간다 |
  | 속 읽기 | 이미 내려온 스크립트를 실행 없이 읽는다 (REA analyze-web-bundle 과 이름 찾기) | **코드 흔적**(`status: code`, 근거에 `seen: code`). 화면 경로 이름, 결제 모듈 이름, 가격처럼 보이는 글자 |

  - 흐름 읽기에서 폼 제출, 로그인, 가입, 결제, 구매 단추와 다른 페이지로 가는 링크는 누르지 않는다. 주고받은 내용, 쿠키, 토큰은 남기지 않는다.
  - 속 읽기는 약관이 서비스 코드 분석을 금지하면 하지 않는다. 약관을 읽지 못했을 때도 하지 않는다(내 것이면 한다). 하지 않았으면 `meta.depth` 에 까닭이 적힌다. 에이전트가 다른 방법으로 대신 읽지 않는다.
  - **찾은 주소는 절대 부르지 않는다.** 코드에서 찾은 화면 경로와 서버 호출 주소는 이름만 적는다. 열어 보거나 요청을 보내 확인하지 않는다.
  - 어느 단계가 실패하거나 시간 한도를 넘으면 수집기가 건너뛰고 `meta.depth` 에 "이 단계는 못 읽음"과 까닭을 남긴다. 그대로 두고 3단계로 간다.
  - 근거 원본은 결과 폴더의 `evidence/` 에 남는다(REA 기록, 호스트 이름과 누른 종류, 코드에서 찾은 이름). 스크립트의 글과 쿠키 값은 남기지 않는다. 이 폴더는 올리지 않는다.
- 하는 일: robots.txt 를 먼저 받고, 허용된 경우에만 첫 페이지 한 장과 그 페이지에 걸린 가격, 약관, 환불 링크까지 최대 5장을 읽는다. 요청 사이 2초 이상(robots.txt 의 Crawl-delay 가 더 길면 그 값, 60초보다 길면 멈춤).
- 그려진 화면 읽기: 요즘 사이트는 화면을 스크립트로 그려서, 받은 HTML 에 글이 거의 없는 경우가 많다. 받은 글이 얇으면(1,500자 미만이거나 가격과 누르는 곳이 하나도 안 보일 때) 이 컴퓨터의 Chrome, Chromium, Edge, Brave 가운데 하나를 **임시 프로필의 헤드리스 창**으로 잠깐 띄워 그려진 화면을 한 번 읽는다. 누르기, 입력, 화면 캡처는 없다. 브라우저 안에서 나가는 요청도 같은 선으로 거른다(GET 이 아닌 요청, robots.txt 가 막은 주소, 로그인과 결제 주소, 분석 도구는 보내지 않는다). 끝나면 브라우저를 끄고 임시 프로필을 지운다. 구역의 뼈대도 이때 실제 위치와 길이로 잰다. `--no-render` 로 끌 수 있다.
- 브라우저가 없으면 받은 HTML 만 읽고, 결과 끝에 "읽은 글이 N자뿐이라 모름이 많다"와 다음에 할 일이 나온다. 그때는 REA 가 있으면 위의 "REA 가 있으면" 순서로 읽고, 없으면 사용자가 직접 본 화면의 메모를 받아 채운다.
- 하지 않는 일: 로그인, 가입, 결제, 폼 제출, 쿠키 저장. 로그인이나 결제로 가는 링크는 열지 않는다. 401, 403, 429 나 사람 확인 화면을 만나면 넘지 않고 멈춘다(종료 코드 3). 멈추면 다른 방법으로 돌아 들어가지 말고 사용자에게 알린다.
- 나오는 것: `report.json`(본 것만 관찰, 나머지는 모름인 초안), `source.json`(겹침 검사용 원본 글 묶음, 올리지 않는다), `requests.json`(보낸 요청 기록).
- 초안에는 `skeleton`(구역의 뼈대)이 채워져 있다. 그려 읽었으면 길이는 잰 값이고, 아니면 어림이다. 층 이름은 어느 쪽이든 규칙으로 붙인 추정이므로 3단계에서 직접 보고 고친다.
- 초안의 `meta.read` 에 읽은 방식과 글자 수가 적힌다. `thin` 이 true 면 화면 맨 위에 알림이 뜬다. 에이전트가 화면을 직접 보고 칸을 채웠으면 `meta.read.thin` 을 false 로 고친다.
- 도구를 쓸 수 없으면 `report.template.json` 을 복사해 처음부터 채운다. 한도, 약관 확인, 가리기 규칙은 똑같다.

#### REA 를 직접 돌릴 때 (수집기의 정밀 모드를 쓸 수 없을 때만)

REA 는 이 스킬과 별개의 도구다(MIT, 공식 저장소에서만 받는다). 이 스킬은 REA 위에서 쓰는 별개의 도구이고, 스킬 절차 안에서는 REA 를 설치하거나 설정을 바꾸지 않는다(설치는 사용자가 확인하는 `rebiz` 의 몫이다). REA 로 읽으면 브라우저가 그린 화면의 글자까지 읽을 수 있어 가벼운 수집기보다 정밀하다. 보통은 위의 수집기가 REA 를 대신 불러 준다. 수집기를 쓸 수 없고 `rea --version` 이 될 때만 아래 순서로 직접 근거를 모은다. 명령의 정확한 인자는 `rea <명령> --help` 로 확인한다.

1. robots.txt 를 한 번 받는다. 이용약관 주소를 알면 그것부터 읽는다.
2. 임시 프로필의 별도 브라우저를 띄운다. 평소 쓰는 브라우저 프로필과 쿠키는 쓰지 않는다. 디버깅 포트는 127.0.0.1 에서만 연다.

   ```bash
   PROFILE=$(mktemp -d)
   "<Chrome 실행 파일>" --headless=new --remote-debugging-port=9333 --user-data-dir="$PROFILE" about:blank &
   echo $! > chrome.pid
   curl -s -X PUT "http://127.0.0.1:9333/json/new?<공개 페이지 주소>"
   ```

3. REA 로 붙어서 읽는다. REA 는 페이지를 열거나 누르지 않고, 이미 떠 있는 페이지를 읽기만 한다.

   ```bash
   rea list-browser-targets http://127.0.0.1:9333 --allowed-origins <출처> --format json > evidence/01_targets.json
   rea capture-web-screenshot http://127.0.0.1:9333 <targetId> --allowed-origins <출처> --format json > evidence/02_screenshot.json
   rea inspect-web-page http://127.0.0.1:9333 <targetId> --allowed-origins <출처> \
     --include-accessibility-text --include-storage-keys --format json > evidence/03_inspect_page.json
   rea analyze-web-bundle http://127.0.0.1:9333 <targetId> --allowed-origins <출처> \
     --detail summary --evidence_output evidence/04_bundle_evidence.json \
     --view '{"kind":"web-bundle","collection":"summary"}' --format json > evidence/04_bundle_summary.json
   ```

   - `--include-accessibility-text` 를 꼭 준다. 제목, 가격 문구, 누르는 곳의 글자가 여기서 나온다.
   - 저장소는 `--include-storage-keys` 로 키 이름만 받는다. 값, 쿠키, 요청 머리말은 받지 않는다. 스크립트 원문(`--include-script-sources`)과 소스맵(`--fetch-source-maps`)은 남의 서비스에서는 받지 않는다.
   - REA 는 보이는 화면 한 장만 찍는다. 전체 길이가 필요하면 창을 문서 길이만큼 늘린 뒤 다시 찍는다.
   - 큰 스크립트는 정적 분석이 끝나지 않을 수 있다. 기본값으로 한 번만 돌리고, 안 된 것은 모름으로 둔다.
4. REA 가 주지 않는 것은 같은 한도 안에서 보충하거나 모름으로 둔다. 메타 태그 값과 JSON-LD 는 공개 HTML 한 장을 한 번 받아 보충한다. 접혀 있는 글, 붙기 전의 요청, 다른 출처의 자원, 색과 글꼴 값은 REA 근거에 없다.
5. 다 읽었으면 대상 탭을 닫고, 내가 띄운 브라우저만 `kill $(cat chrome.pid)` 로 끈다.
6. 근거에서 초안을 만든다 (아래 `from-rea.mjs`). 초안은 본 것만 관찰로 옮기고, 3단계부터는 사람이 읽고 채운다.

#### 도구: REA 근거에서 초안 만들기 (`tools/from-rea.mjs`)

```bash
node "<이 스킬 폴더>/tools/from-rea.mjs" evidence/03_inspect_page.json evidence/02_screenshot.json evidence/04_bundle_evidence.json \
  --html evidence/public.html --robots evidence/robots.txt \
  --brand "<원본 브랜드 이름>" \
  --out report.draft.json --source-out evidence/source.json
```

- 넣는 것: REA Evidence JSON 여러 개(종류는 알아서 가린다), 선택으로 공개 HTML 한 장, robots.txt 사본, 캡처 파일. 수집기의 정밀 모드가 남긴 `evidence/03_flow.json`(흐름 읽기 기록)과 `evidence/04_code_scan.json`(속 읽기 기록)도 함께 줄 수 있다. 코드에서 본 것(analyze-web-bundle, 04_code_scan.json)은 코드 흔적으로 들어간다.
- 나오는 것 1: `report.draft.json`. 제목, 가격 문구, 가입과 결제로 가는 누르는 곳, 구역 순서, 스크립트와 저장소 키 이름 같은 기술 흔적이 관찰로 들어가고, 근거 장부가 E1 부터 만들어진다. 고객, 문제, 첫 가치, 매출, 내 버전 명세는 채우지 않는다. 끝에 검사기가 알려 주는 빈칸 목록이 나온다.
- 나오는 것 2: `source.json`. 원본에서 모은 글, 브랜드 이름과 도메인, 그림과 영상 주소. 7단계의 겹침 검사에만 쓰고 다른 곳에 올리지 않는다. 브랜드 이름은 제목에서 짐작한 것이므로 `--brand` 로 더하거나 파일을 열어 고친다.
- 가리기: 쿠키, 토큰, 인증 머리말처럼 비밀 값이 실릴 수 있는 키는 통째로 버린다. 이메일, 전화번호, 키 모양 글자는 가린다. 주소는 물음표 뒤를 떼고 적는다.
- 초안은 추정을 하지 않는다. 초안의 문장을 그대로 두지 말고, 근거를 다시 열어 보고 내 말로 고쳐 쓴다.

### 3단계. 6칸 채우기

문장 하나 = 주장 하나. 주장마다 `status` 와 `evidence` 를 붙인다.

| 칸 | 물음 | 채우는 것 |
|---|---|---|
| 1. 누가 왜 돈을 내는가 | 고객, 문제, 가격 | `customer`, `problem`, `price`, `revenue`(공개 근거 있을 때만) |
| 2. 핵심 사용자 흐름 | 유입, 첫 가치, 가입, 결제, 다시 오기 | `steps` 를 순서대로. `signup`, `first_value`, `payment` 단계는 반드시 한 줄씩(없거나 모르면 그렇게 적는다). `arrive`(유입)와 `return`(다시 오기)도 한 줄씩 적으면 구조도의 다섯 마디가 채워진다 |
| 3. 화면과 기능 지도 | 어떤 화면에서 무엇을 하나 | `screens`: 화면 이름, 목적, 기능 목록 |
| 4. 기술 구성 | 무엇으로 만들었나 | `items`: 층(layer)과 내용. 남의 것은 밖에서 보이는 단서만 |
| 5. 근거와 모르는 것 | 무엇을 보고 말했나, 무엇을 모르나 | 근거 장부 전체 + `unknowns`(질문, 모르는 이유, 알아낼 방법) |
| 6. 내 버전 명세 | 같은 문제를 푸는 다른 제품 | `my_version`: 가칭, 같은 문제, 대상 고객, 최소 기능, 차별점 3개, 가져오지 않는 것 |

상태 표기:

- `observed` 관찰: 근거 화면이나 문서에서 직접 본 것. 근거 1개 이상 필수.
- `inferred` 추정: 본 것에서 끌어낸 것. 근거 1개 이상 필수, 문장에 추정임이 드러나게 쓴다.
- `unknown` 모름: 확인할 수 없는 것. 근거 없이 둔다. 지어서 채우지 않는다.
- `code` 코드 흔적: 내려온 코드 안에서만 본 것. `seen: code` 인 근거가 1개 이상 필수. "지금 그렇다"는 뜻이 아니다. 코드 안에 가격 숫자나 화면 이름이 있어도 화면에서 확인되기 전에는 관찰로 올리지 않는다. 검사기는 코드 근거만 붙은 관찰을 오류로 잡는다. 화면에서 같은 것을 다시 봤다면 화면 근거를 함께 붙여 관찰로 쓴다.

코드나 문서를 읽은 것은 "읽어서 확인"이고 실행해서 본 것이 아니다. 실행해 보지 않았으면 실행 결과처럼 쓰지 않는다.

#### 뼈대 (`skeleton`, 해부 장면의 재료)

페이지 한 장의 구역을 위에서 아래로 적는다. 해부 화면이 이것을 선으로만 그려 층으로 벌린다.

```json
"skeleton": { "note": "", "evidence": ["E1"], "blocks": [
  { "name": "제목과 가격 상자", "role": "pay", "weight": 765, "kind": "price", "status": "inferred", "mine": ".lead" }
] }
```

- `name` 은 내 말로 붙인다. 원본의 제목이나 문구를 옮기지 않는다. 원본의 화면 캡처, 로고, 그림은 넣지 않는다.
- `role`: `attract` 데려오는 층, `value` 가치를 주는 층, `pay` 돈 받는 층(가격, 신청, 후기, 걱정 풀기), `return` 다시 오게 하는 층, `other` 그 밖. 층 이름은 해석이므로 `status` 는 보통 `inferred`. 보이지 않는 층은 지어내지 않는다.
- `weight` 는 세로 길이의 어림값(픽셀이든 비율이든 서로의 비만 맞으면 된다). `kind` 는 `media`, `headline`, `price`, `nav`, `numbers`, `list`, `notice`, `quotes`, `faq`, `cta`, `footer`, `text` 중 하나.
- 내 버전을 만든 뒤에는 같은 구실을 하는 내 구역의 CSS 선택자를 `mine` 에 적는다. 가져오지 않은 구역은 `"taken": false`.

### 4단계. 모르는 것 정리

- 칸마다 "이 칸에서 모르는 것"을 다시 훑어 `unknowns` 에 올린다. 가격, 매출, 고객 수, 전환, 서버 쪽 로직은 밖에서 대부분 모른다.
- 모르는 것이 0개인 리포트는 의심한다. 다시 확인한다.

#### 해부만 할 때는 여기서 저장하고 검사한다

```bash
node "<이 스킬 폴더>/tools/check-report.mjs" ./report.json --dissect-only    # 내 버전 칸이 비어 있어도 통과
node "<이 스킬 폴더>/tools/build-view.mjs" ./report.json --open
```

오류가 나오면 `report.json` 을 직접 고치고 다시 검사한다.

### 5단계. 내 버전 명세 (클린룸) 쓰고 저장 (내 버전까지 갈 때만)

- 6번 칸은 1~5번 칸의 내 문장만 보고 쓴다. 대상의 화면 문구, 캡처, 코드를 옆에 두고 쓰지 않는다.
- 같은 문제를 푸는 **다른** 제품의 최소 명세를 쓴다: 누구의 어떤 문제, 최소 기능 3~5개, 차별점 정확히 3개(대상, 형태, 방식, 가격, 유통 중에서), 가져오지 않는 것 목록.
- `report.json` 으로 저장하고 검사한 뒤 리포트를 연다.

```bash
# 이 스킬 폴더 기준. 템플릿을 복사해서 채운다.
cp "<이 스킬 폴더>/report.template.json" ./report.json

# 검사: 오류 0개가 될 때까지 고친다.
node "<이 스킬 폴더>/tools/check-report.mjs" ./report.json

# 해부 화면 만들기: report.html 이 report.json 옆에 생긴다. --open 을 주면 브라우저로 연다.
node "<이 스킬 폴더>/tools/build-view.mjs" ./report.json --open
```

### 6단계. 내 버전 만들기

- 출발점은 도구로 만든다. 6번 칸의 명세와 뼈대의 구역 종류, 순서만 보고 바로 열리는 정적 페이지(index.html, style.css)를 쓴다. 문구 자리는 "여기에 무엇을 쓸지" 안내로 채워져 있으므로, 그 점선 자리를 내 말로 바꿔 쓰고 색과 그림을 내 것으로 정한다.

  ```bash
  node "<이 스킬 폴더>/tools/make-site.mjs" ./report.json --out ./my-version --topic "<내 사업 주제>"
  ```

  6번 칸이 비어 있으면 만들지 않는다(5단계를 먼저 한다). 이미 파일이 있는 폴더는 `--force` 없이는 건드리지 않는다. 리포트 옆에 `source.json` 이 있으면 끝나고 겹침 검사를 스스로 돌린다. 뼈대의 `mine` 이 비어 있던 구역에는 만든 구역의 선택자(`#rb-1` 같은)를 리포트에 적어 준다.
- 넘기는 것은 6번 칸의 명세와 내 디자인 규칙뿐이다. 대상의 주소, 캡처, 받아 둔 파일, `source.json` 은 만드는 쪽에 넘기지 않는다.
- 배우는 것은 구조다: 구역의 순서, 흐름, 가격을 보여 주는 짜임. 문구, 이름, 색, 글꼴, 그림, 숫자는 전부 새로 정한다.
- 공부용으로 가상의 주제를 쓸 때는 화면에 예시라고 적는다. 지어낸 후기와 지어낸 실적 숫자는 넣지 않는다. 후기 칸은 빈자리로 둔다.
- 폴더와 파일 이름에 대상의 이름을 넣지 않는다.
- 다 만들면 `skeleton.blocks[].mine` 에 내 구역의 선택자를 적고, 해부 화면에 내 버전을 넣어 다시 만든다. 화면의 비교 칸에서 뼈대가 내 버전으로 바뀌는 것을 볼 수 있다.

```bash
node "<이 스킬 폴더>/tools/build-view.mjs" ./report.json --mine ./my-version --open
```

### 7단계. 겹침 검사 (`tools/check-clone.mjs`)

```bash
node "<이 스킬 폴더>/tools/check-clone.mjs" ./my-version --source evidence/source.json
```

실패로 보는 것 세 가지. 하나라도 있으면 종료 코드 1.

1. 원본과 다섯 낱말 이상 연달아 같은 구간 (`--words` 로 바꿀 수 있다)
2. 원본 브랜드 이름이나 도메인. 글, 코드, 파일 이름 어디에 있든, 띄어쓰기나 대소문자를 바꿔도 잡는다
3. 원본 그림, 아이콘, 영상, 글꼴 주소

경고로 알리는 것: 원본의 한 줄과 통째로 같은 짧은 문구, 원본과 같은 자원 파일 이름, 바깥 주소에서 불러오는 자원.

- REA 없이 모은 원본 글은 한 줄에 한 문장씩 텍스트 파일로 만들어 `--text 원본글.txt --brand "<이름>" --domain <도메인>` 으로 준다.
- 실패가 나오면 그 부분을 내 말, 내 이름, 내 자원으로 바꾸고 다시 돌린다. `--allow` 는 법으로 정해진 고지 문구처럼 같을 수밖에 없는 글에만 쓴다.
- 이 검사가 보지 않는 것: 색, 글꼴, 배치의 닮음. 원본 캡처와 내 버전 캡처를 나란히 놓고 사람이 본다. 통과는 겹치는 글과 주소가 없다는 뜻이지 법적으로 안전하다는 보증이 아니다.

## 해부 다음: 이미 있는 프로젝트에 적용하기, 영상 뽑기

사용자가 "이 구조를 내 사이트에 적용해 줘", "우리 프로젝트에 반영해 줘"라고 하면 새로 만들지 않고 아래 순서로 한다.

1. 계획부터 만든다. 내 첫 화면을 수집기와 같은 구역 분류로 읽어 배운 뼈대와 견준다. 코드는 고치지 않는다.

   ```bash
   node "<이 스킬 폴더>/tools/apply-plan.mjs" ./report.json --to <내 프로젝트 폴더>
   ```

   - 결과는 `<내 프로젝트 폴더>/rebiz-apply/plan.md` 와 `plan.json`: 대상에는 있는데 내 첫 화면에는 없는 구역(빈칸), 순서가 다른 구역, 넣을 자리, 그 구역에 무엇을 쓸지.
   - 프레임워크 프로젝트라 첫 화면의 HTML 파일이 없으면 멈추고 알려 준다. 그때는 `--page <첫 화면 소스 파일>` 을 주거나, 사용자가 띄운 개발 서버 주소를 `--url http://localhost:포트` 로 준다. `--url` 은 내 컴퓨터 주소만 받는다. 바깥 주소를 여기에 넣지 않는다.
   - 구역의 종류는 규칙으로 붙인 추정이다. 화면을 직접 보고 틀린 곳은 계획을 고쳐 쓴다.
2. 고치기 전에 확인한다. 프로젝트가 git 저장소인지, 작업 트리가 깨끗한지 본다. 아니면 멈추고 사용자에게 까닭을 알린다. 깨끗하면 새 브랜치 `rebiz/apply-YYYYMMDD` 를 만들고 그 위에서만 고친다.
3. 계획의 빈칸을 첫 화면에 넣는다. 그 프로젝트의 지금 디자인(색, 글꼴, 클래스 이름을 붙이는 방식)을 따르고, 새 구역의 글은 그 프로젝트에 이미 있는 글과 계획의 "쓸 것"만 보고 내 말로 쓴다. 가격, 숫자, 후기는 지어내지 않고 자리 표시로 둔다. 내 첫 화면에만 있는 구역은 지우지 않는다. 순서는 내 이야기의 흐름에 맞을 때만 옮긴다.
4. 끝나면 `git diff --stat` 을 사용자에게 보여 주고, 바뀐 파일에 겹침 검사(7단계)를 돌린다. **커밋, push, 배포는 하지 않는다.** 사용자가 바뀐 것을 본 뒤에 정한다.

영상은 화면을 열지 않고 뽑을 수 있다. Chrome 계열 브라우저를 임시 프로필로 잠깐 띄워 해부 화면의 영상 저장을 대신 누르고, 끝나면 브라우저를 끄고 프로필을 지운다. 바깥으로 나가는 요청은 없다.

```bash
node "<이 스킬 폴더>/tools/video.mjs" ./report.json --mine ./my-version --out ./dissection.mp4
```

터미널에서 사람이 쓰는 같은 명령은 `rebiz fill`, `rebiz build`, `rebiz apply`, `rebiz video` 다. `rebiz` 의 `--agent` 옵션은 사람이 터미널에서 에이전트에게 한 번 맡길 때 쓰는 것이다. 에이전트인 나는 그 옵션을 붙여 다른 에이전트를 부르지 않고, 맡은 일을 직접 한다.

## report.json 모양

전체 규칙은 같은 폴더의 `report.schema.json`, 빈 틀은 `report.template.json`.

```json
{
  "schema": "rebiz/report@1",
  "meta": {
    "target": { "name": "", "kind": "web-service", "url": "", "relation": "third-party" },
    "analyzed_at": "YYYY-MM-DD",
    "analyst": "",
    "scope": "",
    "method": [],
    "terms": { "status": "checked | robots-only | not-found | not-applicable", "note": "", "evidence": [] },
    "one_line": ""
  },
  "evidence": [ { "id": "E1", "type": "url", "ref": "https://...", "note": "", "seen_at": "YYYY-MM-DD", "seen": "page | flow | code" } ],
  "sections": {
    "money":   { "customer": [], "problem": [], "price": [], "revenue": [] },
    "flow":    { "steps": [ { "stage": "arrive | first_value | signup | payment | return | other", "label": "", "text": "", "status": "unknown", "evidence": [] } ] },
    "map":     { "screens": [ { "name": "", "purpose": "", "features": [], "status": "observed", "evidence": ["E1"] } ] },
    "tech":    { "items": [ { "layer": "", "text": "", "status": "inferred", "evidence": ["E1"] } ] },
    "unknowns": [ { "question": "", "why": "", "next": "" } ],
    "my_version": { "working_name": "", "same_problem": "", "who": "", "mvp": [], "differences": [ { "title": "", "text": "" } ], "not_taken": [] }
  }
}
```

주장 하나의 모양: `{ "text": "...", "status": "observed | inferred | unknown | code", "evidence": ["E1"] }`

## 끝내기 전 검수

- [ ] `check-report.mjs` 오류 0개 (해부만 했으면 `--dissect-only`). 고칠 때는 `report.json` 을 직접 고쳤다.
- [ ] `meta.terms.status` 가 실제로 한 만큼만 적혀 있다 (약관을 읽지 않았으면 `checked` 가 아니다).
- [ ] 관찰과 추정마다 근거가 있고, 근거를 열면 그 말이 실제로 보인다 (3개 이상 직접 다시 열어 확인).
- [ ] 수익, 사용자 수 숫자는 공개 주소가 붙은 것만 남았다. 없으면 `revenue` 는 빈 배열.
- [ ] 코드에서만 본 것은 코드 흔적(`status: code`)으로 남아 있다. 코드에서 찾은 주소를 열거나 불러 본 적이 없다.
- [ ] `meta.depth` 가 실제로 읽은 깊이와 같고, 건너뛴 단계에는 까닭이 적혀 있다.
- [ ] 가입, 첫 가치, 결제 단계가 모두 있다 (없음이나 모름도 한 줄로). 유입과 다시 오기도 적었다.
- [ ] `skeleton` 의 이름이 내 말이고, 원본의 문구, 캡처, 로고가 들어 있지 않다.
- [ ] (내 버전까지 갔다면) 6번 칸에 대상의 이름, 문구, 화면 이름이 없다. 차별점이 정확히 3개다.
- [ ] 리포트에 비밀 값, 이메일, 내 컴퓨터의 절대 경로가 없다.
- [ ] 로그인, 결제, 접근 제한을 넘은 적이 없고, 본 공개 페이지가 한도 안이다.
- [ ] 내가 띄운 브라우저를 껐고, 모은 원본 자료는 `evidence/` 밖으로 나가지 않았다.
- [ ] 내 버전을 만들었다면 `check-clone.mjs` 가 통과했고, 두 화면을 나란히 놓고 한 번 봤다.
- [ ] 이미 있는 프로젝트에 적용했다면 새 브랜치에서만 고쳤고, 커밋, push, 배포를 하지 않았고, `git diff --stat` 을 사용자에게 보여 줬다.

## 사용자에게 보고하는 법

짧게 다섯 줄: 한 줄 요약, 관찰 / 추정 / 모름 개수, 가장 중요한 모르는 것 3개, 내 버전 차별점 3개(해부만 했으면 "내 버전은 아직 만들지 않음"), `report.json` 과 해부 화면(`report.html`) 위치. 해부 화면의 "영상으로 저장" 단추나 `rebiz video report.json` 으로 해부 과정을 9:16 영상으로 받을 수 있다는 것도 한 줄로 알린다. 다음에 할 수 있는 일(`rebiz build` 로 새 사이트 만들기, `rebiz apply` 로 내 프로젝트에 적용)도 한 줄로 알린다. 내 버전까지 만들었으면 겹침 검사 결과와 내 버전 위치를 한 줄 더한다. 그리고 "모르는 것 중 사용자가 직접 확인해 줄 수 있는 것"을 물어본다.
