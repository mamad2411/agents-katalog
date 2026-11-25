---
name: aisa-source-skill-editor
description: "Guide for refining neutral mother skills in targetSkills/ without leaking ClawHub breakout or platform-specific release copy into the source layer."
---

# AIsa Source Skill Editor

Refine `targetSkills/` mother skills as neutral, cross-platform source assets.

## When to use

- When editing `targetSkills/*/SKILL.md` or `README.md`
- When the goal is to keep the mother skill portable across ClawHub, Claude, Hermes, AgentSkills.so, and GitHub
- When improving clarity, task framing, or sibling separation without turning the mother skill into a platform-specific publish bundle

## Core rules

- Treat `targetSkills/` as the canonical mother layer, not a ClawHub upload layer.
- Preserve runtime behavior, relative paths, filenames, and shipped commands.
- Keep canonical source frontmatter centered on `metadata.aisa`.
- Do not add `metadata.openclaw`, `metadata.hermes`, marketplace wrapper fields, or release-only install sections to the mother skill.
- Do not introduce ClawHub-only breakout slugs or plugin packaging details into the source layer.
- Sibling differentiation is allowed, but keep it portable and neutral enough to regenerate into multiple platform layers later.
- Prefer task-first descriptions with `Use when:` or `触发条件：`, but avoid overfitting to one marketplace's ranking surface.
- If the skill already exists in `AIsa-team/agent-skills@main`, treat that upstream runtime as the baseline before polishing copy.

## Output expectations

- Mother skills should explain the real runtime clearly.
- Platform-specific structure should be emitted later by build scripts, not hand-written into `targetSkills/`.
- Breakout positioning should stay lightweight unless the runtime itself truly changed.
