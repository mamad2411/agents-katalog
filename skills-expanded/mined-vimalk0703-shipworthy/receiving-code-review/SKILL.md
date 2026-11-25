---
name: receiving-code-review
description: Process code review feedback with technical verification — not performative agreement. Fix real issues, push back on incorrect feedback with evidence.
invoke_when: Use when processing code review feedback, addressing reviewer comments, or responding to PR review requests.
---

# Receiving Code Review

## Core Principle

**Technical verification over performative agreement.** Don't accept feedback just because it comes from a reviewer. Verify that the feedback is correct before acting on it.

## Processing Feedback

For each issue raised:

### 1. Understand the Issue
Read the feedback carefully. What exactly is the concern? Is it about correctness, style, architecture, or performance?

### 2. Verify the Claim
- If the reviewer says "this will break when X": test it. Does X actually cause a break?
- If the reviewer says "this violates architecture rule Y": check architecture.md. Does it?
- If the reviewer suggests "use pattern Z instead": is pattern Z actually better here?

### 3. Respond with Evidence

**If the feedback is correct:**
- Fix the issue
- Show the fix with test evidence
- Thank the reviewer for catching it

**If the feedback is incorrect:**
- Explain why with evidence (test results, documentation, architecture.md)
- Don't be confrontational — provide facts
- If it's a judgment call, explain your reasoning

**If the feedback is partially correct:**
- Acknowledge the valid part and fix it
- Explain why the other part doesn't apply

## Anti-Patterns

- **Performative agreement** — "Yes, you're right, I'll fix that" without verifying
- **Defensive rejection** — dismissing feedback without investigation
- **Scope creep** — using review feedback as an excuse to refactor unrelated code
- **Fix-and-forget** — fixing the symptom without understanding the root cause

## After Addressing All Feedback

1. Run the full test suite
2. Verify all Critical and Important issues are resolved
3. Summarize what was changed and why
4. Request re-review if significant changes were made
