# Voice Module

End-to-end voice boundary for KOTA clients: speech-to-text (STT) input and
text-to-speech (TTS) output. Every client that wants voice — CLI, web,
native macOS, mobile, Telegram, etc. — reaches it through the daemon's
control API, not through a per-client audio pipeline.

## Contract

- **STT reuses the `transcription` protocol.** The voice service calls
  `transcribeAudio` from `#modules/transcription/service.js`. Any registered
  `TranscriptionProvider` (cloud Whisper, local Whisper, custom) serves
  both Telegram channel voice notes and voice-module clients.
- **TTS introduces a `SpeechSynthesisProvider` protocol** registered under
  the `"speech-synthesis"` provider type. No default ships; absence is a
  typed `SpeechSynthesisProviderUnavailableError`.
- **Preflight validation at the service boundary.** Empty TTS text and
  unsupported output formats fail loudly in `synthesizeSpeech` before the
  request leaves the process.
- **Providers opt in.** `voice-openai-tts` registers a server-side TTS
  provider when an API key is configured. `voice-whisper-local` registers
  an opt-in local STT provider when a binary and model are reachable. A
  missing opt-in provider never breaks module load.
- **Transport-neutral.** Clients hit JSON endpoints with base64-encoded
  audio. No client owns vendor calls, credential handling, or audio
  format negotiation.
- **Realtime voice lifecycle.** Future streaming voice transports (WebRTC,
  telephony, native live microphone sessions, huddles) must route audio,
  partial/final transcripts, assistant audio, interruptions, completion,
  and terminal errors through the module-owned realtime session protocol
  and state machine. Do not create a per-surface audio lifecycle.

## Client surfaces

- **Daemon control API** (`POST /voice/transcribe`, `POST /voice/synthesize`):
  the primary surface. The `voice` `KotaClient` namespace
  (`client.voice.transcribe()` / `client.voice.synthesize()`) routes
  through these routes via the module's `daemonClient(link)` factory, so
  every daemon-aware client calls voice uniformly through the shared
  namespace contract.
- **`kota serve` HTTP** (`POST /api/voice/transcribe`,
  `POST /api/voice/synthesize`): the mirror surface for web / macOS /
  mobile clients that target the HTTP API server rather than daemon-control.
- **CLI** (`kota voice transcribe <file>`, `kota voice speak <text>`):
  routes through `ctx.client.voice.{transcribe,synthesize}`. The local
  handler returns `daemon_required` (providers register in module onLoad,
  which is skipped on the CLI's `"commands"` lifecycle path), so the CLI surfaces a
  single "Daemon is not running" hint when no daemon is reachable. There
  is no local audio stack beyond reading input bytes and spawning a
  platform-detected player for output.
- **Web client** (`clients/web`): microphone capture via `MediaRecorder`
  posts to `/api/voice/transcribe` and TTS replies stream back through
  `/api/voice/synthesize`; no vendor SDK in the browser.
- **Apple clients** (`clients/apple`): `AVAudioRecorder` capture and
  `AVAudioPlayer` playback against the daemon control API's
  `/voice/transcribe` and `/voice/synthesize` routes. Shared between
  the macOS menu-bar shell and the iOS app via the `KotaShared`
  target.
- **Mobile client** (`clients/mobile`): `expo-av` capture and playback
  against the daemon control API's `/voice/transcribe` and
  `/voice/synthesize` routes.

## Failure modes

Every client sees the same shape at the boundary:

- `503` + `code: "stt-unavailable"` — no transcription provider loaded.
- `503` + `code: "tts-unavailable"` — no synthesis provider loaded.
- `400` + `code: "tts-format-unsupported"` + `supported: [...]` —
  requested format is outside the active provider's declared formats.
- `400` — malformed/empty body, empty `text`, invalid format enum value.
- `502` + `code: "stt-failed"` / `"tts-failed"` — upstream provider error.
- `413` — body exceeded the 16MB voice budget.

Mirror this shape exactly in any new client surface.

### Surface-local codes

Clients may extend the `code` field with platform-natural failure codes that
do not exist on the daemon side: e.g., `stt-mic-denied`, `stt-empty-recording`,
`stt-empty-transcript`, `stt-request-failed`, `tts-playback-failed`,
`stt-unsupported` (web only), `daemon-offline` (macOS only). The intersection
of all clients is exactly the daemon vocabulary above; surface-local codes
encode browser/native-runtime conditions the daemon never observes (mic
permission, missing `MediaRecorder`, broken connection state, ...). New
clients should adopt the matching code from this list rather than minting
synonyms; bring a new code only when no existing one fits the platform
condition.

## Injection-defense parity

Transcribed voice becomes a user turn at each client just like typed text
— not tool output. The `injection-defense` middleware screens tool
output, so it does not re-wrap user voice transcripts. This keeps voice
input on the same footing as typed input: the same autonomy-mode rails
and the same content provenance apply to both paths. If a future client
ever feeds raw voice transcripts back into agent context as *tool
output*, screen it at that ingestion point, not retroactively inside the
voice module.

## Extending

- Add a new STT provider: register a `TranscriptionProvider` via the
  `transcription` module's protocol. Voice picks it up automatically.
- Add a new TTS provider: implement `SpeechSynthesisProvider` and register
  it under `SPEECH_SYNTHESIS_PROVIDER_TYPE`. Declare `supportedFormats`
  honestly so preflight validation works.
- Add a new client: call the daemon control API (or `/api/voice/*`) with
  the JSON shape above. Do not reach providers directly.
- Add a realtime voice transport: bind the transport to an existing KOTA
  session id and channel identity, then drive `realtime-session` events
  through the voice state machine before crossing provider or channel
  boundaries.
