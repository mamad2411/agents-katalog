---
name: design-spec-generate
description: 웹사이트 디자인 명세 생성 스킬. web-designer 에이전트가 사용한다. Figma URL이 입력에 있으면 figma-read를 호출하고 없으면 텍스트 요구사항을 기반으로 화면 명세 + 컴포넌트 분해 + 와이어프레임 SVG를 작성한다. Track 디렉토리의 1_REQ-SNAPSHOT, 2_WORK-SPEC, 3_FEATURE-CHECKLIST, 5_ARCHITECTURE, 6_SPEC 문서를 일관된 포맷으로 채운다. "디자인 명세", "화면 분해", "와이어프레임 생성", "Figma 읽기 후 명세" 같은 작업에 트리거된다.
---

> 산출 문서는 `html-doc` 스킬 규칙을 따라 자체 완결 HTML로 작성한다.
> 산출 HTML 문서에는 html-doc 스킬의 시각화 가이드에 따라 인라인 SVG 다이어그램을 1개 이상 포함한다.

# Design Spec Generate

웹사이트 디자인 단계의 산출물(Track 문서 5종 `.html` + 와이어프레임 인라인 SVG)을 일관된 포맷으로 생성하는 워크플로우.
산출 문서는 `html-doc` 스킬의 `references/template.html`을 skeleton으로 작성하고, 인라인 SVG 다이어그램을 1개 이상 포함한다.

## 입력

호출자(web-designer 에이전트)가 다음을 전달:
- `track_dir`: `.claude/tracks/{track_id}/` 절대 경로
- `requirement`: 원본 요구사항 텍스트 (Figma URL 포함 가능)
- `mode`: `"initial"` 또는 `"partial-rerun"`

## 워크플로우

### Step 1: 입력 정규화

1. `requirement`에서 Figma URL 패턴 검출:
   - `figma.com/design/...`, `figma.com/file/...`, `figma.com/board/...`
2. URL 있으면 → `figma-read` 스킬 호출 → 디자인 메타데이터/스크린샷/노드 정보 획득
3. URL 없으면 → 텍스트 요구사항을 그대로 사용

### Step 2: 화면/컴포넌트 분해

요구사항을 다음 단위로 분해한다:

| 단위 | 식별 기준 | 예시 |
|------|----------|------|
| **페이지(Page)** | 독립 URL을 가지는 화면 | `/signup`, `/admin/users` |
| **컴포넌트(Component)** | 페이지 내 재사용 가능한 DOM 구획 | 헤더, 푸터, 폼 그룹, 모달, 테이블 |
| **필드(Field)** | 사용자 입력 또는 표시 데이터 | email, password, 사용자명 |
| **액션(Action)** | 사용자 인터랙션 | "가입 버튼 클릭", "이메일 검증" |

각 페이지마다 (필드 목록, 액션 목록, 검증 규칙)을 명세한다.

### Step 3: 1_REQ-SNAPSHOT.html 작성

`html-doc` 스킬의 `references/template.html`을 skeleton으로 사용한다.
산출 HTML 문서에는 html-doc 스킬의 시각화 가이드에 따라 인라인 SVG 다이어그램을 1개 이상 포함한다.

```html
<!-- 1_REQ-SNAPSHOT.html 구조 예시 -->
<!-- html-doc/references/template.html 기반 -->
<!-- <section>: 요구사항 원본(원문 <pre> 블록), 출처·일시 메타 -->
<!--   Track ID, 원본 출처(Figma URL | 사용자 입력 | req.md 경로), 스냅샷 일시(ISO 8601) -->
<!-- 인라인 SVG: 요구사항 출처 흐름(Figma/텍스트 → Track) 1개 -->
```

### Step 4: 2_WORK-SPEC.html 작성 (도메인별 분해)

`html-doc` 스킬의 `references/template.html`을 skeleton으로 사용한다.
산출 HTML 문서에는 html-doc 스킬의 시각화 가이드에 따라 인라인 SVG 다이어그램을 1개 이상 포함한다 (예: Phase 타임라인 SVG).

```html
<!-- 2_WORK-SPEC.html 구조 예시 -->
<!-- html-doc/references/template.html 기반 -->
<!-- <section>: 개요(목표/범위/도메인), Phase 1~4 체크리스트(<table>+배지) -->
<!-- 인라인 SVG: Phase 타임라인 다이어그램 1개 -->
<!-- Phase 4 참조: <a href="9_QA-REPORT.html"> -->
```

### Step 5: 3_FEATURE-CHECKLIST.html 작성

