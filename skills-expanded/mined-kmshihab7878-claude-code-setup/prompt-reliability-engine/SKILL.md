---
name: prompt-reliability-engine
description: >
  9-mode prompt reliability framework: diagnose, repair, stress-test, constrain, lock, architect,
  audit, prune, and self-improve prompts, skills, and workflows. Treats prompting as engineering.
risk: low
tags: [process, quality, testing, meta, skills]
created: 2026-03-25
updated: 2026-03-25
---

# Prompt Reliability Engine

Use this skill to make prompts, skills, and workflows production-grade through diagnosis, repair, stress testing, constraints, output locking, workflow design, audit, pruning, and self-improvement.

## Invocation Triggers

- Weak, failing, inconsistent, or under-specified prompt.
- New skill, command, workflow, or reusable instruction set.
- Prompt outputs drift in format, tone, length, naming, or structure.
- User asks whether a prompt is production-ready.
- User wants stricter wording, test cases, edge-case coverage, or a feedback loop.

Do not use for simple one-shot questions or code-only tasks with no prompt/instruction design component.

## Core Workflow

1. Identify the target: prompt, skill, command, workflow, or output contract.
2. Select one or more modes from the routing table.
3. Diagnose before repairing.
4. Convert vague goals into observable constraints.
5. Stress-test important artifacts with normal, minimal, ambiguous, adversarial, and off-scope inputs.
6. Lock output shape when consistency matters.
7. Report evidence, risks, and remaining failure modes.

## Mode Routing

| Mode | Use When | Required Output |
|---|---|---|
| 1 Failure Repair | Prompt is broken or underperforming | Diagnosis, root causes, fixed prompt, retest matrix |
| 2 Skill Builder | Build a reusable prompt/skill/workflow | Goal, risks, production artifact, safeguards, tests |
| 3 Stress-Test | Determine breakability | Adversarial input set, failure log, severity, score |
| 4 Constraint Engineer | Instructions are vague | Before/after constraints and consistency score |
| 5 Output Lock | Outputs drift | Fixed sections, order, limits, allowed/forbidden content |
| 6 Workflow Architect | One prompt should become a pipeline | Phases, handoff formats, checkpoints |
| 7 Production Audit | Decide readiness | 5-dimension scorecard and priority fixes |
| 8 Language Pruning | Wording is soft or bloated | Flagged phrases, tightened version, word-count delta |
| 9 Self-Improving Skill | Artifact will be reused | Failure log schema and improvement cycle |

See [modes.md](references/modes.md) for full mode procedures.

## Reliability Rules

- Preserve original business goal, scope, audience, and required tone unless those are the problem.
- Fix root causes, not cosmetic symptoms.
- Make constraints measurable.
- Name output sections and order when format stability matters.
- Expose weaknesses before proposing fixes in stress-test mode.
- Keep uncertainty when truthfully required; remove hedging that weakens instructions.
- Apply existing anti-slop and public-safety rules from the active repo policy.

## Mode Selection

- Broken prompt: Failure Repair -> Constraint Engineer -> Output Lock -> Audit.
- Build from scratch: Skill Builder -> Stress-Test -> Output Lock -> Audit.
- "Is this good enough?": Stress-Test -> Audit.
- Inconsistent outputs: Output Lock -> Constraint Engineer -> Language Pruning.
- Reusable system: Workflow Architect -> Self-Improving Skill.
- Stricter wording: Language Pruning.

If unspecified, infer the mode and state it briefly.

## Output Expectations

- Mode selected and why.
- Diagnosis before rewrite.
- Revised prompt/skill/workflow only when repair/build is requested.
- Test or stress matrix for important systems.
- Reliability score or readiness score when auditing.
- Remaining risks and next recommended fix.

## Reference Map

| Need | Read |
|---|---|
| Full procedures for Modes 1-9 | [modes.md](references/modes.md) |
| Mode selection algorithm and failure pattern library | [selection-and-failure-patterns.md](references/selection-and-failure-patterns.md) |
| Testing protocol and prompt engineering standards | [testing-and-standards.md](references/testing-and-standards.md) |
| Integration points and cross-references | [integrations.md](references/integrations.md) |
