---
name: CodebrewRouter
description: Project-local guidance for CodebrewRouter Codex skills. Use when documenting, creating, reviewing, or maintaining repository-specific Codex skills under .agents/skills for the Blaze.LlmGateway project.
---

# CodebrewRouter

This repository keeps CodebrewRouter-specific Codex skills project-local under `.agents/skills/`.

## Scope

- Do not install CodebrewRouter skills into `$CODEX_HOME/skills` or another user-global directory unless the user explicitly asks for that.
- Do not treat Copilot agents, OpenCode commands, or generated squad plugins as Codex skill sources of truth.
- Reuse existing repo docs and ADRs instead of copying long references into skill folders.

## Project Skill Pack

The approved project skill design is in `Docs/superpowers/specs/2026-05-22-codebrewrouter-codex-project-skills-design.md`, and the implementation plan is in `Docs/superpowers/plans/2026-05-22-codebrewrouter-codex-project-skills.md`.

The pack contains:

1. `.agents/skills/codebrewrouter-architecture-routing/`
2. `.agents/skills/codebrewrouter-codebase-onboarding/`
3. `.agents/skills/codebrewrouter-mcp-provider-security/`
4. `.agents/skills/codebrewrouter-aspire-local-dev/`
5. `.agents/skills/codebrewrouter-logging-contract/`

## Maintenance

- Keep each skill concise and trigger-focused.
- Include `agents/openai.yaml` for each skill.
- Validate skills with the system skill validator before reporting completion.
- Leave unrelated workspace changes untouched.
