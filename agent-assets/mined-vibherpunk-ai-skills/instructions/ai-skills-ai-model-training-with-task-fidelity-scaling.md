# Copilot Instructions: Ai Model Training With Task Fidelity Scaling
Description: A skill for training AI models using high-quality tasks that adhere to strict fidelity criteria, ensuring meaningful model improvement and clean failure modes.

# Skill: AI Model Training with Task Fidelity Scaling

## Overview
This skill teaches you how to implement task fidelity scaling for AI model training, based on Snorkel's research showing that high-quality tasks produce 5x greater performance improvement than low-quality tasks. The methodology focuses on four core quality criteria for tasks and demonstrates how to validate, categorize, and utilize tasks for maximum training effectiveness.

Key concepts are covered in [Core Concepts](references/core_concepts.md), with implementation details in [Practical Guide](references/practical_guide.md) and [Code Examples](references/code_examples.md).

## Step-by-Step Workflow
1. **Task Creation**
   - Define tasks with clear, testable outcomes
   - Specify all dependencies and requirements
   - Ensure tasks are containerized for reproducibility

2. **Quality Validation**
   - Test each task against the four criteria:
     1. Achievability
     2. Non-triviality
     3. Functional correctness
     4. Environmental reliability
   - Bucket tasks as Accepted or Rejected

3. **Benchmarking Setup**
   - Prepare evaluation harness
   - Establish baseline metrics:
     - Tool call frequency
     - Pass rates
     - Output token counts

4. **Failure Analysis**
   - Categorize failures as:
     - Meaningful (logic errors, incomplete tasks)
     - Degenerate (environment issues)
   - Compare failure distributions between Accepted/Rejected tasks

5. **Model Training**
   - Run parallel RL training sessions:
     - One with high-quality (Accepted) tasks
     - One with low-quality (Rejected) tasks
   - Use identical models and compute budgets

6. **Performance Comparison**
   - Measure improvement delta for both training runs
   - Analyze quality impact ratio (expected 5x difference)

## Best Practices
1. **Task Specification**
   - Avoid underspecification (clear testable outcomes)
   - Example: Instead of "Improve this code", specify "Reduce cyclomatic complexity below 5 while maintaining functionality"

2. **Quality Thresholds**
   - Set minimums for tool calls and output tokens
   - Example: Reject tasks solved with <3 tool calls or <100 output tokens

3. **Expert Involvement**
   - Use human experts for:
     - Initial task design
     - Quality rubric creation
     - Ambiguous case resolution

## Common Pitfalls
1. **False Difficulty**
   - Tasks appear hard due to poor specification
   - Example: Tests expecting unrequested outcomes

2. **Environmental Noise**
   - Unstable containers masking true performance
   - Solution: Test environment reliability separately

3. **Binary Thinking**
   - Treating all failures equally
   - Solution: Categorize failures meaningfully

## Validation Steps
1. **Inter-Annotator Agreement**
   - Measure consistency between:
     - Human judges
     - LLM judges
     - Automated checks

2. **Training Delta Verification**
   - Confirm high-quality tasks produce significantly better improvement
   - Expected: 5-6% vs 1% improvement

3. **Failure Mode Analysis**
   - Verify Accepted tasks produce cleaner failure patterns
   - Meaningful failures should dominate

## Implementation Notes
- Start with verifiable domains (coding, math)
- Gradually extend to fuzzy domains with spectrum scoring
- Maintain quality rubrics for consistent evaluation
- Monitor task quality as models improve (avoid saturation)

## Reference Guides

### Code Examples

# Code Examples for Task Fidelity Implementation

## Task Validation Pseudocode
```python
def validate_task(task):
    # Check achievability
    if not test_achievability(task):
        return False, 'Task not achievable'
        
    # Check non-triviality
    if not test_nontrivial(task):
        return False, 'Task too simple'
        
    # Check functional correctness
    if not test_functional(task):
        return False, 'Logic error in task'
        
    # Check environmental reliability
    if not test_environment(task):
        return False, 'Environment unstable'
        
    return True, 'Task meets all quality criteria'

# Example quality test implementation
def test_nontrivial(task):
    baseline_result = run_with_baseline_model(task)
    return baseline_result['tool_calls'] > MIN_TOOL_CALLS and \
           baseline_result['output_tokens'] > MIN_OUTPUT_TOKENS
```

