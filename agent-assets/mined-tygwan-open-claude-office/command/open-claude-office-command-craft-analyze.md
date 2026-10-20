# /craft-analyze — Phase 1 Only

Phase 1 분석만 실행합니다. 3개 에이전트가 병렬로 Git 레포를 분석합니다.

## Usage

```
/craft-analyze <repo-path>
```

## Arguments

- `repo-path`: 분석할 Git 레포 경로 (필수)

## State Machine

### Pre-check
- `workspace/{project}/.state.yaml` 확인. 없으면 새로 생성 (`current_state: init`)

### Guard
- `current_state`가 `init` 또는 `analyzed` (재실행 허용)
- `analyzed` 상태에서 재실행 시 기존 analysis/ 파일을 덮어씀

### Transitions
```
init → analyzing (3 agents 시작) → analyzed (SUMMARY.md + experience-blocks.md)
```

### Event Logging
- 각 agent 시작 시: `agent_start` 이벤트를 `.state.yaml` log에 기록
- 각 agent 완료 시: `agent_complete` 이벤트를 `.state.yaml` log에 기록
- 인터뷰 시작/완료/스킵 시: `interview_start` / `interview_complete` / `interview_skipped` 이벤트
- 전체 완료 시: `state_transition` 이벤트 (analyzing → analyzed)

## Process

1. `workspace/{project}/analysis/` 디렉토리 생성
2. `.state.yaml` current_state = `analyzing`, phase = 1
3. 3개 에이전트 **병렬** 실행:
   - `code-analyst` → `analysis/architecture.md`
   - `story-analyst` → `analysis/narrative.md`
   - `stack-detector` → `analysis/stack-profile.md`
4. Lead가 3개 산출물을 읽고 `analysis/SUMMARY.md` 작성
5. **Lead가 6블록 갭 분석 수행**:
   - narrative.md에서 Technical Challenges / Key Milestones 추출
   - architecture.md에서 Design Decisions / Key Findings 추출
   - 각 항목을 6블록 템플릿에 매핑 (목표/현상/가설/판단기준/실행/결과)
   - 빈 블록(`[X]`) 또는 부족한 블록(`[△]`) 목록 생성
6. **갭이 있으면 experience-interviewer 호출**:
   - 갭 리스트와 analysis/ 경로를 experience-interviewer에게 전달
   - experience-interviewer가 사용자에게 AskUserQuestion으로 질문
   - 답변을 6블록 형식으로 구조화하여 `analysis/experience-blocks.md` 생성
   - 갭이 없으면 스킵 (`.state.yaml`에 `interview_skipped` 기록)
7. `.state.yaml` current_state = `analyzed`

## CLI Delegation

- `code-analyst`와 `stack-detector`는 대규모 프로젝트에서 Codex CLI 위임 가능 (fc-codex skill 참조)
- `story-analyst`는 Claude 전용 (내러티브 추출 특성상 CLI 위임 불가)

## Error Handling

- Agent 실패 시: `.state.yaml`의 해당 agent 상태를 `failed`로 기록
- 실패한 agent만 재시도 가능 (성공한 agent는 skip)
- 3회 실패 시: `current_state = failed`, 사용자 개입 안내

## Output

```
workspace/{project}/analysis/
├── architecture.md        ← 기술 아키텍처 분석
├── narrative.md           ← 내러티브, 마일스톤, 임팩트
├── stack-profile.md       ← 스택 감지, 템플릿 추천
├── SUMMARY.md             ← Lead 종합 (핵심 인사이트 + 추천)
└── experience-blocks.md   ← 6블록 경험 구조화 (사용자 인터뷰 결과, 선택적)
```

## SUMMARY.md Format

```markdown
# {프로젝트명} Analysis Summary

## Key Insights
- ...

## Recommended Template
`{template-name}` — 근거

## Design Direction
- Palette: ...
- Typography: ...
- Layout: ...

## Notable
특이사항, 주의점, 추가 조사 필요 항목.
```

## Example

```
/craft-analyze /home/coffin/dev/n8n
```
