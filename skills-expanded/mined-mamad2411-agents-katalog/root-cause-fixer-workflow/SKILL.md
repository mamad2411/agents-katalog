---
name: root-cause-fixer-workflow
description: "Use when concrete failure evidence requires root-cause analysis, minimal patching, and regression proof as the Root Cause Fixer."
---

# Root Cause Fixer Workflow

Read `core-workflow-contract` first. This skill owns only the Root Cause Fixer role.

## Role Boundary

Own concrete failure evidence, root-cause analysis, minimal patching, and regression proof. Do not do speculation-driven refactors, broad cleanup, or unrelated redesign.

## Required Flow

1. Consume the frozen PM dispatch packet (six-block format from `core-workflow-contract`), then state the broken behavior, expected behavior, observed evidence, and falsification condition.
2. Reproduce or localize the failure when practical before editing.
3. Trace the actual runtime path instead of patching symptoms.
4. Before editing, read the target file's public surface/exports, the immediate failing caller/callee, and any obvious shared utility or local pattern in the failure path.
5. Make the smallest fix that addresses the cause and preserves surrounding behavior. Do not refactor adjacent code or add speculative hardening outside the proven failure.
6. Follow RED-GREEN-REFACTOR: preserve the reproduced failure as RED, make the smallest GREEN fix, then refactor only under passing evidence. If RED is technically impractical, record why and provide an alternative reproducible check for independent review.
7. Verify the original symptom no longer reproduces, or state the blocker precisely.

## Specialist Ask Boundary

Follow the Specialist Ask Boundary in `core-workflow-contract`. Do not ask users directly.

## Task-Type Routing

- `task_type=fix`: own failure-backed root-cause investigation and the resulting minimal patch when the same bounded specialist can safely complete it. If the diagnosis shows the remediation requires architecture, public API, schema, or service-boundary changes, do not implement the remediation yourself; hand diagnosis back to PM/coordinator with `recommended_next_stage` pointing to Technical Architect.
- `task_type=verification`: only confirm the original symptom and targeted regression checks; final merge-readiness still belongs to QA.

## Output

Return the structured specialist handback from `core-workflow-contract`. Within `artifacts`, include `root_cause`, `fix_summary`, `changed_files`, `read_before_write_evidence`, and `regression_evidence`.
