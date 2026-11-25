---
name: pick-a-method
description: >
  Pick the training method from the graded rows before spending a GPU, out
  of everything the SDK ships: the hosted sft/grpo/dpo/rm, and on your own
  GPUs OPSD, OPD, GroupwiseGrading (GRS/GAR), Async, FlashReinforce, SAO,
  BPCO, ReinforceAda and prime-rl's grpo/max_rl/rae. Use when a coding
  agent has scored a model and must choose a method or its knobs, when a
  base scores zero everywhere, when every task already passes, when rows
  come one per prompt, when rows came from another model, or when someone
  proposes distilling from a bigger teacher.
metadata:
  version: "2.0.0"
---

# Pick a method from the graded rows

The hosted trainer knows four methods (`sft`, `grpo`, `dpo`, `rm`).
`whileai.methods` ships about ten more for your own GPUs, and nothing in
`train` points at them. Don't route from the hosted menu. Ask the rows six
questions, in order, and stop at the first one that decides.

`check.py` runs every block below offline. Names it defines: `MODEL` (the
model you will train), `TASKSET`, `TEACHER` (a `wai.Endpoint`), `grader`
(a program standing in for the judge), and graded rows, each with
`task_id`, `reward`, `truncated` and `model`: `mixed_rows`, `floor_rows`,
`saturated_rows`, `one_per_prompt`, `teacher_made_rows`, `cut_off_rows`,
`student_rows`, `weak_teacher_rows`, `strong_teacher_rows`.

## What there is to pick from

| layer | options | where it runs |
|---|---|---|
| hosted | `sft`, `grpo`, `dpo`, `rm` | `wai.train` |
| prime-rl base | `grpo`, `max_rl`, `rae` | `wai.prime_rl_config(env, "rae", model=)` |
| distillation | `wai.OPD(teacher)`, `wai.OPSD(privileged=)` | `prime_rl_config` |
| ranks the passes | `wai.GroupwiseGrading(grader, mode="reward" \| "advantage")` | your trainer |
| stale sampler | `wai.Async(method, correction=)` wraps `grpo`, `max_rl`, `rae`, `OPD` or `OPSD` | `prime_rl_config` |
| one rollout per prompt | `wai.FlashReinforce`, `wai.SAO`, `wai.BPCO` | your trainer, `.update(batch)` |
| adaptive sampling | `wai.methods.ReinforceAda` | before a grouped update |

The equations, defaults and papers for every row are in the methods
reference: https://docs.while.ai/reference/methods (`docs/reference/methods.md`).

**They compose.** `Async("grpo", correction="icepop")` is one config;
`GroupwiseGrading` shapes a grouped method's reward or advantage. **Read
`cfg.ignored` on every config**: prime-rl drops some knobs and says why.

## 0. The grader first

A program that decides the task beats any judge. If it needs a judge, run
`audit-your-judge/` before trusting any number below: every split rate and
pass rate here is only as good as the grader that produced it.

## 1. Can a cut-off reply pass?

A reply cut at the token cap can land a keyword and score. Then truncation,
not the model, decides every rate below. Don't score truncated completions;
DAPO penalizes over-long samples for this reason (Lambert 2025, chapter
Reinforcement Learning).

```python
def truncated_passes(rows) -> int:
    return sum(1 for r in rows if r.get("truncated") and r["reward"] >= 1.0)
```

Any count above zero: stop and fix the reward (a truncated reply fails, or
raise `max_tokens`) before you read anything else.

## 2. How many rollouts per prompt?

GRPO's advantage is a reward minus its group's mean, which is zero in a
group of one (Lambert 2025, chapter Reinforcement Learning). Production
traces arrive one per prompt.

```python
def rollouts_per_task(rows) -> int:
    return min(Counter(r["task_id"] for r in rows).values())
```

**`k = 1`**: no grouped method. Use `FlashReinforce` (baseline from the
batch; Hu et al. 2026), `SAO` (a critic plus a token band; Hou et al.
2026) or `BPCO` (a bounded critic; Qi et al. 2026). The class docstrings
carry the papers. Each takes a batch and returns per-token coefficients for
your own loss. On prime-rl the option is `rae`, an EMA baseline; prime-rl
refuses the three above.

