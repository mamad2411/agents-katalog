---
name: cose
description: >-
  CBOR Object Signing and Encryption (COSE): Structures and Process: Concise Binary Object Representation (CBOR) is a data format designed for small code size and small message size. Covers RFC 9052 CBOR Object Signing and Encryption (COSE): Structures and Process, RFC 9053 CBOR Object Signing and Encryption (COSE): Initial Algorithms, RFC 9360 CBOR Object Signing and Encryption (COSE): Header Parameters for Carrying and Referencing X.509 Certificates, RFC 9964 ML-DSA for JSON Object Signing and Encryption (JOSE) and CBOR Object Signing and Encryption (COSE). Use when signing or encrypting with COSE. Triggers: COSE, RFC 9052, ML-DSA.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# CBOR Object Signing and Encryption (COSE): Structures and Process

Concise Binary Object Representation (CBOR) is a data format designed for small code size and small message size. There is a need to be able to define basic security services for this data format. This document defines the CBOR Object Signing and Encryption (COSE) protocol. This specification describes how to create and process signatures, message authentication codes, and encryption using CBOR for serialization. This specification additionally describes how to represent cryptographic keys using CBOR. ¶ This document, along with RFC 9053, obsoletes RFC 8152. ¶

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when signing or encrypting with COSE.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: RFC 9052 CBOR Object Signing and Encryption (COSE): Structures and Process (default); RFC 9053 CBOR Object Signing and Encryption (COSE): Initial Algorithms (default); RFC 9360 CBOR Object Signing and Encryption (COSE): Header Parameters for Carrying and Referencing X.509 Certificates (default); RFC 9964 ML-DSA for JSON Object Signing and Encryption (JOSE) and CBOR Object Signing and Encryption (COSE) (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **RFC 9052 § 3.** "When processing messages, if a label appears multiple times, the message MUST be rejected as malformed."
2. **RFC 9052 § 3.** "If the message is not rejected as malformed, attributes MUST be obtained from the protected bucket, and only if an attribute is not found in the protected bucket can that attribute be obtained from the unprotected bucket."
3. **RFC 9052 § 3.1.** "When present, the "crit" header parameter MUST be placed in the protected-header-parameters bucket."
4. **RFC 9052 § 7.1.** "Implementations MUST verify that the key type is appropriate for the algorithm being processed."
5. **RFC 9052 § 8.3.** "The message content MUST NOT be used if the decryption does not validate."
6. **RFC 9052 § 9.** "Encoding MUST be done using definite lengths, and the length of the (encoded) argument MUST be the minimum possible length."
7. **RFC 9053 § 4.1.1.** "The key and nonce pair MUST be unique for every message encrypted."
8. **RFC 9053 § 7.1.** "Applications MUST check that the curve and the key type are consistent and reject a key if they are not."
9. **RFC 9360 § 2.** "The trust mechanism MUST process any certificates in this parameter as untrusted input."
10. **RFC 9360 § 5.** "In any event, both the signature validation and the certificate validation MUST be completed successfully before acting on any requests."
11. **RFC 9964 § 3.** "The priv parameter contains private information and MUST NOT be present in public keys."

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

- `jwt`, when the work also follows that specification: `npx skills add ScaleDockHQ/scaledock-skills --skill jwt`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [RFC 9052 CBOR Object Signing and Encryption (COSE): Structures and Process](https://www.rfc-editor.org/rfc/rfc9052.html): INTERNET STANDARD, RFC 9052 (INTERNET STANDARD, August 202), checked 2026-10-06.
- [RFC 9053 CBOR Object Signing and Encryption (COSE): Initial Algorithms](https://www.rfc-editor.org/rfc/rfc9053.html): INFORMATIONAL, RFC 9053 (INFORMATIONAL, August 202), checked 2026-10-06.
- [RFC 9360 CBOR Object Signing and Encryption (COSE): Header Parameters for Carrying and Referencing X.509 Certificates](https://www.rfc-editor.org/rfc/rfc9360.html): PROPOSED STANDARD, RFC 9360 (PROPOSED STANDARD, February 2), checked 2026-10-06.
- [RFC 9964 ML-DSA for JSON Object Signing and Encryption (JOSE) and CBOR Object Signing and Encryption (COSE)](https://www.rfc-editor.org/rfc/rfc9964.html): PROPOSED STANDARD, RFC 9964 (PROPOSED STANDARD, May 2026), checked 2026-10-06.
