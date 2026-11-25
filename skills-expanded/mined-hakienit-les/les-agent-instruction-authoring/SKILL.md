---
name: les-agent-instruction-authoring
description: Create or revise agent-facing instructions, skills, rules, and context pointers with explicit triggers, boundaries, and evidence contracts.
invocation: user
maturity: stable
route: instruction-authoring
profile: core
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/task-lifecycle.md","../../policies/rules/ai-authority.md","../../policies/rules/documentation.md","../../policies/rules/file-organization.md","../../policies/rules/definition-of-done.md"]
---

# Agent Instruction Authoring

## Invoke

Bootstrap LES when the requested change alters what an agent loads, invokes,
decides, mutates, verifies, or reports.

## Inputs

Behavior goal, target instruction type, trigger branches, authority boundary,
context budget, output contract, and verification scenario.

## Procedure

1. Resolve the canonical owner and invocation mode. Done when: no duplicate source of truth or accidental auto-trigger exists.
2. Write the smallest useful pointer and ordered steps. Done when: every branch has a clear trigger, completion criterion, and stop condition.
3. Add near-miss and unauthorized behavior coverage. Done when: the instruction cannot silently widen scope or authority.
4. Validate package, references, and realistic behavior. Done when: paths resolve, stale wording is removed, and evidence is recorded.
5. For a substantial behavior change, pressure-test the old and new instruction in an isolated disposable scenario. Done when: the new rule closes a demonstrated failure without widening unrelated behavior.

## Output

Instruction change record with owner, trigger, invocation, authority, context cost,
behavior fixtures, verification results, and terminal status.

## Guardrails

Do not duplicate policy in skills. Do not make a skill implicitly invokable when
the user must explicitly authorize it. Do not add generic advice that changes no
decision.

## Verification

Check frontmatter, references, positive/near-miss/stop fixtures, package registry,
and one realistic request. For substantial changes, compare a baseline pressure
scenario with the updated behavior. Keep claims evidence-bound.
