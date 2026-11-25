---
license: CC-BY-4.0
description: >-
  Interview the Data Analyst on the research decisions of a data request — cohort and age
  limits, code-set edges, outcomes and windows, identifiers and presentation, governance and
  the grain — then fill answers.yaml, write answers.intake.json (schema 1) and, on approval,
  render the data-analysis-scaffold over a request-template repo with copier. Needs no
  .sqlreview/. Re-running walks through what changed. Use before the engineer's
  /data-request:bootstrap, whenever an analyst fills or revises answers.yaml.
argument-hint: '[answers.yaml path] [--update]'
user-invocable: true
compatibility: >-
  answers.intake.json schemaVersion 1, validated by data-analysis-scaffold validate-answers or a
  generated child's scripts/validate_answers.py (sidecar checks from scaffold v0.5.1). Render
  step verified with copier 9.18.2, scaffold v0.5.1 and request-template 47b702d; needs
  copier >= 9.15 and GitHub access to nq-rdl/data-analysis-scaffold. Python 3 with PyYAML.
allowed-tools: Bash, Read, Glob, Grep, Write, Edit, AskUserQuestion
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Data Request — intake (Data Analyst)

The **Data Analyst** runs this pass while filling `answers.yaml`, before the Data Engineer
starts. The analyst has the requester's knowledge: what the research needs. The engineer has
the systems knowledge: which sources, keys and joins deliver it. This skill is the analyst's
interview; `/data-request:bootstrap` is the engineer's. It is not a separate stage: it is the
`answers.yaml` filling pass, guided.

Arguments: `$ARGUMENTS` — the answers file (default `answers.yaml` at the repository root).
The sidecar is always its sibling `answers.intake.json`.

Before this skill: Power Automate opens the enquiry issue in `rdl-service-desk/service-desk`,
and the analyst creates the request repository from `rdl-service-desk/request-template` with
GitHub's template button and opens it in the session. This skill does not create repositories.

Read `${CLAUDE_PLUGIN_ROOT}/skills/setup/references/analyst-intake.rst` first. It is the
schema contract shared with `validate-answers`; this skill does not restate it. It writes
`answers.yaml` and `answers.intake.json`; only the approved copier run writes anything else.
Never write `.sqlreview/`, `scope.json` or SQL, and do not require `/data-request:setup`: the
engineer runs it later.

## Validate before and after

```bash
pixi run python scripts/validate_answers.py answers.yaml    # generated child
data-analysis-scaffold validate-answers answers.yaml        # otherwise, when installed
python .github/scripts/validate_answers.py answers.yaml     # request-template seed: answers.yaml only
```

Run one before the interview (an existing sidecar can already be invalid) and again after
every write. The first two validate the sibling sidecar too, but only from a scaffold that
ships `scripts/analyst_intake.py`. Diagnostics name fields, never values.
If neither command is available, say that validation did not run; never report a pass.
The seed's `.github/scripts/validate_answers.py` checks required fields and choices only:
it never reads the sidecar, so its pass is not a sidecar pass.

## Gather the evidence

Read `answers.yaml`, the enquiry (service-desk issue, intake form, requester comments) and the
governance approval when the analyst supplies them. Draft each proposed decision from that
wording and cite where it came from in `rationale`. The analyst's answer is the confirmation;
a draft built from request text is only a proposal until they answer.

## The interview

Ask about research decisions only, in this order. Each topic maps to a schema `topic`:

1. **cohort** — the cohort in clinical terms; age limits with their anchor (age at index event
   differs from age today); sex; inclusions and exclusions. Facility: when the request is silent
   or names TUH, the engineer imports the TUH house default — do not ask. Record a facility
   decision only when the request names a different facility set.
2. **codes** — each code set, its edges and edition (which subcodes count, whether a category
   includes its children). For code discovery run `/data-request:lookup`, and cite its record
   (not its counts) in the decision's `rationale`. A lookup hit is not the analyst's choice.
3. **outcomes** — each outcome, its window and anchor, and who applies it (SQL or researcher).
4. **outputs** — required identifiers and presentation (column names, formats, de-identified
   or identified).
