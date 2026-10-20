---
description: "Full pipeline execution with state machine orchestration. Phase 1→2→3→3.5→4 with CLI distribution."
---

# /craft — Full Pipeline (State Machine Orchestrated)

전체 포트폴리오 생성 파이프라인을 상태 머신 기반으로 실행합니다.

## Usage

/craft <repo-path> [--deploy github-pages|vercel|netlify] [--resume] [--model <model>]

## Arguments

| Arg | Description |
|-----|-------------|
| `repo-path` | 분석할 Git 레포 경로 (필수) |
| `--deploy` | 배포 대상 (미지정 시 사전 질문) |
| `--resume` | 이전 .state.yaml에서 재개 |
| `--model` | 모든 CLI 호출에 모델 오버라이드 |

## Pre-flight

1. repo-path가 유효한 git repo인지 확인
2. project-name 추출 (디렉토리명)
3. workspace/{project}/ 생성
4. .state.yaml 확인:
   - 없으면: 새로 생성 (current_state: init)
   - 있고 --resume: 기존 상태에서 재개 (current_state부터)
   - 있고 --resume 없음: AskUserQuestion "기존 상태 덮어쓰기?"
5. --deploy 미지정 시: AskUserQuestion for deploy target

## State Machine Execution

현재 상태에 따라 해당 phase부터 실행합니다.

### Phase 1: Analyze (init → analyzing → analyzed)
guard: repo_path is git repo
action:
  1. .state.yaml: current_state = analyzing, phase = 1
  2. 3 agents 병렬 실행 (Task tool):
     - code-analyst (Claude + optional Codex)
     - story-analyst (Claude)
     - stack-detector (Claude + optional Codex)
  3. 각 agent 완료 시 .state.yaml 업데이트
  4. Lead가 SUMMARY.md 작성
  5. .state.yaml: current_state = analyzed

### Phase 2: Design (analyzed → designing → design_review)
guard: SUMMARY.md + stack-profile.md exist
action:
  1. .state.yaml: current_state = designing, phase = 2
  2. design-agent 실행 (Gemini CLI primary)
  3. design-profile.yaml 생성
  4. .state.yaml: current_state = design_review
  5. AskUserQuestion: 사용자 검토 요청
  6. approved → continue / revision → re-enter designing

### Phase 3: Build (building)
guard: design approved
action:
  1. .state.yaml: current_state = building, phase = 3
  2. page-writer (Claude) → content.json, tokens.css, site/
  3. figure-designer (Claude + optional Gemini) → diagrams/
  4. .state.yaml 업데이트 (build sub-statuses)

### Phase 3.5: Validate (validating → build_review)
guard: content.json + tokens.css + site/ exist, no PLACEHOLDER
action:
  1. .state.yaml: current_state = validating, phase = 3.5
  2. validation-agent 실행 (Codex CLI primary)
  3. passed → .state.yaml: current_state = build_review
  4. issues → feedback to page-writer, re-build
  5. AskUserQuestion: preview 승인 요청

### Phase 4: Deploy (deploying → done)
guard: user approved preview, deploy target specified
action:
  1. .state.yaml: current_state = deploying, phase = 4
  2. 배포 실행 (target에 따라)
  3. deploy.yaml 생성
  4. .state.yaml: current_state = done
  5. /craft-sync 실행 제안

## CLI Distribution

| Phase | Primary CLI | Model Default | Fallback |
|-------|-------------|---------------|----------|
| 1 | Codex (optional) | gpt-5-mini → gpt-5-codex | Claude |
| 2 | Gemini | gemini-2.5-flash → pro | Claude |
| 3 | Claude | sonnet | - |
| 3 (visuals) | Gemini | gemini-2.5-flash → pro | Claude |
| 3.5 | Codex | gpt-5-mini / gpt-5-codex | Claude |
| 4 | Claude | sonnet | - |

## Error Handling

- CLI 실패: 1회 재시도 → Claude fallback → .state.yaml에 cli_fallback 기록
- Agent 실패: .state.yaml에 에러 기록, 해당 phase 재시도
- 3회 이상 같은 phase 실패: AskUserQuestion for 사용자 개입
- 모든 에러는 .state.yaml log에 기록

## Resume

/craft <repo-path> --resume
- .state.yaml의 current_state를 읽고 해당 phase부터 재개
- paused → previous_state로 복귀
- failed → 실패한 phase 시작점으로 복귀

## Feedback Loop Integration

On pipeline completion (state → `done`):
- If `feedback-loop` skill is available, prompt for learning capture
- Auto-suggest ADR if architecture decisions were made during the pipeline
- Record pipeline metrics (duration, retries, CLI distribution) for retrospective
