# Copilot Instructions: Claude Routine Automation
Description: Automate recurring tasks and event-triggered workflows using Claude's routines, skills, and connectors. This skill enables you to build reliable, autonomous workflows for tasks like payment recovery, churn management, and personalized proposal generation.

## Overview
Claude routines allow you to automate recurring tasks and event-triggered workflows using skills and connectors. Unlike traditional automation platforms, Claude leverages AI agents to handle complex, non-deterministic tasks. Learn more about the core concepts in [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow
1. **Define the Task**: Identify the task you want to automate (e.g., payment recovery, churn management).
2. **Build a Skill**: Create a skill that outlines the Standard Operating Procedure (SOP) for the task. Use the Process Interviewer Skill to ensure clarity and reliability.
3. **Test the Skill**: Use Claude's Skill Eval feature to test the skill. Run multiple tests to ensure reliability.
4. **Set Up Routine**: Create a new routine in Claude Code. Choose between local (scheduled tasks) and remote (event-triggered) routines.
5. **Configure Connectors**: Select the necessary connectors (e.g., Stripe, Gmail, Circle) for the routine.
6. **Upload Skill to GitHub**: Upload the skill to a GitHub repository to make it accessible to the routine.
7. **Set Trigger**: Define the trigger for the routine (e.g., schedule, API, GitHub).
8. **Validate Routine**: Test the routine to ensure it works as expected.

## Code/Prompt Templates
### Prompt Template for Routine
```
Use the [Skill Name] for this [Task].
```
### Example Prompt for Churn Recovery
```
Use the churn recovery skill for this churned client.
```

## Best Practices
- **Use Skills**: Always use skills in routines to make workflows deterministic and reliable.
- **Test Thoroughly**: Use Skill Eval to test skills before integrating them into routines.
- **Optimize Skills**: Use Auto Research Loop to optimize skills for specific criteria.

## Common Pitfalls
- **Non-Deterministic Workflows**: Avoid relying solely on prompts; use skills to ensure reliability.
- **Overloading Context Window**: Run bulk automations in separate sessions to avoid overloading the context window.

## Validation and Testing
- **Skill Eval**: Run multiple tests using Skill Eval to ensure the skill works reliably.
- **Routine Testing**: Test the routine with real data to ensure it performs as expected.

For more detailed guidance, refer to the [Practical Guide](references/practical_guide.md) and [Code Examples](references/code_examples.md).

## Reference Guides

### Code Examples

# Code Examples
This document provides concrete code snippets and prompt templates for setting up and managing Claude routines.

## Prompt Template for Routine
```
Use the [Skill Name] for this [Task].
```

## Example Prompt for Churn Recovery
```
Use the churn recovery skill for this churned client.
```

## Setting Up API Trigger
To set up an API trigger, use the following cURL command:
```bash
curl -X POST https://api.claude.com/routines/trigger \
-H "Authorization: Bearer YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d '{"event": "customer_subscription_updated"}'
```

## Uploading Skill to GitHub
To upload a skill to GitHub, use the following command:
```bash
git add .
git commit -m "Add churn recovery skill"
git push origin main
```

For more detailed guidance, refer to the [Practical Guide](references/practical_guide.md).

### Core Concepts

# Core Concepts
Claude routines are a powerful feature that allows you to automate recurring tasks and event-triggered workflows using skills and connectors. Unlike traditional automation platforms, Claude leverages AI agents to handle complex, non-deterministic tasks. This document covers the fundamental concepts of Claude routines, including the types of triggers, the role of skills, and the importance of connectors.

## Types of Triggers
Claude supports three types of triggers:
1. **Schedule Triggers**: Run routines at specific time intervals (e.g., daily, weekly).
2. **API Triggers**: Trigger routines based on events from external APIs.
3. **GitHub Triggers**: Trigger routines based on events in GitHub repositories.

## Skills
Skills are predefined workflows that outline the Standard Operating Procedure (SOP) for a task. They make AI agent workflows more deterministic and reliable.

## Connectors
Connectors allow Claude to interact with external services like Stripe, Gmail, and Circle. They are essential for fetching data and performing actions in external systems.

For more detailed examples and practical applications, refer to the [Practical Guide](references/practical_guide.md).

### Practical Guide

# Practical Guide
This guide provides step-by-step instructions for setting up and managing Claude routines. It covers everything from defining tasks to testing and optimizing skills.

## Defining Tasks
Identify the task you want to automate. Common tasks include payment recovery, churn management, and personalized proposal generation.

## Building Skills
Use the Process Interviewer Skill to create a detailed SOP for the task. This ensures that Claude has a clear understanding of the workflow.

## Testing Skills
Use Claude's Skill Eval feature to test the skill. Run multiple tests to ensure reliability.

## Setting Up Routines
Create a new routine in Claude Code. Choose between local (scheduled tasks) and remote (event-triggered) routines.

## Configuring Connectors
Select the necessary connectors (e.g., Stripe, Gmail, Circle) for the routine.

## Uploading Skills to GitHub
Upload the skill to a GitHub repository to make it accessible to the routine.

## Setting Triggers
Define the trigger for the routine (e.g., schedule, API, GitHub).

## Validating Routines
Test the routine to ensure it works as expected.

For code examples and prompt templates, refer to the [Code Examples](references/code_examples.md).

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[How to Use Claude Routines Better than 99% of People](https://www.youtube.com/watch?v=LLE6oMh7SxE)** by Ben AI