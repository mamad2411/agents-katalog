---
name: superdiagnose
description: Use when a coding-loop evaluation report is FINAL and FAIL and the failed or missing checks need an evidence-grounded repair or author-input disposition.
argument-hint: "<project-dir> --round <N> --eval-report <path> [--operation <path>]"
license: MIT
related skills: superauthor, supereval, supermeta, supercode
---

# Superdiagnose

Diagnose one selected failed coding-loop round and write one FINAL report. You are the single
**DIAGNOSER worker** already dispatched by the supervisor. Do not dispatch another worker or invoke
superdiagnose recursively. Do not implement a repair, edit product code, or change `prd.md`,
`evaluation.md`, `knowledge-base.md`, binding sources, plans, or findings.

**Input:** `superdiagnose PROJECT --round N --eval-report PATH [--operation PATH]`.
`PROJECT`, the positive round `N`, and the exact selected FINAL FAIL evaluation report are required.
`--operation` selects the supervisor's durable DIAGNOSING operation; without it, create one manual
operation id with `uuid.uuid4().hex` and derive the output name normally.

## Resolve identity and evidence

Resolve the primary checkout and vault exactly as the other coding-loop skills do: the primary root
is the parent of `git rev-parse --path-format=absolute --git-common-dir`; `SUPER_GOAL_ROOT` is
resolved from the process environment, primary `.superenv`, then `templates/superenv.default`.
An absolute or `~` vault is external, physically resolved, and must be its own Git repository.
Synchronize code `main` and, when external, vault `main` before treating either as evidence.

Require READY `prd.md`, `evaluation.md`, and `knowledge-base.md`. Resolve the complete approved
agreement and every binding source before causal analysis, preserving each source revision. Compute
the agreement fingerprint with `scripts/_coding_loop_evidence.py`; never substitute the current
checkout, an old evaluator answer, a test name, or an unverified excerpt for a resolved source.

Validate the selected report with `validate_evaluation(...)` using round, evaluated code commit,
agreement revision, operation identity when present, and source-vault commit. It must be FINAL,
FAIL, and exactly `--eval-report`. Keep its complete failing and missing C/J set. A legacy project
with no J rows retains its explicit command-only acceptance semantics; a project that declares J
rows never gains that exemption because a result is missing.

Inspect the selected code commit in a detached worktree. Read the round's ledger row, meta-plan,
goal master/leaf plans, closeout reports, findings, inner-loop receipt, command outputs, judged
evidence, and applicable approved AC rows. Old rounds may explain history but are not evidence for
the selected round.

If any required source, selected revision, evaluation result, round artifact, tool, dispatch
receipt, or context is unavailable or untrustworthy, record an `execution/evidence failure` and
choose `AUTHOR INPUT`. If the resolved approved requirements or evaluation contradict one another,
record a `PRD/evaluation defect` and choose `AUTHOR INPUT`. Do not fill missing evidence with a
likely product cause and do not return REPAIR.

## Operation targeting and recovery

When `--operation PATH` is supplied, load that exact operation and require phase `DIAGNOSING`, round
`N`, the selected code/agreement/source identities, and a nonempty intended diagnosis-report path.
The operation's `report` fixes the output path and timestamp; retries never choose a new path.

Before writing, call `reconcile_operation(repo, vault, operation)`. For `INTEGRATED`, read the exact
recorded report and run `validate_diagnosis` against the selected evaluation identity and its failed
and missing IDs. If it is valid, return that existing report, integration commit, and disposition
without writing or committing again. A mismatched, invalid, multiple, dirty, or unmerged result is
a conflict for the supervisor; do not overwrite, discard, stash, or silently adopt it. `ABSENT`
allows the one intended report to be written.

Without `--operation`, take one UTC `<STAMP>` and target
`<project-dir>/diagnoses/<STAMP>-r<N>.md`. Refuse an existing target rather than overwrite it.

## Classification and disposition

Classify each independently evidenced problem using exactly one class:

