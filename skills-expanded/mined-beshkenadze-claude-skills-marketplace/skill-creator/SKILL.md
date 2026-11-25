---
name: skill-creator
description: Create new Claude Agent Skills. Use when asked to create, build, or develop a skill.
version: 1.0.0
---

# Skill Creator

## Overview

Guides users through creating well-structured Claude Agent Skills by gathering requirements, generating the skill structure, and producing properly formatted SKILL.md files.

## Instructions

When helping create a new skill, follow this workflow:

### Phase 1: Discovery

Ask the user about their skill requirements:

1. **Purpose**: "What should this skill help Claude do?"
2. **Trigger**: "When should Claude use this skill? What phrases or requests should activate it?"
3. **Scope**: "What are the boundaries? What should this skill NOT do?"
4. **Examples**: "Can you give me an example input and expected output?"

### Phase 2: Design

Based on discovery, determine:

1. **Skill name**: lowercase, hyphens, max 64 chars
2. **Category**: creative, development, enterprise, or document
3. **Description**: clear trigger-focused description (max 1024 chars)
4. **Structure**: simple (SKILL.md only) or advanced (with scripts/templates)

### Phase 3: Generation

Create the skill files:

1. Generate `SKILL.md` with proper frontmatter
2. Add clear instructions section
3. Include concrete examples
4. Add guidelines and constraints
5. Create supporting files if needed

### Phase 4: Review

Present the generated skill and:

1. Explain each section's purpose
2. Suggest improvements
3. Offer to refine based on feedback

## Output Format

### SKILL.md Template

```yaml
---
name: [skill-name]
description: [Clear description explaining what this skill does and when Claude should use it]
version: 1.0.0
---

# [Skill Name]

## Overview
[Brief description of purpose]

## Instructions
[Step-by-step guidance for Claude]

## Examples

### Example: [Use Case Name]

**Input:**
[Example user request]

**Output:**
[Expected response or action]

## Guidelines
[Constraints and best practices]
```

## Examples

### Example: Create a Code Review Skill

**User**: "I want a skill that reviews Python code for best practices"

**Response**:

Let me help you create a Python code review skill. I have a few questions:

1. Should it focus on any specific aspects (security, performance, style)?
2. What coding standards should it follow (PEP 8, type hints)?
3. Should it suggest fixes or just identify issues?

[After gathering requirements, generate the skill]

### Example: Create a Documentation Skill

**User**: "Create a skill for writing API documentation"

**Response**:

I'll help you build an API documentation skill. Let me understand your needs:

1. What format should the docs be in (Markdown, OpenAPI)?
2. Should it include code examples?
3. Any specific sections required (authentication, errors)?

## Guidelines

- Always start with discovery questions
- Generate complete, working skills
- Include realistic examples
- Explain design decisions
- Offer iteration opportunities
- Follow marketplace standards

## Checklist for Generated Skills

Before presenting a skill, verify:

- [ ] Name follows conventions (lowercase, hyphens, ≤64 chars)
- [ ] Description clearly explains trigger conditions
- [ ] Instructions are step-by-step and clear
- [ ] At least one concrete example included
- [ ] Guidelines cover edge cases
- [ ] No hardcoded secrets or credentials
