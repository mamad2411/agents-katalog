---
name: scribe
description: '세션이 끝나도 남아야 할 것을 기록한다. bridge note, journal, 마일스톤 진행, 사용자 교정에서 찾은 프로젝트 규칙(AGENTS.md), guard가 감지한 새 함정, witness 판정이 대상이다. 사용자가 세션을 마무리하거나 넘기려 할 때("마무리하자", "인계해 줘", "새 세션으로 넘어갈게"), 루프·작업이 끝났을 때, 같은 교정이 두 번 나왔을 때 쓴다. 규칙·함정 기록은 사용자 확인 뒤에만 쓴다. 이전 기록을 찾는 일(requery)에는 쓰지 않는다.'
user-invocable: false
---

# Scribe — 작업 뒤 기록 층 (Post-Work Persistence Layer)

scribe는 sonmat 체계에서 축 하나를 맡는다. **지금 세션이 끝난 뒤에도 남아야 하는 모든 것**이다. 다음 세션을 위한 bridge note, 이력을 위한 journal 항목, 마일스톤 진행 체크박스, 사용자가 같은 것을 되풀이해 바로잡으면서 드러난 프로젝트 규칙, guard가 표시한 새 함정, `[Judge]` 파이프라인에서 나온 witness 판정이 여기에 든다. 기록은 모두 scribe를 거친다.

이 역할은 감지(guard), 비교(witness), 완결성 확인(punch)과 다르다. 그 스킬들은 무언가를 찾아낸다. scribe는 찾아낸 것 가운데 무엇을 남길 만한지, 어디에 둘지를 정한다.

scribe는 사용자가 직접 부르지 **않는다**(`/scribe` 명령이 없다). 메인 세션과 다른 스킬이 부르는 절차다. 세션 마무리를 요청받으면 메인 세션이 위임하고, 루프를 끝낼 때 autoloop가 백그라운드 scribe에 위임하고, 작업 중에 guard가 새 함정과 프로젝트 규칙을 넘기고, `[Judge]` 파이프라인에서 나온 witness 판정이 scribe로 흘러든다. 사용자는 마무리하자거나 맥락을 남겨 달라고 말하면 되고, scribe라는 이름을 댈 필요는 없다.

---

## 작동 방식: 동기와 백그라운드 (Operation modes: synchronous vs background)

scribe는 무엇을 기록하느냐에 따라 두 방식으로 돈다. 방식마다 사용자와 주고받는 약속이 달라서 이 구분이 중요하다.

| 방식 | 언제 | 메인 세션을 멈추는가? | 하는 일 |
|---|---|---|---|
| **백그라운드** | 작업이 끝난 뒤(루프 종료, 작업 완료, 세션 종료) | 평범한 위임이면 멈추지 않는다. 사용자가 명시적으로 마무리를 요청한 세션이면 닫기 전에 완료를 확인한다 | bridge note, journal 추가, 진행 체크박스 갱신, witness 판정 기록 |
| **동기** | 작업 도중, 발견 사항을 쓰기 전에 사용자 확인이 필요할 때 | 멈춘다. 메인 세션이 멈추고 사용자에게 예/아니오를 받는다 | 프로젝트 규칙 제안(`AGENTS.md`에 쓴다), 새 함정 제안(메모리에 쓴다) |

평범한 백그라운드 기록은 맡기고 잊는다. 산출물을 주어 sonmat-scribe에 위임하고 사용자와 계속 대화한다. 사용자가 명시적으로 세션 마무리를 요청했다면 메인 세션은 결과를 기다리고, 저장된 기록을 확인한 뒤에 마무리를 알린다. 동기 기록은 사용자 확인을 거쳐야 한다. `AGENTS.md`나 메모리 기록처럼 선언적인 파일은 사용자의 명시적 승인 없이 절대 쓰면 안 되기 때문에, 제안을 주고받는 대화는 메인 세션이 직접 그 자리에서 진행한다.

두 방식이 모두 scribe에 속하는 까닭은 **축이 같기** 때문이다(세션에서 찾은 것을 기록한다). 다른 것은 사용자와 주고받는 약속뿐이다. 둘을 서로 다른 스킬로 나누지 않는다. 나누면 기록 축이 쪼개지고, 다른 스킬은 무엇을 누구에게 넘겨야 할지 헷갈리게 된다.

---

## witness를 보호하는 격리 경계 (Isolation boundaries)