사용자/QA 관점의 체크리스트. 각 항목은 6_SPEC.html의 화면/액션과 1:1 대응되도록 작성.
`html-doc` 스킬의 `references/template.html`을 skeleton으로 사용한다.
산출 HTML 문서에는 html-doc 스킬의 시각화 가이드에 따라 인라인 SVG 다이어그램을 1개 이상 포함한다.

```html
<!-- 3_FEATURE-CHECKLIST.html 구조 예시 -->
<!-- html-doc/references/template.html 기반 -->
<!-- <section>: 화면별 체크리스트(<table> + 배지 badge-ok/badge-warn/badge-err) -->
<!-- 비기능 항목은 별도 <section> -->
<!-- 인라인 SVG: 화면-기능 관계 구조도 1개 -->
```

### Step 6: 5_ARCHITECTURE.html 작성

`html-doc` 스킬의 `references/template.html`을 skeleton으로 사용한다.
산출 HTML 문서에는 html-doc 스킬의 시각화 가이드에 따라 인라인 SVG 다이어그램을 1개 이상 포함한다.
SVG는 `svg-diagram` 스킬로 생성하되 외부 파일이 아닌 본문에 **인라인 `<svg>`**로 임베드한다.

```html
<!-- 5_ARCHITECTURE.html 구조 예시 -->
<!-- html-doc/references/template.html 기반 -->
<!-- <section>: 화면 흐름도(인라인 SVG), 페이지 구조 표(<table>), 와이어프레임 인라인 SVG -->
<!-- 인라인 SVG: 화면 흐름도, 와이어프레임 각 1개 이상 -->
```

### Step 7: 6_SPEC.html 작성 (핵심 문서)

`html-doc` 스킬의 `references/template.html`을 skeleton으로 사용한다.
산출 HTML 문서에는 html-doc 스킬의 시각화 가이드에 따라 인라인 SVG 다이어그램을 1개 이상 포함한다.

```html
<!-- 6_SPEC.html 구조 예시 -->
<!-- html-doc/references/template.html 기반 -->
<!-- <section>: 화면별 필드 표(<table>), 액션 표, API 계약 초안(<details>+<pre>) -->
<!-- 인라인 SVG: 데이터·처리 흐름도 1개 이상 -->
<!-- API 상태 배지: badge-warn (초안), badge-ok (확정) -->
```

### Step 8: 와이어프레임 SVG 생성

`svg-diagram` 스킬을 사용하여 각 화면당 1개의 SVG를 생성. 박스/레이블 위주의 간단한 와이어프레임. 색상은 흑백 + 강조 1색.

SVG는 5_ARCHITECTURE.html 본문에 인라인 `<svg>`로 임베드한다 (자체 완결 단일 파일 원칙, 외부 파일 참조 금지).

### Step 9: 0_INDEX.html 자동 생성

문서가 2개 이상이면 자동 생성/갱신. 번호순 + 한 줄 요약. `html-doc` 스킬의 `references/template.html`을 skeleton으로 사용한다.
산출 HTML 문서에는 html-doc 스킬의 시각화 가이드에 따라 인라인 SVG 다이어그램을 1개 이상 포함한다 (예: 문서 관계도).

## partial-rerun 모드

`mode == "partial-rerun"`일 때:
1. 기존 6_SPEC.html을 먼저 읽기
2. 사용자 피드백을 기준으로 변경 대상 화면/필드/액션만 식별
3. 해당 섹션만 수정 + 와이어프레임 인라인 SVG 재생성
4. 6_SPEC.html 상단 `Changelog` 섹션에 변경 이력 추가

## 폴백 동작

- Figma MCP 미연결 또는 figma-read 실패: 텍스트 요구사항으로 진행, 1_REQ-SNAPSHOT.html의 "원본 출처"에 폴백 사유 명시
- svg-diagram 실패: ASCII 와이어프레임을 `<pre>` 블록으로 5_ARCHITECTURE.html에 직접 작성

## 완료 체크리스트

- [ ] 1_REQ-SNAPSHOT.html 존재 + 원본 출처/일시 기록
- [ ] 2_WORK-SPEC.html의 Phase 1~4 항목이 6_SPEC.html와 일치
- [ ] 3_FEATURE-CHECKLIST.html 항목이 6_SPEC.html의 액션과 1:1 대응
- [ ] 5_ARCHITECTURE.html에 인라인 SVG 다이어그램(와이어프레임 포함) ≥ 1
- [ ] 6_SPEC.html에 (필드, 액션, API 초안) 모두 명시
- [ ] 각 산출 HTML 문서에 인라인 SVG 다이어그램 ≥ 1 (html-doc 시각화 필수 요건)