| Classification | Use when | Disposition effect |
|---|---|---|
| `implementation defect` | Selected product code or an already-required delivered assertion violates the clear approved agreement. A green suite or existence-only assertion does not prove required behavior or assertion meaning. | May be `REPAIR`. |
| `plan gap` | The approved obligation is clear, but the selected round's plan omitted or misstated it. | May be `REPAIR`. |
| `PRD/evaluation defect` | Approved requirements or evaluation are contradictory, ambiguous, invalid, or would require adopting a new requirement. | Forces `AUTHOR INPUT`. |
| `execution/evidence failure` | Tools, context, dispatch, source revisions, results, or receipts are unavailable or untrustworthy. | Forces `AUTHOR INPUT`. |

Use `high`, `medium`, or `low` confidence. High and medium are reliable only when the cited evidence
supports the exact class and cause. Low confidence is unresolved and forces `AUTHOR INPUT`.
Mixed problems force `AUTHOR INPUT` if any row has an author-only class or low confidence.

Every failed or missing C/J ID from the selected evaluation validation must appear in the Problems
table. Cite applicable approved AC IDs. The Evidence cell cites observed file and line locations
when available; an execution/evidence failure states what evidence is unavailable. Keep product
behavior, command execution, and assertion coverage separate: evidence of one does not establish
the others.

Repair guidance is bounded by each problem and may carry only obligations already present in the
approved agreement. Mark extra improvements as nonbinding suggestions; they do not create failures
or repair scope. Never propose automatically editing specifications or weakening checks.

## Report and validate

Copy `templates/coding-loop-diagnosis.md` exactly, replacing every angle-bracket instruction. The
required labels are Date, Status `FINAL`, Round, Operation, Eval report, Evaluated commit, Agreement
revision, and Source vault commit. Keep exactly these sections in order: `Inputs and limitations`,
`Problems`, `Repair guidance`, `Disposition`. The Problems table columns and accepted values are
fixed by the template. Use `none` only for an empty C/J or AC cell.

Before committing, run:

```python
validate_diagnosis(
    diagnosis_path,
    {
        "round": N,
        "operation_id": operation_id,
        "eval_report": selected_eval_report,
        "evaluated_commit": selected_code_commit,
        "agreement_revision": agreement_fingerprint,
        "source_vault_commit": source_vault_commit,
        "failing_ids": evaluation_result["failing_ids"],
        "missing_ids": evaluation_result["missing_ids"],
    },
)
```

Proceed only when its computed disposition equals the report declaration. A REPAIR report also
requires `may_start_next_round: true`. Otherwise preserve the report as an explicit AUTHOR INPUT
outcome or report the conflict; never describe it as repairable.

## Commit and return

Invoke `superagent:superauthor` and apply A3, A5, A6, A7, and A8 to this structural report. A1's
no-product-execution boundary applies; A2's plan format does not. Use:

- branch prefix `project/<project-slug>-r<N>-diagnosis`
- commit subject `docs(project): <project-slug> round <N> diagnosis`
- PR title `docs(project): <project-slug> r<N> diagnosis`
- PR body `Diagnosis for round <N> from <eval-report>; disposition <REPAIR|AUTHOR INPUT>.`
- explicit `git add` of the one diagnosis report only; never bulk-stage

For an internal vault, commit the report through A7's PR workflow and merge it before returning.
For an external vault, commit it directly to that vault's synchronized repository under A7; do not
open a PR in the code repository. Verify the report is integrated before reporting success.

Return exactly:

```text
## Superdiagnose complete

**Project:** <project-dir>   **Round:** <N>
**Eval report:** <exact selected report>
**Report:** <diagnosis path>
**Disposition:** REPAIR | AUTHOR INPUT
**Integration commit:** <short-sha> in <target repository>
**PR:** <url> (merged) | none (external vault)
**Next:** REPAIR → next round may be planned | AUTHOR INPUT → wait for an author decision
```

After returning the report path, integration commit, and disposition, take no further action.
