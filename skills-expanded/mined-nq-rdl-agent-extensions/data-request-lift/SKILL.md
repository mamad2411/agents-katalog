---
name: data-request-lift
license: CC-BY-4.0
description: >-
  Close out request pipelines: inspect the pinned library, classify lift candidates
  with the human, file reusable work on the owning library, and record delivered
  hand-SQL limitations. Revisit released lifts for recurring extracts and candidates
  in builds not yet delivered, without automatic adoption.
argument-hint: '<pipeline path>'
user-invocable: true
compatibility: >-
  .sqlreview schema 2 (schema 1 remains readable); Bash 3.2+, jq >= 1.6.
  record_limitation API floor: query-builder 0.6.0; source
  resolvers live under resolvers/iemr and resolvers/hbcis from 0.5.0;
  inspect the enquiry's actual framework_ref before claiming availability.
allowed-tools: Bash, Read, Glob, Grep, Write, AskUserQuestion
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Data Request — lift

The **Data Engineer** runs library close-out and confirms technical lift
classifications. The Data Analyst owns unresolved research choices.

Close-out asks what belongs in the library; `/data-request:analyse` separately
reviews what the delivered pipeline does. Do not implement library fixes here.

Invoke `/data-request:guardrails` and read the shared ledger contract at
`${CLAUDE_PLUGIN_ROOT}/skills/setup/references/lifts.rst` (canonical source:
`skills/data-request-setup/references/lifts.rst`). Verify correctness-critical API
claims against the pinned implementation and tests in `nq-rdl/query-builder`.
Its source resolvers live under `resolvers/iemr` and `resolvers/hbcis` from
v0.5.0. An older pin may still depend on the archived separate resolver package,
so inspect the pin as it is. Discover releases through the shared tag-list policy
at `${CLAUDE_PLUGIN_ROOT}/skills/guardrails/references/library.rst`; a latest tag
is a discovery aid, not evidence that the request's pin contains a unit.

## Classify-only mode

Use it for a read-only run, such as a read-only subagent, or when the human asks
for a proposal. Do the read-only discovery and scan below; read the ledger files
directly if you cannot run the helper. Propose a bucket and evidence for every
candidate as text, then stop before any write: no `/data-request:setup`, no
`sqlreview.sh` `init`, `publish` or `render`, no AskUserQuestion, no issue filing.
Proposed buckets are unconfirmed. Report close-out as not started.

## Discover before classifying

Resolve the helper at `${CLAUDE_PLUGIN_ROOT}/skills/setup/scripts/sqlreview.sh`.
Run `status --json`, `slug <pipeline path>` and `fingerprint <pipeline path>`.
If uninitialised, use `/data-request:setup --default --yes`; existing config and
custom templates are preserved. Read scope, review and `lifts.json` for that slug.
For schema-1 projects use the bundled lift definition/template when absent;
`render SLUG lifts` installs a missing `templates/lifts.md` and never overwrites.
Read `recurring` from the ledger or explicit request evidence; do not infer it
from a filename or propose a backport for a one-off extract.

Scan the whole pipeline and its local helpers, even when the ledger is populated:
f-string/concatenated SQL, raw query strings, secondary lookup queries, repeated
cohort execution, request-local TypedTables or units, and inline modelling such
as 30-day mortality or latest versus at-time address. Inspect output/metadata
construction too: manually assembled spec descriptions or resolver provenance
may expose a missing library capability.
Read canonical SQL, the dependency lock/framework_ref, matching specs, resolver
handlers and tests at that revision. Record actual paths/revisions and shortfalls;
missing access is unresolved evidence, never proof that a unit is absent.
Capture missed candidates before looking for existing library issues.
If the checkout is only a scaffold, locate the implemented pipeline revision
before claiming a close-out. Reconcile manifest, lock and installed revisions;
a manifest/lock disagreement makes the effective pin unresolved.

## Confirm the boundary

Propose a bucket for every candidate, including composition that should stay local:

- `new-capability`: no pinned unit expresses the reusable need.
- `existing-unit-gap`: a pinned unit exists but lacks required behaviour.
- `request-specific`: researcher modelling or composition using sufficient units.
  An agent not knowing an existing API is a composition error, not a library gap.
  A request-local TypedTable or unit is a `request-specific` candidate, not hand
  SQL: record it in the ledger; it needs no library issue.

Put each candidate, classification, evidence and proposed disposition to the human
via AskUserQuestion, at most four per batch (use smaller batches if the host limit
requires). Options: **Confirm (Recommended)** / **Reword** / **Reject**. Ask again
after rewording. Rejected candidates remain in `lifts.draft.json` with the reason;
remove them from the published ledger so they cannot authorise future hand SQL.
Unanswered candidates stay `candidate`; stop dependent filing, keep the draft.
Never fill any confirmation field without the human's answered question.
The entry revision, not an unrelated newly appended candidate, binds the answer.

## File and record delivery

