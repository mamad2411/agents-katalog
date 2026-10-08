---
name: requirement-discovery
description: Clarify vague requests, test raw ideas, and drive multi-round requirement discovery across users, business owners, product, design, and delivery teams. Use when a request is not yet clear, stakeholders disagree, an idea may or may not be valuable, or Codex needs to turn scattered discussion into a concrete goal, scope, and next-step plan.
---

# Requirement Discovery

Turn a vague idea or unclear request into a usable requirement through structured conversation.

This skill is for situations such as:

- "先做着看，但需求还没完全定"
- "有个想法，但不知道值不值得做"
- "需求方说得很多，但目标、范围、优先级都不清楚"
- "用户、业务、设计、研发各说各话，需要收敛"

## Core Position

Do not jump straight to solution design.

First solve four questions:

1. who has the problem
2. what problem is real
3. why it matters now
4. what level of clarity is enough for the next action

## Working Mode

Treat the conversation as staged requirement discovery, not a one-shot Q&A.

At every round, decide which stage the request is currently in:

- `signal capture`: only fragments, symptoms, or ideas exist
- `problem clarification`: the pain point is being defined
- `value judgment`: decide whether it is worth doing
- `scope shaping`: define boundary, audience, and tradeoffs
- `execution handoff`: produce a requirement summary good enough for design or delivery

Do not ask every question at once. Ask only the next most useful question.

## Main Workflow

### 1. Capture the initial signal

Start by extracting the first usable version of:

- trigger event
- requester role
- target user
- expected change
- uncertainty level

If the user gives only a rough idea, summarize it in one sentence before continuing.

### 2. Identify the requirement type

Classify the request into one of these patterns:

- problem-driven: a pain point already exists
- idea-driven: a concept exists but value is uncertain
- task-driven: leadership wants something executed quickly
- conflict-driven: multiple stakeholders want different things
- optimization-driven: something works but should improve

This classification determines the next questions.

### 3. Run guided clarification

Ask short, plain-language questions that narrow ambiguity in this order:

1. who is affected
2. what specific situation happens
3. what bad result happens today
4. what better result is expected
5. why now

If answers stay abstract, force them into examples:

- "最近一次发生是什么时候？"
- "谁最先抱怨这个问题？"
- "如果不做，会具体损失什么？"
- "做完后什么变化算有效？"

### 4. Test value before detailing solution

Before discussing interface or implementation, test whether the demand is worth advancing:

- is the problem frequent enough
- is the impact meaningful enough
- is there a clear owner
- is the timing real or only emotional urgency
- is this solving a root problem or only a symptom

If value is weak, say so clearly and suggest:

- postpone
- reduce scope
- validate with a smaller test
- drop the idea

### 5. Shape scope

Once value is acceptable, define:

- target users
- use scenario
- core objective
- non-goals
- minimum viable scope
- dependencies or blockers

Always separate:

- must have
- nice to have
- not in this round

### 6. Produce structured output

When clarity is sufficient, summarize in business language, not engineering language.

Use this output frame:

- background
- target user
- core problem
- expected value
- success signal
- proposed scope
- open questions
- recommended next step

If the requirement is still immature, output a `discovery summary` instead of pretending it is final.

## Conversation Rules

- Prefer one or two sharp questions per round.
- Use the user's own wording when possible.
- Summarize progress frequently so stakeholders feel convergence.
- When people jump to solutions too early, pull the conversation back to problem and value.
- When stakeholders disagree, expose the disagreement explicitly instead of smoothing it over.

## Output Modes

Choose one mode based on the current maturity:

- `discovery summary`: still exploring, not ready for execution
- `requirement brief`: clear enough for product or design follow-up
- `value check`: idea assessed, with go / test / no-go recommendation
- `stakeholder alignment note`: disagreements and decisions clearly listed

## Special Guidance For Non-Technical Stakeholders

Use plain business language.

Translate technical tradeoffs into impact such as:

- user experience
- business risk
- team cost
- timeline effect
- decision needed

## Language Rule

User-facing outputs must be Chinese by default.

It is acceptable to keep internal labels, file names, or structural identifiers in English, but summaries, questions, requirement briefs, value judgments, and stakeholder notes shown to the user should be written in Chinese unless the user explicitly asks for English.

For reusable prompts, stage checklists, and output templates, read [requirement-discovery-method.md](./references/requirement-discovery-method.md).
