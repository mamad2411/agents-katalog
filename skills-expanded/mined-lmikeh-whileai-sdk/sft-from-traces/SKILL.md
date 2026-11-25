---
name: sft-from-traces
description: >
  Turn an agent's own production traces into supervised fine-tuning rows and
  prove the result on a frozen held-out test. Use when a coding agent has a
  JSONL of traces (prompt, steps, final_text, a 0/1 label) from a deployed
  agent, wants to fix the failures they show with SFT rather than RL, and
  needs the before/after delta, the noise floor and the contamination count
  reported to the While platform so a person can decide whether to promote.
metadata:
  version: "1.0.0"
---

# SFT from traces

Hold out a test by task first, sample more attempts around the failures
the traces show, keep what a program judge approves, export a TRL file
with loss masks, and score the fine-tuned agent on the same frozen test.

`check.py` runs every block below offline. Its setup defines the names the
blocks use: `TRACES_PATH` (a JSONL the fixture writes, 40 rows from a
scripted refund agent), `TOOLS` and `POLICY`, `before_agent` (the agent in
production, an `agent(message) -> {"steps", "final_text"}` callable),
`after_agent` (the stand-in for the fine-tuned model), `refund_judge` and
`length_judge` (judges that are programs), `fake` (a recording platform
transport), `K = 4`, `TEST_VERSION = "heldout-v1"` and `OUT_DIR`.

## 1. Read the traces

**Load and report.** `load_traces` normalizes the supported shapes;
`trace_report` says what the traces carry and where generation will aim.

```python
traces = wai.load_traces(str(TRACES_PATH))
report = wai.trace_report(traces, tools=TOOLS, policy=POLICY)
print(wai.format_trace_report(report))
```

## 2. Freeze the held-out test first

**Hold out by task, never by row.** A task is a situation; two rows of the
same ask land on the same side. Traces with no `task_id` need one per
distinct ask before this step.

```python
tasks = sorted({t["task_id"] for t in traces})
held = set(tasks[::3])
heldout_traces = [t for t in traces if t["task_id"] in held]
train_traces = [t for t in traces if t["task_id"] not in held]
```

**Roll the same agent three times and measure the spread.** One evaluation
is a draw, not a distribution ("Evaluation"). `tasks=` pins the held-out
asks by `task_id`, `runs=3` stamps `lineage.eval_run`, and `eval_variance`
turns the three pass@1 means into `run_std_points`, the noise floor. Judge
the rows once per behavior: the target and the one nobody trains.

```python
def roll_heldout(agent, version: str) -> wai.SimulationData:
    """The frozen test, rolled three times so the re-run spread is measurable."""
    return wai.simulate(
        agent,
        tools=TOOLS,
        system_prompt=POLICY,
        tasks=heldout_traces,  # the held-out asks, keyed by task_id
        simulator=False,
        mode="rl",
        repeats=K,
        repeat_policy="fixed",
        runs=3,
        reproducible=True,
        seed=0,
        concurrency=1,
        advanced={"model_version": version},  # tells the two arms apart
    )


before_data = roll_heldout(before_agent, "refund-bot-base")
heldout_asks = [t["prompt"] for t in heldout_traces]
before = wai.evaluate(
    before_data.rows(), refund_judge, model="base", tools=TOOLS, eval_set=heldout_asks
)
before_len = wai.evaluate(before_data.rows(), length_judge, model="base", eval_set=heldout_asks)
noise = wai.eval_variance(before.rows)
noise_len = wai.eval_variance(before_len.rows)
```

**Declare the test on the platform before training.** `test_version` names
the frozen set, `n` is the task count, `noise_floor` the spread just
measured. A program that reads the tool calls is a verifier, so
`reward_is_judge=False`; a model judge that also picked the demos is
`True`, and the platform will say so.

```python
tracked = track(
    "refund-bot",
    model="Qwen/Qwen3-4B",
    harness=Harness(instructions=POLICY, tools=TOOLS),
    transport=fake,  # drop transport= to talk to the real platform
)
tracked.behavior(
    Behavior(
        name="refund_policy",
        test_version=TEST_VERSION,
        n=len(held),
        judge=Judge(name="refund policy as a program"),
        noise_floor=noise["run_std_points"],
        reward_is_judge=False,  # a program reading the tool calls is a verifier
        description="Refund only when the policy allows",
    )
)
tracked.behavior(
    Behavior(
        name="length",
        test_version=TEST_VERSION,
        n=len(held),
        noise_floor=noise_len["run_std_points"],
        description="Reply under 40 words; not trained",
    )
)
```

Under 50 held-out tasks the verdict reads `unproven`;
`wai.holdout_size(effect, before=..., after=...)` says how many to hold out.

## 3. More attempts around the failures

**Seed with the asks the agent failed, not with the traces themselves.**
`mine_traces` lists the flawed rows; their asks become `seeds=`, ids and
all. Do not also pass those rows as `traces=`: the leakage gate drops every
generated row that near-copies a source trace, which is every seed.
For the hosted writer drop `simulator=False` and raise `situations`, or
use `wai.simulate_from_traces(train_traces, before_agent, ...)`. Passing
train traces join the pool as demonstrations.

