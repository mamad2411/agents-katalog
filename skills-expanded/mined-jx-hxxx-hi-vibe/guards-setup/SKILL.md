---
name: guards-setup
description: >-
  Machine-enforced quality guards installer. Use for /hi-vibe:gate
  or when the user asks to 린트 설정, 타입 체크 강제, 순환의존 검사,
  CI 세팅, eslint/ruff/mypy 설정, complexity limit. Detects project
  language(s) and installs lint/type/cycle guards and optional CI —
  always asking before writing, always merging with existing configs.
user-invocable: false   # 사용자 표면은 /hi-vibe:* 명령 10개다. 스킬까지 슬래시 메뉴에 나오면 16개가 되어 "외울 게 적다"는 약속이 깨진다. Claude의 자동 호출은 그대로 유지된다.
---

# guards-setup

> **답변 언어**: 이 지침은 한국어로 쓰였지만, **출력은 항상 사용자가 대화에서 쓰는 언어**를 따른다 (한국어→한국어, 영어→영어). 기존 문서·코드에 언어가 있으면 그쪽을 우선한다.

텍스트 규칙은 잊히지만 기계 게이트는 잊히지 않는다. 이 스킬은 규율의
절반을 린트/CI로 내려보낸다. 스니펫은 이 스킬의 `templates/`에 있다.

## 절차 (순서 엄수)

1. **감지**: `pyproject.toml`/`requirements*.txt`/`*.py` → Python;
   `package.json`/`tsconfig.json` → JS/TS; 둘 다면 둘 다.
2. **기존 설정 읽기**: ruff/mypy/eslint/import-linter 설정이 이미
   있으면 먼저 읽는다. 절대 덮어쓰지 않는다.
   **이미 같은 일을 하는 도구가 있으면 그 항목을 아예 빼고 제안한다.**
   타입 검사는 `mypy` 말고도 `basedpyright`·`pyright`가 흔하다
   (`pyproject.toml`의 `[tool.basedpyright]`/`[tool.pyright]`,
   `pyrightconfig.json`, `package.json`의 pyright 스크립트). 있으면
   mypy를 권하지 마라 — 타입체커 둘을 돌리면 서로 다른 소리를 한다.
   비밀키도 `gitleaks`·`detect-secrets` 설정이 있으면 마찬가지다.
   **겹치는 걸 또 깔아주는 건 도움이 아니라 짐이다.**
3. **묻기 (AskUserQuestion, 필수)**: 설치할 가드를 multiSelect로 고르게
   한다. 사용자는 대개 입문자다 — 아래를 지켜라.
   - **쉬운 말로.** 전문용어(complexity·max-depth·dpdm·exit 1·no-any·
     OAuth 등)를 앞세우지 말고, "이게 나한테 뭘 해주는지"를 한 줄로 먼저
     쓴다. 정확한 규칙값은 괄호로 뒤에 짧게. 예: "코드가 너무 길고
     복잡해지면 빨간불로 알려줘요 (함수 60줄·복잡도 10 넘으면)".
   - **추천 표시.** 로컬에서 외부 설정 없이 바로 되는 가드(복잡도 린트 +
     순환 의존 검사)를 **맨 앞에 두고 label에 "(추천)"**을 붙인다. 입문자
     기본값은 이 둘이면 충분하다 — GitHub도 토큰도 필요 없는 순수 이득.
   - **CI 가드**는 **GitHub 리모트(`git remote`)가 있을 때만** 추천으로
     올린다 — "GitHub에 올릴 때마다 자동 검문, 통과 못 하면 못 올려요
     (초반엔 답답할 수 있어요)". 리모트가 없으면 목록에서 빼거나 "나중에"로.
   - **격주 구조 감사**는 label에 "(고급)"을 붙이고, **켜기 전에 OAuth
     토큰 등록·Actions 권한 설정이 필요**하다고 설명에 미리 밝힌다. 처음이면
     나중에 해도 된다고 안내.
   - **"다 켜라"고 밀지 마라.** 4개 전부 체크된 기본값처럼 몰아가지 말고,
     입문자에겐 로컬 2종을 권하고 나머지는 필요해지면 그때 켜라고 말한다.
   - **플래그로 켜게 하지 마라.** CI를 목록에 넣을지는 `git remote`로
     직접 확인해 정한다 — 사용자가 `--ci`를 외워서 쳐야 보이면, 모르는
     사람은 영영 못 켠다. 리모트가 없으면 목록에서 빼고 **왜 뺐는지 한 줄**
     ("GitHub에 안 올리는 프로젝트라 CI는 돌 자리가 없어요"). 안 도는
     워크플로 파일은 보호받는다는 착각만 준다.
