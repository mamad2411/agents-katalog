---
name: agent-supply-chain-assessment
description: >-
  Score new packages and MCP connectors for typosquatting and ordinary
  supply-chain signals, then re-score them weighted by the authority the agent
  that loads them runs with. Use when an agent installs its own dependencies or
  connects to a server somebody added last week.
allowed-tools: Read, Grep, Glob
---

# The same package is a different risk inside an agent

Supply-chain assessment for agents differs in one term: the artefact runs with
the agent's authority. A connector that trips three ordinary signals is a
review; the same connector loaded by an agent holding production credentials is
a block. Weighting by authority is what turns the ordinary assessment into the
right answer.

## When to use this

When an agent can install packages, when an MCP server is added, and at any
review of what a coding agent is allowed to pull.

## Procedure

**1 — Establish the known-good set.** The packages this project actually uses.
Typosquat detection is a comparison against something; without the set it is a
spell-check.

**2 — Score edit distance against known-good names.** A distance of one or two
from a popular package, with a recent first-publication date, is the classic
shape. Report the package it imitates, not just the score.

**3 — Apply the ordinary signals.** Age, maintainer count, download history,
whether it was published after the agent asked for it, install scripts.

**4 — Re-score weighted by agent authority.** What credentials are in the
environment the artefact will execute in, and what the agent can reach. This is
the step that moves a review to a block and it needs no new information.

**5 — Report the two verdicts side by side.** Unweighted and authority-weighted.
The difference is the argument for gating what agents may install, and it is
easier to make with both numbers present.

## Example

**Input** — the fixture committed at the top of [`scripts/agent_supply_chain_assessment.py`](scripts/agent_supply_chain_assessment.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
requests==2.31.0        allow
requsts==2.31.0         block
      · unsigned — no attestation to source
      · published 3d ago — no soak time
      · only 12 downloads
      · distance 1 from popular package 'requests'
colourama==0.4.6        block
      · unsigned — no attestation to source
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
  "known_good": ["str"],
  "artefacts": [{"name": "str", "kind": "package|mcp", "distance": 0, "imitates": "str|null",
                 "signals": ["str"], "verdict": "allow|review|block"}],
  "authority": {"credentials_present": ["str"], "reachable": ["str"]},
  "weighted": [{"name": "str", "verdict": "allow|review|block", "moved": true}]
}
```

## Failure modes

- **Typosquat detection with no known-good set.** Everything is close to
  something.
- **Assessing the package and not the environment.** The authority is the term
  that differs.
- **Treating an MCP connector as configuration.** It is code that runs with the
  agent.
