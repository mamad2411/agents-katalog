---
name: qloop
description: "This skill should be used when the user asks to \"review and fix\", \"iterative review\", \"review loop\", \"qloop\", \"fix all issues\", or wants an artifact reviewed, all issues fixed at all priorities, and re-reviewed until convergence. Enforces: minimum 2 rounds, fix-ALL gate, clean-context re-review, deterministic tests at every step."
version: 0.4.0
---

# /qloop -- Iterative Review-Fix-Verify Loop

Convergence loop: review → fix ALL findings in place → clean-context re-review,
repeated until the artifact converges (zero P0, zero P1, low-severity within
threshold) or the loop hard-stops. `/qloop` is `/qreview` plus a fixer and the
enforcement gates.

> **Hard rule: NEVER hand-write a review/pipeline workflow script.** The ONLY
> sanctioned path for this skill is `scriptPath=review-loop.workflow.js`. If
> that script file is missing, STOP and report — do not improvise a workflow.
> A hand-rolled script has no `model:` tiering, so every agent it spawns
> silently inherits the invoking session's model (including expensive
> long-context variants) — this is the single largest source of runaway spend
> observed across past runs. There is no acceptable workaround; a missing
> script is a bug to report, not a gap to paper over.

**This skill runs via the ai-review-toolkit ultracode Workflow**
(`review-loop.workflow.js`, run until-converged). The Workflow — not prose — owns
the state machine: parallel reviewers with resolved models, JS synthesis/dedup,
the fix-ALL gate, the min-2-rounds floor, stuck detection, and max-rounds
escalation. A single in-place fixer per round edits the artifact so the next
round's reviewers see the changes. Invoking `/qloop` **is** the explicit opt-in
to run that Workflow.

## Protocol

Follow in order.

### 0. Version check (best-effort, non-blocking)

Run `python3 <tools>/version-check.py check` once at the start. It is rate-limited
(~once/day) and fails silent-and-open. If it prints an upgrade notice, relay that
single line to the user, then continue — never block, retry, or wait on it.

### 1. Identify artifact + requirements

Accept a file path or inline content for each. Write inline content to a temp
file. If no requirements exist, ask the user what the artifact must accomplish
and record that as the requirements file.

### 2. Resolve the review team (deterministic, Python)

Same as `/qreview` step 2 — run the team selector and capture the resolved team
(models already tiered). Tools are under `tools/` in the plugin, or
`~/.claude/ai-review-tools/` in the local fork.

```
python3 <tools>/team-selector.py "<short artifact description>" \
  --artifact <artifact_path> --json \
  --files <N> --context-window 200000 [--max 5] [--high-stakes]
```

Default team is 3 reviewers seated by domain relevance; complexity escalates
only the top-2 domain lenses (files `> 3` / context `> 40%`), security earns
Opus only on a scored security domain or `--high-stakes`, and Opus is
hard-capped at 2 seats. Parse the JSON `team` array. Pass it straight into the
Workflow — **do not re-tier or override models by hand.**

### 3. Run the convergence Workflow

Resolve the workflow script path (`js/` beside `tools/`):
- plugin: `<plugin>/js/review-loop.workflow.js`
- fork: `~/.claude/ai-review-tools/js/review-loop.workflow.js`

Invoke the **Workflow** tool with that `scriptPath` and:

```json
{
  "artifact": "<artifact_path>",
  "requirements": "<requirements_path>",
  "team": <team array from step 2>,
  "threshold": 0,
  "maxRounds": 5
}
```

The stopping rules below all have engine defaults; pass a knob only to widen or
tighten a specific bound, never to switch a rule off. `maxGateRounds` (default 2)
caps consecutive deterministic-gate-only rounds; `deltaCaps`
(`{maxChangedLines: 20, maxChangedFraction: 0.05}`) sizes a proportional round;
`divergence` (`{window: 3, warmup: 6}`) tunes the non-convergence halt;
`maxInvalidRounds` (default `maxRounds`) bounds rounds lost to a dead reviewer
panel.

Omit `rounds` (or set > 1) so the loop runs until-converged. The Workflow runs
unattended to convergence, streaming per-round progress via `log()` (watchable
with `/workflows`). It hard-stops — max-rounds or stuck detection — and returns
the unresolved findings rather than spinning. Capture the **Run ID** and the
`workflows/<runId>.json` path from the tool result.

