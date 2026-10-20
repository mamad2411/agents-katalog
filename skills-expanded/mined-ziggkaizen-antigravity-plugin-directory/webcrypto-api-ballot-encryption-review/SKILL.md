---
name: webcrypto-api-ballot-encryption-review
description: Reviews browser-side encrypted ballot flows that use WebCrypto for local encryption support. Use when checking ballot plaintext handling, ciphertext submission, key usage, associated data, runtime compatibility, URL/storage/log leakage, and protocol boundary separation.
license: MIT
---

# WebCrypto API Ballot Encryption Review

This skill reviews browser-side ballot encryption flow boundaries: plaintext handling, public key import, WebCrypto invocation, ciphertext packaging, submission, receipt display, and leakage controls.

It does not design ElectionGuard, homomorphic tallying, proof systems, trustee threshold decryption, credential issuance, or public bulletin-board verification.

## Use For

- Browser handling of ballot plaintext choices.
- Browser encryption invocation.
- Encrypted ballot submission shape.
- Receipt/inclusion reference display.
- URL, storage, log, analytics, and telemetry leakage review.

## Workflow

Use `workflows/browser-ballot-encryption-review-workflow.md`.

## Resource

Use `resources/ballot-encryption-boundary-checklist.md`.

## Example

Use `examples/ballot-encryption-review-notes.md`.
