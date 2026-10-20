# Voice Whisper Local Module

Opt-in local speech-to-text provider backed by a whisper.cpp `whisper-cli`
binary. Registers against the existing `transcription` protocol so the
voice module and any other `transcribeAudio` caller can use it
transparently.

- Operators install whisper.cpp and a GGML model themselves. The module
  never downloads binaries or models.
- Missing or unreadable `binaryPath` / `modelPath` leaves the provider
  inactive with a warning. Local STT is never a required dependency.
- Audio is written to a managed temp directory, passed to whisper-cli,
  and the resulting JSON is parsed for transcript + language. Temp files
  are always cleaned up, including on error.
- Per-invocation timeout kills the subprocess; failures surface as
  `WhisperLocalTranscriptionError` with exit code and stderr excerpt.