**The fixer edits files in place.** There is no worktree isolation — that is
deliberate, so each round's fixes persist for the next round's reviewers. Only
run `/qloop` on an artifact whose current state you are willing to have modified
(commit or stash first if you want a clean rollback point).

### 4. Present the outcome

The Workflow returns
`{ outcome, rounds, final_findings, final_counts, history, ledger }`:
- `outcome.status === "converged"` — present the convergence summary and round
  count. `outcome.message` carries `reviewers <returned>/<requested> returned` and
  `outcome.reviewers` carries the same as data, so a reader who sees only the
  verdict knows the panel actually ran. A converged verdict is only reachable from
  rounds that met quorum, and only from a round a reviewer actually READ (the
  converging round has `reviewers_returned > 0`): a deterministic gate round asks
  for no reviewers, so it can never certify convergence. `budget.reviewedRounds`
  is how many rounds a reviewer panel read the artifact; a converged run always has
  at least one, and `reviewedRounds: 0` means nothing was reviewed.
- `outcome.status === "escalated"` — present `outcome.reason` and `outcome.unresolved`
  (P0/P1 findings), then ask the user to choose: continue (raise `maxRounds` and
  re-run), accept current state, or abandon. Escalation happens on max-rounds,
  stuck detection (identical P0/P1 across two rounds), a failed fix-ALL gate,
  DIVERGENCE, or too many invalid rounds.

  **A divergence escalation is not a "raise maxRounds" case.** `outcome.divergence`
  is present and the reason names SPLIT: the finding rate is not decaying, so the
  artifact is under-specified or too large for one loop. Re-running it with a
  bigger budget reproduces the 19-round, ~5M-token run this rule exists to stop.
  Split it, re-scope it, or hand it back. An ENVIRONMENT escalation (too many
  rounds without a valid reviewer panel) says nothing about the artifact at all:
  fix the environment and re-run.

The result also carries `budget` (`maxRounds`, `roundsRun`, `validRounds`,
`invalidRounds`, `fullRounds`, `deltaRounds`, `gateRounds`, `reviewedRounds`,
`wallClockMs`), and
each `history` entry carries its `kind` (`full`/`delta`/`gate`), `ms`,
`delta_reason`, `valid`, `reviewers_returned`/`reviewers_requested`/`reviewers_quorum`
and `reviewers_missing` (`[{name, reason}]` for every reviewer that did not report).
Present the budget line with the outcome; it is what makes an expensive run visible.
**Any round with `valid: false` must be named when you present the run**, with the
reasons from its `reviewers_missing`, because that round certified nothing.

Show `history` (findings-per-round) so the convergence trajectory is visible.
`ledger` (returned alongside it) lists the findings adjudicated across the whole
run — each with the round that settled it — and is what later rounds' reviewers
were told not to re-litigate.

### 5. Scorecard (mandatory)

Whenever the loop ends (converged OR escalated), run the deterministic scorecard
against the run and present it verbatim; it is the final OUTPUT to the user, but
step 6 below still runs after it:

```
python3 <tools>/scorecard.py --workflow <session>/workflows/<runId>.json
```

A **VERDICT** line first (status, rounds used against the budget and their kinds,
total tokens, USD, wall-clock, plus the escalation reason when there is one),
then four sections in order: **Process**, **Issues Found**, **Token Cost**
(per-model USD), **Model Execution Time** (per-agent wall-clock rolled per model
+ the workflow wall-clock total). Pass `--pricing PATH` to override USD rates.

### 6. Record QAC inputs (fail-open telemetry)

Persist the loop's findings so `fleet metrics --qac` prices the rework (companion
to fleet REQ-COST-153..157; spec: `qreview/requirements.md` REQ-QAC-202/203,
shared with `/qreview`). The fleet contract assigns the findings keys to the
session that PRODUCED the findings, so the orchestrating session writes to its
own key, with no `--session` (that flag exists for the build-supervisor's
ask-size case only):

```
fleet qac-inputs --p0p1 <N> --p2p3 <N> --review-rounds <R>
```

