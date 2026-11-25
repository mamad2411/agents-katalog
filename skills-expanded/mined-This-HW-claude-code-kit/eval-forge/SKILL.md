---
name: eval-forge
description: Turn an observed agent defect into a machine-checkable eval scenario, generated and self-validated in one step. Use after a defect lands in the feedback ledger, or before changing an agent definition that has no eval coverage. Trigger with /eval-forge.
model: sonnet
effort: medium
---

# Eval Forge — 결함을 회귀 게이트로 굳히기

`/self-improve`의 HARD-GATE는 **eval 커버리지가 있는 대상에서만** 이중 게이트다.
실제 커버리지는 33개 에이전트 중 소수뿐이라, 대부분의 정의 파일 수정은
"사용자 승인 단일 게이트"로 퇴화한다. 스킬이 그 한계를 정직하게 고지하고는 있지만,
**고지는 해결이 아니다.** 이 스킬은 커버리지를 늘리는 비용을 낮춰 그 구멍을 메운다.

> **적용 범위**: 이 스킬은 `evals/` 하네스(`evals/run.py`)가 있는 프로젝트 —
> 즉 **kit 레포 자체의 개발**에서 동작한다. 그 하네스가 없는 소비자 프로젝트에서는
> 스크립트가 exit 2(SKIPPED)로 정직하게 멈춘다. `/self-improve`·`/native-watch`와 같은
> kit-개발용 스킬 계열이다.

## 사용 시점

| 상황 | 왜 |
| --- | --- |
| ledger에 에이전트 행동 결함이 올라왔다 | 같은 결함이 다시 나면 기계가 잡게 만든다 |
| eval 커버리지 없는 에이전트의 정의를 고치려 한다 | 고치기 **전에** 안전망을 깐다 (없으면 self-improve가 게이트 없이 돈다) |
| 리뷰형 에이전트가 결함을 놓치는 걸 목격했다 | 거짓 음성은 eval의 1순위 표적이다 |

## 절차

### 1. 대상과 실패 형태를 확정한다 [건너뛰기 금지]

"무엇을 놓쳤는가"가 아니라 **"통과/실패를 무엇으로 판정할 것인가"**를 먼저 정한다.
판정 기준 없이 시나리오를 만들면 채점 불가능한 자산이 트리에 남는다.

- 리뷰/스캔형 → 출력에 **반드시 등장할 표현**(OR 묶음)과 **등장하면 실패인 표현**
- 수정/구현형 → `pytest_green` + 필요하면 `file_contains`

### 2. 픽스처를 준비한다

결함을 심은 최소 코드. 아래는 **강제 규칙**이다 (러너가 거부한다):

- `conftest.py` 금지 — 채점 시 임의 코드 실행 통로 (있으면 생성기가 제거한다)
- **모듈 스코프(=import 시 실행되는 위치)에서 위험 호출 금지.** 러너가 AST로 판정하며,
  대상은 최상위 문장뿐 아니라 **클래스 본문·데코레이터 표현식·함수 기본 인자 값**까지다
  (전부 import 시 실행된다). 함수/메서드 **본문**은 실행되지 않으므로 자유롭다 —
  결함 코드는 함수 안에 두면 된다.
  - 차단: `os.system`·`os.popen`·`os.remove` 류, `subprocess.*`, `socket.*`, `requests.*`,
    `shutil.rmtree`, `eval`/`exec`/`__import__`/`getattr`/`setattr`, `importlib.*`
  - 차단: 별칭·재바인딩·`from X import *` 우회 (`import os as x`, `f = os.system`,
    `getattr(os,"system")` 모두 잡힌다)
  - **허용**: `os.path.join`, `shutil.which`, `urllib.parse.urlparse`, `open`, `json.loads`
    — 모듈 스코프에서 데이터를 읽는 정상 fixture를 막지 않는다
  - 파싱 불가(구문 오류·NUL 바이트)도 **거부**한다 — 검사 불가를 통과로 삼지 않는다
- 시나리오 루트에 `.py` 금지 — 코드는 `fixture/` 안에만

그리고 **커밋되는 자산임을 잊지 마라**: 보안 시나리오의 가짜 자격증명은 저엔트로피로
쓴다. 고엔트로피 가짜 시크릿은 gitleaks를 트립시켜 **CI가 그 eval 자산 자체를 막는다.**
점검 대상은 "소스에 자격증명을 상수로 박았다"는 사실이지 값의 엔트로피가 아니다.

### 3. 생성 (즉시 자기검증된다)

```bash
python3 scripts/eval-forge.py --agent <name> --id <kebab-id> \
  --task-file <과제.md> --fixture <파일 또는 디렉토리> \
  --must-mention "표현a,표현b" \
  --must-mention "다른 발견의 표현c,표현d" \
  --rubric "무엇을 판정하는가 (opt-in judge용)"
```

**`--must-mention`은 반복 지정한다.** 묶음 하나가 OR, 묶음끼리는 AND다.
발견해야 할 결함이 둘인데 한 덩어리로 뭉치면 **하나만 찾고도 green**이 된다 —
그건 게이트가 아니다.

`--must-not-say`를 생략하면 거짓 음성 기본 목록("문제 없음", "no issues found" 등)이
자동으로 들어간다. `--no-default-negatives`로만 끌 수 있고, 끄면 assertion이 0개가
되어 생성이 거부될 수 있다 (채점 불가능한 시나리오 = fail-closed).

`--from-ledger F-NNN`으로 근거를 붙이면 ledger 행이 **인용 블록 + 방어 프레이밍**과
함께 `task.md`에 실린다. 그 텍스트는 데이터이지 지시가 아니다.

### 4. 결과 확인 [건너뛰기 금지]

| exit | 의미 | 대응 |
| --- | --- | --- |
| 0 | 생성 + `run.py --validate` 통과 | 커버리지 확인 후 커밋 |
| 1 | 중복 ID / 미존재 에이전트 / 입력 오류 / 검증 실패 | **생성물은 롤백됐다** — 원인 수정 후 재실행 |
| 2 | SKIPPED — evals 하네스 없음 | 0으로 위장하지 말 것 |

생성은 **원자적**이다. 검증이 깨지면 반쯤 만들어진 시나리오가 남지 않는다 —
남으면 `verify-done.sh §10`을 영구히 막는다.

### 5. baseline은 건드리지 않는다 [건너뛰기 금지]

새 시나리오는 **다음 릴리스의 `--baseline`에서 처음 기준선을 얻는다.**
지금 baseline을 갱신하면 "아직 한 번도 통과한 적 없는 시나리오"가 기준선이 되어
회귀 검출이 무의미해진다.

### 6. 실제 행동 eval은 별도다

`--validate`는 **스키마 검증**일 뿐이다. 에이전트가 실제로 통과하는지는
`./scripts/run-evals.sh --agent <name> --scenario <id>` — API 비용이 들며
릴리스 전 게이트다. 스키마 green을 "에이전트가 통과했다"로 보고하지 마라
(false-green 금지, v2.9.3 교훈).
