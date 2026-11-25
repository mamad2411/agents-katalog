# Migration — AI Tool Transition Guide

## When to Use
- Switching from Cursor, GitHub Copilot, or other AI coding tools to Claude Code
- Migrating prompts and workflows between AI models
- Porting a project's AI configuration to Claude Code's architecture
- Onboarding a team to Claude Code

## Core Principle
Systematically transfer knowledge, prompts, and workflows. Map old tool patterns to Claude Code's 3-layer system (CLAUDE.md + Skills + Memory). Never copy-paste blindly — adapt to Claude's strengths.

## Process
1. **Inventory current setup** — List tools, prompts, custom rules, and codebases. Map each to a Claude Code equivalent.
2. **Translate rules** — Convert .cursorrules, copilot settings, or custom prompts into CLAUDE.md sections. Adapt for Claude's style.
3. **Migrate workflows** — Map repetitive prompt patterns to Skills. Create SKILL.md for each workflow.
4. **Transfer context** — Move project knowledge into MEMORY.md. Decisions, patterns, key files.
5. **Test side-by-side** — Run the same task in both old and new tools. Compare quality and speed.
6. **Document and train** — Create a migration log. Generate team guides for the new setup.

## Output Format
- Migration plan with timeline
- Before/after comparison of key workflows
- Adapted CLAUDE.md and skills
- Success metrics (speed, quality improvements)

## Rules
- Migrate one module at a time — no big bang switches.
- Adapt prompts to Claude's strengths (large context, reasoning) — don't just copy.
- Keep the old tool running during transition as a safety net.
- Involve the team early for buy-in.
- Backup everything before migration.

## Anti-Patterns
- Abrupt full switch without testing (causes workflow disruption)
- Assuming old prompts work identically on Claude (different models, different style)
- Neglecting to document the migration (knowledge loss)
- Skipping the side-by-side comparison (no way to validate improvement)
- Forcing Claude to mimic another tool instead of leveraging its strengths
