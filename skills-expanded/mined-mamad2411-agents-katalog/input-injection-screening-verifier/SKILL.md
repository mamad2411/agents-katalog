---
name: input-injection-screening-verifier
description: >-
  Verify that untrusted ingestion paths pass through an injection detection
  or sanitisation step before reaching model context. Use to attest
  injection screening, to inventory which untrusted sources are screened, or
  to check for the private-data plus untrusted-content plus egress
  combination.
allowed-tools: Read, Grep, Glob
---

# Input Injection Screening Verifier

**Controls:** Control 5 — indirect prompt-injection screening

## Confidence: PARTIAL — and this ceiling is not negotiable

You can verify that a detector **exists on the path** and record its class.
You cannot verify that it works. Published defences that reduce attack success
to a few percent under static attacks have been driven back above 95% by
adaptive, search-based attacks, and human red-teamers defeat them routinely.

**Record the detector class. Do not assert protection. Cap at PARTIAL.**

## When to use this
When a deployment claims to screen untrusted input, and specifically when
somebody wants that claim recorded as PASS. It cannot be: the ceiling here is
PARTIAL and not negotiable, and running this is how that gets written into the
artefact rather than argued about in a review.

## Procedure

1. **Inventory untrusted ingestion paths.** Email, documents, web fetches,
   tickets, tool results, MCP tool descriptions, retrieved corpora, memory
   reads, inter-agent messages. Anything a party outside your trust boundary
   can write into.

2. **For each path, determine whether a screening step exists** between
   ingestion and model context, and record which one — a classifier, a
   prompt-attack filter, delimiting or spotlighting, a dual-model pattern, or
   nothing.

3. **Check provenance tagging.** Whether the origin survives into the context
   window is more durable than any detector, because it does not depend on
   recognising the payload.

4. **Flag the dangerous combination.** Private data reachable **and** untrusted
   content ingested **and** an egress path available is the combination that
   turns injection into exfiltration. Any deployment with all three is a
   finding on its own, whatever the detector says.

## Example

**Input** — the fixture committed at the top of [`scripts/input_injection_screening_verifier.py`](scripts/input_injection_screening_verifier.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
the same payload, through every ingress component:
   knowledge  -> refused   (knowledge may not select a tool)
   memory     -> refused   (memory may not select a tool)
   mcp        -> refused   (mcp may not select a tool)
   tools      -> refused   (tools may not select a tool)
   messaging  -> refused   (messaging may not select a tool)

rewriting the payload does not help - the check never reads it:
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
  "deployment_id": "str",
  "ingestion_paths": [
    {"source": "str", "screened": true, "detector_class": "classifier|filter|spotlighting|dual_model|none",
     "provenance_tagged": true}
  ],
  "unscreened_sources": ["str"],
  "trifecta": {"private_data": true, "untrusted_content": true, "egress": true, "present": true},
  "verdict": "PARTIAL|FAIL",
  "verdict_ceiling_reason": "detector presence is verifiable; robustness under adaptive attack is not"
}
```

`PASS` is not a permitted value.

## Failure modes

- **Reporting a detector's benchmark score as this deployment's protection.**
  Those numbers are from static attacks.
- **Missing tool results as an ingestion path.** They are the most commonly
  forgotten one, because they arrive from a system you trust.
- **Ignoring the combination check** because each element looked acceptable
  alone.