- Derive the numbers mechanically from the workflow result, never by judgment
  and never by summing per-round totals (a finding that persists across rounds
  would double-count, and an inflated write is sticky under the monotonic
  floor): `--p0p1` = sum of `history[].newP0P1` (newly surfaced relative to the
  previous round; a converged final round contributes 0, which is correct (note
  a P0/P1 that regresses and recurs can be counted twice, an acceptable slight
  over-count). `--p2p3` = max over `history` of (`significant` minus that round's
  `counts.P0 + counts.P1`): the per-round significant count with P0/P1 removed,
  a deterministic floor for distinct significant P2/P3 (it under-counts late
  arrivals rather than double-counting persisters; a later, larger corrected
  write still takes). `--review-rounds` = review rounds EXECUTED (the result's
  `rounds`). The fleet key's gloss is "rounds until no P0/P1"; an escalated run
  records the rounds it ran, and its unresolved P0/P1 are already in `--p0p1`,
  so the pair reads correctly together.
- The counts are per-SESSION cumulative, not per-run: the artifact key is this
  session, and the findings keys keep the MAX across writes (monotonic floor; a
  smaller later write does not take). If this session already recorded a review
  (`fleet qac-inputs` with no value flags is read mode; the stored values are the
  `qac_inputs` object, absent keys null), write the running total: stored value
  plus this run's counts. Write once per run, after the loop ends (converged OR
  escalated), never per round. EXCEPTION: a `continue` re-run of the SAME
  artifact in the SAME session (the escalation choice in step 4) is one logical
  review, not a second run: it re-surfaces every still-open P0/P1 as new, so do
  NOT add its counts. Write `max(stored, this run's counts)` for the findings
  keys and `stored + this run's rounds` for `--review-rounds`.
- `--reset` deletes the WHOLE artifact for the key, including any `ask_*` a
  supervisor wrote there and the `_writers` trail. It is for a typo'd count
  only: read first, then re-supply every key it held in the same command.
- Own key is right ONLY when this session is part of the build under review (a
  spawned `pr<N>-reviewer` child, or a builder reviewing its own work). Rows
  group by parent, so if this is a cockpit-class session reviewing another
  build's work, SKIP the write entirely; do not record at your own key (a
  supervisor gets these numbers onto the right build by spawning the reviewer
  child, per the build-supervisor charter).
- Fail open, exactly this shape: run the command; any non-zero exit or missing
  CLI is one printed line ("QAC inputs: skipped") and you move on. Never retry,
  never hunt for the CLI, never ask the user; recording telemetry never blocks
  or fails the loop. Surface the outcome in the loop's final output as one line
  ("QAC inputs: wrote p0p1=N p2p3=N rounds=R at <key>", or "QAC inputs: skipped")
  so a close-out reader can tell a write from a skip. There is no CI flag to
  pass; the CI-red signal is
  read-time-computed on the fleet side.

## Hard rules (enforced in `review-loop.workflow.js`, not prose)

- **Reviewer quorum: a round is evidence only if the panel reported.** Every
  requested reviewer is attested as returned, or missing WITH the reason it died
  (expired auth, killed session, timeout). A round below quorum (a majority of the
  panel, floor 2; a round whose panel is one verifier is still a whole panel) is
  recorded `valid: false` and INVALID: it spends no round budget, feeds no ledger
  adjudication, reaches no fixer or spot-fixer, and can never converge. The loop
  re-runs; a panel that keeps dying escalates on the ENVIRONMENT. Zero findings
  from reviewers that never ran is absence of evidence, not evidence of absence.
- **Minimum 2 rounds, counted in VALID rounds.** Round 1 finds; round 2 verifies
  fixes and catches regressions. The loop never reports `converged` before the
  floor, and a round lost to a dead panel does not count toward it.
- **A converged verdict requires a reviewed round: a gate-only run never
  converges.** The quorum gate catches a DEAD panel; a deterministic gate round
  asks for no panel at all, so it is `valid` with `reviewers 0/0` and used to
  satisfy the min-rounds floor and converge having read nothing (claude-skills#175:
  both rounds `kind: "gate"`, `converged (reviewers 0/0 returned)`). Convergence
  now requires the CONVERGING round to be one a reviewer read (`reviewers_returned
  > 0`, i.e. a full fan-out or a delta verifier). A run the gate starves of review
  escalates as COULD-NOT-REVIEW, naming the gate rather than the artifact. This is
  not a second floor: 1 gate round that finds + fixes a real defect, then 1 full
  clean round, still converges.
- **Fix-ALL gate on significant findings.** Every P0/P1 — plus any P2/P3 a
  reviewer flags `significance:true` or that recurs across rounds — needs a
  `FIXED`/`ESCALATED` resolution with evidence (`checkFixCompleteness`). No
  WONTFIX/DEFERRED/OUT_OF_SCOPE. A failed gate escalates.
