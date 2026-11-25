---
name: npc-mind-testing
description: "NPC Mind Engine MCP를 사용한 시나리오 테스트 및 대화 세션 수행 가이드. 시나리오를 로드하여 LLM 대화 테스트를 실행하고, 감정 흐름을 관찰하며, 정량 평가(Character Fidelity, Scene Appropriateness, Directive Clarity)를 수행한다. npc-mind-studio MCP가 연결된 상태에서 사용자가 시나리오 테스트, 대화 테스트, 감정 시뮬레이션, NPC 연기 테스트, Beat 전환 테스트, 디렉티브 품질 평가, 테스트 레포트 작성 등을 요청하면 반드시 이 스킬을 사용할 것. 엔진 수정 후 회귀 테스트에도 해당."
---

# NPC Mind Testing — MCP 테스트 세션 가이드

시나리오를 로드하여 LLM 대화 테스트를 실행하고, 감정 흐름을 관찰하며, 정량 평가까지 수행하는 워크플로우.

## 3가지 핵심 원칙

### 원칙 1: 한국어 기본
- 모든 description, 대사, 테스트 레포트는 **한국어**로 작성
- PAD 앵커가 한국어 기반이므로 한국어 대사의 자동 분석 정확도가 가장 높다
- 원작이 영어여도 엔진에 입력하는 description·대사는 한국어로 번역

### 원칙 2: NPC Asset 활용
- 테스트 전 `data/{book}/assets/npcs/` 디렉토리에서 기존 Asset 확인
- 있으면 로드, 없으면 새로 생성하여 저장
- 테스트 중 성격 조정이 필요하면 **asset 파일을 수정** (시나리오가 아니라)

### 원칙 3: 순수 대사만 입력
- `dialogue_turn(utterance=...)`에는 **순수 발화만** 포함
- ❌ 금지: `*핸즈가 으르렁거리며* "이 녀석!" *고함친다*`
- ✅ 권장: `"이 녀석! 거기 서라!"`
- 상황 지문은 `situation_description` 파라미터나 Scene Beat 전환으로 표현
- 이유: PAD 자동 분석이 지문에 흔들리지 않고, 순수 대사 톤만 분석해야 정확하다

### 원칙 4: 테스트 스크립트 우선 사용
- 시나리오에 `test_script`가 정의되어 있으면 **반드시 사용**한다
- `get_scene_info()`로 확인 — 각 Focus의 `test_script` 배열과 `script_cursor` 확인
- test_script 사용 시 동일 입력 → 동일 PAD → 일관된 감정 변화가 보장된다
- 즉흥 대사는 test_script가 없거나, 스크립트 소진 후, 또는 추가 검증이 필요할 때만 사용

## 테스트 세션 전체 흐름

```
0. NPC Asset 확인         data/{book}/assets/npcs/ 조회 (원칙 2)
1. load_scenario           시나리오 파일 로드
2. get_scene_info          Scene 활성화 + test_script 존재 확인
3. dialogue_start          세션 시작 + 초기 appraise (save_dir 자동 반환)
4. [test_script 있으면] get_next_utterance → dialogue_turn(utterance=대사) × N
   [test_script 없으면] dialogue_turn(utterance=즉흥 대사) × N
5. dialogue_end            세션 종료 + 관계 갱신 (after_dialogue 포함)
6. 정량 평가 수행           get_history → 3개 지표 채점
7. update_test_report      레포트 작성 (한국어, 정량 섹션 포함)
8. save_scenario("all")    result JSON + report MD 동시 저장
```

**정량 평가는 원칙이다** — 특별한 요청이 없어도 세션마다 수행한다.

### LLM 연기 없이 엔진만 검증할 때 (chat feature 없음)

```
1. load_scenario
2. appraise               초기 상황 → 감정 생성
3. analyze_utterance       대사 → PAD 추출
4. apply_stimulus          PAD → 감정 갱신 + Beat 전환
5. (3-4 반복)
6. after_dialogue
7. save_scenario
```

## 각 단계 상세

### 시나리오 로드
```
load_scenario(path="treasure_island/ch26_mast_duel/짐vs이즈라엘.json")
```
경로는 `data/` 하위 상대 경로. 로드 후 `get_scenario_meta`로 확인.

### Scene 상태 확인
```
get_scene_info()
→ { has_scene: true, active_focus_id: "cornered", trigger_display: "..." }
```
`has_scene: false`이면 시나리오 JSON에 `scene` 필드가 누락된 것.

