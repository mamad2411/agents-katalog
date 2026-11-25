---
name: interactive-prototype
description: Build or specify a minimal interactive product prototype from a testable prototype question. Use when interaction, state, timing, or behavior must be experienced to gather evidence. Do not use for production implementation or purely visual mockups that require no interaction.
---

# Interactive Prototype

Create the smallest runnable artifact that exposes the target behavior and preserves the product decisions already made.

## Before building

Require or infer a precise prototype question, audience, required fidelity, critical states, evidence plan, and stop rule. If these are missing and would materially change the artifact, route to `prototype-question` first.

Inspect available product context, conceptual model, design system, existing code, and prototype tools. Reuse an existing artifact when it can answer the question with a smaller change. Choose an available implementation method; do not require a particular external engine.

## Build for evidence

- Implement only the critical path and states required by the question.
- Make loading, empty, error, success, permission, and recovery states real when they affect the decision.
- Label simulated data or behavior; isolate it from production systems.
- Preserve the user's confirmed terminology, constraints, hierarchy, and interaction intent.
- Add only the minimum instrumentation or observation hooks needed for the evidence plan.
- Keep the artifact easy to reset and share with intended reviewers or participants.

## Handoff

Return the runnable artifact or implementation path, how to operate it, what is simulated, known limitations, the evidence to collect, and the stop rule. After testing, route observations to `learning-loop-readout` rather than treating completion as validation.

## Boundaries

- Do not silently expand a prototype into production architecture.
- Do not add accounts, payments, destructive actions, live customer data, or external publication without explicit authorization.
- Do not polish unrelated surfaces after the prototype can already answer its question.
- Do not claim usability, desirability, or feasibility without observed evidence.
