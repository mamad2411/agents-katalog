---
name: karpathy-understanding-first
description: 'Apply the Karpathy understanding-first principle — verify what AI built, own your understanding, map the jagged capability landscape of LLMs. Use this skill when the user has used AI to build something and needs to verify it, wants to audit their own understanding, needs to know where LLMs are reliable vs unreliable, or says "verify this", "do I actually understand this", "what can I trust the AI on", "jagged capabilities", "understanding not outsourcing". Based on 46k-like quote post.'
disable-model-invocation: false
user-invocable: true
related_skills:
  - karpathy-llm-simulator
  - karpathy-system-prompt-learning
  - karpathy-meta-reflection
  - karpathy-practice-environments
---

# Skill 8: Understanding > Outsourcing（理解 > 外包）

> Source: https://x.com/karpathy/status/2049907410303865030
> "You can outsource your thinking but you cannot outsource your understanding." — 46k likes
> Also: Jagged Capabilities Modeling (Sequoia conversation)

## Core Principle

**Outsourcing is fine. Atrophy is not.**

Use AI to go 10x faster. But every time you skip understanding something, you're borrowing from your own future. Understanding compounds. Blindly shipping agent output does not.

Karpathy's "jagged capabilities" insight: LLMs are **wildly good** at some things (verifiable, high-data domains) and **silently wrong** at others (off-distribution, novel combinations). You need a mental map of which is which.

## The Understanding Audit

After every agent-assisted work session, run this:

```
I just had an AI help me [DESCRIBE WHAT WAS BUILT/WRITTEN/DECIDED].

Help me audit my own understanding:

1. List the 5 key decisions that were made (technical choices, assumptions, trade-offs)
2. For each decision: would I be able to explain WHY this choice was made to a colleague?
   Mark each: UNDERSTOOD / SHALLOW / BLACK BOX
3. For the BLACK BOX items: give me a 3-sentence explanation I can verify
4. What would I need to read/learn to make the SHALLOW items UNDERSTOOD?

Be honest. If I'm shipping something I don't understand, I need to know.
```

## Jagged Capabilities Map

LLMs are NOT uniformly capable. Use this mental model:

### HIGH Reliability (on the rails)
These are well-defined, verifiable, data-rich domains:
- Code in popular languages (Python, JS, SQL)
- Text summarization and rewriting
- Structured data extraction
- Well-known algorithms
- Common patterns (REST APIs, SQL queries, regex)

### MEDIUM Reliability (use carefully, verify)
- Less popular languages (Rust, Haskell, Elixir)
- Integrating multiple systems together
- Anything involving specific versions/APIs after training cutoff
- Multi-step reasoning chains
- Math beyond simple arithmetic

### LOW Reliability (always verify independently)
- Cutting-edge research (may hallucinate papers)
- Novel combinations of technologies
- Domain-specific knowledge you can't easily verify
- Legal/medical/financial specifics
- Anything where being wrong is expensive

## The Capability Check Prompt

Before trusting an AI output on something important:

```
I need to evaluate how reliable your output is for this specific task:

Task type: [DESCRIBE WHAT YOU ASKED THE AI]
Output: [PASTE THE OUTPUT]

Help me assess:
1. How common is this exact pattern in training data? (ubiquitous / common / rare / novel)
2. What's the easiest way to verify this without running it?
3. What's the most likely error — hallucinated API? Wrong logic? Outdated syntax?
4. What search query would I use to double-check the key claim?
5. Should I trust this output? (YES/VERIFY_FIRST/DEFINITELY_CHECK)
```

## The Anti-Atrophy Protocol

Karpathy tracks which skills are atrophying (taken over by AI) and which are growing. Monthly check:

```
Run a skills audit for [MONTH/YEAR]:

Things I've been having AI do for me recently:
[LIST 5-10 TASKS]

For each:
1. Is my ability to do this WITHOUT AI declining? (YES / NO / UNSURE)
2. Is that OK? (Critical skill I must maintain / Commodity I'm fine outsourcing)
3. Action: KEEP_DELEGATING / PRACTICE_MANUALLY / LEARN_DEEPLY

Final question: What's one thing I should deliberately do WITHOUT AI this month to stay sharp?
```

## The Verification Checklist

Before shipping any agent-produced output:

```markdown
Understanding verification:
- [ ] I can explain what this does in plain English without looking at it
- [ ] I've traced through the logic manually for at least one example
- [ ] I know what the failure mode looks like
- [ ] I've run it / tested it myself (not just read the output)
- [ ] If it's wrong, I'll know how to debug it
- [ ] I'm not shipping something I'd be embarrassed to explain in a code review

If any box is unchecked: understand it before shipping.
```

## The Learning Extraction Prompt

When AI writes something you don't understand — learn from it, don't just ship it:

```
You wrote this code/text and I don't fully understand it:

[PASTE OUTPUT]

Teach me:
1. The underlying concept (assume I know [MY_LEVEL] — beginner/intermediate/expert)
2. Walk through the logic step by step
3. What would happen if I changed [SPECIFIC PART]?
4. Point me to the canonical resource where I can learn this properly
5. Give me a simpler version that demonstrates the core idea in isolation

I'm going to use this as a learning moment, not just copy-paste.
```

## Workflow

**属于工作流：反偏见决策（第2步）+ 工作流：月度体检（第2步）**

| 位置 | 上游 | 下游 |
|------|------|------|
| C第2步 | karpathy-llm-simulator（辩论后） | karpathy-system-prompt-learning（沉淀规则） |
| D第2步 | karpathy-meta-reflection（审计后） | karpathy-practice-environments（建练习环境） |

反偏见决策链路：llm-simulator → understanding-first → system-prompt-learning
月度体检链路：meta-reflection → understanding-first → practice-environments → education-first

## Prompt Contract

```text
After completing this task, append an Understanding Report: 1) Key assumptions made (list each), 2) What was verified (with evidence), 3) What remains inferred/unverified (with suggested verification method), 4) Capability boundary notes (where LLM might be off-distribution for this task), 5) Items I must personally inspect or understand before relying on this output.
```

## Verification Checklist

- [ ] 关键假设被明确列出（不藏在输出里）
- [ ] 已验证项有证据（测试通过/文档引用/数据对比）
- [ ] 未验证项有明确的验证方法建议
- [ ] LLM 能力边界有标注（哪些部分它可能不擅长）
- [ ] 「你必须亲自看」清单具体到文件/行/配置
- [ ] 人类确认已理解核心逻辑（不只是看了一眼）
