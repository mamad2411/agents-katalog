---
name: personal
description: Manage personal-only skills and private agent preferences that should not be promoted into public or team skill buckets. Use when the user asks to add personal rules, local setup guidance, private workflows, preferences, or machine-specific instructions.
---

# Personal Skill Rules

Use this skill for instructions tied to one user, one machine, one vault, or one private workflow.

## Purpose

`skills/personal/` keeps personal context out of general-purpose skills. This prevents public skills from becoming noisy, brittle, or too specific to one setup.

## What Belongs Here

- Personal writing preferences
- Local machine paths
- Private project conventions
- Personal Obsidian vault rules
- Private API or service usage notes without secrets
- Repeated workflows that only one user needs

## What Does Not Belong Here

- Secrets, tokens, passwords, or private keys
- Generic engineering practices that belong in `engineering/`
- Team-wide rules that deserve a stable shared skill
- Large reference dumps that should live in a separate private document

## Rules

- Never store secrets in a personal skill.
- Keep local paths and user preferences clearly scoped.
- Do not let personal rules override explicit user instructions in a task.
- Promote only a cleaned, non-private version into public buckets.

## Workflow

1. Classify the instruction
   - If it helps only this user, keep it personal.
   - If it helps a team or repo, consider a stable skill bucket.
   - If it is executable behavior, consider `mcp-tools/`.

2. Keep it scoped
   - Write the smallest instruction that changes agent behavior.
   - Avoid turning preferences into universal rules.
   - Include examples only when they prevent ambiguity.

3. Protect private context
   - Do not store secrets.
   - Do not paste sensitive personal data unless explicitly needed.
   - Prefer references to local files over copied private content.

4. Review promotion
   - If a personal skill becomes broadly useful, promote a cleaned version to a public bucket.
   - Remove user-specific paths, names, secrets, and assumptions before promotion.

## Verification

- Confirm the skill does not contain secrets.
- Confirm the instruction is personal rather than broadly reusable.
- Confirm any local paths are intentional.

## Output Format

End with:

- Personal rule added or changed
- Why it belongs in `personal/`
- Any privacy risk
- Whether it could later be promoted
