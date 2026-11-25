---
name: debug-protocol
description: Scientific debugging workflow using Root Cause Analysis and Minimal Reproducible Examples (MRE).
---

# Debug Protocol Skill

## Purpose

To replace "Shotgun Debugging" (randomly changing code) with a deterministic, scientific process.
**Goal:** Fix the *root cause*, not just the symptom.

## When to Use

- **Trigger**: When a test fails, an exception is thrown, or output is unexpected.
- **Agent**: Primarily used by `execution` mode.
- **Support**:
  - Call `quality` to write the reproduction test.
  - Call `researcher` if the error message is obscure/undocumented.

## The Scientific Method (4-Step Protocol)

### Phase 1: Observation (The MRE)

**Rule**: *If you cannot reproduce it, you cannot fix it.*

1. **Isolate**: Create a standalone script or test case that fails 100% of the time.
2. **Minimize**: Remove all code not strictly necessary to produce the error.
3. **Log**: Do not guess variables. Log them.

### Phase 2: Localization (The "Wolf Fence")

**Rule**: *Divide and Conquer.*

1. **Binary Search**: Is the data wrong at the Database? No? At the API? No? At the UI?
2. **Trace**: Follow the data flow. Find the *exact line* where the reality diverges from expectation.

### Phase 3: Hypothesis (The "5 Whys")

**Rule**: *Do not fix the symptom.*

1. **Identify**: "Variable X is null."
2. **Ask Why**: "Why is X null?" -> "Because the API returned 404."
3. **Ask Why**: "Why 404?" -> "Because the ID was undefined."
4. **Ask Why**: "Why undefined?" -> "Because of a typo in the frontend."
5. **Root Cause**: Typo in the frontend payload.

### Phase 4: Resolution & Verification

**Rule**: *Prove it.*

1. **Apply Fix**: Correct the root cause.
2. **Verify**: Run the MRE from Phase 1. It must pass.
3. **Regression**: Run the full test suite. Ensure nothing else broke.

## Debugging Scratchpad Template

*Copy this into context during a debug session.*

```markdown
## 🐞 Debug Session: [Error Name]

### 1. The Reproduction (MRE)
- [ ] Created `reproduce_issue.ts`
- [ ] Failure is deterministic (Happens every time)
- **Error Message**: `[Paste exact error]`

### 2. Localization (Wolf Fence)
- [ ] Inputs are correct? (Yes/No)
- [ ] Intermediate state correct? (Yes/No)
- **Found at**: File `X`, Line `Y`.

### 3. Root Cause Analysis (5 Whys)
1. Why? [Answer]
2. Why? [Answer]
3. **Root Cause**: [The fundamental flaw]

### 4. Resolution
- **Action**: [What did you change?]
- **Verification**: `npm test -- reproduce_issue.ts` -> ✅ PASS
```

## Anti-Patterns (Must Avoid)

- ❌ **"It should work":** Code does not care what it "should" do. It does what it is told. Look at what it is doing.
- ❌ **Console Log Spray:** Don't leave `console.log('here')` all over the code. Use structured logging or remove them after finding the bug.
- ❌ **The "Blind Fix":** Applying a StackOverflow solution without understanding *why* it applies to your specific context. (Call `researcher` first).
- ❌ **Ignoring Warning Logs:** Often the error is preceded by a warning 10 lines up. Read the *whole* log.

## Integration with Agents

- **`quality` agent**: If you are stuck on **Phase 1 (Reproduction)**, delegate to `quality`. *"I see the error, but I can't write a test for it. Quality Agent, please create a Cypress test for this UI bug."*
- **`researcher` agent**: If you are stuck on **Phase 3 (Hypothesis)**. *"I have the error 'Heap Out of Memory'. Researcher, what are the common causes for this in Node.js 18?"*
