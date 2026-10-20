---
name: uri
description: >-
  URI (RFC 3986): parse, resolve and normalize URIs, plus IRIs, URNs and URI Templates. Covers RFC 3986 Uniform Resource Identifier (URI): Generic Syntax, RFC 3987 Internationalized Resource Identifiers (IRIs), RFC 8141 Uniform Resource Names (URNs), RFC 6570 URI Template. Use when parsing URIs, IRIs, URNs or URI templates. Triggers: URI, IRI, URN, URI Template.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# Uniform Resource Identifier (URI): Generic Syntax

Uniform Resource Identifier (URI): Generic Syntax

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when parsing URIs, IRIs, URNs or URI templates.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: RFC 3986 Uniform Resource Identifier (URI): Generic Syntax (default); RFC 3987 Internationalized Resource Identifiers (IRIs) (default); RFC 8141 Uniform Resource Names (URNs) (default); RFC 6570 URI Template (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **RFC 3986 § 2.2.** "If data for a URI component would conflict with a reserved character's purpose as a delimiter, then the conflicting data must be percent-encoded before the URI is formed."
2. **RFC 3986 § 2.4.** "Implementations must not percent-encode or decode the same string more than once, as decoding an already decoded string might lead to misinterpreting a percent data octet as the beginning of a percent-encoding, or vice versa in the case of percent-encoding an already percent-encoded string."
3. **RFC 3986 § 3.** "When authority is present, the path must either be empty or begin with a slash ("/") character."
4. **RFC 3986 § 5.1.** "A base URI must be established by the parser prior to parsing URI references that might be relative."
5. **RFC 3986 § 6.1.** "In testing for equivalence, applications should not directly compare relative references; the references should be converted to their respective target URIs before comparison."
6. **RFC 3986 § 6.2.2.1.** "When a URI uses components of the generic syntax, the component syntax equivalence rules always apply; namely, that the scheme and host are case-insensitive and therefore should be normalized to lowercase."
7. **RFC 3987 § 3.2.** "Conversions from URIs to IRIs MUST NOT use any character encoding other than UTF-8 in steps 3 and 4, even if it might be possible to guess from the context that another character encoding than UTF-8 was used in the URI."
8. **RFC 3987 § 5.1.** "Applications using IRIs as identity tokens with no relationship to a protocol MUST use the Simple String Comparison (see section 5.3.1)."
9. **RFC 8141 § 3.1.** "If an r-component, q-component, or f-component (or any combination thereof) is included in a URN, it MUST be ignored for purposes of determining URN-equivalence."
10. **RFC 6570 § 1.6.** "Likewise, when non-ASCII data that represents readable strings is pct-encoded for use in a URI reference, a template processor MUST first encode the string as UTF-8 [RFC3629] and then pct-encode any octets that are not allowed in a URI reference."

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

- [RFC 3986 Uniform Resource Identifier (URI): Generic Syntax](https://www.rfc-editor.org/rfc/rfc3986.html): INTERNET STANDARD, RFC 3986 (INTERNET STANDARD, January 20), checked 2026-10-06.
- [RFC 3987 Internationalized Resource Identifiers (IRIs)](https://www.rfc-editor.org/rfc/rfc3987.html): PROPOSED STANDARD, RFC 3987 (PROPOSED STANDARD, January 20), checked 2026-10-06.
- [RFC 8141 Uniform Resource Names (URNs)](https://www.rfc-editor.org/rfc/rfc8141.html): PROPOSED STANDARD, RFC 8141 (PROPOSED STANDARD, April 2017), checked 2026-10-06.
- [RFC 6570 URI Template](https://www.rfc-editor.org/rfc/rfc6570.html): PROPOSED STANDARD, RFC 6570 (PROPOSED STANDARD, March 2012), checked 2026-10-06.
