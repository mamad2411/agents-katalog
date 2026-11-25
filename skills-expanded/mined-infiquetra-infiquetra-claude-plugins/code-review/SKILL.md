---
name: code-review
description: Run the pre-merge code review as a policy-free executor of the lifecycle repository's lens roster. Reads the lens declaration from the run record, resolves review_roster.v1 with the sdlc's own generator, runs one Lens Reviewer per selected lens, computes the verdict in code from the catalogue's strictness ladder, writes review_result.v2 into the run record, and publishes findings as exactly one pull-request comment — never an approving review. Triggers on "review this PR", "code review", "check my diff", or a /work hand-in before shipping.
---

# Code Review

`/code-review` answers **"Is this code safe to merge?"** It runs at the work-to-pull-request
boundary: after the build loop produces code, before a merge happens.

**It owns execution and nothing else.** What a lens means, what dimensions it has, what its anchors
say, what strictness applies, what threshold must be met, which lenses exist, which are always on,
and what shape acceptance takes are all **catalogue and profile content**, owned by
`infiquetra/infiquetra-sdlc` — the lifecycle repository. This skill consumes them. That boundary is
architecture decision record ADR-001, and it is the whole design.

Until 2026-09-19 this skill shipped its own fourteen-lens policy file and scored against it. A
plugin upgrade could therefore change the acceptance bar for every repository with no decision
anywhere that said so. That file is gone.

## Position in the lifecycle

- `/plan` answers: "How should it be built?"
- `/doc-review` answers: "Is this plan ready to execute?"
- the build loop answers: "Build it."
- **`/code-review` answers: "Is the built code safe to merge?"** — this engine
- `/qa` answers: "Does the shipped thing actually work?"

Passing code review completes the review stage. It does not complete testing, and it does not
complete delivery.

## Core principles

1. **Policy-free executor.** This skill consumes the generated roster, the resolved quality profile,
   the run's lens selection, the executor assignments, the recovery rules, and the frozen revision.
   It authors none of them. If you find yourself deciding what a lens should require, stop — that
   decision belongs in the lifecycle repository's catalogue, not here.

2. **Lenses come from the declaration, fixed at admission.** The lens set is
   `run_configuration.applicable_lenses` in the run record, answered once when the run was admitted.
   There is no per-commit conditional-lens prompt, because re-asking a settled question is how a lens
   silently carried from one commit to the next.

3. **The verdict is computed, never judged.** Four typed outcomes and nothing else: `accepted`,
   `repairs_requested`, `cycle_cap_best_available`, `review_incomplete`. The mapping is a total
   function of three facts about the cycle — no averaging across lenses, no reviewer preference, no
   head count.

4. **Verify, don't guess.** Every finding cites `file:line` evidence on the reviewed revision. A
   finding with no citation is an evidence gap, not a finding. Claims of "safe", "handled elsewhere",
   or "tested" must cite the proving line — or be reported as unverified.

5. **A comment, never an approval.** Findings are published as exactly one pull-request comment
   naming the reviewed revision in full. No `gh pr review` in any of its forms, ever. An approving
   review attaches an outcome that a later commit inherits without being read.

6. **A lens that cannot run is not a low score.** Execution failure is an execution problem, retried
   under the run's recovery rules. A missing result can never establish consensus, and acceptance is
   never invented from absence.

## Interaction method

<!-- gate-record: id=code-review-interaction absence=HALT transport=ask-user-question -->
**Operator-absence contract.** Every choice this skill puts to the operator from a known set goes
through `AskUserQuestion`, one question per turn, and the declaration above this line is the
contract. `HALT` here: stop and wait. A timeout, a widget error, or a dropped session is **never
consent** — do not proceed on a default and do not invent an answer. Read the decision from the
operator's actual answer, never from a widget's raw return value.

In a channel session `AskUserQuestion` cannot be called; inline the choices in the reply text
instead, following the convention in `saga/skills/brainstorm/SKILL.md`.

The rewrite of 2026-09-19 left this skill **one** such gate, down from three. The conditional-lens
approval gate is gone, because the lens set is settled at admission; the publication consent
machinery collapsed to a single confirmation. What remains is the required-lens gate in Phase 2.

## Reviewer-session transport

