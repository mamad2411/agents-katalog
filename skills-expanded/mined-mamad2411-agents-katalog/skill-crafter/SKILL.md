---
name: skill-crafter
description: Use this skill when creating a new skill or when modifying, updating, refactoring, restructuring, or reviewing an existing skill. Trigger it for framework-specific and framework-agnostic skill work, including SKILL.md design, folder layout, scripts, references, assets, metadata, and description optimization, even if the user only says "make a skill", "improve this skill", or "refactor the skill".
---

# Skill Crafter

Create and evolve skills in a framework-agnostic way. Treat a skill as a compact, reusable operating guide for another agent, not as user-facing documentation.

## What this skill covers

Use this skill for:

- creating a new skill from scratch
- modifying or extending an existing skill
- refactoring a skill's structure or wording
- improving triggering quality through better descriptions
- adding or revising `scripts/`, `references/`, and `assets/`
- checking whether a skill follows the repository and spec constraints

If the request is only about one downstream artifact inside a skill, still use this skill to keep the skill coherent as a whole.

## Core principles

### Treat context as a limited shared resource

The context window is a public good. A skill competes with the user request, the agent's system instructions, other loaded skills, and any files the agent must read to do the work.

Default assumption: the agent is already capable. Do not spend tokens teaching generic knowledge it already has. Put only the information that is non-obvious, domain-specific, decision-shaping, or easy to get wrong.

A good skill removes repeated rediscovery. A bad skill restates basics, repeats itself, or carries large amounts of background material that rarely changes the outcome.

### Choose the right degree of freedom

Not every task should be specified with the same rigidity.

- High freedom: use prose guidance when many valid approaches exist and judgment matters more than exact sequencing.
- Medium freedom: use structured patterns, checklists, pseudocode, or lightweight templates when a preferred approach exists but some adaptation is expected.
- Low freedom: use scripts, strict templates, or explicit ordered steps when the task is fragile, repetitive, or correctness depends on exact behavior.

Choose the narrowest constraint that improves reliability without making the skill brittle or overfit. A skill should guide the agent, not trap it in needlessly rigid ceremony.

### Use progressive disclosure deliberately

A skill has three practical layers:

- `name` and `description` in frontmatter: always visible before the skill triggers.
- `SKILL.md` body: loaded after the skill is selected.
- `references/`, `scripts/`, and `assets/`: loaded or used only when needed.

This means the `description` carries the triggering burden, `SKILL.md` should contain the core workflow and decision rules, and detailed material should move into `references/` or executable resources. Do not put crucial trigger guidance only in the body, because the body is unavailable before the skill is selected.

### Keep one source of truth per concept

Do not duplicate the same detailed guidance in both `SKILL.md` and `references/`. Repetition bloats context and causes drift.

Use this rule:

- Put always-needed guidance in `SKILL.md`.
- Put detailed standards, schemas, variants, examples, and edge-case catalogs in `references/`.
- Put deterministic reusable logic in `scripts/`.
- Put templates and output resources in `assets/`.

When in doubt, keep the main file lean and link to a single authoritative supporting file.

### Explain why, not only what

Prefer instructions that convey intent and rationale. Modern agents usually perform better when they understand why a rule matters.

Use rigid wording only when strictness is genuinely required. If a behavior matters because of safety, formatting compatibility, trigger reliability, or user expectations, say that. If you can replace a hard-to-generalize command with a decision rule, do it.

### Generalize from examples instead of overfitting to them

Concrete prompts are essential for understanding a skill, but they are not the goal. The goal is to extract reusable workflow, reusable knowledge, and reusable resources from those prompts.

When reviewing examples, ask:

- what decisions repeat across tasks?
- what information has to be rediscovered each time?
- what logic keeps getting rewritten?
- what output structure or quality bar stays stable?

Turn those stable patterns into guidance, references, scripts, or assets. Do not write a skill that only performs well on the handful of prompts used to design it.

### Design the `description` for triggering, not explanation

The `description` field is the primary trigger surface. It should say both what the skill helps do and when the agent should reach for it.

Write the description around user intent, not internal implementation. Include adjacent phrasings and near-synonyms the user might say, even when they do not name the domain directly. Be slightly pushy when necessary so the skill does not under-trigger, but do not make it so broad that it steals unrelated tasks.

