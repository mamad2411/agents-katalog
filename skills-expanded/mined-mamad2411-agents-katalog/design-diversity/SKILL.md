---
name: design-diversity
description: >-
  Claude가 산출하는 PPT·웹사이트 디자인의 천편일률 문제를 해결하는 '디자인 팩 카탈로그' 제작 오케스트레이터.
  공개 디자인 시스템·비주얼 스타일을 수집·증류해, Claude Code에 복붙하면 그 스타일이 재현되는 디자인 팩
  (prompt.md + tokens.json + preview.png + meta.yaml)을 만들고, baseline 대조로 다양성을 검증한 뒤
  GitHub 공개 레포 + 카탈로그 웹사이트로 발행한다. 7인 에이전트 팀(소싱·스키마·PPT집필·웹집필·렌더·다양성QA·발행)을
  파이프라인으로 조율한다. 트리거 — "디자인 다양성", "디자인 팩", "디자인 팩 카탈로그", "디자인 시스템 카탈로그",
  "PPT 디자인 다양화", "웹 디자인 팩", "프롬프트형 디자인 시스템", "Claude 디자인 천편일률", "디자인 팩 만들어줘".
  후속 작업 — "팩 추가", "PPT 팩 N개 더", "웹 팩 추가", "특정 팩만 다시", "다양성 검증 다시", "팩 재집필",
  "스키마 변경", "카탈로그 사이트 재배포", "레포 갱신", "재실행"도 모두 이 스킬로 처리한다.
  단순 PPT 1건 제작은 korean-premium-deck, 단순 웹사이트 1건은 frontend-design을 사용한다.
---

# Design Diversity — 디자인 팩 카탈로그 오케스트레이터

공개 디자인 시스템을 수집·증류해 Claude Code 복붙용 '디자인 팩' 카탈로그를 만들고, 다양성을 검증한 뒤 GitHub + 웹사이트로 발행하는 7인 에이전트 팀을 조율한다.

## 핵심 산출물 (확정 규격)

각 디자인 팩 = `design-packs/{slug}/` 안의 4개 파일:
- `prompt.md` — Claude Code에 복붙하는 자기완결적 디자인 지시문 (SSOT 사용처)
- `tokens.json` — 머신리더블 디자인 토큰 (color/type/spacing/motion)
- `preview.png` — 실제 샘플 렌더
- `meta.yaml` — 카테고리·스타일 계열·출처·라이선스

규격 정의는 `design-pack-schema` 스킬이 SSOT다. 1차 출범 규모 = PPT 20 + 웹 20 = 40팩.

## 실행 모드

**에이전트 팀** (단일 팀 7인, 작업 의존성으로 파이프라인 표현). 팀원은 `SendMessage`로 직접 조율, 산출물은 `_workspace/` 및 `design-packs/` 파일로 공유, 진행은 `TaskCreate`/`TaskUpdate`로 추적. 모든 Agent 호출은 `model: "opus"`.

| 에이전트 | 역할 | 주 스킬 |
|---|---|---|
| design-scout | 공개 디자인 시스템·스타일 후보 소싱 | design-sourcing |
| pack-architect | 스키마 SSOT·카탈로그 인덱스·다양성 게이트 | design-pack-schema |
| ppt-pack-curator | PPT 트랙 팩 집필 | ppt-design-idioms, design-pack-schema |
| web-pack-curator | 웹 트랙 팩 집필 | web-design-idioms, design-pack-schema |
| sample-renderer | 팩 적용 샘플 + baseline 렌더 | sample-rendering |
| diversity-qa | baseline 시각 대조·다양성 점수·반려 | diversity-scoring |
| catalog-publisher | GitHub 레포 + 카탈로그 사이트 발행 | catalog-publishing |

## Phase 0: 컨텍스트 확인

작업 시작 전 `_workspace/`와 `catalog.json` 존재를 확인해 실행 모드를 정한다.

- **초기 실행** — `catalog.json` 없음 → 전체 파이프라인 (Phase 1~5).
- **후속 — 팩 추가** — `catalog.json` 있음 + "팩 N개 추가" → Phase 1(빈 축만 소싱) → 2~5를 신규 슬러그에만 적용. 기존 팩 보존.
- **후속 — 부분 재실행** — "특정 팩만 다시", "다양성 검증 다시" → 해당 슬러그·해당 Phase만 재호출. 시작 전 기존 `_workspace/`를 `_workspace_prev/`로 백업.
- **후속 — 스키마/사이트만** — "스키마 변경"→ pack-architect 단독 + 마이그레이션 보고. "사이트 재배포"→ catalog-publisher 단독.

부분 재실행 시 어느 Phase부터 도는지 사용자에게 1줄로 알리고 진행한다.

## Phase 1: 소싱 (design-scout)

