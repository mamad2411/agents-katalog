---
name: build-eval-suite
description: Build a regression eval suite for an LLM or agent feature — failure taxonomy from real traces, a frozen stratified dataset, deterministic checks before judged ones, binary rubrics, a judge calibrated against human labels before it may gate, k-run CI execution and results reported with uncertainty. Use before claiming a prompt, model or pipeline change is an improvement, when quality is argued anecdotally, before a first release of an AI feature, or when a judge score is about to be trusted as a gate. Produces evals/<suite>/ and a CI job.
allowed-tools: Read Grep Glob Bash Write Edit
argument-hint: "[suite-name] [--from-traces path]"
user-invocable: true
model: opus
effort: high
metadata:
  foundry.vertical: ai
  foundry.io: "requirement.v1 -> plan.v1 + evals/<suite>/"
license: Apache-2.0
---

# Build an eval suite

One feature at a time. The deliverable is a suite that can fail a release, that a sceptic can
rerun, and that reports "no measurable difference" when there is none.

The order is fixed: **traces → taxonomy → dataset → deterministic checks → rubrics → judge
calibration → CI gate → reporting**. Every step skipped downstream of a missing upstream step
produces a number that looks like evidence and is not.

## When not to use this

- **The property is deterministically checkable.** Schema validity, tool arguments, arithmetic,
  presence of a required field — write ordinary tests. An eval suite is what you build for what
  is left over, and pulling deterministic checks into a judged suite is how teams end up paying a
  model to verify JSON.
- **You are measuring retrieval, not answers** → `build-rag-pipeline` step 2. Retrieval metrics
  need no judge and belong in a separate suite with different maintenance.
- **You need a latency or throughput gate** → `foundry-quality:perf-budget`.
- **Nobody will act on a red result.** A gate that will be overridden every time is theatre.
  Establish the consequence first, name the decision-maker, and write the suite second.

## Step 1 — read real failures

Pull 30–50 real interactions: production traces, thumbs-down events, support escalations, or the
last month of complaints. Read them. Do not summarise them with a model before reading them —
the summary drops exactly the specific detail the taxonomy needs.

Label each failure into a class, and count. The output of this step is a table:

```
fabricated-fact          11
wrong-format              7
answered-unanswerable     6
refused-answerable        4
wrong-tool-arguments      3
correct-but-unusable      3
```

Those counts decide where your effort goes, and they are the only defensible answer to "why does
the suite measure this and not that". Without them you are testing your imagination.

## Step 2 — dataset

- **Stratify by the taxonomy** and by real usage share. Record per-stratum counts in the header
  file; a stratum with fewer than ~20 items supports no independent conclusion, and you must say
  so rather than quietly reporting one.
- **Include a held-out slice** (roughly a fifth) that you never look at while iterating. What you
  inspect repeatedly, you overfit — the mechanism is identical to train/test leakage.
- **Freeze and version**: `evals/<suite>/dataset.v1.jsonl`, one object per line, with `id`,
  `input`, `reference` (where one exists), `stratum`, `provenance` (`trace` | `expert` |
  `synthetic`), `addedAt`. Corrections create `v2`; never edit a released file, or every
  historical metric becomes uninterpretable.
- **Flag synthetic items** and exclude them from model-vs-model comparisons: they inherit the
  generating model's blind spots and correlate with the system under test.
- **Guard against contamination**: keep publicly-published items in their own stratum and do not
  use them to compare models — they may sit in a training set.
- **Store the reference as the source span** for grounded tasks, not just the expected answer.
  That is what makes attribution checkable.

Every past incident becomes a permanent item. That single rule is what makes the suite track
your real risk instead of drifting.

## Step 3 — deterministic checks first

Implement these before anything involving a model. They are exact, free, fast, and they catch
most real production defects:

- JSON parses; validates against the schema; enums are members; numbers in range.
- Required fields present; no extra fields; ids referenced exist in the input.
- Citations reference chunks that were actually retrieved.
- Tool name valid; arguments schema-valid; no forbidden tool for the context.
- Language of the answer matches the language of the question.
- Length within bounds; forbidden strings absent (internal hostnames, secret patterns,
  competitor names — whatever your policy says).
- Abstention emitted for the unanswerable stratum.

Report this tier separately and gate it hard: a schema violation is a bug, not a quality score.

## Step 4 — rubrics for what is left

One criterion per judgement, binary or three-point, checkable from the artefact alone. Never a
1–10 scale: fine-grained scales have no stable meaning across items or over time, and graders
cluster in the middle.

Bad: "Rate the answer's quality 1–10."
Good: "Does every factual claim in the answer appear in `<sources>`? yes / no."

Each criterion carries a passing example, a failing example and a borderline rule, all drawn
from the real dataset. Templates and worked criteria: `references/rubric-templates.md`.

## Step 5 — calibrate the judge before it may gate

A judge that has not been compared against humans is a second opinion, not an instrument.

1. Two humans independently label **≥ 100 items** with the same rubric.
2. Measure **inter-human agreement first**. If humans disagree, the rubric is broken — fix the
   rubric, not the judge.
3. Measure judge-vs-human **Cohen's kappa**, not raw agreement: with 95% passes, a judge that
   says "pass" always scores 95% raw agreement and kappa ≈ 0.
4. Thresholds: **kappa ≥ 0.8** to block a release; 0.6–0.8 is directional monitoring and must be
   labelled as such in every report; below 0.6 the judge may not be quoted as a measurement.
5. Record judge model id, judge prompt hash, calibration set version, kappa and date in the suite
   header. Re-validate on any change to any of them, and at least every 90 days.

