# Copilot Instructions: Autoresearchoptimization
Description: A skill enabling AI agents to autonomously optimize skills and processes using Karpathy's Auto Research framework. It involves defining criteria, running iterative hypothesis tests, and evaluating outcomes to achieve measurable improvements.

# AutoResearchOptimization Skill

## Overview
This skill leverages Karpathy's Auto Research framework to enable AI agents to autonomously optimize skills and processes. It involves defining clear criteria, running iterative hypothesis tests, and evaluating outcomes to achieve measurable improvements. For a deeper understanding of the core concepts, refer to [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow
1. **Define Optimization Criteria**: Clearly state the conditions you want to optimize. Each criterion should be specific and testable. For example, "The first line must be under 136 characters."
2. **Establish Baseline**: Run initial tests to determine the current performance level. This serves as the baseline for comparison.
3. **Generate Hypothesis**: Create hypotheses on how to improve the baseline. For example, "Adding an explicit character limit for hooks will improve performance."
4. **Run Iterative Tests**: Execute tests with the updated skill or process to evaluate the hypothesis.
5. **Evaluate Outcomes**: Use deterministic scripts or AI judges to assess if the hypothesis led to improvements.
6. **Decide on Changes**: Keep the changes if they improve the baseline; discard them if they do not.
7. **Repeat Until Goal is Met**: Continue the loop until the desired optimization goal is achieved or the maximum number of iterations is reached.

## Code Snippets and Prompt Templates
```python
# Example prompt for defining criteria
criteria = [
    "The first line must be under 136 characters.",
    "Bullet points must use hyphens."
]

# Example prompt for generating a hypothesis
hypothesis = "Adding an explicit character limit for hooks will improve performance."
```

## Best Practices and Common Pitfalls
- **Best Practices**:
  - Define specific and testable criteria.
  - Use real-world data to inform criteria and hypotheses.
  - Limit the number of iterations to avoid diminishing returns.
- **Common Pitfalls**:
  - Vague criteria lead to ineffective optimization.
  - Running too many iterations can increase costs without significant improvements.

## Validation and Testing Steps
1. **Baseline Testing**: Ensure the initial tests accurately reflect current performance.
2. **Hypothesis Validation**: Verify that each hypothesis is logically sound and testable.
3. **Outcome Evaluation**: Use unbiased methods to assess the impact of each hypothesis.
4. **Final Assessment**: Confirm that the optimized skill or process meets the defined criteria.

For practical implementation guidelines, refer to [Practical Guide](references/practical_guide.md). For detailed code examples, see [Code Examples](references/code_examples.md).

## Reference Guides

### Code Examples

# Code Examples for Auto Research Optimization

This document provides detailed code examples and prompt templates for implementing Auto Research Optimization. These examples illustrate how to define criteria, generate hypotheses, and run iterative tests.

## Defining Criteria
```python
# Example prompt for defining criteria
criteria = [
    "The first line must be under 136 characters.",
    "Bullet points must use hyphens."
]
```

## Generating Hypotheses
```python
# Example prompt for generating a hypothesis
hypothesis = "Adding an explicit character limit for hooks will improve performance."
```

## Running Iterative Tests
```python
# Example code for running iterative tests
for iteration in range(max_iterations):
    test_result = run_test(updated_skill, criteria)
    if evaluate_outcome(test_result):
        keep_changes()
    else:
        discard_changes()
```

## Evaluating Outcomes
```python
# Example code for evaluating outcomes
def evaluate_outcome(test_result):
    if test_result >= baseline_score:
        return True
    else:
        return False
```

## Decision Making
```python
# Example code for decision making
if evaluate_outcome(test_result):
    keep_changes()
else:
    discard_changes()
```

## Practical Applications
These code examples can be applied to various domains, including marketing, sales, customer support, and more. For example, optimizing LinkedIn posts for engagement, improving email open rates, or enhancing landing page conversions.

