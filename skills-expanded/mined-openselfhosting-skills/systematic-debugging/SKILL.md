---
name: systematic-debugging
description: "Diagnoses software bugs, crashes, incorrect behavior, and failing tests by reproducing the symptom, tracing evidence to a root cause, applying a minimal fix, and verifying the result. Use when debugging code or investigating a regression."
license: MIT
metadata:
  author: OpenSelfHosting
  version: "1.0.0"
---

# Systematic Debugging

## Goal
Find and verify the root cause before changing code. Prefer the smallest safe correction that explains the observed failure.

## Workflow
1. **Frame the failure.** Restate actual behavior, expected behavior, scope, environment, and the exact error or reproduction steps. Ask one targeted question only if a critical fact is missing and cannot be inferred safely.
2. **Inspect state and instructions.** Read applicable project guidance; inspect relevant files, recent changes, and the working tree. Never overwrite or discard pre-existing user changes.
3. **Reproduce.** Run the smallest relevant test, command, or manual sequence. Capture the exact output. If reproduction is impossible, explain why and mark the cause as unverified.
4. **Form ranked hypotheses.** Link each hypothesis to evidence and state what observation would distinguish it from alternatives. Change one variable at a time when feasible.
5. **Trace the path.** Follow data and control flow across boundaries. Check assumptions, types, state transitions, timing, configuration, dependency versions, error handling, and environment differences relevant to the symptom.
6. **Find the root cause.** Explain the causal chain from defect to symptom. Do not present a correlated log line or a downstream failure as the cause without evidence.
7. **Apply a minimal fix.** Keep unrelated refactors out. Preserve public contracts unless the requested change explicitly includes a contract change.
8. **Add a regression check.** Prefer a focused test that fails before the fix and passes afterward. When automated coverage is impractical, provide reproducible manual verification steps.
9. **Verify.** Run the focused test first, then additional relevant tests, lint, type checks, or builds according to risk. Report exactly which commands ran and their outcomes.
10. **Review the diff.** Look for unintended files, changed behavior outside scope, leaked secrets, debug code, and weakened tests.

## Required final report
- Symptom and reproduction status.
- Root cause and evidence (or remaining hypotheses if not proven).
- Files changed and why.
- Verification commands and actual results.
- Remaining risk or follow-up work.

## Safety and honesty
- Do not claim a test passed unless it was executed and returned success.
- Do not hide a failed or skipped check.
- Do not run destructive commands, production writes, migrations, or broad cleanup without explicit authorization.
- Do not reset the working tree, force-push, or delete data as a debugging shortcut.
- Treat logs and pasted output as potentially sensitive; redact credentials and personal data.
