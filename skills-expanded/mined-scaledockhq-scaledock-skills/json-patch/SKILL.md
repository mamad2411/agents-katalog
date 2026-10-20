---
name: json-patch
description: >-
  JSON Patch (RFC 6902) and JSON Merge Patch (RFC 7396): describe and apply changes to JSON documents. Covers RFC 6902 JavaScript Object Notation (JSON) Patch, RFC 7396 JSON Merge Patch. Use when applying a JSON Patch or a merge patch. Triggers: JSON Patch, RFC 6902, RFC 7396.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# JavaScript Object Notation (JSON) Patch

JavaScript Object Notation (JSON) Patch

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when applying a JSON Patch or a merge patch.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: RFC 6902 JavaScript Object Notation (JSON) Patch (default); RFC 7396 JSON Merge Patch (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **RFC 6902 § 4.** "Operation objects MUST have exactly one "op" member, whose value indicates the operation to perform."
2. **RFC 6902 § 4.** "Its value MUST be one of "add", "remove", "replace", "move", "copy", or "test"; other values are errors."
3. **RFC 6902 § 4.** "Additionally, operation objects MUST have exactly one "path" member."
4. **RFC 6902 § 4.** "Members that are not explicitly defined for the operation in question MUST be ignored (i.e., the operation will complete as if the undefined member did not appear in the object)."
5. **RFC 6902 § 4.1.** "The specified index MUST NOT be greater than the number of elements in the array."
6. **RFC 6902 § 4.2.** "The target location MUST exist for the operation to be successful."
7. **RFC 6902 § 4.4.** "The "from" location MUST NOT be a proper prefix of the "path" location; i.e., a location cannot be moved into one of its children."
8. **RFC 6902 § 4.6.** "The target location MUST be equal to the "value" value for the operation to be considered successful."
9. **RFC 6902 § 5.** "If a normative requirement is violated by a JSON Patch document, or if an operation is not successful, evaluation of the JSON Patch document SHOULD terminate and application of the entire patch document SHALL NOT be deemed successful."
10. **RFC 7396 § 1.** "Null values in the merge patch are given special meaning to indicate the removal of existing values in the target."
11. **RFC 7396 § 2.** "If the patch is anything other than an object, the result will always be to replace the entire target with the entire patch."

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

- [RFC 6902 JavaScript Object Notation (JSON) Patch](https://www.rfc-editor.org/rfc/rfc6902.html): PROPOSED STANDARD, RFC 6902 (PROPOSED STANDARD, April 2013), checked 2026-10-06.
- [RFC 7396 JSON Merge Patch](https://www.rfc-editor.org/rfc/rfc7396.html): PROPOSED STANDARD, RFC 7396 (PROPOSED STANDARD, October 20), checked 2026-10-06.
