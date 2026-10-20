# Transcription Module

This module owns the audio → text boundary for KOTA channels that accept
voice input.

- Exposes the `TranscriptionProvider` protocol and routes calls through
  the core provider registry under the `"transcription"` service type.
- Does not ship a default provider. Absence of a configured provider is
  an explicit, typed error (`TranscriptionProviderUnavailableError`) so
  channels can surface a clear failure to the user.
- Channels that receive voice/audio must go through `transcribeAudio`;
  they must not call a transcription vendor API directly.
