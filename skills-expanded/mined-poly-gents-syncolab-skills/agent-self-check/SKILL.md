---
name: agent-self-check
description: "Before declaring work complete, run a structured self-assessment that catches the most common 'shipped half a thing' failures (missing tests, missing docs, missing observability, missing handoff)."
---

# Agent self-check

The cheapest way to raise agent quality is to add a structured self-check before declaring done. Most "the agent shipped a regression" reports trace back to a missing self-check step.

## When to run

- Before posting "done" / "complete" in any planning task you own.
- Before closing a Jira / GitHub Issue.
- Before sending a customer-facing answer that involved tool calls.

## The self-check

Ask yourself each question, IN ORDER, and answer it explicitly in your reply (or in the task comment). Do not skip.

1. **Did I actually run the change?** Either a unit test, a smoke run, or a real call to the tool I claim to have used.
2. **Did I check for the silent failure mode?** What is the worst thing that could be wrong with my output that LOOKS right? Did I check for it?
3. **Did I update the related docs/playbooks?** If the change is permanent or recurring, write it down. Use `sks_docs_propose_patch` or `initiative_file_upload`.
4. **Did I leave an observability hook?** For code: a log line / metric / alert. For ops: a planning comment with the timestamps and values.
5. **Did I follow my own playbooks?** Did I trigger `production-validation`, `release-readiness-checklist`, etc. when the work calls for them?
6. **Did I tell the right people?** A handoff packet if someone else continues; a customer-facing summary if the user is waiting.

## When to add a step

If you find a gap in the self-check, fix it in the same turn — do not declare done. If the gap requires a tool you don't have, run `discover-capability-and-request-access` and pause.

## Anti-patterns

- Self-checking by re-stating the original goal.
- Skipping the silent-failure-mode question.
- Marking done with TODO comments still in the diff.
