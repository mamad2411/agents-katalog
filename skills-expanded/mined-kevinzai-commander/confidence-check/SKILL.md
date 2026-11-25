---
name: confidence-check
version: 1.0.0
description: |
  Pre-execution confidence assessment. Rate confidence 0-100% across 4 dimensions
  before proceeding with any plan. Prevents wrong-direction work and saves tokens.
  Inspired by SuperClaude Framework's confidence checking pattern.
triggers:
  - "check confidence"
  - "confidence check"
  - "how confident are you"
  - "assess confidence"
---

# Confidence Check

Before executing any plan or implementation, assess your confidence level.

## Process

### Step 1: Rate 4 Dimensions (0-100%)

| Dimension | Question | Score |
|-----------|----------|-------|
| **Requirements** | Do I fully understand what's being asked? | _/100 |
| **Approach** | Do I know how to implement this? | _/100 |
| **Edge Cases** | Have I considered failure modes and edge cases? | _/100 |
| **Verification** | Can I prove the result works? Do I have a test plan? | _/100 |

### Step 2: Calculate Overall Score

Average the 4 dimensions → **Overall Confidence: _%**

### Step 3: Act on Score

#### 90-100%: HIGH CONFIDENCE
- Proceed with implementation
- Execute the plan as designed
- Token savings: maximum (no wasted exploration)

#### 70-89%: MODERATE CONFIDENCE
- Present 2-3 alternative approaches
- Ask 2-3 clarifying questions
- Only proceed after questions are answered
- Token savings: significant (prevents partial wrong-direction work)

#### Below 70%: LOW CONFIDENCE
- STOP. Do not implement.
- List exactly what is unclear or unknown
- Ask focused questions to raise confidence
- Research or explore the codebase for answers
- Re-assess after gathering information
- Token savings: massive (prevents entire wrong-direction session)

### Step 4: Post-Implementation Validation

After completing implementation, run the **Four-Question Check**:

1. **Tests**: All tests passing? (run them, don't assume)
2. **Requirements**: Every requirement from the spec is met? (check each one)
3. **Assumptions**: No assumptions made without verification? (list any)
4. **Evidence**: Can I show evidence for each claim? (screenshots, test output, logs)

If any answer is "no" → fix before marking done.

## ROI

This pattern saves 25-250x tokens by catching wrong-direction work before it starts:
- 90%+ confidence: 1x cost (proceed normally)
- 70-89%: 2-3x cheaper than fixing after (questions cost less than rework)
- <70%: 25-250x cheaper (prevents entire wasted implementation sessions)

## Credit

Inspired by the SuperClaude Framework's confidence checking and four-question validation patterns.
