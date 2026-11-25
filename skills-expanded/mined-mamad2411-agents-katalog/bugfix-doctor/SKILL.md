---
name: bugfix-doctor
description: "Diagnose and fix broken code for non-coders with a reproduce, isolate, fix, verify workflow. Use this skill whenever the user says something is broken, shows an error, reports a failed build/test/dev server, says they do not understand what went wrong, or asks why the app stopped working."
---

# Bugfix Doctor

Use a calm, evidence-first debugging workflow. The user may not know programming terms, so translate errors before diving into implementation.

## 1. Reproduce The Symptom

Start by gathering the smallest useful facts:

- What did the user expect?
- What actually happened?
- What command, page, button, or workflow triggered it?
- What error text, screenshot, console log, or terminal output is available?

If an error is provided, explain it in plain English before making changes. If no error is available, inspect the likely command, page, or file path and state what evidence you are looking for.

## 2. Isolate The Cause

Form a ranked hypothesis list, then test the top hypothesis with the least invasive evidence:

- Read the relevant files and recent changes.
- Run the smallest command that reproduces the failure when safe.
- Use logs, stack traces, failing test names, or UI behavior to narrow the cause.
- Point to the exact file or component involved.

Avoid broad refactors during diagnosis. If more than one cause remains plausible, say what would distinguish them.

## 3. Fix The Smallest Thing

Apply the minimum change that addresses the verified cause.

Good bugfix behavior:

- Keep the diff focused on the broken behavior.
- Preserve unrelated user changes.
- Prefer one to three files for a single bug unless the evidence clearly requires more.
- Explain the change in plain English before or immediately after editing.
- If the fix is uncertain, frame it as a safe experiment and verify it.

Do not blame the user, hide uncertainty, or add new features while fixing the bug.

## 4. Verify The Fix

Use the same path that failed:

- Rerun the failed command, test, or page flow.
- Confirm the original symptom is gone.
- Run adjacent checks when risk is meaningful, such as a nearby test, build, or manual browser path.
- If verification cannot run, explain the blocker and give the exact manual test steps.

## 5. Final Report

Return exactly these sections:

1. **Symptom**: what the user saw, in plain English
2. **Cause**: what went wrong and why it broke
3. **Fix**: files changed and a one-line explanation per file
4. **Verification**: commands or manual steps used to confirm the fix
5. **Prevention**: one practical way to avoid this class of bug next time

Keep the final answer concise. Include technical detail only where it helps the user trust or repeat the fix.
