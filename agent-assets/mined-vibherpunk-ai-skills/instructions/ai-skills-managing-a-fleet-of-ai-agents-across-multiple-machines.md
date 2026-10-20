# Copilot Instructions: Managing A Fleet Of Ai Agents Across Multiple Machines
Description: Learn how to effectively manage a fleet of AI agents across multiple machines by implementing a hierarchical structure, maintaining state in files, and using a centralized review gateway.

## Overview
Managing a fleet of AI agents across multiple machines requires a structured approach to ensure scalability, consistency, and efficiency. This skill involves creating a hierarchical organization of agents, maintaining state in files, and using a centralized review gateway to manage tasks and approvals.

## Step-by-Step Workflow
1. **Create a Hierarchical Structure**: Implement a hierarchy of agents (CEO, VP, Manager, Worker) where each agent has a scoped context and approval boundary. Context flows down, and results flow back up.
2. **Maintain State in Files**: Move the state out of the model's context window and into files on disk. Each entity gets its own workspace with shared context, machine-bound state, and a handoff folder.
3. **Implement a Review Gateway**: Build a review gateway where any layer that wants to act submits its plan and waits for approval. Once approved, a hook fires the work off automatically.
4. **Handle Machine Failures**: Ensure that the state is preserved by committing context files to Git and pushing them to other machines. Use tmux send-keys over SSH to pull the context files and resume work.
5. **Centralize Control**: Collapse multiple gateways into one main gateway on an always-on machine. Use Discord as a single router with one bot per machine.

## Code Snippets
```bash
# Example CLI harness for dispatching tasks
function dispatch_task() {
  local task=$1
  local worker=$2
  tmux send-keys -t $worker "$task" C-m
}

# Example Git commit and push for context files
git add .
git commit -m "Update context files"
git push origin main

# Example tmux send-keys over SSH
ssh user@machine 'tmux send-keys -t session_name "git pull" C-m'
```

## Best Practices
- **Hierarchical Structure**: Ensure each agent has a clear role and scope to avoid context overload.
- **State Management**: Keep state in files to preserve work even if the context window is cleared or the machine crashes.
- **Review Gateway**: Use a centralized review gateway to manage approvals and avoid manual checks.

## Common Pitfalls
- **Context Overload**: Avoid holding multiple contexts in your head by delegating responsibilities to agents.
- **Memory Issues**: Monitor memory usage and avoid overloading a single machine with too many tasks.
- **Credential Collisions**: Use fully separated environments for each workspace to prevent credential collisions.

## Validation and Testing
- **Test Hierarchical Structure**: Ensure that tasks are correctly delegated and results flow back up the hierarchy.
- **Validate State Management**: Verify that state is preserved and can be resumed after a context reset or machine crash.
- **Check Review Gateway**: Confirm that the review gateway correctly manages approvals and triggers work automatically.

For more detailed information, refer to the following documents:
- [Core Concepts](references/core_concepts.md)
- [Practical Guide](references/practical_guide.md)
- [Code Examples](references/code_examples.md)

## Reference Guides

### Code Examples

# Code Examples
This document provides code examples for managing a fleet of AI agents across multiple machines.

## CLI Harness for Dispatching Tasks
```bash
function dispatch_task() {
  local task=$1
  local worker=$2
  tmux send-keys -t $worker "$task" C-m
}
```

## Git Commit and Push for Context Files
```bash
git add .
git commit -m "Update context files"
git push origin main
```

## Tmux Send-Keys Over SSH
```bash
ssh user@machine 'tmux send-keys -t session_name "git pull" C-m'
```

## Example Workspace Structure
```
/workspaces
  /shared
  /machineA
  /machineB
  /handoff
```

## Example Review Gateway Hook
```bash
function approve_task() {
  local task=$1
  local worker=$2
  tmux send-keys -t $worker "$task" C-m
}
```

For more detailed information, refer to the Core Concepts and Practical Guide.

### Core Concepts

# Core Concepts
Managing a fleet of AI agents across multiple machines involves several core concepts that ensure scalability, consistency, and efficiency.

## Hierarchical Structure
Implementing a hierarchical structure of agents (CEO, VP, Manager, Worker) helps in delegating tasks and managing context effectively. Each agent has a scoped context and approval boundary, ensuring that context flows down and results flow back up.

## State Management
Moving the state out of the model's context window and into files on disk ensures that the state is preserved even if the context window is cleared or the machine crashes. Each entity gets its own workspace with shared context, machine-bound state, and a handoff folder.

## Review Gateway
A centralized review gateway manages task approvals and triggers work automatically. Any layer that wants to act submits its plan and waits for approval. Once approved, a hook fires the work off automatically.

## Handling Machine Failures
Ensuring that the state is preserved involves committing context files to Git and pushing them to other machines. Using tmux send-keys over SSH pulls the context files and resumes work.

## Centralized Control
Collapsing multiple gateways into one main gateway on an always-on machine and using Discord as a single router with one bot per machine centralizes control and simplifies management.

For more detailed information, refer to the Practical Guide and Code Examples.

### Practical Guide

# Practical Guide
This guide provides practical steps to manage a fleet of AI agents across multiple machines.

## Creating a Hierarchical Structure
1. **Define Roles**: Assign roles (CEO, VP, Manager, Worker) to each agent with clear responsibilities.
2. **Scope Context**: Ensure each agent has a scoped context and approval boundary.
3. **Delegate Tasks**: Delegate tasks down the hierarchy and ensure results flow back up.

## Maintaining State in Files
1. **Create Workspaces**: Each entity gets its own workspace on disk.
2. **Shared Context**: Store shared context that everyone has to honor in a shared directory.
3. **Machine-Bound State**: Store machine-specific state under machine directories.
4. **Handoff Folder**: Maintain a handoff folder for the actual work product that gets passed along.

## Implementing a Review Gateway
1. **Submit Plans**: Any layer that wants to act submits its plan to the review gateway.
2. **Wait for Approval**: The layer blocks and waits for approval.
3. **Trigger Work**: Once approved, a hook fires the work off automatically.

## Handling Machine Failures
1. **Commit Context Files**: Commit context files to Git and push them to other machines.
2. **Pull Context Files**: Use tmux send-keys over SSH to pull the context files and resume work.

## Centralizing Control
1. **Collapse Gateways**: Collapse multiple gateways into one main gateway on an always-on machine.
2. **Use Discord**: Use Discord as a single router with one bot per machine.

For more detailed information, refer to the Core Concepts and Code Examples.

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[I Run a Fleet of AI Agents Across Three Machines. Here's What Broke. - Kyle Jaejun Lee, KRAFTON](https://www.youtube.com/watch?v=4kYl2_mqmnQ)** by AI Engineer