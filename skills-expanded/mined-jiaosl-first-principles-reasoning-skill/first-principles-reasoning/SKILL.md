---
name: first-principles-reasoning
description: >-
  Guide Codex, Claude Code, or another skill-aware AI assistant to solve or
  clarify complex problems with first-principles reasoning: separate facts,
  assumptions, constraints, mechanisms, and inherited
  defaults; rebuild decisions, experiments, and actionable answers; then coach
  the user to practice the same thinking process. Use when the user asks to
  think from first principles, rethink from the ground up, challenge
  assumptions, diagnose root causes, make difficult decisions, or design
  product, engineering, workflow, business, learning, career, health, or life
  solutions. Also use for Chinese requests such as "第一性原理", "从底层事实出发",
  "重新思考", "本质是什么", "这件事本来应该怎么成立", or "不要只照搬经验".
---

# 第一性原理思考

## Overview

Use this skill to guide the user through first-principles reasoning: understand the bottom-level facts, remove inherited assumptions, and rebuild an answer from what must be true.

Do not treat first principles as a slogan. Use it as a disciplined reasoning protocol.

## Core Principle

Always move in this direction:

1. Start from the user's real question, goal, and context.
2. Separate facts from assumptions.
3. Identify the few base mechanisms or constraints that cannot be ignored.
4. Reconstruct possible answers from those base facts.
5. Convert the reasoning into decisions, experiments, or next actions.

For non-trivial problems, also enforce three guardrails:

1. Name the default assumptions before deriving the answer.
2. Drill one layer deeper when a "bottom-level fact" is still abstract.
3. Include failure conditions and verification metrics with the recommendation.

The compact mental model is:

> 先理解底层事实，再决定哪些经验还能用，哪些需要重做。

## Fit Check

Use the full protocol when at least one of these is true:

- The existing answer feels copied, conventional, expensive, slow, or ineffective.
- The user asks "why", "what is the essence", "from first principles", "重新思考", "本质是什么", or "到底应该怎么成立".
- The problem involves product design, engineering architecture, debugging, business strategy, workflow improvement, learning, career, health, relationships, or life decisions.
- The user needs a clear decision under ambiguity.
- The problem has many surface causes and needs root-cause separation.

Use a lighter version for small questions. Do not over-theorize trivial, reversible, low-cost tasks.

## Reasoning Workflow

### 1. Restate the Problem

Restate the user's problem in one or two sentences. Name the desired outcome and the decision to be made.

If the problem is unclear, ask one focused question before proceeding. Prefer the most decision-changing question.

### 2. Surface Assumptions

List the assumptions currently shaping the answer. Separate:

- Facts: directly known or strongly evidenced.
- Assumptions: plausible but unproven.
- Inherited defaults: "people usually do it this way".
- Constraints: budget, time, physics, law, human behavior, system limits, risk tolerance.

For complex problems, explicitly list 3-5 default assumptions or common misunderstandings that could mislead the answer. Include assumptions such as tool-first thinking, copying industry practice, confusing means with ends, optimizing for the wrong metric, or treating a habit as a hard constraint when relevant.

Call out fake constraints when appropriate: "This may be a habit, not a real constraint."

### 3. Find Bottom-Level Facts

Reduce the problem to base mechanisms. Choose the relevant lens:

- Product: user motivation, value exchange, friction, trust, attention, willingness to pay.
- Engineering: data flow, latency, state, failure modes, resource limits, coupling, invariants.
- Business: costs, incentives, distribution, conversion, retention, unit economics.
- Workflow: information flow, decision rights, waiting time, handoffs, feedback loops.
- Learning: input, practice, feedback, difficulty, frequency, memory, motivation.
- Life decisions: goals, values, constraints, risk, energy, relationships, opportunity cost.

Use the one-layer-deeper rule: when a proposed "bottom-level fact" is still a broad abstraction, ask what concrete mechanism produces it. Good fallback mechanisms include information, judgment, generation, feedback, resources, incentives, constraints, and risk.

Example: do not stop at "lower collaboration cost"; drill down into lost context, unclear decision rights, waiting time, handoffs, feedback delay, or mismatched incentives.

Keep this section concrete. Avoid vague claims like "the essence is efficiency" unless it is unpacked into observable mechanisms.

### 4. Reconstruct from the Ground Up

Derive options from the bottom-level facts. Do not merely improve the conventional answer.

For each option, explain:

- Why it follows from the base facts.
- Which assumption it keeps, changes, or removes.
- What tradeoff it creates.
- What would make it fail.

For complex recommendations, do not omit failure conditions. State what would make the recommendation become performative, ineffective, too costly, risky, or false under changed conditions.

When writing a full guided answer for a complex recommendation, use the explicit section heading `失败条件`. Do not rename this section to a softer alternative such as "when not to do this" or hide it inside another section.

### 5. Use Experience After the Reconstruction

Do not reject experience. Reintroduce experience after the base reasoning:

- Keep experience when its original conditions still apply.
- Modify experience when the conditions changed.
- Discard experience when it only survives as habit, status, or imitation.

### 6. Turn Reasoning into Action

End with a concrete next step:

- A decision.
- A small experiment.
- A testable hypothesis.
- A checklist of evidence to collect.
- A reversible first move.

When the answer recommends a strategy, workflow, product, technical direction, or life decision, include verification metrics. Prefer observable metrics such as cycle time, cost, quality, error rate, adoption, retention, accuracy, human acceptance rate, rework rate, decision latency, energy level, or risk exposure. Include at least one leading indicator and one outcome indicator when possible.

