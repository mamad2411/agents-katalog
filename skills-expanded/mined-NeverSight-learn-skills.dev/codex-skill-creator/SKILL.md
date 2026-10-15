---
name: codex-skill-creator
description: 새 스킬을 만들고, 기존 스킬을 수정하고 개선하며, 스킬 성능을 측정합니다. 사용자가 스킬을 처음부터 만들고 싶어 하거나, 기존 스킬을 편집 또는 최적화하려 하거나, eval을 실행해 스킬을 테스트하려 하거나, 분산 분석이 포함된 벤치마크를 돌리거나, 더 정확하게 트리거되도록 스킬 설명을 최적화하려 할 때 사용하세요.
---


새 스킬을 만들고, 테스트하고, 반복적으로 개선할 수 있는 스킬이여야 한다.

## 큰 흐름

- 스킬이 무엇을 해야 하는지, 언제 트리거되야 하는지, 어떤 결과를 내야 하는지 정할 수 있어야 한다.
- SKILL.md 초안 작성.
- 현실적인 테스트 프롬프트를 만들고, AI(Codex, Claude, Gemini, 기타 LLM) 가 스킬 지침을 참고해 작업을 수행했을 때 기대한 흐름이 나오는지 확인.
- 테스트시 결과를 정량적으로 평가할 수 있게 도와야 한다.
- 사용자의 피드백과 벤치마크에서 드러난 큰 문제를 바탕으로 스킬을 다시 작성한다.
- 만족할때까지 반복
- description을 다듬어 AI가 이 스킬을 필요할떄 트리거 가능하고, 불필요할 때 트리거하지 않도록 명확한 형태로 정리한다.

---

## 좋은 스킬 철학

- 단순 지식 저장소가 아닌 재사용 가능한 절차 지식 패키지
- 얕게 시작하되 필요하면 깊이 로딩 가능한 동적 context
- 넓은 만능형보다는 좁은 범위의 문제를 효율적으로 해결 가능해야함.( 어떤 특정한 작업을 더 빠르고, 더 일관되게, 더 안전하게 수행)
- 다른 skill과 호환이 잘 되게 설계되야함. 좋은 스킬은 좁고 깊은 스킬의 서로간의 상호작용이 효율적이여야 함.
- 언제 trigger되고 언제 trigger가 안되야 하는지 분명해야 한다.
- 적은 설명으로도 목표(목적)에 맞는 절차를 재현할 수 있는 운영 패키지여야 한다.(적은 설명으로도 예측 가능한 일관성)
- SkILL.md는 skill 본문에 충실하고, 언제 사용할지, 사용 안할지에 대한 Skill Trigger는 description에만 있어야함.(책임이 확실해야 함)

---

## 사용자와 소통

이 스킬은 작업 이전에 사용자 요구사항으로부터 스킬을 작성 또는 재 작성시에 필요한 맥락을 명확히 얻어야 한다. 예를 들면 좋은 스킬을 작성하기 위한 맥락 수집을 명확히하며, 사용자의 스킬 요구사항에 대해 좋은 스킬을 작성할 수 있게끔 비판적으로 대화를 해야 한다. 

소통할 때 중요한 점은 확신이 없다면 용어를 짧게 풀어서 설명해도 되고, 이해할지 애매하면 간단한 정의를 덧붙여도 좋다. 중요한것은 전문 용어를 많이 쓰는 것이 아니라, 사용자가 지금 결정을 내리는 데 필요한 정보만 정확하게 전달하는 것이다.

---

## 스킬 생성하기

### 의도 파악
먼저 사용자의 의도를 이해해라. 현재 대화 자체에 이미 스킬로 만들고 싶은 워크플로가 담겨 있을 수도 있다. 예를 들면 사용자가 이걸 스킬로 만들어줘 라고 말할 수 있다. 그런 경우에는 먼저 대화 기록에서 답을 최대한 추출한다. 어떤 도구를 썻는지, 단계 순서(workflow)가 어땟는지, 사용자가 어떤 수정을 요구했는지, 어떤/출력 형식이 관찰됬는지 살펴보면 된다. 비어 있는 부분만 사용자에게 물으면 되고, 다음 단계로 가기 전에 확인 받는 편이 좋다.

1. 좋은 스킬인지 아닌지 판단하고 아쉬운 점 또는 위험하거나 불필요한 부분이 있다면 설명하고 확인
2. 스킬이 제대로 동작하는지 확인하기 위한 테스트 케이스를 만들지

### 인터뷰와 리서치

엣지 케이스, 입력/출력 형식, 예시 파일, 성공 기준, 의존성에 대해 먼저 적극적으로 질문하세요. 이 부분이 정리되기 전에는 테스트 프롬프트를 쓰지 마세요.

### SKILL.md 작성하기

사용자 인터뷰 내용을 바탕으로 다음 요소를 채우세요.

- **name**: 스킬 식별자
- **description**: 언제 트리거되는지, 무엇을 하는지. 이것이 스킬을 떠올리게 하는 가장 중요한 단서다. 스킬이 무엇을 하는지뿐 아니라, 어떤 상황에서 써야 하는지와 어떤 경계 사례에서 특히 유용한지도 함께 넣어야 한다. "언제 써야 하는지" 정보는 본문이 아니라 description에 넣어야 한다. 모호한 일반론보다, 사용자 의도와 작업 맥락이 드러나는 짧고 선명한 설명이 좋다.
- **compatibility**: 필요한 도구나 의존성(선택 사항이며, 실제로는 드물게만 필요하다)
- **나머지 스킬 본문 :)**

