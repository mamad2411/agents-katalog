---
name: econ-work
description: "Carry out economics research from an agreed plan or clear execution request."
---

# Economist Execution Workflow

Execute the work without losing the research object, realised sample, audit trail, benchmark boundary, or reader-facing deliverable. This file is the contract; read `references/execution_reference.md` at the stage that needs a template or checklist (each pointer below says when), and `references/delegation_reference.md` when delegating.

## Intake

Treat the arguments passed with this invocation, or the user's current request, as the work object. Use the conversation and any named plan or issue to recover the task before asking what to execute. Classify before touching anything:

- **Trivial one-off** — a narrow check, inspection, or mechanical edit with low empirical stakes. Proceed compactly: no task list, no review bundle, a compact closeout. This is the expected path for small work; do not force the full workflow onto it.
- **Saved plan** — read it as the decision artifact (not a progress log) and execute its stages; record divergence in the task tracker or closeout rather than rewriting the plan body.
- **Bare empirical request** — clear task, no plan. Scan the work surface, then write a short execution outline before any non-trivial edit or rerun.
- **Issue-linked work** — read the issue as coordination context only (objective, done-when, linked branches). Record whether issue updates are requested, approved, or out of scope.
- **Unclear work object** — inspect the available surface, then ask only for the unresolved choice that prevents useful authorised work. Continue independent parts of the task.

Route pure software work to the current Compound Engineering work skill (`compound-engineering:ce-work` when available). If the user asked for advice rather than execution, label the response advice-only. Do not start code changes, reruns, output promotion, or note drafting until the task, research object, scope, and rerun authority are sufficiently understood.

## Core invariants

Keep these distinctions explicit for the whole run; collapsing any of them is how research trust is lost:

- project backbone vs dated execution plan; plan labels vs incidental task names;
- the live research object vs any benchmark or comparison object;
- rerun outputs vs pre-existing outputs being inspected;
- audit outputs vs report inputs; the execution note vs the reader-facing note;
- observed facts vs diagnostic explanations vs limitations;
- research-code role and the maturity expected now.

Default order of work: (1) code and run checks; (2) output inspection; (3) economic interpretation and headline triage; (4) note brief when reporting is in scope; (5) only then the note and figures.

When code changes the main output family, update its specification, manifest, and checks in the same unit. When it changes sample, missingness, grouping, denominator, weighting, or timing rules, refresh the corresponding audit before closing. Keep one writer per mutable output family (derived datasets, tables, figures, logs, ledgers, note drafts, bundles, manifests, specs). Delegation follows the "Delegation" section below.

## Run boundary and provenance

Before major edits or reruns, establish what can actually be executed. A directory such as `raw/` is never proof that the required inputs are present. Check the actual files and access conditions; the authorised scope; which outputs or model objects are stale, inherited, or expected to be regenerated now; whether the active specification or computational object matches the intended run; and the stable entrypoint that regenerates the surface.

When required raw, restricted, model, simulation, calibration, or numerical inputs are unavailable or intentionally outside scope, code, manifests, checks, specifications, static validation, and interpretation of defended existing outputs may still proceed. State plainly that the main outputs were not regenerated, name the missing input or scope reason, and never present inherited outputs as fresh. When inputs and authority are present, run the appropriate empirical or computational path and report exactly what was regenerated.

## Delegation

Use `references/delegation_reference.md` for worker selection, model and effort,
context, and resource budgets. Keep the broad research question, definitions,
priorities, evidence assessment, and final conclusions with the coordinator.
Workers can investigate and challenge the reasoning but do not settle choices
reserved for the researcher. Delegate only separable work, with one writer per
output family and disjoint output roots. Treat returns as evidence to check,
not settled results. Do not launch agents just to fill available slots.

## Choice classes and questions

Use the request, prior decisions, plan, and relevant project files before asking. Proceed with authorised, reversible work when the task is clear. Ask only for a genuinely unresolved choice whose answer changes the economics, scope, access, cost, or destructive authority; do not ask again for decisions already supplied. Use `request_user_input` when available, otherwise ordinary chat. Explain what the choice changes, the credible alternatives, and your recommendation. A blocked branch need not stop independent work.