Bias controls that are mandatory, not optional — position swapping, length correlation checks,
judge-family separation, canary items: `references/judge-bias-controls.md`.

## Step 6 — run it k times

LLM outputs are not deterministic, and temperature 0 does not make them so across runs,
providers or hardware. Therefore:

- Run each item **k ≥ 3** times in a gating suite.
- Gate on the **rate**, not on a single pass. "Passes 2 of 3" is a 67% behaviour; reporting it as
  green is the most common eval lie in production systems.
- Record per-item, per-run outcomes to `evals/runs/<date>-<config-hash>.json`. Aggregates cannot
  be re-analysed later; per-item results can.
- Items whose pass rate sits between the thresholds move to a `quarantined` stratum with an owner
  and a date, reported separately (mechanics: `foundry-quality:quarantine-flaky`).

## Step 7 — wire CI with a budget

| Tier | Trigger | Content | Budget |
|---|---|---|---|
| Fast | every PR touching prompts, tools, retrieval or model config | deterministic checks + stratified sample | state the wall-clock and spend cap |
| Full | nightly and every release candidate | all strata, k runs, judged criteria | state the wall-clock and spend cap |
| Red team | before release and after any tool/permission change | adversarial and safety subset | human review of every failure |

Failing conditions must be explicit: a deterministic-tier failure blocks; a judged-tier
regression beyond the stated tolerance blocks; a per-stratum regression blocks even when the
aggregate improved; a canary flip voids the run.

## Step 8 — report honestly

- **Paired comparison on the same items**, never two independent averages. Pairing removes item
  difficulty from the variance and detects far smaller real effects.
- **Interval, not a point.** Bootstrap over items is the simplest defensible method and assumes
  no distribution. For paired binary outcomes use McNemar's test on the discordant pairs.
- **State the minimum detectable effect before running.** If the set cannot resolve the
  difference the decision needs, grow the set or change the decision — do not squint at it.
- **Per stratum, always.** An aggregate gain hiding an abstention regression is a shipped
  incident.
- **Cost and latency next to quality.** A quality gain bought with a large spend increase is a
  human's trade-off to make.
- The honest headline is often "no measurable difference at this sample size". Publish it.

Method, with worked numbers: `references/sampling-and-significance.md`.

## Step 9 — write it down

`evals/<suite>/README.md`: what the suite measures and what it deliberately does not; the
taxonomy with counts and dates; dataset versions and strata; the check tiers; every rubric
criterion; the judge configuration and its calibration record; the k and the gate thresholds;
the CI wiring and budgets; the owner; the review date (≤ 90 days).

Emit `plan.v1` to `.foundry/blackboard/<wave>/build-eval-suite.json` with waves for traces,
dataset, deterministic tier, rubrics, calibration and gating, and `outOfScope` naming every
property deliberately unmeasured.

## Exit criteria

1. Taxonomy built from ≥ 30 real traces, with counts, and read by a human.
2. Frozen versioned dataset with strata, provenance flags and a held-out slice.
3. Deterministic tier implemented and gating independently.
4. Every rubric criterion binary or three-point, single-property, with anchored examples.
5. Any gating judge calibrated: kappa ≥ 0.8 on ≥ 100 double-labelled items, recorded with model
   id, prompt hash and date.
6. Canary items seeded in every judged run; a canary flip voids the run.
7. Gating suite runs k ≥ 3 per item and gates on rate with a stated threshold.
8. CI tiers wired with explicit wall-clock and spend budgets.
9. Results reported per stratum, paired, with an interval, alongside cost and latency.
10. Every known incident represented as a permanent dataset item.
11. Owner named, review date ≤ 90 days, `plan.v1` validates with a non-empty `outOfScope`.

## Degradation

- **No production traces** (pre-launch) → taxonomy from the requirement plus hand-written
  adversarial cases; label the suite `pre-launch`; schedule replacement with real traces in the
  first weeks of traffic and say the coverage is unrepresentative.
- **One labeller only** → have them re-label a shuffled subset later and report intra-rater
  agreement. Do not present it as inter-rater kappa.
- **No budget for a judge** → ship the deterministic and reference tiers, which are free, and
  record the unjudged properties as a `risk.v1` with an owner.
- **Judge version cannot be pinned by the provider** → the suite is monitoring, not a gate; say
  so in every report instead of pretending the number is stable.
- **Provider rate limits make k ≥ 3 impossible** → reduce the item count rather than k. A smaller
  set measured properly beats a larger set measured once.
- **`superpowers` installed** → `superpowers:test-driven-development` when converting a reported
  failure into an eval item (write the failing item first), and
  `superpowers:verification-before-completion` before any claim of improvement leaves the team.

## Deliberately not covered

Retrieval metrics (`build-rag-pipeline`), prompt repair (`prompt-engineer`), agent topology and
budgets (`design-agent-tools`, `agent-architect`), ordinary test architecture
(`foundry-quality:test-strategist`), inference spend modelling
(`foundry-economics:ai-cost-controller`), and regulatory conformity documentation
(`foundry-legal:ai-governance-analyst`) — this suite produces evidence that agent consumes, and
is not itself a conformity assessment.

## Bundled references

- `references/rubric-templates.md` — ready criteria for groundedness, instruction adherence,
  abstention, tone and safety, each with anchors and the borderline rule.
- `references/judge-bias-controls.md` — position, verbosity and self-preference bias, drift,
  canaries, and the exact protocol for each control.
- `references/sampling-and-significance.md` — paired comparison, bootstrap intervals, McNemar,
  minimum detectable effect, and the four ways eval numbers are routinely oversold.