4. **병합**: 스니펫의 키를 기존 설정에 정중히 병합. 사용자가 이미
   정한 값(예: 기존 max-complexity)은 유지하고 차이만 보고.
5. **실측 검증 (grounded-answers 계약)**: 설치 후 도구를 실제로 한 번
   실행해 실제 출력을 보여준다. "될 겁니다"가 아니라 실행 결과로 보고.

6. **위반이 쏟아지면 — 하나씩 묻지 마라.** 이미 다 만든 프로젝트에 켜면
   위반이 수백 개 나오는 게 정상이다. 그걸 하나하나 "의도한 거예요?"라고
   물으면 수백 번 묻는 것이고, 사용자도 코드를 다시 열어보기 전엔 답할 수
   없다. **묻는 횟수 자체가 이 기능의 성패**다.

   순서는 이렇다:

   1. **묻기 전에 센다.** `ruff check --statistics`, `npx eslint -f json` 등으로
      **종류별 개수**를 낸다. 187개가 "함수 길이 120 · 복잡도 50 · 타입 15 ·
      순환 2" 네 줄로 줄어든다.
   2. **질문은 한 번.** "지금 켜면 187개가 뜹니다. 기존 코드 것은 덮어두고
      **새로 쓰는 코드부터** 볼까요?"
   3. **덮는다** (사용자가 동의하면):
      - **JS/TS**: `npx eslint --suppress-all` → 지금 있는 위반을
        `eslint-suppressions.json`에 한 번에 기록한다. **소스는 안 건드린다.**
        이후 목록에 없는 새 위반만 실패하고, 나중에 고치면
        `--prune-suppressions`로 정리한다. 이 파일은 커밋한다.
      - **Python**: `--add-noqa`는 **쓰지 마라** — 소스 수백 군데에 `# noqa`를
        박아 넣고, 이유 없이 꺼둔 것이 영구히 남는다. 대신 ruff 설정의
        `per-file-ignores`에 **기존 경로만** 예외로 잡고 새 코드에는 그대로
        적용한다.
   4. **개별 판단은 미룬다.** 기존 위반이 의도였는지 실수였는지는 **그 코드를
      실제로 건드릴 때** 판단하면 된다 — 그 순간엔 이미 `review`가 자동으로
      돌고 fresh-eyes가 붙는다. 안 건드릴 코드는 영영 판단하지 않아도 된다.
   5. **순환 의존만 예외로 지금 본다.** 대개 2~3개뿐이고, 덮어두면 계속
      악화되는 종류다.

   **임계값은 절대 낮추지 않는다.** 60줄이 걸리적거린다고 100줄로 올리는 것과,
   한 군데를 이유와 함께 예외 처리하는 것은 다르다 (전자는 root-cause-first 위반).

## 가드 목록

**Python** (`templates/ruff-snippet.toml`, `mypy-snippet.toml`,
`importlinter-snippet.toml`):
- ruff: C901 복잡도 ≤10, PLR0913 인자 수, E/F 기본
- mypy: strict (입문자 프로젝트면 단계 적용 제안). **`basedpyright`·`pyright`가
  이미 있으면 이 항목은 목록에서 뺀다** — 이유를 한 줄로 밝히고 넘어간다.
