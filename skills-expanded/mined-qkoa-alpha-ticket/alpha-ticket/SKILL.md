---
name: alpha-ticket
description: "Run the user's Alpha ticket workflow only for an explicit 알파티켓/자동알파티켓 start, an Alpha ID with a stage phrase, or a continuation trigger such as 설계 승인, 커밋 승인, 리뷰 검토, 패치루프, 티켓 클로즈 while an Alpha ticket is active. Assemble task-scoped context from WORK, INDEX, QUEUE, linked source documents, code, and tests; preserve architecture, contract, evidence, and approval boundaries; and use Fast/Core/Strict without micromanaging implementation."
---

# Alpha Ticket

알파티켓은 구현 방법을 통제하지 않는다. 장기 작업에서 사용자가 다시 판단할 수 있도록 **범위·계약·아키텍처·상태·증거·승인 경계**만 보존한다.

일반 코딩 요청에는 적용하지 않는다. 새 흐름은 `알파티켓`, `자동알파티켓`, 또는 Alpha ID와 단계 문구가 함께 있을 때만 시작한다. ID 없는 단계 문구는 활성 Alpha 티켓이 있을 때만 이어서 처리한다.

## 1. 작업 컨텍스트 조립

1. 현재 요청과 활성 ID를 확인한다.
2. `.jaw/alpha.toml`의 `docs_root`를 우선하고, 없으면 실제 Alpha 문서가 있는 `docs/` 또는 `custom/docs/`를 고른다.
3. QUEUE의 해당 행과 WORK의 헤더·A–D를 읽어 scope를 탐색 울타리로 삼는다.
4. INDEX 전체를 출력하지 않는다. 현재 ID·WORK 소유 표의 `name`·직접 언급된 문서 ID만 검색해 일치하는 Documents·Architecture 행과, 그 ID·name이 `from | to | declared by`에 있는 Relations 행만 고른다. ID는 `| WU-1 |`처럼 표 셀 경계를 포함해 정확히 찾고 `WU-1`이 `WU-10`에 걸리는 부분 일치를 쓰지 않는다.
5. 선택한 행의 직접 연결에서 필요한 원본·소비자·계약을 한 단계씩 넓히고, 선택된 WORK 계약·Memory·IR/OL/RFT, 실제 코드 경계, 검사만 읽는다.

INDEX는 커질 수 있는 영속 지도다. 전체 정합성은 `alpha_lint`에 맡기고, 모델 컨텍스트에는 현재 작업과 일치한 행만 가져온다. `feature family`는 Architecture `name` 충돌 구분, PRD Feature 정의 확인, Memory M 항목 범위 선택에만 쓰며 문서나 관계의 대량 선택 검색어로 쓰지 않는다. 현재 표의 열을 모를 때만 각 섹션의 헤더를 확인한다. 검색 결과가 없거나 계약 충돌·공개 연결점 변경·scope 밖 diff가 확인될 때만 관련 식별자로 탐색을 제한적으로 넓힌다. 무관한 INDEX 행·원본·과거 WORK·reference·저장소는 한꺼번에 읽지 않으며 원본끼리 충돌하면 임의로 합치지 않는다.

## 2. 원본 책임과 상태

| 원본 | 책임 |
|---|---|
| WORK | 작업 계약, 결정, 검증된 결과, 상태 전환 이력 |
| QUEUE | 실행 순서, 현재 blocker, 바로 다음 행동 |
| INDEX | 문서 등록, 현재 모듈·공개 연결점의 소유 위치와 검사, 재탐색할 가치가 있는 현재·장기 관계, 5-WU 의미 감사 포함 범위 |
| IR / OL / RFT | 문제·조사 / 미결정 / 개선 제안과 각 처분 |
| Memory | 명시적으로 확인된 사용자 선호와 장기 제품 방향 |
| PRD | Feature 이름과 짧은 정의 |

WORK 상태는 `open → ready → active → closed`를 사용하고 어느 단계에서든 `cancelled`로 갈 수 있다. blocker가 생겨도 상태는 유지하고 QUEUE에 적는다. IR·OL·RFT는 `open | pending | closed | cancelled`, Memory는 `active | superseded`를 사용한다.

같은 사실을 여러 문서가 독립 소유하지 않게 한다. QUEUE와 INDEX의 상태는 원본에서 가져온 표시값이다. 별도 Decisions, Resume Packet, 세션 checkpoint 문서·블록, 세션 인계 요약을 새로 만들지 않는다. INDEX의 Semantic audit checkpoints는 통과한 5-WU 시작 범위만 가리키는 최소 색인이다.

## 3. 모드

실패 결과의 크기로 최소 충분한 모드를 고르고 WORK에 근거 한 줄을 남긴다.

