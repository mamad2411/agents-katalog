---
name: discussion
description: design-to-ui·design-qa로 작업하다 **세션 중 gotcha/이슈가 나왔을 때** 그 경험을 우리 플러그인 레포(naver/design-to-ui)의 GitHub Discussions에 카테고리 분류로 기록한다 — 초기 결과가 안 맞아 추가 프롬프트/SKILL 수정으로 해결한 gotcha, design-qa가 찾은 오차, 기능 아이디어, 도입 사례. `/discussion` 호출로 진입. 세션을 자동 요약해 카테고리를 제안하고 반드시 사용자 확인 후 등록한다. Trigger phrases - /discussion, design-to-ui·design-qa gotcha/노하우/도입사례 공유·제보
license: Apache-2.0
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
metadata:
  author: NAVER
  version: "1.0"
---

# discussion — 사용 경험을 Discussions로 축적

design-to-ui·design-qa로 작업하다 **세션 중 나온 것**(막힘→해결 gotcha · design-qa 오차 · 아이디어 · 문의 · 도입 사례)을 `naver/design-to-ui`의 **GitHub Discussions**에 등록한다.

**진입은 사용자가 `/discussion`을 호출**한다. 자동 트리거(skill description)는 구조적으로 약하므로 명시 호출이 실질 진입점이다.

핵심 목적은 **gotcha 축적의 선순환**이다 — "이 화면이 처음엔 안 맞았는데, 이런
추가 프롬프트로 해결했다"는 경험이 쌓일수록 스킬이 점점 정확해진다. 그래서 이
스킬은 단순 코멘트가 아니라 **세션에서 UI 일치도를 올린 과정**을 자동으로 캡처한다.

> Discussions 등록은 외부에 보이는 행위다. **반드시 초안을 보여주고 사용자 확인을
> 받은 뒤에만** 등록한다(Step 4). 임의 등록 금지.

## 카테고리 (등록 대상)

런타임에 `discussionCategories`를 조회해 이름으로 매칭한다(ID 하드코딩 금지 — 바뀔 수 있음).

**이 레포는 카테고리별 폼(`.github/DISCUSSION_TEMPLATE/*.yml`)을 쓴다.** 폼이 있는 카테고리는 **반드시 그 폼 필드에 맞춰 본문을 구성**한다 — 그래야 웹 폼으로 등록된 글과 구조가 일치한다(Step 3·4). 폼은 API(`createDiscussion`)에서 강제되지 않으므로, 스킬이 직접 폼을 읽어 따라야 한다.

| 카테고리 | 폼 파일 | 언제 |
|----------|---------|------|
| **Gotcha** | `gotcha.yml` | (개선 시도한 경우만) 상황+문제+시도해본 것+반영 희망. **추가 프롬프트/SKILL 수정으로 막힌 걸 푼 경험의 기본 목적지.** |
| **Ideas** | `ideas.yml` | 기능 제안·개선 아이디어 |
| **Q&A** | `q-a.yml` | 사용·확장 문의 |
| **Show & Tell** | `show-tell.yml` | 자유 공유 — 이런 점이 좋았다/아쉬웠다 |
| **플러그인/선디자인검수 워크플로우 도입** | (폼 없음 · 자유형식) | 도입 사례 공유 |

> **공지** 카테고리는 maintainer 전용이므로 여기로 등록하지 않는다.
> 폼 슬러그는 카테고리명을 소문자화 + 공백→`-` + `&`제거 (Q&A→`q-a`, Show & Tell→`show-tell`). **폼 유무·필드는 하드코딩하지 말고 런타임 조회로 확정**한다(위 표는 참고용, 폼이 추가/변경될 수 있음).

## Steps

### Step 1: 의도·코멘트 파악

`/discussion <코멘트>`면 코멘트를 그대로 쓴다. 코멘트가 없으면 묻는다:

> "어떤 걸 공유/제보할까요? (막혔다 해결한 경험, 아이디어, 문의, 도입 사례 등)"

### Step 2: 정보 수집 (이 스킬의 핵심 — 3개 출처, 날조 금지)

**컨텍스트만 믿지 말 것.** 제보만 하러 온 얕은 세션, 길어서 compaction된 세션, 작업이 다른 세션·서브에이전트에서 이뤄진 경우엔 대화 컨텍스트에 정보가 거의 없다. 그래서 아래 **3개 출처를 순서대로** 써서 채운다:

