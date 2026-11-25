---
name: ios-on-device-intelligence-evaluation
description: Design, implement, evaluate, or review iOS on-device intelligence features using Foundation Models, Vision, Core ML, Speech, Translation, Natural Language, Sound Analysis, and App Intents. Use when a feature generates, extracts, classifies, transcribes, translates, analyzes, or safely acts on user content with Apple intelligence frameworks.
allowed-tools: Read, Grep, Glob
---

# iOS On-Device Intelligence Evaluation

## Overview

Use this skill to choose the narrowest intelligence route and keep availability, privacy, model output, deterministic validation, review, fallback, evaluation, and physical-device evidence explicit.

`authorized source -> bounded input -> available model/asset -> cancellable proposal -> validation/provenance -> review/authorization -> durable result or side effect`

## Read before acting

- Inspect the actual Xcode targets, deployment target, device family, model resources, language assets, entitlements, usage descriptions, persistence, network/server routes, and current AI adapter.
- Read the [AI route selector](../ios-knowledge-base/references/30-on-device-ai/00-ai-route-selector.md), [Foundation Models mental model](../ios-knowledge-base/references/30-on-device-ai/01-foundation-models-mental-model.md), [privacy/availability/fallback guidance](../ios-knowledge-base/references/30-on-device-ai/06-privacy-availability-and-fallback.md), [availability/proof matrix](../ios-knowledge-base/references/30-on-device-ai/08-on-device-ai-availability-and-proof-matrix.md), and [evaluation/safety/fallback recipe](../ios-knowledge-base/references/31-on-device-ai-recipes/05-evaluation-safety-and-fallback.md).
- Read the [on-device AI feature package](../on-device-ai-feature/SKILL.md) and the narrower [media/ML/input package](../ios-media-ml-and-inputs/SKILL.md) when capture, Vision, Core ML, audio, or NFC state is part of the route.
- Refresh the exact official Apple pages in the Sources section before relying on model availability, device/region/language behavior, API spelling, output safety, tool calling, context limits, or privacy claims.

## Route workflow

1. State the user outcome and decide whether a model is necessary. Use deterministic code for calculations, parsing, validation, routing, permissions, sorting, and safety rules; use a model only when ambiguity or learned perception/language is the value.
2. Choose the narrowest route: Foundation Models for bounded language generation/extraction; Vision for system observations; Core ML for a packaged custom model; Speech for the exact transcription route; Translation for supported language pairs; Natural Language for deterministic text analysis; Sound Analysis for bounded audio classification; App Intents for system-discoverable actions.
3. Record the route matrix: target SDK, OS/device eligibility, Apple Intelligence/model state, model/resource version, locale/language asset, permission, input sensitivity/retention, server or Private Cloud Compute boundary, expected uncertainty, and manual/deterministic fallback.
4. Model availability as state, not a Boolean: available, not eligible, disabled, model/asset not ready, unsupported language, permission denied, context exceeded, guardrail refusal, cancelled, input failure, service error, and retry/manual route.
5. Keep trusted instructions separate from user or external content. Bound input size, duration, image/audio dimensions, context, tool arguments, and concurrency. Version prompts, schemas, model revisions, preprocessing, and evaluation fixtures.
6. Prefer typed/guided output for structured proposals. Validate every field, enum, range, identifier, source reference, confidence/quality value, and authorization before it can affect domain state, export, messaging, payment, health data, or an irreversible action.
7. Keep tools narrow and app-owned. Prefer read-only tools; for mutation require deterministic authorization, validation, idempotence, timeout/error handling, audit/provenance, and explicit user confirmation. The model never becomes the authority for permissions or side effects.
8. Store generated drafts, observations, predictions, transcripts, translations, and classifications separately from trusted domain truth. Show source context/uncertainty when it matters, allow edit/reject/retry, redact logs, and define raw-input/output retention and deletion.
9. Evaluate representative, empty, oversized, multilingual, adversarial, safety-sensitive, low-quality, and stale-input fixtures. Record quality, abstention/refusal, correction rate, latency, memory, battery, thermal state, dropped inputs, and device/OS/model configuration.
10. Verify the actual physical device and target language/model configuration for any claim that depends on Apple Intelligence availability, camera/microphone/sensor behavior, on-device performance, or system-surface invocation. A simulator, mock, preview, or successful compile is narrower evidence.

## Fast path

Establish a deterministic baseline before tuning a model. Compare a representative fixture set covering valid output, malformed output, refusal, missing context, and oversized context, and promote only fields that pass schema, safety, and human-review gates. Expand the fixture set only when a failure reveals a new risk class.

## Evaluation and safety contract

For each evaluation record:

- route/framework/API and source URL;
- target SDK, OS/build, device family, region/language, Apple Intelligence/model/asset state, and model/prompt/schema version;
- input source, redaction/minimization, maximum size, retention, and consent/permission state;
- expected behavior, fixture class, output type, quality/correction/abstention metric, latency, memory, battery, and thermal observations;
- validation/review/commit rule, fallback, and unresolved risks.

Re-run representative prompts/fixtures after OS, SDK, model, language, prompt, schema, preprocessing, or tool changes. Test prompt-injection-like content when user or web content enters the context. Apple guardrails are a base layer; add app-specific domain, audience, privacy, and harm validation.

## Non-negotiable safety and evidence rules

- Never present generated text, OCR, classification, translation, transcription, sound analysis, or model output as medical/legal/financial truth, identity, authenticity, guaranteed accuracy, or authorization without domain validation and appropriate human review.
- Never claim “on-device,” “private,” “real-time,” “supported,” “accurate,” or “safe” from an imported framework, model response, simulator, preview, mock, one prompt, one language, one device, or successful compile.
- Keep source permission, model availability, input availability, output quality, domain validation, and side-effect authorization separate. A model that is ready can still return an unusable or unsafe proposal.
- Do not send sensitive prompts, audio, images, health/personal data, or model output remotely or retain raw inputs beyond the stated feature. Do not add broad permissions, analytics, telemetry, accounts, or servers merely to make an AI demo work.
- Cancel and clean up model sessions, capture, inference, translation, transcription, tool calls, and background tasks when the feature ends. Ignore stale results so an older proposal cannot overwrite newer user state.

Further sections — read when the above is not enough: `references/details.md`.