### 스킬 작성 가이드

#### 스킬의 구성

```text
skill-name/
├── SKILL.md (필수)
│   ├── YAML frontmatter (name, description 필수)
│   └── Markdown 지침
└── Bundled Resources (선택)
    ├── scripts/    - 결정적이거나 반복적인 작업을 처리하는 실행 코드
    ├── references/ - 필요할 때만 읽어들이는 문서
    └── assets/     - 출력에 사용하는 파일(템플릿, 아이콘, 글꼴 등)
```

#### 점진적 공개

스킬은 3단계 로딩 구조를 사용한다.

1. **메타데이터** (name + description) - 항상 컨텍스트에 들어간다(약 100단어)
2. **SKILL.md 본문** - 스킬이 트리거되면 컨텍스트에 들어간다(500줄 이하 권장)
3. **번들 리소스** - 필요할 때만 사용한다(길이 제한 없음, 스크립트는 읽지 않고 실행 가능)

이 단어 수/줄 수는 대략적인 기준일 뿐이고, 필요하다면 더 길어져도 괜찮다.

**핵심 패턴:**

- SKILL.md는 500줄 이하를 권장한다. 이 한도에 가까워지면 계층을 한 단계 더 나누고, 다음에 무엇을 읽어야 하는지 명확히 안내해라.
- 참조 파일은 언제 읽어야 하는지까지 포함해서, SKILL.md에서 분명하게 가리켜라.
- 큰 참조 파일(300줄 이상)에는 목차를 넣는 것이 좋다.

**도메인 구성**: 하나의 스킬이 여러 도메인이나 프레임워크를 지원한다면, 변형별로 나누어 정리한다.

```text
cloud-deploy/
├── SKILL.md (워크플로 + 선택 기준)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

LLM은 필요한 참조 파일만 읽는다.

#### 놀라움이 없어야 한다는 원칙

당연한 이야기지만, 스킬에는 악성코드나 익스플로잇 코드, 또는 시스템 보안을 해칠 수 있는 내용이 들어가면 안 된다. 스킬 내용은, 설명된 사용자 의도 기준으로 봤을 때 놀랍거나 숨겨진 동작을 해서는 안 된다. 사용자를 오도하는 스킬, 무단 접근이나 데이터 유출 등 악의적 목적을 돕는 스킬 요청에는 동조하지 마라. 다만 "XYZ처럼 역할극해 줘" 정도는 괜찮다.

#### 작성 패턴

지침은 가급적 명령형으로 쓰세요.

**출력 형식 정의**는 이런 식으로 할 수 있습니다.

```markdown
## 보고서 구조
항상 정확히 이 템플릿을 사용하세요:
# [제목]
## 요약
## 핵심 발견
## 권장 사항
```

**예시 패턴**도 유용하다. 다음 같은 형식을 쓸 수 있다. 다만 예시에 "Input"과 "Output"이 함께 있을 때는 약간 다르게 구성해도 된다.

```markdown
## 커밋 메시지 형식
**예시 1:**
입력: JWT 토큰 기반 사용자 인증 추가
출력: feat(auth): implement JWT-based authentication
```

### 글쓰기 스타일

무조건 따라야 하는 규칙을 늘어놓기보다는, 왜 중요한지 모델이 이해하도록 설명해라. 마음 이론을 활용하고, 스킬을 너무 특정 예시에 과적합시키지 말고 일반적으로 유용하도록 만든다. 먼저 초안을 쓴 뒤, 한 걸음 물러나 새 눈으로 다시 보고 개선해라.

### 테스트 케이스

스킬 초안을 쓴 뒤에는, 실제 사용자가 정말 이렇게 말할 법한 2~3개의 현실적인 테스트 프롬프트를 만든다. 사용자에게 공유하면서, 예를 들면 이런 식으로 말하면 됩니다. 정확히 같은 문구일 필요는 없다. "먼저 이런 테스트 케이스를 돌려 보고 싶은데요. 이 방향이 맞을까요, 아니면 더 추가하고 싶은 게 있을까요?" 그런 다음 실행해라.

테스트 케이스는 `evals/evals.json`에 저장해라. 아직 assertion은 쓰지 말고, 프롬프트만 먼저 넣는다. assertion은 다음 단계에서 실행이 진행되는 동안 작성하면 된다.

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "사용자 작업 프롬프트",
      "expected_output": "기대 결과 설명",
      "files": []
    }
  ]
}
```

전체 스키마(나중에 추가할 `assertions` 필드 포함)는 `references/schemas.md`를 참고하세요.

## 테스트 케이스 실행과 평가

이 섹션은 하나의 연속된 흐름이다. 중간에서 멈추지 마라. `/skill-test`나 다른 테스트용 스킬은 사용하면 안된다.

결과는 스킬 디렉터리와 형제 관계인 `<skill-name>-workspace/`에 저장한다. 워크스페이스 안에서는 반복 차수별로(`iteration-1/`, `iteration-2/` 등) 정리하고, 각 테스트 케이스마다 디렉터리를 따로 둔다(`eval-1/`, `eval-2/` 등). `eval` 디렉터리 이름은 계속 `eval-N` 형식을 유지하고, 사람이 읽는 설명적인 이름은 `eval_metadata.json`의 `eval_name`에 넣으세요. 이 구조를 한 번에 전부 만들지는 말고, 진행하면서 필요한 디렉터리만 생성하세요.