All meaningful "when to use this skill" guidance belongs in `description`, not in a body-only section that the agent cannot see before triggering.

### Organize long skills so the main file stays useful

As a skill grows, split material by need rather than by habit.

Common patterns:

- High-level guide plus targeted references: keep the core workflow in `SKILL.md`, and move full technical detail into `references/...`.
- Variant split: when one skill supports multiple frameworks, providers, or domains, keep selection guidance in `SKILL.md` and put each variant in its own reference file.
- Conditional detail: keep the common path in `SKILL.md`, and point to deeper reference material only for specialized cases.

Avoid deeply nested reference chains. Supporting files should usually be one hop away from `SKILL.md`.

### Exclude non-essential project documentation

A skill should contain only the files that help another agent do the task. Do not add auxiliary project documentation unless the user explicitly asks for it.

Common examples to avoid:

- `README.md`
- `INSTALLATION_GUIDE.md`
- `QUICK_REFERENCE.md`
- `CHANGELOG.md`
- process notes about how the skill was authored
- setup walkthroughs that are not part of the skill's actual operating guidance

## Workflow

Follow this sequence unless the user clearly wants only one step.

1. Capture the skill's purpose from concrete user tasks, example prompts, target outputs, and likely trigger phrases.
2. Identify the stable patterns across those examples: repeated decisions, repeated logic, repeated reference material, and repeated output expectations.
3. Choose the smallest reusable scope that solves those tasks repeatedly without overfitting to a narrow prompt set.
4. Decide what belongs in `SKILL.md` versus `references/`, `scripts/`, and `assets/`.
5. Draft or revise `SKILL.md` so the frontmatter triggers reliably and the body stays procedural.
6. Add bundled resources only when they remove repeated effort or improve reliability.
7. Validate the result against the skill specification and naming/layout rules.
8. If triggering quality matters, optimize the `description` with realistic near-match prompts.

## Writing rules

- Write for another capable agent, not for a beginner human reader.
- Prefer imperative instructions and clear decision rules.
- Keep `SKILL.md` focused on the operating model: workflow, choices, constraints, and file navigation.
- Move long standards, schemas, or examples into `references/`.
- Use examples to clarify a pattern, not to dominate the file.
- If a rule exists for a reason that is not obvious, explain the reason.

## Resource planning

Use this quick placement test:

- Put it in `SKILL.md` if the agent must know it every time the skill triggers.
- Put it in `references/` if it is important but only sometimes needed.
- Put it in `scripts/` if the same logic would otherwise be rewritten or must be exact.
- Put it in `assets/` if it is a template, fixture, or output resource rather than reading material.

## Script standard

When you create a Python script for a skill, prefer a self-contained executable file that can run directly with `uv run`.

Requirements:

- Use PEP 723 inline dependency metadata when the script has non-stdlib dependencies.
- Make the script runnable as `uv run path/to/script.py ...`.
- Keep dependencies local to the script instead of requiring a separate package install when practical.
- Emit concise, agent-friendly stdout and actionable errors.
- Handle common edge cases and invalid inputs explicitly.

Use `assets/uv_script.py` as the starting template when helpful. See `references/script_standards.md` for more detail.

## Description optimization

The `description` field is the primary trigger surface. Write it to describe both:

- what the skill helps do
- when the agent should load it, based on user intent

Bias toward slightly pushy but accurate wording. Include adjacent phrasings a user might say even when they do not name the domain directly.

When refining descriptions:

- test with realistic should-trigger and should-not-trigger prompts
- prefer near-miss negatives over obviously unrelated negatives
- revise based on general intent categories, not one-off keywords
- keep the final text within spec limits

See `references/optimizing_descriptions.md` for the detailed loop.

## Detailed references

Load these only when needed:

- `references/specification.md` for the detailed skill format and limits
- `references/optimizing_descriptions.md` for trigger-quality guidance
- `references/script_standards.md` for Python script expectations with PEP 723 and `uv run`

## Output expectations

When delivering a new or updated skill:

- ensure the folder name matches the skill name
- ensure frontmatter fields are valid and concise
- ensure the body tells the agent how to proceed, not just what the topic is
- ensure references are explicitly discoverable from `SKILL.md`
- ensure scripts and assets exist only when they materially help
- ensure the final structure follows the rules in `references/specification.md`

If you are unsure about a format constraint, consult `references/specification.md` before inventing a local convention.
