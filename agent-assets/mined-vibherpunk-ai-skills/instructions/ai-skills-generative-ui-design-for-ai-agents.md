# Copilot Instructions: Generative Ui Design For Ai Agents
Description: A skill for designing and implementing Generative UI layers that bridge AI model outputs and human-friendly interfaces, ensuring seamless, scalable, and user-centric experiences.

### Overview
Generative UI is the layer between AI model outputs and the user interface that ensures the output is rendered in a human-friendly, interactive, and scalable way. This skill focuses on three core patterns: **Rendering Contracts**, **Streaming**, and **Backend for Frontend (BFF)**. Learn how to design these layers effectively to create seamless user experiences.

For a deeper dive into the concepts, see [Core Concepts](references/core_concepts.md).

### Step-by-Step Workflow
1. **Define the Rendering Contract**: Establish a contract between the AI model and the client that specifies UI components and layout rules. Ensure the model outputs structured UI intent rather than raw text.
2. **Implement Streaming**: Use streaming to deliver UI components in chunks, reducing perceived latency. Start with a skeleton UI, progressively fill it, and complete it as data arrives.
3. **Build the BFF**: Create a Backend for Frontend (BFF) that handles platform-specific rendering rules, hydrates UI components, and attaches actions to elements.

For detailed implementation steps, refer to [Practical Guide](references/practical_guide.md).

### Code Snippets
```python
# Example of a Rendering Contract
contract = {
  "components": ["date_field", "time_field", "submit_button"],
  "layout_rules": {
    "flights": {
      "1-3": "swipable_carousel",
      "4+": "vertical_list"
    }
  }
}
```

For more examples, see [Code Examples](references/code_examples.md).

### Best Practices
- **Version Awareness**: Ensure the model is aware of client capabilities by maintaining a version map.
- **Progressive Rendering**: Use streaming to show partial results and keep users engaged.
- **Platform-Specific Rules**: Let the BFF handle platform differences (e.g., Android vs. iOS).

### Common Pitfalls
- **Ignoring Client Capabilities**: Failing to account for client versions can lead to crashes.
- **Overloading the Client**: Avoid making the client infer UI from raw token outputs.
- **Excessive Latency**: Not using streaming can result in poor user experiences.

For more pitfalls and how to avoid them, see [Common Pitfalls](references/common_pitfalls.md).

### Validation and Testing
1. **Test Rendering Contracts**: Ensure the model outputs structured UI intent and adheres to layout rules.
2. **Simulate Streaming**: Verify that UI components are delivered in chunks and rendered progressively.
3. **Validate BFF Outputs**: Check that the BFF correctly hydrates UI components and attaches actions.

### References


## Reference Guides

### Code Examples

# Code Examples for Generative UI
This document provides concrete code examples for implementing Generative UI layers.

### Rendering Contract Example
```python
contract = {
  "components": ["date_field", "time_field", "submit_button"],
  "layout_rules": {
    "flights": {
      "1-3": "swipable_carousel",
      "4+": "vertical_list"
    }
  }
}
```

### Streaming Example
```python
# Simulate streaming UI components
components = ["skeleton", "partial_fill", "complete"]
for component in components:
    render(component)
```

### BFF Example
```python
# Handle platform-specific rendering
if platform == "Android":
    render_android_ui()
elif platform == "iOS":
    render_ios_ui()
```

### Best Practices
- **Version Awareness**: Ensure the model is aware of client capabilities.
- **Progressive Rendering**: Use streaming to show partial results.
- **Platform-Specific Rules**: Let the BFF handle platform differences.

For more details, see [Practical Guide](references/practical_guide.md).

### Common Pitfalls

# Common Pitfalls in Generative UI Design
This document outlines common pitfalls and how to avoid them when designing Generative UI layers.

### Pitfall 1: Ignoring Client Capabilities
Failing to account for client versions can lead to crashes. Always maintain a version map and ensure the model is aware of client capabilities.

### Pitfall 2: Overloading the Client
Avoid making the client infer UI from raw token outputs. Use structured UI intent and rendering contracts.

### Pitfall 3: Excessive Latency
Not using streaming can result in poor user experiences. Use streaming to deliver UI components in chunks and reduce perceived latency.

### Examples
- **Ignoring Client Capabilities**: A new UI component introduced in version 2.0 crashes older clients.
- **Overloading the Client**: The client tries to infer UI from raw token outputs, leading to incorrect rendering.
- **Excessive Latency**: Users experience long wait times because the UI is not streamed.

### Best Practices
- **Version Awareness**: Maintain a version map and ensure the model is aware of client capabilities.
- **Structured UI Intent**: Use rendering contracts to define UI components and layout rules.
- **Streaming**: Deliver UI components in chunks to reduce perceived latency.

For more details, see [Practical Guide](references/practical_guide.md).

### Core Concepts

# Core Concepts of Generative UI
Generative UI is the layer that transforms AI model outputs into human-friendly interfaces. It ensures that the output is not just accurate but also interactive and scalable. This layer is crucial for delivering a seamless user experience.

### Key Components
1. **Rendering Contracts**: These define the UI components and layout rules that the AI model can output. They ensure that the model outputs structured UI intent rather than raw text.
2. **Streaming**: This technique delivers UI components in chunks, reducing perceived latency and keeping users engaged.
3. **Backend for Frontend (BFF)**: This handles platform-specific rendering rules, hydrates UI components, and attaches actions to elements.

### Importance
Generative UI is essential for creating user-centric AI applications. It bridges the gap between AI capabilities and human interaction, ensuring that the output is not just accurate but also user-friendly.

### Examples
- **Rendering Contracts**: A contract might specify that the model can output components like `date_field`, `time_field`, and `submit_button`.
- **Streaming**: A skeleton UI is shown first, then progressively filled as data arrives.
- **BFF**: The BFF handles platform differences and ensures that UI components are rendered correctly.

For more details, see [Practical Guide](references/practical_guide.md).

### Practical Guide

# Practical Guide to Implementing Generative UI
This guide provides step-by-step instructions for implementing Generative UI layers in AI applications.

### Step 1: Define the Rendering Contract
Establish a contract between the AI model and the client that specifies UI components and layout rules. Ensure the model outputs structured UI intent rather than raw text.

### Step 2: Implement Streaming
Use streaming to deliver UI components in chunks, reducing perceived latency. Start with a skeleton UI, progressively fill it, and complete it as data arrives.

### Step 3: Build the BFF
Create a Backend for Frontend (BFF) that handles platform-specific rendering rules, hydrates UI components, and attaches actions to elements.

### Example Workflow
1. **Define the Contract**: Specify components and layout rules.
2. **Stream UI Components**: Deliver components in chunks.
3. **Render with BFF**: Use the BFF to handle platform-specific rendering.

### Best Practices
- **Version Awareness**: Ensure the model is aware of client capabilities by maintaining a version map.
- **Progressive Rendering**: Use streaming to show partial results and keep users engaged.
- **Platform-Specific Rules**: Let the BFF handle platform differences (e.g., Android vs. iOS).

For more examples, see [Code Examples](references/code_examples.md).

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Agent Output Is Not UX: Rendering Layer Your LLM Pipeline Is Missing - Bala Ramdoss, Amazon Lens](https://www.youtube.com/watch?v=maTp79FD9gI)** by AI Engineer