메인 세션은 witness 피드백을 바탕으로 산출물을 고치고 그 결과에서 배워도 된다. 격리는 witness를 새로 부를 때마다 적용된다. 새 witness는 이전 판정이나 실행한 쪽의 해석을 받지 않고, 사용자 원래 요청, 있을 때는 유효한 승인 기준선, 실제 산출물을 비교한다. 메인 세션이 피드백에서 배운다고 해서 그것만으로 이 경계가 깨지지는 않는다.

격리 경계는 다음과 같다.

- 다음 작업을 시작할 때 메인 세션이 읽는 bridge note에는 짧은 PASS/WARN/BLOCK/AUTHORITY_CONFLICT 표시, 따로 확인한 수정 결과, 승인된 결정, 아직 풀리지 않은 상태를 담을 수 있다. 발견 사항 원문, 판정 근거를 인용한 글, 그 근거를 되풀이할 뿐인 요약은 journal에 두고, 자세한 내용이 필요하면 journal로 링크한다.
- journal에는 witness 발견 사항과 그 인용을 자세히 담는다. 자동으로 불러오지는 않지만, 메인 세션이 회고나 기획을 할 때 §journal 열람 (Journal Access)에 따라 읽을 수 있다. 기록된 판정은 그 출처에 대조해 확인할 보고일 뿐, 판정이 옳았다는 증거가 아니다.
- AGENTS.md의 Project Rules, 승인된 메모리 기록, 승격된 힌트는 평소 불러오는 경로로 메인 세션과 worker에 닿을 수 있다. AGENTS.md는 Codex가 기본으로 불러온다. 이런 규칙을 기록하거나 고치려면 여전히 기존 확인 절차와 계열 확인 절차를 거쳐야 한다. witness 발견 사항 하나만으로 새 규칙을 만들 수는 없다.

witness를 띄우는 프롬프트에는 이전 판정, 메인 세션의 해석이나 학습 요약, worker 보고, bridge note, journal 발췌, 그 밖의 scribe 기록을 절대 넣지 않는다. witness가 받는 것은 사용자 발화 원문, 산출물, 그리고 선택적으로 승인 기준선 묶음 하나다. 이 묶음에는 그때 보여 준 계획 그대로와 승인 발화 원문이 들어 있다. 메인 세션은 `skills/autoloop/SKILL.md`의 §6b witness 위임 (Witness dispatch)에 따라 이 입력을 새로 구성해야 한다. 별도 컨텍스트나 대화 이력을 물려받지 않는 분기(no-history fork)를 쓴다고 해서, 제외해야 할 자료를 메인 세션이 프롬프트에 직접 넣는 일까지 막히지는 않는다. 입력 구성 규칙과 인용 규칙은 절차상 의무이고 플랫폼이 보장하는 것이 아니다. [피드백 경계 결정](../../docs/decisions/2026-11-10-feedback-and-witness-input-boundary.md)을 본다.

---

## 위임 절차 (Dispatch Protocol)

### 언제 위임하는가 (When to dispatch)

사용자가 지금 세션을 닫거나 넘기자고 명시적으로 요청하면, 작은 작업이나 대화라서 자동으로 건너뛰는 조건보다 그 요청이 앞선다. 정해진 문구 목록이 아니라 맥락에서 사용자의 뜻을 알아본다. 마무리 표현을 설명하거나 인용하는 것은 요청이 아니다. 코드 diff가 없으면 메인 세션이 사실만 정리한 세션 인계를 산출물로 넘긴다. 무엇을 남길 만한지 검토하고, 같은 기록을 겹쳐 쓰지 않으며, 새로 남길 것이 없으면 그렇다고 알린다. 이 요청이 있다고 해서 기존 확인 절차를 넘어 새 프로젝트 규칙이나 함정 기록을 써도 되는 것은 아니다.

