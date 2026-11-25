---
name: verification-before-completion
description: Gate function — no completion claims without fresh verification evidence. Prevents shipping broken code by requiring proof that the change works.
invoke_when: Use when claiming any work is complete, saying "done", or asserting something "should work" or "is ready" — verification must precede completion claims.
---

# Verification Before Completion

## The Iron Rule

**NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE.**

## The 5-Step Gate

### Step 1: Identify the Proof Command
What command proves this works?
- `npm test` / `pytest` / `go test ./...`
- `npm run build` / `tsc --noEmit`
- `npm run lint`
- A specific test file: `npx vitest run src/services/user.test.ts`

### Step 2: Run It
Execute the command. Do not skip this step.

### Step 3: Read the Output
Read the FULL output — not just "it passed." Look for warnings, skipped tests, deprecation notices.

### Step 4: Verify Your Claim Matches Reality
Does the output actually prove what you're about to claim? "All 47 tests pass" is verifiable. "It should work correctly" is not.

### Step 5: Assert with Evidence
Now claim completion, citing evidence:
- "All 47 tests pass (including 3 new tests for the user service)"
- "Build completes with 0 errors and 0 warnings"

## Red Flag Language

If you catch yourself about to say any of these, STOP — you haven't verified:
- "should work"
- "probably fine"
- "I believe this is correct"
- "this looks right"
- "I'm confident that..."
- "based on my understanding..."

Replace with: "Let me verify." Then run the command.