### 1단계: 제한된 rolling queue로 `codex exec` pair 실행하기

실행의 최소 단위는 `eval × config × run`이다. run 하나는 `codex exec` 프로세스 1회에 대응한다. 기본 운영 방식은 준비된 eval들을 **bounded rolling queue**로 돌리는 것이다. iteration 전체의 모든 eval을 한꺼번에 띄우지는 말고, 준비가 끝난 eval pair부터 백그라운드로 넣되 활성 `codex exec` 프로세스 수는 **절대 6개를 넘기지 마라**.

canonical 구조는 다음과 같습니다.

```text
iteration-N/
  eval-0/
    eval_metadata.json
    with_skill/
      run-1/
        outputs/
        timing.json
        grading.json
    without_skill/
      run-1/
        outputs/
        timing.json
        grading.json
```

config 이름은 기본적으로 `with_skill`과 `without_skill`를 사용한다. 기존 스킬을 개선하는 경우 baseline config는 `old_skill`을 사용하세요.

기본 실행 정책은 config당 1회, 즉 `run-1`만 실행하는 것이다. 사용자가 반복 실행을 명시적으로 요청한 경우에만 `run-1..run-N`으로 확장할 수 있고, 상한은 config당 최대 3회(`run-1..run-3`)다.

병렬 규칙은 이제 **eval 간 rolling queue** 기준으로 적용한다. 공정한 비교를 위해 같은 eval의 `with_skill/run-K`와 baseline(`without_skill/run-K` 또는 `old_skill/run-K`)은 항상 같은 배치로 시작하세요. 기본값인 `run-1`만 돌릴 때는 eval 하나당 `codex exec`가 2개이므로, 최대 3개의 eval을 동시에 진행할 수 있다. 즉 `eval-0`, `eval-1`, `eval-2`의 run-1 pair를 함께 백그라운드로 시작해도 된다. 어떤 eval pair가 끝나면 그 슬롯을 즉시 다음 eval pair로 채워 rolling queue를 유지하세요.

여러 run을 요청받았다면 큐 크기를 자동으로 줄여라. 핵심 규칙은 항상 같다. **동시에 살아 있는 `codex exec` 프로세스 총합이 6을 넘으면 안 된다.** 계산은 대략 `동시 eval 수 × 각 eval에서 동시에 돌리는 run index 수 × 2(config 수)`로 생각하면 된다. 예를 들어 기본 `run-1`만 돌리면 `3 × 1 × 2 = 6`이라 eval 3개 동시 실행이 가능하지만, 같은 eval에서 `run-1`과 `run-2`를 동시에 띄우기 시작하면 큐 폭을 그만큼 줄여야 한다. 어떤 경우에도 with-skill 실행을 먼저 몰아서 돌리고 baseline을 나중에 따로 돌리지 마세요. 같은 run index의 비교군은 같은 시점에 출발해야 합니다.

권장 큐 운영 순서는 다음과 같다.

- 준비가 끝난 eval부터 최대 3개까지 queue에 넣고 `with_skill/run-1`과 baseline `run-1`을 함께 시작한다.
- 활성 `codex exec` 수가 6보다 작은 상태가 되면, 준비된 다음 eval pair를 즉시 백그라운드로 추가한다.
- 어떤 eval의 pair가 끝나면 그 eval의 `timing.json`과 실행 기록을 먼저 저장하고, assertion이 준비되어 있으면 grading 대상으로 넘긴다.
- grading이나 assertion 작성 때문에 queue를 비워 두지 마라. `codex exec` 슬롯이 남으면 다음 eval을 먼저 넣고, 사람이 하는 정리 작업은 그 사이에 진행한다.

**격리 원칙**

- 각 run은 자기 전용 작업 디렉터리에서 실행하세요. 보통 `<workspace>/iteration-<N>/eval-<ID>/<config>/run-<RUN>/` 자체를 작업 디렉터리로 써도 된다.
- 각 run 디렉터리에는 실행 전 `run_prompt.md`를 저장하세요. 이 파일이 그 run의 정확한 입력 증거다.
- `with_skill` 실행에는 benchmark 대상 스킬이 현재 run의 작업 디렉터리 안 `.agents/skills/` 아래에서 보이도록 준비하세요. 가장 단순한 방법은 benchmark 대상 스킬 디렉터리를 복사해 두는 것이다.
- baseline(`without_skill`)에는 benchmark 대상 스킬을 `.agents/skills/`에 두지 마세요. 프롬프트에도 benchmark 대상 스킬의 이름, description, path, 참조 파일 경로를 직접 넣지 않는 편이 좋다.
- 기존 스킬 개선의 `old_skill` baseline은 예외다. 이 경우에는 **스냅샷된 이전 스킬 path만** `.agents/skills/` 아래에 두고, 현재 편집 중인 스킬 path는 넘기지 않는다.

**With-skill 실행 템플릿**

각 run 디렉터리 안에서 다음 파일을 준비하세요.

- `run_prompt.md` — `codex exec`에 그대로 넣을 프롬프트
- `outputs/` — 최종 결과물을 저장할 디렉터리
- 선택 사항: `run_provenance.json` — 실행 메타데이터 기록 파일

