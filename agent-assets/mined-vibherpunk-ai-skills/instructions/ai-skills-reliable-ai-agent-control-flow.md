# Copilot Instructions: Reliable Ai Agent Control Flow
Description: Design and implement a reliable control flow for AI agents by leveraging state machines and harness engineering to ensure predictable, cost-effective, and efficient execution of multi-step workflows.

### Overview

To build reliable AI agents, it's crucial to manage control flow effectively. This skill focuses on designing a state machine that directs the AI model's actions, ensuring it performs specific tasks without deviating from the intended workflow. By leveraging harness engineering, you can reduce costs, improve latency, and enhance reliability.

### Step-by-Step Workflow

1. **Define the State Machine**: Identify the distinct steps in your workflow (e.g., intro, teach, check, grade, advance, wrap). Each step should have a clear purpose and transition logic.

2. **Design the Harness**: Create a harness that manages the state transitions and validates the model's outputs. The harness should decide the next step based on the current state and the model's response.

3. **Implement Neural Contracts**: For each step, define a neural contract that specifies the input and expected output. This confines the model to performing a specific action.

4. **Integrate the Model**: Use a smaller, cost-effective model (e.g., Haiku 4.5) and rely on the harness to guide its actions. The model should only propose outputs, not decide the next steps.

5. **Log and Monitor**: Implement logging to track state transitions and model outputs. This helps in debugging and ensuring the workflow runs as expected.

6. **Test and Validate**: Run the workflow with various scenarios to ensure reliability. Validate that the harness correctly manages state transitions and the model adheres to the neural contracts.

### Code Snippets

```python
# Example state machine implementation
class StateMachine:
    def __init__(self):
        self.state = 'intro'

    def transition(self, model_output):
        if self.state == 'intro' and model_output == 'done':
            self.state = 'teach'
        elif self.state == 'teach' and model_output == 'done':
            self.state = 'check'
        # Add more transitions as needed

# Example neural contract
neural_contract = {
    'input': 'Teach the concept of photosynthesis',
    'expected_output': 'A detailed explanation of photosynthesis'
}
```

### Best Practices

- **Confine the Model**: Ensure the model only performs specific actions by using neural contracts.
- **Use Smaller Models**: Leverage smaller models guided by a harness to save costs and improve latency.
- **Log Everything**: Implement comprehensive logging to track state transitions and model outputs.

### Common Pitfalls

- **Over-reliance on the Model**: Avoid letting the model decide the next steps, as it can lead to unreliable workflows.
- **Complex State Machines**: Keep the state machine simple and well-defined to avoid confusion and errors.

### Validation Steps

1. **Unit Testing**: Test each state transition and neural contract individually.
2. **Integration Testing**: Run the entire workflow with various scenarios to ensure reliability.
3. **Monitoring**: Continuously monitor the logs to detect and fix any issues.

For more detailed information, refer to the [Core Concepts](references/core_concepts.md) and [Practical Guide](references/practical_guide.md).

## Reference Guides

### Core Concepts

# Core Concepts

### State Machines

A state machine is a mathematical model used to design systems with a finite number of states. In the context of AI agents, a state machine helps manage the control flow by defining distinct steps and transitions between them.

### Harness Engineering

Harness engineering involves creating a framework that directs the actions of an AI model. Instead of letting the model decide the next steps, the harness manages state transitions and validates the model's outputs. This ensures reliability and efficiency.

### Neural Contracts

Neural contracts specify the input and expected output for each step in the workflow. They confine the model to performing specific actions, reducing the risk of deviations.

### Smaller Models

Using smaller, cost-effective models guided by a harness can save costs and improve latency. The harness ensures the model performs at the expected level, even with reduced reasoning capabilities.

### Logging and Monitoring

Comprehensive logging helps track state transitions and model outputs, making it easier to debug and ensure the workflow runs as expected.

### Validation

Unit testing, integration testing, and continuous monitoring are essential for validating the reliability of the control flow.

For practical implementation, refer to the [Practical Guide](references/practical_guide.md).

### Practical Guide

# Practical Guide

### Defining the State Machine

1. **Identify Steps**: List the distinct steps in your workflow (e.g., intro, teach, check, grade, advance, wrap).
2. **Define Transitions**: Specify the conditions for transitioning between steps.
3. **Implement Logic**: Write code to manage state transitions based on the model's outputs.

### Designing the Harness

1. **Create Framework**: Develop a framework that manages state transitions and validates model outputs.
2. **Integrate Model**: Use the harness to guide the model's actions, ensuring it adheres to neural contracts.
3. **Log Transitions**: Implement logging to track state transitions and model outputs.

### Implementing Neural Contracts

1. **Specify Inputs**: Define the input for each step.
2. **Define Outputs**: Specify the expected output for each step.
3. **Validate Outputs**: Ensure the model's outputs match the expected outputs.

### Using Smaller Models

1. **Select Model**: Choose a smaller, cost-effective model (e.g., Haiku 4.5).
2. **Guide Actions**: Use the harness to guide the model's actions, ensuring it performs at the expected level.

### Logging and Monitoring

1. **Implement Logging**: Add logging to track state transitions and model outputs.
2. **Monitor Logs**: Continuously monitor the logs to detect and fix any issues.

### Testing and Validation

1. **Unit Testing**: Test each state transition and neural contract individually.
2. **Integration Testing**: Run the entire workflow with various scenarios to ensure reliability.
3. **Continuous Monitoring**: Continuously monitor the workflow to ensure it runs as expected.

For more detailed information, refer to the [Core Concepts](references/core_concepts.md).

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Don't Let the LLM Drive - Ornella Bahidika & Joel Allou, Microsoft](https://www.youtube.com/watch?v=m24UKZomm7k)** by AI Engineer