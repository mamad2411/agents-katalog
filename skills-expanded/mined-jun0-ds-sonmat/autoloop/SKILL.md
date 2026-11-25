---
name: autoloop
description: '여러 파일을 고치거나 되풀이가 필요한 작업을 기획→정의→실행→평가→판단→기록 루프로 끝까지 돌리고, 사용자에게 올릴 지점을 판단한다. 사용자가 "끝까지 알아서 해", "루프 돌려", "자율로 진행해"라고 하거나 마일스톤 단위 구현을 맡길 때 쓴다. 파일 하나로 한 번에 끝나는 수정, 질문 답변, 조사만 하는 요청에는 쓰지 않는다.'
user-invocable: true
---

# Autoloop — 자율 루프 절차 (Autonomous Loop Protocol)

## 0. 진입 분기 (Entry Routing)

작업을 받으면 복잡도를 판단한다.

| 신호 | L0 (바로 실행) | 전체 루프 |
|--------|-------------|-----------|
| 고칠 파일 | 1개 | 여러 개 |
| 되풀이 필요 | 한 번에 끝남 | 되풀이할 것으로 예상됨 |

**L0**: 기획 질문과 정의를 건너뛴다. core.md와 hints.md를 적용한 뒤 실행하고 검증하면 끝난다. 발동 신호가 걸리면 전체 루프로 에스컬레이션한다.

**전체 루프**: 1절로 넘어간다.

**bridge note 확인**: 어떤 작업이든 시작하기 전에 sonmat bridge note가 있는지 확인한다. 위치는 `$SONMAT_PROJECTS_BASE/<slug>` 안의 `bridge-note.md`이고, 기본값은 `~/.sonmat/projects/<slug>/`이다. `<slug>`는 cwd 경로의 `/`를 `-`로 바꾼 값이다. 여기에 없으면 예전 위치인 `.claude/sonmat/`를 본다. 관련 맥락이 있으면 말없이 반영한다. 새 작업과 직접 관련될 때만 사용자에게 언급한다.


## 1. 기획 질문 (Planning Questions)

루프 정의가 없으면 대화로 만든다. 질문을 한꺼번에 다 하지 말고 두세 개씩 묻는다.

### 필수 질문 (Required Questions)

| # | 질문 | 채우는 항목 |
|---|----------|----------|
| 1 | 최종 목표는 무엇인가? | `loop.name` + 목표 |
| 2 | 어떤 파일이나 범위를 고치는가? | `loop.modify` |
| 3 | 고친 뒤 무엇을 실행하는가? | `loop.run` |
| 4 | 결과를 어떻게 평가하는가? | `loop.evaluate` |
| 5 | keep/discard/refine 기준은 무엇인가? | `loop.judge` |
| 6 | 제약은 무엇인가? (손대면 안 되는 파일, 시간, 보존 구역) | `loop.constraints` |
| 7 | 언제 멈추는가? | `loop.exit` |

### 건너뛰는 규칙 (Skip rules)
- 작업 설명에서 이미 답한 것은 묻지 않고 채운다.
- 맥락에서 분명히 짐작할 수 있는 것은 묻지 않고 채운다.
- 최소한 `modify`, `run`, `evaluate`는 확보한다.

### 확인 (Confirmation)
시작하기 전에 루프 정의 YAML을 보여 주고 사용자의 승인을 받는다.
L0 작업은 한 줄 요약으로 충분하다. "이렇게 진행할게요: [요약]. 아니면 말해 주세요."
L0 안내 뒤에 사용자가 아무 말이 없으면 원래 요청 범위 안에서 평소대로 실행해도 된다. 다만 그것으로 승인 기준선 묶음이 생기지는 않는다. 승인 기준선 묶음에는 사용자가 명시적으로 승인한 발화가 있어야 한다.

사용자가 승인하면 그때 보여 준 정의가 실행 기준선으로 고정된다. 보여 준 내용을 그대로, 승인 발화 원문과 함께 보존한다. 승인은 정의에서 빠진 기존 계약을 고치지 않는다. 새 근거가 나오면 그 기준선 안에서 구현 세부는 바꿀 수 있다. 그러나 새 근거 때문에 승인된 목표, `loop.modify`, `loop.constraints`, `loop.judge`가 바뀌거나 기준선이 명시적으로 없앤 동작을 되살려야 한다면, 현재 기준선과 수정안을 보여 주고 다시 승인받은 뒤에 수정안을 실행한다. 안전이나 개인정보와 부딪치면 실행을 멈추되, 대안을 사용자 대신 고르지 않는다.


