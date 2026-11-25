---
name: review-remediation-gate
description: Close review findings deterministically, remediate blocking issues, and prove review closure. Use when the user says to fix review comments, address review findings, run a review-remediation pass, close out blockers, or finish work only after review issues are resolved.
license: Apache-2.0
metadata:
  author: Mike Willbanks
  repository: https://github.com/mwillbanks/agent-skills
  homepage: https://github.com/mwillbanks/agent-skills
  bugs: https://github.com/mwillbanks/agent-skills/issues
  purpose: Remediate review findings with evidence-backed closure
---

# Review Remediation Gate

Use this skill when work has already been reviewed and the next step is to close findings, not re-litigate the whole task.

This is a closure skill. It exists to prevent weak "fixed" claims, review steering, and partial remediation from being treated as completion.

## When to use

Use this skill for prompts like:

- "Fix the review findings"
- "Close the blocking comments"
- "Run a review-remediation pass"
- "Address the reviewer feedback and prove it is resolved"
- "Finish only after the review issues are closed"

Use it when the work already has findings, comments, or a review artifact and the goal is deterministic closure.

## Required workflow

1. Read the original intent, the review findings, and the current implementation state.
2. Classify every finding as blocking, adjacent, validation-related, documentation-related, or intentionally accepted by the user.
3. Convert each finding into a concrete remediation action with exact file scope and a verification step.
4. Make the smallest complete fix that actually resolves the finding.
5. Re-run the relevant validation or proof step after the fix.
6. Record whether each finding is resolved, still open, or no longer applicable, with evidence.
7. Stop only when every blocking finding is actually closed or the user has explicitly accepted the residual risk.

## Non-negotiable rules

- Do not mark a finding resolved without evidence.
- Do not rewrite findings into softer language to make them look closed.
- Do not claim "done" while any blocking finding still lacks verification.
- Do not broaden scope unless the finding genuinely requires a coupled fix.
- Do not hide an unresolved issue behind a summary that only describes the intended fix.
- Do not convert a remediation pass into a redesign unless the review evidence proves the redesign is necessary.

## Remediation discipline

- Preserve the original review context.
- Keep the fix traceable from finding to code change to validation output.
- Prefer the smallest safe patch that closes the issue.
- If a finding is invalid, explain why with evidence instead of silently dropping it.
- If the issue cannot be fixed, state the blocker precisely and name the missing condition.

## Definition of done

This skill is complete only when all of the following are true:

- every blocking finding has a concrete fix or an explicit user-accepted exception
- each claimed fix has a verification step
- the final state is truthful about any remaining risk
- the closure report distinguishes resolved, deferred, invalid, and accepted findings

## Final output contract

Report all of the following:

- original finding text
- remediation taken
- verification performed
- outcome for each finding
- any residual risk or accepted exception

If the work is still blocked, say exactly what remains open and what would unblock it.
