---
name: well-known-uris
description: >-
  Well-known URIs (RFC 8615): publish and register resources under /.well-known/. Covers RFC 8615 Well-Known Uniform Resource Identifiers (URIs). Use when publishing a /.well-known/ resource. Triggers: well-known, RFC 8615.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# Well-Known Uniform Resource Identifiers (URIs)

Well-Known Uniform Resource Identifiers (URIs)

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when publishing a /.well-known/ resource.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: RFC 8615 Well-Known Uniform Resource Identifiers (URIs) (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **RFC 8615 § 3.** "A well-known URI is a URI [RFC3986] whose path component begins with the characters "/.well-known/", provided that the scheme is explicitly defined to support well-known URIs."
2. **RFC 8615 § 1.** "Well-known URIs can also be used with other URI schemes, but only when those schemes' definitions explicitly allow it."
3. **RFC 8615 § 3.** "Applications that wish to mint new well-known URIs MUST register them, following the procedures in Section 5.1, subject to the following requirements."
4. **RFC 8615 § 3.** "Registered names MUST conform to the "segment-nz" production in [RFC3986]."
5. **RFC 8615 § 3.** "Registered names for a specific application SHOULD be correspondingly precise; "squatting" on generic terms is not encouraged."
6. **RFC 8615 § 3.** "Typically, applications will use the default port for the given scheme; if an alternative port is used, it MUST be explicitly specified by the application in question."
7. **RFC 8615 § 3.** "Well-known URIs are rooted in the top of the path's hierarchy; they are not well-known by definition in other parts of the path."
8. **RFC 8615 § 4.1.** "Because well-known locations effectively represent the entire origin, server operators should appropriately control the ability to write to them."

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

- [RFC 8615 Well-Known Uniform Resource Identifiers (URIs)](https://www.rfc-editor.org/rfc/rfc8615.html): PROPOSED STANDARD, RFC 8615 (PROPOSED STANDARD, May 2019), checked 2026-10-06.
