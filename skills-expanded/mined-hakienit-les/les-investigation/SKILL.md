---
name: les-investigation
description: Investigate uncertain causes or system behavior with evidence-ranked hypotheses before editing.
invocation: model
maturity: stable
route: investigation
profile: core
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/investigation.md","../../policies/rules/context-loading.md","../../policies/rules/error-handling.md"]
---

# Investigation

## Invoke

Inherit `../les-bootstrap/SKILL.md` and the investigation workflow.

## Inputs

Observed symptom, context, and available evidence.

## Procedure

1. Build a tight, red-capable reproduction or characterization. Done when: one command can detect the user's exact symptom or the absence of a valid seam is recorded.
2. Rank 3–5 falsifiable hypotheses with predictions. Done when: each hypothesis has a discriminating observation.
3. Run read-only probes one variable at a time. Done when: supporting and conflicting evidence changes the ranking or bounds uncertainty.
4. State root cause confidence and next safe action. Done when: facts, inference, and unresolved questions are separated.

## Output

Hypothesis report with evidence, impact, and terminal status.

## Guardrails

Do not mutate the system or represent inference as fact.

Use `COMPLETE` when the requested read-only characterization, ranked
hypotheses, and next safe action are recorded, even if the root cause remains
uncertain. Use `PENDING_USER_ACTION` only when an owner decision or approval is
required; use `BLOCKED` when required context or a safe probe is unavailable.

## Verification

Include the reproduction command, supporting and conflicting observations, probes
run, cleanup status, selected cause confidence, and the next safe action. This
skill authorizes diagnosis, not the fix.

Bootstrap LES, then load `../../policies/workflows/investigation.md` and the
context-loading and error-handling rules. Output observed facts, ranked causes,
conflicting evidence, impact, and the next safe action. This skill authorizes
read-only diagnosis, not implementation.