`run_prompt.md`는 대략 이런 형태면 된다.

```text
다음 작업을 실행하세요.

- 작업: <eval prompt>
- 입력 파일: <eval files if any, or "none">
- 출력 저장 위치: <absolute path to .../with_skill/run-<RUN>/outputs/>
- 저장해야 할 결과물: <사용자가 중요하게 보는 것 — 예: ".docx 파일", "최종 CSV">
- 실행 요약 저장 위치: <absolute path to .../with_skill/run-<RUN>/transcript.md>
- 선택적 provenance 저장 위치: <absolute path to .../with_skill/run-<RUN>/run_provenance.json>

추가 규칙:
- 산출물은 지정된 `outputs/` 아래에 저장하세요.
- 실행 중 참고한 핵심 파일, 사용한 스크립트, 남은 불확실성을 `transcript.md`에 짧게 정리하세요.
- `run_provenance.json`을 쓴다면 `executor`, `configuration`, `baseline_type`, `skill_path_requested`, `prompt_path`, `command`를 기록하세요.
```

이 스킬에서 benchmark나 eval 목적으로 실행하는 `codex exec` 호출은 모델을 항상 `gpt-5.4-mini`로 고정하세요. 실행 명령은 보통 다음 형태면 충분합니다.

```bash
codex exec - \
  --model gpt-5.4-mini \
  --cd <absolute path to run-dir> \
  --sandbox workspace-write \
  --skip-git-repo-check \
  --json \
  < <absolute path to run-dir/run_prompt.md> \
  > <absolute path to run-dir/codex-events.jsonl>
```

`codex-events.jsonl`은 선택 사항이지만 남겨 두면 timing, usage, 실패 원인, 격리 상태를 사후 점검할 때 도움이 된다.

**Baseline 실행**(프롬프트의 작업 내용은 with-skill run과 동일하지만, skill 구성은 상황에 따라 달라집니다):

- **새 스킬을 만드는 경우**: 스킬 없이 실행합니다. 같은 프롬프트를 사용하고, benchmark 대상 스킬을 `.agents/skills/`에 두지 않은 상태에서 `without_skill/run-<RUN>/outputs/`에 저장하세요. benchmark 대상 스킬의 이름/description/path를 prompt에 직접 넣지 마세요.
- **기존 스킬을 개선하는 경우**: 이전 스킬 버전을 baseline으로 사용합니다. 편집 전에 스킬을 스냅샷으로 저장하세요(`cp -r <skill-path> <workspace>/skill-snapshot/`). baseline run은 그 스냅샷만 `.agents/skills/` 아래에 두고 실행하세요. 결과는 `old_skill/run-<RUN>/outputs/`에 저장한다.

각 테스트 케이스마다 `eval_metadata.json`을 써라(assertion은 지금 단계에서 작성하지 않는다). `eval` 디렉터리 이름은 `eval-0` 같은 형식을 유지하고, 무엇을 검증하는지 드러나는 설명적인 이름은 `eval_name` 필드에 넣으세요. 이 iteration에서 새 프롬프트를 추가하거나 수정했다면, 새 eval 디렉터리마다 파일을 다시 만들어야 합니다. 이전 iteration의 파일이 자동으로 이어진다고 가정하지 마세요.

`eval_metadata.json`에는 `prompt`뿐 아니라 해당 eval이 참조하는 입력 파일 목록도 함께 넣어 두세요. `files`는 `evals/evals.json`의 같은 항목과 동일해야 하며, 리뷰어가 입력 파일을 보여 주거나 실행을 다시 재현할 때 기준이 됩니다.

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name-here",
  "prompt": "사용자의 작업 프롬프트",
  "files": [],
  "assertions": []
}
```

가능하다면 각 run이 끝난 직후 `run_provenance.json`에 실제 실행 명령, prompt 경로, configuration 이름을 남겨 두세요. 나중에 baseline 오염이나 skill 로딩 여부를 점검할 때 도움이 된다.

### 2단계: 실행이 돌아가는 동안 assertion 초안 만들기

그냥 queue가 비거나 현재 실행 중인 eval들이 끝나기만 기다리지 마세요. 이 시간을 생산적으로 써야 한다. 기본 패턴은 다음과 같다. `codex exec`는 백그라운드에서 rolling queue로 계속 돌리고, 그 동안에는 각 테스트 케이스에 대한 정량 assertion을 초안으로 만들고, 이미 끝난 eval 중 assertion이 정리된 것은 바로 grading 준비 단계로 넘긴다. 이미 `evals/evals.json`에 assertion이 있다면, 그것들을 검토하고 각각 무엇을 확인하는 기준인지 설명해라.

좋은 assertion은 객관적으로 검증 가능하고, 이름만 읽어도 무엇을 본다는 게 드러나야 합니다. 벤치마크 뷰어에서 한눈에 봤을 때 바로 이해되도록 만드는 것이 좋다. 문체나 디자인처럼 주관적 요소가 핵심인 스킬은 사람이 보는 정성 평가가 더 적합하다. 사람이 판단해야 하는 부분에 assertion을 억지로 만들지 않는다.

초안을 다 만들었다면 `eval_metadata.json`과 `evals/evals.json` 둘 다 업데이트해라. queue 운영 중에는 보통 **실행 중인 eval들에 대한 assertion 작성 -> 막 끝난 eval의 grading 준비 -> 비는 슬롯에 다음 eval pair 투입** 순서로 손을 움직이게 된다. 그리고 뷰어에서 사용자가 무엇을 보게 되는지도 설명한다. 정성적 결과물과 정량적 벤치마크를 각각 어떻게 읽으면 되는지 알려 주면 된다.

### 3단계: 각 실행이 끝나는 즉시 timing 데이터 저장하기

각 `codex exec` 실행 직전에 시각을 기록하고(`executor_start`), 프로세스가 끝나는 즉시 종료 시각을 기록하세요(`executor_end`). 이 둘의 차이로 `duration_ms`, `total_duration_seconds`, `executor_duration_seconds`를 계산해 해당 `run-*` 디렉터리의 `timing.json`에 저장합니다. `codex exec --json` 이벤트 로그나 다른 CLI 출력에서 `total_tokens`를 얻을 수 있다면 함께 저장하고, 얻을 수 없다면 `0` 또는 미기록으로 두어도 된다.

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3,
  "executor_start": "2026-01-15T10:30:00Z",
  "executor_end": "2026-01-15T10:30:23Z",
  "executor_duration_seconds": 23.3
}
```

