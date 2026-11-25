---
name: watch
description: >
  Keep the platform's Live tile honest with one command a day, without the
  platform ever ingesting a trace. Use when an agent is served and someone
  asks "is it still fine in production", when the Live tile is empty or stale,
  when a served version needs a flagged rate that means the same thing as its
  held-out score, or when deciding whether a rise in failures is real enough
  to open a new run. Covers reading yesterday's traces, a date-seeded sample
  scored by the held-out judge, posting one LiveDay, the two-day drift rule
  against the behavior's noise floor, and scheduling.
metadata:
  version: "1.0.0"
---

# Watch the served version

The held-out score says what a version can do. The Live tile says whether that
survived real traffic (`LiveDay`: the flagged rate over time is the only number
that does). Traces never leave your side: you read them, you score a sample
with the same judge the held-out test uses, and you post one row per day.

Names in the blocks below come from `check.py`: `served_bot` is the scripted
agent as served (v3), `refund_judge` is the held-out judge (a program),
`TOOLS`, `ASKS`, `URGENT_ASKS`, `OIDS` define its world, `trace_path(day)`
says where a day's export lives, and `fake` is the offline transport.

## 0. Declare the behavior and score the served version once

The daily job compares against two numbers the platform already holds: the
behavior's `noise_floor` and the served version's held-out score. Declare
the first; post the second once per served version. The judge here is the
one the held-out test uses; the sample is scored by the same function.

```python
tracked = track("refund-bot", model="Qwen/Qwen3-4B", transport=fake)  # drop transport= for real
tracked.behavior(
    Behavior(
        name="refunds",
        test_version="v1",
        judge=Judge(name="refund policy as a program"),
        noise_floor=2.0,  # points; the re-run spread you measured on this test
        reward_is_judge=False,
        description="Looks the order up, refunds only when policy allows, escalates over-limit.",
    )
)

HELDOUT = [a.format(oid=o) for a in ASKS for o in OIDS] + [
    a.format(oid="A1001") for a in URGENT_ASKS
]  # frozen, test_version v1


def score_served(version: str) -> float:
    """The served version on the frozen held-out test, with the same judge.
    The tile needs this once per version so day one has a baseline."""
    rows = [{"prompt": p, **served_bot(p), "task_id": p} for p in HELDOUT]
    scored = wai.evaluate(rows, refund_judge, tools=TOOLS)
    n, passed = len(scored.rows), len(scored.passes())
    score = round(100 * passed / n, 1)
    ci = round(196 * math.sqrt(score / 100 * (1 - score / 100) / n), 1)
    with tracked.run(version, method="none", id=f"refund-bot-{version}") as run:
        run.score("refunds", score, ci=ci, n=n, test_version="v1")
        run.finish()
    return score
```

**Noise floor.** rlhfbook.com, "Evaluation": post-training evals move 0.25 to
1.5 points between runs of the same setup. Measure yours by scoring the served
version on two draws of the held-out set; a scripted bot has no spread, so the
2.0 above is declared, not measured.

## 1. Read yesterday's traces

Wherever they live: a JSONL export, a table dump, a list of dicts.
`wai.load_traces` converts `tool_trace`/`input`/`output` rows to
`steps`/`prompt`/`final_text` and keeps every other field, so `version`,
`latency_s` and `cost_usd` ride along. Note which served version produced them;
the platform keys one row per day, so on a promotion day post under the version
that served most and say so.

```python
N = 100  # sample per day; the same date always draws the same rows


def read_day(day: date) -> tuple[list[dict], str]:
    """Yesterday's traces, normalised, and the served version that produced them."""
    traces = wai.load_traces(trace_path(day))  # a JSONL path, a table dump, or a list of dicts
    versions = Counter(str(t.get("version") or "unknown") for t in traces)
    version = versions.most_common(1)[0][0]
    if len(versions) > 1:
        print(f"  {day}: served by {dict(versions)}; posting under {version}, which served most")
    return traces, version
```

## 2. Draw a fixed sample, score it with the held-out judge

The draw is seeded by the date, so a rerun picks the same rows and posts the
same number. `flagged` is the count the judge failed. Read `scored.warnings`
first: a sample where no tool ran is hollow, and its rate is not a rate.

```python
def sample_and_score(traces: list[dict], day: date) -> tuple[list[dict], int]:
    """A fixed-size draw seeded by the date, scored by the held-out judge."""
    picked = random.Random(day.isoformat()).sample(traces, min(N, len(traces)))
    scored = wai.evaluate(picked, refund_judge, tools=TOOLS)
    for note in scored.warnings:
        print("  !", note)  # a hollow sample (no tool ran) is not a flagged rate
    return picked, len(scored.failures())
```

**Size N against the floor.** The sample's own 95% half-width at a 3% rate is
about 3.3 points at N=100 and 2.4 at N=200. Step 4 uses the larger of that and
the noise floor as the band, so a small N makes the rule slower, never wrong.

## 3. Post one LiveDay

