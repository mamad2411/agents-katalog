---
name: jsonpath
description: >-
  JSONPath: Query Expressions for JSON: JSONPath defines a string syntax for selecting and extracting JSON (RFC 8259) values from within a given JSON value. Covers RFC 9535 JSONPath: Query Expressions for JSON. Use when querying JSON with JSONPath. Triggers: JSONPath, RFC 9535.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# JSONPath: Query Expressions for JSON

JSONPath defines a string syntax for selecting and extracting JSON (RFC 8259) values from within a given JSON value. ¶

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when querying JSON with JSONPath.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: RFC 9535 JSONPath: Query Expressions for JSON (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **RFC 9535 § 2.1.** "A query MUST be encoded using UTF-8."
2. **RFC 9535 § 2.1.** "Integer numbers in the JSONPath query that are relevant to the JSONPath processing (e.g., index values and steps) MUST be within the range of exact integer values defined in Internet JSON (I-JSON) (see Section 2.2 of [RFC7493]), namely within the interval [-(2^53)+1, (2^53)-1]."
3. **RFC 9535 § 2.1.** "A JSONPath implementation MUST raise an error for any query that is not well-formed and valid."
4. **RFC 9535 § 2.1.** "Specifically, if a valid JSONPath query is evaluated against a structured value whose size is too large to process the query correctly (for instance, requiring the processing of numbers that fall outside the range of exact values), the implementation MUST provide an indication of overflow."
5. **RFC 9535 § 2.1.2.** "A syntactically valid segment MUST NOT produce errors when executing the query."
6. **RFC 9535 § 2.2.1.** "Every JSONPath query (except those inside filter expressions; see Section 2.3.5) MUST begin with the root identifier $."
7. **RFC 9535 § 2.3.1.2.** "Two strings MUST be considered equal if and only if they are identical sequences of Unicode scalar values."
8. **RFC 9535 § 2.3.1.2.** "In other words, normalization operations MUST NOT be applied to either the member name string M from the JSONPath or the member name strings in the JSON prior to comparison."
9. **RFC 9535 § 2.4.** "A function extension MUST be defined such that its evaluation is free of side effects, i.e., all possible orders of evaluation and choices of short-circuiting or full evaluation of an expression containing it MUST lead to the same result."
10. **RFC 9535 § 2.4.** "Any function expressions in a query must be well-formed (by conforming to the above ABNF) and well-typed; otherwise, the JSONPath implementation MUST raise an error (see Section 2.1)."

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

- [RFC 9535 JSONPath: Query Expressions for JSON](https://www.rfc-editor.org/rfc/rfc9535.html): PROPOSED STANDARD, RFC 9535 (PROPOSED STANDARD, February 2), checked 2026-10-06.