| 조건 | 방식 | 기능 |
|-----------|------|-----------|
| 명시적인 세션 마무리 / 인계 요청 (작업 크기와 상관없이, 대화만 했어도) | 백그라운드, 닫기 전에 확인 | 필요한 만큼 bridge + journal. 로컬 기록 규칙을 따른다 |
| **keep**으로 루프 종료 | 백그라운드 | bridge + journal + progress + witness 판정 |
| **discard**로 루프 종료 | 백그라운드 | journal만 |
| 루프 밖 작업 완료 (파일 3개 이상 변경) | 백그라운드 | bridge + journal |
| 루프 밖 작업 완료 (파일 1~2개) | — (위임하지 않음) | 들이는 비용이 얻는 값보다 크다 |
| 맥락이 끝나지 않은 채 세션 종료 (자동 위임, 명시적 마무리 요청 없음) | 백그라운드 | bridge만 |
| L0 / 사소한 작업 | — (위임하지 않음) | — |
| **guard가 새 함정 감지** (작업 크기와 상관없이) | **동기** | `novel_trap` — 사용자 확인 뒤 메모리에 쓴다 |
| **프로젝트 규칙 패턴 감지** (작업 크기와 상관없이) | **동기** | `project_rule` — 사용자 확인 뒤 `AGENTS.md`에 쓴다 |

동기 위임(아래 두 줄)은 메인 세션이 아래 §프로젝트 규칙 기록 (Project Rule Recording)과 §새 함정 기록 (Novel Trap Recording)의 절차를 따라 그 자리에서 처리한다. 백그라운드 위임은 아래 프롬프트 구조로 sonmat-scribe 에이전트를 띄운다.

### 위임하는 방법 — 백그라운드 (How to dispatch)

`sonmat-scribe`를 백그라운드 에이전트로 띄우고 다음 프롬프트 구조를 쓴다.

```
## Scribe Dispatch

**Mode**: {bridge | journal | progress | witness_log | all}
**Completion check**: {verify before closing for explicit session wrap-up | ordinary background}
**Timestamp**: {ISO 8601, KST}

### Artifacts
- Git diff: {summary or "see below"}
- Changed files: {list}
- Loop report: {paste if available, or "N/A"}
- Test results: {pass/fail summary, or "N/A"}
- Witness verdicts: {list of verdicts from the [Judge] pipeline this session — e.g. "PASS (iter 1), WARN (iter 2, not-covered-by-tests), PASS (iter 3)". "N/A" if none.}
- Session handoff: {agreed decisions, corrections, current status, unresolved work with decision owner and resumption conditions, and supporting references; use when there is no code diff}

### Context hint
{1-2 sentences about what was done — enough for scribe to write a useful bridge note.
Do not send the full conversation or speculate about user motivation.}
```

### 위임한 뒤 (After dispatch)

- 평범한 백그라운드 위임이면 기다리지 말고 사용자와 계속 대화한다.
- 명시적인 세션 마무리라면 DONE / PARTIAL / SKIP과 기록한 파일 경로를 받는다. 완료를 알리기 전에 그 파일들에 이번 세션 항목이 실제로 있는지 확인한다. 저장하지 못한 것이 있거나 새로 남길 것이 없으면 그렇다고 분명히 알린다. 위임했다는 것만으로는 완료가 아니다.
- scribe는 `bridge-note.md`와 `journal.md`를 프로젝트별 scribe 디렉터리(파일 위치 참조)에, `progress.md`를 프로젝트 루트에 쓴다.
- 다음 작업을 시작할 때 `bridge-note.md`가 있으면 읽는다. 맥락으로 쓰고 작업을 이어 간다.

---

## bridge note 읽기 (Bridge Note Consumption)

간단하지 않은 작업을 시작할 때마다:

1. scribe 디렉터리에 `bridge-note.md`가 있는지 확인한다(파일 위치 참조. 없으면 예전 위치인 `.claude/sonmat/`를 본다).
2. 있으면 말없이 읽는다. 맥락으로 쓰되 사용자에게 인용하지 않는다.
3. 넘겨받은 항목이 새 작업과 직접 관련되면 자연스럽게 언급한다.
   ```
   참고: 이전 작업에서 {관련 항목}이 나왔는데, 이번 작업과 연관될 수 있어요.
   ```
4. 관련된 것이 없으면 무시한다.
5. **bridge note는 사실이 아니라 가설로 다룬다**. 이전 세션은 부분적으로만 이해한 채 썼을 수 있다. bridge note의 주장을 근거로 행동하기 전에 실제 코드나 상태에 대조해 확인한다. 주장이 관찰과 다르면 관찰을 믿고, 다음 위임 때 bridge note가 어긋났다고 표시한다.

---

## bridge note 작성 원칙 (Bridge Note Authoring Principles)

