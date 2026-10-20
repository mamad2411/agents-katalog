---
name: play-devils-advocate
description: "Stress-test an idea with opposing arguments, failure scenarios, and a premortem before committing resources."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["devils-advocate", "pre-mortem", "red-teaming", "risk-assessment", "critical-thinking", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Ask AI to Play Devil's Advocate (The Pre-Mortem Stress Test) (AI Skill)

## Overview
Founders and project leads naturally develop emotional attachment to their plans, creating confirmation bias that blinds them to operational bottlenecks, churn risks, and economic flaws.

The **Devil's Advocate & Pre-Mortem Protocol** forces the AI to assume an adversarial persona (e.g., a cynical short-seller, a tough venture capitalist, or a strict enterprise auditor) to systematically dismantle your proposal and uncover hidden fatal vulnerabilities.

---

## The Pre-Mortem Mental Model

```
┌─────────────────────────────────────────────────────────────┐
│                 The Pre-Mortem Stress Test                  │
│                                                             │
│  Traditional Planning: "How can we make this succeed?"      │
│  ↳ Triggers optimistic blind spots & wishful thinking       │
│                                                             │
│  Pre-Mortem Prompting (Gary Klein Framework):               │
│  "Fast forward 12 months: This project failed               │
│   catastrophically. Write the post-mortem explaining why."  │
│  ↳ Uncovers fatal assumptions BEFORE investing capital      │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Devil's Advocate Prompt Templates

### Pattern 1: The 12-Month Failure Pre-Mortem
Use before committing money, time, or engineering resources:

```markdown
I am proposing the following business / technical initiative:
[DESCRIBE PROPOSAL / PLAN]

Act as an adversarial Devil's Advocate and conduct a **Pre-Mortem Analysis**:
1. **The Post-Mortem Narrative**: Fast forward 12 months. The initiative has failed completely. Write a 3-bullet post-mortem explaining the exact sequence of events that caused the failure.
2. **Top 3 Fatal Flaws**: What are the 3 weakest assumptions in my plan that I am most in denial about?
3. **The Counter-Strategy**: If you were a well-funded competitor, how would you easily defeat or copy this offer?
4. **Vulnerability Mitigation**: What 2 defensive changes must I make today to prevent this collapse?
```

---

### Pattern 2: The Ruthless VC / Board Member Audit
Use before pitching investors or senior leadership:

```markdown
Review my pitch deck thesis: [PASTE THESIS / METRICS].

Act as a veteran Tier-1 Venture Capitalist who has reviewed 1,000 failed pitches.
- Grill me with the **top 3 hardest, most uncomfortable questions** you would ask to poke holes in our unit economics and defensibility.
- Point out where my customer acquisition cost (CAC) or churn assumptions are unrealistic.
```

---

## Real-World Case Study

### Scenario: Launching a Two-Sided Freelance Developer Marketplace

#### Optimistic Founder Prompt
> *"Here is my plan for a new marketplace connecting React developers with startups. Why will this succeed?"*
> ❌ *Result: AI cheerleads the idea, praising the size of the freelance economy.*

#### Devil's Advocate Pre-Mortem Output
> **AI Adversarial Pre-Mortem**:
> 1. **The Chicken-and-Egg Liquidity Trap**: Without 50 verified clients with active budgets on day 1, top developers will sign up, see zero jobs, and never return.
> 2. **Disintermediation / Platform Leakage**: As soon as a client finds a great developer, they will take the relationship off-platform via PayPal/Stripe to avoid your 15% platform fee.
> 3. **CAC Outweighing LTV**: Paid ads for *"hire developers"* cost $25-$40 per click. If your take rate is only 15% and clients leave after 1 project, your Customer Acquisition Cost (CAC) will exceed Lifetime Value (LTV).

**Actionable Mitigation**: The founder pivoted to a **managed talent retainer model** (handling payroll & IP compliance) rather than an open marketplace, eliminating platform leakage.

---

## Summary Best Practices
- **Give the AI explicit permission to be blunt**: Add *"Do not spare my feelings; be brutally candid and realistic"*.
- **Focus on the mechanism of failure**: Demand the step-by-step causal chain of *how* the failure unfolds.
