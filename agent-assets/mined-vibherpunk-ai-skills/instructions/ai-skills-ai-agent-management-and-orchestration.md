# Copilot Instructions: Ai Agent Management And Orchestration
Description: A comprehensive skill for managing and orchestrating AI agents using Claude, focusing on context infrastructure, agent creation, and team synchronization.

## Overview

This skill provides a detailed SOP for managing and orchestrating AI agents using Claude. It covers the creation of agents, setting up context infrastructure, and synchronizing agents across a team. The core concepts include understanding the importance of context, creating persistent memory, and leveraging system thinking to optimize AI workflows.

For a deeper dive into the core concepts, refer to [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow

1. **Define Agent Roles and Responsibilities**: Start by defining the roles and responsibilities of each agent. Use a structured approach to ensure clarity.

2. **Create Initial Context Files**: Develop context files that include SOPs, business knowledge management (BKM), and other relevant documents.

3. **Set Up Persistent Memory**: Use `claude.md` files to maintain persistent memory across sessions.

4. **Build Skills**: Create skills for repetitive tasks using the skill creator tool in Claude.

5. **Organize Projects**: Organize your work into projects within Claude Co-work or Claude Code.

6. **Sync Across Team**: Use tools like Obsidian Sync or GitHub to synchronize context files across your team.

For practical implementation steps, refer to [Practical Guide](references/practical_guide.md).

## Code Snippets and Prompt Templates

```markdown
# Example Prompt for Creating a Skill
Help me build an infographic skill. The skill should follow these steps:
1. Gather data from the provided context files.
2. Create a visually appealing infographic.
3. Save the infographic in the designated folder.
```

For more code examples, refer to [Code Examples](references/code_examples.md).

## Best Practices and Common Pitfalls

**Best Practices**:
- Always define clear roles and responsibilities for each agent.
- Regularly update context files to ensure accuracy.
- Use persistent memory (`claude.md`) to maintain context across sessions.

**Common Pitfalls**:
- Overloading agents with too many tasks can lead to inefficiency.
- Neglecting to update context files can result in outdated information.

For detailed examples and pitfalls, refer to [Common Pitfalls](references/common_pitfalls.md).

## Validation and Testing Steps

1. **Test Skills**: Use built-in evals in Claude to test skills and ensure they produce consistent outputs.
2. **Review Context Files**: Regularly review context files for accuracy and completeness.
3. **Monitor Agent Performance**: Track the performance of agents to identify areas for improvement.

## Reconciliation of Sources

Both transcripts emphasize the importance of context and system thinking in managing AI agents. The first transcript focuses on the practical application of creating and managing a team of agents, while the second provides a detailed breakdown of context levels and synchronization techniques. This skill synthesizes both approaches into a comprehensive SOP.

## References

```json
[
  {
    "filename": "core_concepts.md",
    "content": "## Core Concepts\n\nUnderstanding the core concepts of AI agent management is crucial for effective orchestration. This document covers the importance of context, persistent memory, and system thinking in optimizing AI workflows.\n\n### Importance of Context\n\nContext is the foundation of effective AI agent management. Without proper context, agents cannot perform tasks efficiently. Context includes SOPs, business knowledge management (BKM), and other relevant documents.\n\n### Persistent Memory\n\nPersistent memory, maintained through `claude.md` files, ensures that agents retain information across sessions. This is essential for continuous improvement and efficiency.\n\n### System Thinking\n\nSystem thinking involves understanding the interconnectedness of various components in a system. Applying system thinking to AI agent management helps in creating optimized workflows and achieving better results.\n\nFor practical implementation steps, refer to [Practical Guide](references/practical_guide.md)."
  },
  {
    "filename": "practical_guide.md",
    "content": "## Practical Guide\n\nThis guide provides step-by-step instructions for implementing AI agent management using Claude. It covers agent creation, context setup, and team synchronization.\n\n### Step 1: Define Agent Roles and Responsibilities\n\nStart by defining the roles and responsibilities of each agent. Use a structured approach to ensure clarity.\n\n### Step 2: Create Initial Context Files\n\nDevelop context files that include SOPs, business knowledge management (BKM), and other relevant documents.\n\n### Step 3: Set Up Persistent Memory\n\nUse `claude.md` files to maintain persistent memory across sessions.\n\n### Step 4: Build Skills\n\nCreate skills for repetitive tasks using the skill creator tool in Claude.\n\n### Step 5: Organize Projects\n\nOrganize your work into projects within Claude Co-work or Claude Code.\n\n### Step 6: Sync Across Team\n\nUse tools like Obsidian Sync or GitHub to synchronize context files across your team.\n\nFor code examples, refer to [Code Examples](references/code_examples.md)."
  },
  {
    "filename": "code_examples.md",
    "content": "## Code Examples\n\nThis document provides concrete code snippets and prompt templates for managing AI agents using Claude.\n\n### Example Prompt for Creating a Skill\n\n```markdown\n# Example Prompt for Creating a Skill\nHelp me build an infographic skill. The skill should follow these steps:\n1. Gather data from the provided context files.\n2. Create a visually appealing infographic.\n3. Save the infographic in the designated folder.\n```\n\n### Example Prompt for Testing a Skill\n\n```markdown\n# Example Prompt for Testing a Skill\nPlease test this skill. The criteria for the test are:\n1. Is this skill functional?\n2. Is the word count similar to my newsletter examples?\n3. Is the sentence structure similar?\n4. Is my tone of voice similar?\n```\n\nFor best practices and common pitfalls, refer to [Common Pitfalls](references/common_pitfalls.md)."
  },
  {
    "filename": "common_pitfalls.md",
    "content": "## Common Pitfalls\n\nThis document outlines common pitfalls in AI agent management and provides best practices to avoid them.\n\n### Overloading Agents\n\nOverloading agents with too many tasks can lead to inefficiency. Ensure each agent has a clear and manageable set of responsibilities.\n\n### Neglecting Context Updates\n\nNeglecting to update context files can result in outdated information. Regularly review and update context files to maintain accuracy.\n\n### Lack of Persistent Memory\n\nFailing to use persistent memory (`claude.md`) can lead to loss of context across sessions. Always maintain persistent memory to ensure continuous improvement.\n\nFor core concepts, refer to [Core Concepts](references/core_concepts.md)."
  }
]


