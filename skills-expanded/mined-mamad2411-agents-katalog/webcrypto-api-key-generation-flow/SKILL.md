---
name: webcrypto-api-key-generation-flow
description: Designs safe browser-local WebCrypto key generation flows. Use when creating anonymous credential keys, encryption keys, signing keys, wrapping keys, key-pair lifecycle UX, recovery behavior, or local CryptoKey persistence.
license: MIT
---

# WebCrypto API Key Generation Flow

This skill designs local key-generation flows in the browser or web runtime. It covers WebCrypto key generation, key usages, extractability, storage, recovery, and UX tradeoffs.

It does not define voting, credential issuance, blind-signature, tally, trustee, or proof-system protocols.

## Use For

- Local browser key generation.
- Anonymous credential key-pair generation.
- Browser-generated encryption or signing keys.
- Key wrapping or local backup UX.
- Recovery, rotation, deletion, and lost-device behavior.

## Workflow

Use `workflows/local-key-generation-flow-workflow.md`.

## Resource

Use `resources/key-generation-decision-tree.md`.

## Example

Use `examples/local-key-generation.ts`.