Orchestrate owns every reviewer session. **Do not launch or collect a reviewer through any saga
transport script**, and do not consult `engine-registry.yaml` as a launch authority — it is
capability metadata only and cannot override the live roster. If a requested reviewer is not in the run record,
halt rather than inventing a custom review or dispatching an unowned session as a substitute.

In a standalone `/code-review` with no orchestrated run, **the operator is the transport**: ask them
to add reviewer seats, or proceed without one and record that you did.

That prohibition is stated here without naming any script, deliberately. An earlier form listed the
scripts by name, and the names went stale when the scripts were deleted — a clause that names a
deleted file reads as satisfied whatever the code does. The rule is about the *authority*, not about
a particular file.

---

## Phase 0 — Read the run

### 0.1 Find the run record

One JSON file per issue holds the run's whole state, outside any worktree:

```bash
uv run python plugins/saga/scripts/run_record.py show --issue <N>
```

If there is no record, admission has not run for this issue. Stop and say so — the lens declaration
and the repair allowances live there, and this skill invents neither.

### 0.2 Freeze the revision

```bash
git fetch origin <base> --quiet
REVIEWED_SHA=$(git rev-parse HEAD)
DIFF_BASE=$(git merge-base origin/<base> HEAD)
git diff "$DIFF_BASE"
```

`REVIEWED_SHA` is a **full forty-character commit identifier**. An abbreviation or a symbolic
reference such as `HEAD` stops meaning anything once the branch moves, and both are refused
downstream.

Untracked files are not in `git diff` output. Note them as excluded from review rather than
reviewing them as though they were part of the change.

## Phase 1 — Resolve the roster

The roster is the run's reproducibility boundary: one content-addressed document naming every lens
the review will run, each one's threshold, its dimensions, and who may score it. It is produced by
the lifecycle repository's own generator, invoked as a subprocess:

```bash
uv run python plugins/saga/scripts/review_roster.py --issue <N> --revision "$REVIEWED_SHA" \
  --resolved-at "$(git show -s --format=%cI HEAD)"
```

The script builds an `applicability_declaration.v1` from the run record's lens declaration, hands it
to `tools/docs/gen_review_roster.py` in the lifecycle checkout, and prints what that generator
returned — unchanged. It never reimplements the resolution and no copy of the generator is vendored
here.

**Exit codes.** `0` the validation report is `ok`. `1` the report is `refused` — a run-setup fact,
not a crash. `2` a refusal this script owns: no lifecycle checkout, no generator in it, or a run
record with no lens declaration.

**The checkout is found** through an explicit path, then `INFIQUETRA_SDLC_PATH`, then
`INFIQUETRA_SDLC_ROOT`, then `~/workspace/infiquetra/infiquetra-sdlc`. The resolution always says
which one it used. When none resolves, the review **refuses by name** and writes `review_incomplete`.
There is no fallback roster: a fallback policy is still a policy.

**The conditional-lens proposal is advisory.** Before resolving, the Planner may ask whether any
excluded conditional lens applies after all:

```bash
uv run python plugins/saga/scripts/review_roster.py --declaration decl.json --propose
```

prints the proposed additions with their probabilities and leaves the declaration's lenses intact.
The proposal can only add lenses, never remove them, and it never questions the four always-on
lenses. The Planner applies additions explicitly, amending the declaration before the roster
resolves. A missing key or a failed call degrades to an empty proposal with a note — never a
refusal, and never a reason to delay the review.

**A refused report is expected today.** The lifecycle repository's executor-verification ledger,
`config/executor-verifications.json`, is empty on purpose. No executor has been qualified against
any lens's fixtures, so the generator assigns no scoring executor and no lens establishes a
threshold. Record the report verbatim, run the lenses for findings, and emit `review_incomplete`.
That is the honest state — a score from an unqualified model is not weak evidence, it is not
evidence — and it changes the day the first qualification lands, with no change here.

## Phase 2 — Run one Lens Reviewer per selected lens

One logical executor owns each selected lens for the cycle. One lens, one reading, one score. There
is no voting inside a lens and no averaging between two readings of it.

**Choose the hosting once, for the whole review, and record it.** A roster session when the run
record's `roster` array already names panes for this issue or the caller asks for one; an isolated
subagent otherwise. Never per lens, never implicit. Stand up roster sessions through agent-launcher's
helper and nothing else:

