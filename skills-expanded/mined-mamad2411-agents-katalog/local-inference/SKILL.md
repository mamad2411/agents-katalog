---
name: local-inference
description: Use when an approved local inference runner is available, especially for privacy-tagged file input that must stay outside agent, cloud, connector, and remote model contexts.
user-invocable: true
---

# Local Inference

Use the installed Kherep local-inference runner and its validated configuration. Discover the runner through repository or installation metadata. Do not assume a path, operating system, backend, model, host, port, transport, or startup command.

## Privacy mode

For credentials, personal data, customer material, private infrastructure details, or another privacy-tagged source:

1. Do not read, search, edit, or copy the private content into the agent context.
2. Pass only a generic task and an authorized file reference to the direct local runner.
3. Require the runner to enforce allowed roots, transport policy, restrictive artifact permissions, and no cloud fallback.
4. Do not read the private result artifact back into an agent or cloud context.
5. Return only metadata explicitly classified as safe by the runner. Default to a minimal status and opaque receipt; reveal paths, host details, backend names, model names, or hashes only when the user needs them and policy permits disclosure.

Remote execution is not equivalent to local execution. It requires a configured encrypted route plus user policy that permits the data to leave the source host.

## Non-private mode

Public input must be positively classified using the runner's supported flag or policy. The runner may return public output only when that classification succeeds. File input remains private by default.

## Failure behavior

If the configured route is unavailable, return `BLOCKED` with a safe diagnostic. Never build an endpoint from guessed machine details, disable transport checks, invent a model identifier, or silently fall back to a cloud service.

## Receipt

For private work, report `STATUS` and an opaque `RECEIPT` unless policy exposes additional metadata. For public work, return the approved output plus the same safe receipt.
