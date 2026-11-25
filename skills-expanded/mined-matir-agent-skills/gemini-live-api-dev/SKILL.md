---
name: gemini-live-api-dev
description: Guide for building real-time streaming applications with the Gemini Live API. Covers WebSocket streaming, audio/video features, and session management (Python, JS).
metadata:
  version: 0.2.0
  category: ai-development
---
# Gemini Live API Development

## Quick Start
```python
from google import genai
from google.genai import types

client = genai.Client(api_key="YOUR_API_KEY")
config = types.LiveConnectConfig(response_modalities=[types.Modality.AUDIO])

async with client.aio.live.connect(model="gemini-3.1-flash-live-preview", config=config) as session:
    await session.send_realtime_input(text="Hello, how are you?")
    async for response in session.receive():
        # Process audio/text parts in response.server_content
        pass
```

## Workflow
1. **Initialize Client**: Set up the `genai.Client` with your API key or ephemeral token.
2. **Configure Session**: Define `LiveConnectConfig` with desired modalities (TEXT/AUDIO) and system instructions.
3. **Establish Connection**: Connect to the `gemini-3.1-flash-live-preview` model via WebSockets.
4. **Send Input**: Use `send_realtime_input` to stream audio, video frames, or text.
5. **Handle Output**: Process server events, handling audio chunks, transcriptions, and interruptions.
6. **Manage Session**: Implement session resumption and context compression for long-running interactions.

## Rules & Constraints
- **RULE-1**: Only one response modality (`TEXT` or `AUDIO`) is supported per session.
- **RULE-2**: Use `send_realtime_input` for all live input; `send_client_content` is only for initial history.
- **RULE-3**: Always process ALL parts in a server event to avoid missing content.
- **RULE-4**: Use headphones during development to prevent audio feedback and self-interruption.

## When to Use
- Building low-latency voice assistants or real-time video interaction apps.
- Implementing applications requiring real-time multimodal reasoning.

## When NOT to Use
- High-latency batch processing tasks.
- Applications requiring response modalities other than TEXT or AUDIO (e.g., image generation).

## References
- [Skill Manual](references/gemini-live-api-dev-manual.md)
- [Official Documentation](https://ai.google.dev/gemini-api/docs/live)
