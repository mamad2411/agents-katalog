---
name: dpo-pairs
description: >
  Turn graded rollouts of an agent into chosen/rejected preference pairs for
  DPO, check that the pairs teach the behavior and not a tic, write the JSONL
  a DPO trainer loads, and prove the result on a frozen held-out test reported
  to the While platform. Use when a coding agent is asked to build DPO or
  preference data from an agent's own rollouts, to fix a tool-use or policy
  slip with preference training, or to show that a trained version beats the
  served one.
metadata:
  version: "1.0.0"
---

# DPO pairs from graded rollouts

DPO trains on pairs: same ask, one reply preferred, no reward model in the
loop ("Direct Alignment"). Where the same ask passed once and failed once, the
contrast is the signal.

Names from `check.py` used below: `TOOLS` and `POLICY` (a refund agent's
tools and rules), `TRAIN_ASKS` and `TEST_ASKS` (two disjoint ask lists),
`before` (the agent you have; a scripted bot that refunds before looking the
order up on half its rollouts), `after` (stands in for the model trained on the
pairs), `refund_judge` (the policy as a program), `train_reward` (one rule of
it, the training signal), `length_judge` (an untrained behavior), `fake` (a
recording transport), `OUT` (an output folder).

## 1. Freeze the held-out test first

Held out by task: the test asks are different situations from the training
asks, not different rollouts of the same ones. Roll the current agent on it
three times so the eval's own re-run spread is on record; that spread is the
`noise_floor` a gain has to clear ("Evaluation": one evaluation is a draw).

```python
K = 4  # rollouts per ask
SIM = dict(
    tools=TOOLS,
    system_prompt=POLICY,
    simulator=False,
    mode="rl",
    repeats=K,
    repeat_policy="fixed",
    reproducible=True,
    seed=0,
    concurrency=1,
)
test = wai.simulate(
    before, seeds=TEST_ASKS, situations=len(TEST_ASKS), budget=len(TEST_ASKS) * K, **SIM
)
test_tasks = {r["scenario_id"] for r in test.trajectories}
base = wai.simulate(before, tasks=test, runs=3, advanced={"model_version": "v0"}, **SIM)
base_scored = wai.evaluate(base, refund_judge, tools=TOOLS)
floor = wai.eval_variance(base_scored.rows)
noise_floor = 100 * floor["run_std"]
print(f"frozen test: {len(test_tasks)} tasks, k={K}, noise floor {noise_floor:.1f} points")

assert len(test_tasks) == len(TEST_ASKS), "every test ask must be its own task"
assert not test.warnings and not base_scored.warnings, (test.warnings, base_scored.warnings)
```

`simulator=False` is the offline situation writer; drop it for the hosted one.
`advanced={"model_version": ...}` names the arm on every row, so the later
delta report can tell the two apart. A scripted bot re-runs identically, so
the floor here is 0; a sampled model gives a real number.

## 2. Roll several times per training ask, graded in the loop

The training reward is a program passed as `grader=`, so every row carries
grade lineage. Do not use `evaluate()` here: its rows carry eval lineage, and
`build_preference_pairs` warns that training on them turns the held-out scorer
into the reward.

```python
train = wai.simulate(
    before,
    seeds=TRAIN_ASKS,
    situations=len(TRAIN_ASKS),
    budget=len(TRAIN_ASKS) * K,
    grader=train_reward,
    **SIM,
)
rows = [dict(r) for r in train.trajectories]
assert not train.warnings, train.warnings
assert test_tasks.isdisjoint(r["scenario_id"] for r in rows), "test tasks leaked into training"
```

## 3. Build the pairs, length-matched

**Why `length_match=True`.** Verbosity is what a reward learns first
("Over-Optimization"); DPO picks up a length gap faster than the behavior. So
each chosen row takes the rejected row closest to it in length, and the pair
differs in what the agent did, not in how many words it used. Read the report:
pairs per ask (`prompts_with_contrast` of `prompts_seen`) and
`chosen_longer_frac`. Near 1.0 means the pairs teach length; the fix is the
same ask set at higher `repeats`, or a reward that does not pay for words.

```python
pairs, pair_report = wai.build_preference_pairs(rows, length_match=True)
print(
    f"pairs {pair_report['pairs']} from {pair_report['prompts_with_contrast']}"
    f"/{pair_report['prompts_seen']} asks, chosen longer in "
    f"{pair_report['length']['chosen_longer_frac']:.0%}"
)
for note in pair_report["warnings"]:
    print("!", note)
assert pairs, "no ask had both a pass and a fail; raise repeats or use a harder ask set"
assert pair_report["length"]["chosen_longer_frac"] < 0.8, "pairs would teach length"
```

Each pair carries `margin`, `first_turn_differs` and `same_policy`; both sides
from the policy you train is the on-policy setup (Tulu 3, Lambert et al. 2024).

## 4. Check the pairs are not teaching a tic

