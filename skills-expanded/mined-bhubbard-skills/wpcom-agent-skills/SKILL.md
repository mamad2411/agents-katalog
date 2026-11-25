---
name: wpcom-agent-skills
description: Use this skill for building and managing WordPress AI Agent Skills and SKILL.md files.
---

# WordPress Agent Skills

This skill provides advanced developer guidance on utilizing, creating, and managing Agent Skills for AI coding agents within the WordPress ecosystem.

## What are Agent Skills?

Agent Skills are curated, reusable packages containing prompts, instructions, and tooling definitions. They are designed to help AI coding agents (like Claude Code or Gemini) perform WordPress-related development tasks more effectively, consistently, and securely.

A skill standardizes instructions for common workflows, such as:
- Block development (`block.json`, attributes, rendering)
- Plugin development (Hooks, Settings API, security)
- Block Themes (`theme.json`, templates, patterns)
- REST API and WP-CLI integrations

## The SKILL.md File

An Agent Skill is fundamentally defined by a `SKILL.md` file. 
- **Structure:** It includes YAML frontmatter (containing the `name` and `description` used for triggering the skill) and a markdown body with detailed instructions.
- **Function:** When an agent is prompted with a relevant task, it reads this file to understand the specific rules, best practices, and context needed to complete the task successfully.

## Installation and Management

Skills can be installed in two primary ways:
1. **Project-local:** Placed within the specific project directory, ensuring the whole development team uses the same AI instructions for that codebase.
2. **Global:** Placed in the developer's global coding agent configuration directory, applying the skill across all their local projects.

### WordPress Studio Integration

WordPress Studio seamlessly integrates these skills to assist with local development:
- **Built-in Skills:** Studio comes with pre-configured skills for plugin, block, and theme development.
- **Automatic Configuration:** When a skill is enabled in Studio, it is copied to the site directory. Studio automatically creates necessary symlinks (e.g., `.claude/skills/<skill-id>`) so the agent can immediately recognize and utilize the skill without manual setup.
- **Management:** Users can install or remove skills on a global or per-site basis directly via the Studio settings menu.

## Reference
Always refer to the official [WordPress.com Developer Docs](https://developer.wordpress.com/docs/) for the most up-to-date instructions on creating and publishing custom Agent Skills.