## RL Training Comparison Script
```python
def compare_training_runs(high_quality_tasks, low_quality_tasks):
    # Initialize same model for both runs
    model = initialize_model()
    
    # Train with high-quality tasks
    hq_model = train_rl(model, high_quality_tasks)
    hq_perf = evaluate(hq_model, benchmark_tasks)
    
    # Train with low-quality tasks
    lq_model = train_rl(model, low_quality_tasks)
    lq_perf = evaluate(lq_model, benchmark_tasks)
    
    # Calculate improvement delta
    base_perf = evaluate(model, benchmark_tasks)
    hq_improvement = hq_perf - base_perf
    lq_improvement = lq_perf - base_perf
    
    return {
        'high_quality_improvement': hq_improvement,
        'low_quality_improvement': lq_improvement,
        'quality_impact_ratio': hq_improvement / lq_improvement
    }
```

## Failure Categorization Logic
```python
class FailureAnalyzer:
    def categorize_failure(self, task, failure):
        if self._is_environment_issue(failure):
            return 'environmental'
        elif self._is_logic_error(failure):
            return 'logic_error'
        elif self._is_incomplete(failure):
            return 'incomplete_task'
        else:
            return 'other'
    
    def _is_environment_issue(self, failure):
        return 'container' in failure.logs or \
               'dependency' in failure.logs
    
    def _is_logic_error(self, failure):
        return 'assertion' in failure.logs or \
               'exception' in failure.logs
```

### Core Concepts

# Core Concepts of Task Fidelity Scaling

Task fidelity scaling is a methodology for improving AI model training by ensuring that the tasks used for training and benchmarking meet high-quality standards. The core premise is that the quality of data (and by extension, tasks) is critical to the performance improvements of AI models.

## Key Principles
1. **Task Quality Criteria**: Tasks must be:
   - Achievable: The task can be completed by the model
   - Non-trivial: The task presents meaningful difficulty
   - Functionally correct: The task logic works as intended
   - Environmentally reliable: The execution environment is stable

2. **Quality Impact**: High-quality tasks lead to:
   - More tool calls (demonstrating engagement)
   - Lower pass rates (indicating genuine difficulty)
   - More output tokens (showing deeper reasoning)
   - Cleaner failure modes (failures that provide meaningful signals)

3. **Empirical Validation**: The Snorkel team demonstrated that models trained with high-quality tasks showed 6% improvement compared to just 1% with low-quality tasks, proving the 5x uplift from quality focus.

## Implementation Context
This approach is particularly valuable for:
- Agentic terminal bench-style tasks
- Containerized environments
- Reproducible, isolated task execution
- Parallelized rollouts

The methodology emphasizes that while architectural changes and harness variations matter, data quality remains the central determinant of training outcomes.

### Practical Guide

# Practical Guide to Implementing Task Fidelity Scaling

## Task Creation Guidelines
1. **Specification**: Clearly define:
   - Desired testable outcomes
   - All required dependencies
   - Success criteria upfront

2. **Validation Checks**:
   - Verify task achievability by testing with baseline models
   - Ensure non-triviality by measuring steps/tokens required
   - Confirm functional correctness through unit tests
   - Test environmental reliability across multiple runs

3. **Quality Bucketing**:
   - Accepted tasks: Pass all four quality criteria
   - Rejected tasks: Fail any criteria (environment issues, underspecification, etc.)

## Task Evaluation Framework
1. **Metrics to Track**:
   - Tool call frequency
   - Pass/fail rates
   - Output token count
   - Failure mode categorization

2. **Failure Analysis**:
   - Meaningful failures: Logic errors, incomplete tasks
   - Degenerate failures: Environmental issues, unsolvable problems

3. **Benchmarking**:
   - Compare performance between accepted/rejected task sets
   - Measure improvement delta during RL training

## Scaling Considerations
- Use expert-in-the-loop for quality assurance
- Develop rubrics for both human and LLM judges
- Maintain high inter-annotator agreement
- For fuzzy domains, implement spectrum scoring rather than binary pass/fail

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Task Fidelity Scaling Laws — Kobie Crawdord, Snorkel](https://www.youtube.com/watch?v=YYH0DMQr30A)** by AI Engineer