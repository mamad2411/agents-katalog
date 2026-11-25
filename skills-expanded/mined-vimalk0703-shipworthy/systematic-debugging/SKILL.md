---
name: systematic-debugging
description: 4-phase root cause investigation — observe, hypothesize, test, implement. Prevents trial-and-error debugging and enforces a 3-fix limit before reassessment.
invoke_when: Use when debugging a bug report, investigating a failing test, diagnosing unexpected behavior, or when previous fixes have not resolved the issue.
---

# Systematic Debugging

## The Anti-Pattern This Prevents

Trial-and-error debugging: change something, see if it works, repeat. This approach takes 2-3 hours and has a 50% first-time fix rate. Systematic debugging takes 15-30 minutes with a 95% first-time fix rate.

## The 4 Phases

### Phase 1: Observe
**Gather evidence before forming theories.**
- What exactly is the symptom? (error message, wrong output, crash)
- When does it happen? (always, sometimes, only in production)
- What changed recently? (git log, recent deploys, config changes)
- Can you reproduce it reliably?
- Read the FULL error message and stack trace

### Phase 2: Hypothesize
**Form testable theories based on evidence.**
- What could cause this symptom?
- List 2-3 hypotheses, ranked by likelihood
- Each hypothesis must be testable — "something is wrong" is not a hypothesis
- Consider: is this a code bug, a data bug, a config bug, or an environment bug?

### Phase 3: Test
**Test each hypothesis methodically.**
- Start with the most likely hypothesis
- Design a test that would CONFIRM or ELIMINATE the hypothesis
- Run the test. Read the results carefully.
- If confirmed: proceed to Phase 4
- If eliminated: move to the next hypothesis

### Phase 4: Implement
**Fix the root cause, not the symptom.**
- Write a test that reproduces the bug FIRST (TDD applies to bugs too)
- Implement the fix
- Run the reproducing test — it should pass now
- Run the full test suite — nothing else should break
- Verify the fix in the original context where the bug was observed

## The 3-Fix Rule

**If 3 attempted fixes don't resolve the issue, STOP.**

You're likely:
- Fixing a symptom, not the root cause
- Working with wrong assumptions
- Dealing with an architectural issue that requires a different approach

When you hit the 3-fix limit:
1. Step back and re-examine your assumptions
2. Re-read the error messages and logs from scratch
3. Consider whether the bug is in a different layer than you're looking at
4. Discuss with the user before proceeding

## Common Debugging Mistakes

1. **Changing multiple things at once** — change one thing, test, repeat
2. **Not reading the full error** — the answer is often in the stack trace
3. **Assuming the bug is where you're looking** — it's often one layer away
4. **Not checking recent changes** — `git log` and `git diff` are your friends
5. **Fixing the symptom** — "add a null check" without asking why it's null
