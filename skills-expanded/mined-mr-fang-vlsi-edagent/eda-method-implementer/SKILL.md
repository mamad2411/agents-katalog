---
name: eda-method-implementer
description: Implement EDA research methods from approved hypothesis plans, with integration discipline, measurable contracts, and minimal-risk iteration.
---

# EDA Method Implementer

## When to use

Use this skill when moving from experiment design to actual method/code implementation.

## Knowledge And Tool Interaction

1. Load the approved hypothesis and experiment-plan artifacts before touching code.
2. If the task needs shared KB/tool lookup before implementation planning, delegate that step to `eda-context-accessor`.
3. If `eda-context-accessor` reports `maintain`, `update`, `overturn`, or `add`, carry that recommendation into the implementation handoff so later validation/infra skills can act on it.
4. Write implementation decisions and validation commands into explicit artifacts so later validation and retro skills can reuse them.

## Workflow

1. Load approved hypothesis and experiment plan artifacts.
2. Query tool catalog before adding new scripts:

```bash
python3 scripts/common/tool_catalog.py query <keyword1> <keyword2>
```

3. Define implementation contract:
- target files/modules,
- expected behavior delta,
- metrics to validate change.
4. Implement minimal viable patch first, then iterate.
5. Run required validation commands and link outputs.
6. Prepare versioned checkpoint handoff to `git-version-control`.

## Outputs

1. `implementation_plan.md`
2. `implementation_change_log.md`
3. `validation_command_log.md`

## Hard rules

1. Do not implement without linked hypothesis ID.
2. Keep each patch testable and reversible.
3. Record known side effects and unresolved risks.

## Reference

Load when needed:
1. `references/implementation-contract-checklist.md`
