---
name: mask-card
description: Maintains the @ekaone/mask-card TypeScript library (credit card masking). Use when working on PAN/credit card masking, maskCard/maskCardAuto/detectCardType/isValidCard changes, PCI display guidance (first 6 + last 4), docs/examples, Vitest tests, tsup builds, versioning, or npm publishing for this repo.
---

# mask-card (project skill)

## Scope

This repository is `@ekaone/mask-card`: a zero-dependency TypeScript library for masking card numbers for **display/logging** and light validation (Luhn + optional length).

Core exported capabilities (high-level):
- `maskCard(input, options?)`
- `maskCardAuto(input, options?)` (brand-typical grouping; normalized spaces; forces `preserveSpacing=false`)
- `maskCardBatch(cards, options?)`
- `detectCardType(input)` and `getCardTypeGrouping(cardType)`
- `isValidCardLuhn(input)` and `isValidCard(input, checkLength?)`
- helpers: `getCardLast`, `getCardFirst`, `getCardLast4`, `getCardFirst6`

## Non-negotiables (security + correctness)

- Do not add features that encourage storing, logging, or transmitting full PANs.
- Keep defaults aligned with common PCI display guidance: **show last 4 digits** by default.
- If adding new examples/docs, avoid printing full PANs; use test numbers and show masked output.
- Preserve behavior documented in `README.md` unless intentionally changed; if changed, update docs + tests together.

## Workflows

### Implementing a change (code + tests + docs)

- Identify affected functions and update behavior in a backward-compatible way when possible.
- Add/adjust Vitest tests for:
  - separators stripping vs `preserveSpacing`
  - grouping behavior (`number` and `number[]`)
  - `maskCardAuto` grouping per brand
  - edge cases: empty/nullish input, very short input, all-zeros for Luhn, 13–19 length checks
- If output format changes (mask char, spacing, grouping), update `README.md` examples accordingly.

### Local validation commands (this repo)

Run from repo root:

```bash
pnpm test
pnpm typecheck
pnpm build
```

### Publishing / release checklist (this repo)

- Ensure `pnpm test` passes (CI parity).
- Ensure `pnpm build` produces `dist/` and package entrypoints remain correct (`main`, `module`, `types`, `exports` in `package.json`).
- Bump `version` in `package.json` using semver.
- Verify `prepublishOnly` remains: `pnpm clean && pnpm build && pnpm test`.
- Publish with npm tooling you already use (this repo is configured as `public`).

## Response style when applying this skill

- Prefer small, targeted diffs and keep API stable.
- When proposing new options, define defaults and update the README option table.
- When asked “is this PCI compliant?”, answer in terms of **display masking guidance** and remind that this library is **display-only** and does not provide secure storage/tokenization/encryption.

