---
name: offensive-agent-safety-preflight
description: >-
  Refuse to start an offensive-agent engagement until zero-retention,
  sandboxing, egress control, secret management, human-in-the-loop,
  deterministic guardrails and SOC notification are in place, and brief the SOC
  on what to expect. Use before giving an agent offensive capability.
allowed-tools: Read, Grep, Glob
---

# The most capable, least supervised thing in the estate

An offensive agent scans, reasons and exploits at machine speed, on credentials
you issued, against systems you care about — and its traffic is, by design,
indistinguishable from an attack. That combination is why the controls go on
*before* it starts, not after the first surprise, and why the preflight is a
gate rather than a checklist.

## When to use this

Before any engagement where an agent has offensive capability, and before
re-running one whose configuration changed.

## Procedure

**1 — Check the six blocking controls.** Zero data retention, sandboxing, an
egress allowlist, secret management, human-in-the-loop on destructive actions,
and deterministic guardrails that enforce scope *outside* the model. Blocking
means the engagement does not start without it — because each one's absence is
invisible until it has already cost something.

**2 — Check the advisory control.** SOC notification is advisory only because
its absence is recoverable: you can pick up the phone mid-engagement. Nothing
else on the list is.

**3 — Refuse, with the reason.** A missing blocking control stops the
engagement and names what it would have prevented. "Looks fine" is not the
output; a decision is.

**4 — Brief the SOC, and tell them not to mute.** Window, source addresses,
expected signatures — and the instruction to record what fired and what did
not, because measuring detection is half the reason to run the engagement at
all.

## Example

```
  ENGAGEMENT REFUSED — 4 blocking control(s) missing:
  zero_data_retention, egress_allowlist, human_in_the_loop, deterministic_guardrails
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
  "controls": [{"name": "str", "blocking": true, "present": true,
                "if_absent": "str"}],
  "engagements": [{"name": "str", "may_start": true,
                   "blocking_missing": ["str"], "advisory_missing": ["str"]}],
  "soc_brief": {"window": "str", "sources": "str", "expect": ["str"]}
}
```

## Failure modes

- **Deterministic guardrails as a prompt.** Scope the model is *asked* to
  respect can be argued away; scope enforced outside it cannot.
- **Skipping SOC notification to stay quiet.** The quiet run produces a clean
  report and no evidence anything would have been caught.
- **Treating retention as advisory.** Once target data reaches a retaining
  provider, no later control gets it back.
- **A preflight that always passes.** Then it is decoration; it has to be able
  to refuse.
