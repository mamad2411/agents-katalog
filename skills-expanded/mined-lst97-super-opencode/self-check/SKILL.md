---
name: self-check
description: Post-implementation validation to enforce the Definition of Done (DoD) and prevent hallucinations.
---

# Self-Check Skill

## Purpose

To validate work **after** implementation but **before** handoff.
This is the "Check" in PDCA. It prevents the "It works on my machine" (or "It works in my context window") syndrome.

**ROI Metric**: Catching a syntax error here costs 50 tokens. Catching it in a PR review costs 5,000 tokens + human time.

## When to Use

- **Trigger**: Immediately after `execution` mode finishes writing code.
- **Trigger**: Before the `backend` agent hands off to `frontend`.
- **Trigger**: Before any `git commit`.

## The "Proof of Work" Protocol

### 1. The Build Check (Syntax)

**Rule**: *Code that doesn't build doesn't exist.*

- Did you run the build/transpile command? (`npm run build`, `go build`, etc.)
- **Evidence**: Paste the exit code and the last 3 lines of output.

### 2. The Logic Check (Behavior)

**Rule**: *Claims require proof.*

- **Forbidden Phrase**: "I ran the tests and they passed." (This is often a hallucination).
- **Required Action**: Run the test command via `run_command` and capture the actual output.
- **Evidence**: Paste the `Total: X Passed, 0 Failed` line.

### 3. The Contract Check (Requirements)

**Rule**: *Did you solve the user's problem?*

- Map every constraint from the original prompt to a specific line of code or test case.

### 4. The Hygiene Check (Cleanup)

**Rule**: *Leave no trace.*

- Scan for: `console.log("here")`, `debugger`, commented out code blocks, or `TODO` comments added by you.
- **Action**: Remove them.

## Execution Template

*Copy this into the context window to validate your work.*

```markdown
## ✅ Self-Check Validation

### 1. Build Verification
- **Command**: `npm run build`
- **Output**:
  ```text
  > build
  > tsc
  ✨ Done in 2.45s.
  ```

- **Status**: [ PASS / FAIL ]

### 2. Test Verification

- **Command**: `npm test -- user.service.test.ts`
- **Output**:

  ```text
  PASS src/services/user.service.test.ts
  Tests: 3 passed, 3 total
  ```

- **Status**: [ PASS / FAIL ] -> *If FAIL, trigger `reflexion` skill.*

### 3. Requirements Mapping

| Requirement | Implemented? | Evidence (File/Line) |
| :--- | :--- | :--- |
| "Users must have a role" | ✅ | `UserSchema.ts:12` (Zod enum) |
| "Passwords must be hashed" | ✅ | `AuthService.ts:45` (bcrypt call) |

### 4. Code Hygiene

- [ ] Removed debug `console.log`s?
- [ ] Removed temporary comments?
- [ ] Ran Linter? (`npm run lint`)

### 🏁 Final Verdict: [ READY TO SHIP / NEEDS FIXING ]

## Red Flags (Hallucination Detection)

If you see these patterns in your own reasoning, **STOP**:

| Red Flag | Why It's Bad | Correction |
| :--- | :--- | :--- |
| *"The code looks correct."* | Visual inspection is insufficient. | Run the code. |
| *"I updated the tests."* | Did you *run* them? | Run the tests. |
| *"This should fix the error."* | Hope is not a strategy. | Verify the fix. |
| *"I'll assume the DB is running."* | Assumption is the mother of all failures. | Check connection. |

## Integration with Agents

- **`execution` mode**: Must run `self-check` before declaring `Status: COMPLETE`.
- **`pm-agent`**: Rejects any task update that does not include a `self-check` artifact.
- **`reflexion` skill**: If `self-check` results in **FAIL**, the agent must immediately enter `reflexion` mode to analyze the root cause before retrying.
