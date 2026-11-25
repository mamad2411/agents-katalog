---
name: add-skill
description: suta 저장소에서 진입 스킬 suta에 UI 패턴(애니메이션·UI·UX)을 추가하거나 기존 패턴을 수정·재검증하는 파이프라인(선택 평가 → 패턴 문서 → 데모 → 카탈로그 → 게이트). "패턴 추가해줘, 스킬 추가해줘, {패턴} 패턴으로 등록해줘, 데모 다시, 재검증, 리뷰 다시" 요청에 쓴다. 패턴 내용에 대한 단순 질문에는 쓰지 않는다.
metadata:
  internal: true
---

# add-skill — 패턴 추가 파이프라인

이 저장소의 반복 작업이다. 작업 전 `docs/harness-rules.md`를 읽는다. 설계 단일 출처는 `docs/design/2026-08-19-fe-skills.md`다.

이 스킬은 저장소 관리용이다. frontmatter의 `metadata.internal: true`는 `npx skills add`가 일반 사용자에게 이 스킬을 설치 후보로 보여 주지 않게 한다. 사용자가 설치하는 것은 진입 스킬 `skills/suta` 하나다.

## 불변 구조 — 왜 이 모양인가

```
skills/suta/
├─ SKILL.md                      # 진입 스킬 — UI 요청에 자동으로 걸린다. 패턴 색인은 생성 블록
├─ references/catalog.md         # 패턴 카탈로그(한 줄 설명) — 생성 블록
└─ patterns/{pattern-name}/
   ├─ PATTERN.md                 # 정본: 언제 쓰는가·사용 방법·핵심 패턴 (SKILL.md가 아니다)
   ├─ references/                # 상세(변형·엣지 케이스·접근성) — 필요할 때만 로드
   └─ assets/                    # 예시 컴포넌트 코드 (정본의 일부, 실행 가능한 파일)
demo/src/demos/{pattern-name}/   # assets/를 import해 렌더링하는 데모 페이지
```

- **패턴 문서는 `PATTERN.md`다.** `SKILL.md`로 만들면 도구가 패턴마다 별도 스킬로 등록해, 스킬 목록 예산을 넘기고 진입 스킬과 경쟁한다. 검사 스크립트가 `skills/` 아래 SKILL.md가 하나뿐인지 본다.
- **assets/의 코드가 유일한 구현본이다.** 데모는 그 파일을 import만 한다 — 복사본을 만들면 한쪽만 고치는 순간 문서가 거짓말이 된다.
- **패턴 문서는 설치된 프로젝트에서 단독으로 완결되어야 한다.** PATTERN.md는 사용 방법과 핵심 패턴을 담고, 전체 구현은 "assets/{파일}을 읽어라"로 가리킨다. demo/ 경로는 참조하지 않는다(설치 시 존재하지 않는다).

## 절차

### 0. 착수 확인

- 브랜치 확인(`branch` 스킬) — 작업은 `feat/{pattern-name}`에서.
- `skills/suta/patterns/`에 같은/유사 패턴이 이미 있는지 확인 — 있으면 신규가 아니라 확장이다.

### 1. 선택 평가 → 패턴 문서 (정본 먼저)

0. `evals/selection/{pattern-name}.json`을 **먼저** 쓴다(Red): `should` — 이 패턴이 골라져야 하는 요청 3개 이상(구어체 1개·영어 표현 1개 포함), `shouldNot` — 이웃 패턴의 요청 3개 이상(골라지면 안 됨). `node scripts/evalSelection.mjs {pattern-name}`이 실패하는 것을 확인한 뒤 description을 쓴다(Green).
1. `skills/suta/patterns/{pattern-name}/PATTERN.md` 작성:
   - frontmatter `name`(폴더명과 일치)·`description` — 3인칭으로 "무엇을 하는가 + 언제 쓰는가"만. 80~300자(150~250자 권장). **첫 문장이 진입 스킬 카탈로그의 한 줄 요약이 된다** — "무엇을 구현한다."로 짧게 끝낸다. 사용자가 실제로 쓸 표현을 따옴표로 나열하고 핵심 영어 용어를 한 번 넣는다. 구현 방식 요약·에이전트 명령문 금지.
   - 본문: **언제 이 패턴을 쓰는가 → 사용 방법(설치·적용 단계) → 사용 예시(최소 코드) → 커스터마이즈 포인트(duration·easing 등) → 주의사항(접근성·성능)**. 명령형, ≤500줄.
