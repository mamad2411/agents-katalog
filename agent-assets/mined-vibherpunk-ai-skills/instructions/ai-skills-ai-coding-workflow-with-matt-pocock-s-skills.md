# Copilot Instructions: Ai Coding Workflow With Matt Pocock'S Skills
Description: A comprehensive guide to setting up and using Matt Pocock's AI coding skills repository for efficient and effective code development. This skill covers installation, configuration, and the main workflow from idea to implementation.

## Overview
This skill provides a step-by-step guide to using Matt Pocock's AI coding skills repository. The repository is designed to streamline the coding process from idea to implementation, leveraging AI agents to handle various tasks efficiently.

## Core Concepts
Before diving into the workflow, it's essential to understand the core concepts:
- **Skills Repository**: A collection of AI-driven tools and scripts that assist in coding tasks.
- **AI Agents**: Software agents that perform specific tasks based on the skills installed.
- **Context Window**: The amount of information (tokens) that an AI agent can process at once.

For a deeper dive into these concepts, refer to [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow
1. **Installation**: Install the skills repository using Node.js and NPX.
   ```bash
   npx skills@latest add mattpocock/skills
   ```
2. **Configuration**: Configure the skills to work with your preferred AI agent.
   ```bash
   # Follow the CLI prompts to select skills and agent
   ```
3. **Setup**: Run the setup command to configure the repository.
   ```bash
   setup_matt_pocock_skills
   ```
4. **Grill with Docs**: Use the 'grill with docs' skill to refine your idea.
   ```bash
   grill_with_docs "I would like to remove most of the internal tooling on this CLI to make it just only public-facing."
   ```
5. **Specification**: Convert the refined idea into a detailed specification.
   ```bash
   to_spec
   ```
6. **Tickets**: Break down the specification into manageable tickets.
   ```bash
   to_tickets
   ```
7. **Implementation**: Implement the tickets using the AI agent.
   ```bash
   implement
   ```
8. **Code Review**: Perform a code review to ensure quality.
   ```bash
   code_review
   ```

For detailed examples and code snippets, see [Code Examples](references/code_examples.md).

## Best Practices
- **Context Window Management**: Keep the context window within the smart zone (around 140k tokens) to avoid attention degradation.
- **Skill Selection**: Choose skills that are well-documented and supported.
- **Regular Updates**: Stay updated with the latest skills and improvements.

## Common Pitfalls
- **Overloading Context Window**: Exceeding the context window limit can lead to hallucinations and degraded performance.
- **Incomplete Setup**: Ensure all setup steps are completed to avoid runtime errors.

For more on best practices and pitfalls, refer to [Practical Guide](references/practical_guide.md).

## Validation and Testing
- **Specification Check**: Ensure the specification matches the initial idea.
- **Ticket Verification**: Verify that tickets are manageable and within the context window.
- **Code Review**: Perform thorough code reviews to catch any issues.

## Conclusion
This skill provides a robust framework for leveraging AI in your coding workflow. By following the steps and best practices outlined, you can enhance your productivity and code quality.

For further reading, check out the [Core Concepts](references/core_concepts.md), [Practical Guide](references/practical_guide.md), and [Code Examples](references/code_examples.md) documents.

## Reference Guides

### Code Examples

# Code Examples

## Installation
To install Matt Pocock's skills repository, use the following command:
```bash
npx skills@latest add mattpocock/skills
```
This command assumes you have Node.js installed and uses NPX to run the skills.sh command line installer from Vercel.

## Configuration
After installation, configure the skills to work with your preferred AI agent. Follow the CLI prompts to select the skills and agent.

## Setup
Run the setup command to configure the repository:
```bash
setup_matt_pocock_skills
```
This command sets up the repository to use an issue tracker, triage labels, and domain documentation.

## Grill with Docs
Use the 'grill with docs' skill to refine your idea:
```bash
grill_with_docs "I would like to remove most of the internal tooling on this CLI to make it just only public-facing."
```
This skill interviews you to sharpen the idea and records what it learns in context.md and ADRs.

## Specification
Convert the refined idea into a detailed specification:
```bash
to_spec
```
This command compresses the discussion into a document that can be used later.

## Tickets
Break down the specification into manageable tickets:
```bash
to_tickets
```
Each ticket is supposed to be the size of a single context window or a single smart zone.

## Implementation
Implement the tickets using the AI agent:
```bash
implement
```
This command runs the code review as part of the implementation process.

## Code Review
Perform a code review to ensure quality:
```bash
code_review
```
This command compares the work done against the original spec and checks against the standards documentation.

## Best Practices
- **Context Window Management**: Keep the context window within the smart zone (around 140k tokens) to avoid attention degradation.
- **Skill Selection**: Choose skills that are well-documented and supported.
- **Regular Updates**: Stay updated with the latest skills and improvements.

## Common Pitfalls
- **Overloading Context Window**: Exceeding the context window limit can lead to hallucinations and degraded performance.
- **Incomplete Setup**: Ensure all setup steps are completed to avoid runtime errors.

## Validation and Testing
- **Specification Check**: Ensure the specification matches the initial idea.
- **Ticket Verification**: Verify that tickets are manageable and within the context window.
- **Code Review**: Perform thorough code reviews to catch any issues.

### Core Concepts

# Core Concepts

## Skills Repository
A skills repository is a collection of AI-driven tools and scripts designed to assist in various coding tasks. These skills can be invoked by AI agents to perform specific functions, such as code generation, debugging, and documentation.

## AI Agents
AI agents are software entities that perform tasks based on the skills installed in the repository. They can be configured to work with different environments and tools, making them versatile for various coding projects.

## Context Window
The context window refers to the amount of information (measured in tokens) that an AI agent can process at once. Managing the context window is crucial for maintaining the agent's performance and avoiding issues like attention degradation.

## Installation and Setup
Installing and setting up the skills repository involves using Node.js and NPX to add the repository to your project. Configuration steps ensure that the skills are compatible with your preferred AI agent.

## Workflow
The main workflow involves refining an idea using the 'grill with docs' skill, converting it into a detailed specification, breaking down the specification into manageable tickets, and implementing these tickets using the AI agent. Code reviews are performed to ensure quality and adherence to standards.

## Best Practices
- **Context Window Management**: Keep the context window within the smart zone (around 140k tokens) to avoid attention degradation.
- **Skill Selection**: Choose skills that are well-documented and supported.
- **Regular Updates**: Stay updated with the latest skills and improvements.

## Common Pitfalls
- **Overloading Context Window**: Exceeding the context window limit can lead to hallucinations and degraded performance.
- **Incomplete Setup**: Ensure all setup steps are completed to avoid runtime errors.

## Validation and Testing
- **Specification Check**: Ensure the specification matches the initial idea.
- **Ticket Verification**: Verify that tickets are manageable and within the context window.
- **Code Review**: Perform thorough code reviews to catch any issues.

### Practical Guide

# Practical Guide

## Installation
To install Matt Pocock's skills repository, use the following command:
```bash
npx skills@latest add mattpocock/skills
```
This command assumes you have Node.js installed and uses NPX to run the skills.sh command line installer from Vercel.

## Configuration
After installation, configure the skills to work with your preferred AI agent. Follow the CLI prompts to select the skills and agent.

## Setup
Run the setup command to configure the repository:
```bash
setup_matt_pocock_skills
```
This command sets up the repository to use an issue tracker, triage labels, and domain documentation.

## Grill with Docs
Use the 'grill with docs' skill to refine your idea:
```bash
grill_with_docs "I would like to remove most of the internal tooling on this CLI to make it just only public-facing."
```
This skill interviews you to sharpen the idea and records what it learns in context.md and ADRs.

## Specification
Convert the refined idea into a detailed specification:
```bash
to_spec
```
This command compresses the discussion into a document that can be used later.

## Tickets
Break down the specification into manageable tickets:
```bash
to_tickets
```
Each ticket is supposed to be the size of a single context window or a single smart zone.

## Implementation
Implement the tickets using the AI agent:
```bash
implement
```
This command runs the code review as part of the implementation process.

## Code Review
Perform a code review to ensure quality:
```bash
code_review
```
This command compares the work done against the original spec and checks against the standards documentation.

## Best Practices
- **Context Window Management**: Keep the context window within the smart zone (around 140k tokens) to avoid attention degradation.
- **Skill Selection**: Choose skills that are well-documented and supported.
- **Regular Updates**: Stay updated with the latest skills and improvements.

## Common Pitfalls
- **Overloading Context Window**: Exceeding the context window limit can lead to hallucinations and degraded performance.
- **Incomplete Setup**: Ensure all setup steps are completed to avoid runtime errors.

## Validation and Testing
- **Specification Check**: Ensure the specification matches the initial idea.
- **Ticket Verification**: Verify that tickets are manageable and within the context window.
- **Code Review**: Perform thorough code reviews to catch any issues.

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[mattpocock/skills: A complete AI Coding workflow, end-to-end](https://www.youtube.com/watch?v=M6mYodf0dJM)** by Matt Pocock