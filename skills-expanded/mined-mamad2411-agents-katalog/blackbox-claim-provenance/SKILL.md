---
name: blackbox-claim-provenance
description: >-
  Split an external probe's claims into what the evidence entails and what it
  merely suggests, and refuse to attach a severity to the second kind. Use for a
  black-box engagement, or when a report reads more confidently than its
  evidence supports.
allowed-tools: Read, Grep, Glob
---

# An inference with a severity beside it is a finding to everyone downstream

Black box is the mode with the least information and the most room to narrate. A
model handed status codes, headers and timings will produce a fluent
architecture, and every sentence of it will be plausible. Some of it is entailed
by the evidence. Most of it is not, and the report does not distinguish them
unless you make it.

## When to use this

An external engagement with no credential, a bug-bounty triage queue, and any
report where the reader cannot tell which claims were tested.

## Procedure

**1 — List what the mode may look at.** DNS and certificate transparency, the
TLS handshake, HTTP status/headers/body, error strings, response timing, public
artefacts, the scope document. The list is short, and that is the constraint.

**2 — Write each claim with the evidence beside it.** Not a summary of the
evidence — the actual observation that produced the claim.

**3 — Ask one question per claim: does this evidence entail the claim, or is it
merely consistent with it?** A 404 on a random id is consistent with correct
authorisation *and* with a missing object. A `csrftoken` cookie is consistent
with Django and with anything copying its conventions.

**4 — Report observed claims as findings and inferred ones as open questions,
with no severity on the second list.** Then say what each open question would
need. The ones needing a second credential are grey-box tests, not better
black-box ones.

## Example

```
report: 5 findings, 7 open questions
no severity is attached to anything in the second list.
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
  "data_sources": [{"source": "str", "establishes": "str"}],
  "claims": [{"claim": "str", "evidence": "str", "entailed": true}],
  "findings": ["str"],
  "open_questions": [{"claim": "str", "would_need": "str"}]
}
```

## Failure modes

- **Scoring an inference.** A CVSS number converts a guess into a finding for
  every reader after you.
- **Treating untested as disproved.** "No per-account rate limit" from a single
  address is a gap in the test, not a property of the system.
- **Fingerprinting from headers.** They are copied, proxied and templated.
- **Dropping the open questions.** They are the engagement's most useful output:
  they say what mode to run next.