2. `assets/`에 예시 컴포넌트 작성. 기술 기준: **CSS 우선** — CSS transition/animation으로 되는 것은 CSS로, 어려운 것(제스처·레이아웃 전이)만 TypeScript로 쓰고 PATTERN.md에 "왜 이 기술인가" 한 줄을 명시한다.
3. 접근성은 선택이 아니다: `prefers-reduced-motion` 대응을 모든 패턴에 포함한다.
4. 코드 컨벤션: 화살표 함수, useCallback/useMemo 지양, 인자 2개 이상이면 named-object, useEffect는 명명된 함수로.
5. 다른 패턴의 코드가 필요하면 import하지 않고 파일을 복사하되, 첫 줄의 `@shared-core {파일} origin: {패턴}` 헤더를 유지한다.

### 2. 데모 구현

1. `demo/src/demos/{pattern-name}/`에 데모 페이지 작성 — `@skills` alias(= `skills/suta/patterns`)로 assets/ 컴포넌트를 import해 렌더링한다.
2. `demo/src/demos/index.ts`의 데모 레지스트리에 등록한다(라우팅·목록·카탈로그 카테고리는 레지스트리가 단일 출처). `title`·`description`과 영어 `titleEn`·`descriptionEn` 모두.
3. 데모는 쇼케이스다: 트리거 버튼·리플레이 등 확인 장치는 데모 쪽에 두고, assets/ 컴포넌트를 데모 편의를 위해 오염시키지 않는다.
4. **데모 콘텐츠는 suta 고유 브랜드(국수집 테마)로 쓴다** — 토스·당근·인스타그램 등 레퍼런스 앱의 실제 UI 문구·탭 이름·구성을 복제하지 않는다. 레퍼런스 언급은 PATTERN.md의 "언제 쓰는가"(관례 설명)까지만.
5. **데모 안 문구는 한국어·영어 두 벌이다.** 파일 위에 `const COPY = defineCopy({ ko: {...}, en: {...} })`(`demo/src/demoLang.ts`)를 두고 컴포넌트에서 `const t = COPY[useDemoLang()]`로 읽는다. 경로·가격·아이콘처럼 언어와 무관한 값은 COPY 밖에 둔다. 기준 예시는 `demo/src/demos/bottom-nav/BottomNavDemo.tsx`. 패턴이 화면 낭독 문구를 한국어로 박아 두었으면 데모에서 고치지 말고 패턴에 선택 prop(기본값 한국어)을 더한다. `npx vitest run src/tests/demoCopy.test.tsx -t {패턴}`이 영어 화면에 한글이 남았는지 본다.
6. 로직이 있는 부분(상태 전이·옵저버·제스처)은 테스트를 먼저 쓴다(Red→Green). 순수 시각 효과에 빈 테스트를 양산하지 않는다.

### 3. 카탈로그·문서

1. `npm run catalog` — 진입 스킬 `skills/suta/SKILL.md`의 패턴 색인 블록과 `skills/suta/references/catalog.md`의 카탈로그 블록을 다시 만든다. 손으로 고치지 않는다(검사 스크립트가 동기 여부를 본다). 색인에는 데모 레지스트리의 `title`이 실린다.
2. 상세 안내 `docs/guide.md`와 `docs/guide.en.md`의 패턴 표에 한 행씩 더하고, `README.md`·`README.ko.md`의 배지 숫자(패턴 수·tests 수)를 갱신한다.
3. 화면 비교 — 수정이면 고치기 전·후 데모를 같은 폭으로 찍어 한 장(줄 머리 AS-IS·TO-BE)으로, 새 패턴이면 데모 캡처를 `docs/worklog/assets/{날짜}-{주제}.jpg`로 두고 워크로그에 싣는다(`AGENTS.md` 규칙 12).

### 4. 게이트 검증 — 전부 통과해야 완료

| # | 게이트 | 명령/방법 |
|---|--------|----------|
| 1 | 빌드·린트·테스트 | `npm run build && npm run lint && npm test` |
| 2 | 구조·선택 평가 | `npm run validate` — 진입 스킬·패턴 구조, 카탈로그·매니페스트 동기, 배지, 선택 평가(트리거 + 패턴), 레이아웃·모션 통합 검사(error 0) |
| 3 | 브라우저 실동작 | 데모 페이지를 브라우저로 열어 스크린샷/녹화로 실제 동작 확인 |
| 4 | 모션 리뷰 | `fe-craft` 스킬로 이징·타이밍·reduced-motion 리뷰, 지적 반영 |

### 5. 종료

- 워크로그 기록(`docs` 스킬, `docs/templates/worklog.md` 형식).
- 커밋·PR은 사용자가 명시 요청한 경우에만 `pr` 스킬로(PR 베이스 main). 요청 없으면 "커밋은 직접 진행하세요"로 안내.
- 세션 중단·인계 시 `handoff` 스킬.

## 에러 핸들링

- 게이트 실패 → 수정 후 해당 게이트부터 재실행(전체 재시작 불필요).
- 모션 리뷰에서 설계 문서와 충돌하는 지적 → 임의 판단하지 말고 사용자 확인 후 설계 문서 먼저 갱신.
