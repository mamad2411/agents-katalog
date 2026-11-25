---
name: closeout
description: End a work session cleanly: report what happened, commit safe files, and leave one clear next step for whoever resumes. Use when running `coderail done` or writing the Owner Receipt.
---

# closeout

Compatibility guidance for choosing the result passed to the single
`coderail done` completion authority.

## Action

In workspace-v1 use the host workspace skill and `workspace paths`. Code and
its process archives share one exact task-scoped commit in the same repository.
Detachment is not closeout, does not mark delivery success, and preserves history.

```bash
python .coderail/coderail.py done
```

For a verified partial boundary, use:

```bash
python .coderail/coderail.py done --result stage-complete
```

If acceptance items exist, include every `--accept-status` on that first call.
Cheap preflights run before verification. A valid same-transaction receipt may
carry CI into final checks; direct calls and invalid receipts run their gates.

## Owner channel

On success, return only the generated 3-6 sentence Owner Receipt. Match the
user's language. In Chinese, necessary English terms require a Chinese note;
task IDs, paths, lifecycle labels, commit receipts, and internal gate names do
not belong in this channel unless the owner asks.

Use `--owner-locale zh-CN` or `en` to override the saved or explicit host
preference. Otherwise CodeRail falls back deterministically to English and
reports unsupported locale or rendering diagnostics without repeating any
closeout effects. Never recreate the retired fallback report.

## Agent channel

Use the Agent Blackboard and Technical Report for task result, exact checks,
safe files, Git receipt, handoff state, recovery anchor, and next executable
step. Do not make the blackboard a new lifecycle authority.

## Rules

- Do not include project-specific examples from another repository.
- Do not stop with only a narrative summary.
- Do not expand the Owner Receipt into the old seven-section technical packet.
- Do not run the legacy `finish` adapter as a second closeout path.
- Do not manually repeat persistence, staging, or commit work after `done`.
- Do not repeat a passing same-transaction CI; use its compact summary and open
  the named `.coderail/reports/` log only for detailed diagnosis.
- Do not downgrade failed verification, scope violations, damaged required
  facts, or an incomplete transaction into presentation warnings.
- If useful work is not verified, keep the task active and state the next
  validation step instead of manufacturing a checkpoint.
