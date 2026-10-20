---
name: confidence-provenance-decay-check
description: >-
  Track a hedged claim across summarisation hops and measure confidence rising
  while provenance disappears. Use when output from one model or agent becomes
  input to another, in report chains, research pipelines, or any place a summary
  is summarised.
allowed-tools: Read, Grep, Glob
---

# Confidence rises at exactly the rate evidence disappears

"I could not find a CVE, it is probably fine" becomes "libfoo is clean" in
three hops. Nothing in the chain lied. Each step did what summarising does —
dropped the hedge, dropped the caveat, dropped the sentence saying where the
claim came from — and the result is a confident statement with no evidence
behind it.

## When to use this

Report generation, triage pipelines, research chains, any agent that consumes
another agent's output, and any workflow where a human reads only the last
artefact.

## Procedure

**1 — Find the chains.** Every place where generated text is input to a later
generation step. Include the human-visible summary at the end; it is a hop.

**2 — Instrument the original claim.** Record its hedge, its confidence if one
is stated, and its provenance — the source it rests on.

**3 — Step the chain and record both series.** After each hop, the claim's
confidence and its surviving provenance fields. Two numbers per hop; the shape
is the finding.

**4 — Identify the hop where provenance empties.** That is where the claim
became unfalsifiable, and it is almost always earlier than where the confidence
peaked.

**5 — Test the carry rule.** A chain that propagates confidence and provenance
as structured fields, rather than as prose the next step must re-read, does not
decay this way. Check whether the interface has those fields at all.

## Example

**Input** — the fixture committed at the top of [`scripts/confidence_provenance_decay_check.py`](scripts/confidence_provenance_decay_check.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
 hop   confidence  claim
   0         0.20  I could not find a CVE for libfoo, it is probably fine
   1         0.80  a CVE for libfoo, it is fine
   2         0.80  a CVE for libfoo, it is fine
   3         0.80  a CVE for libfoo, it is fine

provenance recorded at hop 3: none
confidence at hop 0: 0.20   at hop 3: 0.8
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
  "chain": [{"hop": 0, "claim": "str", "confidence": 0.0, "provenance": ["str"]}],
  "confidence_delta": 0.0,
  "provenance_lost_at": 0,
  "interface": {"carries_confidence": false, "carries_provenance": false},
  "human_reads_hop": 0
}
```

## Failure modes

- **Judging the final claim on its own.** It reads well. That is the problem.
- **Measuring only confidence.** The pair is the finding; either alone is
  ordinary.
- **Fixing it with a prompt.** "Preserve caveats" is advisory; a field is not.