`style_report` says how often each side carries hedging, apology, boilerplate
or sycophancy, and whether reward correlates with the phrase. A flag means the
reward pays for the tic and the pairs will teach it; fix the reward, not the
pairs. Print it: its last line names the markers it did not stamp, so a clean
report is not read as a clean agent. `length_report` catches truncated replies.

```python
sides = [p["chosen"] for p in pairs] + [p["rejected"] for p in pairs]
style = wai.style_report(sides)
length = wai.length_report(sides)
assert not style["warnings"], style["warnings"]
assert length["n_truncated"] == 0, length
print(style)  # the report prints itself: every marker, and the ones it did not stamp
```

## 5. Decontaminate against the frozen test

The Llama 2 rule (8-grams, 80% coverage) plus exact and same-task matches
("Evaluation"). A hit is a test ask in the pairs; drop it or the gain is
memorization.

```python
clean, decon = wai.decontaminate(pairs, against=[base_scored.rows])
assert decon["n_contaminated"] == 0, decon["examples"]
print(f"decontaminate: {decon['n_kept']} pairs kept against {decon['n_eval_texts']} test asks")
```

## 6. Write the JSONL the trainer loads

`format="trl"` writes the conversational preference triple TRL's `DPOTrainer`
loads: `prompt` is the messages up to the first assistant turn, `chosen` and
`rejected` are the completions. `wai.to_trl(pairs)` is not this step: it
reshapes rows already exported.

```python
export = wai.export_preference(
    clean, str(OUT / "pairs.jsonl"), system_prompt=POLICY, tools=TOOLS, format="trl"
)
print(f"wrote {export['path']}: {export['pairs']} pairs")
```

Train with `DPOTrainer(..., train_dataset=load_dataset("json",
data_files=str(OUT / "pairs.jsonl")))` and add
`wai.TrainerCallback(run)` once the run below exists, so the loss curve
reaches the platform. Here `after` stands in for the trained model.

## 7. Prove it on the frozen test and report

Both arms run the same pinned tasks three times. `delta_report` pairs by task,
bootstraps the interval, and computes the re-run floor from the six runs;
`target_verdict == "moved"` is the claim.

```python
cand = wai.simulate(after, tasks=test, runs=3, advanced={"model_version": "v1"}, **SIM)
cand_scored = wai.evaluate(cand, refund_judge, tools=TOOLS)
delta = wai.delta_report(base_scored.rows, cand_scored.rows, target="pass_at_1")
print(wai.format_delta_report(delta))
assert delta["ok"] and delta["target_verdict"] == "moved", delta["warnings"]
```

Then report every behavior, not only the target: `length` is the check that
the gain did not come with a tic ("Over-Optimization"). `reward_is_judge=False`
is true here because `train_reward` is one rule and `refund_judge` is the whole
policy. Drop `transport=fake` for the real platform.

```python
def score(data: wai.SimulationData, judge) -> dict[str, float | int]:
    """One behavior on the frozen test: pass@1 in points, 95% half-width, tasks."""
    graded = wai.evaluate([dict(r) for r in data.trajectories], judge, tools=TOOLS)
    pa = wai.pass_at(graded.rows, k=K)
    lo, hi = pa.ci95
    return {"score": 100 * pa.pass_at_1, "ci": 100 * (hi - lo) / 2, "n": pa.n_groups}


JUDGES = {"refunds": refund_judge, "length": length_judge}
tracked = track(
    "refund-bot",
    model="Qwen/Qwen3-4B",
    harness=Harness(instructions=POLICY, tools=TOOLS),
    transport=fake,
)
tracked.behavior(
    Behavior(
        name="refunds",
        test_version="t1",
        n=len(test_tasks),
        judge=Judge(name="refund_judge, a program"),
        noise_floor=noise_floor,
        contamination=decon["n_contaminated"],
        reward_is_judge=False,
    )
)
tracked.behavior(Behavior(name="length", test_version="t1", n=len(test_tasks)))
v0 = tracked.run("v0", method="none")
for name, judge in JUDGES.items():
    v0.score(name, test_version="t1", **score(base, judge))
v0.finish()
tracked.promote("v0")
run = tracked.run("v1", method="DPO", targets=["refunds"], trained_on=["refund-pairs"])
for name, judge in JUDGES.items():
    run.score(name, test_version="t1", **score(cand, judge))
run.finish()
verdict = str(tracked.verdict("refunds"))
print(verdict)
```

Expected line: `unproven: refunds: v1 beats v0 by 34.4 (interval excludes
zero, clears the noise floor of 0); n=8 (n=8 under 50; judge agreement
unmeasured)`. The two gaps are real. `wai.holdout_size(0.05,
before=base_scored.rows)["n_tasks"]` says how many test tasks buy the first;
grading a labeled slice by hand and passing `Judge(agreement=, human_n=)` buys
the second. Pass `hours=`, `gpu=`, `cost_usd=` to `run.finish` from the real
job.
