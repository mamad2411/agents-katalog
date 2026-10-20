# Copilot Instructions: Effective Context Engineering For Ai Agents
Description: Learn how to leverage grounding, retrieval-augmented generation (RAG), and context engineering to improve AI accuracy and reliability by providing the right context instead of focusing solely on prompt perfection.

## Overview
Effective AI interactions rely on providing the right context rather than obsessing over perfect prompts. This skill teaches you how to use grounding, retrieval-augmented generation (RAG), and context engineering to ensure AI outputs are accurate and reliable. For foundational concepts, see [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow
1. **Understand Grounding**: Ensure the AI has access to relevant documents or data to base its responses on. This reduces reliance on memory and improves accuracy.
2. **Implement RAG**: Use retrieval-augmented generation to pull relevant information from external sources before generating responses. See [Practical Guide](references/practical_guide.md) for implementation details.
3. **Assemble Context**: Provide background information, examples, and constraints to guide the AI's output. Focus less on perfecting the prompt wording.
4. **Validate Outputs**: Test the AI's responses against the provided context to ensure accuracy and relevance. Use the validation steps in [Common Pitfalls](references/common_pitfalls.md) to avoid errors.

## Code Snippets and Prompt Templates
```python
# Example of grounding in Python
response = ai_model.generate(
    prompt="Summarize this document",
    context=document_text
)

# Example of RAG implementation
relevant_data = retrieve_from_database(query)
response = ai_model.generate(
    prompt="Write an essay on this topic",
    context=relevant_data
)
```
For more examples, see [Code Examples](references/code_examples.md).

## Best Practices
- Always provide context when accuracy matters.
- Use RAG for tasks requiring external knowledge.
- Focus on assembling comprehensive context rather than perfecting prompts.

## Common Pitfalls
- Relying solely on memory-based responses without grounding.
- Over-optimizing prompt wording instead of providing context.
- Failing to validate outputs against the provided context.

## Validation Steps
1. Compare AI responses to the provided context.
2. Check for citations or references in the output to confirm RAG usage.
3. Test with varying levels of context to ensure robustness.

For detailed validation techniques, refer to [Common Pitfalls](references/common_pitfalls.md).

## Reference Guides

### Code Examples

# Code Examples

## Grounding Example
```python
# Example of grounding
response = ai_model.generate(
    prompt="Summarize this document",
    context=document_text
)
```

## RAG Example
```python
# Example of RAG
relevant_data = retrieve_from_database(query)
response = ai_model.generate(
    prompt="Write an essay on this topic",
    context=relevant_data
)
```

## Context Engineering Example
```python
# Example of context engineering
response = ai_model.generate(
    prompt="Generate a report",
    context={
        "background": "The company's Q2 financials",
        "examples": ["Q1 report", "Q2 summary"],
        "constraints": "Include only positive trends"
    }
)
```

These examples demonstrate how to implement grounding, RAG, and context engineering in practice. For more detailed guidance, see [Practical Guide](references/practical_guide.md).

### Common Pitfalls

# Common Pitfalls

## Relying on Memory-Based Responses
One common mistake is relying solely on the AI's memory without providing grounding. This can lead to inaccurate or unreliable responses. Always provide specific data or documents for the AI to reference.

## Over-Optimizing Prompt Wording
Another pitfall is spending too much time perfecting the prompt wording instead of assembling comprehensive context. Focus on providing complete background information, examples, and constraints.

## Failing to Validate Outputs
Always validate AI outputs against the provided context. Check for citations or references to confirm RAG usage and ensure the response aligns with the given context.

## Validation Steps
1. Compare AI responses to the provided context.
2. Check for citations or references in the output to confirm RAG usage.
3. Test with varying levels of context to ensure robustness.

For practical examples, see [Code Examples](references/code_examples.md).

### Core Concepts

# Core Concepts

## Grounding
Grounding ensures AI responses are based on specific, reliable data rather than general knowledge or memory. This is crucial for tasks requiring high accuracy. For example, asking an AI to summarize a document is more reliable if the document is provided as context.

## Retrieval-Augmented Generation (RAG)
RAG combines retrieval of external information with generative AI. Instead of generating responses from memory, the AI first retrieves relevant data from a database or document and then uses this data to generate a response. This approach is particularly useful for tasks like essay writing or answering complex questions.

## Context Engineering
Context engineering focuses on providing the AI with all necessary background information, examples, and constraints. Unlike prompt engineering, which emphasizes the wording of the prompt, context engineering prioritizes the completeness and relevance of the provided context. This approach leads to more accurate and reliable AI outputs.

For practical applications, see [Practical Guide](references/practical_guide.md).

### Practical Guide

# Practical Guide

## Implementing Grounding
To implement grounding, always provide the AI with the specific data or documents it needs to reference. For example, when asking for a summary, include the full text of the document in the prompt.

```python
# Example of grounding
response = ai_model.generate(
    prompt="Summarize this document",
    context=document_text
)
```

## Using RAG
To use RAG, first retrieve relevant information from a database or external source. Then, provide this information as context to the AI.

```python
# Example of RAG
relevant_data = retrieve_from_database(query)
response = ai_model.generate(
    prompt="Write an essay on this topic",
    context=relevant_data
)
```

## Context Engineering
Assemble comprehensive context by including background information, examples, and constraints. Focus less on perfecting the prompt wording and more on providing complete context.

```python
# Example of context engineering
response = ai_model.generate(
    prompt="Generate a report",
    context={
        "background": "The company's Q2 financials",
        "examples": ["Q1 report", "Q2 summary"],
        "constraints": "Include only positive trends"
    }
)
```

For code examples, see [Code Examples](references/code_examples.md).

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Stop perfecting your prompt. Do this instead](https://www.youtube.com/watch?v=jxHIw_OA8_I)** by Jeff Su