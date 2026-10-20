# Copilot Instructions: Agent Driven Data Platform Migration And Optimization
Description: This skill enables AI agents to migrate and optimize data platforms, focusing on transitioning from human-centric to agent-centric systems. It includes steps for context engineering, query optimization, and handling autonomous agent workloads.

## Overview
This skill focuses on migrating and optimizing data platforms to support autonomous AI agents. The core concepts include context engineering, query optimization, and handling autonomous agent workloads. For a detailed understanding, refer to [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow
1. **Assess Current Data Platform**: Evaluate the existing data platform to identify human-centric assumptions and limitations.
2. **Design Context Serving Layer**: Create a context serving layer that provides fresh, joinable, and cheap-to-query runtime data for AI systems. Refer to [Practical Guide](references/practical_guide.md) for detailed steps.
3. **Migrate Codebase**: Transition the codebase from Python to Rust, ensuring compatibility with agent-driven workloads.
4. **Optimize Queries**: Implement query optimization techniques to handle autonomous agent workloads efficiently.
5. **Validate and Test**: Ensure the migrated and optimized platform meets performance and reliability standards.

## Code Snippets
```python
# Example: Migrating Python code to Rust
fn main() {
    println!("Hello, world!");
}
```
For more examples, see [Code Examples](references/code_examples.md).

## Best Practices and Pitfalls
- **Best Practice**: Ensure the context serving layer is scalable and can handle high concurrency.
- **Common Pitfall**: Avoid treating AI agents as faster humans; they require fundamentally different access patterns.

## Validation and Testing
1. **Performance Testing**: Measure query response times and ensure they meet agent-driven workload requirements.
2. **Reliability Testing**: Verify the system's ability to handle continuous, autonomous queries without failure.

For more detailed validation steps, refer to [Practical Guide](references/practical_guide.md).

## Reference Guides

### Code Examples

# Code Examples

## Migrating Python Code to Rust
```rust
fn main() {
    println!("Hello, world!");
}
```

## Query Optimization
```sql
-- Example: Optimizing a narrow query
SELECT region, SUM(sales) FROM sales_data WHERE region = 'North' GROUP BY region;

-- Example: Optimizing a wide query
SELECT region, SUM(sales) FROM sales_data GROUP BY region;

-- Example: Optimizing a join-heavy query
SELECT a.region, SUM(b.sales) FROM sales_data a JOIN sales_data b ON a.region = b.region GROUP BY a.region;
```

## Handling Autonomous Agent Workloads
```python
# Example: Handling continuous queries
while True:
    query = generate_query()
    result = execute_query(query)
    process_result(result)
```

For more detailed steps and examples, refer to the [Core Concepts](references/core_concepts.md) and [Practical Guide](references/practical_guide.md).

### Core Concepts

# Core Concepts

## Context Engineering
Context engineering involves creating a context serving layer that provides fresh, joinable, and cheap-to-query runtime data for AI systems. This layer is crucial for agents to make informed decisions autonomously.

## Query Optimization
Query optimization in agent-driven systems focuses on handling autonomous agent workloads efficiently. This includes optimizing for narrow queries, wide queries, and join-heavy queries.

## Autonomous Agent Workloads
Autonomous agents generate queries dynamically and continuously, requiring data platforms to handle unpredictable access patterns and high concurrency.

## Migration from Python to Rust
Migrating the codebase from Python to Rust ensures compatibility with agent-driven workloads, leveraging Rust's performance and safety features.

For more detailed steps and examples, refer to the [Practical Guide](references/practical_guide.md) and [Code Examples](references/code_examples.md).

### Practical Guide

# Practical Guide

## Assessing Current Data Platform
1. **Identify Human-Centric Assumptions**: Evaluate the existing data platform to identify assumptions based on human users.
2. **Evaluate Limitations**: Determine the limitations of the current platform in handling autonomous agent workloads.

## Designing Context Serving Layer
1. **Create Fresh Data Sources**: Ensure data sources provide fresh, joinable, and cheap-to-query runtime data.
2. **Implement Scalability**: Design the context serving layer to handle high concurrency and unpredictable access patterns.

## Migrating Codebase
1. **Transition from Python to Rust**: Migrate the codebase to Rust, ensuring compatibility with agent-driven workloads.
2. **Ensure Compatibility**: Verify that the migrated codebase supports autonomous agent queries and workflows.

## Optimizing Queries
1. **Implement Query Optimization Techniques**: Optimize queries for narrow, wide, and join-heavy workloads.
2. **Handle Autonomous Agent Workloads**: Ensure the optimized queries can handle continuous, autonomous queries efficiently.

## Validation and Testing
1. **Performance Testing**: Measure query response times and ensure they meet agent-driven workload requirements.
2. **Reliability Testing**: Verify the system's ability to handle continuous, autonomous queries without failure.

For more detailed steps and examples, refer to the [Core Concepts](references/core_concepts.md) and [Code Examples](references/code_examples.md).

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[OpenXData Conference](https://www.youtube.com/watch?v=YInxWv_4N7w)** by MLOps.community