1. **대화 컨텍스트** — 이번 세션에서 한 변환/검증 내역.
2. **디스크 근거 (컨텍스트가 얕으면 반드시)** — 최근 작업을 실제 파일에서 복원:
   - `git status` / `git diff` 로 최근 수정된 UI 파일(Compose/XML/Swift/`res/`)과 변경 내용
   - design-qa 산출물이 있으면 읽는다: `OVERLAY-REPORT.md` · `metrics.json` · `ledger.json` · `blend50.png`/`cmp_*`
   - 대상 화면 소스 파일 직접 확인
3. **사용자 인터뷰 (그래도 부족하면)** — 근거로 못 채우는 항목, 특히 **폼 필수 필드**(상황·문제·시도해본 것)는 **추측하지 말고 구체적으로 질문**해서 채운다.
   > 예: "어떤 화면/컴포넌트였나요? 처음엔 뭐가 안 맞았죠? 어떤 추가 프롬프트나 수정으로 해결하셨어요?"

> **날조 금지.** 빈 필드를 그럴듯한 문장으로 메우지 않는다 — 컨텍스트·디스크 근거·사용자 답변 **셋 중 하나에 실제로 있는 것만** 적는다. 근거가 없으면 비워두지 말고 **질문**한다.

채울 정보(폼 필드·자유형식 공통). **개선 여정이 핵심**:

- **요청**: Figma URL·node-id, 플랫폼/프레임워크, 화면 이름
- **결과**: 생성/수정 파일, 주요 결정(에셋 A/B/C·토큰 매핑)
- **개선 여정** (gotcha 핵심): 처음 안 맞은 점 → 추가 프롬프트/막힘(끙끙) → 최종 해결책 (예: SVG Read로 stroke-width 확인 · design-qa 오버레이 8px 밀림→선언값 교체)
- **design-qa**면: probe/오버레이가 잡은 오차·보정

**Gotcha 게이트 (엄격):** (1) 구체적 문제 + (2) 인세션에서 실제로 개선을 시도한 흔적(추가 프롬프트/SKILL 수정), **둘 다 있을 때만 Gotcha**로 제안한다. 문제만 있고 해결 시도가 없으면 gotcha.yml 규칙대로 **Ideas / Show & Tell / Q&A**로 보낸다. 3화면×3회 검증까지 됐으면 이상적이지만 1회성 해결도 유효하다 — 단 '시도해본 것'에 **검증 범위를 정직하게** 적는다(3×3 안 했으면 안 했다고).

### Step 3: 카테고리 분류 + 폼 확인 + 제목

1. 내용으로 카테고리를 1개 자동 제안한다(위 표 기준).
2. **그 카테고리의 폼을 런타임에 조회한다** (레포 `.github`에서):
   ```bash
   gh api \
     "repos/naver/design-to-ui/contents/.github/DISCUSSION_TEMPLATE/<slug>.yml" \
     --jq .content 2>/dev/null | base64 -d    # 404면 폼 없음 → 자유형식으로
   ```
   폼이 있으면 `body:` 아래 각 필드(`label` / `type` / `validations.required`)를 파싱해 Step 4의 본문 골격으로 삼는다.
3. 제목: Gotcha `[Gotcha] <화면/증상> — <해결 요지>` · 도입 `[도입 사례 공유] <팀/프로젝트>`.

### Step 4: 본문 구성 (폼 준수) + 확인 게이트

**폼이 있으면 — 폼 필드 = 본문 구조.** 각 필드를 `### {label}` 섹션으로 만들고 Step 2 요약을 매핑해 채운다(웹 폼 제출 글과 동일 형태). `required: true` 필드는 반드시 채운다.

`gotcha.yml` 매핑 예:

| 폼 필드 | 채울 내용 |
|---------|-----------|
| 사용 모델 (dropdown) | 현재 실행 중인 모델에 가장 가까운 옵션 (예: Opus 4.x → `Opus 4`) |
| 상황 | 어떤 화면/컴포넌트를 변환하려 했나 (Figma URL·플랫폼) |
| 문제 | 처음 결과에서 무엇이 안 맞았나 |
| 시도해본 것 | 추가 프롬프트를 몇 번/어떻게 썼나, SKILL 수정 여부, 무엇이 해결책이었나 |
| 반영 희망 사항 | 스킬에 반영됐으면 하는 것 |
| PR 링크 | 있으면 |

