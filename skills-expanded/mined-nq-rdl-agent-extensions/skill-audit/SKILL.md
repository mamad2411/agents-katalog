---
name: skill-audit
license: CC-BY-4.0
description: >-
  Audit a skill for non-inferable value. Use when creating, compressing, or
  reviewing a SKILL.md to check it encodes a gap the fresh model cannot see
  rather than restating public specs. Applies the Biggs "could a fresh model
  write this verbatim?" test and the SkillsBench conciseness rubric, checks
  version pins and the verify-canonical guard, and flags reference-card skills.
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Skill Audit

Run the non-inferable-value rubric over a target `SKILL.md` (or the session's
skill diff). The rubric below is self-contained. In the agent-extensions
repository, CONTRIBUTING.md → "Skill content conventions" holds the authoring
rules it enforces; elsewhere, do not search for that file.

## Rubric
1. **Non-inferable value (Biggs):** could a fresh model write this verbatim? If yes → cut.
2. **Conciseness (SkillsBench):** verifier-facing, non-inferable detail over comprehensive prose.
3. **Version pins:** any encoded library/tool API surface is pinned in `compatibility:`.
4. **Verify-canonical guard:** fast-moving/high-stakes subjects point to canonical docs.
5. **Frontmatter/discovery:** `name` matches dir; `description` triggers well; structure-standard clean.
6. **Complexity contract:** the skill earns its context cost.

## How to run

Read the target skill or diff and score each rubric item. Return severity-rated
findings (CRITICAL / MODERATE / MINOR) with file:line anchors and a concrete
keep/cut/compress/pin recommendation. End with KEEP / COMPRESS / REMOVE.
This is a read-only audit; do not edit the target files.

## Optional delegation

[references/subagent.rst](references/subagent.rst) contains the subagent outline,
handoff inputs, execution boundaries, and expected result. Read it when delegating
would help or the user asks to “create a subagent to execute this.” Otherwise,
work directly from this skill; the reference does not need to be loaded.
A worker that received this skill in a handoff is the auditor: it applies the
rubric itself and does not delegate again.
