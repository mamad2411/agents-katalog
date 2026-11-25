---
name: tool-call-efficiency
description: >
  Measure and train down the number of tool calls an agent spends per solved
  task, with no judge. Use when a coding agent is asked to make an agent
  cheaper or faster without making it worse: redundant re-fetches, tools
  called that the task did not need, lookups repeated across turns. The
  score is a program (checks pass AND at most `budget` calls), so it is a
  verifiable reward for GRPO, and correctness is tracked beside it so cutting
  calls never cuts solves.
metadata:
  version: "1.0.0"
---

# Tool-call efficiency

Every step below is in `check.py`, which runs offline in seconds. Its setup
defines the names the blocks use: `TOOLS`, `POLICY`, `before_agent` (wastes
calls), `after_agent` (does not), `HOLDOUT_SEEDS`, `TRAIN_SEEDS`, `K`,
`N_TASKS`, `REWARD_REF`, `stamp` (puts each task's checks in
`privileged.reference`), `pct`, `half`, `fake` (a recording transport), and
`tool_calls` from `whileai.simulations.score.hygiene`.

## 1. The score is a program

**Solved within budget.** A task counts when its checks pass AND the rollout
spent at most `BUDGET` tool calls. The behavior's score is the share of
held-out tasks solved within budget; higher is better. Mean calls per solved
task is the second number, from the same rows. No model grades anything, so
this is a verifiable reward (the SDK's `whileai.simulations.verify` module,
and "Policy Gradients", where GRPO climbs a reward that is a checker), and
`reward_is_judge=False` holds by construction.

```python
BUDGET = 1  # tool calls a solved task may spend


@wai.verifier
def solved(candidate, reference, row):
    """The task's checks: the reply says what the record says. Budget ignored."""
    return reference.lower() in candidate.lower()


@wai.verifier
def within_budget(candidate, reference, row):
    """Solved AND at most BUDGET tool calls. No judge: a program decides."""
    if reference.lower() not in candidate.lower():
        return 0, "unsolved"
    calls = tool_calls(row)
    if calls > BUDGET:
        return 0, f"solved with {calls} tool calls, budget {BUDGET}"
    return 1, f"solved with {calls} tool calls"


CASES = [
    ("solved within budget", {"final_text": "$129.00", "steps": [{"tool": "lookup_order"}]}, 1),
    ("solved over budget", {"final_text": "$129.00", "steps": [{"tool": "lookup_order"}] * 2}, 0),
    ("unsolved", {"final_text": "sorry", "steps": [{"tool": "lookup_order"}]}, 0),
]
for name, row, want in CASES:
    got = within_budget({**row, "privileged": {"reference": "$129.00"}})["reward"]
    assert got == want, f"{name}: reward {got}, wanted {want}"
```

**Unit-test the verifier before anything runs.** The three cases are the
labeled slice the platform's `Judge(agreement=, human_n=)` rests on. Add
your own before you quote a number.

**Both numbers from one grading pass.** Reward is `within_budget`; the
marker `solved` is correctness regardless of budget.

```python
def grade(rows):
    """Both numbers from the same rows: reward is within_budget, marker
    ``solved`` is correctness regardless of budget."""
    graded = wai.evaluate(rows, within_budget).rows
    for row in graded:
        row["markers"] = {"solved": solved(row)["reward"]}
    return graded


def score(graded, k=K):
    """Share of held-out tasks solved within budget (the behavior), share
    solved at all (correctness), mean tool calls per solved task."""
    efficiency = wai.pass_at(graded, k=k)
    correctness = wai.pass_at([{**r, "reward": r["markers"]["solved"]} for r in graded], k=k)
    solved_rows = [r for r in graded if r["markers"]["solved"] == 1]
    calls = sum(tool_calls(r) for r in solved_rows) / max(1, len(solved_rows))
    return efficiency, correctness, calls
```

## 2. The frozen held-out test first

**Draw the tasks once, then replay them.** `seeds=` draws the set;
`tasks=holdout` pins it for every later run, so before and after are paired
by task ("Evaluation": held-out sets stay apart from training, and a result
is only comparable with its setup held constant). `runs=3` gives the re-run
spread that becomes the behavior's `noise_floor`. A scripted agent gives 0;
a sampled model does not.

```python
holdout = wai.simulate(
    before_agent,
    tools=TOOLS,
    system_prompt=POLICY,
    seeds=HOLDOUT_SEEDS,
    situations=N_TASKS,
    budget=N_TASKS * K,
    mode="rl",
    repeats=K,
    repeat_policy="fixed",  # every task gets all k
    simulator=False,  # offline template writer; drop for the hosted writer
    reproducible=True,
    seed=1,
    concurrency=1,
)
before = wai.simulate(
    before_agent,
    tools=TOOLS,
    system_prompt=POLICY,
    tasks=holdout,  # the same tasks, frozen
    runs=3,  # three draws give a re-run spread
    mode="rl",
    repeat_policy="fixed",
    simulator=False,
    reproducible=True,
    seed=1,
    concurrency=1,
)
before_rows = grade(stamp(before.rows()))
before_eff, before_corr, before_calls = score(before_rows)
spread = wai.eval_variance(before_rows)
n_tasks = before_eff.n_groups
```

