# Contributing to Agent Maxxing

Thanks for considering contributing! Here's how to add skills, improve existing ones, or share workflow examples.

## How to Contribute

### 1. Add a New Skill

1. Fork the repository
2. Choose the appropriate folder:
   - `frontend-design/` — UI, CSS, motion, typography
   - `engineering/` — Code, security, testing, debugging
   - `content/` — Writing, humanization
   - `visual/` — Diagrams, memes, canvas
   - `agent-meta/` — Self-improvement, skill creation
   - `workflows/` — Task management, git, orchestration
   - `adaptation/` — Cross-platform, responsive
   - `components/` — Reusable UI patterns
   - `system-prompts/` — Extracted from top AI agents
3. Create your skill file following the template below
4. Test with Claude Code, Codex, or any compatible agent
5. Submit a Pull Request

### 2. Improve Existing Skills

- Add real-world examples and use cases
- Enhance with modern patterns
- Fix typos, improve clarity
- Add success metrics

### 3. Share Workflow Examples

Used these skills successfully? Add an example to `examples/`:

- Describe the scenario
- List the skills you used
- Show the step-by-step workflow
- Include the outcome

### 4. Report Issues

- Check if the issue already exists
- Provide clear reproduction steps
- Include context about your use case

## Skill File Structure

Every skill should follow this structure:

```markdown
---
name: skill-name
description: One-line description of what this skill does
---

# Skill Name

## When to Use
- Trigger condition 1
- Trigger condition 2
- "Do X when Y" pattern

## Instructions

### Phase 1: [Name]
1. Step one
2. Step two

### Phase 2: [Name]
1. Step one
2. Step two

## Rules
- Rule 1
- Rule 2

## Examples

### Example 1: [Scenario]
[Concrete example of the skill in action]

### Example 2: [Scenario]
[Another concrete example]

## Output Format

```json
{
  "field": "description"
}
```
```

## Style Guide

### Writing
- Write like you're talking to a smart friend
- Be direct, opinionated, specific
- Avoid AI slop words (delve, tapestry, crucial, pivotal)
- Use active voice
- Vary sentence rhythm

### Formatting
- Headers for structure, not decoration
- Bold for key terms on first use
- Code blocks for code, not emphasis
- Lists for parallel items, not prose
- Tables for comparisons

### Code Examples
- Use real, runnable code
- Include error handling
- Match common patterns
- Add comments for non-obvious logic

## Quality Standards

Every skill should be:
- **Actionable** — concrete steps, not vague advice
- **Tested** — verified with real agents
- **Specific** — named tools, specific patterns, measurable outcomes
- **Concise** — respect the reader's time

## Review Process

1. All submissions go through review
2. We check for: clarity, accuracy, actionability
3. We verify: tested with at least one agent
4. We ensure: follows the style guide

## Questions?

Open a GitHub Discussion. We're friendly.
