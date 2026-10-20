# Copilot Instructions: Ai Agent Workflow Integration
Description: A comprehensive skill for integrating AI agents into development workflows using CLI, custom agents, and guardrails to scale productivity.

## Overview
This skill teaches you how to integrate AI agents into your development workflow using CLI tools, custom agents, and guardrails. The goal is to scale your productivity by delegating repetitive tasks and focusing on higher-level system design. Learn more in [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow
1. **Start with the CLI**: Use the CLI as your entry point for managing tasks like GitHub issues, PRs, and status checks. This reduces the need to open an editor for every task.
2. **Set Up Guardrails**: Create an `Agents.md` file in your repository to define high-level guidance, application architecture, and constraints. This ensures agents adhere to your project's intent.
3. **Create Custom Agents**: Define custom agents with specific roles (e.g., security expert, backend developer) and equip them with tools and skills. Learn more in [Practical Guide](references/practical_guide.md).
4. **Delegate Tasks**: Use the CLI or GitHub UI to delegate tasks like feature development or bug fixes. Agents will create draft PRs for your review.
5. **Fine-Tune in the Editor**: Use the editor for fine adjustments and final reviews, leveraging AI tools for assistance.

## Code Snippets and Prompt Templates
```bash
# Example CLI command to delegate a task
copilot delegate "Create a finance app that tracks my spending. Use HTML, CSS, and JavaScript."
```
```markdown
# Example Agents.md content
## Project Overview
This project is a finance tracker built with React and Tailwind.
## Agent Responsibilities
- Do not change the architecture without explicit approval.
- Follow coding standards defined in the repository.
```

## Best Practices
- **Use Guardrails**: Always define constraints in `Agents.md` to prevent agents from making unauthorized changes.
- **Delegate Wisely**: Delegate repetitive tasks but keep humans in the loop for final approvals.
- **Leverage Skills**: Create reusable skills for common tasks to ensure consistency.

## Common Pitfalls
- **Lack of Guardrails**: Without constraints, agents may produce incorrect or unwanted results.
- **Over-Delegation**: Delegating too much without oversight can lead to chaos. Always review draft PRs.

## Validation and Testing
- **Test Guardrails**: Verify that agents adhere to the constraints defined in `Agents.md`.
- **Review Draft PRs**: Check the quality and correctness of draft PRs created by agents.
- **Monitor Agent Behavior**: Ensure agents are performing tasks as expected and not deviating from their roles.

For more detailed examples, see [Code Examples](references/code_examples.md).

## Reference Guides

### Code Examples

## Code Examples
### CLI Commands
```bash
# Delegate a task to create a finance app
copilot delegate "Create a finance app that tracks my spending. Use HTML, CSS, and JavaScript."
```

### Agents.md
```markdown
## Project Overview
This project is a finance tracker built with React and Tailwind.
## Agent Responsibilities
- Do not change the architecture without explicit approval.
- Follow coding standards defined in the repository.
```

### Custom Agent Definition
```yaml
# Example custom agent definition
role: Security Expert
tools:
  - Read files
  - Search the web
  - Create to-do lists
skills:
  - Security audit
  - Vulnerability scanning
```

### Delegation in GitHub UI
```markdown
# Example GitHub issue
Title: Add dark mode to my app
Description: Implement dark mode using Tailwind CSS.
Assign to agent: Copilot
```

### Core Concepts

## Core Concepts
### CLI as Entry Point
The CLI is now the primary entry point for developers using AI tools. It allows you to manage tasks like GitHub issues, PRs, and status checks without opening an editor. This shift reduces friction and speeds up workflows.

### Guardrails
Guardrails are essential to ensure AI agents adhere to project constraints. The `Agents.md` file serves as a high-level guide, defining the project's intent, architecture, and dos and don'ts. Without guardrails, agents may produce incorrect or unwanted results.

### Custom Agents
Custom agents are AI entities with specific roles and tools. They can orchestrate tasks, reason, and plan, making them more powerful than simple skills. Examples include security experts, backend developers, and frontend developers.

### Delegation
Delegation allows developers to scale their productivity by assigning repetitive tasks to AI agents. Agents create draft PRs, bringing humans into the loop for final approvals.

### Editor for Fine-Tuning
While the CLI handles bulk tasks, the editor remains essential for fine adjustments and final reviews. AI tools assist in the editor, but human oversight ensures quality.

### Practical Guide

## Practical Guide
### Setting Up Guardrails
1. Create an `Agents.md` file in your repository.
2. Define the project overview, agent responsibilities, and constraints.
3. Ensure agents adhere to these guidelines by testing their behavior.

### Creating Custom Agents
1. Define the agent's role (e.g., security expert, backend developer).
2. Equip the agent with tools and skills.
3. Place the agent in the `.github/agents` directory.
4. Test the agent's functionality to ensure it performs as expected.

### Delegating Tasks
1. Use the CLI or GitHub UI to delegate tasks.
2. Specify the task details in the prompt (e.g., "Create a finance app that tracks my spending").
3. Review the draft PR created by the agent.

### Fine-Tuning in the Editor
1. Use the editor for final adjustments and reviews.
2. Leverage AI tools for assistance in the editor.
3. Ensure all changes adhere to the project's constraints.

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[From Writing Code to Designing Systems: How the Developer Role is Changing — Chris Noring, Microsoft](https://www.youtube.com/watch?v=GdvKNwMcfd0)** by AI Engineer