5. **governance** — the approval number and any known restriction. A restriction applies at
   once. An approval number alone does not prove each element was checked; that check is the
   analyst's at delivery review.
6. **grain** — always ask, in these words: "What does one row represent — one row per <unit>,
   in clinical terms? Are any requested outputs finer, such as per surgery or per ward stay?"
   Record the answer as the one `grain` decision with `unit` and any `finer_outputs`.
   `measurement_granularity: Patient` in `answers.yaml` is often an untouched Copier default,
   not an answer: never copy it into the sidecar, even when it matches.

Put proposals to the analyst with AskUserQuestion, at most four per call, one question per
decision. Show the proposed `text` **and** `rationale` — both are recorded. Options:
**Confirm (Recommended)** / **Reword** / **Leave open**. A reworded decision is asked again
in its new words. **Leave open** becomes an `open_questions` entry phrased for the requester,
with the proposed reading noted. Batch the open questions so the analyst can send them to the
requester in one message.

Stay out of the engineer's lane. Do not ask about source tables, joins, keys, timezones,
validity rules or SQL. If the analyst volunteers one, keep it for the hand-off note; do not
record it as a decision. Prior SQL or delivery can support a proposal, but only the analyst's
answer confirms it.

## Recording a decision

- `confirmed_by` is the analyst's handle: GitHub login when known, else
  `git config user.name`, else ask. Never an email, and never the agent's identity.
- `confirmed_at` is the UTC time of the analyst's answer (`YYYY-MM-DDTHH:MM:SSZ`).
- `decided` only when the evidence names who made the decision (for example a requester's
  dated reply); omit it otherwise. Never infer a decider or date from prose.
- `approval_number` matches `answers.yaml` exactly.
- No identifiable patient data, and no lookup counts, in either file.

With no human to answer (a non-interactive run), confirm nothing: every proposal goes to
`open_questions`. A partial intake is valid; an invented confirmation is not.

## Fill `answers.yaml` in the same pass

When an interview answer fills an empty or placeholder field, or contradicts one (for example
the grain answer against `measurement_granularity`), show the field and the proposed value
and write it only when the analyst agrees. Offer each correction once. If the analyst
corrects `approval_number`, the sidecar takes the corrected value.

Field ownership — write a field only where this table allows it:

| Field | Owner | This skill |
|---|---|---|
| `answers.intake.json` | Analyst | Writes all of it |
| `request_id` | Analyst | The enquiry number from the service-desk issue, as issued: `THHSRDLENQ-<n>`, no zero padding |
| `approval_number`, `governance_type` | Analyst | Asks under governance; writes after confirmation; keeps the sidecar's approval equal |
| `measurement_granularity` | Analyst | Sets it from the grain answer, never from a default |
| `short_title`, `project_title`, `project_description`, `delivery_outcomes`, `requestor_name`, `requestor_email` | Analyst | Fills from the enquiry, after confirmation |
| research text (`inclusion_criteria`, `exclusion_criteria`, `requested_data_elements`, `ehr_sources`) | Analyst | Fills or corrects from answers, after confirmation |
| `license`, `platform`, `include_*`, `use_*`, `framework_ref`, `engineering_reviewers` | Engineer / defaults | Never changes them; shows them before the render |

A `request-template` copy holds a short form without most of these fields: add them. The
rendered project's validator requires every field in the first five rows, and copier
renders a missing one as its placeholder text. `measurement_granularity` is blank in the
seed: map the grain answer to `Patient`, `Admission`, `Encounter` or `Observation`. If no
choice fits the clinical unit, ask which to use and keep the exact unit in the sidecar.

## Render the scaffold (after approval)

A `request-template` copy is a thin seed. Rendering the scaffold over it gives the project
its pipeline, validator and DVC layout, which a supplied cohort needs. Do it once, after the
sidecar validates, and only when the analyst approves:

1. Skip this section when `.copier-answers.yml` already records `nq-rdl/data-analysis-scaffold`:
   the project is rendered. A later answers change goes to the engineer as `copier update`.
