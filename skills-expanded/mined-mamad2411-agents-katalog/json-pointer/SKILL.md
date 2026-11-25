---
name: json-pointer
description: >-
  JSON Pointer (RFC 6901): identify and evaluate a specific value within a JSON document. Covers RFC 6901 JavaScript Object Notation (JSON) Pointer. Use when evaluating a JSON Pointer. Triggers: JSON Pointer, RFC 6901.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# JavaScript Object Notation (JSON) Pointer

JavaScript Object Notation (JSON) Pointer

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when evaluating a JSON Pointer.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: RFC 6901 JavaScript Object Notation (JSON) Pointer (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **RFC 6901 § 3.** "Because the characters '~' (%x7E) and '/' (%x2F) have special meanings in JSON Pointer, '~' needs to be encoded as '~0' and '/' needs to be encoded as '~1' when these characters appear in a reference token."
2. **RFC 6901 § 3.** "It is an error condition if a JSON Pointer value does not conform to this syntax (see Section 7)."
3. **RFC 6901 § 4.** "Evaluation of each reference token begins by decoding any escaped character sequence. This is performed by first transforming any occurrence of the sequence '~1' to '/', and then transforming any occurrence of the sequence '~0' to '~'."
4. **RFC 6901 § 4.** "The member name is equal to the token if it has the same number of Unicode characters as the token and their code points are byte-by-byte equal."
5. **RFC 6901 § 4.** "No Unicode character normalization is performed."
6. **RFC 6901 § 4.** "If the currently referenced value is a JSON array, the reference token MUST contain either: * characters comprised of digits (see ABNF below; note that leading zeros are not allowed) that represent an unsigned base-10 integer value, making the new referenced value the array element with the zero-based index identified by the token, or * exactly the single character "-", making the new referenced value the (nonexistent) member after the last array element."
7. **RFC 6901 § 4.** "Implementations will evaluate each reference token against the document's contents and will raise an error condition if it fails to resolve a concrete value for any of the JSON pointer's reference tokens."
8. **RFC 6901 § 4.** "Any error condition for which a specific action is not defined by the JSON Pointer application results in termination of evaluation."
9. **RFC 6901 § 5.** "Per [RFC4627], Section 2.5, all instances of quotation mark '"' (%x22), reverse solidus '\' (%x5C), and control (%x00-1F) characters MUST be escaped."
10. **RFC 6901 § 7.** "An application of JSON Pointer SHOULD specify the impact and handling of each type of error."

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

- `json-schema`, when the work also follows that specification: `npx skills add ScaleDockHQ/scaledock-skills --skill json-schema`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [RFC 6901 JavaScript Object Notation (JSON) Pointer](https://www.rfc-editor.org/rfc/rfc6901.html): PROPOSED STANDARD, RFC 6901 (PROPOSED STANDARD, April 2013), checked 2026-10-06.
