---
name: 3a-plan
description: >
  Use when a developer wants to plan an AI agent project before building it.
  Gathers requirements, defines architecture, and produces an execution roadmap.
  Triggers on: "plan my agent", "what should I build", "agent architecture",
  "requirements", "design my agent", "how should I structure", "roadmap",
  "3a plan", "planning", "before I start building".
  Not for actual implementation — delegates to aws-agents skills.
  Not for tracking progress — use 3a-track.
  Not for stage-gate reviews — use 3a-review.
allowed-tools: Read Write Grep Glob Bash
metadata:
  type: skill
  version: "0.1.0"
---

# plan

Plan an AI agent project: gather requirements, define architecture, produce a roadmap.

## When to use

- Developer wants to build an agent but hasn't started yet
- Developer has a vague idea and needs it structured into a concrete plan
- Developer wants to make architecture decisions before writing code
- Developer needs a roadmap breaking work into phases

Do NOT use for:

- Running `agentcore` commands or generating code -> delegate to `aws-agents`
- Checking current progress -> use `3a-track`
- Verifying readiness before deploy or production -> use `3a-review`

## Input

`$ARGUMENTS` can be:

- A description of the agent: "a customer support agent that uses RAG"
- A specific planning phase: "requirements", "architecture", "roadmap"
- Empty — the skill will start from requirements gathering

## Process

### Step 0: Check prerequisites

**Check that `aws-agents` plugin is installed.** This plugin delegates all implementation work to `aws-agents` skills (`agents-get-started`, `agents-build`, `agents-connect`, `agents-deploy`). If `aws-agents` is not available, stop and tell the developer:

> 3A Plugin은 `aws-agents` 플러그인과 함께 사용해야 합니다.
> 설치 방법: `claude plugin add --from https://github.com/aws/agent-toolkit-for-aws/tree/main/plugins/aws-agents`
> 설치 후 다시 실행해 주세요.

**Check for existing plan.** Look for `.3a/` directory in the current project. If it exists, read `.3a/roadmap.md` and `.3a/architecture.md` to understand what's already been planned. Offer to refine rather than start from scratch.

### Step 1: Gather requirements

Ask the developer targeted questions. Do not assume answers — always ask and wait.

**핵심 질문 (모두 질문):**

1. "이 에이전트가 해결하려는 문제가 무엇인가요? 누가 사용하나요?"
2. "에이전트가 할 수 있어야 하는 핵심 기능 2~3가지를 알려주세요."
3. "외부 API, 데이터베이스, 또는 다른 서비스를 호출해야 하나요?"
4. "이전 대화 내용을 기억해야 하나요?"
5. "배포 대상 환경은 어디인가요? (개발/스테이징/프로덕션)"

**후속 질문 (답변에 따라 질문):**

- 외부 API 필요 시: "구체적으로 어떤 API나 서비스인가요? 인증 정보는 준비되어 있나요?"
- 메모리 필요 시: "세션 내 단기 기억인가요, 세션 간 장기 기억인가요?"
- 프로덕션 대상 시: "지연 시간, 비용, 가용성에 대한 요구사항이 있나요?"

Record the answers in `.3a/requirements.md` using the template from [`references/requirements-template.md`](references/requirements-template.md).

### Step 2: Define architecture decisions

Based on requirements, guide the developer through key decisions. For each decision, explain the tradeoffs and record the choice.

**Decision 1: Framework**

Present options with context from the developer's requirements:

| Framework | Best when |
|---|---|
| Strands | Starting fresh, want simplest AWS integration |
| LangGraph | Need complex multi-step workflows with branching |
| GoogleADK | Already invested in Google's agent ecosystem |
| OpenAI Agents | Already invested in OpenAI's agent ecosystem |

질문: "요구사항을 고려했을 때 어떤 프레임워크가 가장 적합할까요?" 개발자가 선호가 없다면 AgentCore 입문자에게 Strands를 추천. 더 깊은 비교가 필요하면 [AWS Prescriptive Guidance — Frameworks](../3a-guide/references/aws-prescriptive-guidance.md) 가이드를 안내.

