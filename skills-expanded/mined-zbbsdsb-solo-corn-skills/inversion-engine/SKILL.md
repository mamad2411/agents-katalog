---
name: inversion-engine
description: Systematically applies Charlie Munger's inversion principle to identify failure modes, work backwards from success, and design robust strategies by asking "What would guarantee this fails?" before asking "How to make this succeed?"
category: deep-thinking
version: 1.0.0
tags:
  - inversion
  - failure-analysis
  - pre-mortem
  - decision-making
  - risk-mitigation
  - strategic-planning
operations:
  - pre-mortem
  - backcast
  - invert-problem
  - failure-taxonomy
  - kill-criteria
---

# Inversion Engine Skill

## Overview

The Inversion Engine is a systematic framework for applying Charlie Munger's powerful inversion principle to decision-making, planning, and problem-solving. Instead of starting with "How do we succeed?" this skill forces you to first ask "What would guarantee we fail?"—then work backwards from there to eliminate those failure modes.

**Core Philosophy**: "What would guarantee this fails? — then work backwards from there" (Charlie Munger's inversion)

This skill provides a structured approach to:
- **Pre-Mortem**: Conduct a 5-layer decomposition of a hypothetical failure
- **Backcast**: Work backwards from a desired future to identify critical steps
- **Invert-Problem**: Flip problems on their head to find novel solutions
- **Failure-Taxonomy**: Categorize and prioritize failure modes
- **Kill-Criteria**: Define clear conditions that signal it's time to pivot or stop

## Why Inversion Matters

Inversion is a powerful mental model because:
- **Failure is more predictable than success**: There are far more ways to fail than to succeed
- **Avoiding stupidity is easier than seeking brilliance**: It's often simpler to eliminate bad decisions than to generate brilliant ones
- **Blind spots are revealed**: Inversion surfaces risks and flaws that forward-thinking misses
- **Contingencies become obvious**: By identifying failure modes, you can design mitigations upfront

### Key Sources of Failure That Inversion Uncovers
- Overconfidence in assumptions
- Unplanned dependencies
- Ignoring second-order consequences
- Underestimating execution complexity
- Failing to anticipate competitor responses
- Misaligned incentives

## Core Operations

### 1. Pre-Mortem (5-Layer Decomposition)

Imagine the project/product has failed catastrophically. Work backwards through 5 layers to understand exactly what happened.

**Layer 1: The Failure Event**
- What is the specific failure? (e.g., "Product launch failed, zero paying customers in first 3 months")
- When did it occur?
- What was the immediate impact?

**Layer 2: Direct Causes**
- What 3-5 things directly caused the failure?
- Which of these were avoidable?
- Which were unpredictable?

**Layer 3: Contributing Factors**
- What underlying conditions allowed the direct causes to occur?
- What processes/systems failed?
- What assumptions were violated?

**Layer 4: Root Causes**
- What fundamental decisions/omissions led to the contributing factors?
- What cognitive biases were at play?
- What incentives were misaligned?

**Layer 5: Prevention & Mitigation**
- What could we have done at each layer to prevent this?
- What early warning signs could we have monitored?
- What contingencies could we have had in place?

### 2. Backcast

Start from a successful future state and work backwards to identify what must happen at each step.

**Step 1: Define the Success State**
- What does success look like in 1 year? 3 years?
- Be specific: metrics, outcomes, impact
- Write it as if it's already happened

**Step 2: Identify the Predecessor States**
- What must be true 6 months before success?
- What must be true 3 months before that?
- Continue backwards to the present

**Step 3: Map Critical Milestones**
- What are the non-negotiable milestones?
- What are the dependencies between milestones?
- What resources are required at each step?

**Step 4: Identify Risks & Mitigations**
- For each milestone: What could prevent it?
- How will we know if we're off track?
- What's the backup plan?

### 3. Invert-Problem

Flip the problem on its head to find novel solutions and uncover hidden risks.

**How to Invert a Problem**:
1. State the original problem clearly
2. Ask: "What is the exact opposite of what we want?"
3. Ask: "How would we achieve that opposite outcome?"
4. Take those answers and invert them to find solutions

**Examples of Inverted Problems**:
- Original: "How do we increase customer retention?"
  Inverted: "How would we guarantee customers leave as quickly as possible?"
- Original: "How do we make this product launch successful?"
  Inverted: "How would we make this product launch fail spectacularly?"
- Original: "How do we build a great team?"
  Inverted: "How would we build a terrible team?"

### 4. Failure-Taxonomy

Categorize and prioritize failure modes to focus mitigation efforts.

**Failure Categories**:
1. **Strategic Failures**
   - Wrong market, wrong product, wrong timing
   - Misunderstood customer needs
   - Poor competitive positioning

2. **Execution Failures**
   - Missed deadlines, budget overruns
   - Quality issues, technical debt
   - Team misalignment, turnover

3. **Financial Failures**
   - Burn rate too high, runway too short
   - Revenue below projections
   - Unit economics don't work

4. **Market Failures**
   - Market smaller than expected
   - Competitors respond aggressively
   - Market conditions shift

5. **Operational Failures**
   - Supply chain disruptions
   - Legal/regulatory issues
   - Reputational damage

**Prioritization Framework**:
- **Likelihood**: How likely is this failure? (High/Medium/Low)
- **Impact**: How bad would it be? (Catastrophic/Significant/Minor)
- **Detectability**: Can we see it coming? (Easy/Hard/Impossible)
- **Mitigation Cost**: How much would it cost to prevent?

### 5. Kill-Criteria

Define clear, objective conditions that signal it's time to pivot, stop, or fundamentally change course.

**How to Define Kill-Criteria**:
1. **For Each Major Initiative**:
   - What metrics would tell us this is working?
   - What metrics would tell us this is NOT working?
   - What are the minimum acceptable thresholds?

2. **Set Time-Based Checkpoints**:
   - When will we review progress?
   - What must be achieved by each checkpoint?

3. **Define Decision Rules**:
   - If X happens by Y date, we pivot
   - If Z happens, we stop entirely
   - No exceptions—stick to the criteria

**Example Kill-Criteria**:
- "If we don't have 100 paying customers in 3 months, we pivot the business model"
- "If burn rate exceeds $50k/month for 2 consecutive months, we cut expenses by 30%"
- "If user retention is below 20% after 3 months, we stop development and reassess"

## Workflow: Sequencing Operations

A typical inversion workflow looks like this:

1. **Start with Invert-Problem**: First flip the problem to uncover obvious failure modes
2. **Conduct Pre-Mortem**: Do a deep 5-layer decomposition of hypothetical failure
3. **Build Failure-Taxonomy**: Categorize and prioritize all identified failure modes
4. **Define Kill-Criteria**: Set clear stop/pivot conditions based on the taxonomy
5. **Use Backcast**: Work backwards from success to design a plan that avoids the failures

## Integration with Other Skills

This skill works synergistically with:

**Strategic-Decision Skill**
- Use inversion to stress-test strategic options
- Apply pre-mortem to strategic plans
- Use kill-criteria to define decision points

**Principle Skill**
- Use principle's questioning techniques to dig deeper in pre-mortems
- Extract principles from failure analysis
- Use biases section to identify cognitive traps in forward thinking

**Collector Skill**
- Collect failure patterns across projects
- Build a library of kill-criteria templates
- Track outcomes against pre-mortem predictions

## Founder-Specific Annotated Examples

### Example 1: SaaS Startup Pre-Mortem

**Context**: Founder planning to launch a project management tool for remote teams

**Pre-Mortem Decomposition**:
- **Layer 1 (Failure)**: "Launch failed—only 20 signups in first month, 0 paid"
- **Layer 2 (Direct Causes)**: "No one signed up because they didn't see value; existing tools are good enough"
- **Layer 3 (Contributing Factors)**: "Didn't talk to enough customers; assumed our features were unique; no clear differentiation"
- **Layer 4 (Root Causes)**: "We built what we wanted, not what customers needed; confirmation bias made us ignore negative feedback"
- **Layer 5 (Mitigation)**: "Talk to 50 customers before building; do a concierge MVP first; define clear differentiation"

**Kill-Criteria Defined**:
- "If < 100 signups in first month, pivot"
- "If < 10% conversion to paid, reassess pricing/value"

### Example 2: E-commerce Backcast

**Context**: Founder wants to build a sustainable clothing brand to $1M ARR in 3 years

**Backcast from $1M ARR**:
- **Year 3 ($1M ARR)**: 10,000 customers @ $100 average order value, 4x/year
- **6 Months Before Year 3**: 5,000 customers, strong repeat purchase rate
- **Year 2**: 2,000 customers, proven supply chain
- **Year 1**: 500 customers, validated product-market fit
- **Now**: Validate demand with pre-orders, find suppliers

**Failure-Taxonomy Applied**:
- Prioritized supply chain risk (high impact, medium likelihood)
- Built contingency suppliers upfront

## Quick Reference Card

| Operation | Purpose | Key Questions |
|-----------|---------|---------------|
| **Pre-Mortem** | 5-layer failure decomposition | What happened? Why? How to prevent? |
| **Backcast** | Work backwards from success | What must be true before that? |
| **Invert-Problem** | Flip problems for solutions | How would we guarantee failure? |
| **Failure-Taxonomy** | Categorize & prioritize failures | Likelihood? Impact? Mitigation cost? |
| **Kill-Criteria** | Define stop/pivot conditions | What metrics? What thresholds? When? |

---

*"It is remarkable how much long-term advantage people like us have gotten by trying to be consistently not stupid, instead of trying to be very intelligent." — Charlie Munger*
