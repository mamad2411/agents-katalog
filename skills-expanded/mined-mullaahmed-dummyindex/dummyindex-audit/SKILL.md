---
name: dummyindex-audit
description: Run a task-specific adversarial code audit, synthesize evidence-backed findings, and transfer confirmed new reusable lessons into existing canonical conventions before reporting.
---

# Dummyindex audit

You conduct the audit; the `dummyindex context audit` CLI only scaffolds and tracks its workspace. Read the real source. Conventions and feature docs guide review, but source is authoritative when they disagree. Audits leave source unchanged; closeout may update a canonical convention with a verified lesson.

## 1. Start and scope

The user must describe what to audit. If missing, ask one concise question. Pass any requested paths as `--scope`; otherwise choose a narrow scope when the request implies one. Pick a host-valid model: Claude reuses configured selection or asks among `opus|sonnet|haiku|fable`; never silently choose one. On Codex, always pass `--model current`; other portable hosts should use their current-model selector. Do not offer Claude labels on the portable host path.

Start with `dummyindex context audit start --describe "..." [--scope PATH]... [--mode light|standard|deep] [--model ...] --json`. Read the returned slug, scope, mode, model, and persona catalog. Before dispatch, capture hashes of in-scope source/test files; add any other files you audit before reading them. If considering a convention update, capture its original hash too. The CLI needs a model unless configuration supplies one. Do not invent CLI verbs or claim it runs auditors; host orchestration is yours.

## 2. Choose and run the panel

Select 2–5 catalog personas whose roles fit the task; give the user a one-line panel rationale. For independent round-zero work, dispatch them in parallel. On Claude use each persona's `subagent_type`, falling back to `general-purpose`; on the portable host path (Codex), use built-in `worker`, falling back to `default`. Read each selected `agents/<persona_id>.md` body and include its mandate in the prompt; do not send a path and assume a worker can read it. Ask auditors to read real source, relevant existing conventions and feature docs, and write findings to `.context/audits/<slug>/findings/<persona_id>.md`.

Every finding cites exact `path:Lstart-Lend`, severity (`critical|high|medium|low|info`), one-sentence claim, source evidence, and a suggested fix or `none`. Log each persona's start and completion with `dummyindex context audit-log --slug S --round N --persona P --status started|complete`.

In `light` mode skip debate and synthesize. In `standard` and `deep`, run the same panel for rebuttal rounds, up to the CLI's `max_rounds` (never more than 3). Include the other findings and require each auditor to concur, dispute, defend, or concede with cited evidence. Update statuses (`open|confirmed|disputed|refuted|withdrawn`). Stop immediately when a round changes no statuses; preserve unresolved disputes. In `deep` only, dispatch skeptics to refute each remaining confirmed finding before synthesis; downgrade a finding only when a majority of skeptics refute it.

## 3. Synthesize findings

Read all findings and rebuttals. Deduplicate claims about the same issue. Keep only supported outcomes: `confirmed`, `disputed` with both sides, or `refuted`/`withdrawn` briefly noted. Rank by severity, then put confirmed findings ahead of disputed ones. Source decides if it conflicts with a convention or feature document.

## 4. Finalize the report

Write `.context/audits/<slug>/report.md` with a 3–5 line executive summary, findings by severity and verdict, unresolved disagreements, and any lesson that was deferred or found already covered. Finish it before the closeout inventory; do not edit it afterward.

## 5. Close out one reusable lesson

For confirmed findings, consider at most one concise, new, reusable rule: a contract supported by audited source and independently verified behavior, not a suggested fix. A confirmed helper contract may be reusable while the caller bug is open; do not imply it is fixed. Skip covered lessons, update an ID, or supersede an obsolete managed rule; preserve owner text. Include only meaningful existing tests. No supported novel rule: omit `learning_reflection`. No applicable test: submit with no tests; the gate records `evaluated/blocked` without promotion.

`learning_reflection` is one lesson object: `cue`, `lesson`, `evidence`, `confidence` (`low|medium|high`), all required and nonempty; optional `edits` rows `{component, change, verdict}` with verdict `helped|hurt|no_observed_effect|confounded`. A list is rejected. Delivery fields (`verified`, `target`, `rule_id`, start-captured `expected_sha256`, repo-relative `sources`, `tests`, optional `supersedes`) follow `closeout.md`. `body` is ignored for a lesson-shaped reflection (rule text becomes `When {cue}: {lesson}`); cite `sources`/`evidence`, not `body`. Never cite the temporary audit workspace. Read sibling `closeout.md` and give every workspace file a specific reason. Recheck every captured source/test and convention hash before closeout; on mismatch, stop and report it.

Finalize the report first; the `closeout.md` recipe writes it outside the workspace with `transfers: []`. Run:

`dummyindex context gc closeout --kind audit --slug <slug> --manifest <manifest.json> --json`

Learning status is `applied|evaluated|blocked|no_entry|pending|ignored|failed`. Only `failed` exits non-zero; `blocked` prints with exit 0. Do not override or claim adoption. If closeout rejects the manifest, stop: do not refresh hashes or rerun the recipe automatically. Re-review the changed inventory or evidence; prepare a new manifest only after rechecking the report and every disposition. Once a receipt is accepted, never mutate the report. Report the returned `learning` state accurately. An applied rule qualifies only its checked project behavior; it does not establish model improvement.

Tell the user the panel, rounds to convergence (or cap), confirmed findings by severity, unresolved disputes, learning state, and report path.
## CLI reference

- `dummyindex context audit start --describe TEXT [--scope PATH]... [--mode light|standard|deep] [--model current|opus|sonnet|haiku|fable] [--slug S] [--force] [--root DIR] [--json]` creates the audit head, brief, catalog, and findings directory.
- `dummyindex context audit show --slug S [--root DIR] [--json]` shows current state and report path.
- `dummyindex context audit-log --slug S --round N --persona P --status started|complete|failed|skipped [--note TEXT] [--root DIR]` appends debate progress.

To implement findings, use the separate plan/build workflow, not an audit.