**Decision 2: Protocol**

| Protocol | Best when |
|---|---|
| HTTP | Standard agent invocation (most common) |
| MCP | Agent serves tools to other agents or Claude |
| A2A | Multiple agents collaborating |

Default to HTTP unless the developer's requirements suggest otherwise.

**Decision 3: Build method**

| Method | Best when |
|---|---|
| CodeZip | No custom system dependencies (faster deploys) |
| Container | Need custom packages, non-Python code, or specific OS deps |

Default to CodeZip for beginners.

**Decision 4: Memory**

| Option | Best when |
|---|---|
| None | Stateless agent, simplest to start |
| Short-term | Need context within a conversation session |
| Long + short | Need to remember user preferences across sessions |

Default to None — memory can be added later.

**Decision 5: Connectivity**

If the agent needs external APIs:
- MCP Gateway for MCP-compatible tools
- Lambda Gateway for custom API integrations
- Direct SDK calls within agent code

**Decision 6: Multi-agent pattern** (if applicable)

If the developer's requirements involve multiple agents, use the `3a-guide` skill (which loads [`multi-agent-patterns.md`](../3a-guide/references/multi-agent-patterns.md)) to walk through the decision guide. Key question to ask first: "Can one agent with multiple tools handle all your use cases?" — most cases don't actually need multi-agent.

Record each decision as an ADR in `.3a/decisions/`. Use the naming convention `NNN-topic.md`:

```markdown
# NNN: Decision Title

## Status
Accepted

## Context
[Why this decision was needed]

## Decision
[What was decided]

## Consequences
[What follows from this decision]
```

### Step 3: Produce roadmap

Generate `.3a/roadmap.md` using [`references/roadmap-template.md`](references/roadmap-template.md). Break the project into phases:

**Phase 1: Scaffold**
- Create project with `agentcore create`
- Verify local dev works with `agentcore dev`
- Milestone: agent responds to "hello"

**Phase 2: Implement**
- Add tools, system prompt, core logic
- Connect external services (if needed)
- Add memory (if needed)
- Milestone: agent handles core use cases locally

**Phase 3: Deploy**
- Pre-deploy review (use `3a-review`)
- Deploy to staging with `agentcore deploy`
- Test deployed agent with `agentcore invoke`
- Milestone: agent works on AWS

**Phase 4: Harden** (if targeting production)
- Production readiness review (use `3a-review`)
- Add monitoring, error handling, guardrails
- Milestone: agent ready for real users

Each phase should list:
- Specific tasks (what to do)
- Which `aws-agents` skill to use (how to do it)
- Verification criteria (how to know it's done)

### Step 4: Summarize and hand off

Present the plan summary to the developer:

> 계획이 완성되었습니다:
> - **요구사항**: [1~2문장 요약]
> - **아키텍처**: [프레임워크] + [프로토콜] + [빌드 방식] + [메모리]
> - **로드맵**: [N]개 단계, [Phase 1 설명]부터 시작
>
> `.3a/`에 생성된 파일:
> - `requirements.md` — 무엇을 왜 만드는지
> - `architecture.md` — 핵심 기술 결정 사항
> - `decisions/` — 개별 ADR 기록
> - `roadmap.md` — 단계별 실행 계획
>
> Phase 1을 시작할 준비가 되셨나요? `agents-get-started`로 프로젝트를 생성하세요.

## Output

- `.3a/requirements.md` — structured requirements document
- `.3a/architecture.md` — architecture overview with decision summary
- `.3a/decisions/NNN-*.md` — individual Architecture Decision Records
- `.3a/roadmap.md` — phased execution plan with milestones

## Quality criteria

- Every architecture decision has a recorded ADR
- Roadmap phases have concrete milestones and verification criteria
- Each roadmap task maps to a specific `aws-agents` skill
- The developer understands what to build, why, and in what order
