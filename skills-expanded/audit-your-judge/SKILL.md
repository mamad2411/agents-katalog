---
name: audit-your-judge
description: >
  Check whether a judge can be trusted before its scores reach Select or
  Train: label a sample blind, grade it with every candidate judge, and
  read agreement, kappa and the false-pass rate against floors. Use before
  trusting any judge, rubric or grader score, before choosing a judge
  model, before calling compare_judges, judge_trust or attach_labels, and
  before Select curates rows by a judge's score. Triggers on judge,
  rubric, LLM-as-judge, grader, judge_trust, compare_judges, kappa,
  false-pass rate, judge agreement.
metadata:
  version: "1.1.0"
---

# Audit your judge

**Why.** A judge is a reward model, and a reward model is only as good as
its measured accuracy against people (Lambert 2025, chapter Reward
Modeling). A biased judge does not look biased. It looks like the training
method failed. So measure the judge before you believe any number it
produced, and before any row is selected by its score.

**The order, every time.**

1. Pin a model judge's temperature to 0.
2. Label a sample blind, with a codebook written first.
3. Grade that sample with every candidate judge: `compare_judges`.
4. Read agreement, kappa and the false-pass rate against the floors.
5. Report the length correlation.
6. Ablate the rubric one clause at a time.
7. Reverse the presentation order on pairs.
8. Only then grade the frozen test and report.

