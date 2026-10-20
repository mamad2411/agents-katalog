---
name: control-baseline-index
description: >-
  Index every control an agentic platform needs — the ordinary ones that predate
  agents and the agentic ones that do not — score each as in place, partial or
  absent, and name the lesson that owns it. Use when asked what controls an AI
  or agent platform needs, to build or review a control baseline, to check
  whether a security programme is only covering the AI-specific rows, or when
  coverage is being reported against a list that was never complete.
allowed-tools: Read, Grep, Glob, Bash
---

# Every control the platform needs, not just the new ones

**Controls:** Cross-cutting — control baseline and coverage

## What this adds

A team that has just shipped agents writes an agentic control list: provenance,
default-deny, sandboxing, egress, budgets. Every row on it is correct, and the
list is a trap. It reports coverage of the ten controls somebody thought of last
quarter and says nothing about the dozen that were required before any of this
existed — and those are where an attacker starts, because they are older, more
reachable and better understood.

The fix is one index with both eras in it and a status per row. The `era` column
is what makes the point arguable: when foundation coverage and agentic coverage
are printed side by side, "we are doing AI security" stops being a defensible
summary of an estate that shares one service account across four agents.

## When to use this

Building a control baseline for a system that has agents in it, reviewing one
somebody else built, or auditing a coverage claim that sounds higher than the
estate feels. Also when a programme has to be sequenced: the absent foundation
rows almost always come first.

## Procedure

**1 — List the controls that were always required.** Vulnerability management,
supply chain, environment segregation, encryption at rest and in transit, input
validation, SDLC and change management, perimeter and DMZ termination,
credential management, PKI, key lifecycle, logging and monitoring. Write them
before you write a single agentic row, so the list is not shaped by what is
currently interesting.

**2 — Add what the agents introduced.** Workload identity, delegated authority
that narrows, just-in-time authorisation, provenance at ingress, default-deny on
the tool call, sandboxed execution, egress control, budgets and stop conditions,
agent telemetry, and human oversight that survives volume.

**3 — Mark each row with what the agents changed about it.** Most foundation
rows are not replaced; they are stressed. Change management did not stop
applying when a model started authoring changes — it started failing on volume.
A row whose note is empty is a row you have not thought about yet.

**4 — Score each row in place, partial or absent** against what is actually
running, not what is documented. Partial is the honest answer for most, and a
scoring scheme with only two values pushes teams to round up.

**5 — Name the owning control for each row** — the team, and here the lesson.
A row with no owner is a row that will be absent again next quarter.

**6 — Report coverage per era, never blended.** One overall number hides exactly
the gap this index exists to surface.

## Example

**Input** — the index committed at the top of
[`scripts/control_baseline_index.py`](scripts/control_baseline_index.py). Edit
the rows and re-run: every count, percentage and verdict below is derived from
them, not hard-coded.

**Output** — the tail of a real run:

```
coverage by era
------------------------------------------------------------------------------
foundation  ##########..........    50%  2 in place, 8 partial, 2 absent  (n=12)
agentic     ##..................    10%  0 in place, 2 partial, 8 absent  (n=10)
overall     ######..............    32%  (n=22)
```

The run continues past this with every absent row, what it needs, and what the
agents changed about it. `test_skills.py` executes the script on every build,
**with no model configured** — so what CI proves is that it runs and refuses
legibly, not that it prints these lines. The output above is a recorded run
against a real model, and nothing re-diffs it: a model's answer is not
reproducible, and this repository does not claim otherwise anywhere it can be
checked.

## Output contract

```json
{
  "index": [{"id": "str", "domain": "str", "control": "str", "era": "str",
             "status": "str", "agent_note": "str", "owns": "str"}],
  "coverage": [{"era": "str", "score": 0.0, "in_place": 0, "partial": 0,
                "absent": 0, "n": 0}],
  "absent": ["str"]
}
```

## Failure modes

- **Indexing only the agentic rows.** The most common failure, and it reports a
  number that is true about the wrong denominator.
- **Scoring against documentation.** A control that exists in a policy and not
  in a running system is absent, whatever the policy says.
- **A blended coverage figure.** 32% overall tells a reader nothing; 50% and 10%
  tells them which programme to fund first.
- **No owner per row.** Coverage measured without ownership regresses silently
  between measurements.
- **Treating a foundation row as unchanged.** Agents did not remove the need for
  change management; they broke the assumption that a human read every change.
