---
name: edu-deck-series
description: "Use when the user wants a multi-episode education or training series as HTML (예: \"사내 교육 시리즈 만들어\", \"여러 편으로 나눠 교육 자료\", \"N편짜리 교육\", \"진도 관리되는 교육\", \"시리즈 포털\"), or when the entry skill edu-deck 판별이 시리즈(2편 이상 + 진도·허브)로 내려온다. 한 주제 한 덱은 edu-deck-solo 스킬이다. 결과물은 목차(허브)에서 편을 골라 보고, 편마다 진도가 저장되어 이어보는 단일 HTML 포털이다."
---

# edu-deck-series: 주제 → 리서치 → 교육용 HTML 시리즈 포털

여러 편의 교육 덱을 하나의 HTML 시리즈로 만든다. 첫 화면(목차·허브)에서 편을 고른다. 데스크톱은 1920×1080 발표 덱, 좁은 화면은 원래 1920×1080 배치를 화면 폭에 맞춰 축소한 세로 스크롤 읽기(단계 자동 공개, 장 탭으로 크게 보기) 배치로 열린다. 본 장 수가 브라우저에 저장되어 이어보기·완강 표시가 되고, 자습 모드(S)·인쇄(P)·용어집(G)·확인 문제는 편 단위로 동작한다.

결과물은 외부 글꼴·이미지·스크립트가 필요 없는 HTML 파일 하나다. 시리즈의 편별 CSS 격리는 native `@scope` 지원 브라우저가 필요하며, legacy 편만 있는 시리즈에도 적용된다. 현재 렌더·동작 검증은 Chrome에서만 수행했다. 다른 브라우저·버전의 호환성은 미검증이며 지원 최저 버전도 확정하지 않았다. 배포 대상 브라우저에서 별도 확인한다. 각 편은 edu-deck-solo 절차로 만든 완전한 덱이라 편 하나만 단독 발행도 가능하다.

## 기본값 (사용자가 따로 말하지 않으면)

| 항목 | 기본값 |
|---|---|
| 청중 | 비전공 일반 직원 |
| 규모 | 3~5편 (기초 1편 + 심화 2~4편), 편당 10~16장 |
| 목차(허브) 유형 | 아래 선택 규칙으로 자동 추천 → 구성안에 적고 승인받는다 |
| 작업 폴더 | `${EDU_DECK_OUTPUT_DIR:-./outputs}/edu-deck-series/<YYYYMMDD>-<영문-slug>/` — 사용자가 위치를 정하면 그 폴더를 쓰고, 정하지 않으면 이 기본값을 쓴다. 포털 결과물과 각 편 산출물은 모두 이 작업 폴더 안에 쌓인다 |
| 결과 파일 | `<작업 폴더>/<시리즈 제목>.html` (series.json 의 `output`) |
| 중간 확인 | **1회 — 편 나누기 구성안 승인**. 승인 후에는 편마다 solo 절차(중간 확인 없음)를 따른다 |

## 작업 순서

`<base>` = 공통 자산 폴더 `edu-deck/shared`(진입 스킬 edu-deck 폴더 안. 조각·문서·검사 스크립트가 모두 거기 있다). `<series>` = 이 스킬 폴더 `edu-deck-series`. 명령은 경로를 그대로 붙여 부른다. `<base>` 를 못 찾으면 진행을 멈추고 edu-deck(라우터) 스킬 설치를 확인한다.

시작할 때 한 번: `python3 <base>/scripts/env_check.py` — solo 와 같다.

### 1. 요청 정리 + 편 나누기 구성안 → 승인 1회
- brief.md: 주제, 청중, 전체 시간, 시리즈로 나눈 이유(정기·단계별·역할별), 교육 뒤 할 수 있어야 하는 것.
- `<series>/references/series.md` 1~2절(편 나누기 기준)으로 편 목록을 정한다: 편 제목·한 줄 소개·장 수(10~16장)·기초/심화 구분. 기초편은 전체 그림 1개, 심화편은 주제별 2~4개가 기본.
- 시리즈 제작 전에 경로(팩/legacy)를 `edu-deck/SKILL.md` 의 "경로 결정"으로 시리즈 단위로 한 번 정한다(기본값 없음, 애매하면 사용자에게 한 번 묻고, 물을 수 없으면 추천으로 진행해 근거를 남긴다). 한 시리즈의 편들이 같은 경로를 쓰는 것을 원칙으로 하며, 편마다 경로를 바꾸려면 이유를 구성안에 적는다.
  - 팩이면: `python3 <base>/scripts/pack_router.py --title "<시리즈 제목>" --outcomes … --audience …` 로 후보 3종·추천·흐름을 계산하고 `<base>/references/resource-packs.md` 를 읽어 디자인 1종·주흐름 1종·필요시 다른 보조활동 최대 2종을 정한다. 기본은 에이전트가 청중·수행 행동 근거로 확정해 구성안에 남기고(authoring.md 5절), 시안 3종 비교는 사용자가 요청할 때 쓰는 선택적 절차다(물을 수 없으면 추천으로 진행하며 근거를 남긴다). 팩 선택은 시리즈 제작 전 1회만 하고 모든 편이 같은 선택을 공유한다(같은 시리즈 안에서 다양성을 만들려고 편마다 바꾸지 않는다. 시리즈끼리는 `--recent` 로 최근 쓴 디자인을 넘겨 반복을 줄인다).
  - legacy 면: `<base>/references/composition.md` 의 유형표·줄거리, `layouts.md`·`snippets/` 로 편을 만들고 편마다 `theme`(시리즈 안에서는 같은 테마를 권장) 을 `tone_router.py` 추천으로 정한다.
  - 편별 수행 행동·평가 증거와 선택 이유를 구성안에 적는다. 시리즈의 디자인 일관성을 우선하되 편의 학습 목적에 맞춰 흐름은 달리할 수 있다. 이유 없는 무작위 디자인 전환은 하지 않는다.