| 모드 | 기준 | 종료 후보 검증 |
|---|---|---|
| Fast | 공개 계약·자료 의미·소유권을 바꾸지 않는 작고 되돌리기 쉬운 변경 | focused 이상 |
| Core | 나머지 일반 변경 | related |
| Strict | 자료 손상·복구 실패·권한 침해·금융 의미 오류·비가역 이관·서비스 간 공개 계약 파손·조용한 오답 가능 | related + full |

작업 중 Strict 위험이 드러나면 즉시 올린다. 실제 Strict 경계를 바꿨으면 그 변경을 제거하고 다시 검증하지 않는 한 낮추지 않는다.

## 4. 진행 흐름

| 트리거 | 수행 | 정지점 |
|---|---|---|
| `알파티켓 <id>` | 필요한 최소 컨텍스트와 얇은 PRD·빈 Memory만 준비해 설계 전 분할을 판단한다. 단일 진행이면 WU를 `open`으로 만들고 설계한다 | 분할 승인 또는 설계 승인 요청 |
| `자동알파티켓 <id>` | 같은 분할 판단을 먼저 한다. 단일 진행이면 WU 생성·설계 후 바로 구현·검증한다 | 분할 승인 또는 커밋 승인 요청 |
| `단독 설계`, `설계 문서만` | 설계와 요청 문서만 갱신한다 | 구현하지 않음 |
| `설계 승인` | WU를 `ready`, 구현 시작 시 `active`로 바꾸고 구현·검증한다 | 커밋 승인 요청 |
| `커밋 승인` | 승인 diff를 commit하고, 원격이면 push·PR·필요한 리뷰까지 시작한다 | 리뷰 결과 또는 close 준비 |
| `리뷰 검토`, `패치루프`, `티켓 클로즈` | finding 판정·수용 패치·재검증·감사·종료 정리를 수행한다 | 필요한 승인 또는 종료 |
| 초기화, IR/WU/OL/RFT, 정합성 점검, 결과 요약 | 요청한 운영 범위만 수행한다 | 요청 범위 |

`알파티켓` 트리거는 WORK·QUEUE·INDEX의 설계 기록까지 승인한다. `설계 승인`이 런타임 구현을 승인한다. `자동알파티켓`은 구현까지 승인하지만 commit은 승인하지 않는다.

첫 Alpha 스캐폴딩에서는 WU 설계 전에 기존 PRD에서 `feature family`와 정의를 확인한다. 두 값이 명확하지 않을 때만 `<docs_root>/prd.md`를 만들며 그 밖의 내용을 필수로 늘리지 않는다. 이때 Memory 항목이 없어도 canonical 템플릿으로 빈 `<docs_root>/memory.md`를 항상 만든다.

새 요청은 WU 파일을 만들거나 기존 WORK 범위를 바꾸기 전에 한 사용자 결과·한 승인 경계·한 연결된 검증 묶음으로 닫히는지 한 번 판단한다. 독립 준비 작업과 제품 변경을 각각 승인·검증·되돌릴 수 있고 중간 종료해도 각각 유효하면 권장 분할 하나와 선행 순서만 제시하고 사용자 수용을 기다린다. 분할하지 않으면 판단을 보고하거나 기록하지 않고 단일 설계를 계속한다. 세부 기준은 `references/design.md`를 따른다.

첫 스캐폴딩 뒤에는 설계 승인을 요청하기 전에 전체 alpha_lint의 error 0을 확인한다. 오류가 있으면 승인 요청 단계로 넘어가지 않는다.

설계는 하나만 작성한다. 사용자 의미를 결정할 수 없으면 대안을 늘어놓지 말고 필요한 질문을 한다. 지금 닫지 않을 내용은 OL, 개선 제안은 RFT, 문제와 조사 결과는 IR로 분리한다.

## 5. 실행 경계

- 설계 승인 전 일반 알파티켓 구현을 시작하지 않는다.
- 커밋 승인 전 commit·push·PR·리뷰 요청을 하지 않는다.
- 별도 게시 승인 게이트를 만들지 않는다. 사용자가 명시적으로 범위를 좁히면 그 범위를 따른다.
- 원본 삭제, 파괴적 이관, 비가역 외부 쓰기, 비용 발생, 보안 경계 변경은 계약이 닫히지 않았으면 확인받는다.
- unrelated dirty/untracked 작업을 보존하고 승인 diff에 섞지 않는다.
- 실제 diff가 WORK scope·소유 표 밖으로 나가면 계약을 먼저 바로잡는다.
- 새 제품 코드는 Feature 안에서 시작한다. 확인된 공통 계약은 실제 독립 구현 단위로 Foundation에, 제품 의미를 모르는 실행 수단은 Platform에 추출한다. 여러 Feature를 실제로 조립할 때만 Workflow를 만든다.
- 문서의 layer 표기만 바꾸거나 빈 전달 모듈을 만들지 않는다. Feature끼리 내부 코드를 직접 사용하지 않고 공개 연결점을 통한다. 테스트는 검증 대상의 소유 구역을 따르고 별도 레이어를 만들지 않는다.

