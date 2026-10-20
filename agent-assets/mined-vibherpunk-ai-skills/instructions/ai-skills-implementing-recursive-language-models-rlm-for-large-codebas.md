# Copilot Instructions: Implementing Recursive Language Models (Rlm) For Large Codebases
Description: This skill teaches you how to implement Recursive Language Models (RLM) to manage and analyze large codebases effectively. It includes externalizing context management, curating relevant code chunks, and using recursive queries to enhance understanding and reasoning over structured code data.

### Overview
Recursive Language Models (RLM) are designed to handle large codebases by externalizing context management into a programmable execution environment. This approach allows you to curate relevant code chunks and use recursive queries to enhance understanding and reasoning over structured code data. For a deeper dive into the core concepts, refer to [Core Concepts](references/core_concepts.md).

### Step-by-Step Workflow
1. **Set Up the Environment**: Create a separate, dedicated environment for the model to operate on the codebase.
2. **Curate Context**: Write code to inspect, slice, and compute relevant chunks of the codebase.
3. **Feed Context**: Feed the curated context into the main context window of the model.
4. **Recursive Queries**: Use recursive queries to ask another language model or system for additional information if needed.
5. **Terminate Loop**: Continue the loop until a final result is achieved.

### Code Snippets
```python
# Example of curating context
import os

def curate_context(codebase_path):
    relevant_chunks = []
    for root, dirs, files in os.walk(codebase_path):
        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(root, file), 'r') as f:
                    content = f.read()
                    if 'relevant_keyword' in content:
                        relevant_chunks.append(content)
    return relevant_chunks
```

### Best Practices
- **Externalize Context Management**: Always externalize context management to avoid overwhelming the model's main context window.
- **Use Recursive Queries**: Utilize recursive queries to gather additional information when the initial context is insufficient.
- **Monitor Token Usage**: Keep an eye on token usage to manage costs and performance effectively.

### Common Pitfalls
- **Overloading Context**: Avoid overloading the model's context window with irrelevant information.
- **Ignoring Structure**: Do not ignore the structured nature of codebases; leverage directories, imports, and dependencies.

### Validation and Testing
- **Run Test Cases**: Execute test cases to ensure the curated context is relevant and the recursive queries return accurate information.
- **Check Traces**: Review traces in JSONL format to validate the RLM loop and final output.

For practical implementation guidelines, see [Practical Guide](references/practical_guide.md). For more code examples, refer to [Code Examples](references/code_examples.md).

## Reference Guides

### Code Examples

# Code Examples for RLM Implementation

This document provides concrete code examples for implementing Recursive Language Models (RLM) in your workflow.

### Example: Curating Context
```python
import os

def curate_context(codebase_path):
    relevant_chunks = []
    for root, dirs, files in os.walk(codebase_path):
        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(root, file), 'r') as f:
                    content = f.read()
                    if 'relevant_keyword' in content:
                        relevant_chunks.append(content)
    return relevant_chunks
```

### Example: Recursive Query
```python
def recursive_query(query, model):
    response = model.query(query)
    if response.is_incomplete:
        return recursive_query(response.next_query, model)
    return response
```

### Example: Feeding Context
```python
def feed_context(model, context):
    model.feed_context(context)
    return model.get_response()
```

These examples illustrate how to curate context, perform recursive queries, and feed context into the model. For a deeper understanding of the core concepts, refer to [Core Concepts](references/core_concepts.md).

### Core Concepts

# Core Concepts of Recursive Language Models (RLM)

Recursive Language Models (RLM) are designed to handle large codebases by externalizing context management into a programmable execution environment. This approach allows the model to operate on the entire repository as data, curating relevant chunks and feeding them into the main context window. The core thesis of RLM is to avoid overloading the model's context by creating a separate environment where the model can write code to inspect, slice, and compute relevant chunks.

### Key Components
- **Externalized Context Management**: A dedicated environment for the model to operate on the codebase.
- **Curated Context**: Relevant chunks of code identified and fed into the main context window.
- **Recursive Queries**: Additional queries to other language models or systems to gather more information.

### Benefits
- **Improved Performance**: By externalizing context management, the model's performance does not degrade with larger codebases.
- **Enhanced Understanding**: Curated context and recursive queries enhance the model's understanding and reasoning over structured code data.

For practical implementation guidelines, refer to [Practical Guide](references/practical_guide.md).

### Practical Guide

# Practical Guide to Implementing RLM

Implementing Recursive Language Models (RLM) involves setting up a dedicated environment, curating relevant code chunks, and using recursive queries to enhance understanding. This guide provides step-by-step instructions for practical implementation.

### Step-by-Step Instructions
1. **Set Up the Environment**: Create a separate, dedicated environment for the model to operate on the codebase.
2. **Curate Context**: Write code to inspect, slice, and compute relevant chunks of the codebase.
3. **Feed Context**: Feed the curated context into the main context window of the model.
4. **Recursive Queries**: Use recursive queries to ask another language model or system for additional information if needed.
5. **Terminate Loop**: Continue the loop until a final result is achieved.

### Best Practices
- **Externalize Context Management**: Always externalize context management to avoid overwhelming the model's main context window.
- **Use Recursive Queries**: Utilize recursive queries to gather additional information when the initial context is insufficient.
- **Monitor Token Usage**: Keep an eye on token usage to manage costs and performance effectively.

### Common Pitfalls
- **Overloading Context**: Avoid overloading the model's context window with irrelevant information.
- **Ignoring Structure**: Do not ignore the structured nature of codebases; leverage directories, imports, and dependencies.

For more code examples, refer to [Code Examples](references/code_examples.md).

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[RLM: Recursive Language Models for Large Codebases - Shashi, Superagentic AI](https://www.youtube.com/watch?v=8oyalrfwgjw)** by AI Engineer