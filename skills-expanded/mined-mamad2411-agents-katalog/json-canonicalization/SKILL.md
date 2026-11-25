---
name: json-canonicalization
description: >-
  JSON Canonicalization Scheme (JCS): Cryptographic operations like hashing and signing need the data to be expressed in an invariant format so that the operations are reliably repeatable. Covers RFC 8785 JSON Canonicalization Scheme (JCS). Use when canonicalizing JSON for signing. Triggers: RFC 8785, JCS.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# JSON Canonicalization Scheme (JCS)

Cryptographic operations like hashing and signing need the data to be expressed in an invariant format so that the operations are reliably repeatable. One way to address this is to create a canonical representation of the data. Canonicalization also permits data to be exchanged in its original form on the "wire" while cryptographic operations performed on the canonicalized counterpart of the data in the producer and consumer endpoints generate consistent results. ¶ This document describes the JSON Canonicalization Scheme (JCS). This specification defines how to create a canonical representation of JSON data by building on the strict serialization methods for

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when canonicalizing JSON for signing.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: RFC 8785 JSON Canonicalization Scheme (JCS) (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **RFC 8785 § 3.1.** "Irrespective of the method used, the data to be serialized MUST be adapted for I-JSON [RFC7493] formatting, which implies the following:"
2. **RFC 8785 § 3.1.** "* JSON objects MUST NOT exhibit duplicate property names."
3. **RFC 8785 § 3.1.** "An additional constraint is that parsed JSON string data MUST NOT be altered during subsequent serializations."
4. **RFC 8785 § 3.2.1.** "Whitespace between JSON tokens MUST NOT be emitted."
5. **RFC 8785 § 3.2.2.2.** "* If the Unicode value falls within the traditional ASCII control character range (U+0000 through U+001F), it MUST be serialized using lowercase hexadecimal Unicode notation (\uhhhh) unless it is in the set of predefined JSON control characters U+0008, U+0009, U+000A, U+000C, or U+000D, which MUST be serialized as \b, \t, \n, \f, and \r, respectively."
6. **RFC 8785 § 3.2.2.2.** "Since invalid Unicode data like "lone surrogates" (e.g., U+DEAD) may lead to interoperability issues including broken signatures, occurrences of such data MUST cause a compliant JCS implementation to terminate with an appropriate error."
7. **RFC 8785 § 3.2.2.3.** "Since Not a Number (NaN) and Infinity are not permitted in JSON, occurrences of NaN or Infinity MUST cause a compliant JCS implementation to terminate with an appropriate error."
8. **RFC 8785 § 3.2.3.** "* JSON object properties MUST be sorted recursively, which means that JSON child Objects MUST have their properties sorted as well."
9. **RFC 8785 § 3.2.3.** "* JSON array data MUST also be scanned for the presence of JSON objects (if an object is found, then its properties MUST be sorted), but array element order MUST NOT be changed."
10. **RFC 8785 § 3.2.4.** "Finally, in order to create a platform-independent representation, the result of the preceding step MUST be encoded in UTF-8."

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

- [RFC 8785 JSON Canonicalization Scheme (JCS)](https://www.rfc-editor.org/rfc/rfc8785.html): INFORMATIONAL, RFC 8785 (INFORMATIONAL, June 2020), checked 2026-10-06.
