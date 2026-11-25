---
name: karpathy-meta-reflection
description: 'Run a structured reflection on how AI is reshaping your skills, career, and leverage. Use this skill for monthly career audits, skill atrophy reviews, understanding what''s worth learning vs delegating to AI, or when the user says "career audit", "skills review", "what should I learn", "am I becoming obsolete", "AI impact on my work", "leverage review", "meta reflection". Based on Karpathy 56k-like programmer identity post.'
disable-model-invocation: false
user-invocable: true
related_skills:
  - karpathy-understanding-first
  - karpathy-practice-environments
  - karpathy-education-first
  - karpathy-system-prompt-learning
---

# Skill 10: Meta-Reflection（元反思）

> Source: https://x.com/karpathy/status/2004607146781278521 | https://x.com/karpathy/status/2015883857489522876
> "I've never felt this much behind as a programmer" — 56k likes

## Core Principle

**The landscape is shifting faster than your intuition updates. Deliberate reflection is how you stay calibrated.**

Karpathy tracks three things relentlessly:
1. What skills are **atrophying** (AI is taking over, for better or worse)
2. What's **exploding** (new leverage you didn't have before)
3. What's your **real job** now (has the role description changed under your feet?)

## Monthly Career Audit Prompt

Run this once a month, 20-30 minutes:

```
Monthly AI Impact Audit — [MONTH YEAR]

My role/field: [YOUR JOB OR DOMAIN]

Part 1: ATROPHYING SKILLS
Things I've been having AI do in the last month:
[LIST 5-10 TASKS YOU DELEGATED TO AI]

For each, analyze:
- How much would it hurt if AI wasn't available for this?
- Is my ability to do this manually getting worse?
- Is that acceptable? (YES = commodity skill / NO = must maintain)

Part 2: EXPLODING LEVERAGE
New things I can now do (or do much faster) because of AI:
[LIST 3-5 NEW CAPABILITIES OR SPEED MULTIPLIERS]

For each: what specifically unlocked this? What should I double down on?

Part 3: ROLE REDEFINITION
Complete this: "In 2023, my job was to [X]. In [CURRENT YEAR], my job is actually to [Y]."

Part 4: NEXT MONTH FOCUS
1. One skill I will DELIBERATELY practice without AI:
2. One new AI capability I will DELIBERATELY learn:
3. One thing I will STOP doing manually because AI is better:
```

## The Atrophy/Leverage Matrix

For any skill you have, plot it on this 2x2:

```
                    HIGH LEVERAGE WITH AI
                           │
    MUST RETAIN            │      MAXIMIZE
    (ai makes it faster    │      (your competitive
     but you need the      │      edge lives here)
     judgment)             │
                           │
HIGH ──────────────────────┼────────────────────── LOW
ATROPHY                    │                      ATROPHY
                           │
    SAFELY DELEGATE        │      ABANDON/AUTOMATE
    (commodity, ai is      │      (low value, losing
     better, let it go)    │      it doesn't matter)
                           │
                    LOW LEVERAGE WITH AI
```

## The Role Redefinition Prompt

Every 6 months, do this deep reflection:

```
Help me understand how my role has evolved.

My job title/domain: [ROLE]
Experience: [YEARS]

Before AI tools (2022 and earlier), my core value was:
[WHAT YOU WERE HIRED/VALUED FOR]

Today, with current AI tools:
1. What percentage of my old tasks can AI now do at 80%+ quality?
2. What tasks have INCREASED in value because AI can't do them (judgment, relationships, taste, ethics)?
3. What new tasks exist now that didn't exist 2 years ago?
4. If I were hiring for my own role today, what would the job description say?
5. What would I tell my 2022 self about what skills to prioritize?

Be specific. Name actual tasks, not abstract concepts.
```

## Tracking the Phase Shift

Karpathy described 2025 as a "phase shift" — not incremental improvement but a different mode. This prompt helps you notice phase shifts in your own domain:

```
Diagnose if my field/work has hit a phase shift.

Domain: [YOUR FIELD]
Recent changes I've noticed: [LIST 3-5 CHANGES IN HOW WORK IS DONE]

Is this:
A) Incremental improvement (same work, faster tools)
B) Role shift (different emphasis within same field)  
C) Phase shift (fundamentally different mode of working)
D) Field transformation (new field is emerging from the old one)

Evidence for your diagnosis. And: what does this mean for where I should invest my time in the next 12 months?
```

## Weekly 5-Minute Check-In

Lighter version for weekly cadence:

```
Quick weekly AI reflection — [DATE]

3 things AI helped me do better this week:
1.
2.
3.

1 thing I learned from reviewing AI output:

1 skill I exercised without AI:

One thing I want to pay more attention to next week:
```

## The "Karpathy Test" for Any Skill

Before investing time learning something, ask:

```
Should I learn [SKILL] deeply in the current AI landscape?

Evaluate:
1. Can current LLMs do this at 80%+ quality? (yes/no)
2. Is human judgment still required for the 20% that matters? (yes/no)
3. Does understanding this deeply make me better at directing AI to do it? (yes/no)
4. Is this skill a prerequisite for judgment that AI can't replicate? (yes/no)

Recommendation: LEARN_DEEPLY / LEARN_BASICS / DELEGATE / SKIP
Reasoning: [2-3 sentences]
```

## Workflow

**属于工作流：月度体检（入口）**

| 位置 | 上游 | 下游 |
|------|------|------|
| 入口 | 每月定期触发 / 用户感到焦虑时 | karpathy-understanding-first（定位理解力盲区） |

完整链路：meta-reflection → understanding-first → practice-environments → education-first

## Prompt Contract

```text
Run a monthly career atrophy audit. Step 1: List my completed tasks this month (I'll provide or you pull from context). Step 2: For each, mark if I delegated to AI and the atrophy risk level. Step 3: Identify my top 3 leverage points (where AI made me 10x). Step 4: Identify my top 2 atrophy risks (skills degrading). Step 5: Recommend one thing to practice next month and one thing to fully delegate. Output as a structured report.
```

## Verification Checklist

- [ ] 任务清单来自实际工作（不是假设）
- [ ] 萎缩风险有具体证据（不是泛泛焦虑）
- [ ] 杠杆点有量化感知（「快了多少」）
- [ ] 下月练习计划具体到可执行（不是「多学习」）
- [ ] 下月委托计划明确到什么任务完全交给 AI
- [ ] 报告可以月月对比追踪变化趋势
