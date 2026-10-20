# Services/

Transcription and translation backends. All services take the API Key via constructor injection (decoupled from storage). **Language and timeout are internal concerns**: language flows in as a per-call parameter (resolved by the Manager), timeout is computed and enforced inside each service.

| File | Description |
|------|-------------|
| **LocalTranslator.swift** | `protocol LocalTranslator` (single async throws `translate` method) + `enum LocalTranslatorFactory` with `@MainActor static func make() -> LocalTranslator?`. The factory encapsulates the `if #available(macOS 15.0, *)` gate so storage / call sites can hold a plain `LocalTranslator?` without availability annotations or `#if canImport(Translation)` clutter. Adding a second on-device translation backend is a one-line change in the factory |
| **CloudOpenAIService.swift** | OpenAI Whisper HTTP client. `@MainActor final class ... ObservableObject` mirroring `LocalWhisperService`'s shape, with `@Published private(set) var health: Health` (`.healthy` by default, transitions to `.unavailable(reason: UnavailabilityReason, since: Date)` when `executeRequest` catches a transient error). `transcribe(samples:audioDuration:language:) async throws -> String` encodes audio internally (AudioEncoder M4A/WAV) and uploads to `/v1/audio/transcriptions` (gpt-4o-transcribe), using a private `transcribeTimeout(audioDuration:)` formula `clamp(minutes × transcribeTimeoutPerMinute, [transcribeTimeoutMin, transcribeTimeoutMax])`. `chatTranslate(text:targetLanguage:) async throws -> String` hits Chat Completions with fixed `chatTranslateTimeout` (30s). Shared private `executeRequest` helper: fresh `URLSession` per call, unified error mapping to `WhisperError`, and on failure consults the nested **`EngineErrorClassifier`** static enum (`classify(_: Error) -> Outcome` returning `.markUnavailable(UnavailabilityReason)` or `.ignore`) to decide whether to flip `health → .unavailable`. `markRecovered()` flips it back. Language is a per-call parameter — empty string = auto-detect, non-empty normalized via `LocaleManager.whisperCode(for:)`; no `"ui"` branch here (Manager resolves it) |
| **LocalAppleTranslationService.swift** | Apple Translation Framework local translation (macOS 15.0+). `translate(text:sourceLanguage:targetLanguage:) async throws -> String`. On-device translation via SwiftUI `.translationTask` bridge (hidden NSWindow host); internally wraps the callback bridge in `withCheckedThrowingContinuation`. Auto-detects source language via `NLTagger` and pre-checks language pack availability (fast-fail on missing/unsupported). 60s hard timeout internal. `#if canImport(Translation)` conditional compilation |
| **LocalWhisperService.swift** | WhisperKit local transcription. `transcribe(samples:language:audioDuration:) async throws -> String`. Model `openai_whisper-large-v3-v20240930_626MB` (auto-download on first use). Temperature fallback (0.0 → +0.2 × 5), hallucination detection (compression ratio 2.4), VAD chunking. **No internal timeout** — Swift cooperative cancellation can't actually preempt WhisperKit's blocking CoreML/ANE call, and a races-based timer would spuriously discard correct results near the threshold. User-driven ESC (cancel via AppController's `currentPipelineTask`) and `state = .failed(.runtime)` on real WhisperKit exceptions cover both axes. Returns raw joined text — post-processing (tag filtering, trim, Chinese script conversion) is now TranscriptionManager's job via `TextPostProcessor` |

## Rules — Language Codes & Silent Fallbacks

Two bugs shipped from this pattern: `""` silently became `"en"`; `nil` silently became `"zh-Hans"`. Don't repeat it.

- **No hardcoded language/locale/model fallback.** Banned: `?? "en"`, `?? "zh"`, `Locale.Language(identifier: someVar ?? "zh-Hans")`.
- **"Auto" propagates as `nil` or `""` to the detection boundary.** Audio → omit `language` param. Text translation → run `NLLanguageRecognizer` first, then pass the detected `Locale.Language`.
- **No default parameter values for language, model, or API identifiers.** `func f(lang: String = "en")` is banned. Force the caller to decide.
- **Normalization ≠ fallback.** `"zh" → "zh-Hans"` (UI code → BCP-47) is deterministic mapping, allowed. `"" → "en"` is invention, forbidden.
- **Fail fast on unknowns.** If a required identifier is missing, log and return an error. Don't substitute a guess to keep the code path alive.
- **No dead code.** Unused methods attract copy-paste reuse of their bad patterns.
- **Hardcoded strings → named constants** in `Config/EngineeringOptions.swift`. Inline literals inside `??` are forbidden.

Before committing, grep your diff for `?? "[a-z]`, `Locale.Language(identifier: "`, `= "en"`, `= "zh"` — justify each hit or remove it.

## Known Limitation — Cloud health is service-level

`CloudOpenAIService.health` is a single `@Published` field shared between transcription (`/v1/audio/transcriptions`) and translation (`/v1/chat/completions`) usages. A failure on only one OpenAI endpoint (e.g. transcription returning 5xx while chat is fine) will be over-reported as affecting both rows in the Settings panel — both will show the same `recentApiError` reason. Accepted for now in exchange for a single observable surface and one network monitor instance. Future split into `CloudHTTPClient` + 2 endpoint-specific wrappers (each with its own `health`) if real-world frequency of single-endpoint failures warrants the composition cost.
