# Voice OpenAI TTS Module

Opt-in text-to-speech provider backed by OpenAI's `/audio/speech`
endpoint (or any OpenAI-compatible host that serves the same shape).

- Requires `modules.voice-openai-tts.apiKey`. Absence leaves the provider
  inactive with a warning — never a silent default.
- Declares supported formats so the voice service can preflight-reject
  unsupported requests before a network round-trip.
- Owns semantic retry on transient upstream failures; the shared outbound HTTP
  boundary owns request timeout and network policy.
  callers see a single success/fail.