For confirmed library candidates, search the owning library's open and closed
issues for equivalent work before creating anything. Reuse a matching issue after
checking its evidence and scope; do not create a duplicate on retries. For new
issues use the fixed [evidence block](references/evidence.rst), with canonical SQL
and regression expectations grounded in inspected sources. The owning repo is
`nq-rdl/query-builder`, for shared composition/spec infrastructure and for
source-specific resolvers (`resolvers/iemr`, `resolvers/hbcis`). Invoking this skill
includes filing confirmed library candidates. Do not file on the enquiry repo.
Use a structured GitHub tool or `gh issue create --repo <owner> --body-file <file>`.
After success record the returned URL and `filed`; after an uncertain response,
search for the issue before retrying. Keep confirmed evidence intact across retries.
Publish/render the ledger through the shared helper after each successful filing.

For every delivered-by-hand library candidate, propose a review limitation with
`lift_id` and exactly this text, derived from the ledger:

> <need> resolved with in-repo SQL. Library unit tracked in <issue_url>. Not backported.

Confirm it with the human under the existing review contract. Never autonomously
stamp limitation confirmations. Increment the review revision and reassess every
assumption/limitation as analyse requires; publish, snapshot and render only after
confirmation and a current fingerprint. If no review exists, hand off to analyse
with the proposed limitation; report close-out incomplete until it is recorded.
For request-specific hand SQL there is no library issue: propose a truthful
limitation describing the local composition and no planned backport, without a
fabricated URL. Keep rejected/unconfirmed delivery risks visible in the draft.
Recommend recording the confirmed text with `pipeline.record_limitation(text,
consequence=...)` beside the workaround so the rendered header carries it; draft or
fix makes that edit, and recomposition removes it with the workaround.

## House-style hand-off

When you propose or launch the house-style workflow (`/rdl-team:workflow`) for
filed library work, first reuse a recorded direct-mode decision for the same
repository `owner/name` (for example one recorded by triage); do not ask twice.
Otherwise ask once, up front, whether to authorise spec-kit
`generativeMode: "direct"` for `specify`, `plan`, `tasks` and `analyze`. Record a
yes as a workflow decision in exactly this shape and pass it in the workflow
`decisions`:

```json
{"decision":"generativeMode","value":"direct","by":"<who>","at":"<ISO-8601 time>","scope":"nq-rdl/query-builder"}
```

Set `by` to the person's GitHub login, never an email address. Set `scope` to
the owning repository's `owner/name`. If a worktree for the work already exists,
add the same record with its absolute path as `scope`. The workflow matches only
the unit's worktree path; the main session translates
`owner/name` into the unit's `physicalWorktree`. Without a recorded yes, keep
`invoke`. Clarify, `analyze` remediations and constitution changes stay with the
human. Routing `/speckit.*` through another agent (Codex, a subagent) to avoid
`disable-model-invocation` is not a workaround; direct mode is the supported path.

## Release revisit and recurring follow-up

For a build **not yet delivered**, revisit `candidate` entries even with
`recurring: false`. Resolve the latest stable tag for each entry's owning library
using the shared tag-list policy, then run `sqlreview.sh lifts-stale SLUG --tag TAG`.
For mixed-library ledgers run once per owning library's latest tag; use only that
library's rows from each result. Entries without unit references still need manual
inspection. A symbol-presence result is only a nudge: check the complete shortfall,
implementation and tests. Partial results leave the other units unresolved.
Propose the exact re-pin and re-composition, not an automatic pin or status edit.
The human decides whether to adopt it: a released class may include clinician names
that the request intentionally excludes. Preserve approval restrictions and the
confirmed output; do not treat an engineer's API choice as a research answer.
After acceptance, use draft and analyse, and reconfirm changed ledger evidence.
Do not invent an issue or advance a candidate through the filed/released lifecycle.

For `filed` entries inspect the linked issue, merged change and release/tag that
contains it. A closed issue alone is not release evidence. On verified release,
record `release_evidence: {version, url}` and advance to `released`, retaining the
human-confirmed need. For an explicitly recurring extract propose the exact pin
bump and re-composition, with changed APIs and tests to verify. After the user
accepts, hand off to `/data-request:draft`, then `/data-request:analyse`; advance
to `recomposed` only after the workaround is removed, validation succeeds and the
updated review is confirmed. Record `recomposition_evidence` with the new `pin`,
`sql_sha256` and `review_revision`. Retain the original delivery limitation as history.
Already-delivered one-off extracts stay forward-only; do not open backport issues
or modify their pins. An undelivered one-off candidate may receive the proposal above.

## Upstream decision candidates

Scope and review items marked `upstream` repeat a listed decision (#362); they are not hand SQL.
List them by decision with `bash "${CLAUDE_PLUGIN_ROOT}/skills/setup/scripts/recurring-decisions.sh" marked`
on the slug's `scope.json` and `review.json`. For each target issue, link it or add one evidence
comment, or file a new issue, without duplicates and only after the human confirms. Follow
`${CLAUDE_PLUGIN_ROOT}/skills/setup/references/recurring-decisions.rst`, including the list change it proposes.

## Report

Report candidates by bucket, upstream decision candidates, issue links, unresolved
confirmations/evidence and review limitation publication status. Do not call a candidate filed or a close-out
complete until those writes have succeeded.
