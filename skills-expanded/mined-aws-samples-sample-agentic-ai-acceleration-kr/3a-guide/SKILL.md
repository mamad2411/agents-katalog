---
name: 3a-guide
description: >
  Use when a developer asks about agent design best practices, patterns,
  or how to make a better agent. Provides curated guidance on architecture
  patterns, tool design, prompt engineering, error handling, and other
  quality aspects of agent development.
  Triggers on: "best practice", "how should I design", "good agent",
  "agent pattern", "multi-agent", "tool design", "prompt design",
  "3a guide", "advice", "is this a good approach", "what pattern",
  "single vs multi agent", "how to structure my agent".
  Not for project planning — use 3a-plan.
  Not for progress tracking — use 3a-track.
  Not for stage-gate reviews — use 3a-review.
  Not for implementation — delegate to aws-agents.
allowed-tools: Read Grep Glob
metadata:
  type: skill
  version: "0.1.0"
---

# guide

Curated design guidance for building better agents.

## When to use

- Developer asks "what's the best way to..." about agent design
- Developer is choosing between patterns or approaches
- Developer wants to validate a design idea before committing
- `3a-plan` needs a reference to guide an architecture decision

Do NOT use for:

- Creating a project plan or roadmap -> use `3a-plan`
- Checking progress -> use `3a-track`
- Readiness reviews -> use `3a-review`
- Running `agentcore` commands or writing code -> delegate to `aws-agents`

## Input

`$ARGUMENTS` can be:

- A topic: "multi-agent", "tool design", "prompt"
- A question: "should I use one agent or two?"
- Empty — list available guidance topics

## Process

### Step 1: Identify the topic

Match the developer's question to an available reference:

| Topic | Reference | Covers |
|---|---|---|
| Multi-agent patterns | [`references/multi-agent-patterns.md`](references/multi-agent-patterns.md) | When to use multi-agent, pattern comparison, decision guide |
| AWS Prescriptive Guidance | [`references/aws-prescriptive-guidance.md`](references/aws-prescriptive-guidance.md) | 9개 AWS 가이드 카탈로그 — 패턴, 프레임워크, 보안, 서버리스, 경제성, 거버넌스 등 |

If no reference matches, answer from general knowledge but flag: "이 주제에 대한 정리된 가이드는 아직 없습니다. 지금 논의한 내용을 `/3a-decide`로 기록해두시겠어요?"

### Step 2: Load and present

Load the matching reference. Don't dump the entire document — extract the section relevant to the developer's specific question.

**Present as a conversation, not a lecture:**
- State the key tradeoffs concisely
- Ask a clarifying question to narrow down
- Give a recommendation based on their context

### Step 3: Connect back to the plan

If the developer is in an active project (`.3a/` exists):
- Suggest recording the decision via `/3a-decide`
- Check if this changes anything in `.3a/roadmap.md`

If no active project:
- The guidance stands alone — no need to force a planning workflow

## Available references

References are added incrementally as patterns emerge. Current catalog:

- **Multi-agent patterns** — Single agent vs coordinator vs pipeline vs fan-out vs hierarchical
- **AWS Prescriptive Guidance** — AWS 공식 가이드 9종 카탈로그 (패턴, 프레임워크, 보안, 서버리스, 경제성, 거버넌스, 멀티테넌트 등)

## Adding new references

New references should follow this structure:

```markdown
# [Topic Title]

## When to use this reference
[Trigger conditions]

## [Pattern/Approach sections]
[Each with: when to use, tradeoffs, examples]

## Decision Guide
[Questions to ask in order to narrow down the choice]

## Boundary with aws-agents
[What 3A covers vs what aws-agents covers]
```

## Output

- Targeted advice for the developer's specific question
- Clear tradeoffs, not just "it depends"
- A recommendation when enough context is available
- Suggestion to record the decision as an ADR

## Quality criteria

- Advice is specific to the developer's context, not generic
- Tradeoffs are concrete (latency, complexity, cost), not abstract
- Always distinguishes "what pattern to choose" (3A) from "how to implement it" (aws-agents)
