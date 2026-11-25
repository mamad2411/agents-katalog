---
name: eda-artifact-hygiene-maintainer
description: Clean and normalize knowledge-base, tool-registry, and log artifacts by merging duplicates, removing stale items, and correcting inaccurate naming while preserving traceability.
---

# EDA Artifact Hygiene Maintainer

## When to use

Use this skill when the user asks to:
1. clean the knowledge base, tool registry, or log directories,
2. merge duplicated notes or logs,
3. remove stale or superseded artifacts,
4. correct inaccurate or misleading file names,
5. reduce artifact sprawl without changing domain conclusions.

## Scope Boundary

This skill owns:
- artifact hygiene for `docs/knowledge_base/`,
- artifact hygiene for `docs/tool_registry/`,
- artifact hygiene for repo-maintained logs and meta logs,
- traceable merge, rename, archive, and delete decisions.

It does not own:
- domain experiment conclusions,
- theory promotion decisions,
- new domain-method implementation,
- repo-wide governance policy.

This skill is the direct workflow owner for cleanup and normalization tasks.
`workflow-scoped-execution` is not the default wrapper here; use it only when cleanup is embedded inside a larger execution workflow that explicitly delegates one bounded stage.

## Expected Downstream Consumers

Typical consumers include:
- `workflow-router` when the request is primarily cleanup or naming normalization,
- `eda-infra-maintainer` when cleanup exposes a governance or structural policy problem,
- execution and utility skills that need a dedicated cleanup pass after repeated artifact sprawl.

## Knowledge And Tool Interaction

1. Use `eda-context-accessor` when cleanup needs scoped KB or tool-registry context before deciding whether an artifact is duplicated, stale, or misnamed.
2. Treat `AGENTS.md`, the skill manifest, and relevant KB/tool index files as governing context for hygiene decisions.
3. Write every cleanup action into a traceable cleanup report so later maintenance work can understand what was merged, removed, renamed, or left untouched.

## Inputs

Provide or derive:
1. target scope (`knowledge_base`, `tool_registry`, `logs`, or mixed),
2. target directories or artifact set,
3. cleanup objective (`merge`, `delete`, `rename`, `normalize`, or mixed),
4. required traceability level,
5. whether the cleanup is a direct workflow or a delegated maintenance subtask.

## Outputs

Return or update:
- cleanup report (`artifact_hygiene_report.md`),
- optional rename map (`artifact_rename_map.tsv`),
- optional duplicate-merge note,
- explicit keep/delete/archive rationale for touched artifacts,
- explicit statement of whether `workflow-scoped-execution` was `not_used` or the cleanup was a delegated stage inside another workflow.

## Hard Rules

1. Do not delete or merge artifacts without recording the rationale.
2. Prefer rename or archive over silent deletion when traceability matters.
3. Do not rewrite domain conclusions while performing hygiene-only work.
4. If cleanup exposes a governance problem rather than simple artifact hygiene, hand off to `eda-infra-maintainer`.
5. Do not route routine cleanup through `workflow-scoped-execution` unless the parent workflow explicitly requires a governed execution substage.

## Operational References

1. Load `references/cleanup-scope-policy.md` when deciding whether the task is KB, tool-registry, log, or mixed-scope hygiene.
2. Load `references/workflow-owner-usage.md` when deciding whether cleanup is the direct workflow owner task or a delegated substage inside another workflow.
3. Load `references/folder-first-pass-playbook.md` when the user asks for folder-by-folder cleanup, a first exploratory pass, or a reusable directory cleanup SOP.
4. Load `references/duplicate-merge-rules.md` when deciding whether repeated artifacts should be merged or kept separate.
5. Load `references/stale-delete-and-archive.md` when deciding whether an artifact should be deleted, archived, or left in place.
6. Load `references/naming-normalization.md` when correcting inaccurate, ambiguous, or inconsistent file names.
7. Load `references/reporting-contract.md` when writing the cleanup report and traceability artifacts.
