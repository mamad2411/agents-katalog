---
name: pr-converge
description: Converge an open pull request to merge-ready state.
---

## Intent

Use this skill when the task is to address review feedback, clear CI, and bring a pull request to merge readiness.

## Inputs

- Target pull request or the currently checked out pull request.
- Review comments, CI failures, and repository validation requirements.

## Execution

1. Retrieve active review comments and open threads.
2. Evaluate each comment against the current code and decide whether it requires a fix, explanation, or no action.
3. Implement focused fixes for valid issues and add regression coverage when the comment reveals a bug.
4. Reply to each comment with a concise technical explanation.
5. Re-run the minimal validation needed by the touched areas.
6. Check CI status and iterate until failures are resolved.

## Validation

1. Confirm that review threads are responded to and ready for resolution.
2. Confirm that local validation is green.
3. Confirm that CI is green before declaring convergence.

## Safety

- Do not resolve comments without explanation.
- Keep each fix minimal and scoped to the review issue it addresses.
