---
name: openpgp
description: >-
  OpenPGP: This document specifies the message formats used in OpenPGP. Covers RFC 9580 OpenPGP. Use when signing or encrypting with OpenPGP. Triggers: OpenPGP, RFC 9580.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# OpenPGP

This document specifies the message formats used in OpenPGP. OpenPGP provides encryption with public key or symmetric cryptographic algorithms, digital signatures, compression, and key management. ¶ This document is maintained in order to publish all necessary information needed to develop interoperable applications based on the OpenPGP format. It is not a step-by-step cookbook for writing an application. It describes only the format and methods needed to read, check, generate, and write conforming packets crossing any network. It does not deal with storage and implementation questions. It does, however, discuss implementation issues necessary to avoid security flaws. ¶ This document obsolet

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when signing or encrypting with OpenPGP.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: RFC 9580 OpenPGP (default); RFC 4880 OpenPGP Message Format (legacy: read and upgrade, never author). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **RFC 9580 § 3.7.2.** "Therefore, when generating an S2K Specifier, an implementation MUST NOT use Simple S2K."
2. **RFC 9580 § 4.3.** "If an implementation encounters a critical packet where the packet type is unknown in a packet sequence, it MUST reject the whole packet sequence (see Section 10)."
3. **RFC 9580 § 5.2.** "An implementation MUST generate a version 6 signature when signing with a version 6 key."
4. **RFC 9580 § 5.2.5.** "When an implementation encounters such a malformed or unknown signature, it MUST ignore the signature for validation purposes."
5. **RFC 9580 § 9.1.** "Implementations MUST implement Ed25519 (27) for signatures and X25519 (25) for encryption."
6. **RFC 9580 § 9.3.** "Implementations MUST NOT encrypt data with IDEA, TripleDES, or CAST5."
7. **RFC 9580 § 9.5.** "Implementations MUST NOT generate signatures with MD5, SHA-1, or RIPEMD-160."
8. **RFC 9580 § 9.5.** "Implementations MUST NOT validate any recent signature that depends on MD5, SHA-1, or RIPEMD-160."
9. **RFC 9580 § 10.3.2.1.** "An implementation processing an Encrypted Message MUST discard any preceding ESK packet with a version that does not align with the version of the payload."
10. **RFC 9580 § 13.7.** "In the case of AEAD encrypted data, if the authentication tag fails to verify, the implementation MUST NOT attempt to parse nor release decrypted data to the user, and it MUST halt with an error."
11. **RFC 4880 § 14.** "An implementation MUST treat an MDC failure as a security problem, not merely a data problem."

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

- [RFC 9580 OpenPGP](https://www.rfc-editor.org/rfc/rfc9580.html): PROPOSED STANDARD, RFC 9580 (PROPOSED STANDARD, July 2024), checked 2026-10-06.
- [RFC 4880 OpenPGP Message Format](https://www.rfc-editor.org/rfc/rfc4880.html): PROPOSED STANDARD, RFC 4880 (PROPOSED STANDARD, November 2), checked 2026-10-06.
