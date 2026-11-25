---
name: apple-foundation-models-skill
description: Develop, debug, or review Swift code using Apple's FoundationModels framework (OS 26/27+). Covers LanguageModelSession, SystemLanguageModel, @Generable, @Guide, Tool, streaming, transcripts, prompt attachments, dynamic profiles, session properties, Private Cloud Compute, and custom providers.
---

# Apple Foundation Models Skill

Use this skill as a focused router for the public `FoundationModels` API. Preserve the request's deployment target and distinguish OS 26 APIs from OS 27 additions in code and explanations.

## Workflow

1. Confirm the target OS and toolchain. Keep OS 26 compatibility paths separate from APIs introduced in OS 27.
2. Read [references/_index.md](references/_index.md), then load only the references required by the request. Do not load the entire reference set.
3. Apply the shared requirements below before emitting code. Use the selected references for API signatures, examples, recovery behavior, and edge cases.
4. Produce Swift 6 code. Mark OS 27-only code clearly and use availability guards where a project supports older releases.

## Shared Requirements

- Check `SystemLanguageModel.availability` or `PrivateCloudComputeLanguageModel.availability` before creating a session with that Apple-provided model. A custom `LanguageModel` must expose readiness through its own design.
- Keep `LanguageModelSession` in `@State` or an actor-isolated owner; never create it as a local value in an event handler.
- Wrap every `respond` call and every `ResponseStream` iteration in `do/catch`. On OS 27, distinguish `LanguageModelError`, model-specific errors, `LanguageModelSession.Error`, and `LanguageModelSession.ToolCallError`; use deprecated `LanguageModelSession.GenerationError` only for OS 26 compatibility.
- Recover explicitly from context overflow: on OS 27, trim or replace the mutable transcript and retry, or create a new session; on OS 26, create a new session after `.exceededContextWindowSize`.
- Use `@Generable` only on structs and enums. Match each `@Guide` constraint to the property's type.
- Treat `Tool.call(arguments:)` as `async throws`; propagate failures instead of suppressing them with `try?`.
- Run session work with structured concurrency. Do not block the main actor or use `DispatchQueue.main.async` as a substitute for isolation.
- Call synchronous `prewarm(promptPrefix:)` during idle time, not immediately before generation.
- Use `SystemLanguageModel.contextSize` and `try await PrivateCloudComputeLanguageModel.contextSize` rather than copying a token limit into control flow. Apple's on-device model documentation currently specifies a 4,096-token session context window.

## Boundaries

- For general concurrency or SwiftUI architecture, use the relevant specialist skill; consult this skill only for `FoundationModels`-specific integration constraints.
- Exclude Core ML, Create ML, Vision-only work, model training, Private Cloud Compute internals, non-public endpoints, server deployment, and third-party LLM SDKs.
- Do not infer undocumented API behavior. If an official source does not establish a claim, state: _Technical details pending official release._
