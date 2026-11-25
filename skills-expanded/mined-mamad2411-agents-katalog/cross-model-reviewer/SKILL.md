---
name: cross-model-reviewer
description: "Cross-provider AI review loop, multi-model code review, doer-reviewer pattern. Use when getting a second-opinion review from a different AI model."
---

# Cross-Model Reviewer

## Overview

This skill is inspired by the doer-reviewer loop: one AI model writes the code, while a completely different AI model from another provider reviews it. Instead of using two instances of the same model, different providers (e.g., Claude writes, Gemini reviews) are used so that each model can catch the other's blind spots. This eliminates systematic errors, hallucinations, and biases that arise from relying on a single model.

**Core principle:** NEVER ALLOW THE SAME MODEL TO BE BOTH THE WRITER AND THE REVIEWER. DIFFERENT PROVIDERS MEAN DIFFERENT PERSPECTIVES.

## The Iron Law

```
THE WRITING MODEL AND THE REVIEWING MODEL MUST NEVER BE FROM THE SAME PROVIDER.
DIFFERENT PROVIDERS = DIFFERENT SETS OF BLIND SPOTS.
THE REVIEWER SEES WHAT THE WRITER MISSES.
DO NOT EXCEED THREE (3) ITERATIONS OF THE FIX LOOP — IF NO AGREEMENT IS REACHED, ESCALATE TO A HUMAN.
```

## When to Use

**Use this when:**
- Writing critical production-ready code (auth, payments, database migrations).
- Developing a module with high security sensitivity.
- Modifying a component that has historically caused bugs.
- Asking an AI model "is this code correct?" and wanting to be absolutely sure.
- Writing a performance-critical algorithm.
- Working during hours when human code reviewers are unavailable.

**Use this ESPECIALLY when:**
- All team members are busy and there is no one else to review your code.
- You are under deadline pressure and want to minimize the risk of errors.
- You are writing code in a language or framework you are not fully familiar with.
- You have been coding blindly late at night or early in the morning.

**Don't skip when:**
- Modifying small scripts or single-line commands (always double-check).
- Building prototypes or "proof of concept" code that will eventually reach production.
- Even under intense deadline pressure — this is exactly when the skill is most valuable.

**You may skip when:**
- Modifying a Readme file or comments only.

## Phase 1 — Doer: Write the Code

**BEFORE proceeding:**

Select the reviewing model. You must know which model will review the code before you even start writing — because you will tailor the implementation style accordingly.

1. **Select Model A (The Doer)** — Choose a model with high writing and generation capabilities:
   - **Claude 3.5 Sonnet / Opus** — Best writers for complex logic.
   - **GPT-4o** — Strong writer, especially in JavaScript/Python ecosystems.
   - **DeepSeek Coder** — Specialized for code writing.
   - Avoid: Small/fast models (high risk of generating buggy code).
2. **Define the task clearly** — Provide the Doer with:
   - Precise requirements.
   - Constraints (language, framework, code style).
   - Test expectations.
   - Existing code context (provide relevant files).
3. **Have the code written** — Allocate a generous token budget for the doer to encourage creative problem-solving:
   - Preferably run via API with high token limits.
   - Alternatively, run via CLI tools.
4. **Collect outputs once writing is complete:**
   - All modified/created files.
   - Associated tests.
   - The Doer's self-evaluation (optional).

## Phase 2 — Reviewer: Review the Code

**BEFORE proceeding:**

Ensure you have selected a provider different from the Doer. **This is critical.**

1. **Select Model B (The Reviewer)** — Choose a model with strong evaluation capabilities:
   - **Gemini 2.0 Pro / Flash** — Excellent review, different blind spots.
   - **Claude 3 Haiku** — Fast and sharp reviews.
   - **GPT-4o mini** — Good reviews, cost-effective.
   - If Model A is Claude → Model B must be Gemini or GPT.
   - If Model A is GPT → Model B must be Claude or Gemini.
   - **NEVER use the same provider.**
2. **Blind review** — Show the reviewer only the diff, not the entire codebase context, to minimize bias:
   ```
   Review the following code change. You are seeing only the diff,
   not the entire project. Evaluate it along the following dimensions.
   ```
3. **Review dimensions** — Ask the reviewer for structured feedback across these categories:
   - **Correctness:** Logic errors, incorrect algorithms, off-by-one errors.
   - **Security:** Injections, XSS, auth bypass, secret exposure.
   - **Performance:** Redundant loops, N+1 queries, memory leaks.
   - **Style & Maintainability:** Naming, DRY violations, complexity.
   - **Edge Cases:** Null/empty inputs, race conditions, concurrency issues.
4. **Structured feedback format** — The reviewer must output in the following format:
   ```
   ## Review Report

   ### 🔴 BLOCKING (Do not merge without fixing)
   - [Lines X-Y] Issue: ... Recommendation: ...
   - [Line Z] Issue: ... Recommendation: ...

   ### 🟡 NON-BLOCKING (Fixing recommended)
   - [Line A] Issue: ...

   ### 🔵 SUGGESTION (Optional optimization)
   - [Line B] Idea: ...
   ```
5. **Evidence-based review** — The reviewer MUST:
   - Provide **specific line numbers** for every claim.
   - Provide **concrete alternative code** for every identified issue.
   - Avoid generic comments; perform line-by-line analysis.
6. **Token budget** — Allocate a smaller token budget to the reviewer than the doer:
   - The reviewer needs to be focused and analytical, not creative.
   - Too many tokens lead to unnecessary commentary and thought generation.
   - An ideal budget is 8K-16K tokens for the doer, and 4K-8K tokens for the reviewer.

