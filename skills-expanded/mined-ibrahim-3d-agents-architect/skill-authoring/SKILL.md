---
name: skill-authoring
description: Write, refactor, or improve Claude Code / Claude skill files (SKILL.md). Use when the user asks to "create a skill", "write a SKILL.md", "add a skill for X", "make Claude better at Y", "turn this into a skill", "optimize skill triggers", "my skill isn't firing", or when building any reusable capability that Claude should auto-invoke on matching prompts. Covers trigger-phrase engineering, progressive disclosure, reference-library pattern, scripts, and eval design.
---

# Skill Authoring

You write SKILL.md files that follow Anthropic's skill-creator best practices. A skill is a folder (`skills/<name>/`) containing `SKILL.md` plus optional `reference.md`, `scripts/`, and examples.

## Anatomy of a good SKILL.md

1. **Frontmatter** — `name` (kebab-case, matches folder) and `description` (the single most important field; this is what the model matches against at runtime).
2. **Body** — instructions the model loads WHEN the skill fires. Keep it tight. Push long content into `reference.md` or sibling files loaded on demand.

## Description engineering (the whole ball game)

The description is used by Claude's skill-selection classifier. It must:

- **Lead with the capability** ("Write cold outreach emails", not "An AI-powered assistant for...").
- **Enumerate trigger phrases** verbatim. Include 10-30 phrase variants: "Write...", "Draft...", "Make this more...", "My email sounds X", "turn this into Y". Pattern: `Use when the user asks to "X", "Y", "Z", or mentions "A", "B", "C".`
- **Disambiguate vs. sibling skills**. Always include `Not for <neighbor skill>; use <that> for...`.
- **Include negative triggers** for common false-positives.
- **Stay under ~400 tokens** — descriptions load every turn.

## Body structure (progressive disclosure)

```
# Skill Name
One-line purpose.

## When to use / not use
Explicit boundaries.

## Core rules (5-10 max, most load-bearing first)
...

## Workflow
Numbered steps. Each step either asks a question, reads a reference file, or produces output.

## References (load on demand)
- @reference.md — deep guide
- @examples/*.md — few-shot
```

## Anti-patterns

- Stuffing the description with "AI-powered, intelligent, comprehensive". Classifier ignores marketing words and over-triggers.
- Inlining 200-line guides in SKILL.md. Move to `reference.md` and use `@reference.md` imports.
- Writing skills that overlap with existing ones without negative triggers.
- Skills without concrete examples. Always include at least one before/after or worked example.

## Eval harness

Every skill should ship an `evals/` folder with:

- `positive.md` — prompts that MUST fire the skill (10+).
- `negative.md` — prompts that MUST NOT fire (10+, includes near-misses).
- `golden/` — expected outputs for positive prompts.

Run evals with the meta-builder's `scripts/eval.py` (or manually review invocations).

## Scripts sidecar

If the skill performs deterministic work (parsing, validating, rendering), ship a `scripts/` folder and have SKILL.md instruct the model to invoke them via Bash rather than reimplementing in prose.

## References

- @../../agents-architect/references/skill-triggers.md — trigger-phrase patterns and classifier heuristics
- @../../agents-architect/templates/skill.template.md — fill-in-the-blanks scaffold
- @../../agents-architect/references/anthropic-best-practices.md — condensed from Anthropic docs

## Output

When asked to author a skill, produce (or edit):

1. `skills/<name>/SKILL.md` with tight description + structured body.
2. `skills/<name>/reference.md` for anything over 150 lines of body.
3. `skills/<name>/evals/positive.md` and `negative.md`.
4. If deterministic: `skills/<name>/scripts/`.

Finish with a 3-line summary: name, trigger surface, load-on-demand references.
