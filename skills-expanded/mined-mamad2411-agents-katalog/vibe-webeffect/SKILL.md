---
name: vibe-webeffect
description: >
  사용자가 웹페이지·랜딩페이지·웹앱 UI를 만들거나 고칠 때, 작업 맥락을 읽고 어울리는
  웹 애니메이션 효과를 추천하고 코드까지 적용해주는 스킬. 72개 효과 카탈로그
  (스크롤 스크러빙 / 호버 / 시그니처 / 등장·리빌 / 마이크로 인터랙션 / 로딩·상태 / 실험실)
  기반. 다음 상황에서 반드시 이 스킬을 사용한다: 사용자가 "웹페이지 만들어줘",
  "랜딩페이지", "히어로 섹션", "포트폴리오 사이트", "대시보드 UI", "폼/버튼 만들어줘",
  "애니메이션 넣어줘", "효과 추천해줘", "더 살아있게/고급스럽게/화려하게 해줘",
  "밋밋한데?", "인터랙션 추가" 등을 언급할 때 — 애니메이션이라는 단어가 없어도
  HTML/CSS/JS UI를 새로 만들거나 개선하는 요청이면 트리거한다.
---

# vibe-webeffect — 웹 애니메이션 추천·적용 스킬

사용자의 UI 작업 요구를 읽고 → 카탈로그에서 어울리는 효과를 골라 → **정확한 이름(KR+EN)과 이유와 함께 추천**하고 → 동의하면 코드를 적용한다.
핵심 철학: **"용어가 곧 능력"** — 효과의 정확한 이름을 알려주는 것 자체가 사용자의 자산이 된다.

## 파일 구성
- `catalog.json` — 72개 효과. `{id, cat, kr, en, intensity, tags, prereq, code, ref}` 스키마
- `references/recipes.md` — 카테고리별 공용 구현 패턴(보일러플레이트). **코드 적용 전 반드시 읽는다**

---

## 워크플로우

### 1단계 — UI 컨텍스트 추출
사용자 요청에서 만들려는 화면의 구성요소를 파악한다. 명시가 없으면 요청의 성격에서 추론한다.

| 감지된 컨텍스트 | 매칭 태그 | 우선 카테고리 |
|---|---|---|
| 히어로/랜딩 첫 화면 | hero, landing | signature, scroll, insane(1개만) |
| 콘텐츠 섹션/블로그/소개 | section, content | **reveal** (기본값) |
| 카드 그리드/갤러리/포트폴리오 | grid, gallery, card, portfolio | reveal(stagger) + hover |
| 통계/수치/성과 | stats, number | reveal(count-up), signature(number-roll) |
| 폼/로그인/설정 | form, input, settings | **micro** + loading(error-shake) |
| 버튼/CTA | button, cta | micro, hover |
| 데이터 로딩/API 호출 화면 | loading, wait, feed | **loading** (필수) |
| 챗/AI 인터페이스 | chat, ai | loading(typing), micro |
| 제품 상세/이커머스 | product, ecommerce | hover, scroll(before-after), micro(star) |
| 스토리텔링/브랜드 사이트 | storytelling, brand, wow | scroll, signature, insane |
| 타임라인/프로세스/연혁 | timeline, process | reveal(line-draw, alternate-slide) |
| 배경이 밋밋함 | background, ambient | insane(constellation 등), signature(blob) |

### 2단계 — 카탈로그 매칭
`catalog.json`을 읽고 태그가 겹치는 효과를 후보로 모은다. 동률이면 intensity가 낮은 쪽을 우선한다(과잉 방지).

### 3단계 — 추천 제시 (적용 전에 반드시)
상황별로 **2~4개**를 골라 아래 형식으로 제시하고 사용자의 선택을 받는다:

> **[한국어 이름] ([영어 이름])** — 왜 이 화면에 맞는지 한 줄 + 필요한 전제조건(있으면)

단, 사용자가 "알아서 해줘/바로 적용해줘"라고 했거나 이미 효과를 지정했다면 추천 단계를 건너뛰고 적용한다. 이때도 적용한 효과의 이름은 반드시 결과 보고에 명시한다.

### 4단계 — 적용
1. `references/recipes.md`에서 해당 카테고리의 공용 패턴을 읽는다
2. catalog의 `code`(핵심)와 recipes의 보일러플레이트를 조합해 사용자 프로젝트 구조에 맞게 삽입한다
3. 아래 **적용 규칙**을 지킨다

### 5단계 — 결과 보고
적용한 효과의 이름(KR+EN)을 명시하고, 사용자가 나중에 AI에게 재요청할 수 있는 한 줄 지시문("~효과 넣어줘")을 함께 알려준다.

---

## 적용 규칙 (위반 금지)

1. **강도 배합** — 한 화면(뷰포트)에 `bold`는 최대 1개. 나머지는 subtle/medium. 전 화면이 다 움직이면 아무것도 안 보인다.
2. **reduced-motion 필수** — 모든 애니메이션에 `@media(prefers-reduced-motion:reduce)` 가드 또는 JS `matchMedia` 체크를 넣는다.
3. **성능** — transform·opacity만 애니메이션하는 것을 기본으로 한다. `filter`·`box-shadow` 애니메이션은 작은 요소에만. 스크롤 핸들러엔 lerp/rAF, 리스너엔 `{passive:true}`.
4. **transition 재생 함정** — transition 기반 효과를 재트리거할 땐 recipes.md의 "스냅 리셋" 패턴을 쓴다 (클래스 뗐다 바로 붙이면 재생 안 됨).
5. **등장 효과는 IntersectionObserver 1개로 통합** — 요소마다 옵저버를 만들지 않는다.
6. **로딩 UX 원칙** — 진행률을 알면 확정 프로그레스(+% 숫자), 모르면 무한/스피너, 구조를 알면 스켈레톤. 1초 미만 작업엔 로딩 표시 생략.
7. **의존성 0** — 모든 효과는 라이브러리 없이 순수 HTML/CSS/JS로 적용한다. 사용자가 GSAP 등을 이미 쓰고 있을 때만 그 방식을 따른다.
8. **마이크로 인터랙션 공용 이징** — `cubic-bezier(.34,1.56,.64,1)` (오버슈트 스프링).

## 추천 어조
- 이름을 가르치듯: "이건 **라인 마스크 리빌(line mask reveal)**이라고 하는데…"
- 과잉을 말리는 것도 추천이다: "여긴 효과 없이 두는 게 낫다"가 정답인 화면이 있다.
- 전제조건(예: 이미지 시퀀스는 ffmpeg 프레임 추출 필요)은 추천 시점에 미리 알린다.