**Under 50 tasks the verdict says "unproven".** Raise `situations=` or add
seeds. `wai.holdout_size(effect, before=before_rows)` says how many tasks a
given gain needs.

**`seeds=` and `runs=` together raise.** `tasks= replays a fixed task set;
it cannot be combined with seeds=`. Draw with `seeds=` and `runs` unset,
then replay with `tasks=`, as above.

## 3. Training data, graded by the same verifier

**Roll the shipped agent, keep the 20-80% band, drop held-out overlap,
export.** Tasks every rollout passes or fails carry no gradient ("Policy
Gradients": DAPO's dynamic sampling drops unanimous groups). `decontaminate`
removes training rows that repeat a held-out task ("Evaluation").
`export_environment` writes a GRPO environment whose reward is your verifier,
named as `module:attr` because the trainer imports it by name.

```python
train = wai.simulate(
    before_agent,
    tools=TOOLS,
    system_prompt=POLICY,
    seeds=TRAIN_SEEDS,
    situations=120,
    budget=120 * K,
    mode="rl",  # successive repeats: stops early on unanimous tasks
    repeats=K,
    simulator=False,
    reproducible=True,
    seed=2,
    concurrency=1,
)
train_rows = grade(stamp(train.rows()))
selected, selection = wai.select_for_rl(train_rows, target=200)
clean, contamination = wai.decontaminate(selected, against=[before_rows])
env_dir = Path(tempfile.mkdtemp(prefix="tool-call-efficiency-"))
env = wai.export_environment(
    clean,
    env_dir,
    name="tool_call_efficiency",
    reward=REWARD_REF,
    tools=TOOLS,
    system_prompt=POLICY,
)
```

**Nothing in the band.** The shipped agent is unanimous on every task, so
there is nothing to learn from; raise `repeats=` or make the tasks harder
(`hard_share=0.7`).

**`export_environment` refuses the verifier object.** A verifier defined in
the script has no importable name. Pass `"your_module:within_budget"`.

## 4. After: same tasks, both numbers, then report

**Score the trained agent on the frozen tasks and compare.** `target` is
the claim; `must_not_regress=["solved"]` is the check. "Over-Optimization":
a proxy can rise while the real goal falls, and an agent that stops calling
tools scores perfectly on calls and zero on solves. When `solved` scores the
same on every row the report says the guard cannot fail; that is a floor
both agents share, not a pass.

```python
after = wai.simulate(
    after_agent,
    tools=TOOLS,
    system_prompt=POLICY,
    tasks=holdout,
    runs=3,
    mode="rl",
    repeat_policy="fixed",
    simulator=False,
    reproducible=True,
    seed=1,
    concurrency=1,
)
after_rows = grade(stamp(after.rows()))
after_eff, after_corr, after_calls = score(after_rows)
delta = wai.delta_report(
    before_rows,
    after_rows,
    target="pass_at_1",
    must_not_regress=["solved"],
)
print(wai.format_delta_report(delta))
```

**Report both behaviors on both versions.** The platform's verdict compares
the candidate to the served version and counts every other behavior that
came out lower. Drop `transport=fake` to talk to the platform; pass
`hours=`, `gpu=`, `cost_usd=` to `finish` from the trainer.

```python
tracked = track(
    "order-bot",
    model="Qwen/Qwen3-4B",
    harness=Harness(instructions=POLICY, tools=TOOLS),
    transport=fake,  # drop this line to talk to the platform
)
tracked.behavior(
    Behavior(
        name="tool-call-efficiency",
        test_version="v1",
        n=n_tasks,
        judge=Judge(name="within_budget verifier", agreement=1.0, human_n=len(CASES)),
        noise_floor=pct(spread["run_std"]),
        contamination=0,  # decontaminate ran; else pass what it would have dropped
        reward_is_judge=False,
        description=f"Share of held-out tasks solved within {BUDGET} tool call(s)",
    )
)
tracked.behavior(
    Behavior(
        name="correctness",
        test_version="v1",
        n=n_tasks,
        judge=Judge(name="solved verifier", agreement=1.0, human_n=len(CASES)),
        noise_floor=pct(spread["run_std"]),
        reward_is_judge=False,
        description="Share of held-out tasks solved, any number of calls",
    )
)
base = tracked.run("v0", method="none")
base.score("tool-call-efficiency", pct(before_eff.pass_at_1), ci=half(before_eff.ci95), n=n_tasks)
base.score("correctness", pct(before_corr.pass_at_1), ci=half(before_corr.ci95), n=n_tasks)
base.finish()
tracked.promote("v0")

run = tracked.run("v1", method="GRPO", targets=["tool-call-efficiency"], trained_on=[env["name"]])
run.score("tool-call-efficiency", pct(after_eff.pass_at_1), ci=half(after_eff.ci95), n=n_tasks)
run.score("correctness", pct(after_corr.pass_at_1), ci=half(after_corr.ci95), n=n_tasks)
run.finish()
verdict = str(tracked.verdict())
print(verdict)
```

**The line to read:** `tool-call-efficiency: v1 beats v0 by 45.5 (interval
excludes zero, clears the noise floor of 0); judge agreement 1 on 3, n=60`.
"about the same" means the interval includes zero: add tasks. "1 behavior
lower" means correctness fell: the budget is too tight for some tasks, or
the agent learned to skip a call it needed; raise `BUDGET` or fix the checks.