- 허브 유형을 정한다(선택 규칙은 series.md 3절): ①경로형(map — 단계·흐름이 있는 과정) ②책장형(shelf — 편이 독립적·고르는 맛) ③목록형(list — 편이 많고 정보 위주). 애매하면 추천과 근거를 구성안에 적고 진행한다(허브 유형은 구성안 승인 1회에서 함께 본다).
- **구성안을 사용자에게 보여 승인을 한 번 받는다.** 승인 후 편 추가·삭제는 변경 이유와 함께 다시 확인한다.
- 조사 계획: 편마다 파트별 조사 질문(brief.md 에). 조사 절차는 solo 2단계(`<base>/references/research.md`)를 편 단위로 반복한다. 조사 결과는 시리즈 공통 `research.md` 하나로 모아도 된다.

### 2. 편마다 solo 절차로 덱 만들기
- 허브와 편 모두 [공통 반응형 계약](../edu-deck/shared/references/responsive.md)을 따른다. 공통 계층을 편 CSS에 복제하지 않는다. 기존 포털은 다시 조립해야 반영된다.
- 모든 편에 `<base>/references/DESIGN_TOKENS.md`·`MOTION_LIBRARY.md`를 적용한다. 공통 Pretendard·15색 의미 토큰·단계 시그니처는 포털에 한 번 포함된다. 모션을 편 CSS나 조각에 복제하지 않는다.
- 비유·예시에는 도식·일러스트·장면 모형을 짝짓고 인라인 SVG를 우선한다. 개념 SVG 도식의 설계 규칙·문법·함정은 `<base>/references/diagrams.md`를 따른다(기본·팩 경로 공통). 라스터는 편당 합계 1.5MB 이내 base64만 사용한다. 외부 로딩은 금지한다. 자습·인쇄·움직임 줄이기에서 현재 의미 단계의 정적 완결을 확인한다.
각 편 폴더 `<작업 폴더>/<NN>-<편-이름>/` 에서 edu-deck-solo 의 3~6단계(구성 → 조각 → 조립 → 말투 교정 → 검사)를 그대로 밟는다:
- 새 편의 `deck.json`에는 `title`·`output`을 넣는다. 팩 편일 때만 `resource_pack`을 명시한다: `{"design":"workbook","flow":"follow","activities":[]}` — 디자인·주흐름은 시리즈에서 한 번 고른 선택을 모든 편이 공유한다. 선택 키 `summary`·`glossary`는 series.md 5절대로 편별로 작성한다. 기본 경로 편은 `resource_pack`을 넣지 않는다.
- 새 편은 solo 4단계를 따른다. 기본(legacy) 경로는 snippets·아이콘·개념 SVG 도식으로 직접 저작하고, 팩 경로는 `<base>/references/resource-packs.md`의 init→직접 저작 경로를 따른다(init은 비어 있는 폴더에만 실행). 생성된 안내·자동 노트를 조사된 교육 내용과 실제 110~450자 노트로 교체하고, 같은 디자인 안에서 여러 배치 변형을 만든다. 각 편을 고정 cover→why→how로 만들지 않는다.
- 팩 편도 공통 아이콘 묶음(icons.svg의 `i-*`·화살촉)과 개념 SVG 도식(`diagrams.md`)은 쓸 수 있다. 다만 legacy snippets·배치 클래스·CSS는 팩 편에 섞지 않는다. 확인 문제 `.chk`·자습·단계 공개 계약은 유지한다. 크레파스 저작 속성은 공통 모션 엔진의 캔버스 크레파스 표시로 연결한다. 기본 경로 편은 layouts·expression·classes·icons의 배치 규칙을 쓴다. 조각에 id가 있어도 된다(조립기가 편마다 id 접두를 붙여 충돌을 막는다).
- 기본 경로 편에는 부품 조각(`<base>/assets/snippets/patterns/` 의 code·tabs·faq·pin-shot)과 강조 효과 `data-fx`(`<base>/references/MOTION_LIBRARY.md` 의 "강조 효과 data-fx" 절)도 쓸 수 있다 — 슬라이드가 아니라 호스트 아키타입 본문 안에 넣는다. 손그림 아이콘(Koboyo, 선택 — 라이브러리는 스킬 밖)은 `<base>/references/icons.md` 마지막 절을 따른다.
- 표현 규칙은 solo와 같다: 외국어 문장은 자연스러운 한국어로 옮겨 쓰고, 넘치면 글자를 줄이지 말고 장을 나누거나 노트로 옮긴다(`<base>/references/expression.md` 1·4절).
- 사람이 말하며 넘기는 발표 편(deck.json `talk`)은 `<base>/references/talk.md` 를 따른다. 검색·목차 뷰어 키(Ctrl+K·/ · O)와 `data-fit` 제목 맞춤은 `<base>/references/classes.md` "뷰어 도구" 절을 따른다.
- 사용자 `src/*.css`는 편 내부 클래스 선택자(예: `.lesson-panel`)로 작성한다. `:root`, `html`, `body`, 루트 ID나 편 밖 조상에 의존하는 선택자는 쓰지 않는다. 공통 제공 자산의 `:root{` 토큰만 조립기가 편의 `:scope`로 변환한다. 사용자 CSS에 같은 변환을 기대하지 않는다(`<base>/references/resource-packs.md` 5절).
- 각 편의 확인 문제(check 장)는 **같은 편 안의 장**을 다시 보기 대상으로 잡는다(data-review ↔ data-key 가 편 안에서 짝).
- 편 단위 검사: `python3 <base>/scripts/build_deck.py <편 폴더>` → `python3 <base>/scripts/check_deck.py <편 폴더>/<output> …` — 편마다 PASS 나올 때까지(solo 6단계 기준).
- 편 단위 말투 교정: 3단계 포털 조립 전에 각 편이 solo 5.5단계(`<base>/references/copyedit.md`)를 끝낸다. 어느 편이든 교정을 건너뛰면 그 사실을 보고한다.