scribe가 bridge note를 쓸 때는 네 원칙이 핵심이다. 그 밖의 절은 선택이다. 작업에 필요한 것은 쓰고, 분량만 늘릴 것은 뺀다. (A3의 한 장 분량 제약은 `docs/research/spec-induction-and-sisyphus-review.md`의 Toyota A3 절을 본다.)

1. **남은 일은 지시가 아니라 상태로 쓴다.** "X를 다음에 구현할 것"이 아니라 "X는 아직 구현되지 않았다. Y가 먼저 확정되어야 한다"로 쓴다. 지시형으로 쓰면 다음 세션이 전제를 확인하지 않고 그대로 실행한다(방법이 아니라 의도를 전하는 Auftragstaktik 원칙). 무엇을 할지는 다음 세션이 정하고, scribe는 지금 어떤 상태인지를 기록한다.
2. **피해야 할 함정(Traps to Avoid)이 있으면 반드시 쓴다.** 실패한 방법, 막다른 길, 틀린 것으로 드러난 가설은 코드에서는 사라지지만 다음 세션에는 중요하다. 작업이 실패한 갈래를 하나라도 거쳤다면 그 기록은 bridge note에 들어가야 한다.
3. **bridge note는 사실이 아니라 가설이다.** scribe는 제한된 종합을 바탕으로 쓰고, 다음 세션은 확인해야 한다. 주장을 단정하지 말고 잠정적이라는 것이 드러나게 쓴다("~로 보인다 / 관찰했다 / ~를 근거로 정했다"). 다음 세션이 혼자서 확인할 수 있도록 파일과 줄 위치를 충분히 적는다.
4. **완결성보다 간결함을 앞세운다.** 다음 세션이 1분 안에 읽을 수 있는 노트를 목표로 한다. 자세한 내용이 필요하면 본문에 넣지 말고 별도 산출물(journal, ADR, 보고서)에 링크한다. 훑어 읽어야 하는 bridge note는 하려던 말을 놓친다.

Summary, Key Decisions, Relevant Files, Working Agreements, Prompt for New Chat 같은 절은 쓸모가 있을 수 있다. 작업에 필요하면 넣고, 분량만 늘릴 것 같으면 뺀다. 구조는 자유지만 위의 네 원칙은 자유가 아니다.

---

## journal 열람 (Journal Access)

journal(scribe 디렉터리의 `journal.md`, 파일 위치 참조)은 쌓아만 두는 기록이다. 컨텍스트에 자동으로 불러오지 **않는다**.

다음 경우에만 읽는다.
- 사용자가 "지난번에 뭐 했지?"라고 물을 때
- 사용자가 진행 요약을 달라고 할 때
- 회고나 기획에 이력 맥락이 필요할 때

### journal의 witness 기록 (Witness events in the journal)

위임 산출물에 witness 판정이 들어 있으면 scribe는 그것을 요약에 섞지 않고 journal에 따로 한 줄로 기록한다. `BLOCK`, `WARN`, `AUTHORITY_CONFLICT`는 특히 값진 학습 신호다. 메인 세션의 실행이 사용자 원문 의도나 승인 기준선에서 벗어난 순간을 보여 주므로 회고에서 다시 볼 만하다. `PASS`는 짧게 한 줄로 기록한다.

자세한 발견 사항과 그 인용은 journal에 둔다. bridge에는 짧은 판정 표시와 함께, 따로 확인한 수정 결과, 승인된 결정, 아직 풀리지 않은 상태를 둘 수 있다. 이 기록들은 메인 세션의 후속 작업과 회고를 돕는다. 어느 것도 새 witness 호출의 입력이 되지 않는다. §witness를 보호하는 격리 경계 (Isolation boundaries)를 본다.

실제로 비교하는 사례라면 원래 요청과 산출물 참조, 판정을 확인하는 데 쓴 출처·테스트·확인된 사용자 정정(없으면 "unverified"), 관찰한 후속 상태, 관찰한 재발이나 비용을 기록한다. 사례가 뒷받침하는 필드만 더하고, PASS마다 보고서로 부풀리지 않는다. 호출 여부, 지침 로드 여부, 준수 여부, 작업이 맞았는지는 서로 다른 관찰이며, 재지 않은 것은 0이 아니다.

---

## 프로젝트 규칙 기록 (Project Rule Recording)

예전 guard §2에서 옮겨 왔다.

프로젝트 규칙은 사용자가 어시스턴트도 당연히 안다고 여기는 암묵적 관례다. 작업 중에 guard가 신호를 감지하고, scribe가 그것을 `AGENTS.md`에 기록한다.

