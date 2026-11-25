---
name: api-stream-diagnose
description: 'Debug and verify streamed parsers, framing, terminal state and continuation requests. Use when a streamed response or parser fixture misbehaves. RU: стриминг, SSE, потоковый ответ.'
license: MIT
---

# Stream protocol contracts

Use when a streamed response, parser fixture, event-level usage guard or continuation request behaves unexpectedly. Inspect the actual parser, framing, yielded types, state ownership, terminal marker and client loop before changing a fixture or production logic. Do not infer an event shape from a nearby model or assume each transport chunk is a complete event.

Build the smallest valid synthetic stream with real parser and dispatch seams. Cover fragmented frames, multiline events, state-establishing messages, terminal state and documented limits as applicable. First prove the parser reaches the intended state; then separately prove request count and continuation behavior, including identity, policy and privacy flags on each request. A fixture cannot make an intentionally disabled branch reachable.

Validate an event-level budget only after the protocol has assembled the relevant event; one network read or data line is not necessarily one event. Bound frame and buffering growth while parsing, retain the original byte stream when the contract requires passthrough, and establish a protocol-valid positive control through the installed consumer before treating an absent guard rejection as a product defect.

For security and durable delivery, distinguish local send completion from receiver consumption and acknowledgment. Test replay and finalization only through authorized isolated components; test-only controls must be capability-gated and unavailable to ordinary production requests. Keep an active timeout or transport failure distinct from a later cleanup failure. Report synthetic, integration and live-provider evidence separately.

When a protocol emits partial structured calls or other sparse deltas, validate
fragments according to that protocol and assemble them by the documented
identity and ordering before judging the final object. Interleaved text, usage,
completion and terminal markers may have distinct timing; test the real parser
and consumer with representative fragments without requiring each delta to be
a complete object. Do not invent provider-specific fields or terminators.
