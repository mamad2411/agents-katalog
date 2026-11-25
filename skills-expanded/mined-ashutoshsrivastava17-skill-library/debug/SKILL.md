---
name: debug
description: >
  Systematic debugging workflow — reproduce, isolate, diagnose, and fix
  software defects using structured root cause analysis.
  TRIGGER when: user says /debug, reports a bug, asks why something is
  broken, needs help troubleshooting an error, or wants to find the root
  cause of an issue.
argument-hint: "[error message, symptom, or description of the bug]"
user-invocable: true
---

# Systematic Debugging Workflow

You are an expert debugger. Guide the user through a structured debugging process to find and fix the root cause efficiently, avoiding shotgun debugging.

## Process

### Step 1: Gather Information

Collect the following before making any hypotheses:

| Question | Why It Matters |
|----------|---------------|
| What is the expected behavior? | Defines the contract being violated |
| What is the actual behavior? | Defines the symptom precisely |
| When did it start? | Narrows the search window |
| Is it reproducible? (Always / Sometimes / Once) | Determines debugging strategy |
| What changed recently? | Most bugs come from recent changes |
| What is the environment? | OS, runtime version, config differences |
| Are there error messages or stack traces? | Often points directly to the cause |
| Who is affected? (All users / Some / One) | Hints at data-dependent vs systemic issues |

### Step 2: Reproduce the Bug

Reproduction is the most important step. A bug you cannot reproduce is a bug you cannot confidently fix.

**Reproduction checklist:**
- [ ] Can you trigger the bug on demand?
- [ ] What is the minimal set of steps to reproduce?
- [ ] Does it reproduce in a clean environment?
- [ ] Does it reproduce with minimal data/config?

**If you cannot reproduce:**
- Check logs for the exact timestamp of the failure
- Look for race conditions or timing-dependent behavior
- Check for environment-specific config (env vars, feature flags, DNS)
- Ask: is this a Heisenbug (disappears under observation)?

### Step 3: Isolate the Problem

Narrow down systematically. Use bisection, not guessing.

**Isolation techniques:**

| Technique | When to Use |
|-----------|------------|
| Git bisect | Bug exists now but didn't before — find the commit |
| Binary search in code | Comment out half the code, see if bug persists |
| Input reduction | Simplify the input until you find the minimal trigger |
| Environment diffing | Compare working vs broken environment configs |
| Dependency pinning | Roll back dependencies one at a time |
| Feature flag toggling | Disable features to isolate the interaction |
| Log injection | Add targeted logging around suspected areas |
| Network isolation | Rule out external service issues with mocks/stubs |

**Key question at each step:** "Does the bug still occur?" — binary search the problem space.

### Step 4: Form and Test Hypotheses

Once isolated, form hypotheses and test them:

```
Hypothesis: [What you think is causing the bug]
Evidence for: [What supports this hypothesis]
Evidence against: [What contradicts it]
Test: [How to confirm or refute — be specific]
Result: [What happened when you tested]
```

**Rules for hypotheses:**
- Generate at least 2 hypotheses before testing any
- Test the most likely hypothesis first
- Each test must be able to DISPROVE the hypothesis, not just confirm it
- If a test is inconclusive, it was a bad test — design a better one

### Step 5: Identify Root Cause

Distinguish between:

| Type | Example | Action |
|------|---------|--------|
| **Root cause** | Buffer overflow in parser | Fix the parser |
| **Contributing cause** | No input validation on caller | Fix both |
| **Symptom** | Application crashes | Do not "fix" the crash — fix the cause |
| **Trigger** | Specific input pattern | Use in regression test |

Use the "5 Whys" technique:
1. Why did the server return 500? — Unhandled null pointer
2. Why was the pointer null? — User record not found
3. Why was it not found? — Lookup used email, user changed email
4. Why did email change break lookup? — No index on the new email
5. Why is there no index? — Migration was not run in production

Root cause: Missing migration deployment step.

### Step 6: Fix and Verify

**Before fixing:**
- [ ] Write a failing test that reproduces the bug
- [ ] Confirm the test fails for the right reason

**The fix:**
- [ ] Fix the root cause, not just the symptom
- [ ] Check for the same pattern elsewhere in the codebase
- [ ] Keep the fix minimal — do not mix bug fixes with refactoring

**After fixing:**
- [ ] The reproduction test now passes
- [ ] No existing tests broke
- [ ] The fix works in the same environment where the bug was found
- [ ] Edge cases are covered (null, empty, boundary values)

### Step 7: Document Findings

```markdown
## Bug Report

**Summary:** [One-line description]
**Root Cause:** [Technical explanation]
**Fix:** [What was changed and why]
**Impact:** [Who was affected and for how long]
**Prevention:** [What would have caught this earlier — test, lint rule, monitoring]
**Timeline:**
- [timestamp] — Bug introduced (commit/deploy)
- [timestamp] — Bug reported
- [timestamp] — Bug diagnosed
- [timestamp] — Fix deployed
```

## Common Bug Categories

| Category | Typical Symptoms | First Things to Check |
|----------|-----------------|----------------------|
| Off-by-one | Wrong count, missing last item, index error | Loop bounds, array indexing, fence-post logic |
| Race condition | Intermittent failures, works in debugger | Shared state, async operations, locks |
| Null reference | Crash, undefined behavior | Optional values, missing data, failed lookups |
| Resource leak | Slow degradation, OOM after hours/days | Unclosed connections, missing cleanup, growing caches |
| Encoding | Garbled text, wrong characters, hash mismatch | UTF-8 vs Latin-1, BOM, line endings, binary mode |
| Timezone | Wrong times, off by N hours, DST glitches | UTC storage, timezone conversion, DST transitions |
| Floating point | Tiny differences, comparison failures | Equality checks on floats, currency math |
| Dependency | Works locally, fails in CI/prod | Version mismatch, transitive deps, lockfile drift |

## Edge Cases

- If the bug is in a third-party library, confirm with a minimal reproduction before filing upstream
- If the bug is intermittent, add logging and monitoring first — do not guess
- If the bug is in production and causing harm, apply a temporary mitigation first, then do proper root cause analysis
- If multiple bugs are interacting, isolate and fix them one at a time
