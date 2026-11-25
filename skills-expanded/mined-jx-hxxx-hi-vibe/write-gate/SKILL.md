---
name: write-gate
description: >-
  Use before creating or refactoring functions, helpers, types, components,
  or files, and after finishing code changes that need review. Triggers on
  만들어줘, 추가해줘, 구현해줘, 새 파일, 리팩토링, 다 했어, 리뷰해줘,
  검토, and review my change.
user-invocable: false
---

# write-gate

출력은 사용자의 대화 언어를 따른다. 이 파일에는 모든 모드가 함께 쓰는 판단과
분기만 둔다. 긴 체크리스트·사례·보고 형식은 필요한 모드에서만 references를 읽는다.

## 세션당 한 번: 훅 생존 확인

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/doctor.py" --root <repo> --quick`

- `alive`·`optout`: 말하지 않고 진행한다.
- `stale`·`never-ran`: 훅이 돌지 않았다고 한 줄 알리고 작업은 계속한다.
- `not-initialized`: 자동 감지·기록을 쓰려면 `/hi-vibe:init`이라고 한 번만
  알린다. 마음대로 init하지 않는다. 사용자가 쓰지 않겠다고 하면
  `.hi-vibe/optout`을 만든다.
- `tracked_env`가 있으면 파일명만 알린다. 파일 내용은 열지 않는다. 이미
  push했다면 키 폐기가 필요하다고 말한다.
- 조회가 실패해도 작업을 막지 않는다(fail-open).

## Mode: find (코드 작성 전)

1. 새 이름 후보 2~3개를 repo-xray로 검색하고 스캔 범위를 확인한다.
   `python3 "${CLAUDE_PLUGIN_ROOT}/skills/repo-xray/scripts/audit.py" find <name> --root <repo>`
2. 외부 API·라이브러리의 버전 민감한 동작은 공식 문서로 확인한다. 확인할 수
   없으면 추정이라고 밝힌다. 프로젝트 내부 코드만 다루면 생략한다.
3. 대상 폴더의 `MODULE.md`가 있으면 책임과 경계를 확인한다.
4. 공용 유틸·타입·shape은 기존 SSOT를 재사용하고 로컬 복사본을 만들지 않는다.
5. 판정은 **재사용 / 확장 / 신규** 중 하나로, 신규라면 검색 범위를 근거로 남긴다.

요청 밖 문제를 발견하면 한 줄로 보고하고 사용자가 정하게 한다. 요청 자체를
완료하는 데 필수인 수정만 이유를 밝히고 함께 처리한다.

## Mode: review (코드 작성 후)

리뷰를 시작하면 반드시
`references/review-checklist.md`를 읽고 그 절차를 끝까지 따른다. 핵심 순서는:

1. `review_scope.py list`로 리뷰 범위를 기계적으로 구한다.
2. 기본은 순차로 본다. 아주 큰 변경(파일 15개+ / 1,500줄+)일 때만 둘로 나눈다.
3. 체크리스트에서 결함을 찾으면 요구사항 안의 결함만 고쳐 재검사한다.
4. 실행 검증과 문서 동기화를 마친 뒤 `review_scope.py mark`로 완료를 표시한다.
5. 결과는 결함과 검증 근거 중심으로 짧게 보고한다.

**`fresh-eyes`를 부르는 자리는 둘뿐이다** (`references/review-checklist.md` 4번):

- **커밋 게이트가 막았을 때** — 사유에 온 파일 목록으로 소환하고, 지적을 고친
  뒤 커밋을 재시도한다. 자동 경로는 이것뿐이다.
- **사용자가 직접 요청했을 때** — `/hi-vibe:review`, "설계 검토해줘", "남의
  눈으로 봐줘". 명시 요청이 예산보다 우선한다.

훅이 턴 끝에 세운 리뷰(Stop 차단)에서는 **부르지 않는다.** 턴마다 부르면
리뷰가 고친 것이 또 리뷰를 부르는 고리가 된다.

사용자가 “가볍게 봐줘” 또는 “keep it light”라고 하면 분할 없이 체크리스트만
적용한다. 생략 사실은 한 줄로 밝힌다.

## 정량 성과가 나온 경우

리뷰·테스트·벤치마크 결과에 변경 전후 수치, 백분율, 정확도, 처리량, 지연 시간
같은 **정량 주장**이 있을 때만 `references/metrics-evidence.md`를 읽는다.
그 조건을 만족하면 docs-keeper의 evidence 모드로 근거를 기록하고 CHANGELOG에서
연결한다. 숫자가 없거나 비교 조건이 다르면 이 참조를 읽거나 수치를 만들지 않는다.

## 공통 완료 계약

- 실제로 실행한 검증만 말한다. 못 했으면 이유와 함께 “실행 검증 안 됨”이라고 쓴다.
- 구조·제약·실질 동작 변화는 docs-keeper 규칙에 맞춰 같은 턴에 기록한다.
- 사용자가 그냥 지나쳤을 진짜 결함을 hi-vibe가 새로 찾아낸 경우에만
  `👋 hi-vibe가 방금 <무엇>을 잡아서 고쳤어요 — <스킬/에이전트>.`를 붙인다.
  통과, 취향, 사용자가 이미 발견한 문제에는 붙이지 않는다.
