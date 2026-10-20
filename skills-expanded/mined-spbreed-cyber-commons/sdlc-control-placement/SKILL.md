---
name: sdlc-control-placement
description: >-
  Place each security technique on the pre-deployment / post-deployment line and
  report which risks are covered only on the side that cannot act on them. Use
  when reviewing AppSec tooling coverage, when choosing where a new control
  belongs, or when a risk is described as covered and the incident happened
  anyway.
allowed-tools: Read, Grep, Glob
---

# Which side of the deploy is each control on, and what does that cost?

Every security technique works on one of two things: **artefacts sitting
still** — source, a manifest, an IaC plan, a tool schema — or **a system that
is running**. That is not a taxonomy for its own sake. It decides two
properties that nothing else changes:

- pre-deployment is cheap, repeatable and **can block a merge**, and it is
  blind to every fact that only exists at runtime — the identity the workload
  actually got, the traffic it actually saw;
- post-deployment sees what really happened and **cannot block the change that
  caused it**. It can only tell you afterwards.

A risk covered only on the left is a risk you can prevent and cannot detect. A
risk covered only on the right is one you can detect and cannot prevent. Both
appear as "covered" on a tooling inventory, and only one of them is what the
person reading the inventory thought they were buying.

## When to use this

Before buying anything, when a tooling inventory is presented as coverage, and
after any incident where the answer to "did we have a control for that" was yes.
Also when placing a new control: the same technique run at build time and at
runtime answers different questions, and choosing is a design decision rather
than a scheduling one.

## Procedure

**1 — List the techniques you actually run**, not the ones on the architecture
diagram. A tool that is deployed and muted is not a control.

**2 — Place each one.** Pre, post, or genuinely both. "Both" is rarer than it
looks: a technique that runs at build time and again at runtime counts as both
only if the runtime pass can see something the build pass could not.

**3 — For each one, name what the other side sees that it cannot.** This is
the sentence that turns a list into an argument. If you cannot write it, the
placement is wrong or the technique is not doing what you think.

**4 — Map risks to sides, not to tools.** For each risk class, which sides
cover it. Then count the two failure shapes: **preventable but invisible**
(pre only) and **visible but unpreventable** (post only).

**5 — Report the uncovered and the one-sided separately.** A risk with nothing
on either side is a gap everybody understands. A risk covered only on the side
that cannot act is the one that gets signed off, and it is the one this
procedure exists to surface.

## Example

**Input** — the fixture committed at the top of [`scripts/sdlc_control_placement.py`](scripts/sdlc_control_placement.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
techniques, placed
   technique                     side   gate  blind to
   SAST / code analysis          pre    yes   whether the vulnerable path is reached with real traffic
   SCA and SBOM scanning         pre    yes   what actually loaded, versus what the manifest pinned
   IaC and policy-as-code        pre    yes   the identity and network the workload really got
   threat modelling              pre    -     entry points added by a config change, not a commit
   tool-schema / MCP review      both   yes   a description edited by the server after review
   DAST / attack simulation      post   -     the commit that introduced it
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
  "techniques": [{"name": "str", "side": "pre|post|both", "blind_to": "str"}],
  "risks": [{"risk": "str", "sides": ["pre|post"], "shape": "covered|pre-only|post-only|uncovered"}],
  "counts": {"pre_only": 0, "post_only": 0, "uncovered": 0},
  "gate_capable": 0
}
```

`gate_capable` counts the techniques that can actually block a merge. It is
usually much smaller than the tooling budget suggests, and it is the number
that decides how much of your security posture is advisory.

## Failure modes

- **Counting a muted tool as coverage.** It runs, it reports, nobody reads it.
- **Marking everything "both".** The word stops meaning anything and the
  one-sided risks disappear into it.
- **Assuming pre-deployment sees the deployment.** It sees the plan. The
  identity the workload got, the route it can reach and the guardrail that was
  switched off after the demo are all facts that do not exist yet.
- **Reading post-deployment coverage as prevention.** Detection tells you it
  happened. Nothing on that side of the line stops the merge.
