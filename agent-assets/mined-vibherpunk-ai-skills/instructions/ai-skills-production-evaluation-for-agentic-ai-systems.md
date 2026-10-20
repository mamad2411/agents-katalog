# Copilot Instructions: Production Evaluation For Agentic Ai Systems
Description: A comprehensive skill for evaluating agentic AI systems in production environments, focusing on workflow behavior, reliability, and continuous monitoring.

## Overview

Agentic AI systems have fundamentally changed the landscape of AI evaluation. Unlike traditional models that generate answers, agentic systems plan, call tools, retrieve information, execute workflows, and interact with production infrastructure. This shift necessitates a new approach to evaluation that focuses on system behavior rather than just model outputs.

### Core Concepts

1. **Workflow Evaluation**: Instead of evaluating individual outputs, assess the entire workflow, including planning quality, tool usage, execution, and recovery from failures.
2. **Production Telemetry**: Utilize real user interactions and system behavior data as the most valuable evaluation signals.
3. **Continuous Monitoring**: Implement ongoing evaluation to detect and address system drift and reliability degradation.
4. **Reliability Metrics**: Focus on metrics like task completion, tool success, escalation rate, safety violations, latency, cost, and recovery rate.

For a deeper dive into these concepts, refer to [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow

1. **Define Evaluation Scenarios**: Identify key workflows that the agentic system will perform, such as customer support, code generation, or research workflows.
2. **Simulate Workflows**: Create simulated environments where the agent operates, and measure task completion rate, tool correctness, planning quality, and resource usage.
3. **Collect Production Telemetry**: Continuously gather execution traces, user outcomes, escalations, failures, and feedback signals from real user interactions.
4. **Implement Continuous Monitoring**: Set up observability tools to capture detailed traces of reasoning paths, tool calls, memory access, execution timelines, and state transitions.
5. **Combine Automated and Human Evaluation**: Use automated metrics for scalability and targeted human reviews for assessing correctness, trust, usefulness, and safety.
6. **Analyze and Iterate**: Regularly analyze evaluation data to identify drift, improve workflows, and update evaluation pipelines.

For practical implementation steps, see [Practical Guide](references/practical_guide.md).

## Code Snippets and Prompt Templates

```python
# Example: Setting up continuous monitoring for an agentic system
import logging
import traceback

class AgentMonitor:
    def __init__(self):
        self.logger = logging.getLogger('AgentMonitor')
        self.logger.setLevel(logging.INFO)

    def log_execution_trace(self, trace):
        self.logger.info(f'Execution Trace: {trace}')

    def log_failure(self, exception):
        self.logger.error(f'Failure: {exception}', exc_info=True)

# Usage
monitor = AgentMonitor()
monitor.log_execution_trace('Tool call: retrieve_info')
monitor.log_failure(Exception('Tool execution failed'))
```

For more code examples, refer to [Code Examples](references/code_examples.md).

## Best Practices and Common Pitfalls

### Best Practices

- **Scenario-Driven Evaluation**: Focus on evaluating entire workflows rather than individual prompts.
- **Combine Metrics**: Use a combination of reliability, availability, latency, cost, and recovery metrics.
- **Continuous Monitoring**: Implement ongoing evaluation to detect and address system drift.

### Common Pitfalls

- **Over-Reliance on Benchmarks**: Benchmarks measure model capability but miss system behavior.
- **Ignoring Human Feedback**: Humans provide critical signals that automated systems cannot.
- **Neglecting Drift Detection**: Without continuous monitoring, reliability degradation can go unnoticed.

For detailed best practices and pitfalls, see [Common Pitfalls](references/common_pitfalls.md).

## Validation and Testing Steps

1. **Scenario Validation**: Validate simulated workflows against real-world scenarios to ensure accuracy and relevance.
2. **Telemetry Accuracy**: Verify that collected telemetry data accurately reflects system behavior.
3. **Metric Calibration**: Calibrate evaluation metrics using human feedback to ensure they capture the correct signals.
4. **Drift Detection Testing**: Test continuous monitoring systems to ensure they can detect and alert on system drift.

## References

```json
[
    {
        "filename": "core_concepts.md",
        "content": "# Core Concepts\n\nAgentic AI systems require a shift from traditional model evaluation to workflow evaluation. This involves assessing planning quality, tool usage, execution, and recovery from failures. Production telemetry, derived from real user interactions, provides the most valuable evaluation signals. Continuous monitoring is essential to detect system drift and reliability degradation. Reliability metrics, such as task completion, tool success, escalation rate, safety violations, latency, cost, and recovery rate, become the focus of evaluation efforts.\n\n## Key Points\n\n- **Workflow Evaluation**: Assess entire workflows rather than individual outputs.\n- **Production Telemetry**: Utilize real user interactions and system behavior data.\n- **Continuous Monitoring**: Implement ongoing evaluation to detect and address system drift.\n- **Reliability Metrics**: Focus on metrics that reflect system reliability and operational success."
    },
    {
        "filename": "practical_guide.md",
        "content": "# Practical Guide\n\nImplementing production evaluation for agentic AI systems involves several key steps. First, define evaluation scenarios that reflect real-world workflows. Simulate these workflows in controlled environments and measure task completion rate, tool correctness, planning quality, and resource usage. Collect production telemetry continuously, including execution traces, user outcomes, escalations, failures, and feedback signals.\n\n## Implementation Steps\n\n1. **Define Evaluation Scenarios**: Identify key workflows the system will perform.\n2. **Simulate Workflows**: Create simulated environments for the agent to operate in.\n3. **Collect Production Telemetry**: Gather data from real user interactions.\n4. **Implement Continuous Monitoring**: Set up observability tools to capture detailed traces.\n5. **Combine Automated and Human Evaluation**: Use both automated metrics and human reviews.\n6. **Analyze and Iterate**: Regularly analyze evaluation data to improve workflows.\n\n## Tools and Techniques\n\n- **Observability Tools**: Use tools like distributed tracing to capture detailed execution traces.\n- **Human Review**: Incorporate targeted human reviews to assess correctness, trust, usefulness, and safety.\n- **Continuous Monitoring**: Implement systems that continuously monitor and evaluate system behavior."
    },
    {
        "filename": "code_examples.md",
        "content": "# Code Examples\n\nHere are some practical code examples for implementing production evaluation for agentic AI systems.\n\n## Continuous Monitoring Setup\n\n```python\nimport logging\nimport traceback\n\nclass AgentMonitor:\n    def __init__(self):\n        self.logger = logging.getLogger('AgentMonitor')\n        self.logger.setLevel(logging.INFO)\n\n    def log_execution_trace(self, trace):\n        self.logger.info(f'Execution Trace: {trace}')\n\n    def log_failure(self, exception):\n        self.logger.error(f'Failure: {exception}', exc_info=True)\n\n# Usage\nmonitor = AgentMonitor()\nmonitor.log_execution_trace('Tool call: retrieve_info')\nmonitor.log_failure(Exception('Tool execution failed'))\n```\n\n## Scenario Simulation\n\n```python\ndef simulate_workflow(scenario):\n    # Simulate the workflow based on the scenario\n    pass\n\n# Example scenario\nscenario = 'customer_support'\nsimulate_workflow(scenario)\n```\n\n## Telemetry Collection\n\n```python\ndef collect_telemetry(data):\n    # Collect telemetry data from the system\n    pass\n\n# Example telemetry data\ndata = {'execution_trace': 'retrieve_info', 'outcome': 'success'}\ncollect_telemetry(data)\n```"
    },
    {
        "filename": "common_pitfalls.md",
        "content": "# Common Pitfalls\n\nWhen evaluating agentic AI systems in production, several common pitfalls can undermine the effectiveness of your evaluation efforts.\n\n## Over-Reliance on Benchmarks\n\nBenchmarks measure model capability but miss system behavior. Relying solely on benchmarks can lead to high scores in controlled environments but unreliable performance in production.\n\n## Ignoring Human Feedback\n\nHumans provide critical signals that automated systems cannot. Neglecting human feedback can result in blind spots in your evaluation metrics and missed opportunities for improvement.\n\n## Neglecting Drift Detection\n\nWithout continuous monitoring, system drift and reliability degradation can go unnoticed. This can lead to gradual declines in performance and user satisfaction.\n\n## Best Practices to Avoid Pitfalls\n\n- **Scenario-Driven Evaluation**: Focus on evaluating entire workflows rather than individual prompts.\n- **Combine Metrics**: Use a combination of reliability, availability, latency, cost, and recovery metrics.\n- **Continuous Monitoring**: Implement ongoing evaluation to detect and address system drift.\n- **Human Feedback**: Incorporate targeted human reviews to assess correctness, trust, usefulness, and safety."
    }
]


