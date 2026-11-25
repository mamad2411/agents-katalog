---
name: tier-1-2-3-skill-system
description: Use when creating, editing, reviewing, packaging, or organizing AI-agent skills and deciding whether a skill should be text-only, script-backed, or backed by an ML/specialist pipeline.
version: 1.0.0
author: Hasan Ali
license: MIT
metadata:
  tags:
    - ai-agents
    - skills
    - skill-design
    - automation
    - ml-pipeline
  related_skills:
    - recursive-agent-improvement
  related_repositories:
    - https://github.com/H-Ali13381/recursive-agent-improvement
---

# Tier 1-2-3 Skill System

## Overview

Use this skill to choose the lightest reliable shape for an AI-agent skill.

A skill is reusable operational knowledge. It should reduce future steering, capture real pitfalls, and make repeatable work more reliable. It should not become a bloated prompt dump or a session diary.

Core rule: start simple, then promote only when the workflow proves it needs more machinery.

## When to Use

Use this when:

- Creating a new agent skill.
- Reviewing or cleaning up an existing skill.
- Deciding whether a workflow belongs in plain instructions, scripts, or a specialist model.
- A skill is becoming too long, vague, or hard to operate.
- Agents keep rewriting the same helper code for the same task.
- A task needs perception, scoring, ranking, detection, or classification that the base agent cannot do reliably.

Do not use this to justify overbuilding. The default answer is the lowest tier that works.

## The Three Tiers

| Tier | Shape | Use when | Upgrade trigger |
|---|---|---|---|
| 1. Text-only | `SKILL.md` | The value is judgment, policy, sequencing, taste, style, or a checklist. | Agents repeatedly rewrite glue code or make mechanical mistakes. |
| 2. Text + script | `SKILL.md` + `scripts/` | The workflow has deterministic, repeatable mechanics: parse, validate, convert, audit, launch, package, benchmark, or export. | Scripts and prompts cannot provide the missing perception, ranking, scoring, detection, or domain inference. |
| 3. Text + script + ML pipeline | `SKILL.md` + `scripts/` + training/eval/model artifacts | The agent needs a non-native capability: classifier, detector, reranker, scorer, evaluator, verifier, or specialist model. | The specialist is stable enough to package as a tool, MCP server, CLI, or standalone skill. |

Short version:

- Tier 1 teaches the agent what to do.
- Tier 2 gives the agent deterministic machinery to do it.
- Tier 3 gives the agent a new sense organ.

## Tier 1: Text-only

Use Tier 1 when the hard part is judgment.

Good fits:

- Writing voice
- Review philosophy
- Research synthesis
- Design principles
- Safety rules
- Operational checklists

Keep the skill focused on:

- Trigger conditions
- Decision rules
- Common mistakes
- Verification checklist
- One or two concrete examples

Avoid adding scripts when the agent only needs better taste, sequencing, or policy.

## Tier 2: Text + Script

Use Tier 2 when the skill would otherwise make agents keep inventing the same glue code.

Good fits:

- File validation
- Format conversion
- Skill packaging
- Report generation
- Project audits
- Benchmark aggregation
- Repeatable setup or launch commands

Rules:

- `SKILL.md` explains when, why, and how to call the script.
- `scripts/` does the deterministic work.
- Scripts should be idempotent where practical.
- Scripts should expose flags or environment variables instead of requiring edits.
- Scripts should verify success before exiting 0.
- Scripts should avoid logging secrets.
- Bulky rationale belongs in `references/`, not the main skill body.

Promotion signal: if an agent writes the same helper script twice, make it a bundled script.

## Tier 3: Text + Script + ML Pipeline

Use Tier 3 when the base model lacks a measurable capability and ordinary scripts cannot fill the gap.

Good fits:

- Wakeword/audio detection
- Screenshot or layout scoring
- UI/theme coherence judging
- Search reranking
- Patch-risk classification
- Fact-consistency verification
- Domain-specific extraction
- Anomaly detection

Rules:

- Define inputs, outputs, metrics, and baselines before training.
- Include hard negatives and failure cases.
- Keep inference compact and machine-readable, preferably JSON.
- Explain when to trust the specialist and when to abstain.
- Explain how the specialist output changes the agent's next action.
- Add an eval plan and model card before publishing a specialist model.

Promotion signal: the missing piece is perception, ranking, scoring, detection, classification, or domain inference.

## Related Skill

Use `recursive-agent-improvement` when the decision reaches Tier 3 and the agent needs to turn a measurable failure into a specialist tool, evaluator, reranker, classifier, detector, verifier, or ML training pipeline. This skill chooses the lightest reliable shape; `recursive-agent-improvement` builds the Tier 3 capability.

Repo: https://github.com/H-Ali13381/recursive-agent-improvement

## Decision Checklist

Before writing or changing a skill, ask:

1. Is this durable operational knowledge?
2. Will it reduce future steering?
3. Which tier is the lightest reliable fit?
4. Can this be consolidated with an existing skill?
5. Is repeated mechanical work better handled by a script?
6. Is the missing capability actually ML-shaped and measurable?
7. What verification proves the skill works?

## Example

```text
Task: Package a repeated workflow as a public agent skill.

Decision:
- If the hard part is judgment, sequencing, policy, or style, keep it Tier 1 with only SKILL.md.
- If agents keep rewriting the same validation, conversion, audit, launch, or packaging code, promote it to Tier 2 and add a `scripts/` directory.
- If the workflow needs a measured classifier, detector, reranker, scorer, evaluator, verifier, or specialist model, promote it to Tier 3.

Verification:
- The selected tier is the lightest reliable shape.
- The SKILL.md description says when to use the skill.
- Any referenced scripts, references, assets, models, or eval docs exist.
```

## Common Mistakes

- Writing a giant prompt when a small checklist would do.
- Creating many overlapping skills instead of one clear router skill.
- Making agents rewrite deterministic code that should be scripted.
- Adding ML because it sounds impressive, not because the task has a measurable capability gap.
- Putting private paths, secrets, or session-specific history into public skill docs.
- Treating a skill as a completed-work log instead of reusable operational knowledge.

## Error Handling

- If the tier is unclear, choose the lower tier and write down the concrete upgrade signal.
- If a Tier 1 skill keeps causing repeated mechanical mistakes, add or reference a tested script instead of expanding the prompt.
- If a Tier 2 script fails, fix the script, expose clearer flags, and make the failure machine-readable before adding more prose.
- If Tier 3 has no metrics, eval set, or abstention rule, do not publish the model-backed version yet.
- If validation fails, fix frontmatter, broken file references, hardcoded paths, or missing supporting files before sharing.

## Verification

Before publishing a skill shaped by this model:

- Confirm the frontmatter has at least `name` and `description`.
- Confirm the description says when to use the skill, not just what it contains.
- Confirm the main `SKILL.md` is lean enough to scan.
- Confirm any referenced scripts or files exist.
- Confirm scripts have safe defaults and success/failure signals.
- Confirm Tier 3 models have documented inputs, outputs, metrics, and limitations.

Final rule: do not overbuild. The strongest skill system is lean at the top, mechanical where needed, and ML-backed only when the payoff is real.