## 2. 루프 절차 (Loop Protocol)

```
[Plan] → [Define] → [Execute] → [Evaluate] → [Judge] → [Record] → [Repeat/Exit]
```

### [Plan]
- 정의가 없으면 1절의 질문을 진행한다.
- 정의가 있으면 [Define]으로 넘어간다.
- 마일스톤 규모의 기획이면 L3로 에스컬레이션한다(아래 참조).

**브레인스토밍** (간단하지 않은 기획일 때):
처음 떠오른 방법을 그대로 채택하지 않는다. worker(§6a)에 브레인스토밍 프롬프트를 주어 위임한다. 제약, 우선순위, 트레이드오프를 달리한 변형 N개를 만들어 어느 것도 고르지 말고 목록으로 돌려달라고 한다. 메인 세션은 변형들을 서로 비교한 뒤 사용자에게 선택지로 보여 준다. 이것은 [Execute]가 아니라 [Plan] 단계에서 worker를 하나 띄우는 `L2`다. worker의 출력은 [Define]으로 바로 가지 않고, 사용자에게 보여 주도록 메인 세션으로 돌아간다.

**마일스톤 기획** (plan 스킬에서 흡수):
사용자가 "로드맵 만들어 줘", "마일스톤 재구성해 줘"처럼 `progress.md`의 구조를 바꾸자고 하면 L3로 에스컬레이션한다. 기획 질문은 다음과 같다.
1. 최종 목표는 무엇인가?
2. 마감이 있는가?
3. 마일스톤을 얼마나 크게 잡을까?
4. 바로 시작해야 하는 일이 있는가?

답을 바탕으로 `progress.md` 초안을 쓰고 사용자에게 검토받는다. Milestone > Phase > Task 3단 구조에 `[x]`/`[ ]` 체크박스를 쓴다. 그 뒤의 체크박스 갱신은 scribe가 맡는다.

### [Define]
- 이번 회차의 루프 정의 YAML을 확정한다.
- 이번 회차에 무엇을 고칠지 구체적으로 정한다.
- 첫 회차에는 기준선(현재 테스트 결과, 현재 지표)을 잡는다.

### [Execute]
- 파일을 고치기 전에 git이 추적하는 파일인지 확인한다.
  - 추적되는 파일: discard하면 `git restore`로 되돌린다.
  - 추적되지 않는 파일: discard할 때 되돌릴 수 있도록 원본을 메모리에 들고 있는다.
- `loop.modify` 범위 안에서만 고친다.
- 고치기 전에 `loop.constraints`를 확인한다.
- `loop.run` 명령을 실행하고 출력을 모은다.

### [Evaluate]
- `loop.evaluate` 기준으로 결과를 잰다.
- 직전 회차와 비교한다(첫 회차면 기준선과 비교한다).
- 평가는 숫자와 근거를 붙여 보여 준다.

### [Judge] — 세 갈래 판단

| 판단 | 조건 | Git 동작 |
|----------|-----------|------------|
| **keep** | `loop.judge.keep` 충족 | 자기 검토 → guard(운영 검사) → witness(의도·기준선 일치) → 커밋 |
| **discard** | `loop.judge.discard` 충족 | `git restore`(되돌림) |
| **refine** | 일부만 나아짐 | 잘된 부분은 두고 잘못된 부분을 고쳐 다시 실행 |

**keep 파이프라인**은 세 관문을 차례로 거친다. 어느 관문이든 판단을 낮출 수 있다. 하지만 세 관문이 똑같이 튼튼한 층은 **아니다**. 값싼 것부터 돌리는 순서이고, 관문마다 실제로 무엇을 보장하는지 정직하게 적어 둔 것이다.

