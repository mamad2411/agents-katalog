---
# This file is a REFERENCE TEMPLATE for creating new skills, not a real skill.
# It is hidden from auto-discovery via the two flags below. To make a real skill,
# COPY this directory to .claude/skills/<your-skill>/ and remove these two flags.

name: skill-template-reference
description: Reference template for skill frontmatter. Not a real skill — copy this directory to create a new one.
disable-model-invocation: true
user-invocable: false
allowed-tools: Bash, Read, Glob
argument-hint: "<argument>"

# OPTIONAL fields you can add when copying this template:
#
#   model: claude-haiku-4-5            # override session model
#   paths: ["src/**/*.ts"]              # path-scoped auto-invocation
#   when_to_use: "Trigger phrases"      # extra context for Claude beyond description
---

# My skill

A short paragraph describing what this skill is for. Lead with the *why* — the rest of the file is the *how*.

## When to use

- Concrete trigger 1 — describe the situation, not the verb. "When tests fail and the failure isn't obvious."
- Concrete trigger 2.

## When NOT to use

- Anti-trigger 1.
- Anti-trigger 2.

## Steps

1. First step. Make it concrete.
2. Second step. Reference exact files or commands.
3. Third step. Note any decisions the agent should make.

## Common Rationalizations

> Required section. List excuses an agent might use to skip steps, paired with rebuttals.
> The "Common Rationalizations" table is the single most important driver of skill adherence —
> agents will rationalize their way around any process unless you preempt the specific rationalizations.

| Rationalization | Rebuttal |
|---|---|
| "This is a simple change, I'll skip the spec." | If it's truly simple, the spec takes 2 minutes. If it doesn't, it wasn't simple. |
| "The user is in a hurry, I'll skip verification." | Skipping verification *creates* hurry on the next turn when bugs surface. |
| "I already understand the codebase, I don't need to re-read." | The codebase changes between sessions; your memory of it doesn't. Re-read. |

Replace these with rationalizations specific to your skill's domain.

## Output

Describe what a successful invocation produces. If it's a file, give the path. If it's a report, sketch the format.

## Verification checklist

> Required section. End every skill with a binary checklist the agent (or reviewer) can run through.

- [ ] Did I follow every step in the order specified?
- [ ] Did I produce the output described above?
- [ ] If I deviated, did I record *why* in the session log or commit message?
- [ ] [Skill-specific check 1]
- [ ] [Skill-specific check 2]

---

**Authoring notes — read before writing a new skill:**

- **Description precision drives auto-invocation.** Be specific about *when*, not *what*.
  - ❌ `"A skill for writing specs"`
  - ✅ `"Use when starting a new project, feature, or significant change and no specification exists yet. Use when requirements are unclear, ambiguous, or only exist as a vague idea."`
- **Keep the body under ~200 lines.** Long skills get skimmed.
- **Inline cross-references work better than reference tables.** Write `"After this, follow the test-driven-development skill"` rather than pointing readers to a separate index.
- **The Common Rationalizations + Verification Checklist sections are required.** Every skill in this template has them.
- **Supporting files** (templates, scripts) live in this directory — reference as `.claude/skills/<my-skill>/template.md`.
