# Copilot Instructions: Building A Decoupled Ai Agent Architecture
Description: This skill teaches you how to design and implement a decoupled AI agent architecture with a focus on the execution layer, ensuring durability, observability, and flexibility.

## Overview

Building a robust AI agent architecture requires a clear separation of concerns to handle the rapid evolution of models, tools, and frameworks. This skill focuses on decoupling the architecture into three layers: **Execution**, **Context**, and **Compute**. The execution layer is the most stable and critical for ensuring durability, observability, and flexibility. Learn more about the core concepts in [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow

1. **Identify the Layers**: Separate your architecture into Execution, Context, and Compute layers. The Execution layer handles flow, state, and retries; the Context layer manages models, prompts, and tools; and the Compute layer deals with sandboxes and runtimes.

2. **Design the Execution Layer**: Focus on durability, resumability, and observability. Ensure that state is external and durable, allowing the system to resume after failures. Implement flexible orchestration primitives for crons, event triggers, and sub-agent coordination. See practical examples in [Practical Guide](references/practical_guide.md).

3. **Decouple Context and Compute**: Keep the Context layer independent of the Compute layer. This allows you to swap models, prompts, or sandboxes without affecting the Execution layer.

4. **Implement Observability**: Ensure full session traces across LLM calls, tool calls, and system errors. This is crucial for debugging and improving your agent. Use tools like Ingest for durable execution and observability.

5. **Test and Validate**: Validate your architecture by simulating failures and ensuring resumability. Test different invocation patterns (crons, event triggers) and observe the system's behavior. Detailed validation steps are provided in [Validation Steps](references/validation_steps.md).

## Code Snippets

```python
# Example of a durable execution layer
from ingest import ExecutionLayer

execution_layer = ExecutionLayer()
execution_layer.run(task, retries=3, state_store='external')
```

## Best Practices

- **Decouple Layers**: Avoid merging layers to prevent technical debt. For example, don't embed orchestration logic within the Context layer.
- **External State**: Store state externally to ensure resumability. Avoid relying on in-memory or disk-based state for long-running tasks.
- **Flexible Orchestration**: Use primitives like crons, event triggers, and sub-agent coordination to handle various invocation patterns.

## Common Pitfalls

- **Tight Coupling**: Merging layers leads to inflexibility and technical debt. For example, embedding retry logic within prompts makes it hard to swap models.
- **In-Memory State**: Relying on in-memory state for long-running tasks results in lost work during failures.
- **Poor Observability**: Lack of full session traces makes debugging and improving agents difficult.

## Validation Steps

1. **Simulate Failures**: Test how your system handles failures in LLM calls, tool calls, and sandboxes.
2. **Check Resumability**: Ensure the system can resume from the point of failure without restarting.
3. **Test Invocation Patterns**: Validate crons, event triggers, and sub-agent coordination.
4. **Observe Traces**: Verify that full session traces are available for debugging and analysis.

For more detailed guidance, refer to [Core Concepts](references/core_concepts.md), [Practical Guide](references/practical_guide.md), and [Validation Steps](references/validation_steps.md).

## Reference Guides

### Core Concepts

# Core Concepts

## Execution Layer

The Execution layer is the brain of your AI agent architecture. It manages the flow, state, durability, and retries of your system. This layer is designed to remain stable even as other components evolve. Key responsibilities include:

- **Flow Management**: Coordinating the sequence of tasks, such as planning, model calls, and tool invocations.
- **State Durability**: Ensuring that state is stored externally and can be resumed after failures.
- **Retries**: Handling retries for failed LLM calls, tool calls, and other operations.

## Context Layer

The Context layer is the knowledge hub of your architecture. It includes models, prompts, tools, and memory. This layer changes frequently as new models and tools emerge. Key responsibilities include:

- **Model Management**: Swapping models without affecting the Execution layer.
- **Prompt Engineering**: Designing and updating prompts to improve agent performance.
- **Tool Integration**: Integrating new tools and APIs as needed.

## Compute Layer

The Compute layer is the hands of your architecture. It includes sandboxes, runtimes, and browsers that your agent automates. This layer is ephemeral and stateless by design. Key responsibilities include:

- **Sandbox Execution**: Running code in isolated environments.
- **Browser Automation**: Automating web interactions.
- **File Manipulation**: Handling file operations within the sandbox.

By decoupling these layers, you can build a flexible and durable AI agent architecture that evolves with the rapidly changing landscape of AI tools and models.

### Practical Guide

# Practical Guide

## Designing the Execution Layer

1. **External State Storage**: Use a durable external store like a database or cloud storage to persist state. This ensures that your system can resume after failures.

```python
# Example of external state storage
from ingest import ExecutionLayer

execution_layer = ExecutionLayer(state_store='external')
```

2. **Flexible Orchestration**: Implement primitives for crons, event triggers, and sub-agent coordination. This allows your system to handle various invocation patterns.

```python
# Example of cron scheduling
execution_layer.schedule(task, cron='*/30 * * * *')
```

3. **Full Session Traces**: Ensure that every session is traceable from start to finish. This includes LLM calls, tool calls, and system errors.

```python
# Example of session tracing
execution_layer.trace(session_id)
```

## Decoupling Context and Compute

1. **Model Swapping**: Design your Context layer to allow easy swapping of models without affecting the Execution layer.

```python
# Example of model swapping
context_layer.swap_model(new_model)
```

2. **Sandbox Isolation**: Ensure that the Compute layer is stateless and ephemeral. Use sandboxes for isolated code execution.

```python
# Example of sandbox execution
compute_layer.run_in_sandbox(code)
```

## Implementing Observability

1. **Session Monitoring**: Monitor every session for performance, errors, and outcomes. Use tools like Ingest for comprehensive observability.

```python
# Example of session monitoring
execution_layer.monitor(session_id)
```

2. **Feedback Loops**: Implement feedback loops to continuously improve your agent based on user feedback and session outcomes.

```python
# Example of feedback loop
feedback_loop.run(session_id)
```

By following these practical steps, you can build a robust and flexible AI agent architecture that evolves with the rapidly changing landscape of AI tools and models.

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Your agent architecture has a half-life of 6 months — Dan Farrelly, CTO, Inngest](https://www.youtube.com/watch?v=X1kp-ABIIxQ)** by AI Engineer

### Validation Steps

# Validation Steps

## Simulating Failures

1. **LLM Call Failures**: Simulate failures in LLM calls to test your system's retry logic.

```python
# Example of simulating LLM call failure
execution_layer.simulate_failure('llm_call')
```

2. **Tool Call Failures**: Simulate failures in tool calls to ensure your system can handle them gracefully.

```python
# Example of simulating tool call failure
execution_layer.simulate_failure('tool_call')
```

3. **Sandbox Failures**: Simulate sandbox crashes to test your system's ability to resume.

```python
# Example of simulating sandbox failure
execution_layer.simulate_failure('sandbox')
```

## Checking Resumability

1. **State Recovery**: Ensure that your system can recover state after a failure and resume from the point of interruption.

```python
# Example of state recovery
execution_layer.recover_state(session_id)
```

2. **Task Continuation**: Verify that tasks continue from where they left off after a failure.

```python
# Example of task continuation
execution_layer.continue_task(session_id)
```

## Testing Invocation Patterns

1. **Cron Scheduling**: Test cron scheduling to ensure tasks run at the specified intervals.

```python
# Example of testing cron scheduling
execution_layer.test_cron(task, cron='*/30 * * * *')
```

2. **Event Triggers**: Test event triggers to ensure tasks are invoked correctly.

```python
# Example of testing event triggers
execution_layer.test_event_trigger(task, event='user_input')
```

3. **Sub-Agent Coordination**: Test sub-agent coordination to ensure tasks are delegated correctly.

```python
# Example of testing sub-agent coordination
execution_layer.test_sub_agent_coordination(task)
```

## Observing Traces

1. **Session Traces**: Verify that full session traces are available for debugging and analysis.

```python
# Example of observing session traces
execution_layer.observe_trace(session_id)
```

2. **Performance Metrics**: Check performance metrics to identify bottlenecks and areas for improvement.

```python
# Example of checking performance metrics
execution_layer.check_performance(session_id)
```

By following these validation steps, you can ensure that your AI agent architecture is robust, durable, and flexible.