1. **자기 검토** (메인 세션, System 1) — diff를 쓴 에이전트가 직접 빠르게 다시 읽는다. 이것은 **구조적 격리가 아니다**. 자기 검토에는 작성자의 판단이 그대로 남으므로 규율에 의존하는 잔여 층이다. 서브에이전트를 띄우는 비용을 쓰기 전에 눈에 띄는 실수를 싸게 걸러 내는 것이 이 관문의 역할이다. 검증이 아니라 잡음 거르개로 여긴다. 루프가 자기 검토 *하나만* 관문으로 삼는다면 설계가 망가진 것이다.
2. **guard** (메인 세션, 검증 검사) — 커밋 전 테스트 실행, 민감 파일 차단, 규율 준수, 새 함정 감지를 맡는다. 같은 컨텍스트 안에서 돈다. 여전히 메인 세션 쪽이지만, 의도를 스스로 해석하기보다 구조적 규칙(파일 패턴, 테스트 결과)을 기준으로 삼는다. `skills/guard/SKILL.md`를 본다.
3. **witness** (따로 띄운 서브에이전트, 절차상 격리) — 산출물이 의도·기준선과 맞는지 확인한다. 사용자 발화 원문을 차례대로 모은 것과, 있을 때는 승인 기준선 묶음을 서로 다른 입력으로 넘겨 띄운다. 메인 세션의 추론 과정은 띄울 때 쓰는 프롬프트 층(규율)과 실행 컨텍스트 층(하네스가 강제)에서 빠진다. 현재 Claude Code에서 이것이 실제로 무엇을 뜻하는지는 `agents/sonmat-witness.md` §격리의 세 층 (Isolation stack)에 정직하게 나눠 적어 두었다. 커밋마다 witness를 띄울지는 `loop.yaml`에 정한 구조적 결정이다(`witness.commit: required | optional | skip`). 메인 세션이 실행 중에 판단할 일이 결코 아니다. 루프 정의에 아무 말이 없으면 `required`로 본다.

어느 관문이든 막는 판정(guard 차단 / witness `BLOCK`)을 내면 판단은 keep이 아니라 **refine**이 된다. 막지 않는 발견 사항(guard 경고 / witness `WARN`)은 사용자에게 보여 주고, 사용자가 확인하면 진행한다.
witness의 `AUTHORITY_CONFLICT`는 어느 쪽 경로도 아니다. refine할 대상을 고르지 말고 판단을 멈춘 뒤, 어느 쪽 지시를 고칠지 사용자에게 묻는다.

witness 판정의 신뢰도에 관한 참고: witness가 비교자로서 지키는 규율(유효한 출처만 인용하고, 출처에 따라 판정을 정하고, 강도를 판단하지 않는 것)은 **프롬프트 수준**이고 실행 중에 강제되지 않는다. 자세한 구분은 `agents/sonmat-witness.md` §격리의 세 층 (Isolation stack)에 있다. witness를 쓰기 시작한 초기에는 사람이 판정을 표본으로 골라 지정된 규칙을 실제로 따르는지 확인해야 한다. 규칙에서 벗어나는 모습(예: 인용 없는 판정, 강도를 근거로 매긴 WARN)이 보이면 에이전트 파일을 고쳐야 한다. 이런 일은 journal에 남기는 것이 맞다(scribe가 witness 판정을 기록하는 까닭이 바로 이것이다).

세 관문의 순서는 일부러 정한 것이다. 값싼 검사를 먼저 하고, 서브에이전트를 띄우는 비용이 드는 구조적 격리 검사를 마지막에 둔다. witness가 마지막 관문인 까닭은, 값싼 관문이 어차피 잡지 못했을 내용에서 격리의 가치가 가장 크기 때문이다. **세 관문은 스위스 치즈 모형에서 서로를 보완하는 층이다. 중복도 아니고, 서로 바꿔 쓸 수도 없으며, 하나가 다른 것을 대신할 수는 더더욱 없다. 자기 검토만으로는 가장 얇은 층 하나뿐이고, 정직하게 말할 수 있는 최소 구성은 guard와 witness를 함께 쓰는 것이다.**

**보존 구역** (글쓰기처럼 주관적인 분야): refine이나 discard를 하다가 어떤 부분은 "이전 판이 더 나았다"는 것이 드러나면 그 부분을 `loop.constraints`에 더한다. 회차마다 사용자 확인을 받아 보존 구역을 갱신한다.

**에스컬레이션 확인**: 판단할 때마다 FOR(Feeling of Rightness, 맞다는 느낌)를 발동 신호 4개(5절)에 비춰 스스로 점검한다. 하나라도 걸리면 에스컬레이션한다.

### [Record]
- keep: 커밋 메시지에 회차 번호와 지표 변화를 넣는다.
- discard: 왜 버렸는지 적는다(다음 회차에 같은 실수를 막는다).
- refine: 무엇을 남기고 무엇을 고칠지 적는다.

### [Repeat/Exit]
- `loop.exit`을 충족하면 루프를 끝내고 최종 보고를 낸다.
- 충족하지 못하면 [Define]으로 돌아간다.
- 끝낼 때는 전체 회차 수, 지표 변화 궤적, 최종 상태를 적는다.
- **루프 산출물**: 다음 루프로 맥락을 이어 가야 하면 출력 경로, 핵심 결과, 다음 루프의 제약을 기록한다.

**숲 범위 witness 확인** (끝낼 때, scribe보다 먼저):

