---
name: forge-research
description: Run evidence-led market, competitor, repository, documentation, review, file, and video research. Use when product decisions need current external or supplied evidence.
license: MIT
---

# forge-research

Read \`${CLAUDE_PLUGIN_ROOT}/references/WORKFLOW_PROTOCOL.md\` before mutating project state.

## Inputs

research questions; depth; permitted sources; time and budget limits.

## Outputs

evidence ledger with source, date, observation, confidence, kind, decision supported, staleness, and license constraints.

## Workflow

Prefer deterministic retrieval and installed research skills. Respect access controls. Inspect repository licenses before reuse. Separate fact, opinion, and inference. Keep unresolved questions queued while useful research remains.

Honor the current permission mode. Use only task-relevant tools and installed skills. Log consequential actions. Persist outputs before reporting success.

## Failure handling

On tool failure, record the command, safe retry state, and blocker. Retry only idempotent work. Never convert a missing credential, unavailable provider, failed test, or incomplete adapter into a success claim.

## Example

\`/forge-research competitor complaints and open-source tutoring engines\`

## Evaluation case

Every decision claim links to a source record and unlicensed code is rejected.