### 프로젝트 지침 파일 계약 (Project instruction file contract)

- `AGENTS.md`는 프로젝트 지침의 정본이며 `## Project Rules`를 쓸 유일한 대상이다. Codex는 이 파일을 기본으로 불러온다. 이 목적으로 `CODEX.md`를 만들거나 쓰지 않는다.
- 프로젝트에 `CLAUDE.md`가 필요하면 그것은 Claude Code용 어댑터다. `@AGENTS.md`를 불러오고, 그 밖에는 Claude에만 해당하는 추가 내용만 담을 수 있다.
- 기존 `CLAUDE.md`를 덮어쓰거나 말없이 옮기지 않는다. 그 파일에 프로젝트 규칙이 있는데 `AGENTS.md`가 없으면, 나눌 방안을 보여 주고 사용자에게 따로 승인을 받은 뒤에 어느 파일이든 고친다.
- Codex SessionStart hook은 두 파일 어느 것도 만들지 않는다. 사용자가 승인한 프로젝트 규칙 기록으로 `AGENTS.md`를 만들 수는 있다. Claude 어댑터를 만들거나 바꾸는 일은 여전히 명시적이고 검토할 수 있는 변경으로 남는다.

### scribe에 닿는 신호 (Signals that reach scribe)

다음 가운데 하나라도 일어나면 guard(또는 메인 세션의 관찰)가 프로젝트 규칙 제안을 scribe에 위임한다.

- **직접 말함**: 사용자가 "이 프로젝트에서는 항상 X" 같은 말을 한다
- **되풀이한 정정**: 같은 수정을 2번 이상 요청한다
- **구조에서 짐작**: 설정 파일, 테스트 패턴, 이름 짓는 관례가 어떤 규칙을 함축한다

### scribe가 하는 일 (What scribe does)

1. **초안**: 규칙을 한두 줄로, 프로젝트의 주 언어로 쓴다.
2. **동기적으로 제안한다** (백그라운드가 아니다). scribe가 하는 일 가운데 사용자 확인을 기다리며 멈추는 몇 안 되는 작업이다. 결과가 사용자가 직접 읽는 파일에 쓰이기 때문이다.

   ```
   💡 Project rule detected: {draft rule}
      Add to AGENTS.md? [Yes / No / Rephrase]
   ```

3. 사용자가 확인한 뒤에만 프로젝트 `AGENTS.md`의 `## Project Rules` 절에 **쓴다**. 파일이나 절이 없으면 만든다.
4. **확인 없이 절대 쓰지 않는다**. 프로젝트 규칙은 선언적이고 오래 남는다. 잘못 쓴 규칙은 나중에 원인을 찾는 데 비용이 크다.

프로젝트 규칙은 관찰한 실제 작업 방식에서 쌓인다. 그 쌓는 일, 곧 패턴을 지켜보고 일반화하고 그 일반화를 기록하는 일을 scribe가 맡는다.

---

## 새 함정 기록 (Novel Trap Recording)

예전 guard §4에서 옮겨 왔다.

새 함정은 둘 가운데 **하나**다. 기존 규율과 메모리가 예상하지 못한 검증 실패 패턴이거나, "명세가 이 경우를 다루지 않았다"는 순간이다. 뒤의 것은 규율은 제대로 돌았지만 기존 규칙·명세·계약에 빈틈이 있었고 상황이 그 빈틈을 드러낸 경우다. 둘 다 "무엇을 살펴야 하는가"에 관한 체계의 기존 모델이 불완전하다는 신호이므로 메모리에 넣을 입력이 된다.

두 갈래(flavor)는 다음과 같다.

- **검증 실패** (전형적인 새 함정): 규율이 돌았지만 실제 문제를 놓쳤다. 포착 신호는 그 문제를 더 일찍 잡았을 무언가다.
- **명세 빈틈** (즉흥 대응이 드러난 경우): 규율이 실패한 것이 아니다. 명세나 규칙이 그 경우에 아무 말도 하지 않아서 행위자가 즉흥으로 대응해야 했다. 포착 신호는 명세가 다뤘어야 할 경우가 어떤 종류인지다.

