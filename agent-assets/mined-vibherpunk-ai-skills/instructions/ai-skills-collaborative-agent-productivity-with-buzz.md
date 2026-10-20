# Copilot Instructions: Collaborative Agent Productivity With Buzz
Description: A skill enabling AI agents to enhance team collaboration and productivity using Buzz, an agentic Slack alternative built on open protocols.

## Overview
Buzz, developed by Jack Dorsey, is a revolutionary tool designed to enhance team collaboration by integrating AI agents as first-class team members. Unlike traditional tools like Slack, Buzz allows seamless interaction with agents, enabling real-time brainstorming, project management, and software development. This skill will guide you through leveraging Buzz to maximize productivity and streamline workflows.

## Core Concepts
Buzz operates on open protocols, primarily Nostr, which ensures flexibility and integration capabilities. Key features include agent huddles, shared compute, and tight Git integration, making it a versatile tool for both technical and non-technical teams.

## Step-by-Step Workflow
1. **Setup Buzz Environment**: Install Buzz and configure your relay server.
2. **Integrate Agents**: Add agents to your team and assign specific roles or tasks.
3. **Utilize Agent Huddles**: Engage in real-time audio chats with agents for brainstorming and problem-solving.
4. **Leverage Shared Compute**: Share local LLMs with team members to optimize resource usage.
5. **Manage Projects**: Use Buzz’s project view to oversee and manage ongoing projects.
6. **Automate Workflows**: Set up recurring tasks and automate workflows using agents.

## Code Snippets
```python
# Example: Adding an agent to Buzz
agent = BuzzAgent(name='Fizz', role='Code Reviewer')
agent.add_to_team(team_id='your_team_id')
```

## Best Practices
- **Clear Instructions**: Provide concise and clear instructions to agents to avoid misinterpretation.
- **Regular Updates**: Continuously update agent roles and tasks based on project needs.
- **Resource Management**: Efficiently manage shared compute resources to avoid bottlenecks.

## Common Pitfalls
- **Overloading Agents**: Avoid assigning too many tasks to a single agent, which can lead to inefficiency.
- **Ignoring Context**: Ensure agents have access to relevant context to perform tasks effectively.

## Validation and Testing
- **Task Completion**: Verify that agents complete assigned tasks accurately.
- **Performance Metrics**: Monitor agent performance using Buzz’s analytics tools.

For more detailed information, refer to the [Core Concepts](references/core_concepts.md) and [Practical Guide](references/practical_guide.md).

## Reference Guides

### Code Examples

# Code Examples for Buzz
This document provides practical code snippets for integrating and managing agents in Buzz.

## Adding an Agent
```python
# Example: Adding an agent to Buzz
agent = BuzzAgent(name='Fizz', role='Code Reviewer')
agent.add_to_team(team_id='your_team_id')
```

## Assigning Tasks
```python
# Example: Assigning a task to an agent
task = Task(description='Review the latest code commit', agent='Fizz')
task.assign()
```

## Initiating an Agent Huddle
```python
# Example: Initiating an agent huddle
huddle = AgentHuddle(agents=['Fizz', 'Honey'])
huddle.start()
```

## Sharing LLMs
```python
# Example: Sharing a local LLM
llm = LocalLLM(model='Codex')
llm.share_with_team(team_id='your_team_id')
```

For best practices and common pitfalls, refer to the [Practical Guide](references/practical_guide.md).

### Core Concepts

# Core Concepts of Buzz
Buzz is built on the Nostr protocol, ensuring openness and flexibility. It integrates AI agents as first-class team members, allowing for seamless collaboration. Key features include agent huddles, shared compute, and Git integration. These features enable real-time brainstorming, resource optimization, and project management. Understanding these core concepts is essential for leveraging Buzz effectively.

## Agent Huddles
Agent huddles allow real-time audio chats with agents, facilitating brainstorming and problem-solving. This feature is particularly useful for creative tasks that require live interaction.

## Shared Compute
Shared compute enables team members to share local LLMs, optimizing resource usage. This is especially beneficial for small teams with limited resources.

## Git Integration
Buzz’s tight Git integration allows agents to manage code repositories, create feature branches, and work in parallel work trees. This feature streamlines software development workflows.

For a practical guide on using these features, refer to the [Practical Guide](references/practical_guide.md).

### Practical Guide

# Practical Guide to Using Buzz
This guide provides step-by-step instructions for setting up and using Buzz to enhance team collaboration and productivity.

## Setting Up Buzz
1. **Install Buzz**: Download and install Buzz from the official website.
2. **Configure Relay Server**: Set up a relay server to host your team’s data and communications.

## Integrating Agents
1. **Add Agents**: Add agents to your team and assign specific roles or tasks.
2. **Assign Roles**: Define clear roles for each agent to ensure efficient task management.

## Utilizing Agent Huddles
1. **Initiate Huddle**: Start an audio chat with an agent for real-time brainstorming.
2. **Engage Agents**: Use agents to generate ideas and solve problems collaboratively.

## Leveraging Shared Compute
1. **Share LLMs**: Share local LLMs with team members to optimize resource usage.
2. **Monitor Resources**: Regularly monitor resource usage to avoid bottlenecks.

## Managing Projects
1. **Use Project View**: Utilize Buzz’s project view to oversee and manage ongoing projects.
2. **Automate Workflows**: Set up recurring tasks and automate workflows using agents.

For code examples and best practices, refer to the [Code Examples](references/code_examples.md).

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Jack Dorsey's Buzz: The New Hermes Agent?](https://www.youtube.com/watch?v=_jGSgzBkzrY)** by Greg Isenberg