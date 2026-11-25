---
name: sample-return
description: Use when 샘플반납 탭/영역의 수정·조회·기능추가 요청을 받았을 때. 트리거 — "샘플반납", "샘플 반납", "sample-return", "/sample-return", "반납 리포트", "반납대상", "집계샘플", "샘플집계명", "상품 상세", "반품집계", "반납 시뮬레이션", "기한초과", "과락", "무판매", "교차부진", "배치 폴더 저장", "sample_ledger" (실제 반납 실행 판단은 returns-agent, 샘플 진행/종결 판정 정본은 sample-judgment-rule 메모리 — §경계)
---

# 샘플반납 탭 작업 — 라우팅 스킬

> 샘플반납(`SampleReturnView.js`)은 3모드(데이터 뷰 · 반납 리포트 · 교차추천) + 매장 상세 5서브탭으로 구성된다.
> 이 스킬은 **메인 Claude가 따르는 절차서**다.
> 영역을 식별 → 전담 에이전트로 위임(Agent 도구) → 결과 통합 → 전체 탭 회귀 검증.
> 탭 개발 표준은 `dev-blueprint` 스킬을 상위 규범으로 따른다(중복 서술 금지).

## 0. 영역 ↔ 에이전트 ↔ 파일 매핑

| # | 영역 | 에이전트 | 프론트 | API | DB |
|---|---|---|---|---|---|
| 0 | 셸 · 리포트 상단 | `sample-return-report-agent` | `SampleReturnView.js`(3모드·시뮬박스·전체핵심지표·통합엑셀 2종·이미지모달), `SampleReturnSummary.js`(데이터 뷰), `SampleReturnCompare.js`(매장간 비교) | `GET /api/sample-return/data`, `GET`·`PATCH /sim-settings` | `sample_return_sim_settings` |
| 1 | 매장 상세 | `sample-return-store-agent` | `SampleReturnStore.js` — 매장 KPI + 5서브탭(샘플집계명 상세 / 반납대상 / 집계샘플 / 상품 상세 / 반품집계) + 정렬 + 엑셀 2종 + 배치 폴더 저장 | `POST /api/sample-return/export-batch` | — (`.cache/batch/sample_return/<YYYYMMDD>/<매장명>/`) |
| 2 | 판정 정본 | `sample-return-logic-agent` | `sampleReturnLogic.js` — `classifyItem`/`classifyStore`/`computeCutoff`/`storeSummary`/`buildProductDetail`/`grandTotals`/컬러규칙 | — | — |
| 3 | 백엔드 파이프라인 | `sample-return-data-agent` | — | `/api/sample-return` 4엔드포인트 전체 | 11테이블(§아키텍처) + `rebuild_sample_return_db.py`·`run_sample_return_batch.py` |

공통 셸: `frontend/js/views/SampleReturnView.js` · `frontend/js/views/SnapshotHistoryBar.js`(교차추천 모드) ·
`frontend/js/api.js`(sample-return 메서드 4개).
공통 백엔드: `backend/app/routers/sample_return_router.py` · `backend/app/services/sample_return_service.py`(1544L) ·
`backend/app/services/sample_return_export_service.py`.

## 1. 작업 흐름

1. **요청 영역 식별** — 사용자 요청이 어느 영역(들)인지 §0 표로 판별. 불명확하면 AskUserQuestion.
2. **단일 영역** → 해당 에이전트 1개에 위임.
3. **여러 영역** → **병렬 위임**(단일 메시지에 다중 Agent 호출).
4. **결과 통합** — 각 에이전트 변경/리스크를 메인이 취합.
5. **전체 탭 회귀 검증** — §3.

## 2. 위임 규칙 (공유 자산 주의)

영역은 독립이 아니다. 아래 **공유 자산**을 건드리는 작업은 영향받는 에이전트를 **모두** 위임하거나
메인이 직접 조정한다(`service/sample-return-architecture.md`로 영향 범위 확인):

- **판정 정본 이중화(JS ↔ py)** — 반납 판정은 `sampleReturnLogic.js`(프론트 라이브 재계산)와
  `sample_return_service.py`(원자재 산출·경과일·점수)에 **2곳으로 나뉘어 있다**. 기한·과락·무판매·교차
  규칙을 바꾸면 **양쪽을 동시에** 고쳐야 한다(커밋 347bfe6 기한초과 게이트 개정 = 이 사고 지점).
  → 반드시 `sample-return-logic-agent` + `sample-return-data-agent` 동시 위임.
- **`sampleReturnLogic.js` 순수함수** — `classifyStore`는 셸이, `storeSummary`/`grandTotals`는 셸+Compare가,
  `buildProductDetail`은 셸(통합엑셀)+Store(상품상세)가 소비한다. 시그니처·반환키 변경은 4파일 회귀.