scribe에 위임하기 전에, 아래 조건 가운데 하나라도 맞으면 witness를 **세션 숲 범위**(session forest scope)로 띄운다. 이 세션의 승인 기준선 묶음이 있으면 함께 넘기고, 기억에 의존해 다시 만들어 내지 않는다.

| 조건 | witness 범위 |
|---|---|
| 세션에서 서로 다른 파일을 3개 이상 건드렸다 | `session-forest` |
| 세션의 사용자 발화 가운데 범위를 넓히는 표현("전체", "모든", "시스템 전반", "일관되게", "across all" 등)이 하나라도 있다 | `principle-coverage` |
| `loop.yaml`에 `witness.forest: required`가 있다 | 선언한 대로 |

숲 범위 witness는 (a) 세션 전체의 사용자 발화를 차례대로 모은 것, (b) 있을 때는 승인 기준선 묶음, (c) 세션 동안 쌓인 `git diff`를 받는다. 발견 사항은 다음과 같이 처리한다.

- `PASS` 또는 `WARN` → scribe 위임으로 넘어간다. WARN은 사용자에게 그대로 보여 주고, 사용자가 무시하기로 할 수 있다.
- `BLOCK` → 평범한 keep 종료라면 아직 scribe에 위임하지 않는다. BLOCK 발견 사항을 사용자에게 보고한다. 루프 종료를 멈추고, 고칠지([Execute]로 돌아간다) 무시할지(불일치를 인정하고 진행한다)는 사용자가 정한다.
- `AUTHORITY_CONFLICT` → 평범한 종료라면 scribe에 위임하지도 `[Execute]`로 돌아가지도 않는다. 서로 부딪치는 출처를 보고하고, 어느 쪽 지시를 고칠지 사용자가 정할 때까지 기다린다.
- `INSUFFICIENT_GROUND_TRUTH` → 사용자에게 보고하고 scribe 위임으로 넘어간다.

메인 세션 혼자서는 세션이 끝날 때 "숲 검토"를 믿을 만하게 해낼 수 없다. 이 확인은 그 검토를 구조로 대신한다. 사용자 발화만 보도록 격리된 비교자는, 여러 파일에 반쯤만 적용했거나 끊긴 참조를 남긴 종류의 누락을 잡는다. 메인 세션의 추론은 이런 누락을 그냥 통과시키기 쉽다. 전체 정의는 `agents/sonmat-witness.md` §범위 규모 (Scope scales)를 본다.

**scribe 위임** (끝낼 때, 숲 범위 witness 다음):
- **keep**: scribe에 mode `all`(bridge + journal + progress)로 위임한다. 루프 보고, git diff, 숲 범위 witness 판정을 산출물로 넣는다.
- **discard**: scribe에 mode `journal`로만 위임한다. 무엇을 시도했고 왜 실패했는지 기록한다.
- **사용자가 명시적으로 세션 마무리나 인계를 요청했다면**, keep이든 discard든 scribe의 마무리 절차로 bridge와 journal에 무엇을 남길지 검토한다. `BLOCK`이나 `AUTHORITY_CONFLICT`가 풀리지 않은 채 남아 있으면 기록을 생략하지 말고, 멈춘 상태와 아직 내려지지 않은 결정을 기록한다. 이것은 끝나지 않은 일을 넘기는 인계이지 keep 판정이나 무시 결정이 아니며, 실행은 멈춘 채로 둔다. witness 격리는 여기에도 그대로 적용된다. bridge에는 짧은 판정 표시만 두고, 발견 사항은 journal에 둔다.
- 평범한 종료에서는 scribe가 백그라운드에서 돈다. 기다리지 말고 사용자와 계속 대화한다. 종료가 명시적인 세션 마무리 요청에 답하는 것이라면 scribe의 완료 확인 절차를 따르고, 저장된 기록을 확인한 뒤에 마무리를 알린다.

### 회고 (Retrospective, 3회차 이상일 때)
- 시도한 방법의 순서가 최선이었는가?
- 어디서 의도와 결과가 갈라졌는가?
- 시도하지 않은 방법 가운데 더 나았을 법한 것은 무엇인가?
- 루프 보고에 1~2줄 요약을 넣는다.

