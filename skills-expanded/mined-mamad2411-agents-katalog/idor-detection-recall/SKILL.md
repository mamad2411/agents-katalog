---
name: idor-detection-recall
description: >-
  Find missing ownership checks on caller-supplied identifiers, and score the
  result on recall against a labelled key rather than on finding count. Use when
  auditing endpoints or tools that take a record id, when evaluating a scanner
  that claims to detect broken object-level authorisation, or when a clean
  access-control scan needs a number behind it.
allowed-tools: Read, Grep, Glob
---

# The defect is what is missing, so the metric has to be recall

An IDOR — broken object-level authorisation — is a function that takes an
identifier from the caller, loads the record it names, and returns or mutates
it without comparing an owner. Two things follow, and both change how you
measure.

**There is no pattern.** `get_booking` and `get_my_booking` differ by one call
that is present in the second and absent in the first. A rule matches syntax
that is there; nothing matches syntax that is not. This is why the class
survives every ruleset width in
[`sast-semgrep-deterministic`](../sast-semgrep-deterministic/SKILL.md).

**So precision is the easy half and recall is the whole problem.** A scanner
that reports nothing has perfect precision. The number that decides whether an
access-control audit meant anything is what fraction of the real defects it
found, and that requires a key — which is why almost nobody publishes one.

Semgrep did, in
[a 2026 IDOR benchmark](https://semgrep.dev/blog/2026/idor-detection-benchmark-semgrep-multimodal/):
275 manually reviewed labels across four repositories, the same revisions for
every system.

| system | recall | precision | F1 |
|---|---|---|---|
| Semgrep Multimodal | **59.9%** | 57.5% | 57.1% |
| Claude Security with Mythos | 13.9% | **80.1%** | 23.7% |
| Codex Security | 11.3% | — | 17.7% |

Read the two bold cells together, because they are the shape of the problem.
The most *precise* system found roughly **one IDOR in seven**. The best recall
on the board is **six in ten** — from a system that reasons about the class
rather than matching a pattern, and that is a real change from what rules could
do. It is also not a solved problem, and a report that quotes only precision is
quoting the number that improves when you find less.

## When to use this

On any surface where a caller passes a record identifier: REST handlers, RPC
methods, and — the one people forget — **agent tools**, where the identifier
arrives in a model-proposed argument and the tool runs with the agent's scope
rather than the requester's. Also whenever an access-control scan comes back
clean, because clean and unmeasured look identical.

## Step-by-step

**1 — Enumerate the object-handling units first, not the findings.** Every
function that takes an identifier and touches a record. This is the
denominator; without it you cannot compute recall and every later number is
decoration.

**2 — For each, find the ownership comparison, or its absence.** A call that
compares something from the record against something from the session. Trace
it through helpers — a check inside `require_owner` counts, and a check in a
decorator counts.

**3 — Include the correct ones in the key.** A corpus where everything is
broken cannot measure precision. The near-identical safe twin of each defect is
what catches a detector that flags on shape rather than on the missing check.

**4 — Score recall and precision separately, and report the denominator.**
"Three findings" is not a result. "Three of the five object-handling units,
against a key of eight" is.

**5 — Weight by the authority the caller holds, not by the CWE.** The same
missing check is a different severity in a tool the Workflow Agent invokes with
`payments.refund` than in one a traveller invokes with their own session. CVSS
does not know that; your architecture map does.

## Example

**Input** — the fixture committed at the top of
[`scripts/idor_detection_recall.py`](scripts/idor_detection_recall.py), scanning
the `cybertravels/` sample repository against `cybertravels/LABELS.md`.

**Output** — the opening lines of a real run:

```
cybertravels/ · 7 object-handling units, 4 of them authorised
detector                        found  tp  fp   prec  recall
pattern rule (execute + id)         0   0   0   0.00    0.00
ownership-comparison analysis       3   3   0   1.00    1.00
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
  "units": [{"file": "str", "unit": "str", "takes_id": true,
             "ownership_check": "present|absent|via-helper"}],
  "detectors": [{"name": "str", "found": 0, "true_positives": 0,
                 "precision": 0.0, "recall": 0.0}],
  "findings": [{"unit": "str", "cwe": "CWE-639", "caller_authority": "str",
                "severity": "str"}],
  "denominator": 0
}
```

`denominator` is the field that makes recall meaningful, and the one a scanner
that reports only findings cannot give you.

## Common edge cases

- **The check is in a decorator.** `@requires_owner` above the function is an
  ownership check and a naive body scan misses it, reporting a false positive
  on correct code.
- **The check is on the wrong object.** Comparing `session.user_id` to the id
  the *caller supplied* rather than to the one on the *loaded record* passes
  every structural test and authorises nothing.
- **The identifier is not obviously an id.** A slug, a reference string, a
  filename. `download_invoice(session, path)` is the same defect wearing a
  different parameter name.
- **List endpoints.** `list_my_bookings` takes no id at all — it is scoped by
  the session, so there is nothing to tamper with. Including it in the
  denominator understates recall.

## Failure modes

- **Reporting precision without recall.** The number that looks best is the one
  that improves when the detector finds less.
- **Scoring without a key.** Then "no findings" and "no defects" are the same
  sentence, and only one of them is good news.
- **Treating a reasoning detector's output as findings.** 59.9% recall at 57.5%
  precision means roughly two in five reports are wrong; they are hypotheses,
  and C2.4 is what promotes them.
- **Ranking by CWE.** Every IDOR is CWE-639. The one on the refund path is not
  the same finding as the one on a read.
