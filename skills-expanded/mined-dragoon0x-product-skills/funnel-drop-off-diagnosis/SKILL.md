---
name: funnel-drop-off-diagnosis
description: "Diagnose why users drop off at specific funnel steps. Moves beyond 'conversion is low' to identifying root causes and recommending specific fixes. Use when a funnel step has unexpectedly low conversion, overall funnel has degraded, or launching a new flow."
---

# Funnel Drop-Off Diagnosis

Find out why users drop off at specific steps — then fix the right thing.

## How to use

- `/funnel-drop-off-diagnosis` Apply funnel diagnosis constraints to this conversation.
- `/funnel-drop-off-diagnosis <funnel data>` Diagnose a specific funnel with the provided conversion data.

## Constraints

### Funnel Definition
Before diagnosing, MUST ensure the funnel is:
- Sequential: each step logically follows the previous
- Measurable: exact user counts at each step
- Complete: no invisible steps between measured ones
- Time-bounded: define a reasonable window (same session? 7 days?)

### Diagnostic Checklist
For the problem step, work through causes in this order:

1. Technical issues: page loading? Broken elements? Cross-device/browser? Intermittent failures? Check here first — most common, easiest to fix.
2. Clarity problems: does the user know what to do? Is the CTA obvious? Too many choices? Mismatch between promise and reality?
3. Friction problems: too many inputs? Information user doesn't have ready? Unnecessary verification?
4. Trust problems: asking for sensitive data without trust signals? Design inconsistency? No help available?
5. Motivation problems: user doesn't see the value of completing this step? Effort exceeds perceived reward?
6. Expectation mismatch: previous step set wrong expectations? Marketing promised something different?

- MUST work through in order. Don't jump to motivation problems before ruling out bugs.

### Segment the Drop-Off
- MUST break down conversion by: acquisition channel, device type, geography, user segment, time
- If one segment converts dramatically differently, the fix is specific to that segment's context
- NEVER diagnose a funnel problem without checking segments first

### Impact Estimation
For each diagnosis, estimate:
- Confidence: how sure is this the cause? (High/Medium/Low)
- Impact: if fixed, how much would conversion improve?
- Effort: how hard is this to fix?
- MUST prioritize: high confidence + high impact + low effort first

### The Funnel Paradox
- Optimizing one step can hurt a later step
- Making signup easier may bring less-qualified users who churn faster
- MUST measure downstream impact, not just the step being fixed

### Anti-Patterns
- Guessing causes without checking data or segments
- Fixing the page where drop-off happens when the problem started earlier
- Optimizing a step that already works well while ignoring the real bottleneck
- A/B testing without a diagnosis — you're guessing with more steps
