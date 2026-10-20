# Copilot Instructions: Implementing Evals Driven Development For A Mental Health Ai Coach
Description: This skill teaches you how to build and evaluate a mental health AI coach using evals-driven development, focusing on safety, modularity, and clinical grounding.

## Overview

This skill focuses on creating a mental health AI coach that is safe, clinically grounded, and modular. The goal is to provide support to individuals who may not be ready for therapy or need assistance between sessions. The system uses input and output guardrails to ensure user safety and employs evals-driven development to continuously improve the AI's responses.

For a deeper understanding of the core concepts, refer to [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow

1. **Define Input and Output Guardrails**: Establish separate guardrails for user inputs and AI outputs to ensure safety and clinical appropriateness. Use separate language models (LMs) for these guardrails to enhance robustness.

2. **Modular System Design**: Design the system with modularity in mind to allow for iterative improvements without compromising user safety. This includes separate components for guardrails, core AI, and analytics.

3. **Clinical Grounding**: Collaborate with licensed clinicians to define and calibrate the guardrails. Use clinical expertise to interpret nuanced messages and ensure the AI responds appropriately.

4. **Evals-Driven Development**: Implement a learning loop where clinicians annotate conversation traces, turning them into typed evals. Use these evals to score prompt changes, model changes, and guardrail updates.

5. **Continuous Evaluation**: Regularly evaluate the system using annotated scenarios to ensure it meets clinical standards. Focus on reducing false positives and false negatives while maintaining user safety.

For detailed practical steps, see [Practical Guide](references/practical_guide.md).

## Code Snippets and Prompt Templates

```python
# Example of a guardrail prompt template
guardrail_prompt = """
Analyze the following user message for any signs of immediate danger or need for clinical intervention:

User Message: {user_message}

Provide a response indicating whether the message requires immediate intervention or can proceed to the core AI.
"""

# Example of an eval annotation script
def annotate_conversation(trace, rubric):
    # Logic to annotate conversation traces based on clinical rubric
    pass
```

For more code examples, refer to [Code Examples](references/code_examples.md).

## Best Practices and Common Pitfalls

- **Best Practices**:
  - Use separate LMs for guardrails to enhance robustness.
  - Collaborate closely with clinicians to define and calibrate guardrails.
  - Implement a continuous learning loop with evals-driven development.

- **Common Pitfalls**:
  - Over-calibration can lead to false positives, preventing users from receiving necessary support.
  - Ignoring the clinical nuance in user messages can result in inappropriate responses.

For more detailed guidelines, see [Common Pitfalls](references/common_pitfalls.md).

## Validation and Testing Steps

1. **Scenario Testing**: Test the system with synthetic but representative scenarios to ensure guardrails trigger correctly.
2. **Clinical Review**: Have clinicians review and annotate conversation traces to validate AI responses.
3. **Continuous Monitoring**: Use analytics and alerting platforms to monitor system performance and detect any issues.

## References

```json
[
  {
    "filename": "core_concepts.md",
    "content": "## Core Concepts\n\n### Introduction\n\nBuilding a mental health AI coach requires a deep understanding of both AI technology and clinical mental health practices. The primary goal is to provide safe, effective support to individuals who may not be ready for therapy or need assistance between sessions.\n\n### Key Components\n\n1. **Input Guardrails**: These analyze user messages as they come in to determine if any immediate intervention is required before the AI responds.\n\n2. **Output Guardrails**: These evaluate the AI's responses and the overall conversation to ensure clinical safety and appropriateness.\n\n3. **Modularity**: Designing the system with separate, modular components allows for iterative improvements without compromising safety.\n\n4. **Clinical Grounding**: Collaboration with licensed clinicians ensures that the AI's responses are clinically appropriate and safe.\n\n### Importance of Evals-Driven Development\n\nEvals-driven development involves continuously evaluating the AI's performance using annotated conversation traces. This process ensures that the AI remains clinically grounded and safe over time.\n\n### Conclusion\n\nUnderstanding these core concepts is essential for building a mental health AI coach that is both effective and safe. By focusing on modularity, clinical grounding, and continuous evaluation, you can create a system that provides meaningful support to users in need."
  },
  {
    "filename": "practical_guide.md",
    "content": "## Practical Guide\n\n### Step-by-Step Implementation\n\n1. **Define Input and Output Guardrails**: Establish separate guardrails for user inputs and AI outputs. Use separate language models (LMs) for these guardrails to enhance robustness.\n\n2. **Modular System Design**: Design the system with modularity in mind. This includes separate components for guardrails, core AI, and analytics.\n\n3. **Clinical Grounding**: Collaborate with licensed clinicians to define and calibrate the guardrails. Use clinical expertise to interpret nuanced messages and ensure the AI responds appropriately.\n\n4. **Evals-Driven Development**: Implement a learning loop where clinicians annotate conversation traces, turning them into typed evals. Use these evals to score prompt changes, model changes, and guardrail updates.\n\n5. **Continuous Evaluation**: Regularly evaluate the system using annotated scenarios to ensure it meets clinical standards. Focus on reducing false positives and false negatives while maintaining user safety.\n\n### Tools and Resources\n\n- **Annotation Tools**: Use tools that allow clinicians to easily annotate conversation traces.\n\n- **Analytics Platforms**: Implement analytics and alerting platforms to monitor system performance and detect any issues.\n\n### Conclusion\n\nFollowing this practical guide will help you build a mental health AI coach that is safe, clinically grounded, and continuously improving. By focusing on modularity, clinical collaboration, and evals-driven development, you can create a system that provides meaningful support to users in need."
  },
  {
    "filename": "code_examples.md",
    "content": "## Code Examples\n\n### Guardrail Prompt Template\n\n```python\n# Example of a guardrail prompt template\nguardrail_prompt = \"\"\"\nAnalyze the following user message for any signs of immediate danger or need for clinical intervention:\n\nUser Message: {user_message}\n\nProvide a response indicating whether the message requires immediate intervention or can proceed to the core AI.\n\"\"\"\n```\n\n### Eval Annotation Script\n\n```python\n# Example of an eval annotation script\ndef annotate_conversation(trace, rubric):\n    # Logic to annotate conversation traces based on clinical rubric\n    pass\n```\n\n### Conclusion\n\nThese code examples provide a starting point for implementing guardrails and evals-driven development in your mental health AI coach. By using these templates and scripts, you can ensure that your system is clinically grounded and continuously improving."
  },
  {
    "filename": "common_pitfalls.md",
    "content": "## Common Pitfalls\n\n### Over-Calibration\n\nOver-calibration can lead to false positives, preventing users from receiving necessary support. For example, if the system is too sensitive, it may trigger guardrails unnecessarily, making users feel isolated.\n\n### Ignoring Clinical Nuance\n\nIgnoring the clinical nuance in user messages can result in inappropriate responses. For instance, a message like \"I packed a box today\" might seem innocuous but could indicate deeper issues if interpreted correctly.\n\n### Lack of Continuous Evaluation\n\nFailing to continuously evaluate the system can lead to outdated or unsafe responses. Regular evaluation using annotated scenarios ensures that the AI remains clinically grounded and safe.\n\n### Conclusion\n\nAvoiding these common pitfalls is essential for building a mental health AI coach that is both effective and safe. By focusing on appropriate calibration, clinical nuance, and continuous evaluation, you can create a system that provides meaningful support to users in need."
  }
]


