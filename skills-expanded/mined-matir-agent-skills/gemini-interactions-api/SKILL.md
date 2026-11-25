---
name: gemini-interactions-api
description: Unified agent interface for executing Gemini model interactions, managing conversation state, and orchestrating tool calls.
metadata:
  version: 0.2.0
  category: gemini
---
# Gemini Interactions API

## Quick Start
```python
from google import genai
client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3-flash-preview",
    input="Explain quantum entanglement."
)
print(interaction.outputs[-1].text)
```

## Workflow
1. **Model Selection**: Choose a current model (e.g., `gemini-3-flash-preview`) or agent.
2. **Interaction**: Call `interactions.create` with input text, images, or tool definitions.
3. **State Management**: Use `previous_interaction_id` to continue existing conversations.
4. **Backgrounding**: Set `background=True` for long-running agentic tasks like Deep Research.
5. **Streaming**: Set `stream=True` and iterate over SSE chunks for real-time responses.
6. **Tooling**: Orchestrate tools like Google Search, Code Execution, and Function Calling.

## Rules & Constraints
- **RULE-1**: Use ONLY current models (`gemini-3.*`, `gemini-2.5-*`) and agents (`deep-research-*`).
- **RULE-2**: Use SDKs `google-genai` (Python) or `@google/genai` (JS). Legacy SDKs are deprecated.
- **RULE-3**: `tools` and `system_instruction` are interaction-scoped; re-specify each turn.
- **RULE-4**: Background execution requires `store=true` (default).
- **RULE-5**: Thinking/Reasoning depth is configurable; check `thought` output blocks.

## When to Use
- Building agentic applications with server-side state.
- Performing complex research using the Deep Research agent.
- Orchestrating multiple tools (Google Search, Code Execution, MCP).

## When NOT to Use
- Simple, stateless text generation where `generateContent` is sufficient (Interactions is preferred for all new apps).
- Real-time audio/video streaming (use Gemini Live API).

## References
- [Skill Manual](references/gemini-interactions-api-manual.md)
- [Gemini API Docs](https://ai.google.dev/gemini-api/docs/)
