# Motion Fundamentals

## Purpose

Foundational vocabulary, purpose, and constraints for purposeful motion.

## Problem Statement

Unstructured motion can obscure state, reduce accessibility, create visual inconsistency, and consume performance budgets.

## Engineering Principles

- Motion communicates change and hierarchy.
- Motion is purposeful, interruptible, and proportionate.
- Accessibility and performance are acceptance criteria.
- Decisions remain provider-independent.

## Core Concepts

Intent, state, continuity, timing, spatial relationships, feedback, preference, and measurable quality.

## Decision Framework

Choose the least expressive motion that clearly communicates the change, then verify inclusive alternatives and performance impact.

## Design Considerations

Consider user intent, context, hierarchy, interruption, viewport, input modality, reduced-motion preference, and failure recovery.

## Architecture Guidance

Define motion roles and boundaries separately from interface implementation. Record invariants, alternatives, and review evidence.

## Best Practices

- Establish explicit intent before selecting motion.
- Prefer consistent roles and predictable state transitions.
- Provide non-motion equivalents where needed.
- Test representative content and constrained devices.

## Common Mistakes

- Adding motion decoratively.
- Coupling meaning only to movement.
- Ignoring interruption, preference, or reduced-motion behavior.
- Treating a visual effect as a system standard.

## Anti-patterns

- Unbounded motion.
- Motion that blocks task completion.
- Inconsistent timing for equivalent states.
- Provider-specific decisions in the architecture layer.

## Review Checklist

- Is intent explicit?
- Is state understandable without motion?
- Are accessibility and performance addressed?
- Is the decision compatible with the motion system?

## Quality Checklist

- Clear
- Consistent
- Inclusive
- Measurable
- Provider-independent

## Related Skills

- official.frontend.accessibility
- official.frontend.frontend-performance
- official.foundation.testing-fundamentals

## Compatible Agents

Motion, Frontend, Architecture, Testing.

## Compatible Sub-Agents

motion-motion-architecture.

## Primary Owner Agent

Motion.

## Primary Owner Sub-Agent

motion-motion-architecture.

## Secondary Owners

Frontend, Architecture, Testing.

## Consumer Agents

Frontend, Architecture, Testing, Presentation.

## Prerequisites

Approved requirements, interaction states, and relevant constraints.

## Expected Outcomes

A documented motion decision that is coherent, accessible, performant, and reviewable.

## Version History

- 1.0.0 — Initial Official OniRoute release.