## Reference Guides

### Code Examples

## Code Examples

### Guardrail Prompt Template

```python
# Example of a guardrail prompt template
guardrail_prompt = """
Analyze the following user message for any signs of immediate danger or need for clinical intervention:

User Message: {user_message}

Provide a response indicating whether the message requires immediate intervention or can proceed to the core AI.
"""
```

### Eval Annotation Script

```python
# Example of an eval annotation script
def annotate_conversation(trace, rubric):
    # Logic to annotate conversation traces based on clinical rubric
    pass
```

### Conclusion

These code examples provide a starting point for implementing guardrails and evals-driven development in your mental health AI coach. By using these templates and scripts, you can ensure that your system is clinically grounded and continuously improving.

### Common Pitfalls

## Common Pitfalls

### Over-Calibration

Over-calibration can lead to false positives, preventing users from receiving necessary support. For example, if the system is too sensitive, it may trigger guardrails unnecessarily, making users feel isolated.

### Ignoring Clinical Nuance

Ignoring the clinical nuance in user messages can result in inappropriate responses. For instance, a message like "I packed a box today" might seem innocuous but could indicate deeper issues if interpreted correctly.

### Lack of Continuous Evaluation

Failing to continuously evaluate the system can lead to outdated or unsafe responses. Regular evaluation using annotated scenarios ensures that the AI remains clinically grounded and safe.

