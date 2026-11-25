---
name: github-skill-research
description: Research real AI-agent skill repositories, official docs, prompt libraries, SKILL.md patterns, AGENTS.md or CLAUDE.md conventions, and reusable workflow prompts. Use when creating, improving, auditing, comparing, templating, or monitoring AI agent skills and workflow repositories.
---

# GitHub Skill Research

Research reusable AI-agent skill patterns from real repositories and primary documentation.

## Workflow

1. Define the research target
   - Identify whether the user wants structure, trigger logic, workflow design, operating rules, examples, portability, or repository organization.
   - If the target is unclear, make a narrow useful assumption and state it.

2. Search sources
   - Prioritize real repositories with `SKILL.md`, `AGENTS.md`, `CLAUDE.md`, prompt libraries, workflow playbooks, or MCP/tooling examples.
   - Prefer official documentation and maintained repositories over generic blog advice.
   - Include `thananon/9arm-skills` as a useful comparison point when evaluating concise skill structure.
   - See [research-methodology](../research-methodology/SKILL.md) for tiering sources (repo itself vs. a blog post about the repo) and tracking which candidates were actually checked vs. skipped.

3. Analyze examples
   - Extract frontmatter style, trigger descriptions, workflow steps, output formats, safety rules, bundled resources, and repo layout.
   - Identify whether each pattern is portable across agents or tied to one tool.

4. Compare against the user's repo
   - Mark patterns to copy, adapt, skip, or keep private.
   - Call out duplication, overbroad skills, stale instructions, and missing validation.

5. Produce recommendations
   - Respond in the user's language.
   - Include links or local file paths.
   - Keep templates short enough to install or edit immediately.

## Output Format

```markdown
# AI Agent Skill Research

## Summary

## Useful Sources

## Patterns To Copy

## Patterns To Adapt

## Anti-patterns To Avoid

## Suggested Skill Template

## Action Items
```

## Rules

- Do not summarize sources without links or file paths.
- Do not copy a skill verbatim unless the user asks.
- Keep trigger logic in YAML `description`.
- Prefer workflows with verification over advice-only prompts.