- **`appliedSim` 4파라미터**(`fWeeks`/`mWeeks`/`scoreCut`/`crossMin`, 기본 여21·남28·컷30·교차2) —
  셸이 소유하고 Store·Compare 에 props 로 내려간다. DB(`sample_return_sim_settings`)에도 영속된다.
  파라미터 추가는 프론트 3곳 + service `_SIM_FIELDS`/`_SIM_BOUNDS` + DDL 을 동시에.
- **`items._checked` 라이브 상태** — 매장별 체크가 `report` 배열의 원본 item 에 직접 붙는다.
  전체 핵심지표·매장간 비교·집계기준 통합엑셀이 전부 이걸 읽는다. 체크 모델 변경은 전 영역 회귀.
  (⚠ 상품상세 개별 토글은 `SampleReturnStore` **로컬 휘발성** — 통합엑셀은 기본 분류 기준 산출.
   의도된 설계이며 UI 라벨로 명시돼 있다. 승격 시도 전 `SampleReturnStore.js` 주석 FIX⑥ 필독.)
- **`sample_ledger` + `sample_products` LATERAL 매칭** — `sample_products` 는 period 마다 누적 INSERT 라
  **최신 1건만** 취해야 한다. 정본 규칙 = `.claude/memory/domain/sample-judgment-rule.md`.
- **`_RESULT_CACHE` 데이터 버전 스탬프** — 라이브 스코어가 무거워(매장별 수십초) 입력 테이블 최신도로
  캐시한다. 새 입력 테이블을 참조하면 `_data_version_stamp` 에도 추가해야 stale 이 안 난다.

단일 영역에 갇힌 작업(예: 매장간 비교표 색상만 변경)은 해당 에이전트 단독.

## 3. 회귀 검증 (dev-blueprint 스킬 §6 게이트 재사용)

- **import 스모크**(필수): `python -c "from app.routers import sample_return_router"` 무에러 — 또는 배포 후
  `Application startup complete` + `/docs` 200. (`py_compile`만으론 미충족)
- **3모드 렌더**: 데이터 뷰 / 반납 리포트 / 교차추천(iframe) 전부 정상, **콘솔 에러 0**.
- **매장 5서브탭**: 8매장 각각 샘플집계명 상세·반납대상·집계샘플·상품 상세·반품집계 전환·정렬 동작.
- **시뮬 왕복**: 여/남 기한·점수 컷오프 변경 → `시뮬레이션 적용` → 분류·KPI·컷오프 즉시 재계산 →
  새로고침 후에도 DB 저장값 복원. `기본값` 버튼 → 여21/남28/컷30/교차2 복원.
- **엑셀 4종**: 매장 집계기준·매장 반납기준·전매장 집계기준·전매장 상품상세 전부 생성.
  배치 폴더 저장은 `rel_path`·`row_count` 응답 확인.
- **판정 정합**: 판정 규칙을 바꿨다면 **통합재고관리 `진행중샘플` 탭도 회귀**(공유 규칙 — §경계).
- **빌드리스 유지**(CDN Vue + ES모듈), **다른 탭 무손상**(라우팅 독립).
- 공유 자산 변경 시 §2의 교차 영향 영역을 실제로 다시 확인.

## 4. 작업 전 필독

- `.claude/memory/domain/sample-return.md` — 업무 규칙·용어·영역 관계
- `.claude/memory/domain/sample-return-feedback.md` — 과거 지적 누적(F1~)
- `.claude/memory/service/sample-return-architecture.md` — Vue/API/DB/데이터 흐름
- `.claude/memory/domain/sample-judgment-rule.md` — 샘플 진행/종결 판정 **공용 정본**
- `dev-blueprint` 스킬 — 탭 개발 표준(상위 규범)

## 경계 — returns-agent / inventory / md-agent 와 혼동 금지

트리거 키워드(반납·반품·샘플)가 겹친다. **"탭개발 vs 업무실행"** 으로 가른다.

- **이 스킬/sample-return-\*-agent** = 샘플반납 **탭 자체**의 화면·API·DB 개발/수정.
  「탭이 안 뜬다 / 컬럼 추가 / 반납대상이 0건이다 / 엑셀이 틀리다」
- **returns-agent**(업무실행) = 실제로 무엇을 반납·반품할지 **결정하고 실행**, 반품처리원장 기록.
- **`inventory` 스킬** = 별개 탭(`/inventory`) 통합재고관리. 단 **`진행중샘플` 판정 규칙은 공유** —
  판정을 건드리면 `inventory-sample-agent` 를 **함께** 위임한다.
- **`샘플교차추천`·`샘플오버뷰`** 는 별개 탭이다. 이 탭의 `교차추천` 모드는 그 스냅샷 HTML 을
  iframe 으로 얹은 것뿐이라, 내용 수정 요청은 `generate_sample_cross_report.py` 쪽 별건이다.
- **md-agent**(기획) = 샘플을 *입력 축*으로 쓰는 주문추천·포트폴리오 결정.