```bash
R=$(ls -d ~/.claude/plugins/cache/*/agent-launcher/*/skills/agent-launcher/scripts/roster.py \
    | sort -V | tail -1)
python3 "$R" up --issue <N> --dry-run    # inspect the panes before creating any
```

**Every lens runs as a roster session in its own worktree.** A lens reviewer reads; it never
writes, and a reviewer sharing this session's filesystem could clobber the tree it is reviewing.
The roster helper gives each role its own worktree, so that isolation is a property of how the role
is hosted rather than a flag each dispatch has to remember. Where a lens must run as a subagent
instead of a pane, it runs read-only and in a disposable worktree for the same reason.

**Each dispatch carries exactly five things**: the issue, the one lens identifier, the frozen
revision, the roster hash, and the vendor, model, effort and prompt hash the roster names for that
lens. It carries no other lens's findings, no host's reading of the diff, and no prior cycle's
scores. The rubric itself is **not** copied into the brief: `plugins/agent-launcher/roles/lens-reviewer.md`
tells the session how to reach the lifecycle repository and read the catalogue for itself.

Six invariants travel with every logical executor, under any hosting shape:

| Invariant | The rule |
|---|---|
| No shared-context contamination | A lens executor is never a fork of its host. It starts from the frozen inputs only. |
| No hidden model inheritance | Every dispatch names vendor, model, effort and prompt version explicitly. An inherited configuration is an unverified one. |
| Failure isolation | Each lens result is written durably the moment it completes, never batched at cycle end. |
| Concurrency ceilings | Fan-out queues inside the run's recorded allocation. |
| Read-only and isolation | Every lens executor holds a read-only toolset over the reviewed source and its own worktree. |
| Attribution | The result records, per lens, the executor, the topology, and the verification entry it cited. |

**A lens the catalogue marks `scorable: false`** reports findings and establishes no threshold.
Eleven of the catalogue's fifteen lenses are in that state, because they carry no fixtures yet. A
reviewer staffing one reports what it found and says plainly that it did not score. That is a
complete result, not a failure.

### Recovery when a lens cannot execute

Two backoff retries on the same verified executor — the first after 30 seconds, the second after 120
— then **one** substitution to a pre-declared verified fallback meeting the lens's floor. None of the
three consumes a review cycle, because an execution failure is not a review result.

<!-- gate-record: id=code-review-required-lens-unexecutable absence=HALT transport=ask-user-question -->
**When the recovery budget is spent**, the lens stays could-not-execute and the cycle stays open. The
Architect decides one thing only: whether the lens is applicable to this work at all. If it is not,
the cycle proceeds without it. If it is required, the question stops being technical and goes to the
**operator** through `AskUserQuestion`, whose choice is between providing another verified executor
and waiting for the current one. **On silence: HALT.** A timeout, a widget error or a dropped session
is never consent. Dropping or weakening a required lens is forbidden to every role — there is no path
through this skill that scores a required lens with something that does not meet its floor.

In a channel session `AskUserQuestion` cannot be called; inline the choices in the reply text
instead, following the convention in `saga/skills/brainstorm/SKILL.md`.

## Where the lens work runs

**One backend: `inline`.** Issue #1030 archived the `team-execution` plugin and removed the
`cc-workflows` plugin, so there is no alternative transport to weigh, nothing to pre-select against,
and no operator question to ask here. §1 of
[`../../references/operator-choice.md`](../../references/operator-choice.md) is the contract.

The property that outlived the three-backend era is the one worth stating: the transport never owns
policy. Wherever a lens seat runs — this thread, or a roster session in its own worktree — it returns
evidence to **this** controller, which resolves the roster, computes the verdict and emits the
result. No seat recomputes a score, and none owns a second acceptance rule. The Code Review outcome
blocks a merge when the caller applies it, whoever ran the lens.

**Search before recommending a fix pattern.** Before citing one (concurrency, caching, authentication,
framework behaviour), verify it is current practice for the version in use. If a web search is
unavailable, say so and proceed on in-distribution knowledge rather than presenting it as verified.

## Phase 3 — Compute the verdict

Not a judgment call. The verdict is a total function of three facts about the cycle, read in this
order:

