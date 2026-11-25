---
name: strengthen-your-evals
description: >
  Turn the tests an agent already has into an eval that can fail, measure it
  the way a paper would, and report it so the platform can tell a fix from a
  fluctuation. Use when a coding agent is asked to build or improve evals for
  an agent that runs on a frontier model (Claude, GPT, Gemini) or on its own
  weights: find what the suite never reaches, build a frozen held-out set,
  check the judge against people, read pass@1 with an interval and the
  failure-capable count, measure the noise floor, size the set, and post
  every behavior to while.ai/platform/runs. No GPU, no key until you want
  the hosted writer.
metadata:
  version: "3.2.0"
---

# Strengthen your evals

Every step below is in `check.py`, which runs offline in seconds. Its setup
defines the names the blocks use: `TOOLS`, `POLICY`, `OLD_TESTS` (the
three-ask suite the team has), `SEEDS` (one ask per policy branch),
`refund_judge` (the policy as a program), `VERSIONS` (`v1` the agent as
shipped, `v2` after a prompt fix; you have one entry today), `LABELS` (hand
labels for sixty replies), `MODEL`, and `fake` (a recording transport).
Your agent is any callable `message -> {"steps": [...], "final_text": ...}`
that runs its own tools; `wai init-evals` writes that wrapper.

## 1. Find what the suite never reaches

Ask what the old tests miss before writing new ones: which policy rule,
which tool, what stance, and whether any ask runs more than once.

```python
gap = wai.coverage_gap(OLD_TESTS, tools=TOOLS, system_prompt=POLICY)
print(wai.format_coverage_gap(gap))
```

A suite that passes on a good day only is the usual finding: every ask
ordinary, every ask run once, one rule no ask reaches.

## 2. Build the frozen test

The held-out set is one artifact, named, and the same for every version.
`seeds=` keeps your asks on the policy branches; the writer varies the
wording and the stance and adds asks of its own, and it reads the record
ids off your tool descriptions ("Orders on file: A1001, ..."). Write the
asks once, then replay that run with `tasks=` for every other version: the
writer steers toward what the agent it watches gets wrong, so two versions
run from the same seed do not face the same asks.

```python
K, N = 4, 64  # rollouts per ask, asks


def holdout(agent, tasks=None, seed=0):
    """Write the N asks once (tasks=None), then replay that run's asks for every
    version: the writer adapts to the agent it watches, so the same seed does
    not mean the same asks."""
    where = {"tasks": tasks} if tasks is not None else {"seeds": SEEDS, "situations": N}
    return wai.simulate(
        agent,
        tools=TOOLS,
        system_prompt=POLICY,
        budget=N * K,
        simulator=False,  # offline writer, no key; drop it for the hosted writer
        mode="rl",
        repeats=K,
        repeat_policy="fixed",
        reproducible=True,
        seed=seed,
        fault_rate=0.0,
        avg_turns=1,
        **where,
    )


frozen = holdout(VERSIONS["v1"])
data = {"v1": frozen}
for v, agent in VERSIONS.items():
    if v != "v1":
        data[v] = holdout(agent, tasks=frozen)
asks = sorted({r["prompt"] for r in frozen.rows()})
for d in data.values():
    assert sorted({r["prompt"] for r in d.rows()}) == asks, "every version must face the same asks"
TEST_VERSION = "t-" + hashlib.sha256("\n".join(asks).encode()).hexdigest()[:8]
print(f"held-out test {TEST_VERSION}: {len(asks)} asks x {K} rollouts")
```

**Name the set by its content.** `TEST_VERSION` changes when the asks
change, so two scores are comparable only when they carry the same name
("Evaluation": a result is comparable with its setup held constant). Steer
with `hard_share=` or `dimensions={"stance": [...]}` before you freeze, and
never by hand-picking the asks the agent failed: a prompt chosen for a bad
draw scores better on the re-draw with no change at all.

## 3. Check the judge against people

