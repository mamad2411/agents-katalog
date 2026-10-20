# /craft-state — State Inspector & Controller

프로젝트의 파이프라인 상태를 조회, 제어합니다.

## Usage

```
/craft-state <project-name> [action]
```

## Arguments

- `project-name`: 프로젝트 이름 (workspace/ 하위 디렉토리명, 필수)
- `action`: 수행할 동작 (선택, 기본값: `inspect`)

## Actions

| Action | 설명 |
|--------|------|
| `inspect` | 현재 상태 시각적 표시 (기본) |
| `log` | 이벤트 로그 출력 (최근 20건) |
| `log --all` | 전체 이벤트 로그 출력 |
| `reset` | 상태를 `init`으로 초기화 (확인 필요) |
| `resume` | `paused`/`failed` 상태에서 이전 상태로 복귀 |
| `resume --retry` | `failed` 상태에서 retry_count 리셋 후 복귀 |
| `pause` | 현재 활성 상태를 `paused`로 전환 |

## Process

### inspect (기본)

1. `workspace/{project}/.state.yaml` 읽기
2. 없으면 "No state file found. Run /craft or /craft-analyze first." 출력
3. 있으면 아래 시각적 포맷으로 출력

### Visual State Display

```
╔══════════════════════════════════════════════════╗
║  {project} — Pipeline State                      ║
╠══════════════════════════════════════════════════╣
║                                                  ║
║  Phase 1: Analyze    [===========] DONE          ║
║    code-analyst      ✓ done                      ║
║    story-analyst     ✓ done                      ║
║    stack-detector    ✓ done                      ║
║    summary           ✓ done                      ║
║                                                  ║
║  Phase 2: Design     [======>    ] REVIEW        ║
║    design-profile    ⏳ review (gemini)           ║
║    approval          ⊘ pending                   ║
║                                                  ║
║  Phase 3: Build      [           ] PENDING       ║
║    page-writer       ○ pending                   ║
║    figure-designer   ○ pending                   ║
║    content.json      ✗ no                        ║
║    tokens.css        ✗ no                        ║
║    site/             ✗ no                        ║
║                                                  ║
║  Phase 3.5: Validate [           ] PENDING       ║
║    validation        ○ pending                   ║
║    issues            0 found                     ║
║                                                  ║
║  Phase 4: Deploy     [           ] PENDING       ║
║    target            —                           ║
║    url               —                           ║
║                                                  ║
║  State: design_review                            ║
║  Updated: 2026-02-21T14:30:00Z                   ║
║  Errors: 0 (retry: 0/3)                         ║
╚══════════════════════════════════════════════════╝
```

#### Status Icons

| Icon | Meaning |
|------|---------|
| `✓` | Done / Passed |
| `⏳` | In progress / Awaiting |
| `○` | Pending (not started) |
| `✗` | Not yet / Failed |
| `⊘` | Awaiting input |
| `—` | Not applicable yet |

### log

1. `.state.yaml`의 `log` 배열 읽기
2. 각 이벤트를 시간순으로 포맷:

```
[2026-02-21 14:00:00] state_transition  init → analyzing          (lead)
[2026-02-21 14:00:05] agent_start       code-analyst              (code-analyst)
[2026-02-21 14:00:05] agent_start       story-analyst             (story-analyst)
[2026-02-21 14:00:06] cli_invocation    codex exec (gpt-5-mini)   (stack-detector)
[2026-02-21 14:02:30] agent_complete    code-analyst              (code-analyst)
[2026-02-21 14:03:00] error             timeout on stack-detector (stack-detector)
[2026-02-21 14:03:01] cli_fallback      codex → claude            (stack-detector)
```

### reset

1. 사용자에게 확인 요청: "Reset {project} state to init? All progress tracking will be lost. (analysis files are preserved)"
2. 확인 시 `.state.yaml`을 초기 상태로 재생성
3. 로그에 `user_input` 이벤트 기록

### resume

1. `current_state`가 `paused` 또는 `failed`인지 확인
2. `paused`: `previous_state`로 복귀, 로그 기록
3. `failed`: `--retry` 없으면 안내 메시지 출력. `--retry` 있으면 `error.retry_count` 리셋 후 `previous_state`로 복귀
4. 다른 상태: "Not in a paused or failed state." 출력

### pause

1. `current_state`가 active 상태(`analyzing`~`deploying`)인지 확인
2. `previous_state`에 현재 상태 저장
3. `current_state`를 `paused`로 변경
4. 로그에 `user_input` 이벤트 기록

## State File Location

```
workspace/{project}/.state.yaml
```

## Examples

```
/craft-state n8n                    # 상태 조회
/craft-state n8n log                # 로그 보기
/craft-state n8n pause              # 일시정지
/craft-state n8n resume             # 재개
/craft-state n8n resume --retry     # 실패 후 재시도
/craft-state n8n reset              # 초기화
```