가능하면 `codex-events.jsonl`이나 다른 실행 로그를 함께 남겨 두세요. timing이나 token 수치를 나중에 검산할 때 도움이 된다. 실행기 자체가 `outputs/execution_window.json`을 쓰게 할 수 있다면 그것도 괜찮지만, 핵심 기준 파일은 여전히 `timing.json`이다.

### 3.5단계: 격리 상태 점검하기

벤치마크가 끝난 뒤에 "with/without이 정말 분리됐는가?"를 따로 확인하세요. pass rate가 같게 나왔을 때 특히 중요합니다.

- `with_skill` transcript에는 스킬을 읽었거나 스킬 path를 사용했다는 흔적이 있는가?
- `without_skill` 쪽 `run_prompt.md`, transcript, report, user notes에는 benchmark 대상 스킬의 이름/path/description이 직접 새어 들어가지 않았는가?
- `run_provenance.json`이 있다면 `executor`, `configuration`, `skill_path_requested`, `baseline_type`, `prompt_path`, `command` 같은 `codex exec` 메타데이터를 확인한다.

가능하면 이 점검 결과를 `isolation_report.md` 같은 메모 파일로 남기세요. baseline 오염 가능성이나 skill 적용 증거 부족이 보이면, 그 iteration의 benchmark 결과는 강한 결론의 근거로 쓰지 않는 편이 좋다.

### 4단계: 채점하고, 집계하고, 뷰어 띄우기

개별 eval의 grading 자체는 전체 iteration 종료 전에도 앞당겨 시작할 수 있다. 다만 최종 `benchmark.json` 집계와 뷰어 생성은 모든 실행과 grading이 끝난 뒤에 진행하세요. 전체 순서는 다음과 같습니다.

1. **각 실행 채점하기** — `agents/grader.md`를 기반으로 grader 서브에이전트를 띄워서 채점한다. grading도 run 단위로 수행하세요. 즉 `with_skill/run-1`, `without_skill/run-1` 같은 각 `run-*` 디렉터리마다 별도의 grader를 생성하고, 각 assertion을 출력 결과에 비춰 평가한 뒤 결과를 해당 `run-*` 디렉터리의 `grading.json`에 저장한다. `grading.json` 안의 expectations 배열은 반드시 `text`, `passed`, `evidence` 필드를 사용해야 한다. `name`/`met`/`details` 같은 다른 이름을 쓰면 안 된다. 뷰어가 이 정확한 필드 이름을 기대한다. 프로그램적으로 검사할 수 있는 assertion이라면 눈으로 보지 말고 스크립트를 작성해 실행해라. 그 편이 빠르고, 신뢰성이 높고, 다음 iteration에도 재사용할 수 있습니다. assertion이 확정된 eval은 iteration 전체가 끝나기를 기다리지 말고 바로 grading해도 된다. 저장이 끝난 뒤 해당 grader 서브 에이전트를 종료한다.

2. **벤치마크로 집계하기** — 집계 스크립트를 실행하세요.

   ```bash
   python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
   ```

   이 스크립트는 각 설정별 pass_rate, time, tokens의 평균과 표준편차, 그리고 차이를 담은 `benchmark.json`과 `benchmark.md`를 생성합니다. 만약 `benchmark.json`을 수동으로 만들게 되면, 뷰어가 기대하는 정확한 스키마는 `references/schemas.md`를 참고하세요.
   각 with_skill 버전은 그에 대응하는 baseline보다 앞에 오도록 정렬하세요.

3. **분석가 시각으로 한 번 더 보기** — 벤치마크 데이터를 읽고, 단순 평균만 보면 놓치기 쉬운 패턴을 짚어 주세요. 무엇을 봐야 하는지는 `agents/analyzer.md`의 "벤치마크 결과 분석" 섹션을 참고하세요. 예를 들어 스킬 유무와 상관없이 항상 통과하는 assertion(구분력이 없음), 분산이 지나치게 큰 eval(플레이키 가능성), 시간/토큰과 품질 사이의 절충 같은 것들입니다.