### 대화 세션 시작
```
dialogue_start(session_id="unique_id", appraise={npc_id: "jim", partner_id: "israel_hands"})
```
서버가 자동으로 initial focus에 대한 appraise를 수행한다. Scene이 활성이면 situation 생략 가능.
반환값에 `save_dir`이 포함되므로 별도 `get_save_dir` 호출 불필요.

### 대화 턴 실행 — test_script 사용 흐름

test_script가 있는 경우, `get_next_utterance` → `dialogue_turn` 순서로 진행한다.

**1단계: 다음 대사 조회**
```
get_next_utterance()
→ {
    "utterance": "핸즈, 뒤에서 무슨 소리가 났어...",
    "beat_id": "cornered",
    "index": 0,
    "remaining": 2,
    "total": 3,
    "exhausted": false
  }
```
- `advance` 파라미터 생략 시 기본값 `true` → 커서 자동 전진
- `get_next_utterance(advance=false)` → peek만 (커서 전진 없음)
- `exhausted: true`이면 해당 Beat의 스크립트가 모두 소진된 것

**2단계: 대사 전송**
```
dialogue_turn(
  session_id="unique_id",
  npc_id="jim",
  partner_id="israel_hands",
  utterance="핸즈, 뒤에서 무슨 소리가 났어..."
)
```
- `pad` 생략 시 → 대사를 자동 PAD 분석 (embed feature)
- 반환: LLM 연기 응답 + 감정 갱신 + `beat_changed` + `active_focus_id`

**3단계: 반복 또는 즉흥 대사**
- `exhausted: false`이면 1-2단계 반복
- 스크립트 소진 후 추가 턴이 필요하면 즉흥 대사를 직접 `dialogue_turn`에 입력
- 즉흥 대사는 커서에 영향을 주지 않는다

### 커서 관리

| 이벤트 | 커서 동작 |
|--------|----------|
| `dialogue_start` | 0으로 초기화 |
| `get_next_utterance(advance=true)` | +1 전진 |
| `get_next_utterance(advance=false)` | 변동 없음 |
| `dialogue_turn` (스크립트 대사 일치 시) | +1 전진 |
| `dialogue_turn` (즉흥 대사) | 변동 없음 |
| Beat 전환 발생 | 0으로 리셋 (새 Beat의 스크립트 처음부터) |

**주의**: `get_next_utterance`와 `dialogue_turn` 둘 다 커서를 전진시킬 수 있다. `get_next_utterance(advance=true)`로 조회한 대사를 `dialogue_turn`에 그대로 전송하면 커서가 **한 번만** 전진한다 (이미 전진된 상태이므로).

### PAD 입력

**자동 분석 (기본값)**: pad 파라미터를 생략하면 대사에서 자동 추출. 자연스러운 흐름에 적합.

**수동 입력이 필요한 경우**:
- D축이 0.00으로 반환될 때 (구조적 한계)
- 반사적/무의식 행동 (대사에 감정이 명시되지 않은 격한 순간)
- 원작 재현을 위해 특정 감정 강도가 필요할 때

**수동 PAD 판단 기준표**:
| 상황 | P | A | D |
|---|---|---|---|
| 차가운 위협 (우위) | -0.3 | 0.3 | +0.6 |
| 애원/굴복 | -0.5 | 0.5 | -0.7 |
| 반사적 분노 | -0.5 | 0.9 | +0.4 |
| 침착한 명령 | 0.0 | -0.2 | +0.7 |
| 충격/경악 | -0.3 | 0.8 | -0.3 |
| 안도 | +0.5 | -0.4 | +0.2 |

### Beat 전환 관찰

`dialogue_turn` 결과에서 `beat_changed: true`이면 새 Focus로 전환된 것.

**정상 동작**: 활성 Focus는 재전환 대상에서 제외된다 (state latching). 같은 Focus로 매 턴 전환되지 않는다.

전환이 의도와 다르면:
- `get_scene_info()`로 trigger 조건 확인
- `get_history()`로 감정 강도 변화 추적
- Trigger 설계가 문제면 시나리오 수정 (→ `npc-scenario-creator` 스킬 참조)

### 세션 종료 + 관계 갱신
```
dialogue_end(
  session_id="unique_id",
  after_dialogue={npc_id: "jim", partner_id: "israel_hands", significance: 1.0}
)
```
`after_dialogue`를 포함하면 세션 종료와 관계 갱신을 한 번에 처리한다.
`significance`: 0.0~1.0. 중요한 장면일수록 1.0. before/after 관계 수치를 반환한다.
`after_dialogue`를 생략하면 관계 갱신 없이 세션만 종료.