### 3. series.json → 포털 조립
- `<작업 폴더>/series.json` 을 series.md 4절 양식으로 쓴다: 시리즈 제목·소개·허브 유형(map 은 단계 묶음 groups)·편 목록(폴더·라벨·제목·소개·색·태그)·시리즈 공통 용어집(선택).
- 조립:
```bash
python3 <series>/scripts/build_series.py <작업 폴더>
```
허브 유형을 바꿔 보려면 `--hub shelf` 같이 덮어쓰고, 결과 경로를 바꾸려면 `--out` 을 쓴다.

### 4. 시리즈 검사
```bash
python3 <series>/scripts/check_series.py <작업 폴더>/<결과 파일> --sheets <작업 폴더>/qa --json <작업 폴더>/qa/check.json
```
- 정적: 표식·id 중복·외부 자원·허브 카드↔편 일치·목차 칩·EDU_STUDY 메타 + **편마다 check_deck 정적 규칙 그대로**(아키타입·확인 문제·노트 분량).
- talk 편이면 check_deck talk 경고(예상 시간·시간 합계·대본 분량·제목 줄 수)가 0이고 `V` 발표자 보기를 열어 확인한다.
- 렌더: Chrome 으로 목차 시작 화면 확인 + 각 편의 모든 장·단계를 그려 넘침·글자 크기·대비·겹침 측정(solo check_deck 과 같은 기준).
- 허브 유형을 바꿨으면 그 유형으로도 1회 빌드해 check_series 를 돌린다(허브 3종 모두 같은 검사기를 쓴다).
- 최종 포털을 공통 반응형 계약의 6개 화면 조건에서 검사한다. 허브 3종, 편 열기·복귀·진도, 노트·퀴즈·회전·인쇄를 확인하고 실제 기기·다른 브라우저 미검증을 구분한다.
- WARN 은 읽고 판단한다. 편마다 "어떤 도식이 어디에 들어가는지"를 저작 때 정해 두고, 축소판·목차 화면 PNG(`--sheets`)을 직접 본다(solo 6단계와 같은 육안 기준). check_series·check_deck 통과는 디자인 승인이 아니다 — 배치 판단은 축소판을 직접 보고 내린다.
- **심미 크리틱**: 편마다 solo 6단계 기준 크리틱(`<base>/references/design-critique.md`)을 마친 뒤, 시리즈 전체(포털 표지·목록 카드·편 간 난이도 리듬)를 같은 9항목으로 1회 더 본다. Blocker 는 필수 수정, Major 는 개선 또는 수용 사유 기록.
- `외국어 문장`·글자 크기 경고는 `<base>/references/expression.md` 1·4절 기준으로 고친다.

