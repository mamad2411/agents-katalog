---
name: writing-editor-proofreader
description: "Edit writing for grammar, clarity, structure, and tone while preserving the author’s intent. USE WHEN a task matches the Craft workspace workflow for writing-editor-proofreader."
cluster: growth-content
version: 1.0.0
origin: "craft-agent workspace"
globs:
  - "**/*draft*.md"
  - "**/*draft*.txt"
  - "**/*copy*.md"
  - "**/*copy*.txt"
  - "**/*article*.md"
  - "**/*blog*.md"
  - "**/*post*.md"
  - "**/*newsletter*.md"
  - "**/*email*.md"
alwaysAllow:
  - "Read"
---

# Writing Editor & Proofreader

Use this skill when the user wants polished writing with better grammar, clarity, flow, and tone.

## Trigger Conditions
- User asks to proofread or edit text
- User asks to improve clarity or tone
- User asks to rewrite writing for a specific audience

## Required Inputs
1. Original text
2. Intended audience
3. Desired tone/style
4. Constraints (length, format, voice)

## Workflow
1. **Issue detection**: find grammar, syntax, and clarity issues.
2. **Structural edit**: improve organization and flow.
3. **Tone alignment**: adapt wording for target audience.
4. **Concision pass**: remove fluff and redundancy.
5. **Delivery**: provide edited version plus key change notes.

## Output Format
- Clean edited draft
- Optional tracked-style change summary
- 3-5 writing improvement tips tailored to the user

## Guardrails
- Preserve original meaning unless user requests reframing.
- Avoid unnecessary stylistic overreach.
- Flag ambiguous source text instead of guessing intent.