`check.py` runs every block below offline in under a second. Its setup
defines: `ROWS` (60 transcripts whose true verdict is known by
construction), three scripted judges (`always_pass`; `generous`, which
reads only the reply's tone; `accurate`, which reads the tool calls),
`generous_with_clause` and `accurate_with_clause` (the same two with one
extra rubric clause), `prefers` (a pairwise pick that breaks ties by
position), `BLIND_LABELS` (the codebook applied with no judge's verdict in
view), and `fake` (a recording transport that answers like the platform). It imports `wai` as `import whileai as wai`, and `attach_labels`,
`evaluate` from `whileai.simulations`.

## Four traps in the SDK

- **`judge_trust(rows, judge)` reads the `reward` already on each row.** It
  does not call `judge` for the headline agreement, so it can print 1.0
  for a judge that never ran. Use `compare_judges`, which grades the rows
  with each judge itself. If you must use `judge_trust`, grade the rows
  with that judge first (`run_judge` or `data.grade` stamp `judge_name` on
  every row).
- **`Judge(agreement=, human_n=)` are typed fields.** Nothing checks them.
  Fill them from a `compare_judges` result (step 8), never from memory.
- **`check_spread` measures variance, not accuracy.** "spread: yes" means
  the scores differ. A position-biased judge spreads too.
- **`attach_labels` defaults `kind="human"`.** Pass `kind=` every time.
  Labels a model wrote are `kind="model"`; recording them as human makes
  every later check trust a measurement no person made.

## 1. Temperature 0

A rating that moves when the answer did not is noise, and it is free to
remove. The book names the trick: "a common trick to improve the
robustness of LLM-as-a-judge workflows is to use a sampling temperature of
0" (Lambert 2025, chapter Reward Modeling). A spec-backed `Judge` gets it
already (`JUDGE_TEMPERATURE = 0.0`, `whileai/simulations/defaults.py`). **A
raw judge callable does not**: pin it yourself. The judges in `check.py`
are programs, so they have no sampling to pin.

## 2-4. Label blind, grade, read the floors

**Sample.** Pull rows across the judge's whole score range, not the easy
middle. Strip anything that gives the verdict away (`rule_reason`,
`gold_*`). Write the codebook before labelling, or it drifts toward what
is on screen. The book's size for a held-out reward-model check is 50 to
200 examples (Lambert 2025, chapter Reward Modeling).

**Size by the failures, not the rows.** The false-pass rate is computed
only over rows the labels call a failure. At a rate near 0.5 its 95%
half-width is about `1.96 * sqrt(0.25 / n_fail)`: 24 failures give
±20 points, 96 give ±10. Count `n_fail` before you trust the rate.

```python
labeled, label_report = attach_labels(ROWS, BLIND_LABELS, annotator="reviewer", kind="human")
table = compare_judges(
    labeled, {"always pass": always_pass, "generous": generous, "accurate": accurate}
)
print(table)

assert label_report["rows_labeled"] == 60, label_report
assert table.n_rows == 60
always_pass_score, generous_score, accurate_score = (
    table["always pass"],
    table["generous"],
    table["accurate"],
)

assert always_pass_score.agreement == 0.4, always_pass_score.agreement
assert always_pass_score.kappa is not None and abs(always_pass_score.kappa) < 1e-9, (
    always_pass_score.kappa  # "just says pass": kappa is 0, exactly
)
assert always_pass_score.leak == 1.0, always_pass_score.leak
assert generous_score.agreement == 0.7, generous_score.agreement  # looks like a real judge...
assert generous_score.kappa is not None and generous_score.kappa < 0.5, generous_score.kappa
assert generous_score.leak == 0.5, generous_score.leak  # ...but passes half of what really failed
```

**Read three numbers, not one.**

- **Agreement** alone is not enough. A judge that always says pass agrees
  at the base pass rate: 0.40 here.
- **Kappa** subtracts that chance rate (Cohen 1960):
  `kappa = (observed - chance) / (1 - chance)`. `always_pass` lands at
  exactly 0.
- **False-pass rate** (`leak`) is the share of true failures the judge
  passes. `generous` agrees 0.70, which looks fine, and passes half of
  what really failed. Train on its rewards and you train the failure.

**Floors: Wilson lower bound of agreement >= 0.8 and kappa >= 0.6.**
Convention, untested: the SDK's own gate. The 0.8 borrows the 81%
human-human agreement in Zheng et al. 2023 (arXiv:2306.05685), and 0.6 is
the bottom of Landis and Koch's (1977) "substantial" band. Neither paper
sets these as trust thresholds. Only `accurate` clears both:

```python
assert accurate_score.ok, accurate_score
assert accurate_score.agreement is not None and accurate_score.agreement >= 0.8
assert accurate_score.kappa is not None and accurate_score.kappa >= 0.6
assert table.best is not None and table.best.name == "accurate", table.best
```

## 5. Length correlation

Longer answers win preference labels for reasons unrelated to quality
(verbosity bias; Lambert 2025, chapter Preference Data), and unexplained
verbosity is a symptom of optimizing against a flawed reward (chapter
Over-Optimization). It is why AlpacaEval is length-controlled (Dubois et
al. 2024). Report the correlation on every judge, not only the suspect:

```python
def pearson(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    vx = sum((x - mx) ** 2 for x in xs)
    vy = sum((y - my) ** 2 for y in ys)
    return cov / (vx * vy) ** 0.5


def length_bias(judge_score) -> float:
    """Pearson correlation between reply length and judge reward: the
    check AlpacaEval's length control exists because a judge skips."""
    graded = [r for r in judge_score.rows if r.get("reward") is not None]
    lengths = [float(len(str(r.get("final_text") or ""))) for r in graded]
    rewards = [float(r["reward"]) for r in graded]
    return pearson(lengths, rewards)


generous_length_bias = length_bias(generous_score)
accurate_length_bias = length_bias(accurate_score)
print(
    f"length x reward correlation: generous {generous_length_bias:+.2f}, "
    f"accurate {accurate_length_bias:+.2f}"
)

assert generous_length_bias < -0.9, generous_length_bias  # shorter replies read as "resolved"
assert abs(accurate_length_bias) < abs(generous_length_bias), (
    accurate_length_bias,
    generous_length_bias,
)
```

`generous` comes out at -1.00: here tone and length are the same signal.
`accurate` is at -0.59, because one failure class writes longer refusals.
A good judge can still carry length by accident; the number tells you.

## 6. Ablate the rubric

Add or remove one clause and re-grade. A large swing in mean reward means
that clause is carrying the score. A judge that pattern-matches the
surface collapses under a clause it cannot verify; a judge that reads the
trajectory does not move. The book does not prescribe this audit; it is
house practice.

```python
def mean_reward(judge_score) -> float:
    """Mean judge reward across a JudgeScore's own graded rows."""
    graded = [r["reward"] for r in judge_score.rows if r.get("reward") is not None]
    return sum(graded) / len(graded)


baseline = compare_judges(labeled, {"generous": generous, "accurate": accurate})
with_clause = compare_judges(
    labeled, {"generous": generous_with_clause, "accurate": accurate_with_clause}
)
for name in ("generous", "accurate"):
    delta = mean_reward(with_clause[name]) - mean_reward(baseline[name])
    print(f"clause delta, {name}: {delta:+.3f}")

generous_delta = mean_reward(with_clause["generous"]) - mean_reward(baseline["generous"])
accurate_delta = mean_reward(with_clause["accurate"]) - mean_reward(baseline["accurate"])
assert generous_delta < -0.5, generous_delta  # the weak judge collapses
assert accurate_delta == 0.0, accurate_delta  # the judge that reads substance does not move
```

## 7. Reverse the order

The MT-Bench judge prompt the book quotes tells the judge to "avoid any
position biases" (Lambert 2025, chapter Reward Modeling); telling it does
not make it so. Grade each pair both ways and count flips. The noise sits
where the pair is a real tie: here every tie flips and no decisive pair
does. Before you feed a ranking (DPO pairs, GAR, anything relative) from a
real judge, measure its flip rate on your own ties. If it is high, use the
top pick only.

```python
def flip_rate(pairs: list[tuple[dict, dict]]) -> float:
    flips = 0
    for a, b in pairs:
        winner_forward = a if prefers(a, b) == "a" else b
        winner_backward = b if prefers(b, a) == "a" else a
        if winner_forward is not winner_backward:
            flips += 1
    return flips / len(pairs)


ok_rows = [r for r in ROWS if r["rollout_id"].startswith("ok-")]
refuse_rows = [r for r in ROWS if r["rollout_id"].startswith("refuse-")]
tied_pairs = list(zip(ok_rows[::2], ok_rows[1::2]))  # both score 1 under `generous`: a real tie
decisive_pairs = list(zip(ok_rows, refuse_rows))  # one scores 1, one scores 0: real signal

tied_flips = flip_rate(tied_pairs)
decisive_flips = flip_rate(decisive_pairs)
print(f"order reversal: {tied_flips:.0%} of ties flip, {decisive_flips:.0%} of decisive pairs flip")

assert tied_flips == 1.0, tied_flips  # every tie is decided by position alone
assert decisive_flips == 0.0, decisive_flips  # real disagreement does not move
```

## 8. Grade the frozen test, then report

The judge that cleared the floors, not a fresh one, grades the frozen
test. Its `Judge` record carries the numbers `compare_judges` just
measured. `check.py`'s setup builds the test the way
`strengthen-your-evals` does and defines `data` (two agent versions),
`LIVE_TOOLS`, `LIVE_POLICY`, `TEST_VERSION`, `NOISE`, `K`, `asks` and
`behaviors`:

```python
JUDGE = Judge(
    name="accurate (tool-call eligibility check)",
    agreement=table["accurate"].agreement,
    human_n=table["accurate"].n,
)
scored = {v: evaluate(d.rows(), accurate, tools=LIVE_TOOLS) for v, d in data.items()}
```

Every skill ends the same way (`skills/README.md`): score every behavior,
not only the one you audited the judge for, and post the run with the
judge's measured agreement attached:

```python
tracked = track(
    "returns-agent",
    model="scripted-agent",
    harness=Harness(label="v1", instructions=LIVE_POLICY, tools=LIVE_TOOLS),
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
            contamination=0,
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
            eval=EvalSetup(metric="pass@1", k=K, run_std=NOISE, run_std_runs=2, reader=JUDGE.name),
        )
    )
tracked.promote("v1")
print(tracked.verdict())
```

A judge that fails the floors never reaches this step. A policy trained
against a judge's habits will find every hole this file measured
(Lambert 2025, chapter Over-Optimization).

## Reading the result

| you see | it means |
|---|---|
| agreement >= 0.8, kappa >= 0.6, low false-pass rate on enough failures | the judge is usable |
| a high mean with no blind labels behind it | unknown; a soft judge produces exactly this |
| the mean moves a lot when one clause changes | that clause, not the behavior, drives the score |
| a clause hurts the strongest judge most | it names evidence the payload does not carry |
| pairwise ties flip on reversed order | use the top pick only, never the full ranking |
| "the method failed" and the judge was never audited | audit the judge before believing it |

Two more once a judge clears: grade with a different model family than
the one you train, since models favor their own outputs (self-preference
bias, Panickssery, Bowman and Feng 2024; Lambert 2025, chapter Synthetic
Data and Distillation). And never let a judge check what code can check
exactly (a field present, an id kept, an exact string). Split the rubric:
a program checks those, the judge grades only what a program cannot.

## Sources

**From the book (rlhfbook.com, Lambert 2025).** Reward Modeling: a judge
is a generative reward model (Zheng et al. 2023), temperature 0, a small
held-out accuracy set of 50 to 200 examples, generative judges still lag
trained reward models (Mahan et al. 2024; Zhang et al. 2025; Ankner et al.
2024), the MT-Bench prompt's position-bias line. Preference Data:
verbosity bias. Synthetic Data and Distillation: self-preference.
Over-Optimization: what a policy does to a flawed reward.

**House practice, not the book.** The false-pass rate as the headline;
the floors (convention, untested); rubric ablation and order reversal as
routine audits; sizing by the number of failures; splitting the rubric
between a program and a judge.
