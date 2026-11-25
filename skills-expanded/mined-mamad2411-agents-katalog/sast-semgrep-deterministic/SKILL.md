---
name: sast-semgrep-deterministic
description: >-
  Score a real Semgrep run against a ground-truth key and report recall per
  ruleset width, not just the finding count. Use when choosing or reviewing a
  SAST configuration, when a scan comes back clean, or when asked how much of
  the codebase a scanner is actually looking at.
allowed-tools: Read, Grep, Glob, Bash
---

# What did Semgrep look for, and what did it never look for?

Deterministic SAST parses code to a graph and asks a rule a question about it.
Given the same file and the same rules it returns the same findings, every
time — which is what makes it the half of the audit you can gate a merge on.

The mistake is reading its output as a measure of the file. It is a measure of
the **rules that were enabled**. A scan with one pack and a scan with seven
disagree by a factor of four on the same file and both exit `0`, so the number
that matters is never the finding count — it is **recall against a key**, and
almost nobody computes it because it requires knowing the answer in advance.

## When to use this

Before trusting any clean scan, and whenever a SAST configuration is chosen,
widened or inherited. Also the honest way to compare two scanners: run both
against a file whose defects you have enumerated by hand, and compare recall
rather than volume.

## Procedure

**1 — Enumerate the defects by hand first.** One line per defect, with its CWE
and whether it is expressible as a pattern at all. Do this before running
anything; a key written after the scan is a description of the scan.

**2 — Run the scanner at every width you are considering.** The default pack,
the widest set your team would plausibly enable, and any custom rules you
wrote. Keep the raw JSON — the finding's rule id is what tells you *which*
rule fired, and that is what you tune.

**3 — Score each width against the key.** Precision and recall separately.
Deterministic SAST usually has excellent precision and the recall is the
number under discussion; reporting them merged as "accuracy" hides exactly
that.

**4 — Partition what was missed into two classes.** A defect a rule *could*
match but none did is a **coverage gap** — someone writes the rule. A defect
that is the **absence** of a call, or depends on the caller's authority, is
not expressible as a pattern and no amount of rule-writing reaches it. Only
the second class justifies a model pass.

**5 — Report the width, not just the result.** Every finding count is
meaningless without the config that produced it. A report that says "Semgrep:
1 finding" and not "p/python + p/secrets" has withheld the part that decides
whether the scan meant anything.

## Example

**Input** — the fixture committed at the top of [`scripts/sast_semgrep_deterministic.py`](scripts/sast_semgrep_deterministic.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
semgrep 1.176.0 · booking.py · 6 defects in the key, 5 of them expressible as a pattern

config                   found  tp  fp   prec  recall
p/python + p/secrets         1   1   0   1.00    0.17
seven registry packs         4   4   0   1.00    0.67
custom taint rule            2   2   0   1.00    0.33

Nothing about the file changed between those rows. Three of the four
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
  "key": {"defects": 0, "pattern_expressible": 0},
  "runs": [{"config": "str", "findings": 0, "true_positives": 0,
            "precision": 0.0, "recall": 0.0}],
  "missed_by_all": [{"line": 0, "cwe": "str", "class": "coverage-gap|not-expressible"}],
  "widest_recall": 0.0
}
```

`class: not-expressible` is the only honest argument for adding a
probabilistic reviewer. If every miss is a coverage gap, the fix is a rule and
it is cheaper.

## Failure modes

- **Reading a clean scan as a clean file.** It means no enabled rule matched.
- **Comparing scanners on finding count.** The noisier one wins, which is
  backwards.
- **Writing the key after the run.** It converts recall into 1.00 by
  construction.
- **Enabling every pack to fix recall.** Recall rises and so does triage cost;
  the widest width here still misses a third of the key, so width alone was
  never going to be the answer.
