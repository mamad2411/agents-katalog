# Copilot Instructions: Enterpriseagentimprovementskill
Description: A skill to improve enterprise AI agents by addressing ambiguity, staleness, and preference issues through structured knowledge bases, context lifecycle management, and feedback loops.

## Overview
Enterprise AI agents often face three main problems: ambiguity, staleness, and preference. Ambiguity arises when the agent doesn't know which data source or knowledge base to use. Staleness occurs when the context becomes outdated. Preference issues emerge when different teams or individuals have varying definitions or metrics. This skill provides a structured approach to address these issues.

## Step-by-Step Workflow
1. **Identify Sources of Truth**: Divide knowledge bases into three layers: semantic layer, canonical tables, and database graph. Start from the cleanest source and move to the most dynamic one.
2. **Create a Context Lifecycle**: Embed live data sources and establish a feedback loop to keep the context updated.
3. **Capture Preferences**: Store individual or team preferences in a semantic layer or agent memory.
4. **Evaluate and Update**: Regularly evaluate the agent's performance and update the context based on feedback.

## Code Snippets
```python
# Example of embedding live data sources
live_data_sources = ['GitHub', 'CRM', 'Tableau', 'DBT']
for source in live_data_sources:
    embed_data(source)

# Example of creating a feedback loop
def log_event(event):
    with open('feedback_log.md', 'a') as f:
        f.write(f'{event}\n')

# Example of evaluating agent performance
def evaluate_agent(questions, answers):
    for q, a in zip(questions, answers):
        if q != a:
            log_event(f'Incorrect answer for question: {q}')
```

## Best Practices
- **Hierarchical Knowledge Bases**: Always start from the cleanest source of truth and move to the most dynamic one.
- **Regular Updates**: Ensure that live data sources are regularly updated and reviewed.
- **Feedback Loop**: Capture and log every event that indicates a change in context or preference.

## Common Pitfalls
- **Equal Weighting of Knowledge Bases**: Avoid treating all knowledge bases equally. Use a hierarchical approach.
- **Outdated Context**: Regularly update the context to avoid staleness.
- **Ignoring Preferences**: Capture and store individual or team preferences to avoid ambiguity.

## Validation Steps
1. **Human Annotated Questions**: Curate a set of questions with human-annotated answers to evaluate the agent.
2. **Automated Evaluation**: Compare the agent's answers to actual answers from the last few days.
3. **Feedback Review**: Regularly review the feedback log to identify and address issues.

For more detailed information, refer to the following documents:
- [Core Concepts](references/core_concepts.md)
- [Practical Guide](references/practical_guide.md)
- [Code Examples](references/code_examples.md)
- [Common Pitfalls](references/common_pitfalls.md)

## Reference Guides

### Code Examples

# Code Examples
This document provides code snippets to implement the improvements for enterprise AI agents.

## Embedding Live Data Sources
```python
live_data_sources = ['GitHub', 'CRM', 'Tableau', 'DBT']
for source in live_data_sources:
    embed_data(source)
```

## Creating a Feedback Loop
```python
def log_event(event):
    with open('feedback_log.md', 'a') as f:
        f.write(f'{event}\n')
```

## Evaluating Agent Performance
```python
def evaluate_agent(questions, answers):
    for q, a in zip(questions, answers):
        if q != a:
            log_event(f'Incorrect answer for question: {q}')
```

For more detailed information, refer to the [Core Concepts](references/core_concepts.md) and [Practical Guide](references/practical_guide.md).

### Common Pitfalls

# Common Pitfalls
This document outlines common pitfalls when improving enterprise AI agents and how to avoid them.

## Equal Weighting of Knowledge Bases
Avoid treating all knowledge bases equally. Use a hierarchical approach, starting from the cleanest source of truth and moving to the most dynamic one.

## Outdated Context
Regularly update the context to avoid staleness. Embed live data sources and establish a feedback loop to keep the context updated.

## Ignoring Preferences
Capture and store individual or team preferences to avoid ambiguity. Store preferences in a semantic layer or agent memory.

For more detailed information, refer to the [Core Concepts](references/core_concepts.md) and [Practical Guide](references/practical_guide.md).

### Core Concepts

# Core Concepts
Enterprise AI agents face three main problems: ambiguity, staleness, and preference. Ambiguity arises when the agent doesn't know which data source or knowledge base to use. Staleness occurs when the context becomes outdated. Preference issues emerge when different teams or individuals have varying definitions or metrics.

## Ambiguity
Ambiguity is addressed by dividing knowledge bases into three layers: semantic layer, canonical tables, and database graph. The semantic layer is the cleanest source of truth, containing curated queries, KPI definitions, and business definitions. Canonical tables provide parametric queries, offering flexibility. The database graph connects tables and columns, allowing for complex queries.

## Staleness
Staleness is managed through a context lifecycle, which includes embedding live data sources and establishing a feedback loop. Live data sources are regularly updated and reviewed. The feedback loop captures events that indicate changes in context or preference.

## Preference
Preference issues are addressed by storing individual or team preferences in a semantic layer or agent memory. This allows the agent to route to the right metric based on who is using it.

For more detailed information, refer to the [Practical Guide](references/practical_guide.md) and [Code Examples](references/code_examples.md).

### Practical Guide

# Practical Guide
This guide provides practical steps to improve enterprise AI agents by addressing ambiguity, staleness, and preference issues.

## Step-by-Step Workflow
1. **Identify Sources of Truth**: Divide knowledge bases into three layers: semantic layer, canonical tables, and database graph. Start from the cleanest source and move to the most dynamic one.
2. **Create a Context Lifecycle**: Embed live data sources and establish a feedback loop to keep the context updated.
3. **Capture Preferences**: Store individual or team preferences in a semantic layer or agent memory.
4. **Evaluate and Update**: Regularly evaluate the agent's performance and update the context based on feedback.

## Best Practices
- **Hierarchical Knowledge Bases**: Always start from the cleanest source of truth and move to the most dynamic one.
- **Regular Updates**: Ensure that live data sources are regularly updated and reviewed.
- **Feedback Loop**: Capture and log every event that indicates a change in context or preference.

## Common Pitfalls
- **Equal Weighting of Knowledge Bases**: Avoid treating all knowledge bases equally. Use a hierarchical approach.
- **Outdated Context**: Regularly update the context to avoid staleness.
- **Ignoring Preferences**: Capture and store individual or team preferences to avoid ambiguity.

For more detailed information, refer to the [Core Concepts](references/core_concepts.md) and [Code Examples](references/code_examples.md).

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Enterprise Agents Have a Structure Problem - Ishita Daga, Tesla](https://www.youtube.com/watch?v=B8l81jhvHbI)** by AI Engineer