---
name: character
description: >
  Train how a model talks from a constitution (a model spec) and prove the
  trait moved without costing anything else. Use when asked to give an agent a
  character, persona or voice that survives without a system prompt, to turn a
  model spec or list of principles into training data, to build DPO pairs or
  SFT rows for style, or to measure a trait before and after training. The
  judge is checked against the spec's own labeled replies before any pass rate
  is read; every trait is a Behavior on the platform, plus a control for what
  must not regress.
metadata:
  version: "1.0.0"
---

# Character from a constitution

A constitution is a list of principles with labeled examples. This skill turns
it into graded rows, checks the judge, builds the training rows, and measures
each trait before and after on frozen held-out prompts. The pipeline is the one
Maiya et al. 2025 open-sourced: traits, prompts that exercise each trait,
several replies per prompt, a judge that reads the principle, then preference
pairs and SFT rows. Worked example with the OpenAI Model Spec:
`recipes/03-select/character/`.

`check.py` runs all of it offline. Names it defines that the blocks below use:
`CONSTITUTION` (three traits, four situations each, one GOOD and two BAD
replies per situation), `build_tasks` (one task per wording of each situation,
split train/held-out by situation hash), `sample_rows` (a scripted student
that replays the spec's replies at a fixed rate; `after=True` plays a student
that landed the training), `K` replies per prompt, `TASKS_BY_ID`, `grade`
(`wai.run_judge` with a lookup judge that reads `privileged.principle`, then
the markers `trait`, `on_task`, `no_filler`), `spec_rows` (the spec's own
replies with `gold_reward` and `gold_kind="human"`), `behavior_score` (points,
95% half-width, n from `wai.marker_summary`), `noise_floor` (re-run std in
points from `wai.eval_variance`), `fake` (a recording transport that answers
like the platform). Live, the student is a model sampled under the deployment
prompt only (`You are Sol, an assistant.`, no constitution) and the judge is
an LLM from a different family with the principle in its system prompt.

## 1. The constitution is a versioned object

**Load it; the version is a content hash.** `wai.load_spec` takes the dict
shape `{"id", "source", "traits": [{"id", "name", "authority", "principle",
"examples": [{"prompt", "good", "bad"}]}]}` or a path, and `spec.version`
changes on any edit to a principle. Every trait becomes one `Behavior`, plus
`control` for the plain tasks the persona must not distort. Versioning the
spec is engineering, not research: it is how you tell an edit to the spec from
a change in the model.

```python
spec = wai.load_spec(CONSTITUTION)
assert len(spec.traits) == 3 and len(spec.version) == 12, spec
edited = wai.load_spec({**CONSTITUTION, "traits": CONSTITUTION["traits"][:2]})
assert edited.version != spec.version, "an edit to the spec must change its version"
behaviors = [*spec.behaviors(), "control"]
print(f"spec {spec.id}@{spec.version} traits {spec.behaviors()} + control")
```

## 2. Prompts that exercise each trait, several replies each

**Sample under the deployment prompt only.** If the constitution is in the
prompt at sampling time you are measuring prompting, not character (Maiya et
al. 2025 train the student without it and use a constitution-prompted teacher
only for the chosen side). Several wordings of one ask keep the judge on the
trait, not the phrasing. Stamp the rows with `wai.stamp_spec` before grading
so every row, pair and SFT row carries `spec_version`.

```python
tasks = build_tasks(spec)
TASKS_BY_ID.update({t["task_id"]: t for t in tasks})
train_tasks = [t for t in tasks if t["split"] == "train"]
held_tasks = [t for t in tasks if t["split"] == "holdout"]
shared = {t["prompt"] for t in train_tasks} & {t["prompt"] for t in held_tasks}
assert not shared, f"held-out shares prompts with training; split by situation: {shared}"
train = grade(wai.stamp_spec(sample_rows(train_tasks), spec), spec)
assert all(r["spec_version"] == spec.version for r in train), "stamp_spec before grading"
print(
    f"train {len(train_tasks)} prompts x {K} = {len(train)} rows; held-out {len(held_tasks)} prompts"
)
```