The judge reads the trajectory, not the prose: which tools ran, with what.
A model judge is only as good as its agreement with people on a labeled
slice, and a program judge is held to the same bar. Label sixty replies by
hand, attach them as human labels, and measure.

```python
scored = {v: wai.evaluate(d.rows(), refund_judge, tools=TOOLS) for v, d in data.items()}
LABELS = hand_labels(scored["v1"].rows[:60])

labeled, _ = wai.attach_labels(scored["v1"].rows[:60], LABELS, kind="human")
trust = wai.judge_trust(labeled, refund_judge)
print(trust)
JUDGE = Judge(
    name="refund policy, as a program",
    agreement=trust["agreement"]["agreement"],
    human_n=trust["agreement"]["n"],
)
```

`judge_trust` also reports the two-half split, length sensitivity and
re-judge flips. Under 0.8 agreement, fix the judge before quoting any number
it produced (Zheng et al. 2023, MT-Bench).

## 4. The number, and what it rests on

Scores are in points, with the half-width of a 95% interval bootstrapped
over asks, not rollouts: raising `K` sharpens each ask and does not narrow
the interval. A branch every ask passes (or fails) gets a zero-width
bootstrap; that is not certainty, so `half_width` posts the exact bound
instead: 7 of 7 still allows a true rate of 59%, which is ±41 points. Every policy branch is its own behavior, so a fix to one shows
up next to what it did to the others.

```python
def half_width(ci95, mean, n_asks):
    """Half-width of a 95% interval over asks. When every ask agrees the bootstrap
    has zero width, which is not zero uncertainty: use the exact one-sided bound
    1 - 0.025**(1/n) (Clopper-Pearson; 18 of 18 asks still allows 81%)."""
    if ci95 and ci95[1] > ci95[0]:
        return (ci95[1] - ci95[0]) / 2
    assert mean in (0.0, 1.0), (mean, ci95)  # a zero-width interval off the edges is a bug
    return 1 - 0.025 ** (1 / n_asks)


def score(rows):
    """pass@1 in points, the half-width of its 95% interval, and the asks it rests on."""
    pa = wai.pass_at(rows, k=K)
    ci = half_width(pa.ci95, pa.pass_at_1, pa.n_groups)
    return round(100 * pa.pass_at_1, 1), round(100 * ci, 1), pa.n_groups


def behaviors(rows):
    """The headline and every policy branch as its own behavior."""
    out = {"refund_policy": score(rows)}
    for name, m in wai.marker_summary(rows).items():
        if m["n_tasks"] < 3:
            continue  # unmeasured: under three asks reach it, and the card says so
        ci = half_width(m["ci95"], m["mean"], m["n_tasks"])
        out[name] = (round(100 * m["mean"], 1), round(100 * ci, 1), m["n_tasks"])
    return out


for v, s in scored.items():
    pa = wai.pass_at(s.rows, k=K)
    capable = sum(1 for p in pa.per_task.values() if p < 1)
    print(f"{v}: pass@1 {score(s.rows)}  failure-capable asks {capable}/{pa.n_groups}")
    for name, (pts, ci, n) in behaviors(s.rows).items():
        print(f"   {name:<26} {pts:>5} +- {ci:<5} n={n}")
```

