---
name: econ-plan
description: "Plan empirical or computational economics research from a question, brief, or issue."
---

# Economist Planning Workflow

This skill owns planning, not execution. Stop after the saved plan unless the caller is `econ-lfg` or the current request explicitly asks for end-to-end execution. In those two cases return the saved plan to the caller and let `econ-work` continue in the same turn; no second instruction is needed. A direct invocation that merely mentions later execution still ends at the plan. This file is the contract; read `references/plan_template.md` only when writing or refreshing the saved plan, and `references/project_brief_template.md` only when the user approves a project-backbone document.

Before delegating a planning investigation or specifying worker models, reasoning effort, or delegation budgets in a plan, read `../econ-work/references/delegation_reference.md` relative to this skill directory. Apply that shared policy to the particular assignment; its examples are starting choices, not fixed tiers. Reading it does not invoke `econ-work` or authorise execution.

## Direct invocation contract

Every direct invocation ends in exactly one of two states:
- **an alignment conversation in progress**, asking one decision per blocking question until the material task context is shared; or
- **a saved plan file plus a short receipt.**

An inline-only plan is not a valid completion. Write the saved markdown plan unless file creation is genuinely blocked (missing write access, no workspace location, or a failed file operation), in which case state the blocker and the exact no-save reason. The saved file is the artifact; the chat receipt is only the summary and handoff. For pure software tasks, use the domain-routing boundary below rather than forcing an economics plan.

## Receipt

Lead with the research bottleneck and the proposed way to resolve it. Link the saved plan and state the deliverable, the consequential assumptions, and the next step. Explain what the plan lets the researcher learn or decide, not the internal workflow vocabulary. Write the receipt in prose; use a short list only for genuinely parallel items such as the assumptions, the paths, and the next step. Do not repeat the plan in chat.

Keep classifications, stage bookkeeping, and detailed evidence paths in the saved plan. Surface them only when they explain a material limitation or choice. For an autonomous caller, return the plan path and any genuine blocker without a separate user handoff or permission request.

## Questions and scope

First use the current request, prior decisions in the conversation, and the named project material. Ask only when a remaining ambiguity would materially change the research question, estimand, identification, sample boundary, baseline, benchmark treatment, main claim, costly rerun, or authorised scope. Do not re-ask a settled choice or ask the researcher to supply information you can read. Use `request_user_input` when available; otherwise ask in ordinary chat. Explain the economic consequence and your recommended default, one decision per question.

Choose reversible implementation and presentation details within the agreed task, stating consequential assumptions rather than seeking blanket confirmation. Infer the reader and requested format from the task where clear. A missing optional project brief, figure preference, or administrative field is not a reason to stop.

After gathering evidence, briefly state material assumptions and exclusions before saving. This is a scope disclosure, not an automatic approval gate. An unresolved researcher-level choice must be asked before the affected branch is finalised; meanwhile, save the known plan with that branch explicitly blocked and continue independent planning. Never present a blocked branch as ready for execution.

## What a ready plan locks

- a plain-language restatement and the decision problem, not just the topic;
- the final human reader and the desired output;
- the project backbone used, or that none was found;
- `domain_mode`, `task_family`, `code_role`, and `reporting: yes|no`;
- one central bottleneck;
- sparse stable labels for important decisions, outputs, and work units (`F1`, `F2`, … reserved for `econ-review` findings);
- the live research object separate from any benchmark or comparison block, and audit outputs separate from report inputs;
- a four-stage execution path handed to `econ-work`: code and run checks → output inspection → interpretation and headline triage → note and figures.

**Smallest correct round.** When the validated evidence already exists, plan the smallest correct next round; do not reopen adjacent branches unless the central bottleneck requires it.

When reporting is in scope, lock the reader-facing note contract before execution. Do not draft it from raw diagnostics:
- note type (free text), and the question the note must answer;
- the one-sentence headline it may make if the evidence holds;
- what the reader should know by the end;
- the definitions and sample distinctions that must appear before findings;
- the finished human-facing surface and render target (respect the requested format; otherwise use the HTML default below);
- the likely headline figure, and what belongs in the appendix rather than the main text.

Honour an explicitly requested output format. Otherwise, standalone researcher-facing notes and memos default to HTML. Produce `.tex` plus rendered `.pdf` only when the user explicitly requests those formats or explicitly asks for integration into a paper. Unless explicitly requested as the final format, Markdown is an agent-facing planning or drafting surface, not the default finished note.

## Domain routing

Classify `domain_mode` before writing the plan (this is its single home):
- `empirical` — economics research where sources, data, models, outputs, interpretation, reporting, benchmark comparison, or reproducibility matter;
- `hybrid` — research-object integrity and software-implementation integrity both matter (data pipelines, reproducibility, custom interfaces, model computation, simulation, calibration, estimation machinery, reusable research tooling);
- `software-handoff` — pure app, API, UI, infrastructure, tooling, refactor, or debugging with no research-object, output, interpretation, or reporting stakes. Mark it and route to the software-engineering workflow rather than `econ-work`.

## Proportionality

**Compact plan.** For a bounded task, save only the relevant template sections: the research objective, fixed definitions and scope, evidence, execution steps, and checks. Combine overlapping sections; do not create empty headings or lists of inapplicable fields. Keep the four-stage logic but mark unnecessary stages as skipped in one sentence. A saved plan remains required for the non-trivial `econ-lfg` handoff.

## Workflow

Saved plans use repo-relative paths for files, outputs, and evidence (`analysis/build_sample.do`, not `/path/to/repo/...`); use absolute paths only in the final chat link. When the user names a specific file, issue, plan, output, register, dataset, or document, inspect it before substituting a generic alternative; if it cannot be found, say so.

