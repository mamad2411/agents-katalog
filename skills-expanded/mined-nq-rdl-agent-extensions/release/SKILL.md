---
license: CC-BY-4.0
description: >-
  Draft the researcher-facing Extraction Summary and Extraction Assumptions / Important
  limitations for a release from the release tag's own pipeline, outputs and validation,
  checked against the confirmed scope and .sqlreview reviews. A stale review or conflicting
  source holds its claim; the analyst accepts, rewords or rejects each claim, and the record
  keeps wording and provenance. It never publishes. Use when an analyst prepares a release body.
argument-hint: '<release tag or candidate ref>'
user-invocable: true
compatibility: >-
  .sqlreview schema 2 (schema 1 remains readable) (docs/specs/2026-09-15-sql-review-plugin-design.md);
  bash 3.2+, jq >= 1.6, git (reads the release tag). Scaffold paths (specs/amendments.md,
  .copier-answers.yml, runbook, UAT checklist) follow data-analysis-scaffold 0.5.0; verify the
  repository's own layout at use time.
allowed-tools: Bash, Read, Glob, Grep, Write, AskUserQuestion
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Data Request — release (Data Analyst)

This step is Analyst → Researcher communication. `/data-request:analyse` stays the engineer's
detailed review, and `/data-request:explain` walks the analyst through it. This skill drafts a
short release body from the release's own artifacts. It never changes a scope, review or SQL
file, and it never publishes a release, pushes a tag or posts the body.

Order: the Data Engineer completes `analyse`, the authorised operator run, UAT and the triage
hand-off; the Data Analyst runs `explain`, accepts for release preparation, sends back or
amends presentation, then drafts here and publishes. Never direct the engineer to release.
If the analyst chooses **Send back** here, use the paste-ready *Analyst outcome* note in
`${CLAUDE_PLUGIN_ROOT}/skills/explain/SKILL.md`: logic changes or defects to `fix`, presentation
changes to `amend` before or after release. Keep unresolved claims `pending` and the current
candidate record `draft`; do not overwrite a previously approved release record, post the
note or clear a gate. Refreshed review and operator-run/UAT evidence precede another hand-off.

For RDL cohort SQL, read `${CLAUDE_PLUGIN_ROOT}/skills/guardrails/SKILL.md` when a claim rests on
a storage fact or conversion. Worked example:
[references/worked-example.rst](references/worked-example.rst).

Arguments: `$ARGUMENTS` — the release tag or candidate ref (for example `v1.0.0`). If none is
given, ask for it.

```bash
S="${CLAUDE_PLUGIN_ROOT}/skills/setup/scripts"
bash "$S/sqlreview.sh" status --json   # exit 3 → stop: not initialised, run /data-request:setup first
```

## 1. Gather the release evidence

Read every source at the tag with `git show <tag>:<path>`, never the working tree or another
branch:

- the request, confirmed scope (`scope.json`), analyst intake, answers configuration
  (`answers.yaml` or `.copier-answers.yml`), open questions and `specs/amendments.md`;
- the pipeline or builder that produced the extract, and the SQL it generates;
- the output manifest or schema: each delivered file, its columns and its row grain;
- validation and UAT evidence: runbook, UAT checklist and validation outputs.

For counts in that evidence, apply guardrails `references/release.rst`, **Probe disclosure control**, before quoting them.

Then list the reviews and whether each describes the release:

```bash
bash "$S/release.sh" evidence "<tag>"   # exit 0 every review applies · 10 at least one does not · 2 unknown ref
```

For each slug, load `bash "$S/sqlreview.sh" questions "$SLUG" review`: `questions.json`
is the authoritative current handoff question status; `release.sh evidence` includes its
structured rows and open-only compatibility list. Closed legacy strings in scope/review
are not unresolved questions. Label these as current handoff evidence against the tag, not
question status at the historical tag. Reconcile obsolete intake copies with their owner;
do not silently update `answers.yaml` or convert engineer choices into analyst answers.

A claim that needs a missing manifest, schema or validation result is a question, not a fact.
Say which source is missing.

## 2. Check that each review applies

Do this before you use any review item. `evidence` reports `applies` for each review:

- `current`: the SQL at the tag is the reviewed SQL.
- `header-only`: only the leading comment header differs. The items apply.
- `changed`: the SQL at the tag differs. The review is stale for this release.
- `missing-at-ref`: the reviewed SQL is not in the release.
- `unreviewed`: a scope only, with no review.

It also reports `reviewed_commit_in_ref`: `false` means the review was made on a commit outside
the release. Then compare the review with the pipeline yourself. A review of draft SQL, or of SQL
the pipeline no longer generates, does not describe the release, even when a file matches.

A review that does not apply blocks every claim based on it. Re-derive the claim from the
release's own files and cite them, or raise it as a question. Never infer confirmation from an
old review. Offer `/data-request:analyse --update` to the engineer when the release SQL needs a
current review.

