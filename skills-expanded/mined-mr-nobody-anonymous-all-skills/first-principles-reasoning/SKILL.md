---
name: first-principles-reasoning
description: Deconstruct complex problems into fundamental axioms and apply 5-Whys root cause analysis to eliminate cognitive overwhelm.
category: productivity
aliases:
- 5-whys
- root-cause-analysis
- first-principles
- axiomatic-thinking
triggers:
- first principles analysis
- 5 whys root cause
- break this down to first principles
- find the root cause of this
- deconstruct this problem
keywords:
- first-principles
- 5-whys
- root-cause
- axioms
- deconstruct
- diagnostic
- reasoning
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
lifecycle: enabled
capabilities:
- first-principles-deconstruction
- 5-whys-root-cause
- assumption-testing
inputs:
- problem
- assumptions
- symptoms
outputs:
- core_axioms
- root_causes
- fundamental_solutions
permissions:
  filesystem: none
  network: none
  shell: none
  secrets: none
author: Mr-Nobody-Anonymous
tags:
- 5-whys
- axioms
- first
- first-principles
- principles
- productivity
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# First Principles Reasoning

## Purpose
Deconstructs complex, overwhelming challenges down to their foundational truths and axioms, applying iterative 5-Whys diagnostic analysis to isolate true root causes and discard baggage assumptions.

## When to Use
- Facing an intractable bug or systemic architectural bottleneck.
- Challenging entrenched "that's how we've always done it" assumptions.
- Overwhelmed by layers of secondary symptoms or conflicting opinions.
- Designing a greenfield architecture or business workflow from the ground up.

## When NOT to Use
- Routine, well-understood operational tasks with established standard operating procedures.
- When an immediate incident triage requires symptom containment before long-term post-mortem analysis.

## Capabilities
- **Axiomatic Reduction**: Strip away analogies and conventions until reaching verifiable physical/logical facts.
- **5-Whys Root Cause Traversal**: Drill past immediate symptoms to identify the systemic cause.
- **Assumption Invalidation**: Identify hidden assumptions and test their factual validity.
- **Reconstruction from Ground Truth**: Build fresh solutions bottom-up from primary axioms.

## Inputs
- `problem` (required) — Description of the breakdown, limitation, or challenge.
- `observed_symptoms` (optional) — Observable indicators and failure modes.
- `known_assumptions` (optional) — Existing beliefs regarding why the problem exists.

## Workflow
1. State the observable symptom or surface problem clearly.
2. Perform iterative 5-Whys interrogation to peel back proximate causes.
3. List all underlying assumptions and classify each as either a fact or convention.
4. Discard arbitrary conventions and isolate foundational axioms.
5. Reconstruct an optimal solution directly from fundamental axioms.

## Tools
- Analytical reasoning and root-cause tracing frameworks.

## Examples
- "Our build takes 45 minutes; break this down to first principles."
- "Apply 5-whys root cause analysis to our database connection timeouts."
- "Deconstruct our deployment pipeline from foundational truths."

## Safety
- Distinguish between verified empirical facts and unproven hypotheses during root-cause discovery.
- Do not dismantle essential defensive safeguards while stripping conventions.

## Source
Custom skill maintained in this library based on Kaizen and First Principles methodologies.

## Notes
Composes effectively with `development.debugging` and `development.architecture` for high-leverage technical problem solving.
