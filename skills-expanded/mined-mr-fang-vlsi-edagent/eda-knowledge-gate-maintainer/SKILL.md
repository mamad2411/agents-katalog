---
name: eda-knowledge-gate-maintainer
description: Enforce experiment hygiene for this EDA repo. Utility skill for knowledge gate, tool reuse checks, and maintenance-log updates during scoped execution.
---

# EDA Knowledge Gate Maintainer

## When to use

Use this skill when the task needs:
1. repo experiment-hygiene gate execution,
2. enforced tool-reuse checks before adding scripts,
3. maintenance-log writeback during scoped execution,
4. diagnosis or repair of gate-hygiene failures.

## Shared Capability Boundary

This skill owns:
- invocation of the repo knowledge gate,
- tool-query evidence for scoped execution work,
- maintenance-log discipline around substantive work,
- hard-failure policy for missing gate evidence.

It does not own:
- domain conclusions,
- workflow routing,
- artifact cleanup policy,
- KB retrieval beyond gate hygiene.

## Expected Downstream Consumers

Typical consumers include:
- `workflow-scoped-execution` before and after substantive execution,
- execution skills that submit jobs, create scripts, or write experiment artifacts,
- `eda-infra-maintainer` when gate behavior itself needs repair.

## Inputs

Provide or derive:
1. interaction scope,
2. task brief path,
3. keywords for tool query,
4. whether the call is routine gate use or gate-hygiene repair/debug.

## Outputs

Return or update:
- gate command evidence,
- tool-query evidence,
- maintenance-log row in `slurm_logs/00_meta/knowledge_tool_maintenance_log.md`,
- explicit hard-failure reason if the gate contract is not satisfied.

## Knowledge And Tool Interaction

1. Treat `knowledge_gate.sh` and `tool_catalog.py query` as canonical utilities, not optional suggestions.
2. Use the task brief and current maintenance log as the minimum local evidence set for gate execution.
3. Escalate to `eda-infra-maintainer` if repeated gate failures indicate a broken policy or missing infrastructure rather than a one-off task issue.

## Hard Rules

1. Gate command failure is a hard stop.
2. Missing tool-query evidence for non-trivial work is a hard stop.
3. Missing maintenance-log update after file/script/job changes is a hard stop.
4. Do not silently continue if the task brief is missing for a scoped experiment interaction.

## Operational References

1. Load `references/invocation-scope.md` when deciding whether the call is routine `workflow-scoped-execution` usage or direct gate-hygiene repair/debug.
2. Load `references/gate-run-and-tool-query.md` when running the gate command and tool-catalog query.
3. Load `references/maintenance-log-writeback.md` when writing the maintenance-log row and artifact summary.
4. Load `references/hard-failure-policy.md` when deciding whether the interaction must stop or escalate due to missing gate evidence.
5. Load `references/checklist.md` when you need the compact pre/post checklist view.
