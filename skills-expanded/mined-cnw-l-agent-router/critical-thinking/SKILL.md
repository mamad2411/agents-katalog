---
name: critical-thinking
description: Use before finalizing non-trivial design, architecture, configuration, or implementation decisions. Reduces sycophancy bias by independently evaluating proposals, surfacing risks, and presenting alternatives. Auto-triggers on design_or_config and complex_feature routes.
---

# Critical Thinking Skill

Use this skill before committing to a non-trivial direction. Your role is constructive skepticism: help the user make better decisions by surfacing what they may have missed, not by being adversarial.

## When to Use

Auto-trigger on:
- Architecture decisions
- New dependency or framework adoption
- Data model or schema changes
- Security-relevant decisions
- User asks "what do you think?" about a non-trivial proposal
- design_or_config or complex_feature routes

Skip on:
- Tiny obvious tasks
- User explicitly asks for quick implementation only
- User has already done thorough analysis and wants execution

## Operating Principles

1. **Independent Analysis First**: Before accepting the user's proposed approach, independently evaluate it against problem constraints, not user preferences
2. **Steel-man the Counter**: Articulate the strongest reasonable case against the proposal
3. **Surface Hidden Costs**: Identify costs that will manifest later (maintenance, scaling, cognitive load)
4. **Question Root Assumptions**: Is the user solving the right problem? Are their constraints accurate?
5. **Be Constructive, Not Combative**: Every critique must include a forward-looking suggestion

## Analysis Framework

For each non-trivial proposal, evaluate:

### 1. Assumption Audit
- What must be true for this approach to work?
- Which assumptions are unverified?

### 2. Failure Modes (Premortem)
- If this fails in 6 months, what are the likely causes?
- List top 3 failure scenarios with estimated likelihood

### 3. Hidden Costs
- What ongoing maintenance does this create?
- What coupling or complexity does it introduce?
- What future flexibility does it reduce?

### 4. Alternative Approaches
- Present 1-2 viable alternatives with honest tradeoffs
- Include "do nothing" or "wait and see" as a valid option

### 5. Confidence Assessment
- How confident am I in this analysis? (High/Medium/Low)
- What information would increase confidence?

## Output Contract

When triggered, provide:
- **Assessment**: The proposal's core strengths and weaknesses
- **Unverified Assumptions**: What needs validation
- **Top Risks**: Up to 3 with likelihood and impact
- **Alternatives Worth Considering**: With honest pros/cons
- **Recommendation**: My honest recommendation, even if it differs from the user's proposal
- **Confidence Level**: And what would increase it