### 5. 보고
- 결과 파일 경로, 편 수·총 장 수, 편 구성(라벨·제목·장 수 한 줄씩), 허브 유형과 고른 이유. 팩 편은 디자인·주흐름·보조활동·선택 이유와 성과 확인 활동을 함께 보고한다.
- 검사 결과: 편별 check_deck RESULT 줄 + check_series RESULT 줄 그대로. 못 돌린 검사는 이유와 함께.
- 심미 크리틱 결과: 편별 + 시리즈 전체 Blocker/Major/Minor 건수와 처리(수정 완료·수용 사유), 전후 비교 캡처 경로.
- 말투 교정 결과: 편별로 바뀐 줄 수·보류 줄·실행 못 한 교정 스킬.
- 확인 필요 목록: solo 보고 기준 + 시리즈 고유(편 나누기·허브 유형에 대한 사용자 확인 여부).
- 여는 법: 목차에서 편 카드를 눌러 열기 · 목차에서 숫자키로 편 열기 · Esc 또는 오른쪽 위 `목차` 로 복귀 · 편 안 조작은 solo 와 같음(→ 단계, S 자습, P 인쇄, G 용어집, 확인 문제) · 주소 `#` 목차, `#2-5` = 2번째 편 5장 · 진도·확인 문제 결과는 이 브라우저에 저장, 목차의 `기록 지우기`(두 번 누름)로 삭제.

## 반드시 지킬 것

- solo 의 "반드시 지킬 것" 전부(기준 덱 문장 불가져오기, 확인 안 된 수치 금지, 개인정보 금지, 검사 기준 못바꾸기).
- 편은 각각 완결된 학습 경험이어야 한다(목표·맥락·활동·확인 문제·성과 확인·마무리). 표지와 순서를 별도 장으로 강제하지 않고 주흐름에 맞게 배치한다. 편 간 중복 장은 허브·진도로 이어지지 않는 한 쓰지 않는다.
- series.json 의 편 폴더·편 수는 실제 폴더와 일치해야 한다(조립기가 검사한다).
- 공통 자산(`<base>`)을 이 스킬 폴더로 복사하지 않는다. 조립기가 shared 에서 읽는다.

## 파일 안내

| 파일 | 언제 읽나 |
|---|---|
| `<series>/references/series.md` | 1·3단계: 편 나누기 기준, 허브 유형 선택 규칙, series.json 양식, 진도·자습 동작 |
| `<base>/references/resource-packs.md` | 팩 편을 쓸 때(1·2단계): 편별 디자인·흐름 선택, 독립 생성·배치 변형·실제 노트·평가 증거 |
| `<base>/references/composition.md` · `research.md` | 2단계: 기본(legacy)/팩 분기, 공통 노트·자습·조사 규칙 |
| `<base>/references/layouts.md` · `expression.md` · `classes.md` · `icons.md` | 기본(legacy) 경로 편의 배치·표현 — 새 편의 기본 재료; 공통 동작 계약은 resource-packs.md에서 안내 |
| `<base>/references/diagrams.md` | 2단계 저작(기본·팩 공통): 개념 SVG 도식의 설계 규칙·문법·함정 |
| `<base>/assets/packs/` | 팩 편의 catalog·flows·독립 CSS·템플릿 |
| `<base>/assets/snippets/` | 기본(legacy) 경로 편의 조각 — 새 편의 기본 재료 |
| `<base>/assets/snippets/patterns/` | 기본 경로 편의 부품 조각(code·tabs·faq·pin-shot·fx) — 호스트 아키타입 본문 안에 넣는 부분 |
| `<series>/dev/portal_template.html` | 포털 뼈대(손으로 고칠 때만 — 다시 조립해야 반영) |
| `<series>/scripts/build_series.py` · `check_series.py` | 조립 · 시리즈 검사 (`--help`) |
| `<base>/scripts/build_deck.py` · `check_deck.py` · `verify_sources.py` · `env_check.py` · `extract_copy.py` | 편 단위 조립 · 검사 · 출처 검사 · 환경 확인 · 말투 교정용 글 추출/되돌리기 |
| `<base>/references/copyedit.md` | 편 단위 말투 교정(solo 5.5) 순서·되돌리기 규칙·내장 체크리스트 |
| `<base>/references/design-critique.md` | 4단계: 공통 심미 크리틱 — 편 단위 + 시리즈 전체(포털·편 간 리듬) 독립 검수·캡처 도구 |
