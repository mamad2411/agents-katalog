---
name: grpo-verifier
description: >
  Train an agent with GRPO when the reward is a program, and prove the gain.
  Use when a coding agent is asked to do RL on a rule code can check (a tool
  called before another, an argument in range, a phrase in the reply), to
  write or test a verifier reward, to export a verifiers environment for a
  GRPO trainer, or to report a trained version against a frozen held-out test
  with its training curve. Not for rewards that need a model judge.
metadata:
  version: "1.0.0"
---

# GRPO with a verifier reward

The reward is a function of the trajectory. It costs nothing per call and
can be wrong in one way: rejecting right answers or accepting wrong ones. So
the order is fixed: test the reward, freeze the held-out test, then generate,
select, export, train, score, report.

`check.py` runs every block below offline. Names it defines: `TOOLS`, `POLICY`,
`LIMIT`, `TRAIN_SEEDS`, `HELD_SEEDS`, `K` (rollouts per ask), `before_agent`
(the policy before training), `after_agent` (stands in for the trained
policy), `placeholder` (an agent whose replies are never scored), `points`
(pass@1 as score, 95% half-width, task count), `fake` (a recording transport),
`fake_grpo_loop` (a stand-in for the trainer), `OUT`.

## 1. Write the reward and unit-test it first

**The verifier reads the trajectory**: which tools ran, with what arguments,
in what order, and the final text. `@wai.verifier` wraps
`fn(candidate, reference, row) -> score` or `(score, reason)`; `candidate` is
the final text, `row["steps"]` the tool calls. Compose rules with
`verify.All([...])`.

**Three hand-written rows before anything else.** A reward that rejects a
right answer teaches the policy to avoid right answers, and no later step can
see it. `wai.audit_grades` does this at scale with a model judge, and
`select_for_rl(audit=...)` carries its warning.

```python
@wai.verifier
def refund_verifier(candidate: str, reference: Any, row: dict) -> tuple[float, str]:
    """Reads the trajectory: tool calls, their arguments, and the final text."""
    looked: dict[str, dict] = {}
    for step in row.get("steps") or []:
        args = step.get("arguments") or {}
        if step.get("tool") == "lookup_order":
            looked[str(args.get("order_id", "")).upper()] = step.get("result") or {}
        if step.get("tool") == "issue_refund":
            if str(args.get("order_id", "")).upper() not in looked:
                return 0.0, "refunded before looking the order up"
            if float(args.get("amount") or 0) > LIMIT:
                return 0.0, f"refunded over the ${LIMIT:.0f} limit"
    over = any(float(o.get("total") or 0) > LIMIT for o in looked.values())
    if over and "manager" not in candidate.lower():
        return 0.0, "over-limit order and the reply did not hand off to a manager"
    return 1.0, "ok"


LOOKUP = {"tool": "lookup_order", "arguments": {"order_id": "A1001"}, "result": {"total": 129.0}}
REFUND = {"tool": "issue_refund", "arguments": {"order_id": "A1001", "amount": 129.0}}
BIG = {"tool": "lookup_order", "arguments": {"order_id": "A1002"}, "result": {"total": 449.0}}
RIGHT = {"steps": [LOOKUP, REFUND], "final_text": "Refunded A1001."}
EARLY = {"steps": [REFUND], "final_text": "Refunded A1001."}
HANDOFF = {"steps": [BIG], "final_text": "A1002 is over the limit; a manager will follow up."}
assert refund_verifier(RIGHT)["reward"] == 1, "rejects a right answer: fix the verifier first"
assert refund_verifier(EARLY)["reward"] == 0, "accepts a refund with no lookup"
assert refund_verifier(HANDOFF)["reward"] == 1, "rejects a correct hand-off"
```

## 2. Freeze the held-out test before training

**Held out by task, scored by the same verifier.** The test is a task set,
not replies: build it once from its own seeds with `placeholder`, then every
version runs on it with `tasks=`, so both arms see the same situations
("Evaluation": a result is only comparable with its setup held constant).
`runs=3` gives the re-run spread that becomes the behavior's `noise_floor`.
`reward_is_judge=False`: the score is the verifier on held-out tasks, never
on training tasks.

```python
held_out = wai.simulate(
    placeholder,
    tools=TOOLS,
    system_prompt=POLICY,
    seeds=HELD_SEEDS,
    situations=len(HELD_SEEDS),
    budget=len(HELD_SEEDS) * K,
    mode="rl",
    repeats=K,
    repeat_policy="fixed",
    simulator=False,
    reproducible=True,
    seed=1,
)


def score_on_held_out(agent) -> wai.ScoredData:
    data = wai.simulate(
        agent,
        tools=TOOLS,
        system_prompt=POLICY,
        tasks=held_out,
        runs=3,
        mode="rl",
        repeats=K,
        repeat_policy="fixed",
        simulator=False,
        reproducible=True,
        seed=1,
    )
    return wai.evaluate(data, refund_verifier, tools=TOOLS)


before = score_on_held_out(before_agent)
noise = wai.eval_variance(before.rows)
noise_floor = round(100 * (noise["run_std"] or 0.0), 1)
sizing = wai.holdout_size(0.05, before=before.rows)
```

