---
name: behavioural-drift-monitor
description: >-
  Track an agent's drift from its signed-off baseline across a quarter and count
  how many of the surfaces that change its behaviour bypass change management.
  Use when an agent behaves differently than it was approved to, with no code
  change to point at.
allowed-tools: Read, Grep, Glob
---

# Four of six things that change an agent are not code changes

The model version, the prompt, the tool manifest and the approval settings all
change what an agent does, and none of them generates a change record. So drift
is the only signal that the approved system and the running system have diverged,
and it has to be measured rather than inferred from a changelog.

## When to use this

Continuously, for any agent under governance — and specifically after a provider
announces a model update.

## Procedure

**1 — Enumerate the change surfaces.** Code, model version, system prompt, tool
manifest, approval settings, retrieval corpus. For each, record whether a change
produces a record anybody reviews.

**2 — Count the ones that bypass change management.** Four of six is typical.
That count is the argument for measuring drift at all.

**3 — Fix a baseline at sign-off.** Tools, resources, rate, refusal rate — and
the model version and prompt hash alongside, so a later drift can be attributed.

**4 — Compute drift per period and attribute each rise.** A jump that coincides
with a model upgrade is a different conversation from a jump with no
corresponding event, and the second is the one to escalate.

**5 — Set a tolerance and a consequence.** Beyond tolerance: re-attest, or
revert. A drift figure with no consequence is a chart.

## Example

**Input** — the fixture committed at the top of [`scripts/behavioural_drift_monitor.py`](scripts/behavioural_drift_monitor.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
    when  event                       drift  new tools
------------------------------------------------------------------
    90d  control signed off          0.000  []
    60d  prompt edited               0.100  []
    30d  tool added (no PR)          0.330  ['run_shell']
     5d  model upgraded by vendor    0.550  ['run_shell']
observed drift rate  0.00647 TVD/day
tolerance            0.25
```

The run continues past this. `test_skills.py` executes the script on every
build, **with no model configured** — so what CI proves is that it runs and
refuses legibly, not that it prints these lines. The output above is a recorded
run against a real model, and nothing re-diffs it: a model's answer is not
reproducible, and this repository does not claim otherwise anywhere it can be
checked.

## Output contract

```json
{
  "surfaces": [{"name": "str", "produces_change_record": false}],
  "bypass_count": 0,
  "baseline": {"at": "str", "tools": ["str"], "model_version": "str", "prompt_hash": "str"},
  "timeline": [{"period": "str", "drift": 0.0, "new": ["str"], "attributed_to": "str|null"}],
  "tolerance": 0.0,
  "consequence": "str"
}
```

## Failure modes

- **Trusting the changelog.** Most of what changes an agent is not in it.
- **Drift with no attribution.** A number nobody can act on.
- **No consequence at the tolerance.** The line stops being a line.
