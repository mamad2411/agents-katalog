---
name: onchain-router-guide
description: Use Onchain Router models and media safely through the local Buyer Runtime.
---

# Onchain Router

Use provider `onchain-router` for ordinary chat. Select an explicit model from the live model picker
or call `onchain_router_models`; never invent a model name. The local human-owned Buyer Runtime
controls wallet, network, recipient, model allowlist, per-call cap, aggregate budgets, and
confirmation policy.

For images, speech, or transcription, call the corresponding `onchain_router_*` tool. Generate one
stable `idempotency_key` for one logical paid request. Reuse that key only with the identical body
when a human chooses recovery. Never automatically retry a timeout, disconnect, `409`, unknown
provider outcome, unknown settlement outcome, or receipt verification failure, and never fall back
to another model after an ambiguous paid call.

Image results use hosted URLs and include an expiry; download before expiry. Speech returns hosted
audio JSON. Transcription accepts bounded canonical MP3 Base64 only. Obtain human permission for
the audio and set `acknowledge_provider_retention: true`; provider copies may outlive Onchain Router's
encrypted staging deletion.

Do not ask for, read, display, or store a wallet key, mnemonic, proxy bearer, payment signature,
raw payment payload, provider key, or receipt capability. Do not change setup, unlock, funding,
policy, backup, recovery, or package versions. Those are human terminal actions. Use
`/onchain-router status` or `/onchain-router doctor` for redacted readiness. Use the free
`/onchain-router models`, `pricing`, and `voices` subcommands for discovery, and
`/onchain-router recovery` for safe same-key guidance. Ask the human to run
`hermes onchain-router doctor` when readiness fails; an unexpected proxy exit requires an explicit
human `hermes onchain-router status --start` after receipt review.