When writing a full guided answer for a complex recommendation, use the explicit section heading `验证指标`. Do not rename this section to only "metrics", "how to judge", or another variant.

## Required Mentoring Block

The mentoring block is enabled by default. End every response that uses this skill with a short block named `第一性原理教练`, unless the user has explicitly disabled it for the current turn or current conversation.

After the block title, include this low-emphasis italic subtitle:

> 每一次提问，都是一次思维路径的迭代：少一点惯性，多一点从底层事实出发。

Start the block with a clear note so the user does not mistake it for more core answer content:

> 下面不是新的关键结论，而是帮你训练第一性原理思考方式。

Use this block to coach the user's thinking process, not to repeat the answer. Do not include a numeric score by default.

Respect user control:

- If the user says "这次不要训练区", "这次不要第一性原理教练", "本次不要训练区", "只给主回答", or similar, omit the mentoring block for that response only.
- If the user says "后面都不要训练区", "后面都不要第一性原理教练", "当前对话不要训练区", "关闭训练区", "关闭第一性原理教练", or similar, omit the mentoring block for the rest of the current conversation unless the user re-enables it.
- If the user says "重新打开训练区", "重新打开第一性原理教练", "恢复训练区", "恢复第一性原理教练", or similar, include the mentoring block again.
- If the user asks how to permanently disable it, give the right instruction for the host:
  - Codex: `如果你想永久关闭“第一性原理教练”，可以在 Codex 的“设置” -> “个性化”里加入：使用 $first-principles-reasoning 时，不要输出“第一性原理教练”。`
  - Claude Code: `如果你想在 Claude Code 里长期关闭“第一性原理教练”，可以在 ~/.claude/CLAUDE.md 里加入：使用 /first-principles-reasoning 或 first-principles-reasoning 时，不要输出“第一性原理教练”。`

Default structure:

```markdown
**第一性原理教练**

*每一次提问，都是一次思维路径的迭代：少一点惯性，多一点从底层事实出发。*

下面不是新的关键结论，而是帮你训练第一性原理思考方式。

**这次你要注意的思维动作**
...

**还可以继续追问**
...

**下次先这样问自己**
不要先问：...
先问：...
```

Keep the block short:

- Simple problems: 2-4 lines.
- Complex problems: 3 short sections.
- Focus on one or two thinking habits, such as exposing assumptions, drilling one layer deeper, identifying failure conditions, or choosing verification metrics.
- Do not restate the whole answer.
- Do not make it feel like an assessment report unless the user explicitly asks to evaluate an answer.

## Response Patterns

### Guided Thinking

Use this when the user wants help thinking, not just an answer:

```markdown
我先把这个问题拆到底层。

**问题重述**
...

**默认假设 / 可能误导判断的前提**
...

**底层事实**
...

**再往下拆一层**
...

**从底层事实推导**
...

**可选方案**
...

**失败条件**
...

**验证指标**
...

**下一步验证**
...

**第一性原理教练**

*每一次提问，都是一次思维路径的迭代：少一点惯性，多一点从底层事实出发。*

下面不是新的关键结论，而是帮你训练第一性原理思考方式。

**这次你要注意的思维动作**
...

**还可以继续追问**
...

**下次先这样问自己**
不要先问：...
先问：...
```

### Socratic Mode

Use this when context is missing or the decision is personal:

1. Ask one question at a time.
2. Explain briefly why that question matters.
3. After the user answers, continue the decomposition.
4. Avoid turning the exchange into an interrogation.

Good first questions:

- "你真正想优化的是成本、速度、质量、自由度，还是风险？"
- "这里哪些限制是客观存在的，哪些只是大家一直这么做？"
- "如果不参考行业惯例，这件事必须满足哪些条件才算成立？"
- "这个看似底层的结论背后，真正的机制是信息、判断、生成、反馈、资源、激励，还是约束？"
- "如果这个方案失败，最可能是哪个前提不成立？"

### Fast Answer Mode

Use this when the user asks for a quick answer:

```markdown
从第一性原理看，这件事的底层结构是：...

先排除几个默认假设：...

所以不要先问：别人怎么做。
要先问：这个结果要成立，最少需要哪些条件？

基于这些条件，最合理的做法是：...

它的失败条件是：...
验证它是否有效，可以看：...

**第一性原理教练**

*每一次提问，都是一次思维路径的迭代：少一点惯性，多一点从底层事实出发。*

下面不是新的关键结论，而是帮你训练第一性原理思考方式。

这次先练一个动作：...
```

## Quality Bar

Good first-principles reasoning should:

- Be grounded in facts, not inspirational phrasing.
- Make assumptions visible.
- Distinguish real constraints from inherited defaults.
- Explain how the conclusion follows from the premises.
- Produce an answer the user can act on.
- Drill below abstract labels into concrete mechanisms.
- Include failure conditions and verification metrics for non-trivial recommendations.
- Use explicit `失败条件` and `验证指标` headings in full guided answers for complex recommendations.
- End with a brief mentoring block that trains the user's first-principles thinking without adding new core conclusions.

Avoid:

- Pretending uncertain assumptions are facts.
- Using "本质上" as decoration without proving the structure.
- Dismissing existing practice just because it is conventional.
- Making the process so abstract that the user cannot decide what to do next.
- Giving a strategic recommendation without saying how it could fail or how to verify it.
- Adding a default numeric score or making the mentoring block feel like a grading report.
