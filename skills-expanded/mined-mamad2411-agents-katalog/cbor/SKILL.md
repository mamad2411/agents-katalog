---
name: cbor
description: >-
  Concise Binary Object Representation (CBOR): The Concise Binary Object Representation (CBOR) is a data format whose design goals include the possibility of extremely small code size, fairly small message size, and extensibility without the need for version negotiation. Covers RFC 8949 Concise Binary Object Representation (CBOR), RFC 8610 Concise Data Definition Language (CDDL): A Notational Convention to Express Concise Binary Object Representation (CBOR) and JSON Data Structures, RFC 9165 Additional Control Operators for the Concise Data Definition Language (CDDL). Use when encoding CBOR or writing CDDL. Triggers: CBOR, CDDL, RFC 8949.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# Concise Binary Object Representation (CBOR)

The Concise Binary Object Representation (CBOR) is a data format whose design goals include the possibility of extremely small code size, fairly small message size, and extensibility without the need for version negotiation. These design goals make it different from earlier binary serializations such as ASN.1 and MessagePack. ¶ This document obsoletes RFC 7049, providing editorial improvements, new details, and errata fixes while keeping full compatibility with the interchange format of RFC 7049. It does not create a new version of the format. ¶

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when encoding CBOR or writing CDDL.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: RFC 8949 Concise Binary Object Representation (CBOR) (default); RFC 8610 Concise Data Definition Language (CDDL): A Notational Convention to Express Concise Binary Object Representation (CBOR) and JSON Data Structures (default); RFC 9165 Additional Control Operators for the Concise Data Definition Language (CDDL) (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **RFC 8949 § 3.** "An encoder MUST produce only well-formed encoded data items."
2. **RFC 8949 § 3.** "A decoder MUST NOT return a decoded data item when it encounters input that is not a well-formed encoded CBOR data item (this does not detract from the usefulness of diagnostic and recovery tools that might make available some information from a damaged encoded CBOR data item)."
3. **RFC 8949 § 2.2.** "For example, in the generic data model, a valid map MAY have both "0" and "0.0" as keys, and an encoder MUST NOT encode "0.0" as an integer (major type 0, Section 3.1)."
4. **RFC 8949 § 4.2.1.** "Indefinite-length items MUST NOT appear."
5. **RFC 8949 § 4.2.1.** "The keys in every map MUST be sorted in the bytewise lexicographic order of their deterministic encodings."
6. **RFC 8949 § 5.** "CBOR-based protocols MUST specify how their decoders handle invalid and other unexpected data."
7. **RFC 8949 § 5.** "Encoders for CBOR-based protocols MUST produce only valid items, that is, the protocol cannot be designed to make use of invalid items."
8. **RFC 8949 § 5.6.** "A CBOR-based protocol MUST define what to do when a receiving application sees multiple identical keys in a map."
9. **RFC 8610 § 2.2.4.** "There is no special syntax to identify the root of a CDDL data structure definition: that role is simply taken by the first rule defined in the file."
10. **RFC 9165 § 2.2.** "If the target is a text string, the result of that concatenation MUST be valid UTF-8."

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

- [RFC 8949 Concise Binary Object Representation (CBOR)](https://www.rfc-editor.org/rfc/rfc8949.html): INTERNET STANDARD, RFC 8949 (INTERNET STANDARD, December 2), checked 2026-10-06.
- [RFC 8610 Concise Data Definition Language (CDDL): A Notational Convention to Express Concise Binary Object Representation (CBOR) and JSON Data Structures](https://www.rfc-editor.org/rfc/rfc8610.html): PROPOSED STANDARD, RFC 8610 (PROPOSED STANDARD, June 2019), checked 2026-10-06.
- [RFC 9165 Additional Control Operators for the Concise Data Definition Language (CDDL)](https://www.rfc-editor.org/rfc/rfc9165.html): PROPOSED STANDARD, RFC 9165 (PROPOSED STANDARD, December 2), checked 2026-10-06.