둘 다 같은 경로로 scribe에 닿는다. 앞의 것은 guard가, 뒤의 것은 메인 세션의 관찰이나 autoloop 회고가 보낸다. 기존 힌트가 다루는 실패도 보낸다. 그 힌트를 놓친 것인지, 발동 조건이나 불러오는 경로를 바꿔야 하는지는 scribe의 계열 확인이 정한다. witness 발견 사항은 후보 신호일 뿐 자동으로 정책을 바꾸지 않는다. 교훈을 일반화하기 전에 그것이 인용한 출처, 사용자 원문 의도, 현재 상태를 확인한다. 독일 국방군 *Gefechtsbericht*(전투 보고)의 교훈: 교리의 빈틈을 드러낸 즉흥 대응의 성공은 검증 실패만큼 값지며, 둘 다 다음 판 교범에 들어가야 한다.

### guard(또는 메인 세션의 관찰)에서 받는 것 (What scribe receives from guard)

위임에는 다음이 들어 있다.
- **갈래(Flavor)**: `verification_failure` 또는 `spec_gap`
- **패턴**: 무엇을 어떻게 놓쳤는가
- **맥락**: 드러났을 때 무엇을 하고 있었는가
- **포착 신호**: 더 일찍 잡았을 구체적인 검사나 신호(검증 실패), 또는 명세가 다뤘어야 할 경우의 종류(명세 빈틈)

### scribe가 하는 일 (What scribe does)

1. **패턴을 일반화한다**: 구체적인 사건을 일반적인 형태의 설명으로 바꾼다. 재사용을 막는 프로젝트 고유 식별자는 지운다.
2. **계열 확인 (귀납)**: 일반화한 패턴을 `discipline/hints.md`, `$SONMAT_MEMORY_DIR/hint-evidence.md`(힌트마다 근거 함정 목록, 있을 때), 그리고 `$SONMAT_MEMORY_DIR`에 있는 기존 `trap_*` / `insight_*` 파일과 비교한다. 계열이란 같은 실패 모양, 곧 같은 잘못된 추론을 말한다. 같은 도구나 같은 프로젝트를 뜻하지 않는다. 결과는 정확히 하나로 정한다.
   - **이미 다루는 힌트가 있다** → 항체 실패다. 힌트가 있었는데 발동하지 않았다. 먼저 그 실패를 코드(훅·가드·도구)로 막을 수 있는지 본다. 막을 수 없으면 힌트의 포착 신호나 발동 조건을 고치자고 제안한다. 사건은 `hint-evidence.md`의 그 힌트 항목에 더하고, `hints.md`에는 사례 목록을 쌓지 않는다. 사건이 별개의 포착 신호를 더할 때만 새 함정 파일을 쓴다.
   - **독립된 두 번째 사례인데 아직 힌트가 없다** → 승격을 제안한다. 행선지는 이 순서로 고른다. (가) 특정 명령·파일·이벤트에서 기계적으로 가려낼 수 있으면 코드를 제안한다. 여러 하네스에서 같은 행동이 일어나면 하네스 훅보다 git 훅이나 도구 자체를 고른다. 코드가 생기면 힌트는 두지 않는다. (나) 판단이 필요하고 포착 신호가 구체적이면 알맞은 `hints.md` 절에 힌트 하나를 둔다. 힌트에는 규칙, 포착 신호, 할 일, 대표 예 하나만 적고 근거 함정 이름은 `hint-evidence.md`에 적는다(없으면 만든다). (다) 특정 작업에서만 필요하면 그 작업이 읽는 파일(`discipline/spec.md` 등)에 둔다. `hints.md`가 8,000자를 넘게 되면 새 힌트를 더하지 말고 기존 힌트와 합치거나 더 큰 원칙으로 흡수한다. 함정 파일은 증거로 남는다. 독립이란 세션이 다르고 드러난 곳(프로젝트, 도구, 시스템)도 다르다는 뜻이다.
   - **계열이 없다** → 새 함정을 기록한다(3~5단계).

   이 단계가 있는 까닭: 함정 메모리는 행동하는 순간에 읽히는 경로가 없지만, `hints.md`는 모든 세션이 불러온다. 설정 출처에 관한 함정이 기록돼 있었는데도 아무것도 그것을 떠올려 주지 않아 2주 뒤에 같은 일이 되풀이됐다. 다만 문서 경고만으로는 재발을 못 막은 계열도 있어서(기록된 경고가 있는데도 여섯 번 재발한 `pkill -f` 자기매칭은 셸 가드로 막았다), 힌트는 코드로 막을 수 없는 판단에만 쓴다. 코드 가드가 생긴 힌트는 지우거나 남은 판단 부분만 남긴다. 승격 제안과 개정 제안은 다른 함정 제안처럼 동기적으로 진행하고, 힌트 변경은 sonmat 릴리스(`VERSIONING.md`)로 배포한다.
