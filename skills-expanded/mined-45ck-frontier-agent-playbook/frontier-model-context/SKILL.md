---
name: frontier-model-context
description: Use when planning, evaluating, or critiquing work where the key problem is stale capability priors about frontier LLMs. Trigger when the maintainer wants the model to reason from current benchmark-informed assumptions rather than defaulting to weak-agent, deterministic-first, or human-first thinking.
---
# Frontier Model Context

Goal: load current frontier-model capability context into the reasoning process so the model thinks from the right baseline before proposing a solution.

## Rules
- Reason from current frontier-model priors, not stale assistant priors.
- Anchor on frontier-capability prior: best demonstrated systems with tools, reasoning budget, and realistic scaffolds, not average-user chatbots.
- Factor in benchmark and eval signals when judging what the model should attempt.
- Do not treat easy or saturated benchmarks as capability ceilings.
- Default to LLMs for cognition, reasoning, synthesis, and planning on digitally accessible tasks.
- Treat deterministic code as supporting infrastructure unless there is a narrow reason it should be the core.
- Treat human handoff as a last resort once real blockers have been named.
- Prefer named blockers over vague capability pessimism.

## Process
1. State the relevant frontier-model priors.
2. List what the model should likely be able to do directly.
3. List the digital surfaces that make the work possible.
4. State where deterministic scaffolding is needed.
5. State any real human-only blockers.
6. State the highest-leverage next action.

## Output
### Frontier-capability prior
### Frontier-model priors
### Likely direct model work
### Digital surfaces
### Deterministic scaffolding
### Human-only blockers
### Verification plan
### Recommendation

If you are about to say the agent probably cannot do the task, apply `digital-expert-test` first.