| When this is true of the cycle | The outcome |
|---|---|
| At least one selected lens has no usable result and recovery could not restore it | `review_incomplete` |
| Every selected lens has a result and every one of them is met | `accepted` |
| At least one lens is not met and the cycle allowance is not exhausted | `repairs_requested` |
| At least one lens is not met and the allowance is exhausted | `cycle_cap_best_available` |

**Read the first row first.** A lens that did not run tells you nothing about the code, so an
unusable result is decided before any low score.

**"Met" is a pair, never one number.** The lens's derived overall must reach the level's minimum
*and* every applicable dimension must reach the level's floor. At `standard` — the level the default
profile sets for every lens — that pair is **9.0 and 7**. The dimension floor is what stops a lens
passing on a good average with one unacceptable part: an architecture lens averaging 9.2 with a 5 on
dependency direction has not met `standard`.

The derived overall is the weighted mean of applicable dimension scores, on the integer 0-to-10
scale, rounded to one decimal place, half away from zero.

**A finding never gates on its own.** A P1 finding shows up as a dimension score below the floor, and
it is the score that decides. Residual findings that leave every dimension at or above its floor are
recorded and carried across cycles; they do not by themselves fail the lens.

```bash
uv run python plugins/saga/scripts/review_consensus.py --result <result.json>
```

prints exactly one of the four words and nothing else.

## Phase 4 — Write `review_result.v2`

One entry per cycle in the run record's `review_cycles`, carrying every provenance field the
catalogue requires: the roster hash, the catalogue version and hash, the profile path, version and
hash, the lens and its strictness, the reviewed revision, the cycle number, the executor's vendor,
model, effort and prompt hash, the verification reference, the hosting topology, the checks executed
with their resolved versions, and the per-dimension scores with their applicability.

**Finding identity** is the catalogue's fingerprint of path, line and category, stable across cycles.
Two lenses reporting the same defect produce **one** finding with the agreement recorded; the second
is `duplicate-of` the first — visible, and counted once. Similar wording is not evidence of the same
defect.

**Two advisory overlays travel beside the findings, and both are shown, never applied.**
`dedupe_findings` groups findings that describe the same defect: code finds the candidate pairs
(same path and category), one yes/no judgment per pair confirms or declines, and confirmed pairs
are grouped with both findings kept — never merged, never dropped, and the fingerprint merge still
owns counting. `flag_severity` scores each finding against the catalogue's severity anchors and
attaches a flag only when the suggestion is strictly more severe than the stated severity, beside
it on `severity_flag` — the reviewer's severity always stands. Both log their suggestion and their
outcome to the verdict log; both fail open to ungrouped and unflagged. Present both beside the
findings they annotate.

**One review history per unit.** A request to start a fresh history for a unit that already has one
is refused, because a fresh history resets the cycle counter and puts incomparable scores side by
side. Scores are compared only within the declared lens set.

**One counter per loop.** The pre-merge code-review loop and the post-merge repair loop each keep
their own allowance and their own count. Every entry carries a `loop` field valued `code_review` or
`post_merge`.

**An older `review_result.v1` entry** already in a record is reported by name, preserved unchanged,
and counted toward no allowance: its cycle accounting used a different acceptance rule and is not
comparable.

## Phase 5 — Present, publish, and route

### 5.1 Present the findings

Render the operator status header through the shared `status_card.py` renderer's
`project_code_review` projection, using the typed outcome and independent-gate state as inputs.
Include the scope-check result, the finding counts, the current cycle, and the outcome. The card is
**presentation only**: it derives no decision from priority or confidence.

Below the card, lead with the findings, P0 first, grouped by severity, as a pipe-delimited table per
severity (`# | File | Issue | Reviewer | Confidence | Route`). Include the built-versus-planned
summary, the scope-check result, the suppressed count, and coverage — residual risks and testing
gaps. `references/findings-schema.md` carries the full output contract.

### 5.2 One comment

Exactly one pull-request comment, naming the reviewed revision as a full forty-character commit
identifier. **No pull-request review, in any of its forms.** Publication commits nothing, pushes
nothing, and does not advance `HEAD`, so a caller's freshness check stays valid. The evidence lands
in the run record — not in a review document, and not through the evidence ledger.