**Read the failure-capable count first.** An ask the agent always passes
contributes exactly zero to a paired comparison. That count is the ceiling
on any gain the set can show; a 90% pass rate on a set with six such asks
means the eval needs steering, not that the agent needs nothing ("Policy
Gradients": groups whose rollouts all score alike carry no signal).

## 5. The noise floor

Score the same version three times on the same frozen set. The floor is
t(df=runs-1) x run_std x sqrt(2): `run_std` is estimated from these very
runs, and a before/after delta is the difference of two draws. Two runs are
a difference, not a spread: t(df=1) is 12.71, so one lucky pair gives a floor
of 0 and an unlucky one a floor wider than the scale. A scripted agent gives
0; a model at temperature gives a few points.

```python
RERUNS = 3  # two give a difference, not a spread: t(df=1) is 12.71
reruns = [scored["v1"].rows] + [
    wai.evaluate(holdout(VERSIONS["v1"], tasks=frozen).rows(), refund_judge, tools=TOOLS).rows
    for _ in range(RERUNS - 1)
]
var = wai.eval_variance(*reruns)
NOISE = round(100 * var["noise_band"], 1)  # points: t(df=2)=4.30 x run_std x sqrt(2)
print(f"noise floor {NOISE} points ({var['n_runs']} re-runs, same test)")
```

## 6. How big the test has to be

Ask for the gain you care about and read how many asks it takes. With two
scored versions the spread is measured off your own paired rows; with one,
pass `rows=` and the model spread is used.

```python
need = wai.holdout_size(0.05, before=scored["v1"].rows, after=scored["v2"].rows, k=K)
print(f"asks to prove 5 points: {need['n_tasks']} (you have {need['n_paired']})")
```

When the estimate keeps sitting under what the set can resolve, stop
buying asks: "the effect is smaller than 5 points on this test" is a
finding.

## 7. Report

Post the behaviors once with what their scores rest on, then one run per
version. `method="eval"` says nothing was trained; the version is the
harness label, and `Harness.fingerprint` changes when the prompt, tools or
model do. Promote the version in production so the next one is the
candidate. The platform's verdict uses the rule this file uses: the
difference interval excludes zero and clears the noise floor.

**Names are the team's; the test's is its content.** `refund-agent`, `refund_policy` and `v1` are this playbook's examples. In a real repo name the agent after the product, the behaviors as the policy doc phrases them, and the versions as the team ships them (tag, PR, date, prompt label); the platform shows exactly what you send. Rules and a table: [docs.while.ai/platform/naming](https://docs.while.ai/platform/naming).

```python
tracked = track(
    "refund-agent",
    model=MODEL,
    harness=Harness(label="v1", instructions=POLICY, tools=TOOLS),
    transport=fake,  # drop this line to talk to the platform
)
for name, (_pts, _ci, n) in behaviors(scored["v1"].rows).items():
    tracked.behavior(
        Behavior(
            name=name,
            test_version=TEST_VERSION,
            n=n,
            judge=JUDGE,
            noise_floor=NOISE,
            contamination=0,  # nothing trained, nothing to leak
            reward_is_judge=False,
        )
    )
for version, s in scored.items():
    run = tracked.run(version, method="eval", targets=["refund_policy"], harness=version)
    for name, (pts, ci, n) in behaviors(s.rows).items():
        run.score(name, pts, ci=ci, n=n, test_version=TEST_VERSION)
    run.finish(
        record=RunRecord(
            data=Data(holdout=TEST_VERSION, n_holdout=len(asks)),
            eval=EvalSetup(
                metric="pass@1", k=K, run_std=var["run_std"], run_std_runs=RERUNS, reader=JUDGE.name
            ),
        )
    )
tracked.promote("v1")  # what is in production today; the next version is the candidate
print(tracked.verdict())
```

```text
refund_policy: v2 beats v1 by 71.4 (interval excludes zero, clears the noise floor of 0); judge agreement 1 on 60, n=63
```

Drop `transport=fake` and set `WHILEAI_API_KEY` (`wai signup --email
you@example.com`), and the same calls draw the Runs page: one dot per
version with its interval on the same held-out scale, the noise band, the
judge block, and the run record.

## Gates, with the math, before you spend

Each is a line of arithmetic on numbers you already have. Four of them
(mixed groups, truncation, teacher before student, the random-reward arm)
also decide which method to train; `pick-a-method/` routes on them. Every one was
skipped by a coding agent in dogfooding (2026-09-24, 314 runs audited), and
the run it would have saved is named.

- **n is asks, not rollouts.** Half-width 1.96·sd_ask/√n_asks. Rollouts as n
  made intervals √k too narrow (1,836 rollouts posted for 153 asks).
- **Assert lo ≤ score ≤ hi, and never post ci=0.** One run posted [94.0, 96.9]
  around its own 92.1.
- **Minimum detectable effect, 80% power: MDE = 2.8·sd/√n.** A gain on a
  selection set below MDE is noise; do not spend the held-out set on it. A
  harness picked on +13.3 at n=30 (MDE 19.2) returned +3.5 [−9.3, +16.3].
- **Ceiling: failure-capable asks / all asks.** Under 50 failure-capable asks,
  or a ceiling below 2·MDE, harden the set before buying an arm. Three
  frontier arms were bought on a set where 31 of 160 asks could move.
- **Expected mixed groups from the model you will train:**
  E = Σ_i (1 − p_i^k − (1 − p_i)^k). Below 0.3·N, an RL pool has nothing to
  learn ("Policy Gradients"). k=1 makes E = 0, so no DPO or GRPO verdict can
  come from a k=1 run. One pool sized with another model's p=0.285, not the
  student's 0.005, came back 0 of 90 mixed.
- **Below 30 asks, add asks, not rollouts.** SE ≥ σ_between/√n at any k.
- **Split by a hash of the ask id, never by position.** Writers cycle ask
  types, so `asks[::N]` aliases them: the same rows moved 20 to 30 points
  between two positional splits.
- **One behavior, one `test_version`, one k per comparison.** A sign test
  between an arm at k=1 and one at k=8 has null P(up) = p_i, not 0.5: a
  claimed p=0.0013 was 0.035.
- **Truncation.** Score only replies that ended; a control truncated at
  more than twice the treatment's rate is void (17 of 99 cut replies
  explained a whole 12.7-point gap). "Policy Gradients": score on EOS only.
