---
name: skill-builder
description: Turn a repeated workflow into a portable skill with precise triggers, useful resources, safe storage, and verified discovery. Use when creating a skill or preparing a shared skill library, not for silently replacing existing installations.
---

# Skill Builder

Build one reusable capability and verify it with realistic input.

## Define and author

- Extract reusable decisions, inputs, outputs, and boundaries. Do not copy private session transcripts, personal operating procedures, or installed third-party bundles.
- Check for overlap and prefer improving an existing skill when the workflow is only a variation.
- Use a lowercase hyphenated folder name and a precise trigger description. Include name and description frontmatter, preserving supported optional metadata when updating.
- Keep instructions concise. Add references for contracts, assets for templates, and scripts when deterministic behavior improves reliability.
- Use relative paths inside the skill. Keep user-specific values in explicitly approved private configuration, not distributed examples.
- Keep agents/openai.yaml consistent with the skill and include its invocation name in the example prompt.

## Storage and discovery

Read [installation safety](references/installation-safety.md) before copying or linking.

Current documentation checked 2026-10-14:

- Codex discovers repository/user skills under `.agents/skills` and supports symlinked skill folders. Inspect compatibility locations already in use before proposing migration. [Codex documentation](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills).
- Claude Code uses project `.claude/skills` and personal `~/.claude/skills` locations. [Claude Code documentation](https://code.claude.com/docs/en/skills).
- A shared source can be linked into applicable discovery locations after verifying ownership and targets. Do not create duplicate registrations merely because multiple paths exist.
- AGENTS.md and CLAUDE.md provide project routing and constraints. They do not replace native discovery or prove a skill loaded.

## Validate and hand off

Run an available structural validator, exercise scripts on disposable fixtures, and forward-test a realistic request. Verify detection in the actual tool after its supported refresh. Distinguish files existing from successful discovery and use.

Report files, behavior checks, discovery status, and conflicts left untouched. Separately review provenance, safety, and the exact release manifest before public sharing. Authoring does not authorize installation elsewhere or publication.
