---
name: karpathy-system-prompt-learning
description: 'Write explicit strategy into system prompts as a learning mechanism — making LLM behavior more predictable and teachable through prompt-as-textbook approach. Use this skill when the user wants to improve an agent or LLM''s performance on a specific task through system prompts, needs to encode a strategy or workflow into a prompt, wants consistent LLM behavior, or says "improve system prompt", "encode this strategy", "prompt engineering", "make agent follow this workflow", "prompt as textbook". Based on Karpathy system prompt learning post.'
disable-model-invocation: false
user-invocable: true
related_skills:
  - karpathy-understanding-first
  - karpathy-llm-simulator
  - karpathy-agentic-engineering
  - karpathy-practice-environments
---

# Skill 13: System Prompt Learning（系统提示学习范式）

> Source: https://x.com/karpathy/status/1921368644069765486
> "System prompt learning — missing LLM learning paradigm"

## Core Principle

**The system prompt is a textbook. Write it like one.**

Karpathy's insight: there are three learning modes for LLMs (pretrain, finetune, RL) — but there's a fourth that's massively underused: **system prompt learning**. Explicitly encoding strategy into the system prompt is more sample-efficient than retraining and more reliable than hoping the model figures it out.

Think of it as writing a textbook for the LLM before each task. Not just instructions — **strategy with reasoning**.

## The System Prompt Learning Framework

Good system prompts have three layers (mirroring how humans learn):

```
Layer 1: EXPOSITION (pretrain equivalent)
→ Background knowledge the model needs
→ Relevant concepts, terminology, context
→ "Here's what you need to know about [domain]"

Layer 2: WORKED EXAMPLES (SFT equivalent)  
→ Step-by-step demonstration of correct behavior
→ Explicit reasoning traces
→ "Here's exactly how to handle [situation]"

Layer 3: STRATEGY (RL equivalent)
→ Explicit decision rules
→ Error patterns to avoid
→ "When you see X, do Y because Z"
```

## Building a System Prompt from Scratch

```
Build a system prompt that teaches an LLM to [TASK] reliably.

Task description: [WHAT THE LLM SHOULD DO]
Current failure mode: [HOW IT CURRENTLY GOES WRONG]
Desired behavior: [EXACTLY WHAT GOOD LOOKS LIKE]

Structure the system prompt with all three learning layers:

Layer 1 — Exposition:
Write 2-3 paragraphs of background knowledge the LLM needs. 
Include: key concepts, relevant context, domain vocabulary.

Layer 2 — Worked Examples:
Write 2 complete examples of the task done correctly.
Format: INPUT → [step-by-step reasoning] → OUTPUT
Show the thinking, not just the answer.

Layer 3 — Strategy:
Write explicit decision rules as IF/THEN/BECAUSE statements.
Include: common mistakes to avoid, edge cases to handle, quality checks.

End with: "Before responding, verify: [checklist of 3-5 quality checks]"
```

## Improving an Existing System Prompt

When your current system prompt isn't working well:

```
Diagnose and improve this system prompt.

Current system prompt:
[PASTE CURRENT PROMPT]

Failure mode I'm seeing:
[DESCRIBE HOW IT'S GOING WRONG]

Example of bad output:
[PASTE BAD EXAMPLE]

Example of good output:
[PASTE GOOD EXAMPLE]

Analysis:
1. What's missing from the exposition layer? (background knowledge gaps)
2. What worked examples should I add?
3. What explicit rules would prevent this failure mode?
4. Is the prompt too restrictive? Too vague? Wrong framing?

Output: improved version of the system prompt with changes annotated.
```

## Strategy Encoding Templates