> 렌더: 각 필드 `label`을 `###` 헤딩으로 두고 아래에 내용을 채운다(웹 폼 제출 글과 동일). ideas/q-a/show-tell도 동일 원칙 — 런타임에 읽은 필드 순서대로, 하드코딩 금지.

**폼이 없으면(도입 등)** — #121 형식(개요 / 생성 과정 / 결과 전문) 또는 아래 자유 템플릿:
~~~markdown
## {제목}
### 코멘트
> {사용자 코멘트}
### 세션 요약 / UI 일치도 개선 여정
- 안 맞았던 것 · 시도/막힘 · 해결책
~~~

**확인 게이트 (필수):** 완성한 본문(폼 형태 그대로)을 사용자에게 보여주고 확인받는다.
> "아래 내용으로 **{카테고리}**에 등록할게요. 폼 항목 채운 것 확인해주시고, 뺄 부분 있으면 말씀해주세요. 이대로 올릴까요?"
- 내부 경로·코드가 과하면 축약 제안(민감정보 최소화) · 카테고리 변경 반영 · **동의 전 등록 금지.**
- 폼 **필수 필드가 근거 없이 비어 있으면 등록하지 말고 Step 2의 인터뷰로 돌아가** 채운다.

### Step 5: Discussions 등록

`gh api graphql`로 `naver/design-to-ui`에 등록한다:
1. repository id와 대상 category id 조회(`discussionCategories`에서 이름 매칭).
2. `createDiscussion(input:{repositoryId, categoryId, title, body})` → 반환 `discussion{ id url }` (id는 Step 6 코멘트에 사용).

> 폼 `labels`(예: `gotcha.yml`의 `labels:["gotcha"]`)는 `createDiscussion`이 자동 부여하지 않는다 — 필요하면 등록 후 `addLabelsToLabelable`(선택, 실패해도 등록은 유효).

등록 후 `discussion.url`을 사용자에게 보여주고 감사 인사를 전한다.

### Step 6: Gotcha 핸드오프 코멘트 (Gotcha 등록 시에만 · 확인 후)

카테고리가 **Gotcha**로 등록됐다면, 이 gotcha를 **다른 Claude가 스킬 개선으로 이어받을 수 있는 핸드오프 문서**를 만들어 **같은 discussion에 추가 코멘트**로 단다. gotcha가 "제보"에 그치지 않고 "스킬 개선 PR"로 연결되게 하는 단계다. (Gotcha가 아니면 이 스텝은 건너뛴다.)

먼저 사용자에게 묻는다:
> "이 gotcha를 다른 Claude가 스킬 개선으로 이어갈 수 있게 **핸드오프 코멘트**도 달아둘까요?"

동의하면 **핸드오프 문서를 자유 형식으로** 작성해 보여주고(확인받은 뒤), 같은 discussion에 코멘트로 단다.

다른 Claude가 이 gotcha를 **스킬 개선 PR**로 이어갈 수 있게, 형식은 자유롭게 하되 최소한 이것들을 담는다:
- 대상 스킬(design-to-ui / design-qa / figma-diff-apply 등 — **어느 스킬 문제인지 먼저 판별**) · 재현 입력 · 현재(잘못된) 출력 · 통한 해결책 · 제안 변경(구체 문구) · 검증법(3화면×3회 또는 golden 픽스처)

등록: Step 5-2에서 반환된 **discussion id**에 `addDiscussionComment`(gh graphql)로 코멘트를 단다. 사용자가 거절하면 코멘트 없이 종료한다(discussion 본문은 그대로 유효).

## Error Handling

| 상황 | 동작 |
|------|------|
| `gh` 미인증 (`gh auth status` 실패) | `gh auth login` 안내 후 중단 |
| 카테고리 이름 매칭 실패 | 5-1의 카테고리 목록을 보여주고 사용자가 고르게 함 |
| `createDiscussion` 권한 오류 | 토큰 스코프(`repo` 또는 `write:discussion`) 확인 안내 |
| 사용자가 등록 거절 | 등록하지 않고 종료 (초안만 남김) |
| 핸드오프 코멘트 실패/거절 | discussion 본문은 유효 — 코멘트만 재시도 안내하거나 건너뜀 |

<!--
Design-To-UI
Copyright (c) 2026-present NAVER Corp.
Apache-2.0
-->
