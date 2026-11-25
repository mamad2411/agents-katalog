---
name: receiving-research-review
description: Use when receiving research review feedback, before implementing suggestions — requires verification against actual data and scientific reasoning, not performative agreement
---

# Receiving Research Review

Handle review feedback with scientific rigor. Verify claims against actual data before acting. Push back on incorrect assessments with evidence.

**Core principle:** Verify before implementing. Evidence before agreement. Scientific correctness over social comfort.

## Response Protocol

When you receive a research review report:

1. **READ** the complete review without reacting
2. **UNDERSTAND** — restate each issue in your own words, or ask for clarification
3. **VERIFY** — check each claim against the actual data files
4. **EVALUATE** — is the feedback scientifically valid for THIS study?
5. **RESPOND** — technical acknowledgment or reasoned pushback
6. **IMPLEMENT** — one issue at a time, verify each fix

## Forbidden Responses

Never respond to a review with:
- "You're absolutely right!"
- "Great point!"
- "Excellent feedback!"
- "Let me implement that now" (before verification)

These are performative, not scientific. The reviewer may be wrong. Verify first.

## Handling Unclear Feedback

If ANY item in the review is unclear:

**STOP.** Do not implement anything.

Ask for clarification on ALL unclear items before proceeding. Why: review items may be related. Partial understanding leads to wrong implementations that waste time and may introduce new errors.

## When to Push Back

Push back (with evidence) when:

- The reviewer's suggestion contradicts your actual data
- The reviewer lacks context about domain-specific practices
- The suggestion would introduce a known confound
- The statistical recommendation is inappropriate for your data type
- The reviewer conflated your phase with a later phase
- The suggestion violates your pre-registered analysis plan (unless the plan itself was flawed)

**How to push back:**
- State the specific claim you disagree with
- Provide the file path and data that contradicts it
- Explain the scientific reasoning
- Propose an alternative if you have one

## For External Reviews (journal peer review, collaborator feedback)

Before implementing any suggestion from an external reviewer:

1. **Check:** Is this technically correct for THIS study's design and data?
2. **Check:** Would this change break the pre-registered analysis plan?
3. **Check:** Is there a reason the current approach was chosen? (Check design doc)
4. **Check:** Does the reviewer have the full context of the study?
5. **Check:** Would this suggestion apply to your specific domain and methods?

## Implementation Order for Multi-Item Feedback

1. **Clarify** anything unclear FIRST (ask all clarification questions at once)
2. Then implement in this order:
   - CRITICAL issues (blocking — must fix before anything else)
   - MAJOR issues that are simple fixes
   - MAJOR issues that are complex
   - MINOR issues
3. **Verify** each fix individually (re-check the data, re-run if needed)
4. **Confirm** no regressions (fixing one issue didn't break something else)

## After Implementing Fixes

After addressing CRITICAL and MAJOR issues:
- Request re-review via `eureka:requesting-research-review`
- Include a summary of what was changed and why
- Reference the original review for continuity

## Integration

- **Called by:** After `eureka:requesting-research-review` returns feedback
- **Pairs with:** `eureka:requesting-research-review` (for re-review after fixes)
