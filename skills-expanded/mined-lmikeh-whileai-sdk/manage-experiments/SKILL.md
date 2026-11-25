---
name: manage-experiments
description: >
  How a coding agent tells the person what it did, why the number moved and
  how to run it again, so the platform page reads in one look. Use before
  posting a second version, a sweep, a replicate or a training run to
  while.ai/platform: the question first, then for every run five
  lines (Changed, Moved, Why, Learned, Reproduce), one picture, the rows that
  failed, points not fractions, and readback(tracked) to read the account
  the way a teammate will. No GPU, no key until the report.
metadata:
  version: "2.1.0"
---

# Manage experiments

You know the repo; the person reading the page does not have your context.
They read for two reasons: to learn what a paper or an idea does when
tried, and to find a behavior and fix it fast at work. Both want one
look: what changed, did it move, why, what it taught, and can I run it
again. On 2026-09-20 real agents posted `dapo-lr5e-05-s17-30st` nineteen
times, no note on any run, no picture, a `0.75` on a page that counts
points, and no question on six agents of seven. Every page was correct
and said nothing. Every step below is in `check.py`, which runs offline
in under a second; its setup defines `MODEL`, `OPEN_MODEL`, `TOOLS`,
`POLICY`, `PROMPT_POLICY`, `DATES_LINE`, `PROMPT_DATES`, `ASKS`, `NOISE`,
`STEPS`, `CHECKPOINT_EVERY`, `score_on`, `score_checkpoint`,
`train_reward`, `worst_of` (20 rows, failures first) and `fake`.
Names follow [platform/naming](https://docs.while.ai/platform/naming);
that part is easy.

## 1. The question, before the first run

One agent per product, one question at a time, at the top of the page.

```python
tracked = track("checkout-support", model=MODEL, transport=fake)  # drop transport= for real
tracked.experiment(
    question="Does telling the prompt today's date cut wrong refunds on old orders?",
    hypothesis="Most wrong refunds are orders past 30 days; a dated rule removes them.",
    method="Same asks, same judge. Harness: two prompts on one model. Training: SFT on traces.",
    measure="refunds_when_eligible on the frozen test, points out of 100, 95% interval.",
    decide="Promote the version whose interval clears the served one and the noise floor.",
)
```

## 2. One frozen test, named by its content, with what you measured

```python
TEST = "t-" + hashlib.sha256("\n".join(ASKS).encode()).hexdigest()[:8]
tracked.behavior(
    Behavior(
        name="refunds_when_eligible",
        test_version=TEST,
        n=len(ASKS),
        judge=Judge(name="refund policy as a program", agreement=0.93, human_n=60),
        noise_floor=NOISE,
        contamination=0,
        reward_is_judge=False,
        rubric=POLICY,
        description="Refunds delivered orders within 30 days; escalates over $200; else denies.",
    )
)
```

## 3. Harness: say why it moved

Score both prompts on the same test, then say which asks flipped. "Why"
is the flipped asks, not an adjective. The note has five lines a person
reads in order: Changed is the fix someone can copy, Why is the behavior it
fixed, Learned closes the hypothesis in one sentence and names the paper
when the run tried one. The picture is one bar per arm with its interval.

```python
def flips(before: list[Example], after: list[Example]) -> tuple[list[str], list[str]]:
    """Which asks changed answer between two scorings of the same test."""
    was = {e.prompt: e.ok for e in before}
    fixed = [e.prompt for e in after if e.ok and not was[e.prompt]]
    broke = [e.prompt for e in after if not e.ok and was[e.prompt]]
    return fixed, broke


ARMS = {"policy": PROMPT_POLICY, "policy+dates": PROMPT_DATES}
scored = {}
for arm, prompt in ARMS.items():
    run = tracked.run(
        arm,
        method="eval",
        harness=Harness(label=f"{arm}@{MODEL}", model=MODEL, instructions=prompt, tools=TOOLS),
        targets=["refunds_when_eligible"],
        record=RunRecord(data=Data(holdout=TEST, n_holdout=len(ASKS)), optimizer=Optimizer(seed=1)),
    )
    score, ci, examples = score_on(prompt, seed=1)
    run.score("refunds_when_eligible", score, ci=ci, n=len(ASKS), examples=worst_of(examples))
    scored[arm] = (run, score, ci, examples)

(base_run, base, base_ci, base_rows), (new_run, new, new_ci, new_rows) = scored.values()
fixed, broke = flips(base_rows, new_rows)
base_run.note("Served prompt, seed 1. Misses are refunds of orders older than 30 days.")
new_run.note(
    f"Changed: one line, '{DATES_LINE}'\n"
    f"Moved: {base} to {new} points (±{new_ci}) on {len(ASKS)} asks.\n"
    f"Why: {len(fixed)} asks now pass, every one an order older than 30 days; {len(broke)} broke.\n"
    f"Learned: the model knew the rule but not the date; giving it the date beat rewriting the rule.\n"
    f"Reproduce: seed 1, test {TEST}, uv run python evals/run.py --prompt policy+dates"
)
tracked.figure(
    "harness",
    {
        "data": [
            {
                "type": "bar",
                "x": list(scored),
                "y": [s[1] for s in scored.values()],
                "error_y": {"type": "data", "array": [s[2] for s in scored.values()]},
            }
        ],
        "layout": {
            "title": "refunds_when_eligible, points out of 100",
            "yaxis": {"range": [0, 100]},
        },
    },
    caption=f"The dates line fixes {len(fixed)} asks and breaks {len(broke)}.",
    run=new_run,
)
for r in (base_run, new_run):
    r.finish(say=False)
```

## 4. Training: say why it moved, and whether to believe it

Log the reward every step and score the frozen test at checkpoints. The
picture is both lines on one chart: reward left, held-out right. The
sentence that matters is whether they rose together. A reward that climbs
while the held-out line stays flat is the judge being gamed
(rlhfbook.com, "Over-Optimization"); say so in the note rather than let
the person find out. The record carries what a rerun needs: data, seed,
learning rate, pins; the note carries the command.

```python
run = tracked.run(
    "dates-sft",
    method="SFT",
    base=OPEN_MODEL,
    targets=["refunds_when_eligible"],
    trained_on=["refund traces 2026-09"],
    record=RunRecord(
        data=Data(train="refund traces 2026-09", n_train=800, holdout=TEST, n_holdout=len(ASKS)),
        optimizer=Optimizer(lr=1e-5, seed=17),
        provenance=Provenance(pins={"trl": "1.13.0", "transformers": "5.17.0"}),
    ),
)
steps, rewards, held = [], [], []
for step in range(1, STEPS + 1):
    reward = train_reward(step)  # what the trainer logged at this step
    run.log(step, reward=reward)
    steps.append(step)
    rewards.append(reward)
    if step % CHECKPOINT_EVERY == 0:
        score, ci, rows = score_checkpoint(step)  # the frozen test on this checkpoint
        held.append((step, score, ci, rows))
        run.score("refunds_when_eligible", score, ci=ci, n=len(ASKS), examples=worst_of(rows))
first, last = held[0], held[-1]
fixed, broke = flips(base_rows, last[3])
together = last[1] - first[1] > NOISE  # held-out moved with the reward, or only the reward did
run.note(
    f"Changed: SFT on 800 refund traces, lr 1e-5, seed 17, {STEPS} steps.\n"
    f"Moved: reward {rewards[0]} to {rewards[-1]}; held-out {base} to {last[1]} points (±{last[2]}).\n"
    + (
        f"Why: {len(fixed)} asks now pass, every one an old order; {len(broke)} broke. "
        "Reward and held-out rose together, so the judge is not being gamed.\n"
        if together
        else "Why: reward rose but held-out did not. Treat as reward hacking until shown otherwise.\n"
    )
    + "Learned: 800 traces taught one rule; the held-out checkpoints are the proof, the reward is not "
    "(rlhfbook.com, Over-Optimization).\n"
    + "Reproduce: uv run python train.py --seed 17 (pins in the record)"
)
tracked.figure(
    "training",
    {
        "data": [
            {"type": "scatter", "name": "reward", "x": steps, "y": rewards},
            {
                "type": "scatter",
                "name": "held-out, points",
                "x": [h[0] for h in held],
                "y": [h[1] for h in held],
                "yaxis": "y2",
                "mode": "lines+markers",
            },
        ],
        "layout": {
            "title": "dates-sft: reward per step and the frozen test at checkpoints",
            "yaxis": {"title": "reward"},
            "yaxis2": {"title": "held-out", "overlaying": "y", "side": "right", "range": [0, 100]},
        },
    },
    caption="Held-out rises with the reward; a flat held-out line under a rising reward is hacking.",
    run=run,
)
run.finish(hours=0.4, gpu="A10G", cost_usd=0.5, say=False)
```

Sweeps are the same five lines per arm. Name the arm by the one thing it
changes, in words; the page reads the axes from `record.optimizer` and
`record.data` and folds seeds into one arm, so a version like
`dapo-lr5e-05-s17-30st` adds nothing a person can read. Try wide: a
different reward, a different data mix, a different base. Each arm is
cheap to explain when the four lines are the template.

## 5. Read it back as the person will

Before you say the page is ready, read it the way they will. One line per
problem, with the call that fixes it. Every fix is a `PATCH` from any
session: `tracked.open(run_id).note(...)`, `tracked.figure(...)`,
`tracked.behavior(...)` again.

```python
SETTING = re.compile(r"(lr\d|\de-0\d|-s\d+\b|_s\d+$|_seed\d+|^h-[0-9a-f]{12}$|^v\d+$)")


def readback(tracked) -> list[str]:
    """What a teammate opening the page could not read. Empty means clean."""
    out = []
    if tracked.experiment() is None:
        out.append("no question posted: tracked.experiment(question=...)")
    for b in tracked.behaviors():
        if SETTING.search(b.name):
            out.append(f"behavior {b.name!r} names a seed or setting; put it in Optimizer(seed=)")
        if not (b.test_version or "").startswith("t-"):
            out.append(f"behavior {b.name!r}: test_version is not the asks' hash")
    pictured = {f.run for f in tracked.figures()}
    for r in tracked.runs():
        v, note = r["version"], r.get("notes") or ""
        trained = r.get("method") not in (None, "none", "eval")
        if SETTING.search(v):
            out.append(f"version {v!r} encodes settings; say the arm in words, numbers in record")
        if not ((r.get("record") or {}).get("data") or {}):
            out.append(f"run {v!r}: no data posted; RunRecord(data=Data(...))")
        for word in ("Changed", "Moved", "Why", "Learned", "Reproduce"):
            if trained and f"{word}:" not in note:
                out.append(f"run {v!r}: note has no '{word}:' line; run.note(...)")
        if trained and r["id"] not in pictured:
            out.append(f"run {v!r}: no picture; tracked.figure(name, fig, run=run)")
        for e in r.get("evals") or []:
            if 0 < e["score"] < 1:
                out.append(
                    f"{v} {e['behavior']}: {e['score']} reads as a fraction; post points, or fraction=True"
                )
    return out


for problem in readback(tracked):
    print("fix:", problem)
```

## 6. Report in sentences, archive the noise

The brief and the verdict are the sentences the page shows, from the same
rows; paste them in the pull request. A wrong launch, a dead arm, a
duplicate: archive, never delete.

```python
print(tracked.brief())
print(tracked.verdict())

dup = tracked.run("dates-sft", method="SFT", base=OPEN_MODEL)  # launched twice by mistake
tracked.archive(dup.id)  # a wrong launch or a dead arm: archive, never delete
```

## What the person sees

The question. One chart per run with the interval on it. Under each run,
five lines: Changed, Moved, Why, Learned, Reproduce. Under each score, the asks
that failed and why. A brief that says whether the change is real and
what to run next. No number without a sentence, no sentence without a
number.