### 결과 저장
```
save_scenario(path="<dialogue_start에서 받은 save_dir>", save_type="all")  → .json + .md 동시 저장
```
`save_dir`은 `dialogue_start` 반환값에 포함되므로 별도 `get_save_dir` 호출 불필요.

## 정량 평가 — 3개 필수 지표

매 세션 종료 후 `get_history()`로 전체 턴 데이터를 조회하고, 각 턴에 대해 3개 지표를 5점 척도로 채점한다. 상세 채점 기준은 `references/quality-metrics.md` 참조.

### 1. Character Fidelity (캐릭터 충실도)
디렉티브(tone/attitude/behavior/restriction)가 NPC의 HEXACO 프로필에서 논리적으로 도출되는가.

### 2. Scene Appropriateness (장면 적절성)
Beat/Focus 전환(또는 유지) 결정이 서사적으로 타당한가.

### 3. Directive Clarity (디렉티브 명확성)
디렉티브가 LLM이 이해하고 준수할 만큼 구체적·명확한가. 실제 LLM 응답이 디렉티브를 따랐는가.

### 채점 원칙
- **5점은 완벽 사례에만**. 우수한 일반 사례는 4점
- 근거를 항상 명시 ("좋음" 같은 모호한 표현 금지, 구체적 facet/지시사항 인용)
- 수행 주체 = 채점 주체이므로 자기 관대함 편향에 주의, 의식적으로 엄격하게

## 테스트 레포트 작성

`update_test_report`로 마크다운 레포트를 작성한다. 필수 섹션:

1. **테스트 정보** — 시나리오명, NPC, Partner, 일시, LLM 모델, test_script 사용 여부
2. **Scene 구성** — Beat별 설명, Trigger 조건, test_script 대사 수
3. **감정 흐름 요약** — 턴별 지배 감정, 강도, Mood, Beat, PAD, CF/SA/DC 점수
4. **관계 변화** — Before/After/Delta 표
5. **정량 평가** — 세션 평균 + 턴별 채점 근거
6. **회귀 비교** — 이전 세션이 있으면 점수 비교 + 변동 원인 분석
7. **긍정적 관찰** / **발견된 이슈** / **결론**

### 레포트 작성 전 체크리스트
- [ ] `get_history`로 전체 턴 데이터 조회했는가
- [ ] 각 턴에 대해 3개 지표 모두 채점했는가
- [ ] 채점 근거가 구체적인가
- [ ] 5점 만점을 남발하지 않았는가
- [ ] 이전 세션 레포트를 읽고 회귀 비교했는가 (있을 경우)
- [ ] test_script 사용 여부와 즉흥 대사 비율을 기록했는가

## 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| "세션을 찾을 수 없습니다" | 이미 닫혔거나 서버 재시작 | `dialogue_start`로 새 세션 |
| `has_scene: false` | 시나리오에 `scene` 필드 누락 | JSON 확인 |
| PAD D축 항상 0.00 | D축 앵커 구조적 한계 | 수동 PAD 입력 |
| `update_test_report` 후 파일 없음 | 메모리에만 저장된 상태 | `save_scenario("all")` 필요 |
| `save_scenario` 성공인데 파일 없음 | 경로에 `data/` prefix 누락 | `dialogue_start`가 반환한 `save_dir`을 그대로 사용 |
| `get_next_utterance` → `exhausted: true` 즉시 | Beat 전환 후 새 Beat에 test_script 없음 | 해당 Beat에 test_script 추가하거나 즉흥 대사 사용 |
| 커서가 예상보다 빨리 진행 | `get_next_utterance(advance=true)` + `dialogue_turn` 이중 전진 | `get_next_utterance`로 조회한 대사를 그대로 전송하면 이중 전진 없음 (일치 시 전진 건너뜀) |
| Beat 전환 후 이전 Beat 대사 나옴 | 커서 리셋 미적용 | Beat 전환 후 `get_scene_info`로 active_focus_id 확인 → `get_next_utterance`로 새 Beat 대사 조회 |

## 참고 문서

- **채점 기준 상세**: `references/quality-metrics.md` — 5점 척도 정의, 체크리스트, 예시
- **도구 스펙 상세**: `references/tools-quick-ref.md`
