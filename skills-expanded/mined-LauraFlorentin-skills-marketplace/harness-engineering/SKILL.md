---
name: harness-engineering
description: Design the context, constraints, tools, observability, and evaluation system around an AI agent. Use for agent architecture, repository instructions, multi-agent coordination, failure prevention, production reliability, evaluation datasets and metrics, cost or latency measurement, safety gates, or harness tradeoffs.
---

# Harness Engineering

A harness is the environment around an agent: the information it receives, tools and permissions it has, state it preserves, checks it runs, and evidence used to judge outcomes. Design it around observed failure modes and user authority, not around a universal scaffold.

## Design sequence

1. Define the task, user, success criteria, unacceptable outcomes, and decision authority.
2. Map required context and its source of truth. Load stable global guidance early and task-specific detail only when relevant.
3. Give the agent the smallest tool set that can complete the task, with clear mutation and approval boundaries.
4. Encode deterministic constraints mechanically where possible; keep judgment calls in concise instructions.
5. Preserve state needed for handoff, audit, recovery, and reproducibility without collecting unnecessary sensitive data.
6. Evaluate end-to-end behavior on representative and adversarial cases.
7. Monitor quality, cost, latency, safety, and drift; revise the harness from observed evidence.

## Context architecture

Use a layered information model:

- a short repository or system map for stable entry points and invariants;
- authoritative design, policy, API, and operational documents;
- task-scoped plans and acceptance criteria;
- runtime state and retrieved evidence with provenance and freshness.

Prefer links and conditional loading over duplicated prose. Resolve contradictions explicitly. See [context-engineering.md](references/context-engineering.md).

## Constraints and control

Classify actions by reversibility, scope, and consequence. Require stronger confirmation for external communication, deployment, money movement, access-control changes, deletion, and destructive Git operations. A hook that silently “recovers” by stashing or reverting can destroy or hide user work; warning and permission-gating hooks are safer defaults.

Use architectural checks, schemas, tests, linters, type systems, policy engines, and sandboxing for rules that can be verified deterministically. Avoid long instruction lists for conditions tooling can enforce.

For value priorities, human oversight, and escalation design, see [alignment.md](references/alignment.md).

## Evaluation

Measure the behavior the user experiences, not only isolated model output. An evaluation suite may include:

- task completion and correctness;
- groundedness and source quality;
- permission and policy compliance;
- regression and consistency across paraphrases;
- tool-choice and recovery behavior;
- latency and cost distributions;
- human escalation quality;
- robustness to missing, conflicting, or adversarial context.

Keep a versioned dataset, deterministic runner, recorded model and harness configuration, scoring definitions, and comparable report. Use human review for subjective or consequential criteria and calibrate model judges before relying on them. See [evaluation-framework.md](references/evaluation-framework.md).

## Common failure modes

- global instructions contain every detail and crowd out the task;
- multiple documents claim to be the source of truth;
- acceptance criteria describe implementation rather than observable behavior;
- hooks mutate Git or external systems without user authority;
- the same model output is used as both answer and uncalibrated judge;
- metrics optimize a proxy while missing usefulness or safety;
- traces collect secrets or personal data without a retention policy;
- multi-agent locks and ownership are ambiguous;
- static benchmarks are treated as permanent evidence.

## Output

When designing a harness, return:

1. task and risk model;
2. context sources and loading rules;
3. tools, permissions, and approval boundaries;
4. state and handoff model;
5. deterministic checks and human review gates;
6. evaluation plan and metrics;
7. rollout, monitoring, and rollback plan;
8. open assumptions and tradeoffs.

Recommend components proportionate to the observed need. Do not scaffold files or integrations unless the user asks for implementation.
