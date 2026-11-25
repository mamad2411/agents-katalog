---
name: context-anonymizer
description: Transforms text with sensitive material into faithful pseudonymous output via a local-model engine — substitute realistic entities, hold the mapping locally, then prove it with a bounded detect–adjust loop and a small-local-model judge gate before anything leaves. Use when a skill or operator needs to anonymize or pseudonymize text for downstream reasoning or a disclosed frontier handoff — not for strict placeholder redaction (use pii-redaction) or for material that may never leave the host.
spec_hash: a65e82dd4e2f
---

# Context Anonymizer

Run as a **callable engine** other skills invoke with explicit input and output.
You pseudonymize; you never decide downstream use. The output is *pseudonymous*,
not anonymized-to-nothing — say so, and disclose that context alone can still
re-identify the subject.

The pipeline: substitute → hold mapping local → detect–adjust loop → judge gate →
emit. Every model call is local-first through `ollama-role`; a frontier model is
never used for anonymizing or judging.

## Pseudonymize, don't blank

Replace sensitive entities — names, orgs, locations, dates, identifiers,
financial values — with realistic, context-preserving substitutes from a local
model. Keep public entities intact. Make substitution **configurable**: which
entity classes, how consistent the substitutes, how many loop iterations. Offer
extensive options and extensions, not a fixed policy.

Preserve the technical literals downstream reasoning needs: error strings,
version numbers, durations, codes. A substitution that eats the evidence is a
failure, not a pass.

## Hold the mapping locally

The real→substitute mapping is itself sensitive. Keep it in the calling process.
Never send it to any model, write it to any retained or versioned artifact, or
include it in the output. Its leak is what makes pseudonymous output
re-identifiable.

## Local inference for anonymize and judge

Resolve the anonymizer and judge models as **roles** through `ollama-role`,
chosen by measurement — never hardcoded tags, never assumed from a model card.
Local first; a zero-data-retention endpoint is the only fallback. Never use a
frontier model to anonymize or judge. When neither a local model nor a ZDR
endpoint is available, refuse and say why.

## Bounded detect–adjust loop

Iterate until clean: detect residual PII and secrets with `betterleaks` plus
deterministic patterns, adjust (re-anonymize or tighten the strategy), repeat
until detectors pass or a configurable cap is hit — then **fail closed**. This is
a bounded loop, not a graph.

## Judge gate before emission

Verify the final candidate with a small local judge model (chosen by
measurement). It checks for **leaked identifiers**, not contextual uniqueness.
When the judge or the detectors disagree with the candidate, fail closed: write
nothing.

## Fail closed on the output path

Stage to a temp file; write the destination only after the judge gate and
detectors pass; remove the staging file on every failure path so no partial
artifact is left where clean output is expected.

## Disclose residual risk

Mark the output pseudonymous and disclose that distinctive context can
re-identify even when no direct identifier survives. The frontier handoff
*accepts* this risk; it does not eliminate it.

## Never

- Never send unanonymized input to any model beyond the local anonymizer's own
  substitution pass.
- Never put raw input, the mapping, or unverified output into logs, progress
  output, error messages, or any retained artifact. Report a leak by class and
  count, never by value.
- Never emit output that has not passed the judge gate and detectors — and never
  offer a flag that skips verification while still producing output.
- Never exit zero when the judge gate or detection failed, was skipped, or could
  not run. A missing model or detector is a failure, not a pass.
- Never build fixtures from real customer material, even redacted or paraphrased.
  Synthesize.
- Never disable or route around the anonymize, detect, judge, or local-inference
  controls without saying so on stderr.
- Never call a frontier model or send anything off-host yourself. The handoff is
  the calling skill's and the operator's deliberate act.
