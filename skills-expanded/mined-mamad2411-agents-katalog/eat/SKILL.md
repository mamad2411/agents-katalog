---
name: eat
description: >-
  The Entity Attestation Token (EAT): An Entity Attestation Token (EAT) provides an attested claims set that describes the state and characteristics of an entity, a device such as a smartphone, an Internet of Things (IoT) device, network equipment, or such. Covers RFC 9711 The Entity Attestation Token (EAT). Use when producing or verifying an entity attestation token. Triggers: EAT, RFC 9711, RATS.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# The Entity Attestation Token (EAT)

An Entity Attestation Token (EAT) provides an attested claims set that describes the state and characteristics of an entity, a device such as a smartphone, an Internet of Things (IoT) device, network equipment, or such. This claims set is used by a relying party, server, or service to determine the type and degree of trust placed in the entity. ¶ An EAT is either a CBOR Web Token (CWT) or a JSON Web Token (JWT) with attestation-oriented claims. ¶

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when producing or verifying an entity attestation token.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: RFC 9711 The Entity Attestation Token (EAT) (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **RFC 9711 § 3.** "An EAT MUST contain a Claims-Set."
2. **RFC 9711 § 3.** "An EAT MUST have authenticity and integrity protection."
3. **RFC 9711 § 4.** "However, in the absence of such requirements, all claims that are not understood by implementations MUST be ignored."
4. **RFC 9711 § 4.** "All claims in an EAT MUST use the same encoding except where otherwise explicitly stated (e.g., in a CBOR-encoded token, all claims must be encoded with CBOR)."
5. **RFC 9711 § 4.1.** "An EAT nonce MUST have at least 64 bits of entropy."
6. **RFC 9711 § 4.2.1.2.** "The consumer of a UEID MUST treat it as a completely opaque string of bytes and MUST NOT make any use of its internal structure."
7. **RFC 9711 § 4.2.18.1.** "The encoding of a submodule Claims-Set MUST be the same as the encoding of the surrounding EAT, e.g., all submodule Claims-Sets in a CBOR-encoded token must be CBOR encoded."
8. **RFC 9711 § 4.3.1.** "An EAT token MUST NOT contain an "iat" claim in floating-point format."
9. **RFC 9711 § 6.2.** "Full profiles MUST be complete such that a complying receiver can decode, verify, and check for freshness for every EAT created by a complying sender."
10. **RFC 9711 § 9.3.** "All EAT use MUST provide a freshness mechanism to prevent replay and related attacks."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the section it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [RFC 9711 The Entity Attestation Token (EAT)](https://www.rfc-editor.org/rfc/rfc9711.html): PROPOSED STANDARD, RFC 9711 (PROPOSED STANDARD, April 2025), checked 2026-10-06.