`TeamCreate`로 7인 팀을 만든 뒤, design-scout에 PPT·웹 두 트랙을 할당한다.
- 출력: `_workspace/01_scout_candidates-ppt.json`, `_workspace/01_scout_candidates-web.json`.
- 후보는 목표치(트랙당 20)보다 ~20% 많게. 후보끼리 시각적으로 충분히 구별돼야 한다.

## Phase 2: 스키마 락 + 팩 집필 (pack-architect → 두 curator 병렬)

1. pack-architect가 `design-pack-schema`를 확인·잠그고, 후보를 다양성 매트릭스로 솎아 `_workspace/02_architect_selected.json` + 초기 `catalog.json` 생성.
2. ppt-pack-curator와 web-pack-curator가 **병렬로** 각 트랙 팩을 집필 → `design-packs/{slug}/prompt.md` + `tokens.json` + `meta.yaml`.
3. pack-architect가 산출물 포맷·라이선스·중복을 검수. 위반 슬러그는 반려·재집필(최대 2회).

대규모(40팩)이므로 트랙별로 5팩씩 배치 집필을 권장 — 배치마다 Phase 3 검증을 이어 돌려 피드백을 빨리 받는다.

## Phase 3: 렌더 + 다양성 검증 루프 (sample-renderer → diversity-qa)

각 팩(또는 배치)에 대해:
1. sample-renderer가 동일 더미 콘텐츠로 팩 적용 샘플 + 트랙 baseline을 렌더 → `design-packs/{slug}/preview.png`.
2. diversity-qa가 baseline과 시각 대조 → `_workspace/04_qa_scorecard.json`.
3. `reject` 판정 → 사유의 축을 담은 채로 담당 curator에 재집필 요청 → 재렌더 → 재검증 (팩당 최대 2회).
4. 2회 후에도 미달이면 `escalate` — 발행하되 사이트에서 `draft` 배지.

전체 종료 시 diversity-qa가 팩 간 유사도 매트릭스(`_workspace/04_qa_diversity-matrix.md`)를 작성, 쌍둥이 팩은 pack-architect가 통합·재정의.

## Phase 4: 발행 (catalog-publisher)

1. 통과 팩 + `catalog.json`으로 GitHub 레포 구조화: `README.md`, `CONTRIBUTING.md`, `LICENSE`, `design-packs/`.
2. `site/`에 Next.js 15 카탈로그 웹사이트 빌드 — 갤러리·필터·prompt.md 원클릭 복사.
3. 자체 QA(빌드·카드 렌더·복사 동작·모바일) 후 Vercel preview 배포.
4. **production 배포는 사용자 명시 승인 후.** preview URL을 먼저 보고한다.

## Phase 5: 피드백 (Phase 7 진화)

발행 후 사용자에게 개선점·팀 구성 피드백 기회를 제공한다. 피드백 유형별 반영 대상은 `harness:harness` Phase 7-2 표를 따르고, 변경은 프로젝트 `CLAUDE.md` 변경 이력에 기록한다.

## 데이터 전달 프로토콜

- **태스크 기반**(`TaskCreate`) — 파이프라인 의존성·진행 추적.
- **파일 기반** — 중간 산출물은 `_workspace/{phase}_{agent}_{artifact}`, 최종 팩은 `design-packs/{slug}/`, 인덱스는 루트 `catalog.json`. `_workspace/`는 감사용으로 보존.
- **메시지 기반**(`SendMessage`) — 반려 사유·재소싱 요청 등 실시간 조율.

## 에러 핸들링

- 에이전트 실패 → 1회 재시도. 재실패 시 해당 산출물 없이 진행하고 최종 보고에 누락을 명시.
- 후보 부족 → design-scout 재소싱 1회, 그래도 부족하면 가능한 수로 진행 + 빈 축 보고.
- 팩 2회 반려 후 미달 → `escalate`(삭제 금지, draft로 발행).
- 라이선스 모호 → 팩을 드롭하지 말고 `license: unclear`로 표시, pack-architect가 1차 출처 확인.
- 렌더 실패 → `render_failed` 표시 후 사람 판단에 위임, 발행에서 자동 제외하지 않음.

## 테스트 시나리오

**정상 흐름:** "디자인 팩 카탈로그 만들어줘" → Phase 0(초기) → 소싱 40+α 후보 → 스키마 락 + 40팩 병렬 집필 → 렌더·검증 루프(반려분 재집필) → 레포 + 사이트 발행 → preview URL 보고 → production 승인 대기.

**후속 흐름:** "PPT 레트로 팩 5개 더 추가해줘" → Phase 0(팩 추가) → scout가 레트로 축만 소싱 → ppt-curator만 5팩 집필 → 렌더·검증 → catalog.json·사이트에 5카드 증분 반영.

**에러 흐름:** diversity-qa가 어떤 팩을 2회 반려 → `escalate` 처리 → 사이트에 `draft` 배지로 노출 → 최종 보고에 escalate 목록 명시.