### 메모리 갱신 (Memory update, 루프를 끝낼 때)
회고를 마친 뒤 이 루프에서 기존 규율이 다루지 않던 실패나, 기존 힌트가 잡았어야 할 실패가 드러났는지 확인한다.
- 드러났다면 새 함정과 같은 꼴의 내용(패턴, 맥락, 포착 신호, 관련 기존 힌트가 있다면 그것)을 담아 scribe에 위임한다. scribe는 계열 확인으로 새 교훈인지, 힌트를 불러오거나 발동하거나 적용하는 데 생긴 문제인지 가른 다음, 일반화와 사용자 확인, 메모리나 힌트 변경을 맡는다. `skills/scribe/SKILL.md` §새 함정 기록 (Novel Trap Recording)을 본다.
- 프로젝트 교훈이 여럿 쌓였다면, 그 가운데 범용 메모리로 올리거나 scribe §새 함정 기록 (Novel Trap Recording) 2단계(계열 확인)에 따라 힌트로 올릴 것이 있는지 확인한다. 이 일도 scribe에 위임한다.


## 3. 루프 정의 템플릿 (Loop Definition Templates)

### 개발 루프 (Dev loop)
```yaml
loop:
  name: "Feature / bug fix"
  modify: "src/ relevant files"
  run: "uv run pytest tests/ -v"
  evaluate:
    metrics: ["test_pass_rate"]
  judge:
    keep: "All tests pass"
    discard: "Existing tests broken"
    refine: "New tests pass, some existing fail"
  witness:
    commit: required    # per-iteration commit gate
    forest: required    # loop-exit forest check
  exit: "All tests pass + self-review done"
```

### 글쓰기 루프 (Writing loop)
```yaml
loop:
  name: "Editing pass"
  modify: "target document"
  run: "One editing pass — show diff"
  evaluate:
    criteria: ["consistency", "flow", "conciseness"]
    require_user_confirmation: true
  judge:
    keep: "Improved over previous"
    discard: "Worse — original was better"
    refine: "Partly improved, partly over-edited"
  witness:
    commit: optional    # subjective domain — witness is advisory
    forest: required    # still worth checking at exit
  exit: "Fewer than 5 changes in a pass"
```

`require_user_confirmation: true`는 글쓰기나 디자인처럼 자동 판단을 믿기 어려운 분야에 쓴다. keep/discard 전에 반드시 바뀐 내용을 보여 주고 승인을 받는다.

### `witness` 필드 참조 (field reference)

루프 정의마다 witness 범위를 지정하는 것이 좋다. 생략하면 `commit: required`와 `forest: required`가 기본값이다.

| 필드 | 값 | 뜻 |
|---|---|---|
| `witness.commit` | `required` \| `optional` \| `skip` | `[Judge]` keep 파이프라인에서 commit-gate witness를 돌릴지 정한다. `optional`이면 witness를 돌리되 발견 사항은 참고용으로 보여 준다. `skip`이면 아예 끈다(의도와의 일치가 본래 모호한 주관적 분야에만 쓴다). |
| `witness.forest` | `required` \| `optional` \| `skip` | 루프를 끝낼 때 session-forest witness를 돌릴지 정한다. 세션에서 파일을 3개 이상 건드렸거나 사용자가 범위를 넓히는 지시를 했으면 기본값은 `required`다. `skip`은 명시적으로 파일 하나만 다루는 루프에만 알맞다. |

`witness.commit: skip`은 메인 세션이 실행 중에 스스로 허락할 수 없는 우회다. 그때그때 정하지 말고 `loop.yaml`에 미리 선언해야 한다. 근거는 `agents/sonmat-witness.md` §witness를 부르는 때 (When witness is invoked)를 본다.


## 4. 규율 주입 (Discipline Injection)

### 주입 순서 (Injection order)
1. core.md를 불러온다(항상)
2. hints.md를 불러온다(항상 — 관련된 것은 worker가 골라 적용한다)
3. 프로젝트 AGENTS.md의 재정의를 적용한다(`## sonmat` 절이 있을 때. AGENTS.md가 없을 때만 예전 방식인 CLAUDE.md를 쓴다)
4. System 1 처리나 System 2 worker 프롬프트에 주입한다

**제외**: witness에는 규율을 **결코** 주입하지 않는다. witness는 규칙을 따르는 쪽이 아니라 비교하는 쪽이다. witness가 지키는 작동 원칙은 에이전트 정의 안에 들어 있고 core.md 규율과는 별개다(`agents/sonmat-witness.md` §작동 원칙 (Operating principles) 참조). witness의 입력은 사용자 발화 원문, 산출물, 그리고 선택적으로 §6b에서 정의한 승인 기준선 묶음 그대로뿐이다. 그 밖에는 아무것도 넣지 않는다.

### 프로젝트 재정의 형식 (Project override format)
```markdown
## sonmat
discipline:
  add:
    - "Custom rule for this project"
```