- **Teacher before student.** Score the teacher on this set, at the
  student's length cap, before distilling from it: teacher − student > MDE.
  A teacher at 54.2 was distilled into a student already at 56.9.
- **RLVR on a Qwen base needs a random-reward arm** ("Evaluation":
  suspicious of RLVR gains on Qwen 2.5/3 bases; Shao et al. 2025). The gain
  from the reward is Δ_reward − Δ_random.
- **Post no score** when one grader reason covers ≥95% of rows, when the
  criterion could fire on under 90% of rows, or when a criterion sits at ≤2%
  on every arm including one told to do it. Each is a grader or a world bug.
- **`run.finish()` in a `finally`, with `cost_usd=`.** 30 of 314 runs were
  left "running", and no GPU run recorded its cost.

## What makes the number lie

- **Rows vanish from the denominator.** A row the grader failed on still
  counts. Report graded-count per version.
- **Both versions answered, one did not finish.** Record `finish_reason` at
  generation time; gate on the truncation gap between versions; pick a
  length cap neither reaches.
- **The simulated user runs on the model under test.** Pin `user_model=`,
  the same on both sides.
- **The world confirms what the agent claims.** A mock that echoes call
  arguments back grounds any fabrication. Prefer a real `execute=` world.
- **Ties.** Report the tie count next to every interval. Ties at 1: the set
  is saturated. Ties at 0 where the criterion could not fire: dilution.
  Ties at 0 where both versions genuinely fail: a result.
- **A trait score averaged with a robustness probe.** They point opposite
  ways by construction. Two behaviors; say which is the headline.

## Grounding

rlhfbook.com, "Evaluation": held-out sets, run-to-run spread, bootstrap over
prompts, judge agreement. "Policy Gradients": groups that all score alike
carry no signal (DAPO dynamic sampling), which is why the failure-capable
count is the ceiling. "Over-Optimization": what moves on the behaviors you
did not aim at. "Evaluation" also for the random-reward
confound on Qwen bases (Shao et al. 2025, Spurious Rewards). Miller 2024
(Adding Error Bars to Evals) for the ask as the unit. Clopper and Pearson
1934 for the exact bound at 0 or n; the t multiplier on a floor from a few
runs is textbook statistics. Zheng et al. 2023 for judge agreement; arXiv
2605.05973 for the winner's curse in adaptive benchmarking. The gates'
thresholds (0.3·N mixed, 50 failure-capable asks, 95%/90%/2%) are
convention, untested.