4. **뷰어 띄우기** — 정성적 결과물과 정량 데이터가 모두 보이도록 뷰어를 생성합니다.

   ```bash
   nohup python <codex-skill-creator-path>/eval-viewer/generate_review.py \
     <workspace>/iteration-N \
     --skill-name "my-skill" \
     --benchmark <workspace>/iteration-N/benchmark.json \
     > /dev/null 2>&1 &
   VIEWER_PID=$!
   ```

   iteration 2 이상에서는 `--previous-workspace <workspace>/iteration-<N-1>`도 함께 넘기세요.

   **Cowork / 헤드리스 환경:** `webbrowser.open()`을 쓸 수 없거나 디스플레이가 없는 환경이라면, 서버를 띄우는 대신 `--static <output_path>`로 단일 HTML 파일을 생성하세요. 사용자가 "Submit All Reviews"를 누르면 `feedback.json` 파일이 다운로드됩니다. 그 뒤에는 이 파일을 워크스페이스 디렉터리로 복사해 두어야 다음 iteration에서 읽을 수 있습니다.

   참고: 리뷰어는 꼭 `generate_review.py`로 생성하세요. 별도의 커스텀 HTML을 직접 만들 필요는 없습니다.


### 사용자가 뷰어에서 보게 되는 것

"Outputs" 탭은 한 번에 하나의 테스트 케이스를 보여 줍니다.

- **Prompt**: 실제로 실행한 작업 프롬프트
- **Output**: 스킬이 생성한 파일. 가능한 경우 인라인 렌더링
- **Previous Output** (iteration 2+): 지난 iteration 결과를 접어서 볼 수 있는 섹션
- **Formal Grades** (채점이 돌았다면): assertion 통과/실패를 보여 주는 접힘 섹션
- **Feedback**: 입력 중 자동 저장되는 피드백 텍스트박스
- **Previous Feedback** (iteration 2+): 지난번에 사용자가 남긴 코멘트

"Benchmark" 탭은 설정별 pass rate, 시간, 토큰 사용량의 요약과 per-eval breakdown, 분석가 메모를 보여 줍니다.

이동은 이전/다음 버튼이나 방향키로 할 수 있습니다. 다 끝나면 사용자는 "Submit All Reviews"를 눌러 모든 피드백을 `feedback.json`으로 저장합니다.

### 5단계: 피드백 읽기

사용자가 검토를 마쳤다고 알려 오면 `feedback.json`을 읽으세요.

```json
{
  "reviews": [
    {"run_id": "eval-0-with_skill", "feedback": "차트에 축 레이블이 빠져 있어요", "timestamp": "..."},
    {"run_id": "eval-1-with_skill", "feedback": "", "timestamp": "..."},
    {"run_id": "eval-2-with_skill", "feedback": "완벽해요, 마음에 들어요", "timestamp": "..."}
  ],
  "status": "complete"
}
```

빈 피드백은 사용자가 별문제 없다고 느꼈다는 뜻입니다. 구체적인 불만이 적힌 테스트 케이스를 우선적으로 개선하세요.

뷰어 서버를 띄웠다면, 작업이 끝난 뒤에는 종료하세요.

```bash
kill $VIEWER_PID 2>/dev/null
```

---

## 스킬 개선하기

이 부분이 반복 루프의 핵심이다. 테스트 케이스를 돌렸고, 사용자가 결과를 검토했고, 이제 그 피드백을 바탕으로 스킬을 더 좋아지게 만들어야 한다.

### 개선을 어떻게 생각할 것인가

1. **피드백에서 일반화할 것.** 여기서 우리가 실제로 하고 있는 큰 일은 몇 번 쓰고 끝나는 프롬프트가 아니라, 아주 많은 요청에서 반복적으로 쓸 수 있는 스킬을 만드는 것이다. 지금은 빠르게 움직이기 위해 몇 개의 예시에만 집중해 반복하고 있지만, 그 예시들에만 맞는 스킬이 되면 아무 쓸모가 없다. 자잘하고 과적합된 수정, 숨 막히게 빡빡한 MUST 규칙 대신, 계속 같은 문제가 남는다면 다른 은유를 쓰거나 다른 작업 패턴을 제안해 보는 편이 낫다. 시도 비용은 비교적 낮고, 뜻밖에 아주 좋은 방향을 찾을 수도 있다.

2. **프롬프트를 날렵하게 유지할 것.** 제 역할을 못 하는 내용은 과감히 빼세요. 최종 출력만 보지 말고 transcript도 반드시 읽으세요. 스킬 때문에 모델이 비생산적인 일에 시간을 낭비하는 것처럼 보이면, 그런 행동을 유도하는 부분을 걷어내고 다시 시험해 보세요.

3. **왜 그런지 설명할 것.** 모델에게 시키는 모든 일의 **이유**를 설명하려고 노력한다. 지금의 LLM은 꽤 똑똑하다. 충분히 좋은 하네스를 제공하면 단순한 지시를 넘어, 상황을 이해하고 실제 문제를 해결할 수 있다. 사용자의 피드백이 짧거나 답답해 보이더라도, 그 사람이 무엇을 하려는지, 왜 그렇게 적었는지, 실제로 무엇을 말했는지 이해하려고 해 보세요. 그리고 그 이해를 지침에 녹여 전달해라. 문장마다 ALWAYS, NEVER를 대문자로 쓰거나 지나치게 딱딱한 구조를 강요하고 있다면 경고 신호다. 가능하면 재구성해서, 왜 그 요구가 중요한지 모델이 이해하도록 만드는 쪽이 더 인간적이고, 더 강력하고, 더 효과적이다.