## Reference Guides

### Code Examples

# Code Examples

Here are some practical code examples for implementing production evaluation for agentic AI systems.

## Continuous Monitoring Setup

```python
import logging
import traceback

class AgentMonitor:
    def __init__(self):
        self.logger = logging.getLogger('AgentMonitor')
        self.logger.setLevel(logging.INFO)

    def log_execution_trace(self, trace):
        self.logger.info(f'Execution Trace: {trace}')

    def log_failure(self, exception):
        self.logger.error(f'Failure: {exception}', exc_info=True)

# Usage
monitor = AgentMonitor()
monitor.log_execution_trace('Tool call: retrieve_info')
monitor.log_failure(Exception('Tool execution failed'))
```

## Scenario Simulation

```python
def simulate_workflow(scenario):
    # Simulate the workflow based on the scenario
    pass

# Example scenario
scenario = 'customer_support'
simulate_workflow(scenario)
```

## Telemetry Collection

```python
def collect_telemetry(data):
    # Collect telemetry data from the system
    pass

# Example telemetry data
data = {'execution_trace': 'retrieve_info', 'outcome': 'success'}
collect_telemetry(data)
```

### Common Pitfalls

# Common Pitfalls

When evaluating agentic AI systems in production, several common pitfalls can undermine the effectiveness of your evaluation efforts.