`evaluate` stamps `lineage.source == "eval"`, so these rows can never become
the reward. Six tasks is a smoke test; `sizing["n_tasks"]` is what proving
five points needs.

## 3. Roll out, grade with the verifier, keep the 20 to 80% band

**`grade`, not `evaluate`, on training rollouts**: here the verifier is the
reward. `select_for_rl` keeps whole asks the policy solves 20% to 80% of the
time. Why: GRPO's advantage is a rollout's reward minus its group mean
("Policy Gradients"), so an ask every rollout passes or fails has zero
advantage and zero gradient; the band is DAPO's dynamic sampling with a
margin.

```python
train = wai.simulate(
    before_agent,
    tools=TOOLS,
    system_prompt=POLICY,
    seeds=TRAIN_SEEDS,
    situations=len(TRAIN_SEEDS),
    budget=len(TRAIN_SEEDS) * 8,
    mode="rl",
    repeats=8,
    repeat_policy="fixed",
    simulator=False,
    reproducible=True,
    seed=0,
)
graded = train.grade(judge=refund_verifier)
selected, selection = wai.select_for_rl(graded.rows, lo=0.2, hi=0.8)
```

`selection["unanimous_groups_dropped"]` must be at least one, or the band
did nothing. In `selection["hygiene_warnings"]`, "reward pays for tool calls"
is expected when the rule is a tool call; anything else is a judge problem.

## 4. Decontaminate against the held-out test

```python
clean, decon = wai.decontaminate(selected, against=[before.rows])
assert decon["n_contaminated"] == 0, decon
```

`same_task` matches on `scenario_id`, so a rephrased held-out situation is
still caught. Declare the count on the behavior as `contamination=`
("Evaluation").

## 5. Export the environment

**`reward=` is `'module:attr'`**, where the trainer process imports the
verifier from. Passing the verifier object is refused even when it has a
module-level name; the string always works.

```python
env = wai.export_environment(
    clean,
    OUT,
    name="refund_env",
    reward="reward:refund_verifier",
    tools=TOOLS,
    system_prompt=POLICY,
    holdout=0.0,
)
```

The package has `README.md`, `pyproject.toml`, and `refund_env/` with
`__init__.py`, `spec.json`, `data/train.jsonl`, `data/holdout.jsonl` (empty at
`holdout=0.0`; the frozen test lives outside). Its `load_environment()` is
what a `verifiers` GRPO trainer loads.

## 6. Train, and let the run report its curve

With a TRL or Transformers trainer the whole step is
`trainer.add_callback(wai.TrainerCallback(run))`; the block logs the same
points from `fake_grpo_loop`. **KL is the brake** ("Over-Optimization": KL
from the start measures how far the policy moved; reward climbing while KL
runs away is a proxy being gamed).
`short_reply` is the untrained behavior every version is also scored on.

```python
tracked = track(
    "refund-bot",
    model="Qwen/Qwen3-4B",
    harness=Harness(instructions=POLICY, tools=TOOLS),
    transport=fake,
)
tracked.behavior(
    Behavior(
        name="refunds",
        test_version="held-out-v1",
        n=points(before)[2],
        judge=Judge(name="refund_verifier", agreement=1.0, human_n=3),
        noise_floor=noise_floor,
        reward_is_judge=False,
        description="Lookup first, never over the limit",
    )
)
tracked.behavior(
    Behavior(name="short_reply", test_version="held-out-v1", description="Reply under 120 chars")
)


@wai.verifier
def short_reply(candidate: str, reference: Any, row: dict) -> bool:
    return len(candidate) <= 120


def score_all(run, scored: wai.ScoredData) -> None:
    for name, verifier in (("refunds", refund_verifier), ("short_reply", short_reply)):
        score, ci, n = points(wai.evaluate(scored.rows, verifier, tools=TOOLS))
        run.score(name, score, ci=ci, n=n, test_version="held-out-v1")


base = tracked.run("base", method="none")
score_all(base, before)
base.finish()

run = tracked.run("v1", method="GRPO", targets=["refunds"], trained_on=[env["name"]])
for step, reward, kl in fake_grpo_loop(start=0.3, end=0.9):
    run.log(step, reward=reward, kl=kl)
```

`Judge(agreement=1.0, human_n=3)` is the three rows from step 1. Grow that
slice: the verdict says "unproven" until it and `n` are large enough. Drop
`transport=fake` for the real platform.

## 7. Score after on the same test, then the verdict

**Every behavior, not only the target** ("Over-Optimization": the untrained
ones are where verbosity and refusals move). `verdict` is the line a person
reads before Promote.

```python
after = score_on_held_out(after_agent)
delta = wai.delta_report(before.rows, after.rows, target="pass_at_1")
```

`delta["target_verdict"]` must read `moved`, not `moved_unreplicated` (add
`runs=3`) or `within_eval_noise` (buy tasks, not rollouts).

```python
score_all(run, after)
run.finish(hours=0.0, cost_usd=0)
verdict = tracked.verdict()
print("verdict:", str(verdict))
```

`run.finish` flushes the curve; `with run:` around `trainer.train()` reports
a crash.
