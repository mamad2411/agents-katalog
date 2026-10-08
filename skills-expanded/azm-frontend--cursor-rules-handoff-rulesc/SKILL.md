---
description: Critical handoff rules, implementation verification, and safety protocol
alwaysApply: true
---

# Azaman — Handoff & Safety Rules

Ensure these handoff and verification steps are followed for every session and change.

## Verification before Implementing
- ALWAYS validate assumptions with a code search in the workspace before implementing any changes.

## Handoff Rules
When concluding a task, finishing a session, or preparing work for handoff, you must explicitly detail the following five points:
1. **What changed:** Provide a clear summary of all file modifications, additions, and deletions.
2. **What did not change:** List the components, state managers, pages, or features that were left untouched.
3. **Validation run and results:** Report on manual testing, automated tests, or lints executed and their successful results.
4. **Remaining risks / unknowns:** Highlight potential side-effects, unresolved edge cases, or external dependencies.
5. **Next recommended action:** Specify clear, actionable next steps for the next developer or agent.