### worker 프롬프트 구성 (Worker prompt composition, L2/L3)
```
[1. Role]       — 1 line. Debugger/executor/researcher/reviewer.
[2. Discipline] — core.md + hints.md + project overrides. ~30 lines.
[3. Loop context] — Loop definition YAML + current iteration state.
[4. Task]       — Specific work instructions + reporting format.
```


## 5. 에스컬레이션 체계 (Escalation System)

이중 처리 이론에 바탕을 둔다. 평소에는 System 1이 처리하고, FOR(Feeling of Rightness, 맞다는 느낌)가 떨어지면 System 2로 에스컬레이션한다.

### 발동 신호 4개 (4 Triggers)

| 발동 신호 | 감지 | 예 |
|---------|-----------|---------|
| **Surprise** (놀람) | 예상한 결과와 실제 결과가 다르다 | 통과할 줄 알았던 테스트가 실패했다 |
| **Error** (오류) | 같은 실패가 2번 이상 나거나, 고치면 다른 곳이 깨진다 | 같은 테스트가 두 번 실패했다 |
| **Fluency break** (흐름 끊김) | 참조가 없거나 범위가 불분명하다 | 파일이나 경로를 찾지 못했다 |
| **Conflict** (충돌) | 행동이 core.md 규칙이나 루프 계획과 부딪친다 | core.md 규칙 위반을 감지했거나, 행동이 `loop.constraints`와 어긋나게 된다 |

### 단계 4개 (4 Levels)

| 단계 | 이름 | 행동 |
|-------|------|--------|
| **L0** | System 1 | 바로 실행하고 에스컬레이션하지 않는다 |
| **L1** | System 1 강화 | 멈추고 영향 범위를 확인한다 |
| **L2** | System 2 띄우기 | sonmat-worker 하나를 띄운다(깊은 분석) |
| **L3** | System 2 확장 | worker 여럿을 병렬로 띄운다 |

### 발동 신호 → 단계 대응 (Trigger → Level mapping)

| 상황 | 단계 |
|-----------|-------|
| 처음 나온 예상 밖 결과 | L0 → L1 |
| 같은 실패 2번 | L1 → L2 |
| 고쳤더니 다른 곳이 깨짐 | → L2 |
| 파일이나 경로가 없음 | L0 → L1 (찾아보고 다시 시도) |
| 의존성이 없고 범위도 불분명함 | → L2 |
| core.md 규칙 위반 | → L1 |
| 기존 계획과 범위가 달라짐 | → L2 |
| 마일스톤 규모의 기획 | → L3 |
| L2 worker가 풀지 못함 | → L3 |

### 에스컬레이션 출력 (Escalation output)
```
⚡ [Trigger] detected
  Cause: [specific cause]
  Action: L[N] → [what will be done]
  💡 Tip: [customization suggestion] (when applicable)
```

### 해소 출력 (Resolution output)
```
✓ [Trigger] resolved → L[N] return ([brief explanation])
```


## 6. 서브에이전트 위임과 분기 (Subagent Dispatch & Routing)

autoloop는 서로 다른 두 종류의 서브에이전트를 띄운다. 목적, 입력, 결과 처리 규칙이 다르다. 띄우고 결과를 처리하는 방식이 비슷해서 여기에 함께 적었지만, 둘은 서로 바꿔 쓸 수 **없다**.

| 서브에이전트 | 목적 | 입력 | 띄우는 때 |
|---|---|---|---|
| **sonmat-worker** | System 1로 감당하기 어려운 깊은 분석이나 구현 단계를 실행한다 | 규율을 주입한 프롬프트 + 루프 맥락 + 작업 지시 | [Execute] 중 L2/L3 에스컬레이션, 또는 [Plan] 브레인스토밍 |
| **sonmat-witness** | 격리된 컨텍스트에서 산출물이 의도·기준선과 맞는지 검증한다 | 사용자 발화 원문을 차례대로 모은 것 + (선택) 승인 기준선 묶음 + 산출물(git diff / 파일) — **규율 주입도, 메인 세션의 추론 과정도 넣지 않는다** | [Judge] keep 파이프라인(commit gate) + [Repeat/Exit](session forest) |

### 6a. worker 위임 (Worker dispatch)

#### L2: worker 하나 (Single worker)
4절(규율 주입)의 프롬프트로 sonmat-worker를 띄운다. worker는 규율 전체를 받는다.