4. **테스트 케이스 전반에서 반복되는 작업을 찾을 것.** 실행 transcript를 읽고, 각 run이 비슷한 보조 스크립트를 반복 작성했는지 살펴봐라. 예를 들어 3개 테스트 케이스 모두에서 `create_docx.py`나 `build_chart.py` 같은 도구를 다시 만들었다면, 그건 스킬에 해당 스크립트를 번들로 넣어야 한다는 강력한 신호다. 한 번만 작성해서 `scripts/`에 두고, 스킬이 그걸 쓰도록 지시하세요. 그러면 미래의 모든 실행이 같은 바퀴를 다시 발명하지 않아도 됩니다.

이 일은 꽤 중요하다. 정말 큰 가치를 만들 수도 있는 작업이니까요. 생각하는 시간은 병목이 아니다. 시간을 들여 충분히 곱씹어 바라. 초안 개정본을 쓴 뒤, 다시 새 눈으로 보고 더 개선하는 식으로 접근하는 걸 권한다. 사용자의 머릿속에 진심으로 들어가 보려 하고, 그 사람이 정말 원하는 것이 무엇인지 이해하려고 해라.

### 반복 루프

스킬을 개선한 뒤에는 다음 순서로 진행합니다.

1. 스킬에 개선 사항을 반영한다
2. 모든 테스트 케이스를 새로운 `iteration-<N+1>/` 디렉터리로 다시 실행합니다. baseline도 포함해야 한다. 새 스킬을 만드는 경우 baseline은 항상 `without_skill`입니다. 그 기준은 iteration이 바뀌어도 그대로 유지된다. 기존 스킬을 개선하는 경우에는 원래 버전과 직전 iteration 중 어느 쪽을 baseline으로 삼는 것이 더 의미 있는지 판단해서 선택해라.
3. 리뷰어를 다시 띄우고, `--previous-workspace`는 이전 iteration을 가리키게 합니다.
4. 사용자가 검토를 마치고 알려 줄 때까지 기다립니다.
5. 새 피드백을 읽고 다시 개선합니다.

다음 중 하나가 될 때까지 계속한다.

- 사용자가 만족한다고 말할 때
- 피드백이 전부 비어 있을 때(즉, 전반적으로 괜찮다고 본 경우)
- 더 이상 의미 있는 개선이 나오지 않을 때

---

## 고급 기능: 블라인드 비교

두 버전의 스킬을 더 엄밀하게 비교하고 싶을 때(예: 사용자가 "새 버전이 진짜 더 나아졌는지 알고 싶어"라고 물을 때) 사용할 수 있는 블라인드 비교 시스템이 있습니다. 자세한 절차는 `agents/comparator.md`와 `agents/analyzer.md`를 읽으세요. 핵심 아이디어는 간단합니다. 두 결과물을 어떤 쪽이 어떤 스킬인지 알려 주지 않은 독립 에이전트에게 보여 주고, 어느 쪽이 더 좋은지 판단하게 한 뒤, 왜 그 결과가 나왔는지 분석하는 방식입니다.

이 기능은 선택 사항이며, 서브에이전트가 필요합니다. 대부분의 사용자에게는 사람이 직접 보는 리뷰 루프만으로도 충분합니다.

---

## description 최적화

SKILL.md frontmatter의 description 필드는 AI가 스킬을 사용할지 결정하는 핵심 기준이다. 스킬을 만들거나 개선한 뒤 description 최적화(개선/검증)를 하려면, **반드시** `references/description-optimize.md`를 먼저 읽고 그 문서를 workflow로 따라라.

---

### 패키징 및 전달 (`present_files` 도구가 있을 때만)

`present_files` 도구를 사용할 수 있는지 먼저 확인하세요. 없다면 이 단계는 건너뜁니다. 사용할 수 있다면 스킬을 패키징하고 `.skill` 파일을 사용자에게 제시하세요.

```bash
python -m scripts.package_skill <path/to/skill-folder>
```

패키징이 끝나면 생성된 `.skill` 파일 경로를 알려 주어 사용자가 설치할 수 있게 하세요.

---

## Codex 또는 헤드리스 실행 지침

**테스트 케이스 실행**: 각 테스트 케이스를 독립된 실행 단위로 취급한다. 최소 실행 단위는 `eval-N/<config>/run-N/`이며, run 하나는 `codex exec` 1회에 대응한다. 이 문서에서 안내하는 `codex exec` 호출은 모두 `--model gpt-5.4-mini`를 포함한다고 가정한다. 기본 운영은 bounded rolling queue다. `eval` 디렉터리 이름은 `eval-N` 형식을 유지하고, 설명적인 이름은 `eval_metadata.json`의 `eval_name`에 둔다. 기본은 각 config당 `run-1`만 실행하고, 사용자가 명시적으로 요청한 경우에만 최대 `run-3`까지 확장한다. 같은 eval의 `with_skill/run-K`와 baseline `run-K`는 같은 배치에서 시작해야 하며, 살아 있는 `codex exec` 총수는 언제나 6개 이하로 유지하세요. 그래서 기본 `run-1` benchmark에서는 eval 3개까지 동시에 굴릴 수 있고, 어떤 eval pair가 끝나면 다음 eval pair를 바로 백그라운드로 넣는 방식이 권장된다. 그 동안 assertion 작성과 이미 끝난 eval의 grading을 겹쳐 진행하면 된다.

