---
name: conventions-skills
description: Load when designing, writing, or reviewing an agent skill (SKILL.md file). Use when creating a new skill, editing an existing SKILL.md, or auditing skill quality.
---

# Skill Conventions

Rules for authoring a SKILL.md file that an agent can discover, load, and follow.

## Anatomy of a Skill

- A skill is a directory containing a `SKILL.md` file (exact name, case-sensitive).
- The directory name must match the `name` field in frontmatter.
- Optional subdirectories: `scripts/`, `references/`, `assets/`. Use them to keep the main file lean; the agent loads them on demand.
- Progressive disclosure: the agent loads only `name` + `description` at startup (about 100 tokens per skill), then the full body on activation (under 5000 tokens), then supporting files only when accessed.

## Frontmatter

- Required fields: `name` and `description`.
- `name` constraints: 1-64 chars, lowercase kebab-case, regex `^[a-z0-9]+(-[a-z0-9]+)*$`, must match the parent directory name.
- `description` constraints: 1-1024 chars, non-empty. See the Description section - this is a trigger, not a label.
- Optional spec fields: `license`, `compatibility`, `metadata`. Use only when the skill has a real need.
- House style: spec-level fields only. Do not use vendor-specific extensions (`disable-model-invocation`, `user-invocable`, `context: fork`, etc.) - they are silently ignored by other agents and break portability.

## Description

The description is the highest-leverage line in the file. It is the only metadata the agent sees before deciding to load the skill.

- Describe when to use the skill, not what it contains. If the description encodes the full procedure, the agent may follow it and skip loading the body.
- Third-person. Do not use first- or second-person ("I can help...", "You can use...").
- Two-part structure: what the skill does, then when to use it. Pattern: `[What it does]. Use when [trigger condition 1], [trigger condition 2], or when [keyword].`
- Include keywords and synonyms users actually type.
- Include negative triggers: "Do NOT use for [adjacent case]."
- Keep under 1024 chars. Shorter is fine if it remains specific.

## Scope and Naming

- One coherent domain or workflow per skill. Too narrow forces multiple skills to load for one task; too broad makes activation imprecise.
- Kebab-case names. Match the directory name.
- Prefix conventions group related skills: `conventions-*` for standards, `review-*` for review workflows, `*-authoring` for meta-skills.
- The name is a stable identifier and a human-browsing label. The description carries the triggering burden.

## Body Structure

- Start with `# Title` (H1) in Title Case.
- Orientation: one or two sentences stating what the skill governs.
- Keep the main file under 500 lines / 5000 tokens. Move detailed reference material into `references/` and link to it.
- Use standard Markdown relative links for file references.

## Voice and Formatting

- Load the `conventions-writing` skill before writing the skill.
- Imperative voice in the body ("Run the linter", "Add a null check"). Third-person in the frontmatter description.
- Curate a small set of canonical examples. Do not stuff a laundry list of edge cases - pick diverse examples that portray the expected behavior.
- Do not use bolding.
- Do not use emojis.

## Rules and Constraints

- Match the specificity of an instruction to the fragility of the task. Give the agent freedom when multiple approaches are valid; be prescriptive when operations are fragile or consistency is critical.
- State the rule, then the reason. Reasoning lets the model generalize to cases the rules did not anticipate.
- Reserve `MUST`, `NEVER`, `ALWAYS` for the few consistency-critical rules. Overuse flattens the signal - the agent treats everything as equally important and starts ignoring all of it.

## Anti-Patterns

- Vague descriptions ("helps with data", "processes files") - the skill never triggers.
- Encoding the full workflow or step count in the description - the agent follows the description instead of the body.
- Rule-creep: adding a rule for every mistake without removing stale ones. The file accumulates contradictory patches.
- Decorative prose the model skips: hard-wrapped prose, blockquotes, dividers, three-deep bullet ladders.
- Embedding information the model already knows (e.g., explaining what a PDF is, how HTTP works). Include only what the agent would not know without the skill.
- Embedding information the model doesn't need to know for execution. (e.g., do not include a list of sources that was used to write the skill).
- Dead relative links (`../`, `docs/...`) that break after the skill is installed into a different directory tree.
- Offering many options ("use X or Y or Z") when one default plus an escape hatch is clearer.
- Bare all-caps directives without a stated reason.
- Time-sensitive information inline ("if doing this before August 2025..."). Use a dated "Old patterns" section instead.
