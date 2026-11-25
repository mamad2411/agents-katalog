---
name: media-fragments
description: >-
  Media Fragments: This document describes the Media Fragments 1.0 (basic) specification. Covers Media Fragments URI 1.0 (basic). Use when addressing a fragment of a media resource. Triggers: Media Fragments.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Media Fragments

This document describes the Media Fragments 1.0 (basic) specification. It specifies the syntax for constructing media fragment URIs and explains how to handle them when used over the HTTP protocol. The syntax is based on the specification of particular name-value pairs that can be used in URI fragment and URI query requests to restrict a media resource to a certain fragment. The Media Fragment WG has no authority to update registries of all targeted media types. We recommend media type owners to harmonize their existing schemes with the ones proposed in this document and update or add the fragment semantics specification to their media type registration.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when addressing a fragment of a media resource.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Media Fragments URI 1.0 (basic) (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **2.1 Terminology.** "The keywords MUST , MUST NOT , SHOULD and SHOULD NOT are to be interpreted as defined in RFC 2119 ."
2. **2.2.1 URI Fragments.** "The registration of URI fragment construction rules, as expressed in Section 4.11 of RFC 4288 , is a SHOULD-requirement."
3. **6.2 Errors detectable based on the URI syntax.** "More specifically, the user agent SHOULD ignore name-value pairs causing errors detectable based on the URI syntax."
4. **6.2.1 Errors on the general URI level.** "Unknown dimensions SHOULD be ignored by the user agent."
5. **6.2.1 Errors on the general URI level.** "t=10 in #t=2&t=10) is interpreted and all previous occurrences (valid or invalid) SHOULD be ignored by the user agent."
6. **6.2.2 Errors on the temporal dimension.** "Invalid temporal fragments SHOULD be ignored by the user agent."
7. **6.2.3 Errors on the spatial dimension.** "Invalid spatial fragments SHOULD be ignored by the user agent."
8. **6.3.1 Errors on the general level.** "If the user agent knows the mime type, it is able to detect non-existent dimensions and SHOULD ignore them."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the heading it came from.
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

- [Media Fragments URI 1.0 (basic)](https://www.w3.org/TR/media-frags/): Recommendation, media-frags REC-media-frags-20120925 (Recommendation, 2012-09-25), checked 2026-10-06.