2. Pin the release: list tags with `git ls-remote --tags
   https://github.com/nq-rdl/data-analysis-scaffold.git` and propose the newest `v*` tag,
   v0.5.1 or later: the first release whose rendered validator checks the sidecar. Never
   render from a branch.
3. Show the analyst the command, the tag and the engineer-owned values it will use, and ask
   for approval. The approval covers committing `answers.yaml` and the sidecar on a branch
   first, so the render is a separate, reviewable diff:

   ```bash
   copier copy --trust --overwrite --defaults --vcs-ref <tag> --data-file answers.yaml \
     gh:nq-rdl/data-analysis-scaffold .
   ```

   `copier copy`, not `recopy` or `update`: the seed's `.copier-answers.yml` names the
   retired `rdl-service-desk/data-science-template`, which copier 9.15 cannot render.
   `--trust` runs the template's post-generation task.
4. Check the result with `git status` and `git diff`: `answers.yaml` and
   `answers.intake.json` unchanged; `.copier-answers.yml` names the scaffold and the tag; the
   seed's release workflows under `.github/` unchanged. Then run the rendered validator
   (`python scripts/validate_answers.py answers.yaml`). If the rendered `scripts/` has no
   `analyst_intake.py`, report that the sidecar was not validated.
5. Commit the render only when the analyst asks. `pixi run setup` (DVC remote and
   credentials) is the analyst's or engineer's, on the VM; do not run it.

## A cohort supplied by the requester

When the requester supplies the cohort (a file of participants), record a `cohort` decision
that describes it by shape only: who supplies it, its columns, an approximate row count and
any instalments. Never ask for, open, read, copy or print the file: it holds identifiers.
After the render, give the analyst these steps to run on the VM: `pixi run setup` if the DVC
remote is not set, place the file under `data/00_raw/`, `dvc add` it, `dvc push`, and commit
only the `.dvc` pointer. The engineer declares the cohort with query-builder's supplied-cohort
support and joins to it; name the file and its `.dvc` pointer in the hand-off.

## Write and validate

Write `answers.intake.json` as one complete document (`schemaVersion: 1`, `approval_number`,
`decisions`, `open_questions`; `open_questions` may be empty). Run the validation above. On
failure, fix the named fields and run it again; do not hand over an invalid sidecar.

## Re-run: walk what changed

When `answers.intake.json` exists (or `--update`):

1. Run the validation and read the sidecar. Read `git log -p -- answers.intake.json
   answers.yaml` when tracked, and the current enquiry, to find what moved since the last pass.
2. Keep an unchanged decision verbatim: its `confirmed_by`, `confirmed_at` and `decided`
   stay as recorded. Do not re-stamp it.
3. Walk only decisions that the new evidence touches (confirm / reword / remove) and new
   topics. A reworded decision gets the analyst's new confirmation. A knock-on edit to
   another decision (a finer output's wording that the new answer contradicts) is a
   proposal too: put it to the analyst. Until they answer, keep that decision verbatim and
   name the conflict in the hand-off; never re-stamp it with this run's time. Keep its `id` when the
   decision is the same one in new words; use a new `id` for a different decision.
4. Move an open question into `decisions` only with the analyst's answer. Remove a question
   only when it is answered or the analyst withdraws it — say which.
5. If `.sqlreview/reviews/*/scope.json` holds `A-intake-<id>` items, the engineer has already
   imported the intake. Name each changed or removed `id` in the hand-off: bootstrap routes
   them as changed analyst decisions on its next run.

## Hand over

Show the analyst a short note for the engineer:

- the branch, the two file paths, the scaffold tag rendered (or why not), and the validation
  result (which validator ran, and whether it covered the sidecar);
- for a supplied cohort, the file's `.dvc` pointer path, or that it is still to come;
- the decisions by topic, the grain (`one row per <unit>`) and finer outputs;
- the open questions that wait on the requester;
- any technical notes the analyst volunteered;
- next: the engineer runs `/data-request:setup` (if `.sqlreview/` is absent), then
  `/data-request:bootstrap <intended sql path>`, which imports these decisions with the
  analyst's confirmation and asks the engineer only about what the sidecar leaves open.

Commit or push only when the analyst asks.