### Conclusion

Avoiding these common pitfalls is essential for building a mental health AI coach that is both effective and safe. By focusing on appropriate calibration, clinical nuance, and continuous evaluation, you can create a system that provides meaningful support to users in need.

### Core Concepts

## Core Concepts

### Introduction

Building a mental health AI coach requires a deep understanding of both AI technology and clinical mental health practices. The primary goal is to provide safe, effective support to individuals who may not be ready for therapy or need assistance between sessions.

### Key Components

1. **Input Guardrails**: These analyze user messages as they come in to determine if any immediate intervention is required before the AI responds.

2. **Output Guardrails**: These evaluate the AI's responses and the overall conversation to ensure clinical safety and appropriateness.

3. **Modularity**: Designing the system with separate, modular components allows for iterative improvements without compromising safety.

4. **Clinical Grounding**: Collaboration with licensed clinicians ensures that the AI's responses are clinically appropriate and safe.

### Importance of Evals-Driven Development

Evals-driven development involves continuously evaluating the AI's performance using annotated conversation traces. This process ensures that the AI remains clinically grounded and safe over time.

### Conclusion

Understanding these core concepts is essential for building a mental health AI coach that is both effective and safe. By focusing on modularity, clinical grounding, and continuous evaluation, you can create a system that provides meaningful support to users in need.

### Practical Guide

## Practical Guide

### Step-by-Step Implementation

1. **Define Input and Output Guardrails**: Establish separate guardrails for user inputs and AI outputs. Use separate language models (LMs) for these guardrails to enhance robustness.

2. **Modular System Design**: Design the system with modularity in mind. This includes separate components for guardrails, core AI, and analytics.

3. **Clinical Grounding**: Collaborate with licensed clinicians to define and calibrate the guardrails. Use clinical expertise to interpret nuanced messages and ensure the AI responds appropriately.

4. **Evals-Driven Development**: Implement a learning loop where clinicians annotate conversation traces, turning them into typed evals. Use these evals to score prompt changes, model changes, and guardrail updates.

5. **Continuous Evaluation**: Regularly evaluate the system using annotated scenarios to ensure it meets clinical standards. Focus on reducing false positives and false negatives while maintaining user safety.

### Tools and Resources

- **Annotation Tools**: Use tools that allow clinicians to easily annotate conversation traces.

- **Analytics Platforms**: Implement analytics and alerting platforms to monitor system performance and detect any issues.

### Conclusion

Following this practical guide will help you build a mental health AI coach that is safe, clinically grounded, and continuously improving. By focusing on modularity, clinical collaboration, and evals-driven development, you can create a system that provides meaningful support to users in need.

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Evals-Driven Development for a Mental Health AI Coach — Akele Reed & Dave Revere, SonderMind](https://www.youtube.com/watch?v=O72p-rBb2bA)** by AI Engineer