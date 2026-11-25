---
name: data-request-analyse
license: CC-BY-4.0
description: >-
  Review a finished SQL file for handoff: read it against its scope, record purpose, inputs,
  outputs, logic steps, assumptions and limitations in .sqlreview/reviews/<slug>/review.json,
  with every assumption and limitation confirmed by the human, and render the standardised
  review.md. Re-running on reviewed SQL diffs against the stored snapshot, walks the human through
  the change, and reassesses every item the change touches. Use when SQL is ready to hand to the Data Analyst.
argument-hint: '<sql path> [--update]'
user-invocable: true
compatibility: >-
  .sqlreview schema 2 (schema 1 remains readable) (docs/specs/2026-09-15-sql-review-plugin-design.md); bash 3.2+, jq >= 1.6,
  git optional (required only for header-decision eligibility; diffs use the stored snapshot).
  The analysis-notes header read by `notes` needs query-builder 0.6.0 or later.
allowed-tools: Bash, Read, Glob, Grep, Write, AskUserQuestion
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Data Request — analyse (Data Engineer)

The **Data Engineer** runs analyse. Keep the Data Analyst's imported research
decisions and provenance visible; confirm technical SQL findings with the
engineer. Any research question missed by intake belongs to the analyst:
prefix its shared question's text `Analyst question:` and send it back through
the handoff for the analyst to consult the requester. Do not relabel an
engineer confirmation as an analyst confirmation.

For RDL cohort SQL, read `${CLAUDE_PLUGIN_ROOT}/skills/guardrails/SKILL.md` before
scoping or reviewing. Consult its dataops/column-spec sources and carry evidence or
unverified facts into the discussion; advisory findings do not replace human confirmation.

Arguments: `$ARGUMENTS`.

```bash
S="${CLAUDE_PLUGIN_ROOT}/skills/setup/scripts"
bash "$S/sqlreview.sh" status --json                # exit 3 → stop: not initialised, run /data-request:setup first
SLUG="$(bash "$S/sqlreview.sh" slug "<sql path>")"  # exit 5 → bound to another path: offer `sqlreview.sh move OLD NEW`;
                                                    # a stderr legacy-review note → offer its `move --slug OLD_SLUG NEW`
bash "$S/sqlreview.sh" fingerprint "<sql path>"     # {sql_path, sql_sha256, sql_body_sha256, git_commit, git_dirty} — embed as-is
```

Read `definitions` from `.sqlreview/config.json` and use that wording verbatim when deciding and
explaining what is an assumption and what is a limitation; never paraphrase it. If
`reviews/$SLUG/scope.json` exists, Read it — the review is written *against* the scope. If it does
not, offer `/data-request:bootstrap` retroactively once, then continue without it if declined.

Before the delta/unchanged-SQL path, apply guardrails `references/grain.rst`: compare
intake/scope and each output's actual grain with answers. Reuse one `L-grain-answers`
drift record and offer an answers correction in the same change; preserve expected
finer outputs. Bare Patient is not an agreed grain or a reason to change released SQL.

## Before presenting prose (fresh or update)

**Name the constant, never its value** in scope/review prose, drafts, logic descriptions,
questions and change summaries (for example, `EVENT_CD`, not its numeric value).
`code-value` scans string fields for maximal runs of 8 to 10 digits, except validated
machine metadata (SQL path/bound slug, fingerprints and ISO timestamps at known locations).
Keep that metadata as-is; lint exemptions do not waive `check` or publication validation.
Never add prose codes to `.pii-code-values` or suppress the PII gate to clear them.

Before every question batch or displayed summary, stage the proposed wording in
`.sqlreview/reviews/$SLUG/review.draft.json`, including stored prose, recurring suggestions,
delta/impact explanations and `bulk`/`walk` questions. Inspect raw helper output locally;
do not paste it into questions. Run:

```bash
bash "$S/sqlreview.sh" lint --ste ".sqlreview/reviews/$SLUG/review.draft.json"
# exit 10 → <id>\t<field>\t<rule>\t<detail>, without code values; other failures → stop
```

Replace each prose code with its constant name and fix STE wording before showing it.
Re-run lint after edits; decision-source warnings require a source check, not a made-up source.
Reworded confirmed items need fresh human confirmation; do not retain their carried
confirmation or edit the final JSON. Lint cannot grant confirmation. A reworded scope
item no longer matches its scope text, so it is walked.

