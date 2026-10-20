---
name: devel-jb-gemini-live-api-dev
description: "The Live API supports 70 languages including: English, Spanish, French, German, Italian, Portuguese, Chinese, Japanese, Korean, Hindi, Arabic, Russian, and many more."
domain: cybersecurity
---

## Limitations

- **Response modality** — Only `TEXT` **or** `AUDIO` per session, not both
- **Audio-only session** — 15 min without compression
- **Audio+video session** — 2 min without compression
- **Connection lifetime** — ~10 min (use session resumption)
- **Context window** — 128k tokens (native audio) / 32k tokens (standard)
- **Code execution** — Not supported
- **URL context** — Not supported

## Best Practices

1. **Use headphones** when testing mic audio to prevent echo/self-interruption
2. **Enable context window compression** for sessions longer than 15 minutes
3. **Implement session resumption** to handle connection resets gracefully
4. **Use ephemeral tokens** for client-side deployments — never expose API keys in browsers
5. **Use `send_realtime_input`** for all real-time user input (audio, video, text). Reserve `send_client_content` only for injecting conversation history
6. **Send `audioStreamEnd`** when the mic is paused to flush cached audio
7. **Clear audio playback queues** on interruption signals

## How to use the Gemini API

For detailed API documentation, fetch from the official docs index:

**llms.txt URL**: `https://ai.google.dev/gemini-api/docs/llms.txt`

This index contains links to all documentation pages in `.md.txt` format. Use web fetch tools to:

1. Fetch `llms.txt` to discover available documentation pages
2. Fetch specific pages (e.g., `https://ai.google.dev/gemini-api/docs/live-session.md.txt`)

### Key Documentation Pages 

> [!IMPORTANT]
> Those are not all the documentation pages. Use the `llms.txt` index to discover available documentation pages

- [Live API Overview](https://ai.google.dev/gemini-api/docs/live.md.txt) — getting started, raw WebSocket usage
- [Live API Capabilities Guide](https://ai.google.dev/gemini-api/docs/live-guide.md.txt) — voice config, transcription config, native audio (affective dialog, proactive audio, thinking), VAD configuration, media resolution
- [Live API Tool Use](https://ai.google.dev/gemini-api/docs/live-tools.md.txt) — function calling (sync and async), Google Search grounding
- [Session Management](https://ai.google.dev/gemini-api/docs/live-session.md.txt) — context window compression, session resumption, GoAway signals
- [Ephemeral Tokens](https://ai.google.dev/gemini-api/docs/ephemeral-tokens.md.txt) — secure client-side authentication for browser/mobile
- [WebSockets API Reference](https://ai.google.dev/api/live.md.txt) — raw WebSocket protocol details

## Supported Languages

The Live API supports 70 languages including: English, Spanish, French, German, Italian, Portuguese, Chinese, Japanese, Korean, Hindi, Arabic, Russian, and many more. Native audio models automatically detect and switch languages.