## Reference Guides

### Code Examples

## Code Examples

This document provides concrete code snippets and prompt templates for managing AI agents using Claude.

### Example Prompt for Creating a Skill

```markdown
# Example Prompt for Creating a Skill
Help me build an infographic skill. The skill should follow these steps:
1. Gather data from the provided context files.
2. Create a visually appealing infographic.
3. Save the infographic in the designated folder.
```

### Example Prompt for Testing a Skill

```markdown
# Example Prompt for Testing a Skill
Please test this skill. The criteria for the test are:
1. Is this skill functional?
2. Is the word count similar to my newsletter examples?
3. Is the sentence structure similar?
4. Is my tone of voice similar?
```

For best practices and common pitfalls, refer to [Common Pitfalls](references/common_pitfalls.md).

### Common Pitfalls

## Common Pitfalls

This document outlines common pitfalls in AI agent management and provides best practices to avoid them.

### Overloading Agents

Overloading agents with too many tasks can lead to inefficiency. Ensure each agent has a clear and manageable set of responsibilities.

### Neglecting Context Updates

Neglecting to update context files can result in outdated information. Regularly review and update context files to maintain accuracy.

### Lack of Persistent Memory

Failing to use persistent memory (`claude.md`) can lead to loss of context across sessions. Always maintain persistent memory to ensure continuous improvement.

For core concepts, refer to [Core Concepts](references/core_concepts.md).

### Core Concepts

## Core Concepts

Understanding the core concepts of AI agent management is crucial for effective orchestration. This document covers the importance of context, persistent memory, and system thinking in optimizing AI workflows.

### Importance of Context

Context is the foundation of effective AI agent management. Without proper context, agents cannot perform tasks efficiently. Context includes SOPs, business knowledge management (BKM), and other relevant documents.

### Persistent Memory

Persistent memory, maintained through `claude.md` files, ensures that agents retain information across sessions. This is essential for continuous improvement and efficiency.

### System Thinking

System thinking involves understanding the interconnectedness of various components in a system. Applying system thinking to AI agent management helps in creating optimized workflows and achieving better results.

For practical implementation steps, refer to [Practical Guide](references/practical_guide.md).

### Practical Guide

## Practical Guide

This guide provides step-by-step instructions for implementing AI agent management using Claude. It covers agent creation, context setup, and team synchronization.

### Step 1: Define Agent Roles and Responsibilities

Start by defining the roles and responsibilities of each agent. Use a structured approach to ensure clarity.

### Step 2: Create Initial Context Files

Develop context files that include SOPs, business knowledge management (BKM), and other relevant documents.

### Step 3: Set Up Persistent Memory

Use `claude.md` files to maintain persistent memory across sessions.

### Step 4: Build Skills

Create skills for repetitive tasks using the skill creator tool in Claude.

### Step 5: Organize Projects

Organize your work into projects within Claude Co-work or Claude Code.

### Step 6: Sync Across Team

Use tools like Obsidian Sync or GitHub to synchronize context files across your team.

For code examples, refer to [Code Examples](references/code_examples.md).

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[We Replaced Our Entire Team with 30+ Claude AI Agents (Here's How)](https://www.youtube.com/watch?v=aoc_NQfxjy8)** by The AI Productivity Podcast
2. **[The 7 Levels of Using Claude Context Explained in 24 min](https://www.youtube.com/watch?v=l5Diqeoffa4)** by Ben AI