## Over-Reliance on Benchmarks

Benchmarks measure model capability but miss system behavior. Relying solely on benchmarks can lead to high scores in controlled environments but unreliable performance in production.

## Ignoring Human Feedback

Humans provide critical signals that automated systems cannot. Neglecting human feedback can result in blind spots in your evaluation metrics and missed opportunities for improvement.

## Neglecting Drift Detection

Without continuous monitoring, system drift and reliability degradation can go unnoticed. This can lead to gradual declines in performance and user satisfaction.

## Best Practices to Avoid Pitfalls

- **Scenario-Driven Evaluation**: Focus on evaluating entire workflows rather than individual prompts.
- **Combine Metrics**: Use a combination of reliability, availability, latency, cost, and recovery metrics.
- **Continuous Monitoring**: Implement ongoing evaluation to detect and address system drift.
- **Human Feedback**: Incorporate targeted human reviews to assess correctness, trust, usefulness, and safety.

### Core Concepts

# Core Concepts

Agentic AI systems require a shift from traditional model evaluation to workflow evaluation. This involves assessing planning quality, tool usage, execution, and recovery from failures. Production telemetry, derived from real user interactions, provides the most valuable evaluation signals. Continuous monitoring is essential to detect system drift and reliability degradation. Reliability metrics, such as task completion, tool success, escalation rate, safety violations, latency, cost, and recovery rate, become the focus of evaluation efforts.

## Key Points

- **Workflow Evaluation**: Assess entire workflows rather than individual outputs.
- **Production Telemetry**: Utilize real user interactions and system behavior data.
- **Continuous Monitoring**: Implement ongoing evaluation to detect and address system drift.
- **Reliability Metrics**: Focus on metrics that reflect system reliability and operational success.

### Practical Guide

# Practical Guide

Implementing production evaluation for agentic AI systems involves several key steps. First, define evaluation scenarios that reflect real-world workflows. Simulate these workflows in controlled environments and measure task completion rate, tool correctness, planning quality, and resource usage. Collect production telemetry continuously, including execution traces, user outcomes, escalations, failures, and feedback signals.

## Implementation Steps

1. **Define Evaluation Scenarios**: Identify key workflows the system will perform.
2. **Simulate Workflows**: Create simulated environments for the agent to operate in.
3. **Collect Production Telemetry**: Gather data from real user interactions.
4. **Implement Continuous Monitoring**: Set up observability tools to capture detailed traces.
5. **Combine Automated and Human Evaluation**: Use both automated metrics and human reviews.
6. **Analyze and Iterate**: Regularly analyze evaluation data to improve workflows.

## Tools and Techniques

- **Observability Tools**: Use tools like distributed tracing to capture detailed execution traces.
- **Human Review**: Incorporate targeted human reviews to assess correctness, trust, usefulness, and safety.
- **Continuous Monitoring**: Implement systems that continuously monitor and evaluate system behavior.

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Production Evals For Agentic AI Systems - Nishant Gupta, Meta Superintelligence Labs](https://www.youtube.com/watch?v=vljxQZfJ9wY)** by AI Engineer