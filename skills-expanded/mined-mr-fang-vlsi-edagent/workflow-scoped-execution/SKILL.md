---
name: workflow-scoped-execution
description: "Execute one scoped EDA task under governed gates: run bootstrap checks, validate artifacts, and return execution evidence."
---

# Workflow Scoped Execution

## Role Boundary

`workflow-scoped-execution` is the scoped execution workflow owner.

It owns:
- governed execution for one concrete task,
- submission hygiene,
- artifact validation,
- post-run closeout.

It does not own:
- global entry policy,
- non-execution workflow ownership,
- cross-turn recursion policy,
- global self-update policy for the full skill system.

`workflow-scoped-execution` should be used only when:
1. it is the selected workflow owner for one bounded execution task, or
2. another workflow owner explicitly delegates one governed execution stage to it.

## Use This Skill When

Use `workflow-scoped-execution` for experiment, debug, flow, baseline, handoff, monitoring, or infrastructure tasks that already have a scoped execution brief and need explicit gates and artifacts.

## Inputs

Provide or derive:
1. scoped objective,
2. target design/config set,
3. required output artifacts,
4. comparison-policy lock if a claim/comparison is requested.
5. selected skill set or explicit statement that no additional skill routing is needed.

## Knowledge And Tool Interaction

1. If the task needs shared KB retrieval or shared tool-reuse evidence, delegate that work to `eda-context-accessor` instead of re-specifying retrieval logic locally.
2. If `eda-context-accessor` returns `kb_feedback_decision != none`, record that feedback in the execution summary and route KB/infrastructure follow-up to `eda-infra-maintainer` when the change is not purely local.
3. Keep `workflow-scoped-execution` focused on execution hygiene:
- run `scripts/common/knowledge_gate.sh` for governed execution startup,
- update `slurm_logs/00_meta/knowledge_tool_maintenance_log.md`,
- update `docs/knowledge_base/90_HYPOTHESIS_VALIDATION_LOG.md` when a hypothesis was actually tested.
4. When a batch completes and the outcome should be reused beyond the immediate turn, delegate `log -> result -> conclusion -> experience` extraction to `eda-experiment-phenomenology-analyst` before handing off to `control-postrun-retro` or a future `control-theory-veto`.

## Execution Rules

1. Announce selected skills and first action.
2. Execute fully unless the user explicitly asks for plan-only behavior.
3. Keep artifact paths explicit.
4. Every experiment submission must create a canonical monitor file immediately; do not leave monitor generation as manual follow-up.
5. Prefer the reusable monitor stack (`scripts/debug/progress_monitor.py` or `scripts/debug/progress_monitor.sh`) over ad hoc markdown.
6. Immediately report monitor/manifest/job ids after submission.
7. Do not close a submission task before monitoring visibility exists.
6. For algorithmic claims, enforce `vanilla_replace` as primary baseline.

## Outputs

Return or update:
- canonical monitor path,
- canonical manifest path,
- key artifact paths,
- structured evidence-lift artifact paths when experiment phenomenology extraction was required,
- execution verdict,
- next constrained action.

## Operational References

Load only the parts needed for the current task:
1. Load `references/workflow-scoped-execution-checklist.md` when starting or closing a normal `workflow-scoped-execution` execution and you need the full bootstrap/pre-submit/post-run checklist.
2. Load `references/execution-gates.md` when the task involves submission gating, route/CTS preflight, testcase-backed DC/Innovus checks, or root-cause mode for non-convergence.
3. Load `references/output-and-stop-policy.md` when deciding whether the task is complete, whether reporting is sufficient, or whether a hard-stop condition blocks closeout.
4. Load `references/postrun-improvement.md` when the current loop exposed a repeated execution gap and you need to decide the smallest acceptable improvement action.
