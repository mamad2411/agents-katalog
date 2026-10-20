# Copilot Instructions: Decision Aware Ai Agent Framework
Description: A comprehensive framework for building decision-aware AI agents using context graphs, memory, and reasoning capabilities to enhance decision-making processes.

## Overview

This skill provides a framework for building decision-aware AI agents using context graphs, memory, and reasoning capabilities. The goal is to enhance the decision-making process by providing agents with the necessary tools to understand the 'why' behind actions, not just the 'how'. This framework leverages Neo4j's graph database to capture and manage contextual knowledge, policies, and rules.

### Core Concepts

- **Context Graphs**: Graphs that capture the relationships and connections between different types of data, enabling AI agents to understand the context of their decisions.
- **Memory**: Divided into short-term memory (capturing conversations and state history) and long-term memory (capturing generalized knowledge about organizations, people, etc.).
- **Reasoning**: The process by which an AI agent determines why it should perform a certain task based on predefined policies and rules.

For a deeper dive into these concepts, refer to [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow

1. **Frame the Problem**: Understand the local context and the causality that led to the current situation.
2. **Capture Context**: Use short-term and long-term memory to capture relevant information.
3. **Apply Reasoning**: Use predefined policies and rules to determine the 'why' behind the decision.
4. **Analyze Risks and Values**: Perform a risk-value analysis to evaluate the potential outcomes of the decision.
5. **Generate Alternatives**: Propose multiple alternatives with pros and cons for each.
6. **Make the Decision**: Hand off the decision to an agent with the authority to act or escalate to a higher authority.
7. **Record the Decision**: Save the entire reasoning process and decision into the graph for future reference.

For a detailed guide on implementing this workflow, see [Practical Guide](references/practical_guide.md).

## Code Snippets and Prompt Templates

```python
# Example: Querying a Neo4j graph database for contextual information
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

def query_context_graph(query):
    with driver.session() as session:
        result = session.run(query)
        return result.data()

# Example query
query = "MATCH (n:Person)-[:WORKS_FOR]->(c:Company) RETURN n.name, c.name"
context_data = query_context_graph(query)
print(context_data)
```

For more code examples, refer to [Code Examples](references/code_examples.md).

## Best Practices and Common Pitfalls

### Best Practices

- **Consistency**: Ensure that decisions are consistent with previous actions and global rules.
- **Explicitness**: Make implicit knowledge explicit by clearly defining policies and rules.
- **Traceability**: Record the entire reasoning process for accountability and future reference.

### Common Pitfalls

- **Overgeneralization**: Avoid assuming that what works in most cases will work in all cases. Always consider the specifics of the situation.
- **Ignoring Context**: Failing to capture and utilize the full context can lead to poor decisions.
- **Lack of Oversight**: Ensure there is a mechanism for human or higher-privilege agent oversight when necessary.

For more on best practices and pitfalls, see [Common Pitfalls](references/common_pitfalls.md).

## Validation and Testing Steps

1. **Unit Testing**: Test individual components of the decision-making process, such as querying the graph database and applying reasoning.
2. **Integration Testing**: Ensure that all components work together seamlessly.
3. **Scenario Testing**: Test the framework with real-world scenarios to validate its effectiveness.
4. **Performance Testing**: Evaluate the performance of the framework under different loads and conditions.

## References

For further reading and detailed documentation, refer to the following resources:

- [Core Concepts](references/core_concepts.md)
- [Practical Guide](references/practical_guide.md)
- [Code Examples](references/code_examples.md)
- [Common Pitfalls](references/common_pitfalls.md)

## Reference Guides

### Code Examples

# Code Examples

## Querying a Neo4j Graph Database

```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

def query_context_graph(query):
    with driver.session() as session:
        result = session.run(query)
        return result.data()

# Example query
query = "MATCH (n:Person)-[:WORKS_FOR]->(c:Company) RETURN n.name, c.name"
context_data = query_context_graph(query)
print(context_data)
```

## Applying Reasoning

```python
def apply_reasoning(context_data, policies):
    decisions = []
    for data in context_data:
        decision = policies.evaluate(data)
        decisions.append(decision)
    return decisions

# Example policies
class LoanPolicies:
    def evaluate(self, data):
        if data['credit_score'] > 700:
            return "Approve"
        else:
            return "Reject"

policies = LoanPolicies()
decisions = apply_reasoning(context_data, policies)
print(decisions)
```

## Risk-Value Analysis

```python
def risk_value_analysis(decision, risks, values):
    risk_score = sum(risks)
    value_score = sum(values)
    if value_score > risk_score:
        return "Proceed"
    else:
        return "Reconsider"

# Example risks and values
risks = [5, 3, 2]
values = [8, 7, 6]
analysis_result = risk_value_analysis("Approve", risks, values)
print(analysis_result)
```

## Recording Decisions

```python
def record_decision(decision, reasoning_process):
    with driver.session() as session:
        session.run("CREATE (d:Decision {decision: $decision, reasoning: $reasoning})",
                    decision=decision, reasoning=reasoning_process)

# Example decision and reasoning
decision = "Approve"
reasoning_process = "Applicant has a high credit score and stable income."
record_decision(decision, reasoning_process)
```

### Common Pitfalls

# Common Pitfalls

## Overgeneralization

One common pitfall is assuming that what works in most cases will work in all cases. For example, prescribing a drug that works for 99% of the population without considering the 1% for whom it might be fatal. Always consider the specifics of the situation.

## Ignoring Context

Failing to capture and utilize the full context can lead to poor decisions. For example, an AI agent might approve a loan application without considering the applicant's recent job loss.

## Lack of Oversight

Ensure there is a mechanism for human or higher-privilege agent oversight when necessary. For example, an AI agent might make a decision that conflicts with global business rules if there is no oversight.

## Inconsistent Decisions

Decisions should be consistent with previous actions and global rules. Inconsistency can lead to confusion and mistrust in the AI agent's decision-making process.

## Lack of Traceability

Recording the entire reasoning process is crucial for accountability and future reference. Without traceability, it can be difficult to understand why a particular decision was made.

## Example Scenarios

### Scenario 1: Overgeneralization

An AI agent approves a loan application based on the applicant's credit score without considering their recent job loss. This decision could lead to financial loss for the lender.

### Scenario 2: Ignoring Context

An AI agent prescribes a drug without considering the patient's medical history, leading to adverse effects.

### Scenario 3: Lack of Oversight

An AI agent makes a decision that conflicts with global business rules, resulting in a violation of company policies.

### Scenario 4: Inconsistent Decisions

An AI agent approves a loan application for one applicant but rejects another with similar credentials, leading to confusion and mistrust.

### Scenario 5: Lack of Traceability

An AI agent makes a decision without recording the reasoning process, making it difficult to understand why the decision was made.

### Core Concepts

# Core Concepts

## Context Graphs

Context graphs are a powerful tool for capturing the relationships and connections between different types of data. They enable AI agents to understand the context of their decisions by providing a structured representation of knowledge. In Neo4j, context graphs are built using nodes and relationships, which can represent entities such as people, organizations, and products, as well as the connections between them.

### Short-Term Memory

Short-term memory captures the immediate context of interactions, such as conversations and state history. This type of memory is crucial for understanding the current state of the agent and the user.

### Long-Term Memory

Long-term memory captures generalized knowledge about organizations, people, and other entities. This memory provides a broader context that helps the agent make informed decisions.

### Reasoning

Reasoning is the process by which an AI agent determines why it should perform a certain task based on predefined policies and rules. This involves analyzing the context and applying relevant rules to arrive at a decision.

## Memory Graphs

Memory graphs combine short-term and long-term memory with reasoning capabilities to provide a comprehensive view of the context. This allows the agent to make decisions that are not only based on knowledge but also on the 'why' behind the actions.

## Policies and Rules

Policies and rules are essential for guiding the decision-making process. They provide the framework within which the agent operates, ensuring that decisions are aligned with organizational goals and constraints.

## Decision-Making Framework

The decision-making framework involves several steps, including framing the problem, capturing context, applying reasoning, analyzing risks and values, generating alternatives, making the decision, and recording the decision. This structured approach ensures that decisions are well-informed and consistent.

### Practical Guide

# Practical Guide

## Step-by-Step Workflow

### 1. Frame the Problem

Understand the local context and the causality that led to the current situation. This involves identifying the objective and the environment within which the decision is being made.

### 2. Capture Context

Use short-term and long-term memory to capture relevant information. Short-term memory captures the immediate context, while long-term memory provides a broader overview.

### 3. Apply Reasoning

Use predefined policies and rules to determine the 'why' behind the decision. This involves analyzing the context and applying relevant rules to arrive at a decision.

### 4. Analyze Risks and Values

Perform a risk-value analysis to evaluate the potential outcomes of the decision. Consider factors such as reversibility, cost of being wrong, and the value of the decision.

### 5. Generate Alternatives

Propose multiple alternatives with pros and cons for each. This step involves brainstorming different options and evaluating their potential outcomes.

### 6. Make the Decision

Hand off the decision to an agent with the authority to act or escalate to a higher authority. Ensure that the decision is aligned with global rules and previous actions.

### 7. Record the Decision

Save the entire reasoning process and decision into the graph for future reference. This ensures traceability and accountability.

## Implementation Tips

- **Consistency**: Ensure that decisions are consistent with previous actions and global rules.
- **Explicitness**: Make implicit knowledge explicit by clearly defining policies and rules.
- **Traceability**: Record the entire reasoning process for accountability and future reference.

## Tools and Technologies

- **Neo4j**: A graph database that is ideal for capturing and managing contextual knowledge.
- **LangGraph**: A framework for building decision-aware AI agents.
- **Text to Cypher**: A tool that translates human text into Neo4j's query language, Cypher.

## Example Scenario

Consider a scenario where an AI agent needs to decide whether to approve a loan application. The agent would frame the problem, capture relevant context (e.g., applicant's credit history), apply reasoning (e.g., loan policies), analyze risks and values (e.g., potential default), generate alternatives (e.g., approve, reject, request more information), make the decision, and record the entire process.

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Context Graphs for Explainable, Decision-Aware AI Agents — Andreas Kollegger & Zaid Zaim, Neo4j](https://www.youtube.com/watch?v=abvQEhvRI_c)** by AI Engineer