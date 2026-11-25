---
name: tds-ui
label: TDS UI 선택과 form 패턴
category: core
order: 3
description: Decision skill for choosing TDS React Native components and UI boundaries in MiniApp screens. Use when translating product requirements into TDS components, reconciling public docs with actual exports, or deciding controlled/uncontrolled state patterns. Do not use for route design, capability lookup, provider/runtime work, or non-TDS native module decisions.
version: 2.0.0
---

# TDS UI Decision Skill

이 Skill은 MiniApp 화면 요구사항을 TDS React Native 컴포넌트로 정확히 매핑할 때 사용한다.
이 Skill의 목적은 "어떤 TDS 컴포넌트를 언제 써야 하는지"를 결정하고, 공개 문서와 실제 export 차이까지 같이 처리하는 것이다.

## Use when

- 입력/선택 UI를 결정해야 할 때
- 리스트, 요약, 스텝, 카드, 배너, 차트 같은 화면 구성 요소를 정해야 할 때
- 로딩/에러/완료/토스트/다이얼로그 같은 상태 UI를 정해야 할 때
- 상단/하단 UI boundary를 정해야 할 때
- 공개 문서 slug와 실제 export가 일치하는지 확인해야 할 때

## Do not use for

- MiniApp capability / API 탐색
- route path, navigation tree, page entry 설계
- provider/runtime bootstrap
- TDS 밖 native module 선택

## Read in order

1. `generated/catalog.json`
2. `generated/anomalies.json`
3. `references/decision-matrix.md`
4. `references/form-patterns.md`
5. `references/layout-and-navigation.md`
6. `references/feedback-and-loading.md`
7. `rules/*.md`

## Decision algorithm

1. 요구사항을 먼저 분류한다.
   - text-input / search / multi-select / single-select / boolean-toggle / content-tabs / menu
   - numeric-stepper / keypad / range-slider / rating
   - list / list-summary / grid / accordion / step-flow / hero-amount / article / disclaimer / chart
   - primary-action / text-action / icon-action / dialog / toast / loading / result / error-page
   - top-nav / bottom-action / sheet
2. 문서가 있고 root export도 명확한 컴포넌트를 먼저 고른다.
3. docs slug mismatch는 catalog alias를 따른다.
   - `chart` -> docs `Chart/bar-chart`
   - `stepper-row` -> docs `stepper`
4. export mismatch는 anomaly 규칙을 따른다.
   - `navbar`는 docs는 있지만 root export path가 다를 수 있으므로 catalog의 `rootImportPath`를 먼저 확인한다.
5. public docs 없는 export는 기본 추천 대상이 아니다.
   - `agreement`, `bottom-cta`, `bottom-sheet`, `fixed-bottom-cta`, `icon`, `tooltip`, `top`, `txt`
   - 이 항목은 사용자가 명시적으로 요구하거나 기존 코드베이스에서 이미 쓰고 있을 때만 추천한다.
   - 추천 시 반드시 `export-only / docs-missing`이라고 표시한다.
6. `paragraph`는 기본 추천 금지다.
   - component dir는 있지만 root export와 public docs가 약하다.
7. 상태 관리는 문서 기준을 그대로 따른다.
   - controlled: `value`/`onChange`, `checked`/`onCheckedChange`, `onValueChange`
   - uncontrolled: `defaultValue`, `defaultChecked`
8. 최종 답변에는 반드시 아래를 포함한다.
   - 추천 컴포넌트
   - 왜 이 컴포넌트인지
   - 왜 가장 가까운 대안이 아닌지
   - controlled/uncontrolled 패턴
   - loading / error / empty / disabled / a11y 고려사항
   - docs URL
   - root export module
   - anomaly note 여부
   - 위 7항 중 하나라도 빠지면 `incomplete answer`로 간주한다.
   - export-only를 추천할 때는 반드시 doc-backed fallback도 같이 적는다.
9. TDS로 대체 가능한 RN primitive를 직접 추천하지 않는다.

## Default selection map

- 자유 텍스트 입력: `text-field`
- 검색 입력: `search-field`
- 다중 선택: `checkbox`
- 단일 선택: `radio`
- 시각적으로 압축된 단일 선택: `segmented-control`
- 즉시 반영되는 on/off 설정: `switch`
- 콘텐츠 섹션 전환: `tab`
- 오버플로 메뉴/액션 메뉴: `dropdown`
- 정수 증감: `numeric-spinner`
- 숫자 패드 입력: `keypad`
- 연속 값 선택: `slider`
- 평점 표시/입력: `rating`
- 기본 액션: `button`
- 약한 액션/링크성 액션: `text-button`
- 아이콘만 있는 액션: `icon-button`
- 블로킹 확인/안내: `dialog`
- 짧은 비차단 피드백: `toast`
- 스피너 로딩: `loader`
- 레이아웃형 로딩 placeholder: `skeleton`
- 수치형 진행 상태: `progress-bar`
- 작업 결과 전체 화면: `result`
- 상태코드 기반 오류 페이지: `error-page`
- 기본 세로 목록: `list` + `list-row`
- 섹션 헤더: `list-header`
- 더보기/목록 확장 footer: `list-footer`
- key/value 요약: `table-row`
- 그리드 배치: `grid-list`
- FAQ/아코디언: `board-row`
- 단계 흐름 요약: `stepper-row`
- 상단 네비게이션: `navbar`
- 큰 금액 hero: `amount-top`
- 하단 안내/법적 고지: `bottom-info`
- 긴 설명/공지/본문: `post`
- 미디어/아이콘/Lottie 프레임: `asset`
- 상태 배지: `badge`
- 가로 스와이프 카드/배너: `carousel`
- 막대형 데이터 시각화: `chart`
- 튜토리얼/온보딩 강조: `highlight`
- 구분선/구간 나누기: `border`
- 그림자/그라데이션 효과: `shadow`, `gradient`

## Required comparisons

- `text-field` vs `search-field`
- `checkbox` vs `switch`
- `radio` vs `segmented-control` vs `tab`
- `numeric-spinner` vs `keypad` vs `slider`
- `button` vs `text-button` vs `icon-button`
- `toast` vs `dialog` vs `result` vs `error-page`
- `list-row` vs `table-row`
- `bottom-info` vs `post`
- `doc-backed` vs `export-only / docs-missing`

## Refusal / fallback rules

- 문서도 없고 기존 코드베이스 근거도 없으면 export-only 컴포넌트는 추천하지 않는다.
- 대신 doc-backed 조합으로 대체안을 제시한다.
- unknown bottom action surface는 우선 `button` 중심 조합으로 답하고 anomaly note를 남긴다.