3. **범위를 고른다**:
   - 프로젝트에만 해당하는 교훈 → 프로젝트별 scribe 디렉터리(파일 위치 참조)의 `{name}.md`
   - 범용 교훈(여러 프로젝트에 적용된다) → `$SONMAT_MEMORY_DIR`(기본값 `~/.sonmat/memory/`)의 `trap_{name}.md`
4. 메모리 기록을 동기적으로 **제안한다**.

   ```
   💡 Novel trap detected: {short title}
      Record as {project | universal} memory? [Yes / No / Edit first]
   ```

5. 사용자가 확인한 뒤에만 다음 형식으로 **쓴다**.

```markdown
# Trap: {title}

## Pattern
{What went wrong and why it wasn't caught}

## Lesson
{What to do differently — name the specific check or signal that would have caught this trap earlier}

## Applies to
{When this trap is likely to recur}
```

6. **명세 개정 제안 (flavor = `spec_gap`이고 프로젝트에 `sonmat.spec_awareness: enabled`인 `docs/specs/`가 있을 때만)**: 두 조건이 모두 맞으면 함정 메모리를 쓴 뒤 기록만 남기지 말고 후속 명세를 만들지 제안한다. ADR `2026-04-26-spec-evolution-loop.md`(T2-C)를 구현한 것이다. 조건은 다음과 같다.

   - 프로젝트에 `docs/specs/` 디렉터리가 있고, 그 안의 `_index.md`가 `sonmat.spec_awareness: enabled`를 선언해야 한다. 없으면 이 단계를 통째로 건너뛴다. Stage 0 프로젝트는 함정 메모리에만 기록한다.
   - 새 함정 위임에 `flavor: spec_gap`이 실려 있어야 한다(곧, 기존 규율의 검증 실패가 아니라 행동이 명세가 다루는 범위 밖에서 일어났다).
   - 빈틈과 관련된 기존 명세를 분명히 짚을 수 있어야 한다. 빈틈이 어느 기존 명세에도 대응하지 않으면 건너뛴다. 그것은 "새 명세가 필요한" 영역이고, scribe가 아니라 사용자가 시작할 일이다.

   세 조건이 모두 맞으면 동기적으로 제안한다.

   ```
   💡 Spec gap detected: {pattern}
      Maps to: {existing spec id or section}
      Catch-signal: {what spec clause would have caught this}

      Propose amendment via successor spec? [Yes / No log only / Edit first]
   ```

   `Yes`이면: 프로젝트의 명세 템플릿(프로젝트 템플릿이 없으면 sonmat 기본값 `templates/spec-template.md`)으로 `docs/specs/SPEC-{YYYYMMDD}-{slug}.md`에 후속 명세 초안을 만든다. `supersedes: {original-spec-id}`를 넣는다. 원래 명세의 frontmatter에 `superseded-by: {new-spec-id}`를 더하고, `status: archived`는 사용자가 완전히 대체한다고 확인한 뒤에만 제안한다(원래 명세를 살려 두는 부분 개정과 구분한다).

   `Edit first`이면: 초안을 보여 주고 사용자가 고치게 한 뒤에 쓴다.

   `No log only`이면: 후속 명세를 만들지 않는다. 함정 메모리 기록으로 충분하다.

   **폐기 의례 자동 발동**: 사용자가 완전 대체를 받아들이면(원래 명세 `status: archived`) `discipline/spec.md`의 「폐기에는 종료 의례를 둔다」 항목에 따라 종료 날짜와 분기 방지 선언을 묻는다. 이 메타데이터 없이 `archived`를 쓰지 않는다.

   **LEARN journal 항목 (Yes/No/Edit와 상관없이 항상)**: `journal.md`에 덧붙인다.

   ```markdown
   ## YYYY-MM-DD [hostname] — Spec gap AAR
   - Trigger: {what was outside spec}
   - Maps to: {existing spec id or "no clear mapping"}
   - Catch-signal: {what spec clause would have caught it}
   - Decision: {amendment generated SPEC-XXX | log only | edited then generated}
   - Reasoning: {1-line justification}
   ```

   이것이 LPS 5대화의 LEARN 단계다(`docs/research/architecture-methodology-and-spec-discipline.md` A4). 개정안을 만들지 않았을 때도 기록하는 까닭은, 미룬 결정 자체가 나중 회고에 쓸 자료이기 때문이다.

