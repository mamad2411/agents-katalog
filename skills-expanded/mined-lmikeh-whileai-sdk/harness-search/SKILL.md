---
name: harness-search
description: >
  How a coding agent runs the Meta-Harness loop as the proposer on an
  agent's own production traffic: point the recipe at yesterday's traces,
  read out/proposal.md, write the next candidates/<n>_<name>.py, run the
  recipe, read the ledger, stop when the gate passes or after N rounds,
  report Changed / Moved / Why / Learned / Reproduce, post every candidate
  as a harness version, and score the next day's traffic on the pick. Use
  when the thing to improve is the harness (the prompt, the tools, the
  turn cap, the retry) and not the weights, on a closed model or an open
  one. No GPU, no key for the dry run.
metadata:
  version: "1.2.0"
---

# Harness search

Lee et al. 2026 (Meta-Harness, arXiv:2603.28052) search over harness code
with an agentic proposer that reads the source, scores and traces of every
prior candidate through a filesystem, and check the pick on held-out tasks
and held-out models. The recipe `recipes/papers/meta-harness` is the inner
half: it scores every file in `candidates/`, writes the ledger, the
proposal and the gate's answer. You are the outer half. Every step below is
in `check.py`, which runs the recipe's dry run on a temporary copy in under
a minute; its setup defines `RECIPE` (that copy), `MODEL` (the search
model), `ROUNDS` (3), `TRACES` (three days of the agent's traffic as a
JSONL, the shape `wai.load_traces` reads, or an OTLP JSON batch), `run(*flags)`
(the recipe with `--dry-run`), `propose_candidate(proposal)` (your job,
scripted there), `load_harness` (a candidate file as `wai.Harness`),
`judge` and `TOOLS` (the recipe's program judge and tool list), `NEXT_DAY`
and `DAY_AFTER` (the traffic the pick served the day after, and its date)
and `fake` (a platform that answers like the API).

## 1. Run the loop once on the traffic and read what it wrote

The frozen set is the traffic: one task per distinct prompt. The holdout
is its latest days, whole days, so no row the proposer reads comes from the
days that decide, and train prompts that overlap a holdout prompt leave the
proposer's window (Wang et al. 2026, arXiv:2607.12227: a harness tuned on
the tasks it is scored on gained 0.6 points on held-out tasks). Four files
carry the state: the split (how the days were cut, what was dropped), the
ledger (one line per candidate: score with its interval on the train and
holdout splits, cost per rollout), the proposal (every candidate's source,
score and five worst rows, then the one instruction), and the selection
(the gate's answer). Read all four; never score by hand.

```python
def read_ledger(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def state() -> tuple[str, list[dict], dict]:
    out = RECIPE / "out"
    return (
        (out / "proposal.md").read_text(encoding="utf-8"),
        read_ledger(out / "ledger.jsonl"),
        json.loads((out / "selected.json").read_text(encoding="utf-8")),
    )


run("--propose", "--select", "--fresh", "--traces", str(TRACES))
proposal, ledger, selected = state()
split = json.loads((RECIPE / "out" / "split.json").read_text(encoding="utf-8"))
print(split["how"], "|", split["contamination"]["n_dropped"], "train prompt(s) left the window")
```

## 2. Propose, run, read, stop

The proposal names the file to write. Read the worst rows of the best
candidate so far and change the one thing they say is wrong: a line in the
instructions, a tool, a `Disclosure` field. One change per candidate, so
the ledger says which change moved the score. The candidate is a file that
defines `harness(model) -> wai.Harness`; copy the shape of the file before
it. Then run again and read the selection. Stop when `selected` names a
candidate, or after `ROUNDS`: a search that never clears the gate is a
result too, and the report says so. The pick is the candidate that leads
the most train tasks, not the best mean (Agrawal et al. 2025, GEPA,
arXiv:2507.19457), and it counts only if the holdout and the held-out model
agree with an interval that excludes zero, at a cost per rollout no higher
than the baseline's. A candidate that wins by spending more is a frontier
point; the selection says what `--cost-margin` would accept it.

```python
NEXT = re.compile(r"write candidates/(\d\d)_<name>\.py")

for _round in range(ROUNDS):
    if selected["selected"]:
        break
    number = NEXT.search(proposal).group(1)
    name, body = propose_candidate(proposal)  # you: read the worst rows, write the file
    (RECIPE / "candidates" / f"{number}_{name}.py").write_text(body, encoding="utf-8")
    run("--propose", "--select", "--traces", str(TRACES))
    proposal, ledger, selected = state()
```

Write each candidate as named edits (`EDITS` of `common.Edit`, built with
`common.from_edits`, as `candidates/02_check_result.py` does) rather than
one instructions string, so the pick can be pruned. Once `selected` names a
candidate, run the recipe once more with `--select --prune`: it takes the
pick's edits out one at a time on the train split and drops each one whose
removal costs no score and no cost per rollout, then gates what is left
(Xia et al. 2026, RRSI, arXiv:2609.24972: unconstrained harness evolution
raised its own split 3.4 points and three unseen benchmarks 0.6 at 2.4x
the tokens; with constraints including pruning, the unseen benchmarks rose
3.9 on 36% fewer tokens than that).
If `out/pruned.json` names a pruned file and it cleared the gate, copy it
into `candidates/` and report that file as the pick; otherwise report the
pick as selected and list the edits the pruner kept.

## 3. Report so a person can decide

Five lines, from the ledger and the selection, never from memory. Changed
is the file and its fingerprint. Moved is the holdout, in points, with the
paired delta and its interval, the tasks the baseline passed and the pick
failed, and the cost ratio. Why is what the baseline's worst rows said.
Learned closes the question and names the paper. Reproduce is the command
and the seed. Post every candidate as a harness version so the Runs page
groups the dots by harness; `load_harness` gives the same fingerprint the
ledger carries. Archive nothing: a candidate that lost is the record of
what was tried.

```python
pick_name = selected["selected"] or selected["best_on_train"]
base, pick = ledger[0], next(e for e in ledger if e["candidate"] == pick_name)
check, cost = selected["checks"][MODEL], selected["checks"]["cost"]
lo, hi = check["ci95"]
worst = read_ledger(RECIPE / "out" / base["worst"])
note = (
    f"Changed: {pick['candidate']}, fingerprint {pick['fingerprint']}, against {base['candidate']}.\n"
    f"Moved: {100 * base['holdout']['pass_at_1']:.0f} to {100 * pick['holdout']['pass_at_1']:.0f} "
    f"points on {pick['holdout']['n_tasks']} held-out tasks ({split['how'].split(':')[0]}), "
    f"{100 * check['delta']:+.0f} [{100 * lo:+.0f}, {100 * hi:+.0f}]; {check['regressed']} task(s) "
    f"the baseline passed and it failed; {cost['ratio']:.2f}x the cost per rollout.\n"
    f"Why: the baseline's worst rows were {'; '.join(sorted({w['why'] for w in worst}))}.\n"
    f"Learned: {selected['reason']} (Meta-Harness, Lee et al. 2026, arXiv:2603.28052).\n"
    f"Reproduce: cd recipes/papers/meta-harness && python run.py --dry-run --traces {TRACES.name} "
    "--propose --select --seed 0"
)

tracked = track("support-bot", model=MODEL, transport=fake)  # drop transport= for real
tracked.behavior(
    Behavior(
        name="plain_answer",
        test_version="t-" + base["fingerprint"][:8],
        n=pick["holdout"]["n_tasks"],
        judge=Judge(name="filler, fault and leak checks as a program"),
        reward_is_judge=False,
    )
)
for entry in ledger:
    version = tracked.run(
        entry["label"],
        method="eval",
        harness=load_harness(entry["candidate"], MODEL),
        targets=["plain_answer"],
    )
    ci = entry["holdout"]["ci95"]
    version.score(
        "plain_answer",
        100 * entry["holdout"]["pass_at_1"],
        ci=50 * (ci[1] - ci[0]),
        n=entry["holdout"]["n_tasks"],
    )
    if entry["candidate"] == pick["candidate"]:
        version.note(note)
    version.finish(say=False)
print(note)
print("verdict:", tracked.verdict())
```

## 4. Serve the pick, then score the next day

The holdout says what the pick can do on traffic it never saw. The next
day says whether that survived contact with real traffic, the only number
that does. Serve the pick, read the day after from your logs, score it
with the same judge the holdout used, and post one `LiveDay`. A flagged
rate near the holdout's failure rate closes the loop; one well above it
reopens step 2 with that day as the traces.

```python
next_day = load_traces(str(NEXT_DAY))  # the day after the pick was served, from your logs
scored = evaluate(next_day, judge, tools=TOOLS)  # the same judge the holdout used
flagged = len(scored.failures())
tracked.live(LiveDay(day=DAY_AFTER, version=pick["label"], replies=len(next_day), flagged=flagged))
live_fail = 100 * flagged / len(next_day)
holdout_fail = 100 * (1 - pick["holdout"]["pass_at_1"])
print(f"next day: {live_fail:.0f} of 100 flagged; the holdout said {holdout_fail:.0f} of 100")
```

## What the person sees

One dot per candidate on the Runs page, grouped by harness, each with its
interval. Under the picked one, five lines that say what changed, by how
much on days it never saw, what it cost, why, what it taught, and how to
run it again. Under the others, the score that lost. The Live tile shows
the day after. A search that stopped at `ROUNDS` with nothing selected
says so in Learned, and the next round starts from the same proposal.