```python
batch = [
    {"reward": 1.0, "logprobs": [-0.5, -1.2, -0.3]},
    {"reward": 0.0, "logprobs": [-0.7, -0.4]},
]
update = wai.FlashReinforce().update(batch)
print(update.advantages, update.notes)
cfg = wai.prime_rl_config(TASKSET, "rae", model=MODEL)  # prime-rl's k=1 option
```

If you can re-run the prompts, re-running at `k >= 4` is usually the
cheaper fix.

## 3. What is the per-task band?

Never read the mean. Per task, a prompt passes always, fails always, or is
split. Only split tasks give a grouped method gradient; all-0 and all-1
groups carry no signal (DAPO dynamic sampling; Lambert 2025, chapter
Reinforcement Learning). A task at pass rate `p` is split with probability
`1 - p**k - (1-p)**k`, so raising `k` buys split tasks only where `p` is
between 0 and 1. **Measure `p` on the model you will train**, not on a
closed model you used to write the data: a band read off a stronger model
predicts split tasks the student will never produce.

```python
def band(rows) -> str:
    rates = list(pass_at(rows).per_task.values())
    if all(r == 0.0 for r in rates):
        return "floor"
    if all(r == 1.0 for r in rates):
        return "saturated"
    return "mixed"


def split_share(rows) -> float:
    rates = list(pass_at(rows).per_task.values())
    return sum(1 for r in rates if 0.0 < r < 1.0) / len(rates)
```

**Floor: every task fails.** Rejection sampling trains only on what it
keeps (Lambert 2025, chapter Rejection Sampling), and `k` draws keep one
with probability `1 - (1 - p) ** k`, which is 0 at `p=0`. More rollouts do
nothing. OPSD gives the model privileged context (Zhao et al. 2026,
arXiv:2601.18734; Lambert 2025, chapter Synthetic Data and Distillation):

```python
cfg = wai.prime_rl_config(TASKSET, wai.OPSD(privileged="reference"), model=MODEL)
print(cfg.method, cfg.command)
print(cfg.ignored)  # knobs prime-rl will not read, and why
print(cfg.warnings)
```

Pick the `privileged=` the task actually has: `reference` (the answer),
`demonstration` (a passing rollout), `hint`, or `feedback` (the
environment's error). Each is a different paper (see the `OPSD`
docstring). OPSD needs about 7B or more; in the repo's own run
(`recipes/04-train/prime-rl/results.json`, Qwen3-0.6B) it came out
**-0.554 [-0.614, -0.495]** against GRPO on 128 paired tasks. Under 7B,
use SFT on a stronger model's completions (`sft-from-traces/`).

**Saturated: every task passes.** Binary reward makes every pass equal.
If the passes really differ in quality (multi-turn agent work, not
one-line answers), `GroupwiseGrading` ranks them: `mode="reward"` is GRS,
`mode="advantage"` is GAR (MiMo-V2.6 2026, section 4.3). Audit its grader
first (`audit-your-judge/`). If no grader can tell the passes apart, the
eval is too easy: harden it (`strengthen-your-evals/`).

```python
method = wai.GroupwiseGrading(grader=grader, mode="reward")
```

**Few split tasks.** `wai.methods.ReinforceAda` keeps sampling a prompt
until it has both a pass and a fail (arXiv:2510.04996). In the repo's
`recipes/papers/talk-methods` it was flat against GRPO at three seeds, so
treat it as an experiment, not a default.

## 4. Did the model you'll train write these rows?

GRPO on rows another model sampled, with no importance ratio, is an
off-policy update with no correction (Lambert 2025, chapter Reinforcement
Learning). `selection_report` can't see this; compare the model yourself.

```python
def on_policy(rows, model: str) -> bool:
    return all(r.get("model") == model for r in rows)
```

Rows from another model: train SFT on them, or use that model as an OPD
teacher. Rows from an older copy of this model (an async sampler): wrap
the method in `Async` with a per-token correction. prime-rl offers `ipo`
and `icepop`; `tis` is verl's.

