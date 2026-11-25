---
name: research-project-rules
description: Initialize or maintain project conventions for scientific research data-analysis projects, including analysis scripts, study inputs, and research outputs. Use when setting up or changing such a project’s layout, data workflow, dependencies, or execution conventions; not for general software development, routine file operations, statistical method selection, or manuscript review.
---

# Research Project Rules

Apply only to scientific research data-analysis projects: work that processes study data to produce research analyses and outputs. An R/Python file or a directory named data/results alone is not sufficient to trigger this skill. Maintain such a project so it is easy to run, iterate on, and hand over. Follow the user's task and the project's existing contract. These are project execution conventions, not a scientific-review workflow or a requirement to audit the whole project.

## Select and guide the task

Determine the requested outcome from the conversation and existing project context. Reuse settled choices; ask only about consequential gaps such as research scope, data access, target location, or a required environment. Use reasonable reversible defaults for routine choices. Do not turn setup into a fixed questionnaire or choose scientific methods just to complete project scaffolding.

- **Initialize or establish missing project conventions:** follow [initialize.md](initialize.md) to create or complete the project layout, README/agent entry, applicable data rules, and necessary dependency setup.
- **Establish or change data handling:** read [data-rules.md](references/data-rules.md), adapt its baseline to the actual data and project instructions, and put essential applicable boundaries directly in the project's agent entry. Raise concrete overrestriction or disclosure risks without silently relaxing explicit limits.
- **Maintain an existing analysis:** apply the principles below and read only the reference needed for the change. R execution and script-adaptation conventions use [r-workflow.md](references/r-workflow.md); ambiguous spreadsheet columns use [tabular-input-contract.md](references/tabular-input-contract.md); clinical table output uses the relevant presentation and export guidance in [clinical-table-reporting.md](references/clinical-table-reporting.md). Statistical decisions follow the project analysis plan or separately requested scientific guidance.

Combine guidance only when the task needs it. A new conversation, an optional missing file, or an unrelated edit does not trigger initialization, a data audit, or all references. Finish with the requested concrete change and proportionate verification, then stop.

## Project layout and orientation

- Inspect the nearby implementation and project guidance only as needed to understand the change. Preserve established paths, output schemas, and names unless the task changes them.
- For a new project without a layout, use `scripts/` for analysis entry scripts, `data/` for inputs and derived data, and `results/` for generated outputs. Create these base directories during requested initialization; add other directories only when they serve actual work.
- Introduce `src/` or the existing shared-code equivalent only when functions are genuinely reused. Keep one-off logic in its entry script; do not prescribe additional subdirectories.
- Keep root `README.md` as the main human entry. Keep `AGENTS.md` or its equivalent as a brief research overview (question, methods and technologies actually used), critical execution constraints, and a reading index. Supporting notes belong in `docs/` or the established equivalent; preserve required root configuration and licenses.
- Maintain detailed knowledge in one place. For substantive documentation work, use `research-log-maintainer` if available. Routine edits do not require new logs, reports, or documentation files. Project files provide durable context; memory is only a navigation aid.

## Analysis entry scripts

- Each analysis entry must run independently in a fresh session once its declared environment and inputs are available. Initialize its paths, explicitly load required packages and shared code, and read its declared inputs; do not rely on restored workspace objects, previously attached packages, or another entry having run in the same session.
- Upstream results are allowed as explicit file inputs. If a required input is missing or invalid, identify it and the relevant preparation step; do not source an earlier analysis to obtain its in-memory objects or silently rerun the entire pipeline.
- Declare shared-code dependencies through the project's existing helper, package, or module mechanism. Loading helpers should not silently launch analyses. An orchestrator can remain available without becoming necessary for every local iteration.
- Prefer project-relative paths and existing helpers. Avoid machine-specific absolute paths in reusable code. Create output directories as needed and retain a clear home for each output.

## Reuse and scope of execution

- Reuse existing outputs when they remain valid for the relevant inputs, code, and configuration. Use the project's available provenance or checks; do not introduce a new cache or hashing framework just to make a small change.
- Recompute the affected analysis and dependent outputs when necessary. Documentation, navigation, and organization changes do not by themselves require statistical reruns. Use a full pipeline when the change or explicit request warrants it.
- Protect human edits and distinguish older valid outputs from incomplete new runs. If a run fails, state which outputs remain usable or uncertain rather than presenting mixed outputs as one completed run.

## Proportionate validation and delivery

Choose the smallest checks that give confidence in the changed behavior. There is no mandatory full checklist, fixed number of checks, or requirement to run an analysis twice.

- Select checks by impact: syntax for code edits, startup checks for path/dependency changes, sample and key-field consistency for joins or filters, and rendered inspection for meaningful presentation changes. These are examples, not requirements to apply to every task.
- Run affected computations when needed to substantiate changed results. A parse check alone does not verify an analysis result; where execution is unnecessary or unavailable, say what was and was not checked. When claiming a deliverable was generated, confirm that the expected file exists and is usable; this does not require checking every unaffected output.
- Once relevant checks pass, stop unless a failure or unresolved concern justifies more work. Do not rerun unchanged analyses or add tests that merely mirror implementation details.
- Report edited, executed, and verified scope accurately. Update durable documentation only when a meaningful contract, result status, or working entry changes.