## 3. Compare the release with scope and review

Before you draft any wording, compare each source with the others and with any existing release
wording:

- **inclusion rule**: the codes, text matches and Boolean structure (and, or) that admit a record;
- **unit of observation**: the grain of each delivered file, against source-citing scope/intake
  and review `grain`, keeping the main grain separate from requested finer outputs. Apply
  guardrails `references/grain.rst`: a bare answers-file default is not a confirmed scope;
- **delivered outputs**: each file and field, against the requested elements. A requested element
  that is absent is a finding;
- **derivations**: period, site, age basis and other derived fields.

Bare-default drift alone is not a blocking discrepancy: reuse the existing `L-grain-answers`
finding once and offer correction to the engineer, without changing answers or SQL here.
An unknown grain or real conflict with an evidenced agreed grain still holds its claim.
Each meaning-changing difference is a blocking discrepancy. Record it as a question (`Q1`, `Q2`, ...) with the
conflicting evidence from each source and a proposed correction, and hold the draft until the
analyst resolves it. Never soften a discrepancy into boilerplate, and never leave it out. A prose
or typo pass comes after.

## 4. Select and translate

Go through each confirmed review item (`A1`, `L1`, ...), scope item, amendment and validation
finding. Keep an item for the researcher when it affects cohort membership, field meaning,
completeness, comparability or interpretation. Merge related items. Keep implementation detail
(locking hints, row order, query structure) in the internal review, unless its consequence
matters to the researcher. Then state the consequence, not the mechanism. Use plain language and
short sentences, without SQL terms.

Show the analyst the items you kept internal, with a one-line reason each, so no omission is
silent.

Draft two sections:

- **Extraction Summary**: population, site, period, unit of observation, delivered files and
  fields, and major derivations.
- **Extraction Assumptions / Important limitations**: what the researcher must know to interpret
  the data.

Label each claim as a **confirmed fact** (the release's files support it) or a **question**
(analyst or engineer resolution needed), and give its **proposed wording**. Give each claim an id
(`C1`, `C2`, ...) and keep its sources: review items by slug, id and revision, and release files
by path and tag.

## 5. The analyst decides each claim

Put the questions first, then each claim, via AskUserQuestion, in batches of at most four. For a
claim, show the proposed wording and its sources, with the options **Accept (Recommended)** /
**Reword** / **Reject**. A reworded claim is shown again. For a question, show the conflicting
evidence and the proposed correction, and record the analyst's resolution. An unresolved question
holds the release: the record stays `draft`.

Never fill `decided_by` or `decided_at` from anything but an answered question. `decided_by` is
the analyst's handle (GitHub login where known, else `git config user.name`, else ask; never
`user.email` — `release.sh check` refuses an `@`). `recorded_by` and `resolved_by` follow the same rule. `decided_at` is now (UTC ISO). If
the analyst stops, write a `draft` record with the undecided claims `pending`, and say so.

## 6. Record and render

Write the whole record to `.sqlreview/releases/<tag>/release.json` (the guard validates it):

```json
{"schemaVersion": 1, "kind": "release", "tag": "<tag>", "commit": "<commit from evidence>",
 "status": "approved", "recorded_at": "<UTC ISO>", "recorded_by": "<analyst>",
 "evidence": [{"slug": "<slug>", "revision": 3, "applies": "current"}],
 "claims": [{"id": "C1", "section": "summary", "proposed": "…", "final": "…",
             "decision": "accepted", "decided_by": "<analyst>", "decided_at": "<UTC ISO>",
             "sources": [{"kind": "review", "slug": "<slug>", "item": "A1", "revision": 3},
                         {"kind": "file", "path": "src/pipelines/x.py", "ref": "<tag>"}]}],
 "questions": [{"id": "Q1", "text": "…", "sources": [], "resolution": "…",
                "resolved_by": "<analyst>", "resolved_at": "<UTC ISO>"}]}
```

`evidence` copies `slug`, `revision` and `applies` from `release.sh evidence`. `section` is
`summary` or `assumptions`. `decision` is `pending`, `accepted` (`final` equals `proposed`),
`reworded` (new `final`) or `rejected` (`final` is null). `status` is `approved` only when every
claim is decided and every question is resolved.

```bash
bash "$S/release.sh" check ".sqlreview/releases/<tag>/release.json"    # exit 4 → one violation per line
bash "$S/release.sh" render ".sqlreview/releases/<tag>/release.json" > ".sqlreview/releases/<tag>/release.md"
```

Show the rendered body. It is paste-ready for the release: each claim carries its sources in an
HTML comment, which GitHub does not display. The confirmed technical review is not changed; a
disagreement with a review item goes to the engineer through `/data-request:analyse --update`.
No claim, question or record may contain row-level data: no identifiers, record values or small
cell counts. The analyst publishes the release.