구현 방법과 도구 순서는 모델이 고른다. focused 검사는 WORK 소유 표의 `check`에서 선택한다. related 검사는 변경한 공개 연결점의 역방향 `uses`로 직접 소비자를 찾고, 그 소비자가 `exposes`하는 공개 연결점들의 Architecture `check`에서 선택한다. 현재 유효한 검사는 Architecture `check`, 이번 작업이 계약한 검사는 WORK 소유 표 `check`, 그때 실행한 결과는 WORK E가 소유한다. INDEX에 새 `verified_by`·`affects` 관계를 만들지 않는다. 확인하지 못한 검사나 실제 코드 경계를 통과로 쓰지 않는다.

모드별 종료 후보 검증 뒤, WORK E를 확정하거나 커밋 승인을 요청하기 전에 `references/implement-verify.md`의 구조 감사를 통과한다. 현재 변경의 실제 코드 경계, 공통 책임, WORK A–D와 INDEX Architecture·Relations를 대조하고 finding이 남으면 영향 검사와 구조 감사를 다시 수행한다. 통과한 실제 diff만 승인 대상으로 제시한다.

Fast는 별도 리뷰 없이 종료 후보가 될 수 있다. Core·Strict는 리뷰어 한 명을 사용한다. 독립 리뷰는 커밋 승인과 commit 뒤에만 시작한다. 원격에서는 PR 리뷰, 로컬에서는 리뷰 서브에이전트를 사용하며 둘을 중복하지 않는다. 리뷰 패치로 새 diff가 생기면 다시 커밋 승인을 받는다.

리뷰 패치가 제품 코드·실제 모듈 경계·공개 연결점·직접 소비 관계·WORK A–D·INDEX Architecture·Relations를 바꾸면 이전 구조 감사는 무효다. 영향 검사와 모드별 종료 후보 검증, 구조 감사로 돌아간 뒤 커밋 승인을 다시 받는다.

## 6. 상태와 보고

상태가 바뀔 때 WORK 이력, QUEUE 표시, INDEX 표시를 함께 맞춘다. `closed`·`cancelled` WU는 QUEUE에서 제거하고 WORK와 INDEX에는 보존한다.

일반 close에서는 같은 diff의 구조 감사를 반복하지 않는다. 마지막 구조 감사 뒤 관련 코드·소유 경계가 바뀌지 않았는지와 HEAD가 승인·커밋된 감사 대상과 같은지만 확인한다. 현재 active WU를 닫기 직전의 기존 closed 수에 1을 더한 값이 5의 배수이면, 최종 리뷰와 모든 패치가 끝난 후보 HEAD에서 병합·배포·closing lint·상태 종료 전에 의미 감사를 수행한다. 기존 Semantic audit checkpoints에 포함되지 않은 closed WU 네 개와 현재 active WU를 시작 범위로 쓰며, 정확히 다섯 개가 아니면 close하지 않는다.

의미 감사 통과 근거를 WORK E에 기록한 뒤 현재 WU의 checkpoint 행을 추가하고 closing lint를 실행한다. finding이 남으면 현재 WU를 `active`로 유지하고 QUEUE의 blocker·next로 같은 WU에서 수정한다. 승인된 WORK A–D 안의 수정에는 새 WU·후속 문서·새 세션을 만들지 않으며, 사용자 의미·수용 기준·범위·비가역 경계의 판단이 필요할 때만 사용자에게 멈춘다.

구조 감사 뒤 커밋 승인 요청 때 실제 diff와 검사 결과를 대조한 Implementation Result만 WORK E에 기록한다. 리뷰 패치 뒤에는 최신 결과로 교체하고 close 때 확정한다.

커밋 승인 요청에는 focused·related로 선택한 검사 개수와 실행 결과를 적는다. related 집합이 비었거나 영향 범위의 공개 연결점에 `check=none`이 있으면 그 사실도 명시한다.

사용자에게는 단계 전환이나 결정이 있을 때만 현재 단계, 핵심 증거, 필요한 결정, 다음 한 동작을 압축해 보고한다.

## 7. Reference

- 설계·수직 슬라이스·아키텍처 경계가 필요할 때 `references/design.md`를 읽는다.
- 구현·검사 선택·구조 감사·Implementation Result가 필요할 때 `references/implement-verify.md`를 읽는다.
- commit·리뷰·패치 재진입·close·의미 감사가 필요할 때 `references/review-close.md`를 읽는다.
- 초기화·PRD·INDEX·IR/OL/RFT·Memory·정합성·레거시 호환이 필요할 때 `references/operations.md`를 읽는다.
- 기존 Alpha 문서를 현재 형식으로 옮길 때 `references/migration-v3.2.1.md`를 읽는다.

현재 단계에 필요한 reference만 읽는다. 프로젝트 고유 사실은 이 스킬이 아니라 해당 저장소의 PRD·WORK·INDEX·Memory에 둔다.