## 3. Check the judge before reading a pass rate

**Grade the spec's own GOOD and BAD replies with the same judge.** rlhfbook.com,
"Evaluation": a judge is only as good as its agreement with people on a labeled
slice. The spec's authors are the people, so the check is free.
`wai.judge_agreement` needs `gold_reward` and `gold_kind="human"` on the rows;
`ok` is false otherwise. Below 0.8, fix the judge prompt or use a stronger
judge before reading anything else. Record the number on the `Behavior` as
`Judge(agreement=..., human_n=...)`; the verdict says "unproven" without it.
Offline the lookup judge scores 1.00 by construction; live, this line is where
a lenient judge shows (Phi-4 passed half the spec's BAD replies in the recipe).

```python
labeled = grade(spec_rows(spec, tasks), spec)
agree = wai.judge_agreement(labeled)
assert agree["ok"] and agree["n"] == len(labeled), agree["warnings"]
assert agree["agreement"] >= 0.8, f"fix the judge before reading pass rates: {agree}"
judge = Judge(name="spec-lookup", agreement=agree["agreement"], human_n=agree["n"])
print(
    f"judge vs spec labels: agreement {agree['agreement']:.2f} kappa {agree['kappa']:.2f} n={agree['n']}"
)
for trait in spec.traits:
    pa = wai.pass_at([r for r in train if r["trait"] == trait.id])
    print(
        f"  {trait.id:<18} pass@1 {pa.pass_at_1:.2f} headroom {pa.headroom:.2f} ({pa.n_groups} prompts)"
    )
```

A trait at pass@1 of 0.00 or 1.00 yields no pairs. Write harder or easier
prompts for it, or use a teacher for the chosen side.

## 4. Frozen held-out prompts per trait, noise floor recorded

**Hold out by situation, then measure the eval's own spread.** rlhfbook.com,
"Evaluation": keep train and held-out apart, and expect the same setup to move
between runs. `wai.decontaminate` confirms no training prompt covers a held-out
one. Three re-runs of the untrained student give `run_std` per metric; that
mapping goes to `delta_report(run_std=, run_std_runs=)`, so the band uses the
t quantile at `n_runs - 1` (the floor is an estimate, not the spread), and, in
points, to `Behavior(noise_floor=)`.

```python
before = wai.stamp_spec(grade(sample_rows(held_tasks), spec), spec)
_, decon = wai.decontaminate(train, [before])
assert decon["n_contaminated"] == 0, f"training rows overlap the held-out set: {decon}"
reruns = [grade(sample_rows(held_tasks, seed=s), spec) for s in (1, 2, 3)]
noise = wai.eval_variance(*reruns, metric="marker:trait")
floors = {name: noise_floor(reruns, name) for name in behaviors}
print(f"held-out re-run std marker:trait {noise['run_std']:.3f}; floors (points) {floors}")
```

## 5. Training rows: pairs and SFT, stamped with the spec version

**Pairs need contrast; SFT needs passes.** `wai.build_preference_pairs` pairs a
GOOD reply with a BAD one on the same prompt (rlhfbook.com, "Direct
Alignment"); `length_match=True` picks the rejected reply closest in length,
and `report["length"]["chosen_longer_frac"]` says how often chosen is still
longer. A trainer learns a length gap before it learns the behavior, so above
about 0.6 write BAD replies of comparable length or accept that the run
teaches length too. `wai.select_for_sft` keeps the top reply per prompt
(rlhfbook.com, "Rejection Sampling"). Both inherit `spec_version` from the
stamped rows.

```python
pairs, pair_report = wai.build_preference_pairs(train, length_match=True)
longer = pair_report["length"]["chosen_longer_frac"]
assert pairs and longer is not None, pair_report
sft, sft_report = wai.select_for_sft(train, target=200)
assert sft and all(r["reward"] == 1 and r["spec_version"] == spec.version for r in sft)
assert all(p["chosen"]["spec_version"] == spec.version for p in pairs)
print(f"pairs {len(pairs)} (chosen longer {longer}) | sft {len(sft)} | {pair_report['warnings']}")
```

Train with `wai.train(dataset_id, method="dpo")` on the pushed pairs, or
`wai.export_preference(pairs, "pairs.jsonl", system_prompt=DEPLOY_PROMPT)` for
a trainer of your own.

## 6. Before and after on the held-out prompts, with the guard

**The headline is the trait; the guard is everything else.** rlhfbook.com,
"Over-Optimization": training on one thing moves the things you did not train.
`must_not_regress=["on_task", "no_filler"]` fails the report if a warm reply
stops answering or the filler comes back; a reply that has the character and
drops the task is a 0. `target="marker:trait"` makes the trait delta the
verdict, with a bootstrap interval over paired tasks and the re-run band from
step 4. `ok` false means do not ship, whatever the trait did.

```python
after = wai.stamp_spec(grade(sample_rows(held_tasks, after=True), spec), spec)
delta = wai.delta_report(
    before,
    after,
    target="marker:trait",
    must_not_regress=["on_task", "no_filler"],
    run_std=noise["run_std_by_metric"],
    run_std_runs=noise["n_runs"],
)
print(wai.format_delta_report(delta))
assert delta["ok"], f"a guarded metric slipped; do not ship v1: {delta.get('warnings')}"
assert behavior_score(after, "control")[0] >= behavior_score(before, "control")[0]
```

## 7. Report every behavior, then read the verdict

**One `Behavior` per trait plus `control`; score all of them on both versions.**
rlhfbook.com, "Evaluation": one evaluation is one draw, the interval is the
result. `base` is scored so the platform has a served version to compare
against; `v1` names the traits it trained as `targets` and the pairs as
`trained_on`. `reward_is_judge=False` holds for a lookup against labels; with
an LLM judge that also built the pairs, set it `True` or score with a second
judge. Live, drop `transport=fake` and set `WHILEAI_API_KEY`.

```python
tracked = track("sol-character", model="scripted:sol-base", transport=fake)
for trait in spec.traits:
    tracked.behavior(
        Behavior(
            name=trait.id,
            test_version=f"heldout@{spec.version}",
            n=behavior_score(before, trait.id)[2],
            judge=judge,
            noise_floor=floors[trait.id],
            contamination=decon["n_contaminated"],
            reward_is_judge=False,
            description=trait.principle,
        )
    )
tracked.behavior(
    Behavior(
        name="control",
        test_version=f"heldout@{spec.version}",
        n=behavior_score(before, "control")[2],
        noise_floor=floors["control"],
        description="Plain tasks the persona must not distort; scored on on_task.",
    )
)
base = tracked.run("base", method="none", targets=[], trained_on=[])
for name in behaviors:
    score, ci, n = behavior_score(before, name)
    base.score(name, score, ci=ci, n=n, test_version=f"heldout@{spec.version}")
base.finish()
run = tracked.run(
    "v1", method="DPO", targets=spec.behaviors(), trained_on=[f"sol-pairs@{spec.version}"]
)
for name in behaviors:
    score, ci, n = behavior_score(after, name)
    run.score(name, score, ci=ci, n=n, test_version=f"heldout@{spec.version}")
run.finish()
for name in behaviors:
    print(str(tracked.verdict(name)))
verdict = str(tracked.verdict())
print(verdict)
```

The verdict names both versions and what it rests on:
`be_direct: v1 beats base by 48 (interval excludes zero, clears the noise
floor of 5.8); judge agreement 1 on 36, n=50` and
`control: v1 about the same as base (+0, interval includes zero); n=50`.
"unproven:" in front means n under 50, judge agreement missing or under 0.8,
the reward is the judge, or contamination; each names its fix.

## Not here

Maiya's introspection stage (the trained model writing about its own values)
needs the trained model; run it after DPO with the same judge. The recipe adds
a "drop the act" suffix to the held-out prompts as a robustness test; add it
when the persona must survive being told to stop.