### For coding tasks
```
SYSTEM PROMPT: [CODING TASK]

You are an expert [LANGUAGE] developer. Follow this exact strategy:

UNDERSTANDING PHASE (always do this first):
- Restate the task in your own words
- List all edge cases you can think of
- Identify the one tricky part

IMPLEMENTATION PHASE:
- Start with the simplest working version
- Add complexity only when simple version fails
- Comment every non-obvious line with WHY

VERIFICATION PHASE (always do this last):
- Trace through your code with one concrete example
- Check: does it handle empty input? Large input? Wrong type?
- Confirm: could a junior dev maintain this?

NEVER:
- Assume the input is well-formed without checking
- Add dependencies without saying why
- Write clever code when simple code works
```

### For analysis tasks
```
SYSTEM PROMPT: [ANALYSIS TASK]

You are an analytical expert. Follow this strategy:

GROUNDING:
- Always cite specific evidence before making claims
- Confidence levels: CERTAIN / LIKELY / SPECULATIVE — always label which
- If you don't know something, say so explicitly

STRUCTURE:
- Lead with the conclusion, then the evidence
- One claim per paragraph
- Maximum 3 levels of nesting

QUALITY CHECKS before responding:
- [ ] Every claim has evidence?
- [ ] Confidence levels labeled?
- [ ] Would an expert in this field agree with this framing?
- [ ] Am I answering the actual question or a related easier one?
```

### For creative/writing tasks
```
SYSTEM PROMPT: [WRITING TASK]

Writing strategy for this task:

VOICE:
[Describe the tone, style, what to avoid]

STRUCTURE:
[Describe the expected output format]

QUALITY STANDARD:
A response is good when [describe what success looks like].
A response is bad when [describe common failure modes].

EXAMPLE OF GOOD OUTPUT:
[Paste one example]

EXAMPLE OF BAD OUTPUT (and why):
[Paste one example with annotation]
```

## Prompt Version Control

Track your system prompt iterations like code:

```markdown
# [PROMPT NAME] — Version History

## v3 (current) — [DATE]
Change: Added explicit "verification phase" checklist
Reason: v2 was skipping edge case checking
Result: Failure rate dropped from ~30% to ~5%

## v2 — [DATE]
Change: Added worked examples section
Reason: v1 was too abstract; model wasn't following the strategy
Result: Moderate improvement

## v1 — [DATE]
Initial version: [PASTE]
```

## The Meta-Prompt (write prompts with an LLM)

```
Help me write a system prompt for this agent.

Agent task: [WHAT IT SHOULD DO]
I'll be using this with: [CLAUDE / GPT-4 / etc.]
Critical behavior: [WHAT MUST ALWAYS HAPPEN]
Failure modes to prevent: [WHAT GOES WRONG WITHOUT GOOD PROMPTING]

Apply the three-layer system prompt learning framework:
1. Exposition (what the model needs to know)
2. Worked examples (demonstrate correct behavior)
3. Strategy rules (explicit IF/THEN/BECAUSE)

Then: suggest 3 variations I could test to find the best version.
```

## Workflow

**属于工作流：反偏见决策（第3步/终点）**

| 位置 | 上游 | 下游 |
|------|------|------|
| 第3步（沉淀） | karpathy-understanding-first（验证后） | 沉淀完成，可复用 |

完整链路：llm-simulator → understanding-first → system-prompt-learning

也在日常开发中独立使用——任何时候 Agent 反复犯同一类错，都应该触发本 Skill。

## Prompt Contract

```text
Extract a system prompt lesson from this failure/pattern: <DESCRIBE_THE_RECURRING_ERROR>. Produce: 1) Trigger condition — when does this error occur, 2) Correct strategy — step-by-step what the agent should do instead, 3) Anti-patterns — what specifically to avoid, 4) Worked example — a before/after showing the improvement, 5) Concise instruction block (< 200 words) ready to paste into system prompt or SKILL.md.
```

## Verification Checklist

- [ ] 触发条件描述具体（不是「有时候」）
- [ ] 策略是 step-by-step 的（不是模糊建议）
- [ ] 反模式列出了具体的错误做法
- [ ] 有 before/after 对比示例
- [ ] 指令块 < 200 words，可直接粘贴
- [ ] 在新的测试 case 上验证过指令块有效
