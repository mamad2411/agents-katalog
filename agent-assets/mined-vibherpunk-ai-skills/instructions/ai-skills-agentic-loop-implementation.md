# Copilot Instructions: Agentic Loop Implementation
Description: Implement autonomous agentic loops for binary decision tasks, with safeguards for non-binary scenarios requiring human review.

# Agentic Loop Implementation Guide

## Overview
Agentic loops enable autonomous AI operation by combining comprehensive initial prompts with self-validation mechanisms. As detailed in [Core Concepts](references/core_concepts.md), these work best for binary decision tasks where success criteria are clearly measurable.

## Step-by-Step Workflow
1. **Task Assessment**
   - Verify the task has binary success criteria
   - Document all known edge cases

2. **Prompt Construction**
   - Create master prompt with:
     - Clear success metrics
     - Validation instructions
     - Iteration limits
   - See templates in [Code Examples](references/code_examples.md)

3. **Validation Layer**
   - Implement automated checks for:
     - Completion state
     - Quality thresholds
     - Safety boundaries

4. **Execution Protocol**
   - Run agent with iteration limits
   - Capture all intermediate states
   - Implement human escalation triggers

## Best Practices
- Start with simple binary tasks before complex flows
- Log all agent assumptions for audit trails
- Set strict iteration limits to prevent infinite loops

## Common Pitfalls
- **Assumption Overreach**: Agents filling unspecified details incorrectly (payment flow example in transcript)
- **Metric Gaming**: Agents optimizing for scores rather than true quality
- **Validation Gaps**: Missing edge cases in automated checks

## Validation Steps
1. Unit test validation layer with known good/bad outputs
2. Run controlled experiments with:
   - Perfect input data
   - Partially flawed data
   - Edge case data
3. Monitor real-world performance with human spot checks

For comprehensive implementation guidance, review [Practical Guide](references/practical_guide.md) and sample code in [Code Examples](references/code_examples.md).

## Reference Guides

### Code Examples

# Agentic Loop Code Examples

## Basic Binary Implementation
```python
# Code review agentic loop example
def agentic_code_review(code):
    max_iterations = 5
    target_score = 5
    
    for attempt in range(max_iterations):
        reviewed_code, score = code_review_agent(code)
        if score >= target_score:
            return reviewed_code
        code = code_fixing_agent(reviewed_code, score)
    
    raise Exception(f"Failed to achieve target score after {max_iterations} attempts")
```

## Prompt Template
```
You are an autonomous code improvement agent. Your goal is to achieve a perfect 5/5 score on these metrics:
1. PEP8 compliance (binary)
2. 100% test coverage (binary)
3. Zero linting errors (binary)

For each iteration:
1. Run all validation checks
2. If any check fails, generate specific fixes
3. Apply fixes and repeat validation
4. Stop when all checks pass or after 5 attempts

Current code:
{code}
```

## Validation Snippet
```python
def validate_agent_output(output, criteria):
    """Returns True only if all binary criteria are met"""
    return all(
        criterion['validator'](output) 
        for criterion in criteria
    )
```

### Core Concepts

# Agentic Loop Core Concepts

Agentic loops represent a paradigm shift from traditional human-in-the-loop prompting to autonomous AI systems that self-validate. Unlike standard workflows where humans repeatedly review and adjust prompts, agentic loops attempt to complete entire tasks through a single comprehensive prompt with built-in validation mechanisms.

Key characteristics:
1. **Autonomy**: The system operates independently after initial prompt
2. **Self-validation**: Built-in checks verify output quality
3. **Binary optimization**: Works best with clear pass/fail criteria
4. **Assumption risk**: The agent fills unspecified details automatically

Example scenario from transcript: Code review systems work well because they can clearly define success (5/5 score) and automatically iterate until achieving it. However, complex UI flows fail because the agent makes incorrect assumptions about screen sequences.

Implementation considerations:
- Success must be quantitatively measurable
- The domain should have limited variability
- Edge cases should be either nonexistent or handled by default behaviors
- The cost of wrong assumptions must be low

### Practical Guide

# Practical Guide to Agentic Loops

## When to Use
Implement agentic loops for:
- Automated testing frameworks
- Code quality review systems
- Binary classification tasks
- Pass/fail compliance checks

## When to Avoid
Use traditional human-in-the-loop for:
- Creative tasks with subjective outcomes
- Multi-step processes with many decision points
- Scenarios where wrong assumptions have high costs

## Implementation Framework
1. **Define Clear Metrics**: Establish quantitative success criteria (e.g. test coverage percentages, code review scores)
2. **Build Validation Steps**: Create automated checks that run after each iteration
3. **Set Failure Protocols**: Determine when the system should stop trying (maximum iterations or time limits)
4. **Human Escalation Paths**: For non-binary cases, include protocols to notify human reviewers

## Transcript Example Analysis
The payment flow failure mentioned in the transcript demonstrates why complex business processes often need human oversight. The agent cannot reliably predict all possible system states after a payment failure, while a code scoring system can objectively measure quality against predefined rubrics.

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Agentic Loops the future of prompting? I’ll break it down in 60s.](https://www.youtube.com/watch?v=ytO3bJWofmw)** by Greg Isenberg