## Phase 3 — Fix Loop: Correct the Code

**BEFORE proceeding:**

Read the review report carefully. Never ignore any 🔴 BLOCKING items.

1. **Classify and prioritize:**
   - 🔴 BLOCKING → Fix immediately.
   - 🟡 NON-BLOCKING → Fix or justify why it won't be fixed.
   - 🔵 SUGGESTION → Evaluate and implement if appropriate.
2. **Have the Doer fix the code** — Provide the same model with the diff + the review report:
   ```
   Fix the BLOCKING items identified in the following code review.
   Review Report: [report]
   Current Diff: [diff]
   ```
3. **Re-review** — Ask Model B (or a third model if appropriate) to review the updated code.
4. **Maximum 3 iterations** — If 🔴 BLOCKING items persist after the 3rd fix:
   ```
   ❌ BLOCKING items unresolved after 3 iterations:
   - ...
   
   ➡️ HUMAN ESCALATION REQUIRED. Unable to resolve agreement on: ...
   ```
5. **Escalate to a human** — Provide a clear summary:
   - What was attempted.
   - Which models were used.
   - The exact point of disagreement.
   - The reviewer's argument.
   - The doer's argument.

## Phase 4 — Final Verification

Before marking complete:

- [ ] Are the Doer and Reviewer models from different providers? (Never the same)
- [ ] Have all 🔴 BLOCKING items been resolved?
- [ ] Have 🔵 SUGGESTIONS been evaluated?
- [ ] Did the reviewer provide specific line numbers and alternative code for every claim?
- [ ] If 3 iterations were exceeded, was the issue escalated to a human?
- [ ] Does the code compile, and do all tests pass? (manual verification)
- [ ] Does the diff contain only necessary changes? (no unrelated modifications)
- [ ] Is the reviewer's report in the structured format (BLOCKING/NON-BLOCKING/SUGGESTION)?

## Red Flags — STOP and Track the Process

If you catch yourself thinking:
- "I'll use the same model, it's basically checking twice anyway" → **THIS IS NOT DOUBLE-CHECKING, IT'S CONFIRMING THE SAME BLIND SPOT TWICE.**
- "This is a simple change, it doesn't need a review" → **Simple changes hide the most insidious bugs.**
- "I don't have time, I'll merge directly" → **Reviews save time; the cost of finding a bug in production is 100x higher.**
- "The model is so good, it won't make mistakes" → **No model is perfect; different models make different errors.**
- "Let me increase the iteration limit, it might solve it next time" → **The 3-iteration rule is empirical; more iterations yield diminishing returns.**
- "Showing the full context will give me a better review" → **Blind reviews reduce bias; too much context distracts the reviewer.**

**ALL OF THESE MEAN: STOP. Return to the relevant phase.**

## Human Partner's "You are doing it wrong" Signals

**Watch for these feedback indicators:**
- "You used the same model provider, didn't you?" — Blind spot replication; different providers are mandatory.
- "Where did the reviewer pull this issue from?" — The reviewer is not evidence-based, lacking line numbers or code alternatives.
- "This code existed before, why did it change?" — Unnecessary changes made, diff is not clean.
- "The same bug is still present" — BLOCKING items were skipped or not fully corrected.
- "How many iterations did this take?" — Exceeded 3 iterations without escalating to a human.
- "This model doesn't work" — Final verification was skipped.

**When you receive these signals:** STOP. Return to the relevant phase or escalate to a human.

## Common Rationalizations

| Rationalization | Reality |
|-----------------|---------|
| "Two different models from the same provider are fine." | No, same training data + same architecture = same blind spots. |
| "A single verification step is enough." | AI models are not 100% reliable; a second perspective catches different issues. |
| "3 iterations are too few, let's do 5." | Studies show diminishing returns after 3 iterations; models begin to loop or argue. |
| "Providing the full context makes the review better." | Full context introduces bias; blind diff reviews are far more objective. |
| "This model is top-tier, it won't fail." | Every model has weaknesses; using different models covers those gaps. |
| "We're on a tight deadline, we'll review later." | "Later" never happens, and bugs in production are 100x more expensive to fix. |
| "Give the reviewer a larger token budget to see more details." | Excess tokens lead to fluff, loss of focus, and overthinking. |

## Related Skills

- **code-reviewer** — Traditional (single-model) code review, when cross-model is not required.
- **spec-first-development** — Used to write specifications for the doer beforehand.
- **security-reviewer** — Combine with cross-model loops for security-focused reviews.
- **edge-case-hunter** — Helps discover edge cases in the code being reviewed.

## Self-Review

After completing this process:

1. **Provider Check:** Are the doer and reviewer actually from different providers? (OpenAI vs. Anthropic vs. Google — not the same family)
2. **Blind Review Check:** Did the reviewer see only the diff, or the entire codebase?
3. **Evidence Check:** Does every blocking item have specific line numbers and alternative code?
4. **Token Balance Check:** Is the reviewer's token budget smaller than the doer's?
5. **Iteration Limit:** Was the 3-iteration limit respected, and escalated to a human if exceeded?
6. **Coverage Check:** Were correctness, security, performance, style, and edge cases all evaluated?
7. **Structure Check:** Is the review report in the BLOCKING / NON-BLOCKING / SUGGESTION format?
8. **Final Verification:** Does the code build, do tests pass, and is the diff clean?

**Iron Law Test:** Ask yourself:
"If the writer and reviewer were the same model, would the output have been different?"
If the answer is "yes" — the skill was applied correctly.
If the answer is "no" or "unsure" — re-evaluate the process.