benchmark run은 각기 독립된 작업 디렉터리에서 실행하세요. `with_skill`은 benchmark 대상 스킬이 `.agents/skills/` 아래에서 보이도록 준비해야 하고, `without_skill`은 benchmark 대상 스킬의 이름/path/description을 prompt에 직접 실어 보내지 않는 편이 좋다.

**결과 리뷰**: 브라우저를 열 수 없는 환경이거나 헤드리스 환경이라면, 브라우저 기반 리뷰어 대신 `generate_review.py --static <output_path>`로 단일 HTML 파일을 생성해라. 정적 리뷰어를 쓰지 않는다면 결과를 대화나 로그에 직접 정리해 보여 주고, 사용자가 확인해야 하는 파일(.docx, .xlsx 등)은 경로와 함께 안내한다.

**벤치마킹**: 정량 벤치마크는 그대로 활용할 수 있습니다. 다만 실행 환경이 시간/토큰 데이터를 안정적으로 남겨 주지 않는다면 `timing.json`은 선택 사항으로 두고, `grading.json`, `benchmark.json`, 사용자 피드백처럼 재현 가능한 신호를 우선하세요.

**반복 루프**: 나머지는 동일합니다. 스킬을 개선하고, 테스트 케이스를 다시 돌리고, 피드백을 받고, 다시 고칩니다. 파일 시스템이 있다면 iteration 디렉터리 구조를 유지해도 됩니다.

**설명 최적화**: `references/description-optimize.md`를 canonical workflow로 사용하세요. 헤드리스 환경에서도 `evals/trigger-eval.json`, split, candidate, iteration 결과를 같은 문서 흐름으로 관리하면 됩니다. 결과를 HTML로 비교해야 하면 `generate_report.py`와 관련 JSON 산출물을 사용하고, 반복 실행 비용을 엄격하게 통제해야 한다면 candidate 수를 줄이고 수동 iteration으로 운영하세요.

**블라인드 비교**: 독립 실행을 두 개 이상 만들 수 있고, 어느 결과가 어떤 버전인지 숨긴 채 평가할 수 있다면 그대로 사용할 수 있습니다. 다만 이 기능은 선택 사항이며, 대부분의 경우에는 사람이 직접 보는 리뷰 루프만으로도 충분합니다.

**패키징**: `package_skill.py`는 Python과 파일 시스템만 있으면 동작합니다. 헤드리스 실행 환경에서도 결과 파일을 생성해 전달할 수 있습니다.

**기존 스킬 업데이트**: 사용자가 새 스킬 생성이 아니라 기존 스킬 업데이트를 원할 수도 있습니다. 이 경우에는 다음을 따르세요.

- **원래 이름을 유지하세요.** 스킬 디렉터리 이름과 frontmatter의 `name` 필드를 확인하고 그대로 사용하세요. 예를 들어 설치된 스킬이 `research-helper`라면 결과물도 `research-helper.skill`이어야 하고, `research-helper-v2`처럼 바꾸지 마세요.
- **편집 전에 쓰기 가능한 위치로 복사하세요.** 설치된 스킬 경로는 읽기 전용일 수 있습니다. `/tmp/skill-name/`으로 복사한 뒤, 그 복사본을 수정하고 패키징하세요.
- **수동 패키징이 필요하다면 `/tmp/`에서 staging 후 이동하세요.** 권한 문제 때문에 최종 위치에 바로 쓰는 것이 실패할 수 있습니다.

---

## 참조 파일

`agents/` 디렉터리에는 전문 역할용 서브에이전트 지침이 들어 있습니다. 해당 역할의 서브에이전트를 띄워야 할 때 읽으세요.

- `agents/grader.md` — assertion을 출력 결과에 대조해 평가하는 방법
- `agents/comparator.md` — 블라인드 A/B 비교를 수행하는 방법
- `agents/analyzer.md` — 어떤 버전이 왜 이겼는지 분석하는 방법

`references/` 디렉터리에는 추가 문서가 있습니다.

- `references/description-optimize.md` — description trigger 개선/검증 및 최적화용 운영 reference
- `references/schemas.md` — `evals.json`, `grading.json` 등 JSON 구조 정의

---

핵심 루프를 한 번 더 강조하면 다음과 같습니다.

- 스킬이 무엇을 위한 것인지 파악합니다
- 스킬 초안을 작성하거나 기존 스킬을 수정합니다
- 스킬에 접근 가능한 Codex로 테스트 프롬프트를 실행합니다
- 사용자와 함께 결과를 평가합니다
  - `benchmark.json`을 만들고 `eval-viewer/generate_review.py`를 실행해 사람이 결과를 쉽게 검토할 수 있게 합니다
  - 정량 eval도 실행합니다
  - description eval과 skill benchmark는 서로 다른 목적의 루프다. 둘 다 `codex exec`를 사용할 수 있지만, skill benchmark는 run별 작업 디렉터리, prompt, transcript, timing 같은 실행 기록을 엄격히 남겨야 한다.
- 만족할 때까지 반복합니다
- 최종 스킬을 패키징해 사용자에게 전달합니다

TodoList 같은 것이 있다면, 잊지 않도록 이 단계들을 꼭 추가하세요.