```python
mined = wai.mine_traces(train_traces)
failing_asks = sorted({train_traces[i]["prompt"] for i in mined["flaw_rows"]})
pool = wai.simulate(
    before_agent,
    tools=TOOLS,
    system_prompt=POLICY,
    seeds=failing_asks,  # the asks the agent failed, real ids and all
    grader=refund_judge,  # graded in the loop; the search re-rolls failures
    simulator=False,  # offline writer; drop for the hosted one
    mode="rl",
    repeats=10,  # rejection sampling wants 10 to 30 per ask
    repeat_policy="fixed",
    situations=len(failing_asks),
    budget=len(failing_asks) * 10,
    reproducible=True,
    seed=1,
    concurrency=1,
    advanced={"model_version": "refund-bot-base"},
)
candidates = pool.rows() + [t for t in train_traces if t.get("reward") == 1]
```

**Grade training rows with `grader=` or `wai.run_judge`, not `evaluate`.**
`evaluate` stamps eval lineage and `select_for_sft` warns on it: training on
those rows makes the held-out scorer the reward model.

## 4. Keep what the judge approved

**Rejection sampling.** `select_for_sft` keeps each ask's highest-reward
completion, then round-robins across behavior signatures so every distinct
way of being right appears before any repeat ("Rejection Sampling"). The
pool is the agent's own output filtered by a judge; unfiltered self-output
teaches the agent its own habits ("Synthetic Data and Distillation").

```python
selected, selection = wai.select_for_sft(candidates, target=200)
```

## 5. Decontaminate before export

**Drop anything that overlaps the held-out asks.** Task id first, then
verbatim, then the Llama 2 rule, 8-grams covering 80% of the words
("Evaluation"). Template-written asks that differ only by an id trip the
last rule; read `contamination["examples"]` and accept the loss, or hold
out by template as well as by task.

```python
clean, contamination = wai.decontaminate(selected, against=[heldout_traces])
```

## 6. Export for TRL

**One row per demonstration, in the shape TRL trains on.** `format="trl"`
writes conversational rows with dict arguments and no `prompt` column, so
TRL applies the chat template, and no `loss_mask`, because trl 0.19.1's
`SFTTrainer` reads none. The report's `mask_mode` says what TRL will do
with the file: every token of every turn, unless `assistant_only_loss=True`
in `SFTConfig` (which needs a chat template with a `{% generation %}`
block) trains the assistant turns only ("Instruction Fine-Tuning"; tool
output is the environment speaking). `mask_mode="final"` writes
prompt/completion rows TRL trains on the last assistant turn only, for
traces whose earlier agent turns were scripted.

```python
SFT_PATH = OUT_DIR / "refund-sft.trl.jsonl"
export = wai.export_dataset(clean, str(SFT_PATH), system_prompt=POLICY, tools=TOOLS, format="trl")
```

Train on `SFT_PATH` with TRL's `SFTTrainer`, log the curve with
`trainer.add_callback(wai.TrainerCallback(run))`, and wrap the adapter as
`after_agent`. `check.py` uses a second script that slips less.

## 7. Score the after agent on the same test

**Same tasks, same k, same runs, one report per behavior.** With three runs
on each side `delta_report` computes the re-run floor itself and marks the
result `replicated`. The second report checks the behavior you did not
train ("Over-Optimization").

```python
after_data = roll_heldout(after_agent, "refund-bot-sft")
after = wai.evaluate(
    after_data.rows(), refund_judge, model="sft", tools=TOOLS, eval_set=heldout_asks
)
after_len = wai.evaluate(after_data.rows(), length_judge, model="sft", eval_set=heldout_asks)
delta = wai.delta_report(before.rows, after.rows, target="pass_at_1")
delta_len = wai.delta_report(
    before_len.rows, after_len.rows, target="pass_at_1", must_not_regress=["pass_at_1"]
)
```

## 8. Report and read the verdict

**Score every behavior on both versions.** `base` is served, `v1` the
candidate. `points(scored)` in `check.py` turns `wai.pass_at(scored.rows,
k=K)` into `score` in points, `ci` the 95% half-width and `n` the task
count.

```python
base = tracked.run("base", method="none")
base.score("refund_policy", test_version=TEST_VERSION, **points(before))
base.score("length", test_version=TEST_VERSION, **points(before_len))
base.finish()
tracked.promote("base")  # what production serves today

run = tracked.run("v1", method="SFT", targets=["refund_policy"], trained_on=["refund-sft"])
run.score("refund_policy", test_version=TEST_VERSION, **points(after))
run.score("length", test_version=TEST_VERSION, **points(after_len))  # the untrained one too
run.finish(hours=0.4, gpu="1xH100", cost_usd=6)
verdict = str(tracked.verdict("refund_policy"))
print("verdict:", verdict)
```

`check.py` prints `unproven: refund_policy: v1 beats base by 20.8 (interval
excludes zero, clears the noise floor of 6.44) ... n=14 under 50; judge
agreement unmeasured`. Each gap names its fix: more held-out tasks, and
`wai.attach_labels(kind="human")` plus `wai.judge_trust` for
`Judge(agreement=, human_n=)`.