- **Trivial P2/P3 are spot-fixed, not looped.** First-seen, unflagged cosmetic
  nits get a cheap Haiku spot-fix + spot-check each round — they're still
  addressed, but they don't block convergence or reset the loop. Convergence is
  reached when the *significant* set is clear (P0/P1 always count as significant,
  so they stay 0-to-ship).
- **Max rounds → escalated, never converged.** A terminal state that blocks
  downstream work until the user decides.
- **Stuck detection.** Identical P0/P1 findings across two consecutive rounds
  auto-escalate — two failed fix attempts on the same issue means the approach
  is wrong.
- **Deterministic checks run BEFORE agentic ones.** The test/lint gate runs first
  every round, and when it FAILS it claims that round on its own: the fixer gets
  the gate's mechanically-derived work list and no reviewer fans out. A defect a
  test, a linter or a schema check can name must never cost a reviewer round.
  Bounded by `maxGateRounds` (default 2 consecutive) so a permanently-red suite
  cannot starve review of the rest of the artifact. A gate round is never the
  round that certifies convergence (see the reviewed-round rule above).
- **Proportional rounds: a small, contract-safe fix batch buys ONE cheap
  verifier, not a full all-lens re-read.** After a full round's fix batch a haiku
  probe MEASURES the diff and the engine decides in JS. Delta-eligible only when
  all four hold: the batch fixed zero P0; it changed at most 20 lines AND at most
  5% of the artifact (both, not either); it touched no contract line (any
  `REQ-<CLASS>-<n>`, any line whose text starts `Acceptance`, any `sto:` line, and
  every line inside `### Requirement classes`, `### Cross-repo design`,
  `### Story points` or `### Review receipt`); and the bookends hold, round 1 is
  always full and a delta round never follows another delta round, so drift stays
  one small batch behind the last whole-artifact read. Any finding a delta round
  surfaces, at any severity, re-opens the full loop. Anything the probe cannot
  establish fails CLOSED to a full round.
- **Divergence halt: a loop that is not converging STOPS and says SPLIT.** Stuck
  detection only matches an IDENTICAL P0/P1 set, so a run surfacing genuinely NEW
  P0s every round slips straight past it: `pm-816-intake-0903` ran 19 rounds,
  ~3.5 hours and ~5M tokens on one issue and was still finding P0s at round 18
  until a human halted it. So: after 6 valid rounds, if each of the last 3
  surfaced at least one NEW P0/P1 and that count did not decay against the 3
  before them, the run escalates. It is not approaching a fixed point; a bigger
  budget will not change that.
- **The round budget is spent in VALID rounds only.** A round whose reviewer panel
  did not reach quorum is not evidence, so it consumes no budget and fills no
  divergence window. Running out of THOSE escalates on the environment, naming it,
  rather than blaming the artifact.
- **Cost travels with the verdict.** The scorecard's first line is
  `VERDICT: <status> - N of M rounds (x full, y delta, z gate) - tokens - $ -
  wall-clock`, and every round logs its budget position live in `/workflows`, so a
  19-round run is obvious WHILE it happens rather than afterwards.
- **Max-severity wins / clean context per reviewer per round / pre-existing
  issues are in-scope** — same as `/qreview`, enforced by the shared JS
  adjudication (drift-locked against the Python oracle in CI).
- **Adjudicated-findings ledger — clean context, not amnesia.** Reviewers stay
  clean-context every round (fresh eyes catch what a primed reviewer rationalizes
  away), but the engine carries a CUMULATIVE ledger of *settled* findings into
  every later round, so round 5 still knows what round 1 decided. A finding is
  admitted only when the fixer marked it `FIXED` **and** the next round's
  reviewers did not re-raise it — a claimed fix that did not hold (including one
  the trivial spot-check reports did not land) is never presented as settled. **Open and `ESCALATED` findings are deliberately
  excluded**: telling a fresh reviewer "the last round thinks X is broken" primes
  them to confirm X, which is the exact bias clean context exists to prevent. The
  ledger instructs reviewers not to re-litigate its entries, to verify each fix
  actually held, and to report any regression of one as a NEW finding.

## Tools

- **`js/review-loop.workflow.js`** — the ultracode Workflow (the loop engine).
  Generated from `js/adjudication.mjs` + `js/prompts.mjs`; do not hand-edit.
- **`tools/team-selector.py`** — deterministic team selection + model tiering.
- **`tools/scorecard.py`** — deterministic end-of-run scorecard.