#### L3: worker 여럿 병렬 (Parallel workers)
- 서로 독립인 작업으로 나눈다(파일이 겹치지 않게).
- 규율은 같게, 작업 지시는 다르게 준다.
- 모두 끝나기를 기다린 뒤 충돌을 확인하고, 합치거나 사용자에게 에스컬레이션한다.

#### 위임 현황판 (Dispatch board, 서브에이전트 2개 이상)

서브에이전트 둘 이상이 동시에 돌거나 사슬로 이어질 때만 현황판을 쓴다(예: 조사 worker → 구현 worker → witness → scribe). L0~L2에서 한 건만 위임할 때는 쓰지 않는다. 대화 안에 마크다운 표 하나로 적는다. 새 파일, 도구, JSON 장부를 만들지 않는다. 작업 단위의 상태가 바뀔 때만 갱신한다.

```markdown
Dispatch board — G1 (requirement as of <turn>)
| Unit (ID · write scope) | Status | Result (one-line pointer) | Cross-impact / open |
|---|---|---|---|
| research-a · WRITE notes-a.md | VERIFIED G1 | 12 cases → notes-a.md §2 | ! overlaps research-b on 2 cases — dedupe at merge |
| impl · WRITE src/auth/ | RETURNED G1 | token refresh patched | ! not run against staging |
```

- **상태(Status)**: `DISPATCHED` → `RETURNED`(보고를 받았으나 확인하지 않음) → `VERIFIED`(산출물을 직접 확인함) / `BLOCKED`(사유) / `CANCELED`. worker가 `DONE`을 보고하면 그 단위는 `VERIFIED`가 아니라 `RETURNED`가 된다.
- **세대(Generation)**: 진행 도중 요구 사항이 바뀌면 `G1`을 `G2`로 올린다. 이전 세대의 결과는 합치기 전에 다시 판단한다.
- **`!` 항목**: 합칠 때의 제약, 이웃 작업 단위에 주는 영향, 확인하지 않은 전제를 마지막 열에 적는다. 그래야 완료 보고에 가려 사라지지 않는다. 전달하기 전에 `!` 항목을 모두 해결하거나 보고한다.

현황판은 일부러 작게 둔다. 추적하는 작업보다 갱신 비용이 더 큰 장부는 결국 건너뛰게 되고, 그러면 상태를 잘못 알린다.

#### worker 상태 → 루프 분기 (Worker status → loop routing)

| 상태 | 루프 동작 |
|--------|-------------|
| `DONE` | [Evaluate]로 넘긴다 |
| `DONE_WITH_CONCERNS` | [Evaluate]로 넘기고 우려 사항을 사용자에게 보고한다 |
| `NEEDS_CONTEXT` | 맥락을 더 주거나 사용자에게 묻는다 |
| `BLOCKED` | L3로 에스컬레이션하거나 사용자에게 넘긴다 |

worker가 `loop.modify` 밖의 파일을 고쳐야 하면 직접 고치지 말고 그 필요를 보고해야 한다. 메인 세션이 사용자에게 범위를 넓힐지 묻는다.

### 6b. witness 위임 (Witness dispatch)

witness는 worker가 **아니다**. 규율을 받지 않고, 작업을 실행하지 않으며, 상태를 바꾸지 않는다. witness가 하는 일은 메인 세션의 추론과 절차상 격리된 채 비교자로서 검증하는 것 하나뿐이다(`agents/sonmat-witness.md` §격리의 세 층 (Isolation stack)).

**witness를 실제로 띄우는 방법**: autoloop의 [Judge] keep 파이프라인과 [Repeat/Exit] 숲 범위 확인 안에서 Task 도구를 `subagent_type: sonmat-witness`로 호출한다. 문서화되어 있고 지원되는 경로다. Task 도구로 서브에이전트에 맡기는 것이 Claude Code에서 격리된 서브에이전트를 띄우는 기본 수단이다. 이 문서의 초기 초안은 "PreToolUse hook → agent hook → deny" 파이프라인을 언급했지만, 그 경로는 PreToolUse에 대해서는 문서화되어 있지 않은 것으로 드러났고 지금 쓰는 경로도 아니다. 강제는 autoloop 규율에 기댄다. 메인 세션은 [Judge] 파이프라인 순서를 따라야 하고, witness Task 호출은 그 순서의 한 단계다. autoloop의 다른 모든 단계와 같은 방식, 곧 규율로 강제하는 방식이다.


띄우는 지점:
- **[Judge] keep 파이프라인** — 회차마다 commit-gate 범위로 띄운다. `loop.witness.commit`이 결정한다.
- **[Repeat/Exit]** — 루프를 끝낼 때 session-forest 범위로 띄운다. `loop.witness.forest`가 결정한다.

