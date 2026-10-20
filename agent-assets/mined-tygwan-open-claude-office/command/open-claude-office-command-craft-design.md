# /craft-design — Phase 2 Only

Phase 1 분석 결과(Markdown)를 읽어 design-profile.yaml을 생성합니다.

## Usage

```
/craft-design <project-name>
```

## Arguments

- `project-name`: workspace 내 프로젝트명 (필수, analysis/ 존재해야 함)

## State Machine

### Guard
- `current_state == analyzed` (SUMMARY.md, stack-profile.md 존재 필수)
- `design_review` 상태에서 revision_requested인 경우에도 재진입 허용

### Transitions
```
analyzed → designing (design-profile.yaml 생성 중) → design_review (사용자 검토 대기)
design_review → designing (수정 요청 시 재진입)
design_review → building (승인 시 Phase 3으로)
```

### Event Logging
- design 생성 시작: `state_transition` (analyzed → designing)
- CLI 호출: `cli_invocation` (gemini 또는 claude)
- design 생성 완료: `state_transition` (designing → design_review)
- 사용자 승인/수정: `user_input` 이벤트

## Prerequisites

- `workspace/{project}/analysis/SUMMARY.md` 존재
- `workspace/{project}/analysis/architecture.md` 존재
- `workspace/{project}/analysis/stack-profile.md` 존재

## CLI Delegation

- Gemini CLI가 primary (design-agent 사용, fc-gemini skill 참조)
- 기본 모델: `gemini-2.5-flash`, 섹션 5+개 또는 커스텀 팔레트 시 `gemini-2.5-pro`
- Gemini 실패 시 Claude fallback, `.state.yaml` log에 `cli_fallback` 기록

## Process

1. `.state.yaml` current_state = `designing`, phase = 2, design.status = `generating`
2. `analysis/SUMMARY.md` 및 개별 분석 파일 읽기
3. `analysis/stack-profile.md`에서 추천 템플릿 확인
4. `design/domain-profiles/index.yaml`에서 도메인 프로파일 매칭
5. `design/palettes/`, `design/typography/`, `design/layouts/`에서 프리셋 선택
6. design-agent 실행 (Gemini CLI primary)
7. 프로젝트 특성에 맞게 커스터마이즈
8. `workspace/{project}/design-profile.yaml` 생성
9. `.state.yaml` current_state = `design_review`, design.status = `review`

## Design Review Gate

design-profile.yaml 생성 후 사용자 검토를 요청합니다:

1. AskUserQuestion: "design-profile.yaml을 검토해주세요. 승인/수정?"
2. **승인 시**:
   - `.state.yaml`: design.approval_status = `approved`
   - Phase 3 진행 가능
3. **수정 요청 시**:
   - `.state.yaml`: design.approval_status = `revision_requested`, design.review_feedback에 피드백 저장
   - 피드백 반영 후 design-profile.yaml 재생성
   - 다시 design_review 상태로 전이

## Output

```yaml
# design-profile.yaml
project: n8n
template: sveltekit-dashboard
domain: automation

palette:
  bg:
    primary: "#0d1117"
    secondary: "#161b22"
    card: "#1c2130"
  text:
    primary: "#e6edf3"
    secondary: "#8b949e"
    muted: "#484f58"
  accent:
    primary: "#ea4b71"
    secondary: "#3ddbd9"
  border: "rgba(255,255,255,0.08)"

typography:
  heading: "'Chakra Petch', sans-serif"
  body: "'Manrope', sans-serif"
  mono: "'JetBrains Mono', monospace"

layout:
  type: dashboard  # or landing
  radius: "18px"
  max_width: "1200px"

sections:
  - hero
  - features
  - architecture
  - tech-stack
  - metrics
  - timeline
```

## Example

```
/craft-design n8n
```
