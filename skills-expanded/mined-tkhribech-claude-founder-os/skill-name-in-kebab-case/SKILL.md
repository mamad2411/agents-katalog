---
name: skill-name-in-kebab-case
description: One or two sentences optimized for TRIGGERING — say when to use this skill, in the words a user would actually say, including the trigger phrases ("run the X", "check Y", "how are Z doing"). The harness matches requests against this line; a vague description means the skill never fires.
---

<!-- Anatomy of a good SKILL.md. Delete these comments in your real skill.
     Principles:
     - The description is for ROUTING; the body is for EXECUTION. Different audiences.
     - Write the body for an assistant with zero session context: name exact file paths,
       exact commands, exact output format.
     - Encode decisions, not vibes: "if A then B" beats "use judgment".
     - State what the skill must NOT do as explicitly as what it does.
     - If the skill produces an artifact, specify where it's written and what "done" looks like. -->

# Skill Name

One paragraph: what this skill does and what exists when it finishes.

## When to use / when NOT to use

- Use when: …
- Do NOT use for: … (route those to <other skill / plain work> instead)

## Inputs

What the skill needs before it can run: files to read, credentials location (a git-ignored folder, read at runtime — never echoed), founder decisions that must already exist.

## Steps

1. …exact, ordered, with the real commands/paths…
2. …
3. Verify: state HOW the result is checked, at the layer of the claim.

## Output

The exact artifact + where it's written + the report format (lead with the answer; separate verified from assumed).

## Guardrails

- The standing rules this skill must respect (link the memory files).
- The irreversible actions inside it that always require founder confirmation.