띄울 때 쓰는 프롬프트의 구성은 worker와 다르다.

```
[1. Scope]    — commit | session-forest | principle-coverage
[2. User turns] — raw, unmodified. Session cascade for forest scope; task cascade for commit.
[3. Approved baseline] — optional envelope: exact displayed plan/loop definition + raw approval turn
[4. Artifact]  — git diff + file paths. No summary.
[5. Principle candidate] — (optional, principle-coverage only) literal phrase anchored to user turns
```

어시스턴트가 쓴 계획 가운데 넣어도 되는 것은 승인 기준선 묶음뿐이다. 승인 발화가 그때 보여 준 바로 그 내용을 가리킨다는 것이 모호하지 않을 때만 넣는다. **절대 넣지 않는 것**: 다른 어시스턴트 계획이나 요약, discipline/core.md, hints.md, 메인 세션의 추론 과정, 메인 세션이 적은 적용 메모나 학습 요약, worker 보고, 이전 witness 판정, bridge note, journal 발췌, 그 밖의 scribe 기록, 별도 입력으로서의 커밋 메시지. 메인 세션은 피드백을 바탕으로 산출물을 고쳐도 된다. 새로 띄운 witness는 이전 피드백을 받지 않고 고친 산출물을 비교한다. 별도 컨텍스트나 대화 이력을 물려받지 않는 분기(no-history fork)를 쓴다고 해서 프롬프트에 직접 넣은 자료가 걸러지지는 않는다. 산출물 안에 들어 있는 주석과 커밋 메시지는 보이지만 인용 근거로 쓸 수 없다(witness.md §보이지만 인용할 수 없는 것 (Seen-but-unusable) 참조).

#### witness 판정 → 루프 분기 (Witness verdict → loop routing)

| 판정 | 루프 동작 |
|---------|-------------|
| `PASS` | 커밋이나 세션 종료를 진행한다. 판정은 journal에 기록한다(scribe 위임으로). |
| `BLOCK` | commit 범위: 판단을 **refine**으로 낮추고, 인용된 불일치를 다음 [Execute]의 대상으로 삼는다. 숲 범위: 세션 종료를 멈추고 발견 사항을 사용자에게 보고하며, 고칠지 무시할지는 사용자가 정한다. 그 사이에 실제 변경이 없으면 같은 산출물로 witness를 다시 돌리지 않는다. |
| `WARN` | 인용을 포함해 그대로 사용자에게 보여 준다. 사용자가 확인하면 진행하고, 거부하면 refine한다. |
| `AUTHORITY_CONFLICT` | 커밋이나 세션 종료를 멈춘다. 서로 부딪치는 사용자 원문 의도와 승인 기준선을 보여 주고, 어느 쪽을 고칠지는 사용자가 정한다. 그 결정 전에는 메인 세션이 어느 쪽으로도 refine해서는 안 된다. |
| `INSUFFICIENT_GROUND_TRUTH` | witness가 검사를 돌리지 못했다. 의도와의 일치를 검증하지 *않은 채* 진행한다고 사용자에게 보고한다. 말없이 묻어 두지 않는다. |

메인 세션이 스스로 판단해서 witness 판정을 뒤집는 일은 없다. witness가 틀렸다고 보면 사용자에게 에스컬레이션하고, 결코 자동으로 우회하지 않는다. 이것이 구조적 격리 원칙이며, 우회하면 이 장치는 쓸모가 없어진다.


## 7. 사용자 성장 (User Growth)

철학: "나쁜 사용자는 없다." 모든 판단을 투명하게 드러내야 사용자가 성장할 수 있다.

### 원칙 3개 (3 Principles)
1. **고칠 수 있는 곳을 열어 둔다**: 루프 정의, 규율 재정의, 프로젝트 규칙은 언제든 고칠 수 있다. 어디를 고치면 되는지 적극적으로 보여 준다.
2. **필요한 순간에 안내한다**: 에스컬레이션할 때 다음에 이를 막는 방법을 제안한다. 강요하지 않는다.
3. **판단을 투명하게 한다**: 모든 keep/discard/refine과 에스컬레이션에 "왜"를 붙인다.

### 루프 보고 형식 (Loop report format)
```
📊 Loop Report
  N iterations | keep M | discard K | refine J
  Escalations: [summary or "none"]
  Retrospective: [1-2 lines, if 3+ iterations]
  Result: [final state]
```

간단한 루프(keep 한 번으로 끝남): `📊 1 iteration. [result]. No escalation.`
