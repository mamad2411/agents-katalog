# Codex Agent Configuration with Claude Skills

You are an AI agent with access to a collection of Claude Skills. These skills enhance your capabilities for specialized tasks.

## Skills System

You have skills available to you. Here's how to use them:

1. **Discover Skills**: Run `./list-skills` to enumerate all available skills. This command reads only the metadata (name, description) from each skill's SKILL.md file to keep context efficient. Remember the list of available skills.

2. **Progressive Loading**: When a user request matches a skill's purpose, read the full SKILL.md file for that skill to understand its complete instructions, guidelines, and examples.

3. **Apply Skills**: Use the skill's instructions to complete the task. Only load a skill's full documentation when it's actually relevant to the current task.

## Available Skills

When you start a session or when asked about your capabilities, list the available skills by running:

```bash
./list-skills
```

This will output a JSON array with each skill's name, description, and path. Keep this list in mind throughout our conversation.

## Workflow

- If a user asks you to do something that matches a skill, first check if that skill is available
- If it is, read the full SKILL.md file to understand the complete instructions
- Follow the skill's guidelines to deliver high-quality results
- If no skill matches, proceed with your standard capabilities

## Example

If a user asks: "Create a beautiful landing page for my startup"

1. You recognize this matches the "frontend-design" skill
2. You read the frontend-design SKILL.md to understand its design philosophy
3. You follow its guidelines on aesthetics, typography, and avoiding generic AI patterns
4. You create a distinctive, production-grade interface

## Notes

- Skills are self-contained and can be used independently
- Each skill has clear guidelines on when and how to use it
- The SKILL.md files contain the authoritative instructions for each skill
- This system allows for progressive discovery without context bloat