7. **GitHub 피드백 보내기 (선택)**: 기록한 뒤 sonmat 리포에 GitHub 이슈로 올릴지 제안한다. 전적으로 선택 사항이다. 사용자가 거절하면 메모리 기록은 로컬에만 남는다.

   ```
   💬 This trap could help other sonmat users. Submit to GitHub?
      Your privacy is respected — only the abstracted pattern is sent,
      no conversation content or personal data.

      Below is EXACTLY what will be sent:

      Title: Trap: {title}
      Pattern: {abstracted pattern}
      Discovered via: {method}

      [Yes / No / Edit first]
   ```

   사용자가 승인하면: `gh issue create --repo jun0-ds/sonmat --template trap-report.md`.
   사용자가 고치고 싶어 하면: 이슈 본문 전체를 보여 주고 고치게 한 뒤 올린다.
   **내용을 먼저 보여 주지 않고 절대 보내지 않는다.**


**guard 쪽에서는 이것이 선택 사항이 아니다.** guard가 새 함정을 감지하고도 scribe에 위임하지 않으면 검증과 기록이 이어지는 고리가 끊긴다. 메모리 체계는 미리 정의해서가 아니라 실제 작업을 거치며 자라고, 실제 작업을 기록으로 바꾸는 단계가 scribe다.

---

## 진행 관리 (Progress Management)

예전 plan 스킬에서 옮겨 왔다.

### scribe가 맡는 일 — 백그라운드 (What scribe handles)
- `progress.md`에서 끝난 작업·단계에 체크 표시
- 완료 시각 추가
- `progress: {item} done`으로 커밋

### 포그라운드에 남는 일 (What stays in foreground)
- `progress.md` 만들기(사용자 결정)
- 새 마일스톤·단계 추가(구조 변경 = 루프 L3)
- 순서나 우선순위 바꾸기(사용자 결정)

### 마일스톤 기획 — 예전 plan 스킬 (Milestone planning)
마일스톤 수준의 기획("로드맵 만들어 줘", "마일스톤 재구성해 줘")은 이제 루프의 L3 에스컬레이션이 맡는다. 예전 plan 스킬의 기획 질문은 L3로 에스컬레이션할 때 루프의 [Plan] 단계로 흡수됐다.

---

## 파일 위치 (File Locations)

sonmat 상태는 **`.claude/` 밖에** 둔다. Claude Code는 모든 `.claude/` 디렉터리를 편집 보호하기 때문이다(Edit/Write마다 묻고, `bypassPermissions`가 아니면 끌 수 없다). 위치는 다음과 같이 정한다.

- **프로젝트별 scribe 디렉터리**(아래 `<scribe-dir>`) = `$SONMAT_PROJECTS_BASE/<slug>`(기본값 `~/.sonmat/projects/<slug>`). `<slug>`는 cwd 경로의 `/`를 `-`로 바꾼 값이다(예: `/home/u/proj` → `-home-u-proj`). Claude Code 자체의 `~/.claude/projects/` 방식을 따른 것이다.
- **범용 메모리** = `$SONMAT_MEMORY_DIR`(기본값 `~/.sonmat/memory/`).
- session-start hook이 이 디렉터리들을 만들고, 예전 위치인 `.claude/sonmat/`와 `~/.claude/sonmat/memory/`의 내용을 자동으로 옮긴다. **대체 경로**: `<scribe-dir>`가 비어 있는데 예전 `.claude/sonmat/`에 내용이 있으면 예전 경로를 읽는다.

| 파일 | 위치 | 수명 |
|------|----------|-----------|
| `bridge-note.md` | `<scribe-dir>/bridge-note.md` | 위임할 때마다 덮어쓴다 |
| `journal.md` | `<scribe-dir>/journal.md` | 덧붙이기만 하고, 50개 항목이 차면 보관한다 |
| `journal-archive.md` | `<scribe-dir>/journal-archive.md` | 장기 보관 |
| `progress.md` | 프로젝트 루트 | 함께 관리한다(포그라운드가 만들고 scribe가 갱신한다) |
