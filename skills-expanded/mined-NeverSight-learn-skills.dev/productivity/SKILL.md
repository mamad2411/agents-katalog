---
name: productivity
description: Helps with workflows, automation, git, and multi-agent collaboration. Use when optimizing development processes or coordinating between different agents (Claude, OpenAI, etc.).
---

# Productivity Skill

This skill optimizes the development workflow and ensures seamless collaboration between agents and humans.

## When to use this skill

- Use this when creating or updating `.agents/workflows/`.
- This is helpful for automating repetitive tasks (e.g., scraping, data prep).
- Use when coordinating work between Antigravity, Claude, and OpenAI.
- Use to manage the `task.md` and project progress tracking.

## How to use it

### Workflow Management
- Prefer structured `.md` workflows for complex tasks.
- Keep `task.md` updated with every task boundary.
- Use artifacts to communicate plans (implementation plans) and results (walkthroughs).

### Multi-Agent Interaction
- Ensure all project rules are mirrored across agent-specific configs (Ref: `project-context`).
- Use standardized commit messages and PR descriptions.
- Share context via the shared `.agents` and `.claude` directories.