### Stage 0 — Locate the planning surface
- If an existing plan is referenced or obviously matches, read it; ask update-in-place vs new when ambiguous; revise only still-relevant sections (plans carry no execution progress log).
- When the planning surface is a scope memo with `readiness: scoping-only` (from `econ-brainstorm`), upgrade that same document in place to a full plan rather than creating a new file.
- Discover the project backbone in order: a brief named in `README.md`/docs index → `PROJECT_BRIEF.md` → `RESEARCH_BRIEF.md` → paper outline, coauthor memo, or methods note → a dated plan only when it is clearly acting as the backbone.
- Use `AGENTS.md`/`README.md` for orientation only, never as the research plan. If no backbone exists, record that fact and plan from the available evidence. Recommend a compact `PROJECT_BRIEF.md` when future sessions need it, without making its creation a prerequisite; substantive backbone changes still need approval. A new project's `DEFINITIONS.md` can be seeded from the backbone's definitions section or a graduated scope memo.
- If a GitHub issue is named (`#123`, `repo#123`, or a URL), read it as coordination context, summarise only the decision-relevant parts, add an `Issue coordination` section, and never create or update issues without approval.

### Stage 1 — Decision frame
Lock the objective; project backbone; issue coordination when issue-linked; reader contract; `reporting: yes|no` (and the note contract when yes); `task_family`; `code_role` when code is in scope; secondary lanes; and the central bottleneck.

Classify `task_family` by the primary research object, not the output format, keeping it orthogonal to `domain_mode` and reporting: an `analysis` or `data_construction` plan may still carry a note, and `writing` is only for when the note or memo is the primary object, built from already-defended or inspection-ready evidence — never drafted from raw diagnostics or uncatalogued sources.

### Stage 2 — Gather evidence, then call out scope
- Read the object-defining code, current outputs and checks, active workflow notes, and the prior plans, notes, or benchmark material that matter.
- Read the project's `DEFINITIONS.md` when present and treat its terms as canonical; the plan's definition registry cites its entries rather than restating them.
- For broad, repeated, risky, or unclear tasks, search repo-local research-learning notes (`docs/research-learnings/`, `.codex/research-learnings/`, legacy `docs/solutions/`), narrowed by task family: `source_collection` → source-provenance, interpretation-claims; `data_construction` → data-measurement, sample-linkage; `model_computation` → theory-models, specification-estimation; `analysis` → specification-estimation, interpretation-claims; `writing` → interpretation-claims, writing-figures.
- Treat any note as precedent, not authority; flag a conflict with live files and mark the note stale rather than following it silently.
- Build a compact evidence map (live and checked / live but unchecked / missing vs the requested target / ambiguous), and call out missing evidence before leaning on it.
- Then disclose material scope assumptions as described above.

### Stage 3 — Lock definitions and deliverables
Make explicit the research question and estimand (or descriptive object), a definition registry for terms that can drift, current authority files vs supporting or benchmark files, interpretation scope, audit outputs, and report inputs. When reporting is in scope, lock the note contract above. The task-family implementation-surface specifics (source/register fields, data-construction registries and audits, model-computation entrypoints and checks, analysis baseline and robustness grid, writing claim-budget) live in `references/plan_template.md` as guidance under the matching sections — read them at template-writing time.

### Stage 4 — Sequence the four econ-work stages and verification
Hand off the same four stages `econ-work` runs; the per-stage fields are in `references/plan_template.md`:
- **Stage 1 code and run checks** — likely entrypoints, expected objects, feasible run boundary, code role and the research-code-quality floor, stop conditions;
- **Stage 2 output inspection** — realised outputs to inspect before interpretation, sample/grouping/denominator/missingness/overlap audits, audit vs report outputs;
- **Stage 3 interpretation and headline triage** — where to stop and decide the main finding, and whether the interpretation and note briefs are required;
- **Stage 4 note writing and figures** — structure, definitions before findings, figure order, text-figure consistency, and portability, or an explicit skip naming any non-note handoff artifact when reporting is out of scope.

Specify verification: input, transformation, realised-sample, grouping, and denominator integrity; object comparability before any benchmark claim; which audit outputs and report inputs must exist; text-figure consistency when reporting; and which findings trigger a stop-and-ask. Keep missing evidence, surprises, and unresolved decisions in the saved plan and user-facing receipt; do not initiate another review workflow from the plan.

### Save
Write or refresh the saved plan with `references/plan_template.md`; it is ready only when it passes the template's minimum quality check. Preferred location: a repo convention if one exists, otherwise `docs/plans/YYYY-MM-DD-<slug>-econ-plan.md`. The ordinary next step is `econ-work` on the saved plan; name the outputs, checks, briefs, and bundles `econ-work` should leave ready for later `econ-review`. Use `econ-review surface:plan` only when the plan is unusually large, risky, ambiguous, or intended for multi-agent execution. If a material question remains, ask it and mark the affected branch blocked in the saved plan. Do not bury it in `Open questions` or imply that execution is authorised on that branch.

## Hard stops

- Do not execute after a direct planning invocation unless the current request explicitly asks for end-to-end execution. In an `econ-lfg` run, hand the saved plan to `econ-work` without a new permission gate.
- Do not leave the objective, reader, reporting scope, or desired output implicit when they materially affect the work.
- Do not use `AGENTS.md` or `README.md` as the home for long research-state content, or create or update GitHub issues without approval.
- Do not hide missing evidence or ambiguities.
- Do not let a benchmark silently redefine the live research object.
- Do not plan to draft the note from raw diagnostics, manifests, or execution logs, or treat the execution note as the reader-facing note.