One confirmation before publishing, and no further consent machinery.

**In programmatic / report-only mode — the mode the build loop calls this skill in — publication does
not happen at all.** That mode makes **ZERO durable writes**: ZERO file writes to reviewed code, no
commit, no push, no comment, and no review submission. It returns the serialised `review_result.v2`
and the caller owns persistence and routing. The staleness gate in the build loop depends on exactly
this split: it counts commits since its captured reviewed revision, and that count stays at zero
because the in-loop call writes nothing.

### 5.3 Repair, and the cycle cap

The allowance is **three standard cycles, then two escalated**. A cycle is one completed review
result followed by one repair batch; an execution retry or a substitution consumes none. Escalation
fires when the standard allowance is exhausted without every lens meeting its acceptance, or when
two consecutive standard cycles pass with no progress on the same below-threshold lens.

An unsuccessful review routes to **repair planning**, never to an implementer directly: the Planner
writes a durable amendment from the authoritative plan, the reviewed revision, the full finding
history, and any dispute. Reviewers stay read-only throughout — they classify and route findings;
they never implement, commit, or repair code.

**At the cap there is no further cycle.** The open findings are prepared as linked defect issues,
mission-control files them, their numbers are listed in the result, and the run proceeds with
`cycle_cap_best_available`. Merging is not production promotion, so remaining quality problems can
still be investigated in testing with the findings preserved.

The narrow exception has **two categories and the catalogue is closed at them**. A merge stays
blocked only by *reproduced* evidence of data loss or destructive behaviour, or of a security
exposure — an authorisation bypass, a tenant-isolation breach, or disclosure of protected data or a
secret. *Reproduced* is the whole standard: speculation, an unsupported priority label, and a
below-threshold score on its own do not qualify.

### 5.4 Continue on the verdict

**Each verdict performs its own next step in the same turn** (issue #1029); none of them is a
recommendation the caller is left to act on. `/code-review` is almost always entered from `/work`
§5.1, so "continue" usually means returning the verdict to that caller and letting it proceed —
say which of the two you did.

- **`accepted`** — continue into the next lifecycle step: return to `/work`'s gate when it called
  you, and otherwise run the step the run record's `next_step` names.
- **`repairs_requested`** — **run repair planning now** on the findings you just wrote. Do not stop
  at naming it.
- **`cycle_cap_best_available`** — continue with the best-available revision and surface every
  residual in the same message. The cap is a stated limit, not a pass.
- **`review_incomplete`** — **stop and report** that delivery did not establish a review. Never
  invent a score and never continue past a review that did not happen.

Continuation changes which step runs next, never what is confirmed: nothing here opens, updates,
approves, or merges a pull request, and the boundary below is unchanged.

### 5.5 Hard boundary

`/code-review` reviews, classifies, and routes. It does **NOT** implement the fixes it requests —
they go to repair planning. It does **NOT** mutate reviewed source. It does **NOT** commit an
implementation change. It does **NOT** open or update a PR. It does **NOT** file issues itself:
filing the residual defects is mission-control's ownership lane, and this skill only prepares them.
It publishes one comment and never a review approval.

---

## Reference files

- `../../scripts/review_roster.py` — builds the declaration from the run record and invokes the
  lifecycle repository's generator; named refusal when the checkout is absent. `--propose` prints
  the advisory conditional-lens proposal without resolving a roster.
- `../../scripts/review_consensus.py` — the scorer, the cycle state machine, and the verdict computed
  from the catalogue's strictness ladder.
- `../../scripts/review_result.py` — the `review_result.v2` writer, finding fingerprints, one history
  per unit, the residual preparation, and publication. `dedupe_findings` and `flag_severity` are its
  two advisory overlays: groups and flags, shown beside the findings, never applied.
- `../../../agent-launcher/roles/lens-reviewer.md` — the prompt each lens session receives.
- `references/lens-execution.md` — how to execute a resolved roster. The catalogue itself lives in the
  lifecycle repository; this plugin holds no copy of it.
- `references/findings-schema.md` — the shared finding schema, its severity and status vocabularies,
  and the fingerprint rule.
- `references/validator.md` — the independent per-finding validator.
- `references/built-vs-planned.md` — scope-drift detection and the plan-completion audit.
