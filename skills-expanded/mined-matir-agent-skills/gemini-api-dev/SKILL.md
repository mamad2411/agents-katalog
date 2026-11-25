---
name: gemini-api-dev
description: Development reference for Gemini models. Provides specifications for multimodal tasks, function calling, and structured outputs.
metadata:
  version: 0.2.0
  category: AI Development
---
# Gemini API Development

## Quick Start
### Python
```python
from google import genai
client = genai.Client()
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Explain quantum computing"
)
print(response.text)
```

## Workflow
1. **Model Selection**: Use `gemini-3.1-pro-preview` for reasoning or `gemini-3-flash-preview` for speed.
2. **SDK Setup**: Install `google-genai` (Python) or `@google/genai` (JS).
3. **Implementation**: Use `generate_content` for text/multimodal or `generateContent` for JS.
4. **Documentation**: Use `search_documentation` (MCP) or fetch `llms.txt` from `ai.google.dev`.

## Rules & Constraints
- **RULE-1**: Use ONLY current models (3.x/2.5). Legacy models (2.0/1.5) are deprecated.
- **RULE-2**: Use ONLY current SDKs (`google-genai`, `@google/genai`). Legacy SDKs are deprecated.
- **RULE-3**: Prioritize `search_documentation` (MCP) over manual URL fetching for ground truth.

## When to Use
- Building applications with Gemini models.
- Implementing function calling, structured outputs, or multimodal features.

## When NOT to Use
- Real-time bidirectional streaming (Use `gemini-live-api-dev` skill).
- Vertex AI-specific implementations (unless using the GenAI SDK).

## References
- [Skill Manual](references/gemini-api-dev-manual.md)
- [Official Docs (llms.txt)](https://ai.google.dev/gemini-api/docs/llms.txt)
