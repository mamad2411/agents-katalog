---
name: creating-skills
description: Generates high-quality, predictable, and efficient .agent/skills/ directories based on user requirements. Use this skill when the user wants to create a new skill or asks for a skill template.
---

# Antigravity Skill Creator

## When to use this skill
- When the user asks to "create a skill" for a specific task.
- When the user wants to "teach" the agent how to do something permanently.
- When the user asks for a "skill template".

## Workflow
1.  **Analyze**: Understand the goal of the proposed skill.
2.  **Generate Structure**: Create the folder `c:\Users\Davi\.gemini\antigravity\knowledge\skills\<skill-name>\`.
3.  **Generate SKILL.md**: Write the instruction file using the "Claude Way" principles.
4.  **Confirm**: Show the output to the user.

## Instructions

### 1. Folder Hierarchy
Always propose creating this structure:
- `<skill-name>/`
    - `SKILL.md` (Required: Main logic and instructions)
    - `scripts/` (Optional: Helper scripts)
    - `examples/` (Optional: Reference implementations)
    - `resources/` (Optional: Templates or assets)

### 2. YAML Frontmatter Standards
The `SKILL.md` must start with YAML frontmatter:
- **name**: Gerund form (e.g., `testing-code`, `managing-databases`). Max 64 chars. Lowercase, numbers, and hyphens only.
- **description**: Written in **third person**. Must include specific triggers/keywords. Max 1024 chars.

### 3. Writing Principles (The "Claude Way")
- **Conciseness**: Focus only on the unique logic of the skill.
- **Progressive Disclosure**: Keep `SKILL.md` under 500 lines.
- **Forward Slashes**: Always use `/` for paths.
- **Degrees of Freedom**:
    - **Bullet Points** for high-freedom tasks (heuristics).
    - **Code Blocks** for medium-freedom (templates).
    - **Specific Bash Commands** for low-freedom (fragile operations).

## Output Template

When generating the skill for the user, use this format for the file content:

```markdown
---
name: [gerund-name]
description: [3rd-person description]
---

# [Skill Title]

## When to use this skill
- [Trigger 1]
- [Trigger 2]

## Workflow
[Insert checklist or step-by-step guide here]

## Instructions
[Specific logic, code snippets, or rules]

## Resources
- [Link to scripts/ or resources/]
```
