---
name: moth-verify-fix
description: Verify bug fixes with the smallest relevant command. Use after patching a test, build, typecheck, lint, runtime, framework, or package error and before recording whether a Moth-analyzed fix worked.
---

# Moth Verify Fix

## Command Choice

Choose the narrowest command that can disprove the fix:

1. Original reproduction command when available.
2. Focused test for the changed module or failing case.
3. Typecheck for TypeScript type errors.
4. Lint for ESLint or formatting-rule failures.
5. Build only when the issue is build-time or no narrower check exists.

## Workflow

1. Run the smallest command that covers the changed behavior.
2. If it fails, use the new output as the next error context instead of guessing.
3. If it passes, run one broader command only when the change touched shared behavior.
4. Auto-call `remember_fix_result` **ONLY** after a fix was attempted and the verification result was verified as `passed` or `failed`.
   - If verified passed: `verification_result: "passed"`
   - If verified failed: `verification_result: "failed"` and include the new error output in `notes`.
5. You must **NEVER** call `remember_fix_result` if:
   - Only a fix was suggested (user hasn't run it and you haven't applied it)
   - You didn't apply the changes
   - You didn't run the verification command yet
   - The result is ambiguous or unknown

## Guardrails

- Do not call a fix successful without a relevant command or reproduction result.
- Do not call `remember_fix_result` for suggestions, unapplied changes, missing verification, ambiguous results, or guesses.
- Do not run unrelated expensive checks first.
- Do not record secrets or full sensitive logs in fix memory.