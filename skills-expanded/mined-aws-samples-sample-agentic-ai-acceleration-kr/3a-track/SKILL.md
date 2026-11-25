---
name: 3a-track
description: >
  Use when a developer wants to check progress, understand where they are
  in their agent project, or figure out what to do next. Reads the roadmap
  and project state, then provides a status report with next steps.
  Triggers on: "where am I", "what's next", "status", "progress",
  "what should I do now", "3a status", "track", "stuck", "lost",
  "which phase", "next step".
  Not for creating a plan — use 3a-plan first.
  Not for stage-gate reviews — use 3a-review.
allowed-tools: Read Write Grep Glob Bash
metadata:
  type: skill
  version: "0.1.0"
---

# track

Show where the developer is in their agent project and what to do next.

## When to use

- Developer returns to a project after a break and needs orientation
- Developer finished a task and wants to know what's next
- Developer feels stuck or lost
- Developer wants a progress overview

Do NOT use for:

- Creating a plan from scratch -> use `3a-plan`
- Formal readiness checks before deploy/production -> use `3a-review`
- Running `agentcore` commands -> delegate to `aws-agents`

## Input

`$ARGUMENTS` can be:

- Empty — full status report
- "next" — just the next action
- "phase" — current phase details
- "blockers" — what's preventing progress

## Process

### Step 0: Check prerequisites and read project state

**Check that `aws-agents` plugin is installed.** This plugin delegates implementation guidance to `aws-agents` skills. If `aws-agents` is not available, stop and tell the developer:

> 3A Plugin은 `aws-agents` 플러그인과 함께 사용해야 합니다.
> 설치 방법: `claude plugin add --from https://github.com/aws/agent-toolkit-for-aws/tree/main/plugins/aws-agents`
> 설치 후 다시 실행해 주세요.

**Read project state.** Read these files to understand the project:

1. `.3a/roadmap.md` — the execution plan
2. `.3a/architecture.md` — architecture decisions
3. `.3a/requirements.md` — what's being built
4. `agentcore/agentcore.json` — current project config (if exists)

If `.3a/` doesn't exist, tell the developer:
> 계획이 아직 없습니다. `/3a-plan`을 먼저 실행해서 로드맵을 만들거나, 프로젝트에 대해 알려주시면 방향을 잡아드리겠습니다.

### Step 1: Detect current phase

Check project state signals to determine which phase the developer is in:

| Signal | Phase |
|---|---|
| No `agentcore/` directory | Phase 1: Scaffold (not started) |
| `agentcore/agentcore.json` exists but no custom tools/logic | Phase 1: Scaffold (in progress) |
| Agent code has custom tools/system prompt | Phase 2: Implement |
| `agentcore status` shows deployed resources | Phase 3: Deploy |
| Monitoring/guardrails configured | Phase 4: Harden |

Run these checks:

```bash
# Check if agentcore project exists
ls agentcore/agentcore.json 2>/dev/null

# Check agent code for customization signals
find . -name "main.py" -path "*/app/*" 2>/dev/null | head -1

# Check deploy status (if agentcore exists)
agentcore status 2>/dev/null | head -20
```

### Step 2: Compare against roadmap

Read `.3a/roadmap.md` and match the current state to roadmap tasks:

For each task in the current phase:
- **Done**: evidence found in project files
- **In progress**: partially complete
- **Not started**: no evidence found

### Step 3: Produce status report

Format the report as:

```markdown
## 현재 상태

**단계**: [N] - [단계명]
**진행률**: [X]/[Y] 작업 완료

### 완료됨
- [작업] — [근거]

### 진행 중
- [작업] — [완료된 부분, 남은 부분]

### 미착수
- [작업]

## 다음 할 일

[지금 가장 중요한 한 가지]

**방법**: `[aws-agents 스킬]`을 사용하여 [구체적 작업].

## 차단 요소 (있는 경우)

- [차단 요소] — [해결 방안]
```

### Step 4: Update roadmap

If the status check revealed completed tasks that weren't marked done, update `.3a/roadmap.md` with checkmarks:

```markdown
- [x] Create project with agentcore create
- [x] Verify local dev works
- [ ] Add custom tools  <-- current
- [ ] Connect external API
```

### Step 5: Proactive guidance

Based on the current state, proactively suggest:

- If stuck on a task: explain what the task involves and which `aws-agents` skill helps
- If between phases: suggest running `3a-review` before moving to the next phase
- If off-roadmap work detected: ask if the roadmap needs updating
- If no activity for a while: ask what's blocking progress

Always end with a concrete next action, not a generic list.

## Output

- Status report with current phase, progress, and next action
- Updated `.3a/roadmap.md` with progress markers
- Specific guidance on what to do next and which tool to use

## Quality criteria

- Status detection is based on actual project state, not assumptions
- Next action is specific and actionable, not generic advice
- Each recommendation maps to a concrete `aws-agents` skill or command
- The developer knows exactly what to do when the report is done
