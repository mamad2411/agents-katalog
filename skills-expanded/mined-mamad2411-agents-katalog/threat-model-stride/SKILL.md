---
name: threat-model-stride
description: >-
  Build a STRIDE threat model for an agentic system from the evidence an estate
  already holds — source code, CSPM findings, IAM policies, network policies and
  the tool surface — and emit a ranked threat table plus a trust-boundary
  diagram. Use when asked what could go wrong with an architecture, to
  threat-model an agent, a pipeline or a service, when a threat model needs
  regenerating after an architecture change, or when someone asks which STRIDE
  categories a design actually exposes.
allowed-tools: Read, Grep, Glob, Bash
---

# STRIDE threat modelling for an agentic system

A threat model written in a workshop describes the system as it was on the day
of the workshop. This one is **derived**: every threat traces to a line of
evidence that already exists somewhere in the estate, so regenerating it is
cheap and the useful artefact is the **diff between two runs**.

STRIDE gives six categories. Against an agentic system each one has a specific
shape that a web-application threat model does not:

| STRIDE | In an agentic system |
|---|---|
| **S**poofing | An agent calls downstream as a shared service account, so "which agent" is unanswerable |
| **T**ampering | Untrusted content the agent read becomes an instruction it follows |
| **R**epudiation | The delegation chain is not on the token, so no log answers "on whose behalf" |
| **I**nformation disclosure | An over-broad tool return, or egress that permits anything |
| **D**enial of service | An unbounded loop, or a budget nobody set |
| **E**levation of privilege | A role assumable by `*`, or a scope that includes refunds because it included payments |

## When to use this

Threat-modelling an agent, an MCP server, or a review pipeline; re-running a
model after an architecture change; or answering "which STRIDE categories does
this design actually expose" with something better than an opinion.

## Inputs it expects

Five evidence sources. Any one alone produces a model that is wrong in a
predictable direction — code alone cannot tell you whether a path is exposed,
and CSPM alone cannot tell you what reaches it.

| Input | What only it can tell you |
|---|---|
| `architecture` | components, flows, sinks, trust levels — what *could* be reached |
| `cspm` | live posture findings: what is public *today* |
| `iam` | which roles exist, who may assume them, whether MFA is required |
| `network` | ingress exposure and egress policy — can anything leave |
| `entitlements` | what the running identity may do once it is through |

## Procedure

**1 — Load the five inputs.** Refuse to proceed on fewer. A model built on
`architecture` alone should say so in its output rather than silently scoring as
though the estate were hardened.

**2 — Walk each entry point to each sink.** For every reachable pair, ask the
six STRIDE questions. A category that has no evidence behind it is not a threat;
do not invent one to fill the row.

**3 — Score from evidence, not from feeling.** Base severity comes from the
asset. Then adjust *only* where an input says so: internet-facing, no WAF, a
live CSPM finding on the resource, a role that holds write, a trust policy with
a wildcard, egress open. Record which adjustment fired — the reasons are the
part a reviewer argues with.

**4 — Emit the trust-boundary diagram.** Nodes are components, edges are flows,
and an edge crossing from a lower trust level to a higher one is a boundary.
Boundaries are where findings live; render them differently from ordinary edges.

**5 — Diff against the previous run.** Report new threats *and* escalated ones.
A pull request that changes only infrastructure introduces no new threat and
raises every existing score, so a gate that counts arrivals alone waves it
through.

## Example

**Input** — the fixture committed at the top of [`scripts/threat_model.py`](scripts/threat_model.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
id      entry           sink           score  why
--------------------------------------------------------------------------------------------
T-10  I upload_voucher  store             11  a live CSPM finding on the resource this path reaches
T-01  S get_booking     load_booking      11  the running role is assumable by *
T-05  D get_booking     load_booking      10  internet-facing with no WAF in front of it
T-06  E get_booking     load_booking      10  the identity holds write, not just read
T-03  R get_booking     load_booking      10  no MFA on the assumable role, so the actor is not established
T-04  I get_booking     load_booking       9  no open CSPM finding on the resource
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
  "inputs_present": ["architecture", "cspm", "iam", "network", "entitlements"],
  "threats": [
    {"id": "T-01", "stride": "S|T|R|I|D|E", "entry": "str", "sink": "str",
     "asset": "str", "score": 0, "reasons": ["internet-facing", "..."],
     "evidence": {"source": "cspm|iam|network|entitlements|architecture",
                  "detail": "str"}}
  ],
  "boundaries": [{"from": "str", "to": "str", "trust": "0->2"}],
  "diagram": "mermaid or svg source",
  "diff": {"new": ["T-07"], "escalated": [{"id": "T-01", "from": 13, "to": 17}]}
}
```

## Failure modes

- **Modelling the code and calling it the system.** The same repository behind
  a private load balancer with default-deny egress and on the internet with a
  wildcard trust policy is two different threat models. Read all five inputs.
- **Counting new threats only.** Escalation is the signal a terraform-only
  change produces, and it is the majority of how an estate gets worse.
- **One row per STRIDE letter.** Six categories is a checklist, not a quota. An
  agent with no state has no meaningful tampering row.
- **Scoring without recording why.** A score nobody can argue with is a score
  nobody will act on.
