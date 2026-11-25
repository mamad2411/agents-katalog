---
name: les-prototyping
description: Build a bounded throwaway probe to answer a design, state, interaction, or integration question before production implementation.
invocation: model
maturity: stable
route: prototype
profile: core
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/task-lifecycle.md","../../policies/rules/change-scope.md","../../policies/rules/coding-quality.md","../../policies/verification.md"]
---

# Prototyping

## Invoke

Bootstrap LES when a small executable probe can answer a concrete uncertainty
faster than committing to production structure.

## Inputs

Question to answer, smallest useful surface, throwaway boundary, success signal,
and cleanup location.

## Procedure

1. State the question and stop condition. Done when: one observable result distinguishes viable from non-viable.
2. Build the smallest isolated probe using existing seams. Done when: production code and project state remain protected.
3. Exercise normal and failure cases. Done when: the result is reproducible and limitations are recorded.
4. Delete or quarantine the probe and report the decision. Done when: no temporary artifact is mistaken for production behavior.

## Output

Prototype result with question, probe boundary, evidence, limitations, decision,
and cleanup confirmation.

## Guardrails

Prototype code is not production approval. Do not add dependencies, migrations,
public interfaces, or persistent configuration for a probe without authorization.

## Verification

Run the probe, capture the decisive output, verify cleanup, and mark unresolved
questions rather than generalizing beyond the evidence.