- **Class A** — estimand, identification, sample boundary, baseline, main output, benchmark treatment, or note scope when reporting is live. Follow a Class A choice already settled by the user or approved plan. Ask before resolving a new or conflicting Class A choice, an unauthorised destructive overwrite, or an out-of-scope empirical branch. In an autonomous parent run, return an unresolved Class A choice to the parent; do not mark it provisional and continue silently.
- **Class B** — a specification or inference choice within the allowed hierarchy. Choose from the plan or repo conventions, log it, and note credible alternatives worth stress-testing.
- **Class C** — a low-stakes implementation detail. Choose directly; log only when the audit trail benefits.

Record new Class A/B decisions and their authority in the existing choice register or an equivalent clearly labelled execution-note section. Reuse settled decisions by reference rather than creating a duplicate register.

## Workflow

For non-trivial work, keep a task list (the platform's task tool, or the existing execution record when that tool is unavailable) derived from the actual work surface — plan stages, required inputs, output families, verification needs, and any interpretation, note, bundle, or issue obligations — not a fixed universal checklist.

### Stage 0 — Ingest the work surface

Read the plan when present (as a decision artifact, not a progress log), the current workflow note, and only the authority-file sections the work needs; do not expand a project backbone or README into a research plan. Identify:

- objective; project backbone and GitHub issue when named; stable plan labels;
- research question and estimand or descriptive object; baseline; current choice register;
- the live object vs any benchmark block; outputs in scope; code role when code is in scope;
- whether reporting is in scope, and if so the reader, finished note format, and whether figures are required;
- which inputs a real rerun requires, and whether a review bundle already exists.

*Close when:* the objective, baseline, research object, feasible run boundary, and review route are named, and a task list exists for non-trivial work.

### Stage 1 — Code execution and run checks

Implement the smallest authorised change per code unit, using stable entrypoints, and record what actually ran and which outputs are newly generated vs pre-existing. Run the unit's verification before moving on. When writing or editing research code, the taste rules and worked examples live in `references/research-code-quality.md`; when the language is R, also consult `references/r-defaults.md` for package and tool defaults. Mandatory inside Stage 1:

- the research-code-quality floor: descriptive names that put the economic object before the plumbing, visible entrypoints, named object-defining parameters, no stale debug or test fragments, analytical logic separated from formatting when practical;
- input checking matched to provenance (the Provenance Ladder in `references/research-code-quality.md`): validate external/untrusted inputs properly; give self-authored workbooks and configs one thin boundary check, never repeated defensive parsing; check generated intermediates on the economic object, not every column; no defensive scaffolding, option flags, or fallback routes in internal helpers for callers that do not exist;
- object-defining assertions for row counts, keys, merge cardinality, denominators, weights, dimensions, convergence, residuals, or identities;
- helper-behaviour checks when a helper defines probabilities, bins, sample keys, denominators, matching, or timing;
- output-specification-first checks when the main output family changes, and a model-spec-ledger refresh when the realised model surface changed;
- for computational work, checks matched to the object (dimensions, convergence, residuals, feasibility, conservation, market clearing, deterministic simulation, small transparent benchmarks).

*Close when:* code changed or was skipped with a reason, what ran is recorded, and changed output families have current specifications and checks.

### Stage 2 — Output inspection and empirical audit

Read the realised outputs, not just the scripts that made them: sample accounting, merge and key diagnostics, missingness and support, weighting, grouping, and denominator, canonical tables and figures, and benchmark diagnostics when benchmark-facing. Make the realised sample legible before interpreting. For a diagnostic that may enter the note, organise the audit as total impact → composition of affected cases → selection consequence. Then simplify the surface without deleting evidence: tag every output with the two orthogonal tags in `references/execution_reference.md` ("Output provenance status vocabulary") — provenance status (`refreshed`/`inherited`/`inspected-only`/`scaffolded`/`stale`) and role tag (`support-only`/`report-input`).

*Close when:* outputs were inspected, the audit surfaces exist or were refreshed, report inputs are separated from support-only diagnostics, and stale or inherited outputs are named rather than silently trusted.

### Stage 3 — Economic interpretation and headline triage

Stop and answer: the main finding; what actually matters in the data; what to visualise; what follow-up is immediately implied. Record an interpretation brief (template in the reference), distinguishing observed fact, diagnostic explanation, limitation, and open question. For a bounded task this can be a short section in the existing execution note or closeout; use a separate `interpretation_brief.md` for a substantial report or handoff. When reporting is in scope, record the reader and argument as a delta on that interpretation, from defended report inputs rather than raw diagnostics. Combine the two briefs for a short note; keep separate files when the report or handoff needs them. When revising, first identify what the existing note gets wrong or needs to change.

If the run turns up a genuinely surprising finding, write a surprise memo (HTML via `econ-html-memo` when installed, plain standalone HTML under the same content discipline otherwise). Keep it as a normal local user-facing output: state the minimal validation already completed, plausible explanations, decisive missing evidence, and the research decision or next local check needed to continue.

*Close when:* the interpretation brief exists, the note brief exists when reporting is in scope, and the main finding, figure priority, and main-text-vs-appendix split are explicit.

### Stage 4 — Note writing and figures

Only after Stage 3. Draft from the note brief, interpretation brief, output-consistency map, tagged sources, and the existing note when revising — revising from the brief, not line-editing machine sentences. Keep the output-consistency map current (minimum structure in the reference) whenever note, memo, table, or figure claims are in scope. Honour an explicitly requested format. Otherwise standalone researcher-facing notes and memos default to HTML through `econ-html-memo` when installed; use plain HTML under the same discipline otherwise. Produce TeX and PDF only when the user explicitly requests those formats or explicitly asks for integration into a paper. Unless explicitly requested as the final format, Markdown is an agent-facing drafting scaffold. Insert existing figures rather than leaving placeholders. Before closing, run the text-figure consistency test and the local **Reader-facing note gate** in `references/execution_reference.md`.

*Close when:* the note is economist-facing, figure order follows the briefs, the consistency map is current, report paths are portable, and the explicitly agreed output format exists or the blocker is named.

### Verify and close

Use the verification ladder in `references/execution_reference.md` to cover the economic failure modes affected by this work. Reuse checks already completed on the same inputs and code; repeat them only after a relevant change or new concern. A formatting-only edit does not require re-estimation. Changes to timing, units, sample, weights, inference, calibration, or numerical solution do require the corresponding checks and affected-output inspection. Add software tests only for a real workflow, interface, or failure mode. Build or refresh the review bundle (minimum structure in the reference) only when the closeout routes to `econ-review` on a bundle or mixed surface, or the work goes to a coauthor or external reviewer — otherwise skip it. Ordinary verification stays within this workflow. Do not automatically invoke `econ-review` after execution, debugging, or output inspection. Set `review_route` to `none` unless the user explicitly selected the formal review workflow or an already-authorised end-to-end caller includes it. Such a caller owns invocation; a route recommendation does not itself launch review. Preserve the broader research assignment when formal review is only one component.

Account for the applicable closeout items in `references/execution_reference.md`, combining them rather than reproducing a fixed form; the run is complete only when the research outcome, evidence status, and unresolved risks are clear — a script run, a generated file, or one passing check is not completion. Route any durable lesson to the lightest surface (issue comment when issue-linked and approved; a drafted project-backbone update applied only on approval; a dated follow-up plan; or closeout-only). Old memos, exploratory reports, and externally supplied packages are leads, not authority, until traced to the underlying source, output, script, or review finding.

## Internal return to `econ-lfg`

An `econ-lfg` parent may supply the private caller contract `caller_contract: econ-lfg/v1`. This is orchestration metadata, not a user-facing option. Return the inline `econ-work-for-caller/v1` envelope defined in `references/execution_reference.md`. Do not deliver the final user closeout or perform Git actions; the parent owns the next stage and final handoff.

## Hard stops

Each is a named failure this workflow exists to prevent; the stage close-conditions above enforce them.

- Do not write the note or memo before the realised outputs are inspected and the interpretation brief exists (and the note brief when reporting is live).
- Do not let old or inherited outputs be presented as freshly regenerated.
- Do not stage, commit, or push unless the user explicitly requests that Git action.
- Do not treat GitHub issue text as analytical evidence without checking the actual plan, outputs, code, or bundle.
- Do not silently change the baseline, sample, estimand, benchmark treatment, or note scope beyond the user’s or approved plan’s authority — unresolved Class A choices require a question.
- Do not write a durable learning or project-state update (including `PROJECT_BRIEF.md`, `AGENTS.md`, or `README.md`) without its evidence paths and scope, or without approval for a substantive backbone change.
- Do not delete, overwrite, or hide stale empirical evidence without explicit approval.
