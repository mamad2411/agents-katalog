# AGENTS.md

## Scope
AI assistant integration for iOS. Applies to `RefWatchiOS/Core/Platform/AI/`.

## Conventions
- All network/API access is adapter-based (`AssistantService`, `OpenAIAssistantService`) behind protocols for easy testing. The concrete assistant transport should talk to the server proxy rather than OpenAI directly.
- Do not commit secrets. Keep OpenAI credentials out of the app bundle and route them through the backend assistant proxy; use `.xcconfig` only for non-OpenAI local configuration that this module still needs.
- Provide a safe no-op or stub implementation when credentials are absent to keep the app running.

## Testing
- Use stubbed services with deterministic responses. Avoid live network calls in tests.
- Support timeouts and cancellation; surface errors explicitly to callers.
