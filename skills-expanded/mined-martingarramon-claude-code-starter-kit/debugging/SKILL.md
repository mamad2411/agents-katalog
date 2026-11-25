# Skill: Systematic Debugging

## When to Use
Activate when anything is broken, behaving unexpectedly, or producing wrong output.
This includes runtime errors, incorrect behavior, build failures, flaky tests, and
"it worked yesterday" situations.

## Core Principle
Root cause first. No random patches. Changing things until it works is not debugging --
it's gambling. Every fix must be traceable to a verified cause.

## Process

### 1. Reproduce
Before anything else, reproduce the problem reliably.
- Get the exact error message, stack trace, or wrong output
- Identify the minimal steps to trigger it
- Note what changed recently (new code, dependency update, config change, environment)
- If you cannot reproduce it, say so -- do not proceed to fix a ghost

### 2. Gather Evidence
Read the relevant code. Read the logs. Check the state.
- Trace the execution path from input to error
- Check recent changes (git log, git diff) for obvious culprits
- Look at the actual values, not what you assume they should be
- Check environment: versions, configs, env vars, permissions

### 3. Form a Hypothesis
Based on the evidence, state a specific hypothesis:
- "The error occurs because X calls Y with a null argument when Z is empty"
- Not "something might be wrong with the database connection"
- A good hypothesis is falsifiable -- you can design a test that proves it wrong

### 4. Test the Hypothesis
Design the smallest possible test to confirm or reject:
- Add a log statement at the suspected point
- Write a minimal reproduction case
- Check a specific value at a specific moment
- If the hypothesis is wrong, go back to step 2 with the new information

### 5. Fix and Verify
Apply the minimal fix that addresses the root cause:
- Change one thing at a time
- Run the reproduction case to confirm the fix works
- Run the broader test suite to check for regressions
- If the fix is a workaround (not a root cause fix), document why

### 6. Document
Update the relevant knowledge:
- What was the root cause?
- What was the fix?
- What signal would have caught this earlier?
- Should a rule be added to prevent recurrence?

## Anti-Patterns (Do Not Do These)
- **Shotgun debugging:** Changing multiple things at once hoping one of them works
- **Cargo cult fixes:** Copying solutions from Stack Overflow without understanding why they work
- **Blame the tool:** Assuming the framework/library has a bug before checking your own code
- **Fix the symptom:** Catching and silencing an exception instead of fixing why it was thrown
- **Time pressure skip:** Skipping reproduction because "we need to fix this fast"

## Output Format
When reporting a debug session:

```
## Bug: [Short description]

**Symptom:** [What was observed]
**Root cause:** [Why it happened]
**Fix:** [What was changed]
**Verification:** [How the fix was confirmed]
**Prevention:** [What would catch this earlier next time]
```