Some decisions recur in every enquiry (#362). Before you put candidate items to the engineer, run
`bash "$S/recurring-decisions.sh" match ".sqlreview/reviews/$SLUG/review.draft.json"`. For each other match,
show the prior enquiries, offer the listed wording and mark the item `upstream`, as
`${CLAUDE_PLUGIN_ROOT}/skills/setup/references/recurring-decisions.rst` says. The engineer still confirms each other item;
the exact recorded TUH house default is not a fresh facility question. Preserve its upstream origin,
and verify the SQL implementation during review.
Rows from `carryforward` include recorded `upstream` and `decided`: preserve them.
Rows from `carryover` omit `upstream`: copy it from the scope item when you re-draft.

## Decision origin (#434)

Keep decision origin separate from engineer confirmation. When evidence identifies the
decider, attach optional `decided: {by, role, at, source}` to the item: a human handle,
role, decision date or ISO time, and comment/PR URL or dated document reference.
Use `unlinked (verbal)` for a reported verbal decision; never invent a source, decider
or date from rationale wording. If origin is unknown, omit `decided` and surface the
attribution question. Show the provenance with the item before confirmation.
Preserve `decided` verbatim when re-drafting, including header candidates, carryover
and carryforward; adding, changing or removing it requires fresh confirmation. Run plain
`lint` before publish: provenance warnings need a source check, separate from wording
reconfirmation. A lint hint is advisory; it does not establish who decided.

## Pre-run plausibility: operator proposals only

Before the delta/unchanged-SQL path, read guardrails `references/performance.rst`,
**Pre-run plausibility**. Compare the population answers in scope with the current SQL;
carry unresolved or contradicted limits into the review and analyst questions without
inventing restrictions. Return the inventory and a proposed count-only probe for **each label column**
across all final outputs, including expected labels/format, SQL location, bounds/cost and suppression.
For expensive requests only, propose an age-band probe with the scoped age anchor and cost evidence.
This check runs **no SQL**: mark proposals **proposed, not executed**, not OBSERVED findings.
Reuse valid existing proposals on reruns but recheck scope, output columns and bounds even if SQL
is unchanged. Show this proposal table alongside `review.md`, not as a confirmed probe result.
Unknown labels/thresholds remain unverified; do not fabricate confirmations to publish a review.

The operator needs explicit authorisation to run approved probes before the delivery run.
Returned counts inform UAT and the data dictionary; surprises go to the analyst, not an automatic
cohort filter. Before showing counts, apply guardrails `references/release.rst`, **Probe disclosure control**. Apply *After review* below for the separate authorised run and handoff.

## Existing review → update path (#130 §2)

If `reviews/$SLUG/review.json` exists (or `--update`):

```bash
bash "$S/sqlreview.sh" delta "$SLUG"     # exit 0 → check review-content changes before completion below · 10 changed · 6 no baseline → full review below (retain revision history) · 2 missing SQL → stop/rebind
```

### Unchanged SQL: complete publication before stopping

Only when the grain precheck requires no review-content change, use this exit-0
completion path. Otherwise bypass this early return and take *Metadata-only changes*
below. `delta` compares SQL bytes, not intake, answers or review content.

On exit 0, the SQL body remains bound, including `header-only` status. Inspect a header-only
diff and run `notes "<sql path>" --against ".sqlreview/reviews/$SLUG/review.json"` before
completion. A body match does not confirm changed assumption text or rationale: reconcile
those differences and obtain fresh confirmation through the update path. For wording-only
header corrections that leave the confirmed record intact, publish that record again to
record the header revision, then render it.
A previous run may have published and snapshotted successfully but failed or stopped
before question publication or rendering. This recovery uses the existing confirmed
revision; do not increment it or ask for its confirmations again. If the declared
store is missing, Read the retained `questions.draft.json` and check its binding and
answers before retrying publication. Do not invent a replacement if the draft is
missing, or overwrite an invalid existing store. Run from the project root:

```bash
bash "$S/sqlreview.sh" publish "$SLUG" review ".sqlreview/reviews/$SLUG/review.json" || exit $?
if ! bash "$S/sqlreview.sh" questions "$SLUG" review >/dev/null; then
  # Recover only a missing first store, never repair an existing invalid one implicitly.
  [ ! -e ".sqlreview/reviews/$SLUG/questions.json" ] && [ ! -L ".sqlreview/reviews/$SLUG/questions.json" ] || exit 4
  [ -f ".sqlreview/reviews/$SLUG/questions.draft.json" ] || { echo "Missing question draft; handoff incomplete" >&2; exit 4; }
  bash "$S/sqlreview.sh" publish-questions "$SLUG" ".sqlreview/reviews/$SLUG/questions.draft.json" || exit $?
fi
bash "$S/sqlreview.sh" render "$SLUG" review || exit $?
if jq -e -s 'length == 2 and (.[0] | del(.header_revisions)) == (.[1] | del(.header_revisions))' \
    ".sqlreview/reviews/$SLUG/review.draft.json" ".sqlreview/reviews/$SLUG/review.json" >/dev/null 2>&1; then
  rm -f ".sqlreview/reviews/$SLUG/review.draft.json"
fi
if [ -e ".sqlreview/reviews/$SLUG/review.draft.json" ]; then
  printf 'Stop: review draft contains unpublished work; retain it for completion.\n' >&2
  exit 4
fi
```

Show `review.md`. Review draft equality is semantic, ignoring only helper-owned
`header_revisions`; formatting and header history are not unpublished work. Keep any
differing or unreadable review or question draft and tell the user it contains
unpublished work; do not discard it or publish it automatically over a valid store.
Stop before *After review* when unpublished work remains; continue below only when
no unpublished draft remains. If question publication or rendering fails, retain
both drafts and report the handoff incomplete; retry this completion step once
the cause is fixed.

### Metadata-only changes: update despite unchanged SQL

On exit 0, a newly confirmed grain, a need to add or revise `L-grain-answers`, or a
correction to retire a resolved drift finding requires a review update. Compare the
precheck with the published review; do not increment merely because the check ran.
An unconfirmed proposal stays in the draft/handoff until answered; it is not published
by this path or discarded by completion.

For a required update, there are no SQL hunks or impact hints to walk. Continue at
steps 3–4 of *Changed SQL* below: draft the next revision, run `carryforward`, reassess
items implicated by the grain/evidence change even when their SQL lines are unchanged,
increment the revision and append to `changes[]`. Then follow *Confirm, write, render*,
including confirmation/carry gates and publish → snapshot → render. Do not change SQL
or auto-confirm a new or reworded item to make this update possible.

### Changed SQL: reassess the review

On exit 10, continue with impact hints and the update below:

```bash
bash "$S/sqlreview.sh" impact "$SLUG"    # HINTS ONLY: identifiers from the changed lines traced into unchanged lines
```

1. Before discussing the delta, stage explanations and questions in the review draft and run
   the pre-presentation lint above. Inspect hunks locally; do not paste raw delta output or
   numeric code values into the discussion. Walk the human through each hunk with the linted explanation:
   what it changes about grain, filters, joins or output, naming constants rather than values.
   Repeat the check for each hunk's questions, then pause (AskUserQuestion: **Continue** / **Discuss**).
2. Stage and lint the impact discussion before showing hints as *places to look*, then check
   the unchanged code yourself for indirect consequences the hints cannot see (a changed literal, join type or `DISTINCT` shifts grain
   without touching an identifier). Confirm or dismiss each candidate with the human.
3. **Reassess the existing assumptions and limitations.** Draft the next revision keeping each
   unchanged item's `id`, `text` and `rationale` verbatim and its old ranges. Compute unchanged
   `location.lines` and `logic[].lines` from the authenticated baseline, then find which keep
   their confirmation (#348):

   ```bash
   bash "$S/sqlreview.sh" remap "$SLUG" ".sqlreview/reviews/$SLUG/review.draft.json"
   # → {document, prior_revision, remapped: [{kind, id, from, to}], walk: [{kind, id, lines, why}]}
   bash "$S/sqlreview.sh" carryforward "$SLUG" review ".sqlreview/reviews/$SLUG/review.draft.json"
   # → {prior_revision, revision, sql_unchanged, sql_body_unchanged, carry: [{kind, id, basis, set}],
   #    bulk: [{kind, id, text, rationale, location, why}], walk: [{kind, id, why}]}
   ```

   `remap` edits only draft ranges, never confirmations or fingerprints. Its `walk` ranges
   stay untouched: reassess their current lines with the human, including affected logic steps,
   before using `carryforward`. Repeated governed text present in an edit is conservatively
   ambiguous, not proof of a safe remap. New/manual ranges stay yours; retries do not shift twice.
   With no draft argument, it seeds or updates `review.draft.json` from the published record
   (scope when no review exists); set the next revision and fresh fingerprint yourself.

   Copy each `carry` item's `set` fields (with `carried_basis`) onto it verbatim; do not ask
   again. Re-run the pre-presentation lint before each `bulk`/`walk` question batch, including
   stored and newly drafted items; reworded carried items need fresh confirmation.
   Ask the `bulk` items once, with their `location` lines, as
   [references/carry.rst](references/carry.rst) describes. Confirm / reword / drop the `walk` items
   (hint-flagged first), plus any `carry` item the hunks or hints implicate indirectly, and add
   new ones. When the human asks for a full re-walk, walk every item and publish with `--reconfirm-all`.
   Seed new header items as in *Rendered header* below, `--against` the published `review.json`.
4. Set `revision` to the previous value + 1, append to `changes[]` `{revision, at, by, summary}`.
   Then *Confirm, write, render* below.

A missing baseline is still an update: preserve the existing `changes[]`, increment the previous
revision, and reassess every item `carryforward` does not list under `carry` (without a baseline
only an unchanged SQL SHA can carry). Never reset an existing review to revision 1.

## Full review

Read the SQL. Draft into `reviews/$SLUG/review.draft.json` (guard-exempt) as you go:

- **purpose** — one paragraph, in the analyst's terms.
- **inputs** — every source with what one row means; **outputs** — `grain` plus each column.
- **logic** — numbered steps with the SQL line range each covers (`lines: [from, to]`): CTE by CTE,
  then the final select; joins, filters and aggregations named explicitly.
- **assumptions** — every place the SQL commits to one reading where the request allowed more;
  **limitations** — every constraint the analyst must know before relying on the output. Give
  each the `location` lines it governs and a one-line rationale. Where an item restates a
  confirmed scope item that still holds, keep the scope's `text` and `rationale` verbatim so it
  can be carried over (below); copy its optional `decided` object verbatim, preserving the original actor,
  role, source and date-only precision, separate from the review confirmer. Decision origin does not supply confirmation.
  Reword only where the SQL changed what is true; retain the origin of any decision that still applies.
- **questions.json** — load `bash "$S/sqlreview.sh" questions "$SLUG" review` on every
  resume: it includes the scope's questions and review-only questions. Never seed a second
  list from scope. Follow `${CLAUDE_PLUGIN_ROOT}/skills/setup/references/questions.rst`;
  migrate legacy strings once, retain stable IDs, owner and closure provenance. Add SQL-specific
  open rows with `applies: review`; close only from an evidenced answer with `publish-questions`.
  Closure alone changes no scope/review revision or confirmation. Publish the question draft
  after the first review publication and before render; failures leave the handoff incomplete.

### Rendered header (#355)

SQL generated by query-builder 0.6.0+ may open with the assumptions and limitations its
pipeline recorded ([contract](https://github.com/nq-rdl/query-builder/blob/main/docs/ANALYSIS_NOTES.md)):

```bash
bash "$S/sqlreview.sh" notes "<sql path>" --against ".sqlreview/reviews/$SLUG/scope.json"  # drop --against if no scope
# → {present, lines, assumptions|limitations: [{text, rationale, lines, match}]} · exit 4 malformed → report the line, continue without it
```

Header items are candidates, not confirmed items: each still goes to the human under
*Confirm, write, render*, never confirmed because the pipeline recorded it. Seed each with the header
text verbatim, `"status": "candidate"` and its `rationale` (a limitation's consequence; draft one
with the human if null); where `match` names an existing item, keep that item's id, text and
rationale verbatim instead, so carryover/carryforward still recognise it. Set `location` to the
SQL lines the item governs, not the header `lines`. Then review the SQL for what the header
omits; `present: false` is not evidence of no assumptions.

## Confirm, write, render

Apply the pre-presentation lint above before each batch below, the carry-over question included (#394).

The human-in-the-loop trigger (#130 §1.1). On an update, items `carryforward` listed under
`carry` are already settled: leave them out of everything below. First, when a scope exists,
find what bootstrap already settled:

```bash
bash "$S/sqlreview.sh" carryover "$SLUG" ".sqlreview/reviews/$SLUG/review.draft.json"
# → {scope_revision, sql_unchanged, sql_body_unchanged, scope_before_sql, carry_over: [{kind, id,
#    scope_id, basis, text, rationale, location, decided?}], carry_over_intent: [same], walk: [{kind, id, why, decided?}]}
```

`carry_over` and `carry_over_intent` list draft items whose list, text and rationale match a
confirmed item of the current scope revision; `basis` is the evidence. Check the SQL against
each, then ask each non-empty list as **one** question, as
[references/carry.rst](references/carry.rst) describes: `carry_over` (the SQL under the item did
not change) with **Carry over all (Recommended)**, `carry_over_intent` (the SQL changed or came
after the scope) with a delta summary and no recommended option. Every item shows its `location`.
Copy each row's optional `decided` onto the draft item verbatim, including matched scope items
returned under `walk`; never replace it with the new confirmer or confirmation timestamp.
Do not invent an origin when absent.

### Named dated header decisions (#431)

For remaining candidates, establish the **explicit intended human confirmer's handle** before
running the command below. Ask if it is not explicitly known; do not infer it from config
`roles` (display labels), `recorded_by`, git author/committer or the header decider. Header/git
bytes prove recorded attribution, not human identity or an answer.

```bash
bash "$S/sqlreview.sh" notes "<sql path>" \
  --against ".sqlreview/reviews/$SLUG/review.draft.json" --confirmed-by "<human handle>"
# → header_carry_over: [{kind, id, text, rationale, location, basis:"header-decision",
#                      decided:{by,role,at,source}, evidence:{commit,committed_at,precision,...}}]
#   header_walk: [{kind,id,text,rationale,location,why}]
```

Exclude items already settled by carryforward or an answered scope question. Check indirect
SQL effects yourself; move affected items to the walk even if their line bytes match. Ask the
remaining `header_carry_over` as **ONE** question: **Carry over all (Recommended)** / **Walk each
individually**. List every kind/id, text, rationale, governed `location`, `decided` and observed
source commit/time, as [references/carry.rst](references/carry.rst) specifies. For date-only
attribution, explain that proof begins at the displayed source time that day, not midnight.
A later-day source or a source after a precise ISO cutoff is not eligible.

Only an **answered** Carry over all question permits copying the listed `decided` verbatim and
setting `carried_basis: "header-decision"` plus fresh `confirmed_*` for this revision from that
answer. Never invent confirmation fields from the candidate rows. Preserve an existing
independent `decided` unchanged: a provenance mismatch is walked, not overwritten to gain
eligibility. Mixed deciders matching another handle are walked with the current confirmer.
Walk each individually (or no answer/interruption) sets nothing; leave the draft unpublished
until all remaining items are answered. Publish re-proves header evidence, but cannot authenticate
who answered. A subsequent update uses normal carryforward, retaining `decided` and copying its
`set`; do not reuse header-decision as a previous-revision confirmation.

Changed, missing, shallow, ambiguous repeated/relocated ranges, relevant merge/rename evidence
and malformed/unnamed attribution go to `header_walk`. Unrelated PR merges alone do not block
eligibility. Only leading comment growth is remapped automatically; body-prefix structural
changes are conservative walks. No git history means ordinary per-item confirmation, not a
blocked review. Correctness and source authenticity still require human/source inspection.

Then put **each** remaining candidate (scope/header `walk`, or every unsettled item) to
the engineer via AskUserQuestion — batches of at most four per call, one question per item
showing its text and rationale, options **Confirm (Recommended)** / **Reword** / **Reject**.
Reworded items are asked again. Only confirmed items reach `review.json`; rejected ones stay in
the draft. If the engineer stops, leave the draft and write nothing final — say so.

**Never fill `confirmed_by`, `confirmed_at` or `confirmed_revision` from anything but an answered
question** (a bulk answer, carry-over or `bulk`, counts for the items it listed, and only those): `confirmed_by` is the user's handle (GitHub
login explicitly known, else ask; never a role label, recorder or git author; never `user.email` — `check` refuses an `@`),
`confirmed_at` is now (UTC ISO), `confirmed_revision` equals the document `revision` — except an
item carried forward on an update, which takes exactly the `set` fields `carryforward` printed.
Never set `carried_from_revision` by hand.

Before publishing SQL with a header, run `notes "<sql path>" --against` the confirmed draft.
Flag each mismatch to the human and as an open row in `questions.json`: a header item with `match: null`
(rejected or reworded) or a confirmed item the header contradicts. Suggest correcting the
pipeline's record with `/data-request:fix`.

Re-run fingerprint and compare its SHA with the bytes you reviewed; if different, reassess the
change before continuing. Write the complete confirmed document to
`.sqlreview/reviews/$SLUG/review.draft.json`, then publish it with the command below:

```json
{
  "schemaVersion": 2, "kind": "review", "slug": "<SLUG>", "sql_path": "<sql path>", "title": "…",
  "revision": 1, "recorded_at": "<UTC ISO>", "recorded_by": "<user>",
  "sql_sha256": "<from fingerprint>", "sql_body_sha256": "<from fingerprint, or null if malformed>", "git_commit": "<from fingerprint>", "git_dirty": "<boolean from fingerprint; preserve its JSON type>",
  "purpose": "…", "grain": "one row per …",
  "inputs":  [{"name": "schema.table", "description": "one row per …"}],
  "outputs": [{"name": "column", "description": "…"}],
  "logic":   [{"step": 1, "title": "…", "lines": [1, 12], "description": "…"}],
  "assumptions": [{"id": "A1", "text": "…", "rationale": "…", "location": {"lines": [3, 5]},
                   "status": "confirmed", "confirmed_by": "<user>", "confirmed_at": "<UTC ISO>", "confirmed_revision": 1}],
  "limitations": [{"id": "L1", "text": "…", "rationale": "…", "location": null,
                   "status": "confirmed", "confirmed_by": "<user>", "confirmed_at": "<UTC ISO>", "confirmed_revision": 1}],
  "question_store": "questions.json",
  "changes": [{"revision": 1, "at": "<UTC ISO>", "by": "<user>", "summary": "initial review"}]
}
```

```bash
bash "$S/sqlreview.sh" publish "$SLUG" review ".sqlreview/reviews/$SLUG/review.draft.json" || exit $?
bash "$S/sqlreview.sh" snapshot "$SLUG" "<sql path>" || exit $?  # only AFTER publish succeeds
bash "$S/sqlreview.sh" render "$SLUG" review || exit $?  # → reviews/<slug>/review.md (never hand-write it)
rm -f ".sqlreview/reviews/$SLUG/review.draft.json"
```

Show `review.md`. Continue with *After review* below.

Publish validates a staged copy, confirmations, next revision and current SQL fingerprint before
atomically replacing `review.json`, and re-proves each carried item against the previous
`review.json` and `source.sql` (so snapshot must follow every publish); on refusal, re-run
`carryforward` and walk what it lists. Never copy or patch the draft directly into the final path.
Snapshot verifies the final review hash before advancing `source.sql` and preserves
`history/<revision>.sql` for resumed explanations. Stop on any failure and keep the draft. A failed
or interrupted publish must never advance the baseline; a failed snapshot leaves the review stale. A header-only snapshot retains the authenticated original bytes; never replace historical snapshots from a claimed body match.

## After review: operator run, UAT and analyst hand-off

The Data Engineer completes `analyse`, the authorised operator run and UAT, then hands the
extract to the Data Analyst. The engineer never releases the extract. The analyst runs
`/data-request:explain`, then accepts it for release preparation, sends it back or uses
`/data-request:amend` for presentation changes. Only the analyst prepares the body through
`/data-request:release <candidate ref>` and publishes the release.

Read `${CLAUDE_PLUGIN_ROOT}/skills/triage/references/handoff.rst`, *Hand-off to review*.
Use that existing procedure after the operator run and UAT, including its run-evidence gate,
child-issue comment, reviewer assignment and board moves. A rendered review alone does not
complete the hand-off. Require the request runbook's **Delivery** section to point to this
same triage hand-off and name the analyst's next step; flag a missing section for the engineer.
Do not run the extract or write to GitHub without the procedure's explicit authorisation.