**Scaled, not raw.** `flagged` is the sample's failures scaled to the day
(`round(replies * failed / n)`), so `flagged / replies` on the tile is the
estimated rate for the whole day. Same rule every day; do not switch to raw
counts, the series would stop meaning one thing. `p50_s` and `cost_usd` come
from the traces when they carry them and are left out when they do not.

```python
def post_day(day: date, version: str, traces: list[dict], failed: int, n: int) -> LiveDay:
    """One LiveDay. flagged is the sample's failures scaled to the day's replies."""
    replies = len(traces)
    latencies = [float(t["latency_s"]) for t in traces if t.get("latency_s") is not None]
    costs = [float(t["cost_usd"]) for t in traces if t.get("cost_usd") is not None]
    item = LiveDay(
        day=day,
        version=version,
        replies=replies,
        flagged=round(replies * failed / n),
        p50_s=round(statistics.median(latencies), 3) if latencies else None,
        cost_usd=round(sum(costs), 4) if costs else None,
    )
    tracked.live(item)  # POST /live; the row key is live#<agent>#<day>, so a rerun overwrites
    return item
```

## 4. The drift rule: two days above the band

rlhfbook.com, "Evaluation": a difference inside the run-to-run spread is not a
result. One bad day is one draw. The signal to open a new run is the flagged
rate sitting above its baseline by more than the band on two days in a row,
on the same served version. Baseline is the median of that version's earlier
days; until there are three, it is the held-out fail rate (`100 - score`).

```python
def drift(dash: Dashboard) -> tuple[bool, str]:
    """True when the flagged rate sat above its baseline by more than the band
    on each of the last two days of the served version. The band is the
    larger of the behavior's noise_floor and the sample's own 95% half-width."""
    live = dash.live
    floor = dash.behavior.noise_floor if dash.behavior else None
    if floor is None:
        return False, "no noise_floor declared; tracked.behavior('refunds', noise_floor=<spread>)"
    version = live.version[-1] if live.version else None
    pcts = [p for v, p in zip(live.version, live.flagged_pct) if v == version and p is not None]
    if len(pcts) < 2:
        return False, f"{len(pcts)} day(s) on {version}; the rule needs two"
    earlier, last_two = pcts[:-2], pcts[-2:]
    if len(earlier) >= 3:
        baseline, source = statistics.median(earlier), f"median of {len(earlier)} earlier days"
    else:
        held = next((v.score for v in dash.versions if v.v == version), None)
        if held is None:
            return False, f"no earlier days and no held-out score for {version}; score_served()"
        baseline, source = 100 - held, "held-out fail rate"
    half = 196 * math.sqrt(baseline / 100 * (1 - baseline / 100) / N)
    band = max(floor, half)
    rises = [round(p - baseline, 1) for p in last_two]
    fired = all(r > band for r in rises)
    note = f"rise {rises[0]:+g} then {rises[1]:+g} vs {source} {baseline:.1f}%, band {band:.1f}"
    return fired, note
```

**When it fires.** Open a run: `tracked.run("v4", targets=["refunds"])`.
Then look at what changed. In `check.py` the model did not move; the traffic
did (urgent asks the held-out set barely covers). Either way the next test
version needs those asks, or the run will train on one thing and be scored on
another.

## 5. The daily job, and scheduling it

One function, run once a day for yesterday. Idempotent because the day is the
key: the platform overwrites `live#<agent>#<day>`, and the seeded draw posts
the same number, so a retry, a double-fired cron, or a backfill is harmless.

```python
def watch(day: date) -> tuple[LiveDay, bool]:
    """The daily job. Run it once per day; the day is the key, so a rerun is harmless."""
    traces, version = read_day(day)
    picked, failed = sample_and_score(traces, day)
    item = post_day(day, version, traces, failed, len(picked))
    fired, note = drift(tracked.dashboard("refunds"))
    pct = 100 * item.flagged / item.replies if item.replies else 0.0
    print(
        f"{day} {version}: {item.replies} replies, {failed}/{len(picked)} sampled failed, "
        f"flagged {item.flagged} ({pct:.1f}%), p50 {item.p50_s}s; {note}"
    )
    if fired:
        print(
            "  DRIFT: two days above the band. Open a run: tracked.run('v4', targets=['refunds'])"
        )
    return item, fired
```

**Schedule.** Cron (`15 6 * * * uv run python watch.py`) or a scheduled coding
agent that runs the same command, after the trace export for yesterday has
landed. One command per day; a missed day is filled by running it with that
date. This is engineering, not research: the platform has no scheduler and
never reads your traces.

## 6. End with the verdict

The same dashboard read carries the promote decision. Print it every day, so
the person sees whether a candidate is waiting or the served version is alone.

```python
def daily(day: date) -> None:
    """What cron runs: yesterday's tile, then the one line a person reads."""
    watch(day)
    print(str(tracked.verdict("refunds")))
```

`refunds: v3 is serving; no newer candidate yet` means nothing is queued.
`refunds: v4 beats v3 by 5 (interval excludes zero, clears the noise floor of
2)` means the run the drift rule asked for is done and scored; the person
presses Promote, and tomorrow's LiveDay posts under v4.
