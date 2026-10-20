---
name: ios-media-ml-and-inputs
description: Route, implement, or review iOS media, camera, audio, Vision, Core ML, Natural Language, NFC, MusicKit, ShazamKit, and video-processing features. Use when a feature captures or imports media, runs on-device models, reads tags, accesses Apple Music, identifies audio, or needs measured physical-device performance.
allowed-tools: Read, Grep, Glob
---

# iOS Media, ML, and Physical Inputs

## Overview

Use this skill to turn a camera frame, audio stream, imported asset, model, NFC tag, music catalog request, or acoustic match into a bounded, reviewable product flow. Keep this pipeline explicit:

`authorized source -> bounded input -> cancellable processing -> observation/prediction/match -> provenance/review -> durable result or user-confirmed side effect`

## Read before acting

- Inspect the actual Xcode targets, deployment target, device family, scene/lifecycle model, capabilities, entitlements, `Info.plist` usage descriptions, model assets, media formats, persistence, and existing capture/playback adapters.
- Read the [knowledge-base map](../ios-knowledge-base/references/README.md), [media/camera/sensor route](../ios-knowledge-base/references/40-framework-routes/02-media-camera-and-sensors.md), [media and ML deep dive](../ios-knowledge-base/references/42-framework-deep-dives/07-media-vision-ml-and-nfc.md), and [media/ML recipes](../ios-knowledge-base/references/70-code-recipes/21-media-vision-ml-and-nfc-recipes.md).
- For AI availability and fallback, read [privacy, availability, safety, and fallback](../ios-knowledge-base/references/30-on-device-ai/06-privacy-availability-and-fallback.md). For proof levels, read the [build/device/release checklist](../ios-knowledge-base/references/60-verification/01-build-device-and-release-checklist.md) and [permission/entitlement/privacy checklist](../ios-knowledge-base/references/60-verification/04-permission-entitlement-and-privacy-checklist.md).
- Refresh the exact official Apple pages in the Sources section before relying on an API spelling, availability annotation, entitlement, codec, model runtime, music access rule, NFC behavior, or iOS 26 claim.

## Route workflow

1. State the user outcome and source ownership: live camera/microphone, imported file, app-owned media, model asset, external NFC tag, Apple Music catalog/account, or ambient audio.
2. Choose the narrowest route. Use AVKit/AVFoundation for playback/capture/session state; Core Image for image recipes/rendering; VideoToolbox only for low-level codec control; Vision for system observations; Core ML for a packaged model; Natural Language for locale-aware text analysis; Core NFC for a foreground tag-reader session; MusicKit for Apple Music authorization/catalog/playback; ShazamKit for acoustic matching.
3. Record target configuration before implementation: permission and usage description, capability/entitlement, supported formats, model availability, locale, account/subscription state, and physical-device requirement. Mark unverified items as `to-verify`.
4. Draw the state machine. Keep permission, source/session readiness, model/asset readiness, processing, result review, persistence, and cleanup as separate states. Include denial, unavailable hardware, malformed input, interruption, timeout, cancellation, no match, no subscription, and retry.
5. Bound the work. Coalesce or drop stale live frames; limit image/audio duration and dimensions; limit NFC payload length; use cancellation checks; avoid one unbounded task per frame; stop capture and release resources when the feature ends.
6. Attach provenance to every result: source identifier, capture/import time, orientation and preprocessing, request/model/revision, locale, confidence or quality when provided, and user review/edit state. Keep an observation, prediction, match, catalog response, or tag payload distinct from domain truth.
7. Define privacy and retention before logging or persistence. Prefer local processing, redact media/text/audio/model outputs from diagnostics, delete raw inputs when no longer needed, and do not add analytics, upload, account access, or telemetry without a product reason and authorization.
8. Verify in layers: compile against the actual SDK, test deterministic fixtures, test denied/interrupted/unavailable states, then exercise the real camera/microphone/audio route/NFC tag/Apple account on representative physical devices. Record device, OS, model, fixture, latency, dropped inputs, memory, battery, and thermal observations instead of claiming generic “real-time” or “on-device” behavior.

## Fast path

Prove the bounded lifecycle with a fixture source before live capture: one input -> one validated output -> cancellation and teardown. Add only the permission and physical route required by that slice, and measure queue, memory, and backpressure behavior rather than recording a successful frame as completion.

## Non-negotiable safety and evidence rules

- Never present model output, OCR, object/face/pose observation, Natural Language result, NFC payload, MusicKit catalog response, or ShazamKit match as identity, authenticity, medical truth, legal truth, guaranteed accuracy, or authorization without a separate validated domain workflow.
- Never claim camera/microphone/NFC/codec/model support, Apple Music availability, audio/video synchronization, “real time,” “on-device,” battery life, or thermal safety from a preview, simulator, fixture, successful compile, or single device.
- Keep source authorization separate from output validity. Permission granted does not mean a usable session; a ready player does not mean rendered output; a loaded model does not mean a valid prediction; a detected tag does not mean trusted data; MusicKit authorization does not mean a subscription; a match does not mean legal or user identity.
- Treat every external or user-controlled input as untrusted. Bound data size and duration, validate types/schemes/commands/shapes, reject malformed payloads, and require confirmation before consequential side effects.
- Stop and clean up capture, playback, reader sessions, model tasks, signatures, and codec sessions on cancellation, view disappearance, interruption, session invalidation, and task expiration. Keep task ownership explicit so stale results cannot overwrite newer state.

## Deliverable

Produce a compact route note or implementation change containing:

- selected framework and rejected alternatives;
- target/device, permission, usage-description, capability, entitlement, model/media-format, account/subscription, and privacy matrix;
- session/model/processing/result state machine with cancellation, backpressure, cleanup, retry, and fallback;
- provenance and review policy for every generated observation/prediction/match;
- source links and exact compile, fixture, physical-device, performance, privacy, signing, and release evidence plan;
- remaining `to-verify` gaps and any claims deliberately not made.

For implementation, change only the requested target and directly related adapters/configuration. Do not add a model download, cloud upload, account, Apple Music access, microphone/NFC permission, background mode, analytics, logging of sensitive inputs, or entitlement without a stated user-facing need and authorization.

Further sections — read when the above is not enough: `references/details.md`.
