# Copilot Instructions: Designing Agentic Systems
Description: A comprehensive skill for designing and implementing agentic systems, focusing on systems thinking, workflow design, decomposition, modularity, and algorithmic thinking.

## Overview
Designing agentic systems involves more than just writing prompts or code; it requires a deep understanding of systems thinking, workflow design, decomposition, modularity, and algorithmic thinking. This skill will guide you through the process of designing robust, maintainable, and efficient agentic systems.

## Core Concepts
Before diving into the workflow, it's essential to understand the core concepts that underpin agentic system design. These include systems thinking, workflow design, decomposition, modularity, and algorithmic thinking. For a detailed explanation, refer to [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow
1. **Systems Thinking**: Identify the entire system in which the agent operates. This includes files, tools, humans, and other agents. Define the agent's job, dependencies, and failure modes.
2. **Workflow Design**: Design the workflow that the agent will follow. This includes defining the path from goal to action, considering retries, escalations, and idempotency.
3. **Decomposition**: Break down the agent's tasks into distinct jobs. Separate these jobs into reusable components.
4. **Modularity**: Create reusable modules such as skills and sub-agents. Ensure these modules can be reused across different agents and workflows.
5. **Algorithmic Thinking**: Determine which tasks are best handled by code and which require the agent's judgment. Use code for deterministic tasks and agents for tasks requiring judgment.

## Code Snippets and Prompt Templates
For concrete examples of code snippets and prompt templates, refer to [Code Examples](references/code_examples.md).

## Best Practices and Common Pitfalls
Best practices include designing for idempotency, using structured outputs, and maintaining clear contracts between system components. Common pitfalls include creating monolithic prompts and ignoring the distinction between tasks best handled by code and those requiring agent judgment. For more detailed guidelines, refer to [Practical Guide](references/practical_guide.md).

## Validation and Testing Steps
Validate your agentic system by ensuring it can handle retries, maintain state, and produce consistent outputs. Test the system by simulating various scenarios and checking for idempotency and consistency. For a detailed validation process, refer to [Validation Steps](references/validation_steps.md).

## Reference Guides

### Code Examples

## Code Examples
### Structured Output Example
```python
{
  "decision": "approve",
  "score": 4.5,
  "reason": "The house meets all criteria and has a short commute."
}
```

### Idempotency Check Example
```python
if not action_already_taken:
    take_action()
    log_action()
else:
    complete_missing_parts()
```

### Core Concepts

## Core Concepts
### Systems Thinking
Systems thinking involves understanding the entire system in which the agent operates. This includes identifying all components such as files, tools, humans, and other agents. Define the agent's job, dependencies, and failure modes.

### Workflow Design
Workflow design is crucial for defining the path from goal to action. Consider retries, escalations, and idempotency to ensure the agent can handle various scenarios.

### Decomposition
Decomposition involves breaking down the agent's tasks into distinct jobs. Separate these jobs into reusable components to improve maintainability and efficiency.

### Modularity
Modularity is about creating reusable modules such as skills and sub-agents. Ensure these modules can be reused across different agents and workflows.

### Algorithmic Thinking
Algorithmic thinking involves determining which tasks are best handled by code and which require the agent's judgment. Use code for deterministic tasks and agents for tasks requiring judgment.

### Practical Guide

## Practical Guide
### Best Practices
1. **Design for Idempotency**: Ensure that retries do not cause unintended side effects.
2. **Use Structured Outputs**: Define clear contracts for the agent's output to ensure consistency.
3. **Maintain Clear Contracts**: Ensure that all system components have agreed-upon shapes for communication.

### Common Pitfalls
1. **Monolithic Prompts**: Avoid creating large, monolithic prompts that handle multiple tasks. Decompose them into smaller, manageable components.
2. **Ignoring Task Distinction**: Do not ignore the distinction between tasks best handled by code and those requiring agent judgment. Use code for deterministic tasks and agents for tasks requiring judgment.

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Build Systems, Not Code - Angie Jones, Agentic AI Foundation](https://www.youtube.com/watch?v=ZD9-4fW2HhM)** by AI Engineer

### Validation Steps

## Validation Steps
1. **Simulate Retries**: Test the system by simulating retries to ensure idempotency.
2. **Check State Maintenance**: Verify that the agent maintains state correctly across sessions.
3. **Consistency Checks**: Ensure that the agent produces consistent outputs for the same inputs.
4. **Edge Case Testing**: Test the system with various edge cases to ensure robustness.