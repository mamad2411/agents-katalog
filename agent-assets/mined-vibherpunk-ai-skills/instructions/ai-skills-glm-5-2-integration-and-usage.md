# Copilot Instructions: Glm_5.2_Integration_And_Usage
Description: Learn how to integrate and effectively use GLM 5.2, an open-source local AI model, with tools like Cursor, OpenRouter, and Codex for cost-efficient and high-performance AI workflows.

## Overview
GLM 5.2 is an open-source local AI model that offers a cost-efficient alternative to closed models like OpenAI's GPT. It can be integrated with tools such as Cursor, OpenRouter, and Codex to optimize token usage and enhance productivity. This skill will guide you through setting up GLM 5.2, using it for specific tasks, and leveraging model chaining for optimal results.

## Step-by-Step Workflow
1. **Obtain API Key**: Visit Z AI, the provider of GLM 5.2, and obtain an API key.
2. **Setup in Cursor**:
   - Open Cursor settings.
   - Paste the GLM API key into the OpenAI field.
   - Override the OpenAI endpoint with the GLM endpoint.
   - Add GLM 5.2 as a custom model.
3. **Setup in OpenRouter**:
   - Obtain an OpenRouter API key.
   - Configure OpenRouter to use GLM 5.2.
4. **Model Chaining**: Use Opus 4.8 for tasks requiring vision capabilities and GLM 5.2 for execution-based tasks.
5. **Run Tasks**: Execute tasks using GLM 5.2 through Cursor or OpenRouter.

## Code Snippets
```python
# Example of setting up GLM 5.2 in Cursor
import cursor

cursor.set_api_key('your_glm_api_key')
cursor.set_endpoint('https://api.zai.com/glm5.2')
cursor.add_model('GLM 5.2', 'glm5.2')
```

## Best Practices
- **Cost Efficiency**: Use GLM 5.2 for tasks where token cost is a concern.
- **Model Chaining**: Combine GLM 5.2 with other models for tasks requiring different capabilities.
- **Local Execution**: Run GLM 5.2 locally to save on cloud token costs.

## Common Pitfalls
- **Resource Intensive**: Ensure your machine has sufficient GPU RAM to run GLM 5.2 locally.
- **Benchmark Misinterpretation**: Focus on practical performance rather than benchmark scores.

## Validation and Testing
- **Task Execution**: Run a series of tasks using GLM 5.2 and compare the results with other models.
- **Cost Analysis**: Compare the token cost of using GLM 5.2 versus other models.

For more detailed information, refer to [Core Concepts](references/core_concepts.md), [Practical Guide](references/practical_guide.md), and [Code Examples](references/code_examples.md).

## Reference Guides

### Code Examples

## Code Examples
This document provides concrete code snippets and prompt templates for integrating and using GLM 5.2 with tools like Cursor, OpenRouter, and Codex.

### Code Snippets
```python
# Example of setting up GLM 5.2 in Cursor
import cursor

cursor.set_api_key('your_glm_api_key')
cursor.set_endpoint('https://api.zai.com/glm5.2')
cursor.add_model('GLM 5.2', 'glm5.2')
```

### Prompt Templates
```python
# Example prompt for model chaining
prompt = "Use Opus 4.8 to analyze the image and describe it. Then, use GLM 5.2 to execute the task based on the description."
```

### Best Practices
- **Cost Efficiency**: Use GLM 5.2 for tasks where token cost is a concern.
- **Model Chaining**: Combine GLM 5.2 with other models for tasks requiring different capabilities.
- **Local Execution**: Run GLM 5.2 locally to save on cloud token costs.

### Common Pitfalls
- **Resource Intensive**: Ensure your machine has sufficient GPU RAM to run GLM 5.2 locally.
- **Benchmark Misinterpretation**: Focus on practical performance rather than benchmark scores.

For more detailed information, refer to [Core Concepts](references/core_concepts.md) and [Practical Guide](references/practical_guide.md).

### Core Concepts

## Core Concepts
GLM 5.2 is an open-source local AI model that offers a cost-efficient alternative to closed models like OpenAI's GPT. It can be integrated with tools such as Cursor, OpenRouter, and Codex to optimize token usage and enhance productivity. This document covers the fundamental concepts of GLM 5.2, including its architecture, benefits, and use cases.

### Architecture
GLM 5.2 is built on a transformer-based architecture, similar to other state-of-the-art models. It supports a 1 million context window, making it suitable for long-sequence tasks.

### Benefits
- **Cost Efficiency**: GLM 5.2 is significantly cheaper in terms of token cost compared to closed models.
- **Local Execution**: It can be run locally, saving on cloud token costs.
- **Open Source**: Being open-source, it offers flexibility and customization options.

### Use Cases
- **Long-Sequence Tasks**: Ideal for projects requiring long-sequence task execution.
- **Cost-Sensitive Applications**: Suitable for startups and businesses looking to optimize AI costs.

For practical implementation, refer to [Practical Guide](references/practical_guide.md) and [Code Examples](references/code_examples.md).

### Practical Guide

## Practical Guide
This guide provides step-by-step instructions on how to integrate and use GLM 5.2 with tools like Cursor, OpenRouter, and Codex.

### Step-by-Step Instructions
1. **Obtain API Key**: Visit Z AI, the provider of GLM 5.2, and obtain an API key.
2. **Setup in Cursor**:
   - Open Cursor settings.
   - Paste the GLM API key into the OpenAI field.
   - Override the OpenAI endpoint with the GLM endpoint.
   - Add GLM 5.2 as a custom model.
3. **Setup in OpenRouter**:
   - Obtain an OpenRouter API key.
   - Configure OpenRouter to use GLM 5.2.
4. **Model Chaining**: Use Opus 4.8 for tasks requiring vision capabilities and GLM 5.2 for execution-based tasks.
5. **Run Tasks**: Execute tasks using GLM 5.2 through Cursor or OpenRouter.

### Best Practices
- **Cost Efficiency**: Use GLM 5.2 for tasks where token cost is a concern.
- **Model Chaining**: Combine GLM 5.2 with other models for tasks requiring different capabilities.
- **Local Execution**: Run GLM 5.2 locally to save on cloud token costs.

### Common Pitfalls
- **Resource Intensive**: Ensure your machine has sufficient GPU RAM to run GLM 5.2 locally.
- **Benchmark Misinterpretation**: Focus on practical performance rather than benchmark scores.

For more detailed information, refer to [Core Concepts](references/core_concepts.md) and [Code Examples](references/code_examples.md).

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[GLM 5.2: What you need to know](https://www.youtube.com/watch?v=xa-9O5cDm3c)** by Greg Isenberg