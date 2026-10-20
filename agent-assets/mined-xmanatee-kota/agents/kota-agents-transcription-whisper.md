# Whisper Transcription Module

OpenAI Whisper (or any OpenAI-compatible `/audio/transcriptions` endpoint)
registered as the active `TranscriptionProvider`.

- Opt-in only. Operators install the module and provide credentials under
  `modules.transcription-whisper`; nothing registers a default provider.
- Always routes through the `transcription` module's `TranscriptionProvider`
  protocol — channels never see this module directly.
- Owns semantic retry behaviour while the shared outbound HTTP boundary owns
  request timeout and network policy. Channels see a single
  success/fail from `transcribe`.

## Configuration

Under `modules.transcription-whisper`:

- `apiKey` (required) — literal bearer token, or `$ENV_VAR` reference
  resolved from `process.env` at module load time.
- `baseUrl` — defaults to `https://api.openai.com/v1`. Override to point
  at any OpenAI-compatible endpoint.
- `model` — defaults to `whisper-1`.
- `timeoutMs` — per-request abort deadline. Default 60000.
- `maxRetries` — retry attempts on transient upstream failure (HTTP 408,
  429, 5xx, network errors). Default 2.

## Failure Modes

- Missing or empty `apiKey` (either absent config or a `$ENV` reference
  that resolves empty) leaves the provider unregistered. The
  `transcription` service then throws `TranscriptionProviderUnavailableError`,
  which channels surface to the user as a clear "voice transcription
  isn't configured" message rather than silently dropping audio.
- Non-transient upstream errors (auth failure, malformed request) raise
  `WhisperTranscriptionError` with the HTTP status attached; channels
  render it as a transcription-failed message.
- Transient upstream errors are retried with exponential backoff up to
  `maxRetries` before the same error surfaces.
