---
name: swarmfusion
description: Orchestrate multi-agent coding workflows with SwarmFusion. Use when the user asks for SwarmFusion, multi-agent orchestration, a swarm of agents, an agent council/review board, agent debate, mixture of agents, majority voting between agents, or an autonomous RARV loop on a spec.
---

# SwarmFusion

SwarmFusion is a multi-agent orchestration system built on the Swarms
framework. It provides an autonomous RARV loop, a blind review council,
deterministic verification gates, named swarm pipelines, and persistent
cross-run memory. All runtime artifacts live under `.swarmfusion/` in the
working directory.

## Prerequisites

- Python 3.10+ with `pip install swarms`
- An LLM API key exported (OPENAI_API_KEY, ANTHROPIC_API_KEY, or any
  LiteLLM-supported provider)
- Run all CLI commands from the plugin root (`${CLAUDE_PLUGIN_ROOT}`), or
  set PYTHONPATH to it, so `sfcore` is importable.

## Capabilities and when to use each

| Need | Use |
|---|---|
| Autonomous spec-to-done loop | `python -m sfcore.cli run <spec>` |
| Research -> implement -> review pipeline | `python -m sfcore.cli swarm pipeline "<task>"` |
| Many perspectives merged into one answer | `python -m sfcore.cli swarm moa "<task>"` |
| Adversarial evaluation of a decision | `python -m sfcore.cli swarm debate "<motion>"` |
| Discrete decision with noise reduction | `python -m sfcore.cli swarm vote "<question>"` |
| Manager delegates to specialists | `python -m sfcore.cli swarm hierarchy "<task>"` |
| Trustworthy review of a change | `python -m sfcore.cli council --diff` |
| Deterministic pass/fail evidence | `python -m sfcore.cli verify` |
| A plan before building | `python -m sfcore.cli plan "<task>"` |
| See what happened | `python -m sfcore.cli status` |

## Core loop: RARV

`run` iterates Reason (architect plans), Act (implementer executes),
Reflect (reviewer critiques, declares STATUS: COMPLETE or CONTINUE), and
Verify (deterministic gates). Findings are injected into the next
iteration. The loop stops on COMPLETE with a non-BLOCKED verdict, or at
the iteration cap. Artifacts: `.swarmfusion/runs/<run-id>/`.

## Review council discipline

The council is blind (reviewers never see each other), requires unanimous
APPROVE, and on unanimous approval a devil's advocate attacks the
consensus. A BLOCK verdict means: fix the findings, then re-run the whole
council. Never accept 2-of-3.

## Verification discipline

`verify` produces `VERIFIED`, `CONCERNS`, or `BLOCKED` from reproducible
gates only (diff, secret scan, debt scan, tests, lint). Inconclusive
evidence is never upgraded to VERIFIED. Configure project commands with
`SF_TEST_COMMAND` and `SF_LINT_COMMAND`.

## Memory

Every run writes an episode; recurring findings become semantic patterns.
Memory is injected into future plans automatically. Store a lesson
explicitly with:

```
python -m sfcore.cli memory add-pattern --text "<lesson>"
```

## Configuration (environment variables)

| Variable | Default | Purpose |
|---|---|---|
| SF_PLANNER_MODEL | gpt-4.1 | Architect/planner/synthesizer model |
| SF_WORKER_MODEL | gpt-4.1 | Implementer/researcher/tester model |
| SF_REVIEWER_MODEL | gpt-4.1 | Reviewer/devil's advocate model |
| SF_FAST_MODEL | gpt-4.1-mini | Cheap parallel workers/voters |
| SF_MAX_ITERATIONS | 5 | RARV iteration cap |
| SF_COUNCIL_SIZE | 3 | Number of council reviewers |
| SF_DEVILS_ADVOCATE | 1 | Devil's advocate on unanimous approve |
| SF_TEST_COMMAND | (unset) | Test gate command |
| SF_LINT_COMMAND | (unset) | Lint gate command |
| SF_BASE_REF | main | Verify base git ref |
| SF_WORKSPACE | .swarmfusion | Artifact directory |

## Extending with the Swarms framework directly

For architectures beyond the named pipelines, write a Python script using
`from swarms import Agent, SwarmRouter, GraphWorkflow, ...` and reuse
`sfcore.factory.build_agent` for consistent role prompts and model tiers.
See `examples/` in the plugin for runnable templates.
