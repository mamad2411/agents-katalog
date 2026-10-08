---
name: calculate-hash
description: Calculate the cryptographic hash of a given text. Supports SHA-1, SHA-256, SHA-384, and SHA-512.
---

# Calculate Hash

This skill calculates the cryptographic hash of any text, fully offline using the built-in WebCrypto API.

## Supported Algorithms
- **SHA-256** (default — recommended)
- **SHA-512**
- **SHA-384**
- **SHA-1** (legacy, avoid for security-sensitive use)

## Instructions

Call the `run_js` tool with:
- **script name**: `index.html`
- **data**: A JSON string with:
  - `text`: String — the text to hash
  - `algorithm`: String (optional) — one of `SHA-256`, `SHA-512`, `SHA-384`, `SHA-1`. Defaults to `SHA-256` if not specified.

## Examples
- "What is the SHA-256 hash of 'hello world'?"
- "Calculate the SHA-512 of this string: ..."
- "Hash 'password123' with SHA-1"
- "What is the hash of 'gemma'?" → use SHA-256 by default
