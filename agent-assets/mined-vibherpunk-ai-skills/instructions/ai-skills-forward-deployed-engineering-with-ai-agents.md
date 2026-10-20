# Copilot Instructions: Forward Deployed Engineering With Ai Agents
Description: A comprehensive skill for deploying AI agents to understand, re-engineer, and optimize enterprise workflows, ensuring seamless integration with existing systems of record.

## Overview
Forward Deployed Engineering (FDE) with AI agents involves embedding AI deeply into enterprise workflows to understand, re-engineer, and optimize processes. This skill focuses on mapping human workflows, re-engineering processes around AI, and deploying agents on top of existing systems of record. For a deeper dive into core concepts, see [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow
1. **Map Human Workflows**: Embed with the client to understand current processes, including edge cases and failure modes.
2. **Re-engineer Processes**: Redesign workflows to maximize AI's capabilities while maintaining usability.
3. **Deploy AI Agents**: Integrate agents with existing systems (e.g., Salesforce, SAP) without requiring migration.
4. **Monitor and Optimize**: Continuously monitor agent performance and refine workflows for maximum ROI.

For detailed steps and best practices, refer to [Practical Guide](references/practical_guide.md).

## Code Snippets and Prompt Templates
```python
# Example: Mapping a workflow using a dependency graph
from graphlib import TopologicalSorter

tasks = {'A': {'B', 'C'}, 'B': {'D'}, 'C': {'D'}, 'D': set()}
ts = TopologicalSorter(tasks)
print(list(ts.static_order()))
```
For more examples, see [Code Examples](references/code_examples.md).

## Best Practices and Common Pitfalls
- **Best Practice**: Always involve process leads in workflow mapping to capture real-world nuances.
- **Pitfall**: Avoid slapping AI onto broken processes; re-engineer workflows first.

For a comprehensive list of pitfalls and how to avoid them, see [Common Pitfalls](references/common_pitfalls.md).

## Validation and Testing
1. **Unit Testing**: Test individual agent functions in isolation.
2. **Integration Testing**: Ensure agents work seamlessly with existing systems.
3. **User Acceptance Testing**: Validate workflows with end-users to ensure usability.

## References
For further reading, explore the following documents:
- [Core Concepts](references/core_concepts.md)
- [Practical Guide](references/practical_guide.md)
- [Code Examples](references/code_examples.md)
- [Common Pitfalls](references/common_pitfalls.md)

## Reference Guides

### Code Examples

# Code Examples
This document provides concrete code snippets and prompt templates for implementing Forward Deployed Engineering (FDE) with AI agents.

## Mapping a Workflow Using a Dependency Graph
```python
from graphlib import TopologicalSorter

tasks = {'A': {'B', 'C'}, 'B': {'D'}, 'C': {'D'}, 'D': set()}
ts = TopologicalSorter(tasks)
print(list(ts.static_order()))
```

## Prompt Template for Extracting Context
```plaintext
Extract the context from the following documentation:
1. Identify key process steps.
2. Highlight edge cases and failure modes.
3. Summarize the workflow in a dependency graph.
```

For more detailed steps and best practices, refer to the [Practical Guide](references/practical_guide.md).

### Common Pitfalls

# Common Pitfalls
This document outlines common pitfalls in implementing Forward Deployed Engineering (FDE) with AI agents and how to avoid them.

## Pitfall 1: Slapping AI onto Broken Processes
Avoid slapping AI onto broken processes; re-engineer workflows first. This ensures that AI is integrated in a way that delivers measurable ROI.

## Pitfall 2: Ignoring Edge Cases
Always involve process leads in workflow mapping to capture real-world nuances. This ensures that edge cases and failure modes are accounted for.

## Pitfall 3: Overlooking System Integration
Ensure that AI agents are integrated with existing systems (e.g., Salesforce, SAP) without requiring migration. This is crucial for enterprises that are married to their systems of record.

For more detailed steps and best practices, refer to the [Practical Guide](references/practical_guide.md).

### Core Concepts

# Core Concepts
Forward Deployed Engineering (FDE) with AI agents is about embedding AI deeply into enterprise workflows to understand, re-engineer, and optimize processes. This involves mapping human workflows, re-engineering processes around AI, and deploying agents on top of existing systems of record.

## Mapping Human Workflows
Mapping human workflows involves embedding with the client to understand current processes, including edge cases and failure modes. This step is crucial for capturing the nuances of how work is done in the real world.

## Re-engineering Processes
Re-engineering processes involves redesigning workflows to maximize AI's capabilities while maintaining usability. This step ensures that AI is not just slapped onto broken processes but is integrated in a way that delivers measurable ROI.

## Deploying AI Agents
Deploying AI agents involves integrating agents with existing systems (e.g., Salesforce, SAP) without requiring migration. This step is crucial for enterprises that are married to their systems of record and cannot afford to migrate.

## Monitoring and Optimization
Monitoring and optimization involve continuously monitoring agent performance and refining workflows for maximum ROI. This step ensures that the AI agents continue to deliver value over time.

For more detailed steps and best practices, refer to the [Practical Guide](references/practical_guide.md).

### Practical Guide

# Practical Guide
This guide provides detailed steps and best practices for implementing Forward Deployed Engineering (FDE) with AI agents.

## Step 1: Map Human Workflows
Embed with the client to understand current processes, including edge cases and failure modes. This involves interviewing process leads and documenting workflows.

## Step 2: Re-engineer Processes
Redesign workflows to maximize AI's capabilities while maintaining usability. This involves identifying steps that can be automated and those that require human intervention.

## Step 3: Deploy AI Agents
Integrate agents with existing systems (e.g., Salesforce, SAP) without requiring migration. This involves using platforms like Veric OS to spin up agents and monitor them.

## Step 4: Monitor and Optimize
Continuously monitor agent performance and refine workflows for maximum ROI. This involves setting up monitoring tools and regularly reviewing performance metrics.

For code examples and prompt templates, refer to the [Code Examples](references/code_examples.md).

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[AI tools for Forward Deployed Engineering — Vasuman Moza, Varick Agents](https://www.youtube.com/watch?v=l0FLhNqBOic)** by AI Engineer