For a deeper understanding of the core concepts, refer to [Core Concepts](references/core_concepts.md). For practical implementation guidelines, see [Practical Guide](references/practical_guide.md).

### Core Concepts

# Core Concepts of Auto Research Optimization

Auto Research Optimization is a framework introduced by Andre Karpathy, designed to enable AI agents to autonomously improve their performance. The core idea revolves around iterative testing and hypothesis evaluation to achieve measurable improvements in skills and processes.

## Key Components
1. **Criteria Definition**: The foundation of optimization lies in defining clear, specific, and testable criteria. These criteria serve as the benchmarks against which improvements are measured.
2. **Baseline Establishment**: Before any optimization can occur, it's crucial to establish a baseline performance level. This involves running initial tests to determine the current state of the skill or process.
3. **Hypothesis Generation**: Hypotheses are educated guesses on how to improve the baseline. They should be specific and directly related to the defined criteria.
4. **Iterative Testing**: This involves running tests with the updated skill or process to evaluate the effectiveness of the hypothesis. Each iteration provides data to inform the next steps.
5. **Outcome Evaluation**: The results of each test are evaluated to determine if the hypothesis led to improvements. This can be done using deterministic scripts or AI judges.
6. **Decision Making**: Based on the evaluation, decisions are made to keep or discard the changes. The process repeats until the optimization goal is achieved.

## Practical Applications
Auto Research Optimization can be applied to various domains, including marketing, sales, customer support, and more. For example, optimizing LinkedIn posts for engagement, improving email open rates, or enhancing landing page conversions.

## Benefits
- **Autonomy**: The framework allows AI agents to autonomously optimize skills and processes, reducing the need for manual intervention.
- **Measurable Improvements**: By defining clear criteria, improvements can be quantified and tracked.
- **Scalability**: The iterative nature of the framework makes it scalable across different tasks and processes.

For practical implementation guidelines, refer to [Practical Guide](references/practical_guide.md). For detailed code examples, see [Code Examples](references/code_examples.md).

### Practical Guide

# Practical Guide to Auto Research Optimization

Implementing Auto Research Optimization involves a series of well-defined steps to ensure effective and measurable improvements. This guide provides practical advice on how to apply the framework to optimize skills and processes.

## Step-by-Step Implementation
1. **Define Clear Criteria**: Start by defining specific and testable criteria. For example, "The first line must be under 136 characters."
2. **Establish Baseline**: Run initial tests to determine the current performance level. This serves as the baseline for comparison.
3. **Generate Hypotheses**: Create hypotheses on how to improve the baseline. Ensure each hypothesis is specific and directly related to the defined criteria.
4. **Run Iterative Tests**: Execute tests with the updated skill or process to evaluate the hypothesis. Each iteration provides data to inform the next steps.
5. **Evaluate Outcomes**: Use deterministic scripts or AI judges to assess if the hypothesis led to improvements.
6. **Decide on Changes**: Keep the changes if they improve the baseline; discard them if they do not.
7. **Repeat Until Goal is Met**: Continue the loop until the desired optimization goal is achieved or the maximum number of iterations is reached.

## Best Practices
- **Specific Criteria**: Ensure each criterion is specific and testable. Vague criteria lead to ineffective optimization.
- **Real-World Data**: Use real-world data to inform criteria and hypotheses. This increases the relevance and effectiveness of the optimization.
- **Limit Iterations**: Limit the number of iterations to avoid diminishing returns and increased costs.

## Common Pitfalls
- **Vague Criteria**: Avoid defining vague criteria that are difficult to test and measure.
- **Excessive Iterations**: Running too many iterations can increase costs without significant improvements.
- **Ignoring Real-World Data**: Failing to use real-world data can result in irrelevant or ineffective optimizations.

For a deeper understanding of the core concepts, refer to [Core Concepts](references/core_concepts.md). For detailed code examples, see [Code Examples](references/code_examples.md).

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[How to use Karpathy's Autoresearch to 10x Claude](https://www.youtube.com/watch?v=bc4NrE0cOE0)** by Ben AI