- import-linter: 레이어 계약 — **실제 디렉터리와 import 관계를 보고**
  레이어 초안을 만들어 사용자와 확인한다(CLAUDE.md에 폴더 목록을 두지
  않으므로 거기서 읽지 않는다). 순환·경계 위반 시 실패.

**JS/TS** (`templates/eslint-snippet.jsonc`,
`package-scripts-snippet.json`):
- eslint: complexity 10, max-depth 3, max-lines-per-function 60,
  max-params 4
- dpdm: `npm run check:cycles` — 순환 의존 발견 시 exit 1
- TS면 tsconfig `strict: true` 확인, `as any` 금지 규칙

**CI** (`templates/github-actions-vibe-guards.yml`):
- push/PR마다 위 가드 전부 실행. 순환·경계 위반 = 빌드 실패 (d-2).
- **기존 워크플로의 의존성 설치 명령을 먼저 읽고 맞춰라.** `.github/workflows/`
  의 다른 파일이 `npm install`을 쓰고 있으면 여기도 `npm install`로 바꾼다.
  `npm ci`는 lock이 정확할 때만 통과하는데, 플랫폼별 optional 의존성(wasm
  패키지가 끌어오는 `@emnapi/*` 등)은 맥에서 만든 lock에 안 들어가 리눅스
  러너에서 거부된다. 배포 워크플로만 `npm install`이고 가드만 `npm ci`여서
  **나흘간 CI가 죽어 있던 실사례**가 있다.
- **깔고 끝내지 마라.** 설치 후 사용자에게 이렇게 안내한다: "푸시하고
  `gh run list --workflow vibe-guards --limit 3`로 실제 통과를 한 번
  확인하세요." 첫 실행이 깨진 채로 방치되면 관문은 세운 적 없는 것과 같다.
- 세워둔 관문이 나중에 죽는 것은 SessionStart 훅이 잡는다 — 현재 브랜치의
  CI가 연속 실패 중이면 세션 첫머리에 알린다(gh CLI 있을 때만, 20분 캐시).
  **깨진 CI는 "빨간불"이 아니라 검사가 아예 안 도는 상태**라서, 모르고
  며칠 더 밀어넣는 것이 진짜 손해다.

**정기 감사** (`templates/github-actions-biweekly-audit.yml`):
- 격주 cron. 직전 `audit/*` 태그 이후 코드 변경(문서 제외)이 없으면
  스킵. 변경이 있으면 CI에서 Claude Code가 repo-xray 스캔 + 구조
  리뷰 체크리스트를 돌려 보고서를 만들고 GitHub 이슈로 게시.
- 설치 시 안내할 것: ① `claude setup-token`으로 구독 OAuth 토큰 발급
  → 저장소 Settings > Secrets에 `CLAUDE_CODE_OAUTH_TOKEN` 등록
  ② Settings > Actions > Workflow permissions를 "Read and write"로.

## unused/dead 정리 주의 (미완성 코드 보호)

린트는 기본적으로 **검사만** 한다 — 코드를 자동으로 지우지 않는다. `--fix`
자동 수정도 보통 안 쓰는 import·지역 변수 수준이지, 함수 정의를 지우지
않는다. 그래도 lint의 unused나 audit의 dead 결과를 보고 코드를 **정리·삭제
하려 할 때는**, 먼저 그게 **미완성(WIP)** 코드인지 확인한다 — `pass`/`...`/
`NotImplementedError`/빈 본문/TODO·FIXME 주석. 미완성이면 "안 쓰는 것"이
아니라 "아직 안 만든 것"이므로 **지우지 말고 사용자에게 물어라**. 삭제는
언제나 사용자 확인 후 (repo-xray `looks_wip` 플래그·FP-07 참고).

## Red Flags

- 사용자 확인 없이 설정 파일을 쓰는 것
- 기존 설정 값을 스니펫 값으로 덮는 것
- 도구를 실행해보지 않고 "설정 완료"라고 보고하는 것
- 위반이 많다고 임계값을 올려서 통과시키는 것 (root-cause-first 위반)
- lint unused / audit dead를 보고 **미완성 코드를 확인 없이 지우는 것**