```python
cfg = wai.prime_rl_config(TASKSET, wai.Async("grpo", correction="icepop"), model=MODEL)
print(cfg.method, cfg.config["orchestrator"]["algo"])
```

## 5. Is there a stronger teacher?

OPD's per-token advantage is `log pi_T - log pi_theta` (Lambert 2025,
chapter Synthetic Data and Distillation, eq. 10). It pulls the student
toward the teacher, so a teacher no better than the student has nothing to
give. Score both on the same held-out rows with an audited judge. The
teacher must clear `PROVE_EFFECT` (0.05) with intervals that don't overlap:
engineering, not a result from the book. Score the teacher at the
student's `max_tokens`: a teacher that only wins with a longer budget
will be cut off inside the OPD run, and its truncated replies teach the
student to run to the cap.

```python
def teacher_clears(teacher_rows, student_rows) -> bool:
    t, s = pass_at(teacher_rows), pass_at(student_rows)
    gap = t.pass_at_1 - s.pass_at_1
    apart = t.ci95[0] > s.ci95[1]  # intervals do not overlap
    print(f"teacher {t.pass_at_1:.3f} {t.ci95}  student {s.pass_at_1:.3f} {s.ci95}")
    return gap >= PROVE_EFFECT and apart
```

Distillation also needs one tokenizer, since the supervision is per token
(Lambert 2025, chapter Synthetic Data and Distillation); a mismatch drops
the signal silently (SimCT, arXiv:2605.07711). `prime_rl_config` doesn't
check it:

```python
teacher_vocab, student_vocab = 151_936, 151_936  # each tokenizer's len(tokenizer)
assert teacher_vocab == student_vocab, "OPD needs one tokenizer: pick a same-family teacher"
cfg = wai.prime_rl_config(TASKSET, wai.OPD(TEACHER), model=MODEL)
print(cfg.method, cfg.command)
```

Don't pick OPD for cost alone. In the repo's run it matched GRPO
(**+0.028 [+0.013, +0.045]**, inside that run's noise) in about the same
wall clock (894 s against 884 s).

## 6. The route, end to end

```python
def route(rows, model: str, teacher_rows=None) -> str:
    if truncated_passes(rows):
        return "fix the reward: a cut-off reply passes"
    if rollouts_per_task(rows) == 1:
        return "FlashReinforce / SAO / BPCO, or prime-rl rae"
    where = band(rows)
    if where == "floor":
        return "OPSD"
    if where == "saturated":
        return "GroupwiseGrading, or a harder eval"
    if teacher_rows is not None and teacher_clears(teacher_rows, rows):
        return "OPD"
    if not on_policy(rows, model):
        return "SFT on these rows, or OPD from their model"
    return "GRPO"
```

| route | trains with |
|---|---|
| fix the reward | nothing yet |
| k = 1 | `FlashReinforce` / `SAO` / `BPCO` in your trainer, or prime-rl `rae` |
| floor | `OPSD`, or SFT from a stronger model under 7B (`sft-from-traces/`) |
| saturated | `GroupwiseGrading`, or a harder eval (`strengthen-your-evals/`) |
| strong teacher, same tokenizer | `OPD` |
| another model's rows | SFT (`sft-from-traces/`), or `OPD` from that model |
| a natural better/worse pair per prompt | DPO (`dpo-pairs/`; Lambert 2025, chapter Direct Alignment) |
| split tasks, on-policy, program grader | GRPO (`grpo-verifier/`) |

`rm` is rarely the answer: where a program can check the task, the
program is the reward.

## 7. Before the GPU: size it and run the control

Size the held-out test with `holdout_size(effect, k=)`. Size what you
select from too; the SDK has no call for it, so work it out the same way.
Train a random selection of the same size beside the real one. If the
method doesn't beat its own random control, the selection or the reward
was the problem, not the optimizer. On a Qwen 2.5 or 3 base, add a
random-reward arm too: gains under random rewards signal base-model
contamination (Lambert 2025, chapter Evaluation). Then finish the way every skill does
(`skills/README.md`): frozen test, noise floor, every behavior, `track`.
