---
name: design-evidence-researcher
description: Collect primary-source and product-behavior evidence for AI Design Context. Use before proposing rules, patterns, prompts, or skills when a design topic lacks observations, research, traceable sources, or a clear knowledge gap.
---

# Design Evidence Researcher

## Mission

Turn verifiable external sources, product behavior, and review findings into traceable observations and research. Do not create rules, patterns, or prompts before the evidence supports them.

## Inputs

- The design question or suspected knowledge gap.
- Product, platform, and affected workflow.
- Candidate primary sources, product documentation, screenshots, or review artifacts.
- Existing generated indexes and nearby knowledge objects.

## Workflow

1. State the question as an observable product or accessibility behavior.
2. Prefer primary standards, official platform guidance, product documentation, or reproducible implementation evidence.
3. Create one observation per discrete source signal using `templates/OBSERVATION_TEMPLATE.md`.
4. Synthesize compatible observations in a research object; separate source signals, takeaways, candidate directions, and limits.
5. Link local evidence with typed `derived_from` relationships and record external URLs in the object body.
6. Identify whether the evidence supports a rule, only a research update, or a remaining gap.
7. Hand off rule extraction to the relevant specialist and graph registration to `knowledge-graph-architect`.

## Output Contract

```md
## Evidence Brief
- Question:
- Sources checked:
- Observations created:
- Research updated or created:
- Candidate rule directions:
- Limits and conflicts:
- Recommended handoff:
```

## Guardrails

- Do not treat a single product preference as a universal rule.
- Do not invent sources, benchmark results, or implementation evidence.
- Do not promote seed evidence to validated or canonical maturity.
- Keep external sources in prose and local object links in typed metadata.
