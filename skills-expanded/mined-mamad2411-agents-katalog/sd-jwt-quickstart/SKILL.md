---
name: "sd-jwt-quickstart"
description: "Use when implementing SD-JWT end-to-end quickly. Covers: issuer construction, holder presentation, verifier validation, SD-JWT VC metadata handling, OpenID4VP integration, and common pitfalls."
sections:
  - "SD-JWT Quickstart"
  - "1. Pick your target profile first"
  - "2. Issuer flow (build first)"
  - "3. Holder flow (presentation)"
  - "4. Verifier flow (strict validation)"
  - "5. OpenID4VP transport path (if applicable)"
  - "6. Recommended implementation order"
  - "7. Common failure modes to avoid"
  - "8. Skill loading map"
---

<!-- ARF version: SD-JWT-Quickstart-2026-03 -->
<!-- Tokens: ~904 -->

# SD-JWT Quickstart

This skill provides a practical implementation path for SD-JWT and SD-JWT VC,
from issuer setup through holder presentation and verifier checks.

## 1. Pick your target profile first

- **Core SD-JWT**: Use when you need selective disclosure for JWT claims in
  general.
- **SD-JWT VC**: Use when issuing and presenting verifiable credentials with
  VC-specific claims such as `vct` and metadata discovery.
- **OpenID4VP integration**: Use when the presentation is transported through
  OpenID4VP.

## 2. Issuer flow (build first)

### 2.1 Model claims and disclosure policy

- Decide which claims are always disclosed vs selectively disclosed.
- Define claim structure early (flat vs nested) because this affects disclosure
  packaging and verifier logic.

Primary skills:
- `sd-jwt-format`
- `sd-jwt-examples`
- `sd-jwt-examples-nested`

### 2.2 Construct and sign SD-JWT

- Create disclosures with salts and digest bindings.
- Sign the issuer payload with JWS.
- If using key binding, define KB requirements and holder key handling.

Primary skills:
- `sd-jwt-format`
- `sd-jwt-security`

### 2.3 Add VC-specific metadata (SD-JWT VC)

- Set and validate the `vct` claim.
- Publish and consume issuer/type metadata consistently.

Primary skills:
- `sd-jwt-vc-intro`
- `sd-jwt-vc-metadata`

## 3. Holder flow (presentation)

- Select only requested claims and include matching disclosures.
- Keep undisclosed claims unlinkable and avoid over-disclosure.
- Include key binding material when required by policy or protocol.

Primary skills:
- `sd-jwt-verification`
- `sd-jwt-vc-presentation-security`

## 4. Verifier flow (strict validation)

### 4.1 Core checks

- Verify issuer signature and algorithm policy.
- Validate each disclosure digest mapping.
- Enforce claim semantics (types, expected values, schema/profile checks).

### 4.2 Security and privacy checks

- Reject malformed or ambiguous claim names.
- Enforce anti-replay and nonce/session binding in protocol flows.
- Apply minimum disclosure and correlation-risk controls.

Primary skills:
- `sd-jwt-verification`
- `sd-jwt-security`
- `sd-jwt-vc-presentation-security`

## 5. OpenID4VP transport path (if applicable)

- Map SD-JWT VC presentations to OpenID4VP request/response parameters.
- Validate protocol-level checks (nonce, audience/context binding, response
  integrity) in addition to credential-level checks.

Primary skills:
- `oid4vp-format-sd-jwt-vc`
- `oid4vp-authorization-request`
- `oid4vp-response`
- `oid4vp-security`

## 6. Recommended implementation order

1. Issuer signs fixed claims (no selective disclosure yet)
2. Add selective disclosures and verifier digest checks
3. Add nested-claim support
4. Add SD-JWT VC metadata (`vct`, type metadata, issuer metadata)
5. Add key binding policy and enforcement
6. Add OpenID4VP transport integration
7. Run negative tests (tampered disclosures, wrong salts, replayed responses)

## 7. Common failure modes to avoid

- Treating disclosure validation as optional (it is mandatory).
- Mixing profile assumptions across SD-JWT and SD-JWT VC deployments.
- Implementing protocol checks without credential-level digest validation.
- Over-disclosing claims due to weak selection logic.
- Ignoring correlation/privacy guidance during verifier design.

## 8. Skill loading map

- **Need foundations** -> `sd-jwt-intro`, `sd-jwt-format`
- **Need concrete examples** -> `sd-jwt-examples`, `sd-jwt-examples-nested`
- **Need verifier logic** -> `sd-jwt-verification`, `sd-jwt-security`
- **Need VC profile details** -> `sd-jwt-vc-intro`, `sd-jwt-vc-metadata`,
  `sd-jwt-vc-presentation-security`
- **Need protocol transport** -> `oid4vp-format-sd-jwt-vc`,
  `oid4vp-authorization-request`, `oid4vp-response`, `oid4vp-security`

